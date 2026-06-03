"""
Reward Script: Set paragraph spacing for body text
Task ID: writer_fs_022
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): space_before on Body Text style ~0.3 cm
  Component 2 (0.35): space_after on Body Text style ~0.3 cm
  Component 3 (0.30): line_spacing on Body Text style == 1.5
"""

import os

from docx import Document
from docx.shared import Pt, Cm, Emu

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_022'

# 0.3 cm in EMU = 108000; allow small tolerance for twips rounding
TARGET_SPACING_EMU = 108000
SPACING_TOLERANCE_EMU = 5000  # ~0.014 cm tolerance


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

    # Check that Body Text style exists
    try:
        style = doc.styles['Body Text']
        pf = style.paragraph_format
    except Exception as e:
        print(f"CRITICAL: Cannot find 'Body Text' style: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Space before paragraph ~0.3 cm (0.35 points)
    # In initial env: space_before=0. In golden: ~107950 EMU (~0.3 cm).
    try:
        space_before = pf.space_before
        if space_before is not None:
            space_before_emu = int(space_before)
            diff = abs(space_before_emu - TARGET_SPACING_EMU)
            if diff <= SPACING_TOLERANCE_EMU:
                print(f"PASS: Component 1 — space_before={space_before_emu} EMU (~{space_before_emu/360000:.3f} cm), target ~0.3 cm (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — space_before={space_before_emu} EMU (~{space_before_emu/360000:.3f} cm), expected ~108000 EMU (~0.3 cm)")
        else:
            print(f"FAIL: Component 1 — space_before is None (inherited/not set)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Space after paragraph ~0.3 cm (0.35 points)
    # In initial env: space_after=0. In golden: ~107950 EMU (~0.3 cm).
    try:
        space_after = pf.space_after
        if space_after is not None:
            space_after_emu = int(space_after)
            diff = abs(space_after_emu - TARGET_SPACING_EMU)
            if diff <= SPACING_TOLERANCE_EMU:
                print(f"PASS: Component 2 — space_after={space_after_emu} EMU (~{space_after_emu/360000:.3f} cm), target ~0.3 cm (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — space_after={space_after_emu} EMU (~{space_after_emu/360000:.3f} cm), expected ~108000 EMU (~0.3 cm)")
        else:
            print(f"FAIL: Component 2 — space_after is None (inherited/not set)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Line spacing == 1.5 lines (0.30 points)
    # In initial env: line_spacing=1.0 (single). In golden: 1.5.
    try:
        line_spacing = pf.line_spacing
        if line_spacing is not None:
            ls_val = float(line_spacing)
            if abs(ls_val - 1.5) < 0.05:
                print(f"PASS: Component 3 — line_spacing={ls_val}, target 1.5 (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 — line_spacing={ls_val}, expected 1.5")
        else:
            print(f"FAIL: Component 3 — line_spacing is None (inherited/not set)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved GUI state
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
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
