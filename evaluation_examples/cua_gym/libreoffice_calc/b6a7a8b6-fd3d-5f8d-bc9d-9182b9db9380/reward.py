"""
Reward Script: Freeze the first row in the 'Sales Data' sheet
Task ID: calc_sht_freeze_row_001
Domain: libreoffice_calc
Scoring:
  Component 1 (0.6): freeze_panes is set on the 'Sales Data' sheet (not None)
  Component 2 (0.4): freeze_panes is exactly 'A2', freezing precisely row 1
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_sht_freeze_row_001'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Freeze the first row in the 'Sales Data' sheet so the headers
    stay visible when scrolling down.
    Expected: ws.freeze_panes == 'A2'
    """
    total_score = 0.0

    # Load the workbook; if it can't be loaded, score is 0.0
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: 'Sales Data' sheet must exist
    if 'Sales Data' not in wb.sheetnames:
        print("FAIL: Sheet 'Sales Data' not found in workbook.")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Sales Data']

    # Component 1: freeze_panes is set (not None) — row freeze was applied (0.6 points)
    # This FAILS on initial (freeze_panes=None) and PASSES on golden (freeze_panes='A2')
    try:
        freeze_val = ws.freeze_panes
        if freeze_val is not None:
            print(f"PASS: Component 1 — freeze_panes is set (value: {repr(freeze_val)}) (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — freeze_panes is None (no freeze applied), expected 'A2'")
    except Exception as e:
        print(f"ERROR: Component 1 — could not check freeze_panes: {e}")

    # Component 2: freeze_panes is exactly 'A2', meaning row 1 is frozen (0.4 points)
    # This FAILS on initial (freeze_panes=None) and PASSES on golden (freeze_panes='A2')
    # This check ensures the freeze is precisely at row 2 (freezing row 1), not some other location
    try:
        freeze_val = ws.freeze_panes
        if str(freeze_val).upper() == 'A2':
            print(f"PASS: Component 2 — freeze_panes is exactly 'A2' (row 1 frozen correctly) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — expected freeze_panes='A2', found {repr(freeze_val)}")
    except Exception as e:
        print(f"ERROR: Component 2 — could not check freeze_panes value: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
