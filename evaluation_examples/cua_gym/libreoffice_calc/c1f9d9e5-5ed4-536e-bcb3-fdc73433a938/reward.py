"""
Reward Script: Insert five new sheets (Jan, Feb, Mar, Apr, May) before 'Summary'
Task ID: calc_gsi_036
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Total sheet count is 6
  Component 2 (0.4): All five month sheet names exist
  Component 3 (0.3): Month sheets are all positioned before Summary
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_036'

EXPECTED_MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May']


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
    print(f"INFO: Sheet names found: {sheet_names}")

    # Component 1: Total sheet count is 6 (0.3 points)
    # Initial has 1 sheet (Summary). Golden should have 6 (5 months + Summary).
    try:
        if len(sheet_names) == 6:
            print(f"PASS: Component 1 — Sheet count is 6 (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected 6 sheets, found {len(sheet_names)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All five month sheet names exist (0.4 points)
    # Award partial credit: 0.08 per month sheet found
    try:
        months_found = [m for m in EXPECTED_MONTHS if m in sheet_names]
        month_score = len(months_found) * 0.08
        if len(months_found) == 5:
            print(f"PASS: Component 2 — All 5 month sheets found: {months_found} (0.4 pts)")
            total_score += 0.4
        elif len(months_found) > 0:
            print(f"PARTIAL: Component 2 — Found {len(months_found)}/5 month sheets: {months_found} ({month_score:.2f} pts)")
            total_score += month_score
        else:
            print(f"FAIL: Component 2 — No month sheets found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Month sheets are positioned before Summary (0.3 points)
    # All month sheets must appear before 'Summary' in the sheet order.
    try:
        if 'Summary' not in sheet_names:
            print(f"FAIL: Component 3 — 'Summary' sheet not found")
        else:
            summary_idx = sheet_names.index('Summary')
            months_in_names = [m for m in EXPECTED_MONTHS if m in sheet_names]
            if len(months_in_names) == 0:
                print(f"FAIL: Component 3 — No month sheets to check ordering")
            else:
                all_before = all(sheet_names.index(m) < summary_idx for m in months_in_names)
                if all_before and len(months_in_names) == 5:
                    print(f"PASS: Component 3 — All month sheets positioned before Summary (0.3 pts)")
                    total_score += 0.3
                elif all_before:
                    # Partial: some months exist and are before Summary
                    partial = 0.3 * (len(months_in_names) / 5)
                    print(f"PARTIAL: Component 3 — {len(months_in_names)}/5 month sheets before Summary ({partial:.2f} pts)")
                    total_score += partial
                else:
                    bad = [m for m in months_in_names if sheet_names.index(m) >= summary_idx]
                    print(f"FAIL: Component 3 — These month sheets are NOT before Summary: {bad}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
