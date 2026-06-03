"""
Reward Script: Verify header/footer configuration on Timesheet sheet
Task ID: calc_mcp_080
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.30): Header left section contains file name placeholder (&F)
  - Component 2 (0.35): Header right section = 'Page &P of &N'
  - Component 3 (0.35): Footer center section = 'Printed on: &D'
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_mcp_080'


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
    Verify header and footer configuration on the Timesheet sheet.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import openpyxl
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check that Timesheet sheet exists (precondition gate)
    if 'Timesheet' not in wb.sheetnames:
        print("CRITICAL: 'Timesheet' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Timesheet']

    # Component 1: Header left section contains file name placeholder &F (0.30 points)
    try:
        header_left = ws.oddHeader.left.text if ws.oddHeader and ws.oddHeader.left else None
        if header_left and '&F' in header_left:
            print(f"PASS: Component 1 — Header left contains '&F' (value: {repr(header_left)}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Expected '&F' in header left, found: {repr(header_left)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Header right section = 'Page &P of &N' (0.35 points)
    try:
        header_right = ws.oddHeader.right.text if ws.oddHeader and ws.oddHeader.right else None
        if header_right and header_right.strip() == 'Page &P of &N':
            print(f"PASS: Component 2 — Header right = 'Page &P of &N' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Expected 'Page &P of &N' in header right, found: {repr(header_right)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Footer center section = 'Printed on: &D' (0.35 points)
    try:
        footer_center = ws.oddFooter.center.text if ws.oddFooter and ws.oddFooter.center else None
        if footer_center and footer_center.strip() == 'Printed on: &D':
            print(f"PASS: Component 3 — Footer center = 'Printed on: &D' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — Expected 'Printed on: &D' in footer center, found: {repr(footer_center)}")
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
