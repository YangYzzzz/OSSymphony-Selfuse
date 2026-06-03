"""
Reward Script: Data entry form validation checks
Task ID: calc_nrv_080
Domain: libreoffice_calc
Scoring:
  Component 1 (0.20) - B2 Name: textLength validation, between 2 and 50
  Component 2 (0.20) - B3 Age: whole number validation, between 18 and 120
  Component 3 (0.20) - B4 Email: custom formula with @ check
  Component 4 (0.20) - B5 Start Date: date validation, after 2020-01-01
  Component 5 (0.20) - B6 Role: list validation with 5 roles
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_080'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


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

    # Build a lookup of data validations by cell reference
    dvs = ws.data_validations.dataValidation
    dv_map = {}
    for dv in dvs:
        # sqref can contain multiple ranges; iterate
        for cell_range in dv.sqref.ranges:
            dv_map[str(cell_range)] = dv

    print(f"INFO: Found {len(dvs)} data validations total")
    print(f"INFO: Validation map keys: {list(dv_map.keys())}")

    # Component 1: B2 Name - textLength validation, between 2 and 50 (0.20 points)
    try:
        dv = dv_map.get('B2')
        if dv is not None and dv.type == 'textLength':
            op_ok = (dv.operator == 'between')
            f1_ok = (str(dv.formula1) == '2')
            f2_ok = (str(dv.formula2) == '50')
            if op_ok and f1_ok and f2_ok:
                print(f"PASS: Component 1 - B2 Name textLength between 2 and 50 (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 - B2 has textLength but wrong params: op={dv.operator}, f1={dv.formula1}, f2={dv.formula2}")
        else:
            dv_type = dv.type if dv else None
            print(f"FAIL: Component 1 - B2 expected textLength validation, found type={dv_type}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: B3 Age - whole number validation, between 18 and 120 (0.20 points)
    try:
        dv = dv_map.get('B3')
        if dv is not None and dv.type == 'whole':
            op_ok = (dv.operator == 'between')
            f1_ok = (str(dv.formula1) == '18')
            f2_ok = (str(dv.formula2) == '120')
            if op_ok and f1_ok and f2_ok:
                print(f"PASS: Component 2 - B3 Age whole number between 18 and 120 (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 - B3 has whole but wrong params: op={dv.operator}, f1={dv.formula1}, f2={dv.formula2}")
        else:
            dv_type = dv.type if dv else None
            print(f"FAIL: Component 2 - B3 expected whole validation, found type={dv_type}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: B4 Email - custom formula with @ check (0.20 points)
    try:
        dv = dv_map.get('B4')
        if dv is not None and dv.type == 'custom':
            formula = str(dv.formula1).upper().replace(' ', '')
            # Check that the formula references @ and B4
            has_at = '@' in str(dv.formula1)
            has_find_or_search = ('FIND' in formula or 'SEARCH' in formula)
            has_b4 = 'B4' in formula
            if has_at and has_find_or_search and has_b4:
                print(f"PASS: Component 3 - B4 Email custom formula with @ check (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 - B4 has custom but formula doesn't match: {dv.formula1}")
        else:
            dv_type = dv.type if dv else None
            print(f"FAIL: Component 3 - B4 expected custom validation, found type={dv_type}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: B5 Start Date - date validation, after 2020-01-01 (0.20 points)
    try:
        dv = dv_map.get('B5')
        if dv is not None and dv.type == 'date':
            op_ok = (dv.operator in ('greaterThan', 'greaterThanOrEqual'))
            # The formula1 should reference 2020-01-01 in some form
            f1_str = str(dv.formula1)
            date_ok = ('2020' in f1_str and '01' in f1_str)
            if op_ok and date_ok:
                print(f"PASS: Component 4 - B5 Start Date after 2020-01-01 (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 - B5 has date but wrong params: op={dv.operator}, f1={dv.formula1}")
        else:
            dv_type = dv.type if dv else None
            print(f"FAIL: Component 4 - B5 expected date validation, found type={dv_type}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: B6 Role - list validation with 5 roles (0.20 points)
    try:
        dv = dv_map.get('B6')
        if dv is not None and dv.type == 'list':
            formula = str(dv.formula1)
            # Expected roles: Manager, Developer, Designer, Analyst, QA
            expected_roles = {'manager', 'developer', 'designer', 'analyst', 'qa'}
            # Parse the list from formula like '"Manager,Developer,Designer,Analyst,QA"'
            clean = formula.strip('"').strip("'")
            actual_roles = {r.strip().lower() for r in clean.split(',')}
            if expected_roles == actual_roles:
                print(f"PASS: Component 5 - B6 Role list with correct 5 roles (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 - B6 has list but roles don't match. Expected={expected_roles}, Got={actual_roles}")
        else:
            dv_type = dv.type if dv else None
            print(f"FAIL: Component 5 - B6 expected list validation, found type={dv_type}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_calc")

file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
