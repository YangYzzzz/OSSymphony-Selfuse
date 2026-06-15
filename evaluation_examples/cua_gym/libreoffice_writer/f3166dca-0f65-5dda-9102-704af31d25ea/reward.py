"""
Reward Script: Insert page count field in footer for 'Page X of Y' format
Task ID: writer_acad_067
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Footer contains 'Page ' text prefix before PAGE field
  Component 2 (0.3): Footer contains ' of ' text between PAGE and NUMPAGES fields
  Component 3 (0.4): Footer contains a NUMPAGES (page count) field code
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_067'


def persist_app_state(domain):
    """Save any unsaved GUI edits before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            import time
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    We check the footer XML for:
    1. 'Page ' text before the PAGE field
    2. ' of ' text between PAGE and NUMPAGES fields
    3. A NUMPAGES field code (page count)

    Initial state has only a bare PAGE field (no text, no NUMPAGES).
    Golden state has 'Page ' + PAGE + ' of ' + NUMPAGES.
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get footer from section 0
    try:
        section = doc.sections[0]
        footer = section.footer
    except Exception as e:
        print(f"CRITICAL: Cannot access footer: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse footer XML to extract structure
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    try:
        footer_elem = footer._element
        # Get all child elements of the first paragraph in footer
        footer_paras = footer_elem.findall('.//w:p', ns)
        if not footer_paras:
            print("FAIL: No paragraphs found in footer")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        # Analyze the footer structure by walking through runs in order
        # We need to find: text "Page " -> PAGE field -> text " of " -> NUMPAGES field
        para_elem = footer_paras[0]
        runs = para_elem.findall('w:r', ns)

        # Collect sequence of elements: text nodes, PAGE fields, NUMPAGES fields
        sequence = []  # list of tuples: ('text', value) or ('field', field_name)

        i = 0
        while i < len(runs):
            run = runs[i]
            # Check for text
            t_elem = run.find('w:t', ns)
            if t_elem is not None and t_elem.text:
                sequence.append(('text', t_elem.text))
                i += 1
                continue

            # Check for field begin
            fld_char = run.find('w:fldChar', ns)
            if fld_char is not None and fld_char.get(f'{{{ns["w"]}}}fldCharType') == 'begin':
                # Next run should have instrText
                if i + 1 < len(runs):
                    instr = runs[i + 1].find('w:instrText', ns)
                    if instr is not None and instr.text:
                        field_name = instr.text.strip()
                        sequence.append(('field', field_name))
                # Skip to after end fldChar
                # Find the matching end
                j = i + 1
                while j < len(runs):
                    fc = runs[j].find('w:fldChar', ns)
                    if fc is not None and fc.get(f'{{{ns["w"]}}}fldCharType') == 'end':
                        break
                    j += 1
                i = j + 1
                continue

            i += 1

        print(f"INFO: Footer structure sequence: {sequence}")

    except Exception as e:
        print(f"ERROR: Failed to parse footer XML: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 1: Footer contains 'Page ' text before PAGE field (0.3 points)
    # This must FAIL on initial (initial has no text, just bare PAGE field)
    try:
        has_page_prefix = False
        for idx, (etype, val) in enumerate(sequence):
            if etype == 'text' and 'Page' in val:
                # Check that a PAGE field follows somewhere after
                for later_idx in range(idx + 1, len(sequence)):
                    if sequence[later_idx] == ('field', 'PAGE'):
                        has_page_prefix = True
                        break
                break

        if has_page_prefix:
            print(f"PASS: Component 1 -- 'Page ' text prefix found before PAGE field (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- 'Page ' text prefix not found before PAGE field")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Footer contains ' of ' text between PAGE and NUMPAGES fields (0.3 points)
    # This must FAIL on initial (initial has no ' of ' text and no NUMPAGES)
    try:
        has_of_between = False
        # Find PAGE field index
        page_idx = None
        numpages_idx = None
        for idx, (etype, val) in enumerate(sequence):
            if etype == 'field' and val == 'PAGE':
                page_idx = idx
            if etype == 'field' and val == 'NUMPAGES':
                numpages_idx = idx

        if page_idx is not None and numpages_idx is not None and numpages_idx > page_idx:
            # Check for ' of ' text between them
            for mid_idx in range(page_idx + 1, numpages_idx):
                if sequence[mid_idx][0] == 'text' and 'of' in sequence[mid_idx][1].lower():
                    has_of_between = True
                    break

        if has_of_between:
            print(f"PASS: Component 2 -- ' of ' text found between PAGE and NUMPAGES fields (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- ' of ' text not found between PAGE and NUMPAGES fields")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Footer contains a NUMPAGES field code (0.4 points)
    # This must FAIL on initial (initial has only PAGE, no NUMPAGES)
    try:
        has_numpages = False
        instr_texts = footer_elem.findall('.//w:instrText', ns)
        for instr in instr_texts:
            if instr.text and 'NUMPAGES' in instr.text.upper():
                has_numpages = True
                break

        if has_numpages:
            print(f"PASS: Component 3 -- NUMPAGES field code found in footer (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 3 -- NUMPAGES field code not found in footer")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
