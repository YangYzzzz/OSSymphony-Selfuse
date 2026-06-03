"""
Reward Script: Filter employee list to show only employees earning above average salary
Task ID: calc_dop_filter_aboveavg_011
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): AutoFilter has a filter applied on column D (Salary, colId=3)
                     with a 'greaterThan' operator (above-average filter)
  Component 2 (0.3): Filter threshold value is near the correct average salary (~72363)
  Component 3 (0.3): Row visibility is correct — 31 rows hidden (at/below avg),
                     24 rows visible (above avg)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_dop_filter_aboveavg_011'

# Expected values derived from the task context:
#   55 employees, sum of salaries = 3,980,000, average = 72363.636...
#   Filter threshold in golden: greaterThan 72363 (truncated integer avg)
EXPECTED_AVG = 72363.63636363637
# Tolerance: filter val should be close to the integer-truncated average (72363)
# Allow +/- 1000 in case implementation uses floor/round/ceiling
FILTER_VAL_MIN = 71000
FILTER_VAL_MAX = 73500
SALARY_COLUMN = 3   # colId is 0-indexed; col D = index 3
EXPECTED_HIDDEN = 31    # rows at or below average
EXPECTED_VISIBLE = 24   # rows strictly above average (data rows 2-56)
TOTAL_DATA_ROWS = 55    # rows 2-56


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

    # Precondition: check the 'Salaries' sheet exists
    if 'Salaries' not in wb.sheetnames:
        print("CRITICAL: 'Salaries' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Salaries']

    # Component 1: AutoFilter has a filter column applied on column D (colId=3)
    # with 'greaterThan' operator — indicating the above-average filter was applied.
    # Initial file has 0 filterColumns; golden file has filterColumn colId=3.
    # This FAILS on initial (no filterColumn) and PASSES on golden. (0.4 points)
    try:
        af = ws.auto_filter
        filter_col_found = False
        filter_is_greater_than = False
        filter_val = None

        if af and af.ref:
            for fc in af.filterColumn:
                if fc.colId == SALARY_COLUMN:
                    filter_col_found = True
                    if fc.customFilters:
                        # CustomFilters has a .customFilter attribute (list of CustomFilter items)
                        custom_list = fc.customFilters.customFilter
                        for cf in custom_list:
                            if hasattr(cf, 'operator') and cf.operator == 'greaterThan':
                                filter_is_greater_than = True
                                filter_val = cf.val

        if filter_col_found and filter_is_greater_than:
            print(f"PASS: Component 1 — AutoFilter has 'greaterThan' filter on Salary column (colId={SALARY_COLUMN}), val={filter_val} (0.4 pts)")
            total_score += 0.4
        elif filter_col_found:
            print(f"FAIL: Component 1 — Filter found on Salary column but operator is not 'greaterThan'. customFilters found but no greaterThan.")
        else:
            num_fc = len(list(af.filterColumn)) if af else 0
            print(f"FAIL: Component 1 — No filter applied on Salary column (colId={SALARY_COLUMN}). filterColumn count={num_fc}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Filter threshold value is near the correct average salary.
    # Average = 72363.636..., so the filter val should be in the range [71000, 73500].
    # This FAILS on initial (no filter applied at all) and PASSES on golden. (0.3 points)
    try:
        if filter_val is not None:
            try:
                val_numeric = float(filter_val)
                if FILTER_VAL_MIN <= val_numeric <= FILTER_VAL_MAX:
                    print(f"PASS: Component 2 — Filter threshold {val_numeric} is in expected range [{FILTER_VAL_MIN}, {FILTER_VAL_MAX}] (near avg ~{EXPECTED_AVG:.2f}) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — Filter threshold {val_numeric} is outside expected range [{FILTER_VAL_MIN}, {FILTER_VAL_MAX}] (avg ~{EXPECTED_AVG:.2f})")
            except (ValueError, TypeError):
                print(f"FAIL: Component 2 — Filter val '{filter_val}' cannot be converted to number")
        else:
            print(f"FAIL: Component 2 — No filter val available (filter not applied or not 'greaterThan')")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Row visibility is correct.
    # After filtering, rows with salary <= average should be hidden (31 rows),
    # and rows with salary > average should be visible (24 rows).
    # Initial file has 0 hidden rows; golden has 31 hidden rows.
    # This FAILS on initial (0 hidden rows) and PASSES on golden (31 hidden). (0.3 points)
    try:
        hidden_count = sum(
            1 for row in range(2, TOTAL_DATA_ROWS + 2)
            if ws.row_dimensions[row].hidden
        )
        visible_count = TOTAL_DATA_ROWS - hidden_count

        if hidden_count == EXPECTED_HIDDEN and visible_count == EXPECTED_VISIBLE:
            print(f"PASS: Component 3 — Row visibility correct: {hidden_count} hidden, {visible_count} visible (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Expected {EXPECTED_HIDDEN} hidden / {EXPECTED_VISIBLE} visible rows, found {hidden_count} hidden / {visible_count} visible")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
