"""
Reward Script: Remove data validation from cell D5 only
Task ID: calc_nrv_071
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): D5 has no data validation
  Component 2 (0.3): D2:D4 retain whole number validation (1-1000)
  Component 3 (0.2): D6:D20 retain whole number validation (1-1000)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_071'


def cell_has_validation(ws, cell_coord):
    """Check if a specific cell is covered by any data validation rule."""
    from openpyxl.utils import coordinate_to_tuple
    row, col = coordinate_to_tuple(cell_coord)
    for dv in ws.data_validations.dataValidation:
        for cell_range in dv.sqref.ranges:
            if (cell_range.min_row <= row <= cell_range.max_row and
                    cell_range.min_col <= col <= cell_range.max_col):
                return dv
    return None


def cell_has_whole_validation(ws, cell_coord, min_val='1', max_val='1000'):
    """Check if a cell has whole number validation with specified range."""
    dv = cell_has_validation(ws, cell_coord)
    if dv is None:
        return False
    if dv.type != 'whole':
        return False
    if dv.operator != 'between':
        return False
    if str(dv.formula1) != str(min_val) or str(dv.formula2) != str(max_val):
        return False
    return True


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

    ws = wb['Inventory']

    # Gate check: determine if D5 has validation removed
    d5_has_no_validation = False
    try:
        dv_on_d5 = cell_has_validation(ws, 'D5')
        d5_has_no_validation = (dv_on_d5 is None)
    except Exception as e:
        print(f"ERROR: D5 validation check — {e}")

    # Component 1: D5 has NO data validation (0.5 points)
    # This is the core task requirement - D5 validation must be removed
    try:
        if d5_has_no_validation:
            print(f"PASS: Component 1 — D5 has no data validation (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — D5 still has validation: type={dv_on_d5.type}, sqref={dv_on_d5.sqref}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: D5 removed AND D2:D4 retain whole number validation 1-1000 (0.3 points)
    # Compound check: anchored to D5 change so it fails on initial_env
    try:
        if not d5_has_no_validation:
            print(f"FAIL: Component 2 — D5 still has validation, skipping D2:D4 check")
        else:
            all_valid = True
            for cell_coord in ['D2', 'D3', 'D4']:
                if not cell_has_whole_validation(ws, cell_coord):
                    print(f"FAIL: Component 2 — {cell_coord} missing whole number validation (1-1000)")
                    all_valid = False
                    break
            if all_valid:
                print(f"PASS: Component 2 — D5 removed AND D2:D4 retain validation (0.3 pts)")
                total_score += 0.3
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: D5 removed AND D6:D20 retain whole number validation 1-1000 (0.2 points)
    # Compound check: anchored to D5 change so it fails on initial_env
    try:
        if not d5_has_no_validation:
            print(f"FAIL: Component 3 — D5 still has validation, skipping D6:D20 check")
        else:
            all_valid = True
            for row_num in range(6, 21):
                cell_coord = f'D{row_num}'
                if not cell_has_whole_validation(ws, cell_coord):
                    print(f"FAIL: Component 3 — {cell_coord} missing whole number validation (1-1000)")
                    all_valid = False
                    break
            if all_valid:
                print(f"PASS: Component 3 — D5 removed AND D6:D20 retain validation (0.2 pts)")
                total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
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
