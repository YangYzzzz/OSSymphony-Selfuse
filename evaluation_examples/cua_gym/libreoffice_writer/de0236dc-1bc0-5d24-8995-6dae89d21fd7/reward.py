"""
Reward Script: Mark 20 key economics terms as index entries and generate a two-column alphabetical index.
Task ID: writer_mt_079
Domain: libreoffice_writer
Scoring:
  Component 1 (0.40): All 20 expected terms have XE index entry fields
  Component 2 (0.20): Terms have multiple XE occurrences (marked at each appearance)
  Component 3 (0.25): INDEX field present with 2-column format specification
  Component 4 (0.15): "Alphabetical Index" heading exists at end of document
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_079'

# The 20 key terms from the task specification
EXPECTED_TERMS = [
    'inflation', 'deflation', 'GDP', 'fiscal policy', 'monetary policy',
    'supply', 'demand', 'equilibrium', 'elasticity', 'monopoly',
    'oligopoly', 'tariff', 'subsidy', 'recession', 'depression',
    'interest rate', 'exchange rate', 'trade deficit', 'capital gains', 'amortization'
]


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_writer", "libreoffice_calc", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
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

    body = doc.element.body
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # ---------------------------------------------------------------
    # Collect all XE (index entry) fields from the document
    # ---------------------------------------------------------------
    from collections import Counter
    xe_term_counts = Counter()
    try:
        instr_fields = body.findall('.//w:instrText', ns)
        for field in instr_fields:
            if field.text and 'XE' in field.text:
                # Extract the term from XE "term" format
                text = field.text.strip()
                # Parse: XE "term name"
                import re
                match = re.search(r'XE\s+"([^"]+)"', text)
                if match:
                    term = match.group(1).strip().lower()
                    xe_term_counts[term] += 1
    except Exception as e:
        print(f"ERROR: Failed to parse XE fields: {e}")

    # ---------------------------------------------------------------
    # Component 1: All 20 expected terms have XE index entry fields (0.40 points)
    # This FAILS on initial (0 XE fields) and PASSES on golden (20 unique terms)
    # ---------------------------------------------------------------
    try:
        found_terms = set(xe_term_counts.keys())
        expected_lower = {t.lower() for t in EXPECTED_TERMS}
        matched_terms = found_terms & expected_lower
        match_ratio = len(matched_terms) / len(expected_lower)

        if match_ratio >= 1.0:
            print(f"PASS: Component 1 - All 20 terms have XE entries ({len(matched_terms)}/20) (0.40 pts)")
            total_score += 0.40
        elif match_ratio > 0:
            partial = round(0.40 * match_ratio, 2)
            missing = expected_lower - found_terms
            print(f"PARTIAL: Component 1 - {len(matched_terms)}/20 terms have XE entries ({partial} pts)")
            print(f"  Missing terms: {sorted(missing)}")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No XE index entries found for any of the 20 expected terms")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # ---------------------------------------------------------------
    # Component 2: Terms have multiple XE occurrences (0.20 points)
    # Task says "each occurrence" should be marked. Multiple occurrences
    # per term indicate the agent marked them throughout the text.
    # This FAILS on initial (0 XE fields) and PASSES on golden (263 total).
    # ---------------------------------------------------------------
    try:
        if len(xe_term_counts) == 0:
            print("FAIL: Component 2 - No XE entries found, cannot check multiple occurrences")
        else:
            # Count how many of the matched terms have more than 1 occurrence
            multi_terms = sum(1 for t in expected_lower if xe_term_counts.get(t, 0) > 1)
            multi_ratio = multi_terms / len(expected_lower)

            if multi_ratio >= 0.8:
                print(f"PASS: Component 2 - {multi_terms}/20 terms have multiple XE occurrences (0.20 pts)")
                total_score += 0.20
            elif multi_ratio > 0:
                partial = round(0.20 * multi_ratio, 2)
                print(f"PARTIAL: Component 2 - {multi_terms}/20 terms have multiple occurrences ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 - No terms have multiple XE occurrences")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # ---------------------------------------------------------------
    # Component 3: INDEX field with 2-column format (0.25 points)
    # The golden doc has an INDEX field with \c "2" specifying 2 columns.
    # This FAILS on initial (no INDEX field) and PASSES on golden.
    # ---------------------------------------------------------------
    try:
        import re
        index_found = False
        two_col_index = False

        instr_fields = body.findall('.//w:instrText', ns)
        for field in instr_fields:
            if field.text and 'INDEX' in field.text:
                index_found = True
                # Check for 2-column specification: \c "2"
                if re.search(r'\\c\s*"2"', field.text):
                    two_col_index = True
                    break

        if two_col_index:
            print(f"PASS: Component 3 - INDEX field with 2-column format found (0.25 pts)")
            total_score += 0.25
        elif index_found:
            # INDEX exists but not 2-column
            print(f"PARTIAL: Component 3 - INDEX field found but not 2-column format (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 - No INDEX field found in document")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # ---------------------------------------------------------------
    # Component 4: "Alphabetical Index" heading at end of document (0.15 points)
    # Golden doc has a Heading 1 with "Alphabetical Index" near the end.
    # This FAILS on initial (no such heading) and PASSES on golden.
    # ---------------------------------------------------------------
    try:
        # Check last 10 paragraphs for the heading
        last_paras = doc.paragraphs[-10:]
        heading_found = False
        for para in last_paras:
            text_lower = para.text.strip().lower()
            if 'index' in text_lower and para.style.name.startswith('Heading'):
                heading_found = True
                print(f"  Found heading: '{para.text}' (style: {para.style.name})")
                break

        if heading_found:
            print(f"PASS: Component 4 - 'Alphabetical Index' heading found at end of doc (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 - No index heading found in the last 10 paragraphs")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # ---------------------------------------------------------------
    # Final score
    # ---------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: persist app state then verify
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
