"""
Reward Script: Verify header/footer configuration in LibreOffice Calc
Task ID: calc_gfl_050
Domain: libreoffice_calc
Scoring:
  Component 1 (0.35): Header left has sheet name (&A)
  Component 2 (0.35): Header right has current date (&D)
  Component 3 (0.30): Footer center has page number (&P)
"""

import os
import time


WORKDIR = '/home/user'
TASK_ID = 'calc_gfl_050'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
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
    Verify that the spreadsheet has correct header/footer configuration.
    Returns: float between 0.0 and 1.0
    """
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb.active
    if ws is None:
        print("CRITICAL: No active sheet found")
        print("REWARD: 0.0")
        return 0.0

    hf = ws.HeaderFooter
    oh = hf.oddHeader
    of = hf.oddFooter

    # Component 1: Header left contains sheet name placeholder &A (0.35 points)
    try:
        left_text = None
        if oh and oh.left:
            left_text = getattr(oh.left, 'text', None)
        if left_text and '&A' in left_text:
            print(f"PASS: Component 1 — Header left contains sheet name '&A' (found: {left_text!r}) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Header left should contain '&A' (sheet name), found: {left_text!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Header right contains current date placeholder &D (0.35 points)
    try:
        right_text = None
        if oh and oh.right:
            right_text = getattr(oh.right, 'text', None)
        if right_text and '&D' in right_text:
            print(f"PASS: Component 2 — Header right contains date '&D' (found: {right_text!r}) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Header right should contain '&D' (date), found: {right_text!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Footer center contains page number placeholder &P (0.30 points)
    try:
        center_text = None
        if of and of.center:
            center_text = getattr(of.center, 'text', None)
        if center_text and '&P' in center_text:
            print(f"PASS: Component 3 — Footer center contains page number '&P' (found: {center_text!r}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Footer center should contain '&P' (page number), found: {center_text!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_calc")

file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
