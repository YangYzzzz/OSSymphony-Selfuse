"""
Reward Script: Data validation for a budget sheet
Task ID: calc_nrv_067
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Decimal validation exists on C2:C20
  Component 2 (0.2): Decimal validation has correct bounds (0-1000000, operator=between)
  Component 3 (0.3): List validation exists on D2:D20
  Component 4 (0.2): List validation formula references $G$1:$G$8
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_067'


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

    ws = wb.active

    # Collect all data validations
    validations = ws.data_validations.dataValidation
    print(f"INFO: Found {len(validations)} data validation(s)")

    # Identify decimal and list validations
    decimal_dv = None
    list_dv = None
    for dv in validations:
        if dv.type == 'decimal':
            decimal_dv = dv
            print(f"INFO: Found decimal validation: sqref={dv.sqref}, formula1={dv.formula1}, formula2={dv.formula2}, operator={dv.operator}")
        elif dv.type == 'list':
            list_dv = dv
            print(f"INFO: Found list validation: sqref={dv.sqref}, formula1={dv.formula1}")
        elif dv.type == 'whole':
            # Some implementations might use 'whole' for integer-like decimals
            # but the task specifies 'decimal'
            print(f"INFO: Found whole validation (not decimal): sqref={dv.sqref}")

    # Component 1: Decimal validation exists on C2:C20 (0.3 points)
    try:
        if decimal_dv is not None:
            # Check that the sqref covers C2:C20
            sqref_str = str(decimal_dv.sqref).upper().replace(' ', '')
            if 'C2:C20' in sqref_str:
                print(f"PASS: Component 1 - Decimal validation found on C2:C20 (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 - Decimal validation exists but on {decimal_dv.sqref}, not C2:C20")
        else:
            print(f"FAIL: Component 1 - No decimal validation found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Decimal validation has correct bounds 0-1000000 with operator=between (0.2 points)
    try:
        if decimal_dv is not None:
            f1 = decimal_dv.formula1
            f2 = decimal_dv.formula2
            op = decimal_dv.operator

            # Normalize formula values for comparison
            f1_val = None
            f2_val = None
            try:
                f1_val = float(str(f1).strip())
            except (ValueError, TypeError):
                pass
            try:
                f2_val = float(str(f2).strip())
            except (ValueError, TypeError):
                pass

            bounds_ok = (f1_val is not None and abs(f1_val - 0.0) < 0.01 and
                         f2_val is not None and abs(f2_val - 1000000.0) < 0.01)
            operator_ok = (op == 'between')

            if bounds_ok and operator_ok:
                print(f"PASS: Component 2 - Correct bounds (0 to 1000000) with operator=between (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 - bounds_ok={bounds_ok} (f1={f1_val}, f2={f2_val}), operator={op}")
        else:
            print(f"FAIL: Component 2 - No decimal validation to check bounds")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: List validation exists on D2:D20 (0.3 points)
    try:
        if list_dv is not None:
            sqref_str = str(list_dv.sqref).upper().replace(' ', '')
            if 'D2:D20' in sqref_str:
                print(f"PASS: Component 3 - List validation found on D2:D20 (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 - List validation exists but on {list_dv.sqref}, not D2:D20")
        else:
            print(f"FAIL: Component 3 - No list validation found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: List validation formula references $G$1:$G$8 (0.2 points)
    try:
        if list_dv is not None:
            formula = str(list_dv.formula1).strip() if list_dv.formula1 else ''
            # Normalize: remove leading = and $, compare range
            normalized = formula.upper().replace(' ', '')
            # Accept =$G$1:$G$8 or $G$1:$G$8 or =G1:G8 etc.
            # Strip leading =
            if normalized.startswith('='):
                normalized = normalized[1:]
            # Remove $ signs for flexible matching
            clean = normalized.replace('$', '')
            if clean == 'G1:G8':
                print(f"PASS: Component 4 - List validation formula references G1:G8 (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 - List formula is '{formula}', expected reference to $G$1:$G$8")
        else:
            print(f"FAIL: Component 4 - No list validation to check formula")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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
