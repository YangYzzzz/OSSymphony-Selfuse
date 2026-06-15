"""
Reward Script: Auto-fit the height of rows 2 through 30 so each row adjusts to exactly fit its content.
Task ID: calc_fmt_row_autofit_050
Domain: libreoffice_calc
Scoring:
  Component 1: Row 1 height unchanged AND rows 2-30 auto-fit initiated (any rows cleared) — 0.2 pts
  Component 2: All 29 rows (2-30) have their custom fixed height removed — 0.8 pts
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_fmt_row_autofit_050'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    The task requires auto-fitting rows 2-30:
      - Initial state: rows 2-30 each have customHeight=True, height=15.0 (fixed)
      - Golden state: rows 2-30 have no explicit height set (auto/optimal height)
      - Row 1 must remain at height=20.0 (unchanged)

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gate: sheet must exist
    if 'Notes Database' not in wb.sheetnames:
        print("FAIL: Sheet 'Notes Database' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Notes Database']

    # Component 1: Row 1 height is still set to the original 20.0 pt (unchanged),
    # AND at least one row in 2-30 has been freed from the fixed 15.0pt height.
    # This partial check ensures the task has been started correctly — it does not
    # award points for simply leaving everything as-is (initial has ALL rows 2-30
    # at 15.0pt with customHeight=True, so "at least one freed" fails on initial).
    # (0.2 points)
    try:
        rd1 = ws.row_dimensions.get(1)
        row1_height_ok = (rd1 is not None and rd1.height == 20.0)

        # Count rows in 2-30 that still have the original fixed 15pt height
        rows_still_fixed = 0
        for r in range(2, 31):
            rd = ws.row_dimensions.get(r)
            # A row still has the fixed height if it has an explicit height of 15.0
            # AND customHeight is True (exactly the initial state)
            if rd is not None and rd.height == 15.0 and rd.customHeight is True:
                rows_still_fixed += 1

        rows_freed = 29 - rows_still_fixed  # rows 2-30 that have been auto-fitted

        if row1_height_ok and rows_freed >= 1:
            print(f"PASS: Component 1 — Row 1 height preserved (20pt) and {rows_freed}/29 rows freed from fixed height (0.2 pts)")
            total_score += 0.2
        elif not row1_height_ok:
            print(f"FAIL: Component 1 — Row 1 height is not 20pt: {rd1.height if rd1 else 'not set'}")
        else:
            print(f"FAIL: Component 1 — No rows freed from fixed height (all 29 rows still at 15pt)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ALL 29 rows (2-30) have their custom fixed height completely removed.
    # A row is considered auto-fitted when it has NO explicit custom height entry
    # (i.e., ws.row_dimensions.get(r) is None, or customHeight is not True, or height != 15.0).
    # The golden file shows rows 2-30 have no row_dimensions entry at all.
    # (0.8 points)
    try:
        auto_fitted_count = 0
        failed_rows = []
        for r in range(2, 31):
            rd = ws.row_dimensions.get(r)
            # Row is auto-fitted if:
            #   - No row dimension entry (rd is None), OR
            #   - row dimension exists but customHeight is not True (auto-sizing enabled), OR
            #   - row dimension exists but height is None or not the fixed 15pt
            is_auto_fitted = (
                rd is None or
                rd.customHeight is not True or
                rd.height is None or
                rd.height != 15.0
            )
            if is_auto_fitted:
                auto_fitted_count += 1
            else:
                failed_rows.append(r)

        if auto_fitted_count == 29:
            print(f"PASS: Component 2 — All 29 rows (2-30) have been auto-fitted (0.8 pts)")
            total_score += 0.8
        elif auto_fitted_count >= 15:
            # Partial credit: more than half completed but not all
            partial = round(0.8 * (auto_fitted_count / 29), 4)
            print(f"PARTIAL: Component 2 — {auto_fitted_count}/29 rows auto-fitted, still fixed: rows {failed_rows[:5]}{'...' if len(failed_rows) > 5 else ''} (partial {partial} pts awarded as 0)")
            # No partial within this component — all-or-nothing for this major check
            print(f"FAIL: Component 2 — {auto_fitted_count}/29 rows auto-fitted (need all 29)")
        else:
            print(f"FAIL: Component 2 — Only {auto_fitted_count}/29 rows auto-fitted, still fixed: {failed_rows[:5]}{'...' if len(failed_rows) > 5 else ''}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = round(min(total_score, 1.0), 4)
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
