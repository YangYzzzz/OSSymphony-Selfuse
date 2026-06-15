"""
Reward Script: Add data validation dropdown to cells D2:D50 in Tasks sheet
Task ID: calc_dop_validate_dropdown_019
Domain: libreoffice_calc
Scoring:
  Component 1: Data validation exists on Tasks sheet (0.3 pts)
  Component 2: Validation covers exactly the D2:D50 range (0.3 pts)
  Component 3: Dropdown list contains exactly the 4 required values (0.3 pts)
  Component 4: Error alert is 'stop' type (rejecting invalid entries) (0.1 pts)
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_dop_validate_dropdown_019'

EXPECTED_VALUES = ['Not Started', 'In Progress', 'Blocked', 'Completed']
EXPECTED_RANGE = 'D2:D50'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that data validation dropdown was added to D2:D50 in Tasks sheet.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Tasks sheet must exist
    if 'Tasks' not in wb.sheetnames:
        print("FAIL: 'Tasks' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Tasks']
    dvs = ws.data_validations.dataValidation

    # Component 1: Data validation exists on the Tasks sheet (0.3 points)
    # This FAILS on initial (0 validations) and PASSES on golden (1 validation)
    try:
        dv_list_validations = [dv for dv in dvs if dv.type == 'list']
        if len(dv_list_validations) >= 1:
            print(f"PASS: Component 1 — Data validation (list type) found on Tasks sheet ({len(dv_list_validations)} validation(s)) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No list-type data validation found on Tasks sheet. Found {len(dvs)} total validations (0 list type).")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if total_score == 0.0:
        # No list validation found at all — skip further checks
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Find the list data validation that applies to column D
    target_dv = None
    for dv in dv_list_validations:
        sqref_str = str(dv.sqref)
        if 'D' in sqref_str:
            target_dv = dv
            break

    if target_dv is None:
        print("FAIL: No list-type data validation applied to column D found.")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Validation covers exactly the D2:D50 range (0.3 points)
    # This FAILS on initial (no validation) and PASSES on golden (D2:D50)
    try:
        sqref_str = str(target_dv.sqref).strip()
        # Normalize: the sqref may have multiple ranges or just one
        # Accept D2:D50 as the range (possibly part of a multi-range sqref)
        if sqref_str == EXPECTED_RANGE or EXPECTED_RANGE in sqref_str.split(' '):
            print(f"PASS: Component 2 — Validation covers D2:D50 exactly (sqref='{sqref_str}') (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected range '{EXPECTED_RANGE}', found '{sqref_str}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Dropdown list contains exactly the 4 required values (0.3 points)
    # This FAILS on initial (no validation) and PASSES on golden (correct 4 values)
    try:
        formula1 = target_dv.formula1
        if formula1:
            # formula1 is stored as: '"Not Started,In Progress,Blocked,Completed"'
            items_str = formula1.strip('"')
            actual_items = [item.strip() for item in items_str.split(',')]
            if actual_items == EXPECTED_VALUES:
                print(f"PASS: Component 3 — Dropdown has exactly the 4 required values: {actual_items} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Expected values {EXPECTED_VALUES}, found {actual_items}")
        else:
            print(f"FAIL: Component 3 — formula1 is empty or None for the data validation")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Error alert is 'stop' type to reject invalid entries (0.1 points)
    # This FAILS on initial (no validation) and PASSES on golden (errorStyle='stop')
    try:
        show_error = target_dv.showErrorMessage
        error_style = target_dv.errorStyle
        if show_error and error_style == 'stop':
            print(f"PASS: Component 4 — Error alert is 'stop' type (showErrorMessage={show_error}, errorStyle='{error_style}') (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — Expected Stop error alert (showErrorMessage=True, errorStyle='stop'), found showErrorMessage={show_error}, errorStyle='{error_style}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
