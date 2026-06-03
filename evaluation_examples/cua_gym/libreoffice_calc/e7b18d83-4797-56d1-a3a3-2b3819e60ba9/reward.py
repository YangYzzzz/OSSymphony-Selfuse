"""
Reward Script: Create BatchRename macro that prefixes all sheet names with 'FY2024_'
Task ID: calc_mcp_028
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): FY2024_Sales sheet exists, original 'Sales' removed
  Component 2 (0.25): FY2024_Expenses sheet exists, original 'Expenses' removed
  Component 3 (0.25): FY2024_Summary sheet exists, original 'Summary' removed
  Component 4 (0.25): Exactly 3 sheets total (no duplicates or extras)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_mcp_028'


def persist_app_state(domain: str):
    """Best-effort save any unsaved GUI edits."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            import time
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
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

    # Expected renamed sheets
    expected_renamed = {
        'Sales': 'FY2024_Sales',
        'Expenses': 'FY2024_Expenses',
        'Summary': 'FY2024_Summary',
    }

    # Component 1: FY2024_Sales exists and original 'Sales' does not (0.25 points)
    try:
        if 'FY2024_Sales' in sheet_names and 'Sales' not in sheet_names:
            print(f"PASS: Component 1 — 'FY2024_Sales' exists, 'Sales' removed (0.25 pts)")
            total_score += 0.25
        elif 'FY2024_Sales' in sheet_names:
            print(f"PARTIAL: Component 1 — 'FY2024_Sales' exists but 'Sales' still present")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — 'FY2024_Sales' not found in {sheet_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: FY2024_Expenses exists and original 'Expenses' does not (0.25 points)
    try:
        if 'FY2024_Expenses' in sheet_names and 'Expenses' not in sheet_names:
            print(f"PASS: Component 2 — 'FY2024_Expenses' exists, 'Expenses' removed (0.25 pts)")
            total_score += 0.25
        elif 'FY2024_Expenses' in sheet_names:
            print(f"PARTIAL: Component 2 — 'FY2024_Expenses' exists but 'Expenses' still present")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2 — 'FY2024_Expenses' not found in {sheet_names}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: FY2024_Summary exists and original 'Summary' does not (0.25 points)
    try:
        if 'FY2024_Summary' in sheet_names and 'Summary' not in sheet_names:
            print(f"PASS: Component 3 — 'FY2024_Summary' exists, 'Summary' removed (0.25 pts)")
            total_score += 0.25
        elif 'FY2024_Summary' in sheet_names:
            print(f"PARTIAL: Component 3 — 'FY2024_Summary' exists but 'Summary' still present")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 — 'FY2024_Summary' not found in {sheet_names}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Exactly 3 sheets total AND all are correctly renamed (0.25 points)
    # Ensures no duplicate sheets were created (renamed, not copied)
    try:
        all_renamed = all(
            f'FY2024_{orig}' in sheet_names
            for orig in ['Sales', 'Expenses', 'Summary']
        )
        no_originals = all(
            orig not in sheet_names
            for orig in ['Sales', 'Expenses', 'Summary']
        )
        if len(sheet_names) == 3 and all_renamed and no_originals:
            print(f"PASS: Component 4 — Exactly 3 sheets, all correctly renamed (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Expected exactly 3 renamed sheets, found: {sheet_names}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
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
