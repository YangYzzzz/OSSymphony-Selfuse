"""
Reward Script: Add data validation to B2:B30 for whole numbers between 2020 and 2030
Task ID: calc_dop_validate_integer_062
Domain: libreoffice_calc
Scoring:
  Component 1: Data validation exists on B2:B30 with type='whole'  (0.4 pts)
  Component 2: Validation range is 'between' 2020 and 2030          (0.3 pts)
  Component 3: Stop error message matches required text              (0.3 pts)
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_dop_validate_integer_062'
SHEET_NAME = 'FiscalReports'
EXPECTED_DV_SQREF = 'B2:B30'
EXPECTED_DV_TYPE = 'whole'
EXPECTED_OPERATOR = 'between'
EXPECTED_FORMULA1 = '2020'
EXPECTED_FORMULA2 = '2030'
EXPECTED_ERROR_MSG = 'Please enter a valid fiscal year between 2020 and 2030'


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

    # Gate: check that FiscalReports sheet exists
    if SHEET_NAME not in wb.sheetnames:
        print(f"CRITICAL: Sheet '{SHEET_NAME}' not found in workbook.")
        print("REWARD: 0.0")
        return 0.0

    ws = wb[SHEET_NAME]

    # Locate the data validation that covers B2:B30
    found_dv = None
    all_dvs = ws.data_validations.dataValidation
    for dv in all_dvs:
        sqref_str = str(dv.sqref)
        # Accept if the sqref contains or equals the expected range
        if EXPECTED_DV_SQREF in sqref_str or sqref_str == EXPECTED_DV_SQREF:
            found_dv = dv
            break

    # Component 1: Whole-number data validation applied to B2:B30 (0.4 points)
    # This fails on initial (no validations) and passes on golden.
    try:
        if found_dv is not None and found_dv.type == EXPECTED_DV_TYPE:
            print(f"PASS: Component 1 — Data validation type='{EXPECTED_DV_TYPE}' found on {EXPECTED_DV_SQREF} (0.4 pts)")
            total_score += 0.4
        else:
            if found_dv is None:
                print(f"FAIL: Component 1 — No data validation found covering {EXPECTED_DV_SQREF} (found {len(all_dvs)} total validations)")
            else:
                print(f"FAIL: Component 1 — Expected type='{EXPECTED_DV_TYPE}', found type='{found_dv.type}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Validation restricts to values between 2020 and 2030 (0.3 points)
    # This fails on initial (no validations) and passes on golden.
    try:
        if (found_dv is not None
                and found_dv.operator == EXPECTED_OPERATOR
                and str(found_dv.formula1).strip() == EXPECTED_FORMULA1
                and str(found_dv.formula2).strip() == EXPECTED_FORMULA2):
            print(f"PASS: Component 2 — Validation restricts to between {EXPECTED_FORMULA1} and {EXPECTED_FORMULA2} (0.3 pts)")
            total_score += 0.3
        else:
            if found_dv is None:
                print("FAIL: Component 2 — No matching data validation found")
            else:
                print(f"FAIL: Component 2 — Expected operator='{EXPECTED_OPERATOR}', formula1='{EXPECTED_FORMULA1}', formula2='{EXPECTED_FORMULA2}'; "
                      f"found operator='{found_dv.operator}', formula1='{found_dv.formula1}', formula2='{found_dv.formula2}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Stop error message is shown and matches required text (0.3 points)
    # The task requires a stop error alert with the specific message.
    # This fails on initial (no validations) and passes on golden.
    try:
        if found_dv is not None and found_dv.showErrorMessage:
            actual_error = (found_dv.error or '').strip()
            if actual_error.lower() == EXPECTED_ERROR_MSG.lower():
                print(f"PASS: Component 3 — Stop error message matches: '{actual_error}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Error message mismatch.")
                print(f"  Expected: '{EXPECTED_ERROR_MSG}'")
                print(f"  Found:    '{actual_error}'")
        else:
            if found_dv is None:
                print("FAIL: Component 3 — No matching data validation found")
            else:
                print(f"FAIL: Component 3 — showErrorMessage is not True (value: {found_dv.showErrorMessage})")
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
