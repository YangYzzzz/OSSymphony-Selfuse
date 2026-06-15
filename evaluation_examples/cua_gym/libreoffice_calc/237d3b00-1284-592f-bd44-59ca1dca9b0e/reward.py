"""
Reward Script: Move Q1 and Q2 sheets to chronological order after Summary
Task ID: calc_gsi_028
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): Q1 sheet is at index 1 (right after Summary)
  Component 2 (0.3): Q2 sheet is at index 2 (right after Q1)
  Component 3 (0.3): Full sheet order is exactly ['Summary', 'Q1', 'Q2', 'Q3', 'Q4']
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_028'

EXPECTED_ORDER = ['Summary', 'Q1', 'Q2', 'Q3', 'Q4']


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
    print(f"Found sheets: {sheet_names}")

    # Precondition: all 5 expected sheets must exist
    missing = [s for s in EXPECTED_ORDER if s not in sheet_names]
    if missing:
        print(f"CRITICAL: Missing sheets: {missing}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Q1 is at index 1 (right after Summary) — 0.4 points
    # Initial has Q1 at index 3, so this FAILS on initial, PASSES on golden
    try:
        q1_index = sheet_names.index('Q1')
        if q1_index == 1:
            print(f"PASS: Component 1 — Q1 is at index 1 (position 2) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Q1 is at index {q1_index}, expected index 1")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Q2 is at index 2 (right after Q1) — 0.3 points
    # Initial has Q2 at index 4, so this FAILS on initial, PASSES on golden
    try:
        q2_index = sheet_names.index('Q2')
        if q2_index == 2:
            print(f"PASS: Component 2 — Q2 is at index 2 (position 3) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Q2 is at index {q2_index}, expected index 2")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Full order matches expected chronological order — 0.3 points
    # Initial order is ['Summary', 'Q3', 'Q4', 'Q1', 'Q2'], so this FAILS on initial
    try:
        if sheet_names == EXPECTED_ORDER:
            print(f"PASS: Component 3 — Full sheet order is correct: {sheet_names} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Sheet order is {sheet_names}, expected {EXPECTED_ORDER}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
