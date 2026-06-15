"""
Reward Script: Modify Default Paragraph Style in Writer document
Task ID: writer_bs_052
Domain: libreoffice_writer
Scoring:
  Component 1: Font name = Georgia (0.25 pts)
  Component 2: Font size = 11pt (0.20 pts)
  Component 3: Line spacing = Proportional 115% (0.20 pts)
  Component 4: Alignment = Justified (0.20 pts)
  Component 5: Spacing after paragraph = ~0.25cm (0.15 pts)
"""

import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_052'


def persist_app_state(domain):
    """Save any unsaved GUI edits before verification."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        import time
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that the Default Paragraph Style (Normal) has been modified to:
      - Font: Georgia
      - Size: 11pt
      - Line spacing: Proportional 115% (1.15 multiple)
      - Alignment: Justified
      - Spacing after paragraph: 0.25cm (~90000 EMU)
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the Normal style (= Default Paragraph Style)
    try:
        style = doc.styles['Normal']
    except Exception as e:
        print(f"CRITICAL: Cannot find Normal style: {e}")
        print("REWARD: 0.0")
        return 0.0

    font = style.font
    pf = style.paragraph_format

    # Component 1: Font name is Georgia (0.25 points)
    try:
        font_name = font.name
        if font_name and font_name.lower() == 'georgia':
            print(f"PASS: Component 1 — Font name is Georgia (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected font 'Georgia', found '{font_name}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Font size is 11pt (0.20 points)
    try:
        font_size = font.size
        if font_size is not None and abs(font_size.pt - 11.0) < 0.5:
            print(f"PASS: Component 2 — Font size is {font_size.pt}pt (0.20 pts)")
            total_score += 0.20
        else:
            size_val = font_size.pt if font_size else None
            print(f"FAIL: Component 2 — Expected 11pt, found {size_val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Line spacing is proportional 115% (1.15 multiple) (0.20 points)
    # In OOXML, proportional 115% = lineRule="auto" with line=276 (240 * 1.15)
    # python-docx exposes this as line_spacing=1.15, line_spacing_rule=MULTIPLE
    try:
        ls = pf.line_spacing
        ls_rule = pf.line_spacing_rule
        # Accept line_spacing between 1.10 and 1.20 with MULTIPLE rule
        from docx.enum.text import WD_LINE_SPACING
        if ls is not None and ls_rule == WD_LINE_SPACING.MULTIPLE and abs(ls - 1.15) < 0.05:
            print(f"PASS: Component 3 — Line spacing is {ls} multiple (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Expected 1.15 multiple, found spacing={ls}, rule={ls_rule}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Alignment is Justified (0.20 points)
    try:
        alignment = pf.alignment
        if alignment == WD_PARAGRAPH_ALIGNMENT.JUSTIFY:
            print(f"PASS: Component 4 — Alignment is JUSTIFY (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Expected JUSTIFY, found {alignment}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Spacing after paragraph ~0.25cm (0.15 points)
    # 0.25cm = 90000 EMU (approximately). Allow tolerance of +/- 5000 EMU.
    try:
        space_after = pf.space_after
        if space_after is not None and space_after > 0:
            # 0.25cm in EMU: Cm(0.25) = 90000 EMU
            target_emu = 90000
            tolerance = 5000
            if abs(space_after - target_emu) < tolerance:
                print(f"PASS: Component 5 — Space after is {space_after} EMU (~0.25cm) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — Expected ~{target_emu} EMU (0.25cm), found {space_after} EMU")
        else:
            print(f"FAIL: Component 5 — Expected spacing after ~0.25cm, found {space_after}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before checking
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
