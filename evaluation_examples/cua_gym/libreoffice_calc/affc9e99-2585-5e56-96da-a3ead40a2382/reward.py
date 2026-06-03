"""
Reward Script: Delete the 'Scratch' sheet from the workbook
Task ID: calc_gg1_038
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): 'Scratch' sheet does not exist in the workbook
  Component 2 (0.3): Workbook has exactly 4 sheets
  Component 3 (0.2): The 4 remaining sheets are exactly Dashboard, Q1 Data, Q2 Data, Charts
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gg1_038'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_calc")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that the 'Scratch' sheet has been deleted and the remaining
    four sheets are intact.
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

    # Component 1: 'Scratch' sheet does not exist (0.5 points)
    # This is the PRIMARY task requirement — the sheet must be deleted.
    # FAILS on initial (Scratch exists) → PASSES on golden (Scratch removed) ✅
    try:
        if 'Scratch' not in sheet_names:
            print(f"PASS: Component 1 — 'Scratch' sheet not found in workbook (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — 'Scratch' sheet still exists in workbook. Sheets: {sheet_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Workbook has exactly 4 sheets (0.3 points)
    # FAILS on initial (5 sheets) → PASSES on golden (4 sheets) ✅
    try:
        sheet_count = len(sheet_names)
        if sheet_count == 4:
            print(f"PASS: Component 2 — Workbook has exactly 4 sheets (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected 4 sheets, found {sheet_count}. Sheets: {sheet_names}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The remaining sheets are exactly the expected four (0.2 points)
    # FAILS on initial (has 5 sheets including Scratch) → PASSES on golden (exactly 4 correct sheets) ✅
    expected_sheets = ['Dashboard', 'Q1 Data', 'Q2 Data', 'Charts']
    try:
        if sheet_names == expected_sheets:
            print(f"PASS: Component 3 — Sheet names match expected: {expected_sheets} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Expected sheets {expected_sheets}, found {sheet_names}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
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
