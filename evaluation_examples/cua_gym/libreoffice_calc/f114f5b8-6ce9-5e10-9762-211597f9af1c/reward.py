"""
Reward Script: Add dropdown validation to the 'Satisfaction Level' column (F2:F500)
Task ID: calc_dop_validate_dropdown_055
Domain: libreoffice_calc

Scoring Rubric:
  Component 1: Dropdown list validation applied to F2:F500             — 0.4 points
  Component 2: Dropdown options are exactly 5 correct values in order  — 0.4 points
  Component 3: Stop error alert with correct error message             — 0.2 points
  Total: 1.0

All components FAIL on the initial file (no data validation present) and PASS on golden.
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_dop_validate_dropdown_055'

# Expected dropdown options in exact order
EXPECTED_OPTIONS = ['Very Satisfied', 'Satisfied', 'Neutral', 'Dissatisfied', 'Very Dissatisfied']
EXPECTED_ERROR_MSG = 'Please select a valid satisfaction level from the dropdown'
TARGET_RANGE = 'F2:F500'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: can we load the file at all?
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: sheet must exist
    if 'SurveyResponses' not in wb.sheetnames:
        print("CRITICAL: Sheet 'SurveyResponses' not found.")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['SurveyResponses']
    dvs = ws.data_validations.dataValidation

    # Component 1: Dropdown list validation applied to F2:F500 (0.4 points)
    # This verifies that a list-type data validation covers F2:F500.
    # FAILS on initial file (0 validations) — PASSES on golden file.
    try:
        target_dv = None
        for dv in dvs:
            sqref_str = str(dv.sqref)
            if dv.type == 'list' and TARGET_RANGE in sqref_str:
                target_dv = dv
                break

        if target_dv is not None:
            print(f"PASS: Component 1 — list-type validation found on {TARGET_RANGE} (0.4 pts)")
            total_score += 0.4
        else:
            # Check if there's any validation on F column at all for more informative output
            f_col_dvs = [dv for dv in dvs if 'F' in str(dv.sqref)]
            if f_col_dvs:
                print(f"FAIL: Component 1 — validation on column F found but not list-type covering {TARGET_RANGE}. "
                      f"Found: type={f_col_dvs[0].type}, sqref={f_col_dvs[0].sqref}")
            else:
                print(f"FAIL: Component 1 — no list-type validation found on {TARGET_RANGE}. "
                      f"Total validations on sheet: {len(dvs)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        target_dv = None

    # Component 2: Dropdown options are exactly the 5 correct values in correct order (0.4 points)
    # Checks that formula1 contains exactly "Very Satisfied,Satisfied,Neutral,Dissatisfied,Very Dissatisfied"
    # in the correct order. FAILS on initial — PASSES on golden.
    try:
        if target_dv is None:
            print("FAIL: Component 2 — skipped because no target validation was found in Component 1")
        else:
            formula1 = target_dv.formula1 or ''
            # formula1 is stored as '"Very Satisfied,Satisfied,Neutral,Dissatisfied,Very Dissatisfied"'
            # Strip surrounding double quotes if present
            stripped = formula1.strip('"')
            actual_options = [opt.strip() for opt in stripped.split(',')]

            if actual_options == EXPECTED_OPTIONS:
                print(f"PASS: Component 2 — dropdown options are exactly correct: {actual_options} (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — dropdown options mismatch.")
                print(f"  Expected: {EXPECTED_OPTIONS}")
                print(f"  Actual:   {actual_options}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Stop error alert with correct error message (0.2 points)
    # Checks that errorStyle='stop' and the error message contains the expected text.
    # FAILS on initial — PASSES on golden.
    try:
        if target_dv is None:
            print("FAIL: Component 3 — skipped because no target validation was found in Component 1")
        else:
            error_style_ok = (target_dv.errorStyle == 'stop')
            error_msg = target_dv.error or ''
            error_msg_ok = (error_msg == EXPECTED_ERROR_MSG)

            if error_style_ok and error_msg_ok:
                print(f"PASS: Component 3 — stop error alert with correct message (0.2 pts)")
                print(f"  errorStyle: {target_dv.errorStyle}")
                print(f"  error: {target_dv.error}")
                total_score += 0.2
            else:
                if not error_style_ok:
                    print(f"FAIL: Component 3 — errorStyle expected 'stop', found '{target_dv.errorStyle}'")
                if not error_msg_ok:
                    print(f"FAIL: Component 3 — error message mismatch.")
                    print(f"  Expected: '{EXPECTED_ERROR_MSG}'")
                    print(f"  Actual:   '{error_msg}'")
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
