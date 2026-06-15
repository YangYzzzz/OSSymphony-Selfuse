"""
Reward Script: Insert a header with [LOGO] left, 'Annual Budget 2024' center (larger font), page number right
Task ID: calc_gao_046
Domain: libreoffice_calc
Scoring:
  - Component 1: Left header contains '[LOGO]' (0.3 pts)
  - Component 2: Center header contains 'Annual Budget 2024' (0.3 pts)
  - Component 3: Center header has larger font size (> default 10) (0.1 pts)
  - Component 4: Right header contains page number field '&P' (0.3 pts)
"""

import os
import time


WORKDIR = '/home/user'
TASK_ID = 'calc_gao_046'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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
    """
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the Budget sheet (precondition gate)
    if 'Budget' not in wb.sheetnames:
        print("CRITICAL: 'Budget' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Budget']
    hdr = ws.oddHeader

    # Component 1: Left header contains '[LOGO]' (0.3 points)
    try:
        left_text = hdr.left.text if hdr.left else None
        if left_text and '[LOGO]' in left_text:
            print(f"PASS: Component 1 — Left header contains '[LOGO]' (text: {left_text!r}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected '[LOGO]' in left header, found: {left_text!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Center header contains 'Annual Budget 2024' (0.3 points)
    try:
        center_text = hdr.center.text if hdr.center else None
        if center_text and 'Annual Budget 2024' in center_text:
            print(f"PASS: Component 2 — Center header contains 'Annual Budget 2024' (text: {center_text!r}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected 'Annual Budget 2024' in center header, found: {center_text!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Center header has larger font size (> default 10) (0.1 points)
    try:
        center_size = hdr.center.size if hdr.center else None
        if center_size is not None and int(center_size) > 10:
            print(f"PASS: Component 3 — Center header font size {center_size} > 10 (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 — Expected center header font size > 10, found: {center_size!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Right header contains page number field '&P' (0.3 points)
    try:
        right_text = hdr.right.text if hdr.right else None
        if right_text and '&P' in right_text:
            print(f"PASS: Component 4 — Right header contains page number field '&P' (text: {right_text!r}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 4 — Expected '&P' in right header, found: {right_text!r}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
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
