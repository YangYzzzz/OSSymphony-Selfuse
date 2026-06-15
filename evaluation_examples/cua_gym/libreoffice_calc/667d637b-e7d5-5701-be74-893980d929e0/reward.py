"""
Reward Script: Apply data validation to D2:D100 with custom formula
Task ID: calc_gao_007
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30): Data validation exists on D2:D100 with type "custom"
  Component 2 (0.35): Formula uses AND(D2<=TODAY(), D2>=TODAY()-365)
  Component 3 (0.20): Error style is "stop"
  Component 4 (0.15): Error message is present
"""

import os
import re

import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gao_007'


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

    # Precondition: 'Expenses' sheet must exist
    if 'Expenses' not in wb.sheetnames:
        print("CRITICAL: 'Expenses' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Expenses']
    validations = ws.data_validations.dataValidation

    # Find the relevant data validation targeting D column cells
    target_dv = None
    for dv in validations:
        sqref_str = str(dv.sqref).upper()
        # Check if this validation covers D2:D100 (or a range in column D)
        if 'D' in sqref_str:
            target_dv = dv
            break

    # Component 1: Data validation exists on D2:D100 with type "custom" (0.30 points)
    try:
        if target_dv is not None:
            dv_type = target_dv.type
            sqref_str = str(target_dv.sqref).upper().replace(' ', '')
            # Check type is custom
            is_custom = (dv_type == 'custom')
            # Check range covers D2:D100
            covers_range = ('D2:D100' in sqref_str)
            if is_custom and covers_range:
                print(f"PASS: Component 1 -- Custom validation on D2:D100 (type={dv_type}, sqref={sqref_str}) (0.30 pts)")
                total_score += 0.30
            elif is_custom:
                # Custom type but maybe slightly different range
                print(f"PARTIAL: Component 1 -- Custom validation found but range is {sqref_str}, expected D2:D100 (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 -- Validation type is '{dv_type}', expected 'custom'. sqref={sqref_str}")
        else:
            print("FAIL: Component 1 -- No data validation found targeting column D")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Formula uses AND(D2<=TODAY(), D2>=TODAY()-365) (0.35 points)
    try:
        if target_dv is not None and target_dv.formula1:
            formula = str(target_dv.formula1).upper().replace(' ', '')
            print(f"  DEBUG: Normalized formula = {formula}")

            # Check key elements of the formula
            has_and = 'AND(' in formula
            has_today = 'TODAY()' in formula
            has_lte_today = ('<=TODAY()' in formula or '<=TODAY(),' in formula)
            has_gte_past = ('>=TODAY()-365' in formula)

            if has_and and has_today and has_lte_today and has_gte_past:
                print(f"PASS: Component 2 -- Formula correctly uses AND(D2<=TODAY(),D2>=TODAY()-365) (0.35 pts)")
                total_score += 0.35
            elif has_and and has_today:
                # Has AND and TODAY but formula structure differs slightly
                print(f"PARTIAL: Component 2 -- Formula has AND+TODAY but structure differs: {formula} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 -- Formula missing key elements. has_and={has_and}, has_today={has_today}, formula={formula}")
        else:
            print("FAIL: Component 2 -- No formula found in data validation")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Error style is "stop" (0.20 points)
    try:
        if target_dv is not None:
            error_style = target_dv.errorStyle
            if error_style and error_style.lower() == 'stop':
                print(f"PASS: Component 3 -- Error style is 'stop' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 -- Error style is '{error_style}', expected 'stop'")
        else:
            print("FAIL: Component 3 -- No data validation found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Error message is present and meaningful (0.15 points)
    try:
        if target_dv is not None:
            error_msg = target_dv.error
            show_error = target_dv.showErrorMessage
            if error_msg and len(str(error_msg).strip()) > 5 and show_error:
                print(f"PASS: Component 4 -- Error message present: '{error_msg}' (0.15 pts)")
                total_score += 0.15
            elif error_msg and len(str(error_msg).strip()) > 5:
                print(f"PARTIAL: Component 4 -- Error message present but showErrorMessage={show_error} (0.08 pts)")
                total_score += 0.08
            else:
                print(f"FAIL: Component 4 -- Error message missing or too short: '{error_msg}'")
        else:
            print("FAIL: Component 4 -- No data validation found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
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
