"""
Reward Script: Adjust page breaks in Page Break Preview and return to Normal view
Task ID: calc_gsi_049
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.25): Revenue Summary has manual row break(s)
  - Component 2 (0.25): Department Budget has manual row break(s)
  - Component 3 (0.25): Quarterly Targets has manual row break(s)
  - Component 4 (0.25): Monthly Breakdown has manual row break(s)

The task asks the user to switch to Page Break Preview, drag page breaks to
new positions across all sheets, then switch back to Normal view.
The key verifiable change is the presence of manual page breaks (row_breaks
with man=True) on each sheet -- these do NOT exist in the initial file.
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_049'


def persist_app_state(domain: str):
    """Save any unsaved changes in LibreOffice before verification."""
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
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Scoring rubric:
      Each of the 4 sheets must have at least one manual row break (man=True).
      Each sheet with manual breaks earns 0.25 points.
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Expected sheets and their point values
    sheets_to_check = [
        ("Revenue Summary", 0.25),
        ("Department Budget", 0.25),
        ("Quarterly Targets", 0.25),
        ("Monthly Breakdown", 0.25),
    ]

    for sheet_name, points in sheets_to_check:
        # Component: <sheet_name> has manual row break(s)
        try:
            if sheet_name not in wb.sheetnames:
                print(f"FAIL: Sheet '{sheet_name}' not found in workbook")
                continue

            ws = wb[sheet_name]
            row_breaks = ws.row_breaks

            # Count manual breaks directly (no flag variable)
            manual_breaks = [b for b in (row_breaks.brk if row_breaks and row_breaks.brk else []) if b.man]

            if len(manual_breaks) > 0:
                break_ids = [b.id for b in manual_breaks]
                print(f"PASS: '{sheet_name}' has {len(manual_breaks)} manual row break(s) at row(s) {break_ids} ({points} pts)")
                total_score += points
            else:
                print(f"FAIL: '{sheet_name}' has no manual row breaks")
        except Exception as e:
            print(f"ERROR: Checking '{sheet_name}': {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification (LibreOffice may have unsaved edits)
persist_app_state("libreoffice_calc")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
