"""
Reward Script: Data validation for cell E2 with Information-style error alert
Task ID: calc_nrv_072
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25) - Data validation exists on E2 with type 'whole'
  Component 2 (0.25) - Validation range is 10-50 (formula1=10, formula2=50)
  Component 3 (0.25) - Error style is 'information' (not 'stop' or 'warning')
  Component 4 (0.25) - Error title is 'Note' and message matches expected text
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_072'


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

    # Precondition: E1 should still be 'Order Quantity' (data integrity gate)
    try:
        e1_val = ws['E1'].value
        if e1_val != 'Order Quantity':
            print(f"WARN: E1 expected 'Order Quantity', found '{e1_val}' — proceeding anyway")
    except Exception as e:
        print(f"WARN: Could not read E1: {e}")

    # Find data validation targeting E2
    dv_for_e2 = None
    try:
        for dv in ws.data_validations.dataValidation:
            sqref_str = str(dv.sqref)
            if 'E2' in sqref_str:
                dv_for_e2 = dv
                break
    except Exception as e:
        print(f"ERROR: Could not read data validations: {e}")

    if dv_for_e2 is None:
        print("FAIL: No data validation found targeting cell E2")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Data validation exists on E2 with type 'whole' (0.25 points)
    try:
        if dv_for_e2.type == 'whole':
            print(f"PASS: Component 1 — Data validation on E2 has type 'whole' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected type 'whole', found '{dv_for_e2.type}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Validation range formula1=10 and formula2=50 (0.25 points)
    try:
        f1 = str(dv_for_e2.formula1).strip() if dv_for_e2.formula1 is not None else None
        f2 = str(dv_for_e2.formula2).strip() if dv_for_e2.formula2 is not None else None
        if f1 == '10' and f2 == '50':
            print(f"PASS: Component 2 — Validation range is 10-50 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected formula1='10', formula2='50', found '{f1}', '{f2}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error style is 'information' (0.25 points)
    try:
        error_style = dv_for_e2.errorStyle
        if error_style is not None and error_style.lower() == 'information':
            print(f"PASS: Component 3 — Error style is 'information' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Expected errorStyle 'information', found '{error_style}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Error title is 'Note' and error message matches (0.25 points)
    try:
        title_ok = dv_for_e2.errorTitle == 'Note'
        expected_msg = 'The recommended range is 10-50. You entered a value outside this range.'
        msg_ok = dv_for_e2.error == expected_msg

        if title_ok and msg_ok:
            print(f"PASS: Component 4 — Error title 'Note' and message match (0.25 pts)")
            total_score += 0.25
        else:
            if not title_ok:
                print(f"FAIL: Component 4 — Expected errorTitle 'Note', found '{dv_for_e2.errorTitle}'")
            if not msg_ok:
                print(f"FAIL: Component 4 — Expected error message '{expected_msg}', found '{dv_for_e2.error}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
