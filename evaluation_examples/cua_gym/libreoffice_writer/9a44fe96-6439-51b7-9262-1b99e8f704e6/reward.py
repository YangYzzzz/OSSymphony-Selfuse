"""
Reward Script: Modify Heading 2 style to Calibri 12pt bold italic, color #333333, with bottom border
Task ID: writer_biz_045
Domain: libreoffice_writer
Scoring:
  Component 1 — Font size is 12pt (0.25)
  Component 2 — Font is bold AND italic (0.20)
  Component 3 — Font color is #333333 (dark gray) (0.25)
  Component 4 — Bottom paragraph border exists (thin line) (0.30)

Note: Font name (Calibri) is NOT scored because the initial Heading 2 style
already inherits Calibri via the majorHAnsi theme. It would pass on both envs.
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_045'


def persist_app_state(domain: str):
    """Send Ctrl+S to save any unsaved GUI edits."""
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
    Verify that the Heading 2 style has been modified per task requirements.
    All checks are on the STYLE definition (not individual paragraph runs),
    since the task asks to modify the style itself.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.shared import Pt, RGBColor
        from docx.oxml.ns import qn
    except ImportError as e:
        print(f"CRITICAL: Missing library: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate the Heading 2 paragraph style
    heading2_style = None
    for style in doc.styles:
        if style.name == 'Heading 2' and style.type == 1:  # PARAGRAPH type
            heading2_style = style
            break

    if heading2_style is None:
        print("CRITICAL: Heading 2 paragraph style not found in document")
        print("REWARD: 0.0")
        return 0.0

    font = heading2_style.font
    elem = heading2_style.element

    # Component 1: Font size is 12pt (0.25 points)
    # Initial: 13.0pt. Golden: 12.0pt
    try:
        font_size = font.size
        if font_size is not None:
            size_pt = font_size.pt
            if abs(size_pt - 12.0) < 0.5:
                print(f"PASS: Component 1 — Font size is {size_pt}pt (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — Expected 12pt, found {size_pt}pt")
        else:
            print("FAIL: Component 1 — Font size is None (inherited)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Font is bold AND italic (0.20 points)
    # Initial: bold=True, italic=None. Golden: bold=True, italic=True
    # This component fails on initial because italic is None (not True).
    try:
        is_bold = font.bold
        is_italic = font.italic
        if is_bold is True and is_italic is True:
            print(f"PASS: Component 2 — Bold={is_bold}, Italic={is_italic} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected bold=True & italic=True, found bold={is_bold}, italic={is_italic}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Font color is #333333 (0.25 points)
    # Initial: 4F81BD (blue). Golden: 333333 (dark gray)
    try:
        color_rgb = font.color.rgb
        if color_rgb is not None:
            color_str = str(color_rgb).upper()
            if color_str == '333333':
                print(f"PASS: Component 3 — Font color is #{color_str} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Expected color #333333, found #{color_str}")
        else:
            print("FAIL: Component 3 — Font color is None")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Bottom paragraph border (thin line) (0.30 points)
    # Initial: no borders. Golden: bottom border single, sz=4
    try:
        border_val = None
        border_sz = None
        pPr = elem.find(qn('w:pPr'))
        if pPr is not None:
            pBdr = pPr.find(qn('w:pBdr'))
            if pBdr is not None:
                bottom = pBdr.find(qn('w:bottom'))
                if bottom is not None:
                    border_val = bottom.get(qn('w:val'))
                    border_sz = bottom.get(qn('w:sz'))
        # Score: border must exist and not be 'none' or 'nil'
        if border_val is not None and border_val not in ('none', 'nil'):
            print(f"PASS: Component 4 — Bottom border found: val={border_val}, sz={border_sz} (0.30 pts)")
            total_score += 0.30
        else:
            print("FAIL: Component 4 — No bottom border found on Heading 2 style")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
