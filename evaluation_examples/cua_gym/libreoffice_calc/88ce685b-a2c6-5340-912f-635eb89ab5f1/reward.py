"""
Reward Script: Insert 3 new sheets (October, November, December) at end of workbook
Task ID: calc_ps_067
Domain: libreoffice_calc
Scoring:
  - Component 1: Sheet count is 6 (0.15 pts)
  - Component 2: 'October' exists at index 3 (0.25 pts)
  - Component 3: 'November' exists at index 4 (0.25 pts)
  - Component 4: 'December' exists at index 5 (0.25 pts)
  - Component 5: Full sheet order matches expected (0.10 pts)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ps_067'

EXPECTED_SHEETS = ['July', 'August', 'September', 'October', 'November', 'December']


def persist_app_state(domain: str):
    """Attempt to save any unsaved GUI state via Ctrl+S."""
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
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    sheet_names = wb.sheetnames
    print(f"INFO: Found sheets: {sheet_names}")

    # Component 1: Sheet count is 6 (0.15 points)
    # Initial has 3 sheets, golden has 6. This checks that 3 new sheets were added.
    try:
        if len(sheet_names) == 6:
            print(f"PASS: Component 1 -- Sheet count is 6 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected 6 sheets, found {len(sheet_names)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: 'October' sheet exists at position index 3 (0.25 points)
    # Initial has no 'October' sheet, so this only passes on golden.
    try:
        if 'October' in sheet_names:
            idx = sheet_names.index('October')
            if idx == 3:
                print(f"PASS: Component 2 -- 'October' exists at index 3 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- 'October' exists but at index {idx}, expected 3")
        else:
            print(f"FAIL: Component 2 -- 'October' sheet not found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: 'November' sheet exists at position index 4 (0.25 points)
    # Initial has no 'November' sheet, so this only passes on golden.
    try:
        if 'November' in sheet_names:
            idx = sheet_names.index('November')
            if idx == 4:
                print(f"PASS: Component 3 -- 'November' exists at index 4 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- 'November' exists but at index {idx}, expected 4")
        else:
            print(f"FAIL: Component 3 -- 'November' sheet not found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: 'December' sheet exists at position index 5 (0.25 points)
    # Initial has no 'December' sheet, so this only passes on golden.
    try:
        if 'December' in sheet_names:
            idx = sheet_names.index('December')
            if idx == 5:
                print(f"PASS: Component 4 -- 'December' exists at index 5 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 -- 'December' exists but at index {idx}, expected 5")
        else:
            print(f"FAIL: Component 4 -- 'December' sheet not found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Full sheet order matches expected exactly (0.10 points)
    # Initial order is ['July','August','September'] which != expected 6-sheet order.
    try:
        if sheet_names == EXPECTED_SHEETS:
            print(f"PASS: Component 5 -- Full sheet order matches expected (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 -- Sheet order {sheet_names} != expected {EXPECTED_SHEETS}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
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
