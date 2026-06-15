"""
Reward Script: Insert 'CONFIDENTIAL' at document beginning in red bold 16pt centered text
Task ID: writer_edit_016
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): First paragraph text is 'CONFIDENTIAL'
  Component 2 (0.30): 'CONFIDENTIAL' paragraph has bold=True, size=16pt, color=#FF0000, alignment=CENTER
  Component 3 (0.20): Second paragraph is an empty blank line after 'CONFIDENTIAL'
  Component 4 (0.20): Original 'Service Agreement' heading is preserved at the correct position
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_edit_016'

FILE_PATH = '/home/user/Desktop/contract_draft.docx'

# Optional persistence: send Ctrl+S for LibreOffice saves before reading
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


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paras = doc.paragraphs
    if len(paras) == 0:
        print("CRITICAL: Document has no paragraphs")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: First paragraph text is exactly 'CONFIDENTIAL' (0.30 points)
    # This FAILS on initial (first para is 'Service Agreement'), PASSES on golden
    try:
        first_para_text = paras[0].text.strip()
        if first_para_text == 'CONFIDENTIAL':
            print(f"PASS: Component 1 — First paragraph text is 'CONFIDENTIAL' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Expected first paragraph 'CONFIDENTIAL', found: {repr(first_para_text)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'CONFIDENTIAL' paragraph is bold, 16pt, red (#FF0000), center-aligned (0.30 points)
    # This FAILS on initial (first para is 'Service Agreement' with no special formatting), PASSES on golden
    try:
        first_para = paras[0]
        runs = first_para.runs

        # Check alignment
        alignment_ok = first_para.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER

        # Check run-level formatting (bold, size, color)
        bold_ok = False
        size_ok = False
        color_ok = False

        for run in runs:
            if run.text.strip():
                # Bold check
                if run.bold is True or run.font.bold is True:
                    bold_ok = True
                # Size check: 16pt = 16 * 12700 = 203200 EMUs
                if run.font.size is not None and abs(run.font.size.pt - 16.0) < 0.5:
                    size_ok = True
                # Color check: #FF0000 red
                # RGBColor str() returns hex string like 'FF0000'
                try:
                    from docx.oxml.ns import qn as _qn
                    color_type = run.font.color.type
                    if color_type is not None:
                        rgb_str = str(run.font.color.rgb).upper()
                        if rgb_str == 'FF0000':
                            color_ok = True
                except Exception:
                    pass

        formatting_ok = alignment_ok and bold_ok and size_ok and color_ok

        if formatting_ok:
            print(f"PASS: Component 2 — CONFIDENTIAL is bold={bold_ok}, 16pt={size_ok}, red={color_ok}, center={alignment_ok} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Formatting check failed: bold={bold_ok}, 16pt={size_ok}, red={color_ok}, center={alignment_ok}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Second paragraph is an empty blank line (0.20 points)
    # This FAILS on initial (second para is original contract text), PASSES on golden
    try:
        if len(paras) > 1:
            second_para_text = paras[1].text.strip()
            if second_para_text == '':
                print(f"PASS: Component 3 — Second paragraph is a blank line after CONFIDENTIAL (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — Expected blank line as second paragraph, found: {repr(second_para_text[:60])}")
        else:
            print("FAIL: Component 3 — Document has fewer than 2 paragraphs")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Original 'Service Agreement' heading is preserved at Para index 2 (0.20 points)
    # This FAILS on initial (Para 0 is 'Service Agreement' not Para 2), PASSES on golden
    try:
        if len(paras) > 2:
            third_para_text = paras[2].text.strip()
            if third_para_text == 'Service Agreement':
                print(f"PASS: Component 4 — 'Service Agreement' heading preserved at paragraph index 2 (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Expected 'Service Agreement' at index 2, found: {repr(third_para_text[:60])}")
        else:
            print("FAIL: Component 4 — Document has fewer than 3 paragraphs")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()

if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
