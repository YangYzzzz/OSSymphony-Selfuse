"""
Reward Script: Insert a 'File Name' field in the footer
Task ID: writer_tm_069
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Footer contains a field code structure (fldChar begin/separate/end)
  Component 2 (0.3): The field is a FILENAME field (instrText contains 'FILENAME')
  Component 3 (0.3): The cached/displayed value shows the correct filename 'Budget_2026.docx'
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_tm_069'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that the footer contains a FILENAME field displaying 'Budget_2026.docx'.
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

    # Get footer from section 0
    try:
        section = doc.sections[0]
        footer = section.footer
        footer_paras = footer.paragraphs
    except Exception as e:
        print(f"CRITICAL: Cannot access footer: {e}")
        print("REWARD: 0.0")
        return 0.0

    # We need to parse footer XML to check for field codes
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Component 1: Footer contains a field code structure (0.4 points)
    # A field code has fldChar elements with begin, separate, and end types
    try:
        has_field = False
        for para in footer_paras:
            fld_chars = para._element.findall('.//w:fldChar', ns)
            fld_types = [fc.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fldCharType')
                         for fc in fld_chars]
            if 'begin' in fld_types and 'end' in fld_types:
                has_field = True
                break

        if has_field:
            print(f"PASS: Component 1 — Footer contains a field code structure (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No field code structure found in footer")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The field is a FILENAME field (0.3 points)
    # instrText should contain 'FILENAME' (not 'PAGE', 'DATE', etc.)
    try:
        has_filename_field = False
        for para in footer_paras:
            instr_texts = para._element.findall('.//w:instrText', ns)
            for instr in instr_texts:
                if instr.text and 'FILENAME' in instr.text.upper():
                    has_filename_field = True
                    break
            if has_filename_field:
                break

        if has_filename_field:
            print(f"PASS: Component 2 — FILENAME field found in footer (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No FILENAME instrText found in footer")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The displayed/cached value shows 'Budget_2026.docx' (0.3 points)
    # The footer text (para.text) should contain the filename
    try:
        footer_text = ''.join(para.text for para in footer_paras).strip()
        expected_name = 'Budget_2026.docx'

        if expected_name in footer_text:
            print(f"PASS: Component 3 — Footer displays '{expected_name}' (0.3 pts)")
            total_score += 0.3
        elif 'Budget_2026' in footer_text:
            # Partial: filename without extension still acceptable (some field configs)
            print(f"PASS: Component 3 — Footer displays 'Budget_2026' (partial match, 0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Footer text is '{footer_text}', expected '{expected_name}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/Documents/{TASK_ID[:-4]}_2026.docx'
# The file is Budget_2026.docx in Documents
file_path = f'{WORKDIR}/Documents/Budget_2026.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
