"""
Reward Script: Insert a new 'Summary' sheet after the last existing sheet
Task ID: calc_gsi_001
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): 'Summary' sheet exists in the workbook
  Component 2 (0.3): 'Summary' is the last sheet (after January, February, March)
  Component 3 (0.2): 'Summary' sheet is visible (sheet_state == 'visible')
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_001'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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

    # Component 1: 'Summary' sheet exists (0.5 points)
    # This is the core task requirement — a sheet named exactly 'Summary' must be present.
    try:
        if 'Summary' in sheet_names:
            print(f"PASS: Component 1 — 'Summary' sheet exists (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — 'Summary' sheet not found in {sheet_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'Summary' is the last sheet (0.3 points)
    # Task says "after the last existing sheet", so Summary must be at the end.
    try:
        if 'Summary' in sheet_names and sheet_names[-1] == 'Summary':
            print(f"PASS: Component 2 — 'Summary' is the last sheet (position {len(sheet_names)}) (0.3 pts)")
            total_score += 0.3
        elif 'Summary' in sheet_names:
            idx = sheet_names.index('Summary')
            print(f"FAIL: Component 2 — 'Summary' is at position {idx + 1}/{len(sheet_names)}, expected last")
        else:
            print(f"FAIL: Component 2 — 'Summary' sheet not found, cannot check position")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'Summary' sheet is visible (0.2 points)
    # Task says "sheet tab should be visible and accessible".
    try:
        if 'Summary' in sheet_names:
            ws_summary = wb['Summary']
            if ws_summary.sheet_state == 'visible':
                print(f"PASS: Component 3 — 'Summary' sheet is visible (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — 'Summary' sheet_state is '{ws_summary.sheet_state}', expected 'visible'")
        else:
            print(f"FAIL: Component 3 — 'Summary' sheet not found, cannot check visibility")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI state before checking
persist_app_state("libreoffice_calc")

# Test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
