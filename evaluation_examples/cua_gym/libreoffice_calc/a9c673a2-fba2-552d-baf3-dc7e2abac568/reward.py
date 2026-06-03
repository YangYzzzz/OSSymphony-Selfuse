"""
Reward Script: Set up data validation on hire date column (B2:B10) to only allow dates within last 2 years.
Task ID: calc_hr_030
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30) - Data validation exists on B2:B10 with type=date
  Component 2 (0.25) - Operator is 'between' with correct date formulas (TODAY()-730 and TODAY())
  Component 3 (0.25) - Error alert title is 'Invalid Date'
  Component 4 (0.20) - Error alert message is 'Hire date must be within the last 2 years'
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_hr_030'


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

    # Precondition: 'NewHires' sheet must exist
    if 'NewHires' not in wb.sheetnames:
        print("FAIL: Sheet 'NewHires' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['NewHires']
    validations = ws.data_validations.dataValidation

    # Find the data validation that covers B2:B10
    target_dv = None
    for dv in validations:
        sqref_str = str(dv.sqref)
        # Check if the validation covers B2:B10 (could be written as "B2:B10" or similar)
        if 'B2' in sqref_str and 'B10' in sqref_str:
            target_dv = dv
            break

    if target_dv is None:
        # Also check for any validation on column B covering the right range
        for dv in validations:
            sqref_str = str(dv.sqref)
            # Accept variations like B2:B10 or partial matches
            if 'B2' in sqref_str:
                target_dv = dv
                break

    # Component 1: Data validation exists on B2:B10 with type=date (0.30 points)
    try:
        if target_dv is not None and target_dv.type == 'date':
            # Verify the range includes B2:B10
            sqref_str = str(target_dv.sqref)
            print(f"PASS: Component 1 - Date validation found on {sqref_str} (0.30 pts)")
            total_score += 0.30
        elif target_dv is not None:
            print(f"FAIL: Component 1 - Validation found but type is '{target_dv.type}', expected 'date'")
        else:
            print(f"FAIL: Component 1 - No data validation found covering B2:B10 (found {len(validations)} total validations)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Operator is 'between' with correct date formulas (0.25 points)
    try:
        if target_dv is not None:
            op_ok = target_dv.operator == 'between'
            # Check formula1 and formula2
            f1 = str(target_dv.formula1).strip() if target_dv.formula1 else ''
            f2 = str(target_dv.formula2).strip() if target_dv.formula2 else ''

            # Normalize: remove spaces, uppercase
            f1_norm = f1.upper().replace(' ', '')
            f2_norm = f2.upper().replace(' ', '')

            # Accept TODAY()-730 for minimum and TODAY() for maximum
            formula1_ok = 'TODAY()-730' in f1_norm or 'TODAY()- 730' in f1_norm
            formula2_ok = f2_norm == 'TODAY()'

            if op_ok and formula1_ok and formula2_ok:
                print(f"PASS: Component 2 - operator='between', formula1='{f1}', formula2='{f2}' (0.25 pts)")
                total_score += 0.25
            else:
                details = []
                if not op_ok:
                    details.append(f"operator='{target_dv.operator}' (expected 'between')")
                if not formula1_ok:
                    details.append(f"formula1='{f1}' (expected 'TODAY()-730')")
                if not formula2_ok:
                    details.append(f"formula2='{f2}' (expected 'TODAY()')")
                print(f"FAIL: Component 2 - {'; '.join(details)}")
        else:
            print("FAIL: Component 2 - No target validation found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Error alert title is 'Invalid Date' (0.25 points)
    try:
        if target_dv is not None:
            error_title = target_dv.errorTitle if target_dv.errorTitle else ''
            if error_title.strip() == 'Invalid Date':
                print(f"PASS: Component 3 - errorTitle='{error_title}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 - errorTitle='{error_title}', expected 'Invalid Date'")
        else:
            print("FAIL: Component 3 - No target validation found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Error alert message is 'Hire date must be within the last 2 years' (0.20 points)
    try:
        if target_dv is not None:
            error_msg = target_dv.error if target_dv.error else ''
            if error_msg.strip() == 'Hire date must be within the last 2 years':
                print(f"PASS: Component 4 - error='{error_msg}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 - error='{error_msg}', expected 'Hire date must be within the last 2 years'")
        else:
            print("FAIL: Component 4 - No target validation found")
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
