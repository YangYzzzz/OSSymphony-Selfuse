"""
Reward Script: Configure print settings on 'Summary' sheet
Task ID: calc_gg3_039
Domain: libreoffice_calc
Scoring:
  - Component 1: Center horizontally (0.2)
  - Component 2: Center vertically (0.2)
  - Component 3: Row/column headings enabled (0.2)
  - Component 4: Grid lines enabled (0.2)
  - Component 5: Footer left=filename, right=date (0.2)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gg3_039'


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
    Verify print settings on the Summary sheet.
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

    # Precondition: Summary sheet must exist
    if 'Summary' not in wb.sheetnames:
        print("CRITICAL: 'Summary' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Summary']
    pp = ws.print_options

    # Component 1: Center horizontally (0.2 points)
    try:
        if pp.horizontalCentered is True:
            print(f"PASS: Component 1 — horizontalCentered is True (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — horizontalCentered is {pp.horizontalCentered}, expected True")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Center vertically (0.2 points)
    try:
        if pp.verticalCentered is True:
            print(f"PASS: Component 2 — verticalCentered is True (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — verticalCentered is {pp.verticalCentered}, expected True")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Row/column headings enabled (0.2 points)
    try:
        if pp.headings is True:
            print(f"PASS: Component 3 — headings (row/column headers) is True (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — headings is {pp.headings}, expected True")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Grid lines enabled (0.2 points)
    try:
        if pp.gridLines is True:
            print(f"PASS: Component 4 — gridLines is True (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — gridLines is {pp.gridLines}, expected True")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Footer — left=filename (&F), right=date (&D) (0.2 points)
    try:
        hf = ws.HeaderFooter
        footer_left = hf.oddFooter.left.text if hf.oddFooter and hf.oddFooter.left else None
        footer_right = hf.oddFooter.right.text if hf.oddFooter and hf.oddFooter.right else None

        # &F is the LibreOffice/Excel code for filename, &D for date
        left_ok = footer_left is not None and '&F' in footer_left
        right_ok = footer_right is not None and '&D' in footer_right

        if left_ok and right_ok:
            print(f"PASS: Component 5 — Footer left='{footer_left}', right='{footer_right}' (0.2 pts)")
            total_score += 0.2
        elif left_ok:
            print(f"PARTIAL: Component 5 — Footer left='{footer_left}' correct (+0.1)")
            print(f"FAIL: Component 5b — Footer right expected '&D', found '{footer_right}'")
            total_score += 0.1
        elif right_ok:
            print(f"FAIL: Component 5a — Footer left expected '&F', found '{footer_left}'")
            print(f"PARTIAL: Component 5 — Footer right='{footer_right}' correct (+0.1)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 5a — Footer left expected '&F', found '{footer_left}'")
            print(f"FAIL: Component 5b — Footer right expected '&D', found '{footer_right}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
