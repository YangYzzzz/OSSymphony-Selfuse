"""
Reward Script: Add date validation to the 'Deadline' column (E2:E30)
Task ID: calc_dop_validate_date_023
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Data validation exists in 'Projects' sheet covering E2:E30
  Component 2 (0.4): Validation type is 'date', operator is 'between',
                      formula1=2025-01-01, formula2=2025-12-31
  Component 3 (0.3): Error style is 'stop' and error message is 'Deadline must be in 2025'
Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_dop_validate_date_023'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Projects' sheet must exist
    if 'Projects' not in wb.sheetnames:
        print("CRITICAL: Sheet 'Projects' not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Projects']

    # Retrieve all data validations on the sheet
    dvs = ws.data_validations.dataValidation

    # Component 1: Data validation exists and covers E2:E30 (0.3 points)
    # This FAILS on initial (no DV) and PASSES on golden (DV present on E2:E30)
    try:
        matching_dv = None
        for dv in dvs:
            sqref_str = str(dv.sqref)
            # Check if the validation covers E2:E30 (exact or superset)
            if 'E2:E30' in sqref_str or sqref_str == 'E2:E30':
                matching_dv = dv
                break
        if matching_dv is not None:
            print(f"PASS: Component 1 — Data validation found covering E2:E30 (sqref: {matching_dv.sqref}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No data validation found covering E2:E30 (found {len(dvs)} DV(s))")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Validation type is 'date', operator is 'between',
    #              formula1 = 2025-01-01, formula2 = 2025-12-31 (0.4 points)
    # This FAILS on initial (no DV) and PASSES on golden (correct date range)
    try:
        if matching_dv is not None:
            dv_type = (matching_dv.type or '').lower()
            dv_operator = (matching_dv.operator or '').lower()
            dv_formula1 = str(matching_dv.formula1 or '').strip()
            dv_formula2 = str(matching_dv.formula2 or '').strip()

            type_ok = (dv_type == 'date')
            operator_ok = (dv_operator == 'between')
            formula1_ok = ('2025-01-01' in dv_formula1)
            formula2_ok = ('2025-12-31' in dv_formula2)

            if type_ok and operator_ok and formula1_ok and formula2_ok:
                print(f"PASS: Component 2 — type={dv_type}, operator={dv_operator}, "
                      f"formula1={dv_formula1}, formula2={dv_formula2} (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — type_ok={type_ok} ({dv_type}), "
                      f"operator_ok={operator_ok} ({dv_operator}), "
                      f"formula1_ok={formula1_ok} ({dv_formula1}), "
                      f"formula2_ok={formula2_ok} ({dv_formula2})")
        else:
            print("FAIL: Component 2 — Skipped (no matching DV from Component 1)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error style is 'stop' and error message is 'Deadline must be in 2025' (0.3 points)
    # This FAILS on initial (no DV) and PASSES on golden (correct stop error)
    try:
        if matching_dv is not None:
            error_style = (matching_dv.errorStyle or '').lower()
            error_msg = (matching_dv.error or '').strip()

            style_ok = (error_style == 'stop')
            msg_ok = (error_msg == 'Deadline must be in 2025')

            if style_ok and msg_ok:
                print(f"PASS: Component 3 — errorStyle={error_style}, "
                      f"error='{error_msg}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — style_ok={style_ok} (errorStyle='{error_style}'), "
                      f"msg_ok={msg_ok} (error='{error_msg}')")
        else:
            print("FAIL: Component 3 — Skipped (no matching DV from Component 1)")
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
