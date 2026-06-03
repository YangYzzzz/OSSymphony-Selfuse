"""
Reward Script: Email format data validation on B2:B40
Task ID: calc_gcv_068
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Data validation exists on B2:B40 with type=custom
  Component 2 (0.3): Formula contains email-format checks (AND, FIND("@"...), FIND("."...), FIND(" "...))
  Component 3 (0.2): Error style is 'stop' and error title is 'Invalid Email'
  Component 4 (0.2): Error message is 'Please enter a valid email address.'
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_068'


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

    # Find the Contact_Form sheet (or active sheet)
    ws = None
    if 'Contact_Form' in wb.sheetnames:
        ws = wb['Contact_Form']
    else:
        ws = wb.active
    print(f"INFO: Using sheet '{ws.title}'")

    # Get data validations
    dvs = ws.data_validations.dataValidation
    print(f"INFO: Found {len(dvs)} data validation(s)")

    if len(dvs) == 0:
        print("FAIL: No data validations found")
        print("REWARD: 0.0")
        return 0.0

    # Find the relevant data validation (type=custom on column B)
    target_dv = None
    for dv in dvs:
        if dv.type == 'custom':
            sqref_str = str(dv.sqref)
            # Check if it covers B column cells
            if 'B' in sqref_str:
                target_dv = dv
                break

    if target_dv is None:
        # Fallback: check any custom validation
        for dv in dvs:
            if dv.type == 'custom':
                target_dv = dv
                break

    if target_dv is None:
        print("FAIL: No custom data validation found")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found custom DV: sqref={target_dv.sqref}, formula1={target_dv.formula1}")

    # Component 1: Data validation exists on B2:B40 with type=custom (0.3 points)
    try:
        sqref_str = str(target_dv.sqref).replace(' ', '')
        # Check that the range covers B2:B40
        range_ok = ('B2:B40' in sqref_str)

        if target_dv.type == 'custom' and range_ok:
            print(f"PASS: Component 1 -- Custom DV on B2:B40 (0.3 pts)")
            total_score += 0.3
        elif target_dv.type == 'custom':
            # Partial: custom type but different range
            print(f"PARTIAL: Component 1 -- Custom DV found but range is '{sqref_str}', expected B2:B40 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- DV type is '{target_dv.type}', expected 'custom'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Formula checks email format (0.3 points)
    try:
        formula = str(target_dv.formula1) if target_dv.formula1 else ''
        formula_upper = formula.upper()
        formula_nospace = formula_upper.replace(' ', '')
        print(f"INFO: Formula: {formula}")

        # Check for key parts of the email validation formula
        # NOTE: Do NOT strip spaces from formula when checking for FIND(" ",...)
        # because the space character inside quotes is the search target
        has_and = 'AND(' in formula_nospace
        has_find_at = 'FIND("@"' in formula_upper or 'FIND("@"' in formula
        has_find_dot = 'FIND("."' in formula_upper or 'FIND("."' in formula
        # For space check, look in the original formula (spaces preserved)
        has_find_space = 'FIND(" "' in formula or "FIND(' '" in formula
        has_iserror = 'ISERROR' in formula_nospace

        checks_passed = sum([has_and, has_find_at, has_find_dot, has_find_space, has_iserror])
        print(f"INFO: Formula checks -- AND={has_and}, FIND(@)={has_find_at}, FIND(.)={has_find_dot}, FIND(space)={has_find_space}, ISERROR={has_iserror}")

        if checks_passed == 5:
            print(f"PASS: Component 2 -- Email validation formula has all required parts (0.3 pts)")
            total_score += 0.3
        elif checks_passed >= 3:
            pts = 0.15
            print(f"PARTIAL: Component 2 -- Formula has {checks_passed}/5 required parts ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 2 -- Formula has only {checks_passed}/5 required parts")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Error style is 'stop' and error title is 'Invalid Email' (0.2 points)
    try:
        error_style = str(target_dv.errorStyle).lower() if target_dv.errorStyle else ''
        error_title = str(target_dv.errorTitle) if target_dv.errorTitle else ''

        style_ok = error_style == 'stop'
        title_ok = error_title.strip().lower() == 'invalid email'

        if style_ok and title_ok:
            print(f"PASS: Component 3 -- Error style='stop', title='Invalid Email' (0.2 pts)")
            total_score += 0.2
        elif style_ok or title_ok:
            pts = 0.1
            print(f"PARTIAL: Component 3 -- style_ok={style_ok} ('{error_style}'), title_ok={title_ok} ('{error_title}') ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 3 -- style='{error_style}' (expected 'stop'), title='{error_title}' (expected 'Invalid Email')")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Error message is 'Please enter a valid email address.' (0.2 points)
    try:
        error_msg = str(target_dv.error) if target_dv.error else ''
        expected_msg = 'Please enter a valid email address.'

        if error_msg.strip().lower() == expected_msg.lower():
            print(f"PASS: Component 4 -- Error message matches (0.2 pts)")
            total_score += 0.2
        elif 'valid email' in error_msg.lower():
            pts = 0.1
            print(f"PARTIAL: Component 4 -- Error message partially matches: '{error_msg}' ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 4 -- Error message is '{error_msg}', expected '{expected_msg}'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
