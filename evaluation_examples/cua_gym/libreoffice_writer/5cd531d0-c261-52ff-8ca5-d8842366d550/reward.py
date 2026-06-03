"""
Reward Script: Two-column layout for second page of newsletter
Task ID: writer_biz_029
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.6): Section 1 (page 2+) has exactly 2 columns
  - Component 2 (0.4): Section 1 column gap is approximately 0.5 cm
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_029'


def persist_app_state(domain):
    """Send Ctrl+S to save any unsaved changes in LibreOffice."""
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
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Create a two-column layout for the second page of the newsletter,
    keeping the first page as a single column with the newsletter title.
    Ground truth: Section 0 = single column. Section 1 = 2 columns with 0.5 cm gap.
    """
    total_score = 0.0

    # Load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: document must have at least 2 sections
    if len(doc.sections) < 2:
        print(f"FAIL: Document has only {len(doc.sections)} section(s), need at least 2 for page layout change")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Section 1 (page 2 onward) has exactly 2 columns (0.6 points)
    # This is the core task requirement. In the initial state, section 1 has no
    # w:num attribute (default = 1 column). In golden, it should be 2.
    try:
        sec1 = doc.sections[1]
        sectPr1 = sec1._sectPr
        cols1 = sectPr1.find(qn('w:cols'))

        if cols1 is not None:
            num_str = cols1.get(qn('w:num'))
            if num_str is not None:
                num_cols = int(num_str)
            else:
                num_cols = 1  # default when w:num is absent
        else:
            num_cols = 1  # no cols element means single column

        if num_cols == 2:
            print(f"PASS: Component 1 -- Section 1 has 2 columns (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 -- Section 1 has {num_cols} column(s), expected 2")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Section 1 column gap is approximately 0.5 cm (0.4 points)
    # 0.5 cm = 283 twips (OOXML spec) OR 180000 EMU (if written in EMU).
    # We accept either interpretation with a tolerance band.
    # Initial state has space=720 (0.5 inch default), golden has ~0.5 cm gap.
    try:
        sec1 = doc.sections[1]
        sectPr1 = sec1._sectPr
        cols1 = sectPr1.find(qn('w:cols'))

        if cols1 is not None:
            space_str = cols1.get(qn('w:space'))
            if space_str is not None:
                space_val = int(space_str)
            else:
                space_val = None

            if space_val is not None:
                # Accept 0.5 cm in various unit interpretations:
                # - EMU: 0.5 cm = 180000 EMU (tolerance: 170000-190000)
                # - Twips: 0.5 cm = 283 twips (tolerance: 270-300)
                # Also accept if it's clearly NOT the default 720 twips (0.5 inch)
                is_emu_match = 170000 <= space_val <= 190000  # ~0.5 cm in EMU
                is_twip_match = 270 <= space_val <= 300       # ~0.5 cm in twips

                if is_emu_match or is_twip_match:
                    print(f"PASS: Component 2 -- Column gap is ~0.5 cm (raw value: {space_val}) (0.4 pts)")
                    total_score += 0.4
                else:
                    # Check if it's at least different from the default 720 (which is 0.5 inch)
                    # and the number of columns is 2 (which means a gap was set)
                    print(f"FAIL: Component 2 -- Column gap value {space_val} does not match ~0.5 cm (expected ~283 twips or ~180000 EMU)")
            else:
                print(f"FAIL: Component 2 -- No space attribute on cols element")
        else:
            print(f"FAIL: Component 2 -- No cols element in section 1")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
