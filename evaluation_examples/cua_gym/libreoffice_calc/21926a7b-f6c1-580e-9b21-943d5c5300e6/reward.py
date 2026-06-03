"""
Reward Script: Timesheet data validation for hours columns
Task ID: calc_nrv_087
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): C2:C31 has decimal validation with min=0, max=12
  Component 2 (0.25): C2:C31 has input message 'Enter regular hours (0-12)'
  Component 3 (0.25): D2:D31 has decimal validation with min=0, max=8
  Component 4 (0.25): D2:D31 has input message 'Enter overtime hours (0-8)'
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_087'


def find_validation_for_range(validations, target_range_str):
    """Find a DataValidation object that covers the target cell range."""
    for dv in validations:
        # sqref can contain multiple ranges; check if target is among them
        sqref_str = str(dv.sqref).upper().replace(' ', '')
        target_upper = target_range_str.upper().replace(' ', '')
        # Could be exact match or part of a multi-range sqref
        if target_upper in sqref_str.split():
            return dv
        if target_upper == sqref_str:
            return dv
        # Also check if the ranges overlap significantly
        # For simplicity, check containment as string
        if target_upper in sqref_str:
            return dv
    return None


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
    validations = ws.data_validations.dataValidation

    # Component 1: C2:C31 has decimal validation with min=0, max=12 (0.25 pts)
    try:
        dv_c = find_validation_for_range(validations, 'C2:C31')
        if dv_c is not None:
            is_decimal = (dv_c.type == 'decimal')
            is_between = (dv_c.operator is None or dv_c.operator == 'between')
            min_ok = (str(dv_c.formula1).strip() == '0')
            max_ok = (str(dv_c.formula2).strip() == '12')
            if is_decimal and is_between and min_ok and max_ok:
                print(f"PASS: Component 1 - C2:C31 decimal validation 0-12 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 - C2:C31 validation properties wrong: type={dv_c.type}, operator={dv_c.operator}, formula1={dv_c.formula1}, formula2={dv_c.formula2}")
        else:
            print(f"FAIL: Component 1 - No data validation found covering C2:C31")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: C2:C31 input message 'Enter regular hours (0-12)' (0.25 pts)
    try:
        dv_c = find_validation_for_range(validations, 'C2:C31')
        if dv_c is not None:
            has_input_msg = dv_c.showInputMessage in (True, None, 1)
            prompt_text = str(dv_c.prompt).strip() if dv_c.prompt else ''
            expected_prompt = 'Enter regular hours (0-12)'
            prompt_match = (prompt_text.lower() == expected_prompt.lower())
            if has_input_msg and prompt_match:
                print(f"PASS: Component 2 - C2:C31 input message correct: '{prompt_text}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 - C2:C31 input message: showInputMessage={dv_c.showInputMessage}, prompt='{prompt_text}' (expected '{expected_prompt}')")
        else:
            print(f"FAIL: Component 2 - No data validation found covering C2:C31")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: D2:D31 has decimal validation with min=0, max=8 (0.25 pts)
    try:
        dv_d = find_validation_for_range(validations, 'D2:D31')
        if dv_d is not None:
            is_decimal = (dv_d.type == 'decimal')
            is_between = (dv_d.operator is None or dv_d.operator == 'between')
            min_ok = (str(dv_d.formula1).strip() == '0')
            max_ok = (str(dv_d.formula2).strip() == '8')
            if is_decimal and is_between and min_ok and max_ok:
                print(f"PASS: Component 3 - D2:D31 decimal validation 0-8 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 - D2:D31 validation properties wrong: type={dv_d.type}, operator={dv_d.operator}, formula1={dv_d.formula1}, formula2={dv_d.formula2}")
        else:
            print(f"FAIL: Component 3 - No data validation found covering D2:D31")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: D2:D31 input message 'Enter overtime hours (0-8)' (0.25 pts)
    try:
        dv_d = find_validation_for_range(validations, 'D2:D31')
        if dv_d is not None:
            has_input_msg = dv_d.showInputMessage in (True, None, 1)
            prompt_text = str(dv_d.prompt).strip() if dv_d.prompt else ''
            expected_prompt = 'Enter overtime hours (0-8)'
            prompt_match = (prompt_text.lower() == expected_prompt.lower())
            if has_input_msg and prompt_match:
                print(f"PASS: Component 4 - D2:D31 input message correct: '{prompt_text}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 - D2:D31 input message: showInputMessage={dv_d.showInputMessage}, prompt='{prompt_text}' (expected '{expected_prompt}')")
        else:
            print(f"FAIL: Component 4 - No data validation found covering D2:D31")
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
