"""
Reward Script: Create index of key terms in User_Manual.docx
Task ID: writer_pd_020
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35) - 8 XE index entry fields present
  Component 2 (0.25) - INDEX field present in document
  Component 3 (0.40) - Index content lists all 8 terms with correct page numbers, alphabetically
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_pd_020'

# Expected index entries: term -> page number
EXPECTED_ENTRIES = {
    'installation': '3',
    'configuration': '5',
    'authentication': '7',
    'dashboard': '8',
    'reporting': '11',
    'backup': '14',
    'troubleshooting': '17',
    'API integration': '19',
}

# Expected alphabetical order
EXPECTED_ORDER = [
    'API integration',
    'authentication',
    'backup',
    'configuration',
    'dashboard',
    'installation',
    'reporting',
    'troubleshooting',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = doc.element.body

    # Component 1: XE index entry fields for all 8 terms (0.35 points)
    # Each XE field is an instrText containing ' XE "term" '
    try:
        all_instr = body.findall('.//w:instrText', ns)
        found_xe_terms = set()
        for instr in all_instr:
            if instr.text and 'XE' in instr.text:
                # Extract term from XE field: ' XE "term" '
                text = instr.text.strip()
                # Parse between quotes
                start = text.find('"')
                end = text.rfind('"')
                if start != -1 and end > start:
                    term = text[start + 1:end]
                    found_xe_terms.add(term.lower())

        # Check how many of the 8 expected terms have XE entries
        expected_lower = {t.lower() for t in EXPECTED_ENTRIES.keys()}
        matched = expected_lower & found_xe_terms
        xe_ratio = len(matched) / len(expected_lower)

        if xe_ratio >= 1.0:
            print(f"PASS: Component 1 - All 8 XE index entries found: {sorted(found_xe_terms)} (0.35 pts)")
            total_score += 0.35
        elif xe_ratio > 0:
            partial = round(0.35 * xe_ratio, 2)
            missing = expected_lower - found_xe_terms
            print(f"PARTIAL: Component 1 - {len(matched)}/8 XE entries found, missing: {missing} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No XE index entries found (expected 8)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: INDEX field exists in document (0.25 points)
    # The INDEX field generates the alphabetical index
    try:
        index_field_found = False
        for instr in all_instr:
            if instr.text and 'INDEX' in instr.text.upper() and 'XE' not in instr.text.upper():
                index_field_found = True
                print(f"PASS: Component 2 - INDEX field found: {repr(instr.text.strip())} (0.25 pts)")
                break

        if index_field_found:
            total_score += 0.25
        else:
            print("FAIL: Component 2 - No INDEX field found in document")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Index content contains all 8 terms with correct page numbers (0.40 points)
    # The cached index text appears between fldChar separate and end, after the INDEX instrText
    try:
        # Strategy: find the paragraph containing the INDEX field, then extract the
        # cached text content from the runs between fldChar separate and fldChar end
        index_text = ''
        paragraphs = body.findall('.//w:p', ns)
        for para in paragraphs:
            runs = para.findall('.//w:r', ns)
            # Check if this paragraph has an INDEX instrText
            has_index_field = False
            for run in runs:
                instr_el = run.find('w:instrText', ns)
                if instr_el is not None and instr_el.text and 'INDEX' in instr_el.text.upper() and 'XE' not in instr_el.text.upper():
                    has_index_field = True
                    break

            if has_index_field:
                # Extract cached text: runs after fldChar separate and before fldChar end
                in_result = False
                for run in runs:
                    fld_char = run.find('w:fldChar', ns)
                    if fld_char is not None:
                        fld_type = fld_char.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fldCharType')
                        if fld_type == 'separate':
                            in_result = True
                            continue
                        elif fld_type == 'end':
                            in_result = False
                            continue
                    if in_result:
                        t_el = run.find('w:t', ns)
                        if t_el is not None and t_el.text:
                            index_text += t_el.text

                break  # found the INDEX paragraph

        if not index_text.strip():
            print("FAIL: Component 3 - No cached index content found")
        else:
            # Parse index entries from cached text
            # Format: "term, page\nterm, page\n..."
            lines = [line.strip() for line in index_text.strip().split('\n') if line.strip()]
            print(f"  Index content lines: {lines}")

            # Check each expected term and page number
            terms_correct = 0
            terms_present = 0
            for expected_term, expected_page in EXPECTED_ENTRIES.items():
                found_match = False
                for line in lines:
                    # Check if line contains the term (case-insensitive) and page number
                    if expected_term.lower() in line.lower():
                        terms_present += 1
                        if expected_page in line:
                            terms_correct += 1
                            found_match = True
                            break
                        else:
                            print(f"  PARTIAL: Term '{expected_term}' found but page number mismatch in: {line}")
                            found_match = True
                            break
                if not found_match:
                    print(f"  MISSING: Term '{expected_term}' not found in index content")

            # Score: weight by terms correct (with page) and terms present (without page)
            if terms_correct == 8:
                print(f"PASS: Component 3 - All 8 terms with correct page numbers in index (0.40 pts)")
                total_score += 0.40
            elif terms_correct > 0:
                # Partial: proportion of correct entries
                partial = round(0.40 * (terms_correct / 8), 2)
                print(f"PARTIAL: Component 3 - {terms_correct}/8 terms with correct pages ({partial} pts)")
                total_score += partial
            elif terms_present > 0:
                # Some terms found but pages wrong
                partial = round(0.40 * (terms_present / 8) * 0.5, 2)
                print(f"PARTIAL: Component 3 - {terms_present}/8 terms found but pages incorrect ({partial} pts)")
                total_score += partial
            else:
                print("FAIL: Component 3 - No expected terms found in index content")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
