"""
Reward Script: Set column B width to 25 characters in 'Contact List' sheet
Task ID: calc_fmt_col_width_specific_051
Domain: libreoffice_calc
Scoring:
  Component 1: Column B has an explicit width set (not the default/None) (0.4 pts)
  Component 2: Column B width is exactly 25 characters (0.6 pts)
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_fmt_col_width_specific_051'

TARGET_COL_B_WIDTH = 25.0
# Tolerance: allow ±0.5 character units (openpyxl rounding may vary)
WIDTH_TOLERANCE = 0.5


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

    # Precondition gate: verify sheet exists
    if 'Contact List' not in wb.sheetnames:
        print("CRITICAL: Sheet 'Contact List' not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Contact List']

    # Get column B dimension object and its width value
    col_b_dim = ws.column_dimensions.get('B')
    col_b_width = col_b_dim.width if col_b_dim is not None else None

    # Component 1: Column B has an explicit non-default width set (0.4 points)
    # In the initial file, column B has no explicit entry in column_dimensions,
    # so col_b_dim is None or width is None/0/default (~8.43).
    # In the golden file, column B has width=25.0 explicitly set.
    # This FAILS on initial (None width) → PASSES on golden (explicit 25).
    try:
        # An explicitly set non-default width: must be > 0 and not the Excel default (~8.43)
        if col_b_width is not None and col_b_width > 10.0:
            print(f"PASS: Component 1 — Column B has explicit width set: {col_b_width} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Column B width not set or is default: {col_b_width}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check column B width existence: {e}")

    # Component 2: Column B width is exactly 25 characters (0.6 points)
    # This FAILS on initial (no width set, None) → PASSES on golden (exactly 25.0).
    try:
        if col_b_width is not None and abs(col_b_width - TARGET_COL_B_WIDTH) <= WIDTH_TOLERANCE:
            print(f"PASS: Component 2 — Column B width = {col_b_width} (exactly {TARGET_COL_B_WIDTH} chars) (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 2 — Column B width = {col_b_width}, expected {TARGET_COL_B_WIDTH} chars")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check column B exact width: {e}")

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
