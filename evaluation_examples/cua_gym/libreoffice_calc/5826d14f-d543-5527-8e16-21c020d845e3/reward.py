"""
Reward Script: Apply filters on three columns simultaneously
Task ID: calc_dop_filter_multi_074
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.35): Column C (Region) is filtered to 'North'
  - Component 2 (0.35): Column D (Status) is filtered to 'Active'
  - Component 3 (0.30): Column E (Revenue) has a custom filter greaterThan 25000
  Total: 1.0

The initial file has AutoFilter enabled but no active filter columns.
The golden file has 3 active filter columns corresponding to the three conditions.
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_dop_filter_multi_074'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that three AutoFilter filter columns have been set:
      - Column C (colId=2): filter == 'North'
      - Column D (colId=3): filter == 'Active'
      - Column E (colId=4): custom filter greaterThan 25000
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: sheet must exist
    if 'SalesReps' not in wb.sheetnames:
        print("CRITICAL: Sheet 'SalesReps' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['SalesReps']

    # Precondition gate: AutoFilter must be set on the sheet
    if not ws.auto_filter.ref:
        print("FAIL: AutoFilter not defined on the sheet")
        print("REWARD: 0.0")
        return 0.0

    # Build a map of colId -> FilterColumn for convenient lookup
    filter_col_map = {fc.colId: fc for fc in ws.auto_filter.filterColumn}

    # Component 1: Column C (Region) filtered to 'North' — colId=2 (0.35 points)
    # This FAILS on initial (no filterColumns) and PASSES on golden (colId=2 with 'North')
    try:
        north_found = False
        if 2 in filter_col_map:
            fc = filter_col_map[2]
            if fc.filters and hasattr(fc.filters, 'filter'):
                for f in fc.filters.filter:
                    if str(f).strip() == 'North':
                        north_found = True
                        break
        if north_found:
            print("PASS: Component 1 — Column C (Region) filtered to 'North' (0.35 pts)")
            total_score += 0.35
        else:
            actual = None
            if 2 in filter_col_map:
                fc = filter_col_map[2]
                if fc.filters and hasattr(fc.filters, 'filter'):
                    actual = [str(f) for f in fc.filters.filter]
            print(f"FAIL: Component 1 — Column C filter not set to 'North', found: {actual}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Column D (Status) filtered to 'Active' — colId=3 (0.35 points)
    # This FAILS on initial (no filterColumns) and PASSES on golden (colId=3 with 'Active')
    try:
        active_found = False
        if 3 in filter_col_map:
            fc = filter_col_map[3]
            if fc.filters and hasattr(fc.filters, 'filter'):
                for f in fc.filters.filter:
                    if str(f).strip() == 'Active':
                        active_found = True
                        break
        if active_found:
            print("PASS: Component 2 — Column D (Status) filtered to 'Active' (0.35 pts)")
            total_score += 0.35
        else:
            actual = None
            if 3 in filter_col_map:
                fc = filter_col_map[3]
                if fc.filters and hasattr(fc.filters, 'filter'):
                    actual = [str(f) for f in fc.filters.filter]
            print(f"FAIL: Component 2 — Column D filter not set to 'Active', found: {actual}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Column E (Revenue) has custom filter greaterThan 25000 — colId=4 (0.30 points)
    # This FAILS on initial (no filterColumns) and PASSES on golden (colId=4 with customFilter)
    try:
        revenue_filter_found = False
        if 4 in filter_col_map:
            fc = filter_col_map[4]
            if fc.customFilters and hasattr(fc.customFilters, 'customFilter'):
                for cf in fc.customFilters.customFilter:
                    # Check that operator is greaterThan and val is 25000 (string or numeric)
                    op = str(cf.operator).strip().lower() if cf.operator else ''
                    val = cf.val
                    try:
                        val_num = float(str(val).strip())
                    except (ValueError, TypeError):
                        val_num = None
                    if op == 'greaterthan' and val_num is not None and abs(val_num - 25000) < 1:
                        revenue_filter_found = True
                        break
        if revenue_filter_found:
            print("PASS: Component 3 — Column E (Revenue) has custom filter greaterThan 25000 (0.30 pts)")
            total_score += 0.30
        else:
            actual_cf = None
            if 4 in filter_col_map:
                fc = filter_col_map[4]
                if fc.customFilters and hasattr(fc.customFilters, 'customFilter'):
                    actual_cf = [(str(cf.operator), cf.val) for cf in fc.customFilters.customFilter]
            print(f"FAIL: Component 3 — Revenue custom filter not greaterThan 25000, found: {actual_cf}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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
