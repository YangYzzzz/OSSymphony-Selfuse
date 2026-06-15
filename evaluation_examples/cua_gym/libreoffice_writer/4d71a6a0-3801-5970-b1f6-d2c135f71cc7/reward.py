"""
Reward Script: Page style transition with different margins
Task ID: wrpara_040
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Document has >= 2 sections (section break inserted)
  Component 2 (0.35): First section margins are 3cm all around
  Component 3 (0.20): Second section margins are 2.54cm all around
  Component 4 (0.15): Section break is positioned correctly (between front matter and body)
"""

import os
from docx import Document
from docx.shared import Emu

WORKDIR = '/home/user'
TASK_ID = 'wrpara_040'

# Margin tolerance: 0.15 cm to handle rounding
MARGIN_TOLERANCE_CM = 0.15


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    num_sections = len(doc.sections)
    print(f"INFO: Document has {num_sections} section(s)")

    # Component 1: Document has >= 2 sections (0.30 points)
    # Initial doc has 1 section; golden has 2. This checks if section break was inserted.
    try:
        if num_sections >= 2:
            print(f"PASS: Component 1 -- Document has {num_sections} sections (>= 2) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 -- Document has {num_sections} section(s), expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: First section margins are 3cm all around (0.35 points)
    # Initial has 2.54cm, golden has 3.0cm. Only passes after task completion.
    try:
        if num_sections >= 1:
            sec0 = doc.sections[0]
            margins_cm = {
                'left': round(Emu(sec0.left_margin).cm, 2),
                'right': round(Emu(sec0.right_margin).cm, 2),
                'top': round(Emu(sec0.top_margin).cm, 2),
                'bottom': round(Emu(sec0.bottom_margin).cm, 2),
            }
            target = 3.0
            all_match = all(
                abs(v - target) <= MARGIN_TOLERANCE_CM
                for v in margins_cm.values()
            )
            if all_match:
                print(f"PASS: Component 2 -- First section margins ~3cm: {margins_cm} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 -- First section margins expected ~3cm, found: {margins_cm}")
        else:
            print(f"FAIL: Component 2 -- No sections found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Second section margins are 2.54cm all around (0.20 points)
    # This only exists in the golden doc (which has 2 sections). Initial has 1 section so this fails.
    try:
        if num_sections >= 2:
            sec1 = doc.sections[1]
            margins_cm = {
                'left': round(Emu(sec1.left_margin).cm, 2),
                'right': round(Emu(sec1.right_margin).cm, 2),
                'top': round(Emu(sec1.top_margin).cm, 2),
                'bottom': round(Emu(sec1.bottom_margin).cm, 2),
            }
            target = 2.54
            all_match = all(
                abs(v - target) <= MARGIN_TOLERANCE_CM
                for v in margins_cm.values()
            )
            if all_match:
                print(f"PASS: Component 3 -- Second section margins ~2.54cm: {margins_cm} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 -- Second section margins expected ~2.54cm, found: {margins_cm}")
        else:
            print(f"FAIL: Component 3 -- Document has < 2 sections, cannot check second section margins")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Section break is positioned correctly between front matter and body (0.15 points)
    # The section break should occur somewhere between paragraph 15 and 25 (front matter ends, body begins).
    # We check that the first section break (sectPr in paragraph pPr) is near paragraph 20.
    # Initial doc has 0 section breaks in paragraphs, golden has 1.
    try:
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        sect_break_para_idx = None
        for i, para in enumerate(doc.paragraphs):
            pPr = para._element.find('.//w:pPr', ns)
            if pPr is not None:
                sectPr = pPr.find('w:sectPr', ns)
                if sectPr is not None:
                    sect_break_para_idx = i
                    break  # first section break found

        if sect_break_para_idx is not None:
            # The break should be roughly between paragraphs 15-25 (before the body/Chapter 1)
            if 10 <= sect_break_para_idx <= 28:
                print(f"PASS: Component 4 -- Section break at paragraph {sect_break_para_idx} (within expected range 10-28) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- Section break at paragraph {sect_break_para_idx}, expected between 10-28")
        else:
            print(f"FAIL: Component 4 -- No section break found in paragraph properties")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state before verification
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
