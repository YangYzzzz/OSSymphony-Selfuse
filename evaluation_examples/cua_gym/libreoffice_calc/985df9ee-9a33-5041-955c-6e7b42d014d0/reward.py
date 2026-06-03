"""
Reward Script: Data validation on D2:D25 for future dates only
Task ID: calc_gcv_074
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): Custom data validation exists on D2:D25
  Component 2 (0.25): Formula is =D2>TODAY()
  Component 3 (0.25): Error alert configured (stop, 'Past Date', 'Only future dates are allowed.')
  Component 4 (0.25): Input message configured ('Check-in Date', 'Enter a future date.')
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_074'


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

    # Precondition: sheet name should be Reservation_System
    if ws.title != "Reservation_System":
        # Try to find it
        if "Reservation_System" in wb.sheetnames:
            ws = wb["Reservation_System"]
        else:
            print(f"WARN: Active sheet is '{ws.title}', expected 'Reservation_System'. Proceeding with active sheet.")

    # Find the relevant data validation (if any) that covers D2:D25
    target_dv = None
    dvs = ws.data_validations.dataValidation
    for dv in dvs:
        sqref_str = str(dv.sqref).upper().replace(" ", "")
        if "D2:D25" in sqref_str or "D2:D25" == sqref_str:
            target_dv = dv
            break

    # Component 1: Custom data validation exists on D2:D25 (0.25 points)
    try:
        if target_dv is not None and target_dv.type == "custom":
            print(f"PASS: Component 1 - Custom data validation found on D2:D25 (type={target_dv.type}) (0.25 pts)")
            total_score += 0.25
        elif target_dv is not None:
            print(f"FAIL: Component 1 - Data validation found on D2:D25 but type is '{target_dv.type}', expected 'custom'")
        else:
            # Check if there's any DV that at least partially covers D2:D25
            print(f"FAIL: Component 1 - No data validation found covering D2:D25. Found {len(dvs)} validation(s):")
            for dv in dvs:
                print(f"  DV: type={dv.type}, sqref={dv.sqref}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Formula is =D2>TODAY() (0.25 points)
    try:
        if target_dv is not None and target_dv.formula1 is not None:
            formula = str(target_dv.formula1).strip()
            # Normalize for comparison: remove spaces, uppercase
            formula_norm = formula.upper().replace(" ", "")
            expected_norm = "=D2>TODAY()"
            if formula_norm == expected_norm:
                print(f"PASS: Component 2 - Formula matches: {formula} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 - Formula mismatch. Expected '=D2>TODAY()', found '{formula}'")
        else:
            print(f"FAIL: Component 2 - No target data validation or no formula1 set")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Error alert configuration (0.25 points)
    # Expected: errorStyle=stop, errorTitle='Past Date', error='Only future dates are allowed.'
    try:
        if target_dv is not None:
            checks_passed = 0
            total_checks = 3

            # Error style
            error_style = str(target_dv.errorStyle).lower() if target_dv.errorStyle else ""
            if error_style == "stop":
                checks_passed += 1
            else:
                print(f"  DETAIL: errorStyle expected 'stop', found '{error_style}'")

            # Error title
            error_title = str(target_dv.errorTitle).strip() if target_dv.errorTitle else ""
            if error_title == "Past Date":
                checks_passed += 1
            else:
                print(f"  DETAIL: errorTitle expected 'Past Date', found '{error_title}'")

            # Error message
            error_msg = str(target_dv.error).strip() if target_dv.error else ""
            if error_msg == "Only future dates are allowed.":
                checks_passed += 1
            else:
                print(f"  DETAIL: error message expected 'Only future dates are allowed.', found '{error_msg}'")

            if checks_passed == total_checks:
                print(f"PASS: Component 3 - Error alert correctly configured (stop/Past Date/message) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 - Error alert partially configured ({checks_passed}/{total_checks} correct)")
        else:
            print(f"FAIL: Component 3 - No target data validation found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Input message configuration (0.25 points)
    # Expected: promptTitle='Check-in Date', prompt='Enter a future date.'
    try:
        if target_dv is not None:
            checks_passed = 0
            total_checks = 2

            # Input message title
            prompt_title = str(target_dv.promptTitle).strip() if target_dv.promptTitle else ""
            if prompt_title == "Check-in Date":
                checks_passed += 1
            else:
                print(f"  DETAIL: promptTitle expected 'Check-in Date', found '{prompt_title}'")

            # Input message
            prompt_msg = str(target_dv.prompt).strip() if target_dv.prompt else ""
            if prompt_msg == "Enter a future date.":
                checks_passed += 1
            else:
                print(f"  DETAIL: prompt expected 'Enter a future date.', found '{prompt_msg}'")

            if checks_passed == total_checks:
                print(f"PASS: Component 4 - Input message correctly configured (Check-in Date/Enter a future date.) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 - Input message partially configured ({checks_passed}/{total_checks} correct)")
        else:
            print(f"FAIL: Component 4 - No target data validation found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
