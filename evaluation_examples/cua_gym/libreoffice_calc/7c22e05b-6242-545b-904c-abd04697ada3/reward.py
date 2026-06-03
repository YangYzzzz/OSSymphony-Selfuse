"""
Reward Script: Set up data validation system for lab equipment reservation sheet
Task ID: calc_edu_equipment_reservation_036
Domain: libreoffice_calc

Scoring Rubric:
  Component 1 (0.30): Equipment Name validation (B2:B76) — list from EquipmentList!$A$1:$A$15 with error alert
  Component 2 (0.30): Status validation (F2:F76) — dropdown list 'Reserved,In Use,Returned' with error alert
  Component 3 (0.20): Checkout Date validation (D2:D76) — date between 2025-01-01 and 2025-12-31 with error alert
  Component 4 (0.20): Return Date validation (E2:E76) — date between 2025-01-01 and 2025-12-31 with error alert
  Total: 1.0

Note: The initial file has 0 data validations. All validations are task-introduced changes.
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_edu_equipment_reservation_036'


def normalize_sqref(sqref_obj):
    """Return the string representation of a cell range reference."""
    return str(sqref_obj)


def find_validation(dvs, expected_type, expected_sqref_contains):
    """Find a data validation matching the given type and covering the expected range."""
    for dv in dvs:
        if dv.type == expected_type:
            sqref_str = normalize_sqref(dv.sqref)
            if expected_sqref_contains in sqref_str:
                return dv
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load workbook — precondition gate
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check that required sheets exist — precondition gate
    if 'Reservations' not in wb.sheetnames:
        print("CRITICAL: Sheet 'Reservations' not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Reservations']
    dvs = ws.data_validations.dataValidation

    # Component 1: Equipment Name validation on B2:B76 (0.30 points)
    # Must be type=list, reference EquipmentList!$A$1:$A$15, with showErrorMessage=True
    try:
        dv_eq = find_validation(dvs, 'list', 'B2')
        if dv_eq is None:
            # Also try finding by formula1 content
            for dv in dvs:
                if dv.type == 'list' and dv.formula1 and 'EquipmentList' in str(dv.formula1):
                    dv_eq = dv
                    break

        if dv_eq is not None:
            formula1 = str(dv_eq.formula1) if dv_eq.formula1 else ''
            sqref_str = normalize_sqref(dv_eq.sqref)
            has_equipment_source = 'EquipmentList' in formula1 and 'A1' in formula1.replace('$', '')
            covers_b_col = 'B2' in sqref_str

            if has_equipment_source and covers_b_col:
                # Check error message is configured
                if dv_eq.showErrorMessage:
                    print(f"PASS: Component 1 — Equipment Name validation on B2:B76 with EquipmentList source and error alert (0.30 pts)")
                    print(f"  formula1={formula1}, sqref={sqref_str}, showError={dv_eq.showErrorMessage}")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 1 — Equipment Name validation found but showErrorMessage is False (partial: no credit)")
                    print(f"  formula1={formula1}, sqref={sqref_str}")
            else:
                print(f"FAIL: Component 1 — Equipment Name list validation found but source or range incorrect")
                print(f"  formula1={formula1}, sqref={sqref_str}")
        else:
            print(f"FAIL: Component 1 — No list validation found covering column B (Equipment Name)")
            print(f"  Available validations: {[(dv.type, str(dv.sqref)) for dv in dvs]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Status validation on F2:F76 (0.30 points)
    # Must be type=list, formula1 contains 'Reserved,In Use,Returned' (in some order), showErrorMessage=True
    try:
        dv_status = None
        for dv in dvs:
            if dv.type == 'list':
                sqref_str = normalize_sqref(dv.sqref)
                if 'F2' in sqref_str:
                    dv_status = dv
                    break
        if dv_status is None:
            # Also search by formula content
            for dv in dvs:
                if dv.type == 'list' and dv.formula1:
                    f1 = str(dv.formula1)
                    if 'Reserved' in f1 and 'In Use' in f1 and 'Returned' in f1:
                        dv_status = dv
                        break

        if dv_status is not None:
            formula1 = str(dv_status.formula1) if dv_status.formula1 else ''
            sqref_str = normalize_sqref(dv_status.sqref)
            has_statuses = ('Reserved' in formula1 and 'In Use' in formula1 and 'Returned' in formula1)
            covers_f_col = 'F2' in sqref_str

            if has_statuses and covers_f_col:
                if dv_status.showErrorMessage:
                    print(f"PASS: Component 2 — Status validation on F2:F76 with correct status list and error alert (0.30 pts)")
                    print(f"  formula1={formula1}, sqref={sqref_str}")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 2 — Status validation found but showErrorMessage is False")
                    print(f"  formula1={formula1}, sqref={sqref_str}")
            else:
                print(f"FAIL: Component 2 — Status list validation found but values or range incorrect")
                print(f"  formula1={formula1}, sqref={sqref_str}")
        else:
            print(f"FAIL: Component 2 — No list validation found for Status column (F2:F76)")
            print(f"  Available validations: {[(dv.type, str(dv.sqref), dv.formula1) for dv in dvs]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Checkout Date validation on D2:D76 (0.20 points)
    # Must be type=date, operator=between, formula1=2025-01-01, formula2=2025-12-31, showErrorMessage=True
    try:
        dv_checkout = None
        for dv in dvs:
            if dv.type == 'date':
                sqref_str = normalize_sqref(dv.sqref)
                if 'D2' in sqref_str:
                    dv_checkout = dv
                    break

        if dv_checkout is not None:
            formula1 = str(dv_checkout.formula1) if dv_checkout.formula1 else ''
            formula2 = str(dv_checkout.formula2) if dv_checkout.formula2 else ''
            sqref_str = normalize_sqref(dv_checkout.sqref)
            operator = str(dv_checkout.operator) if dv_checkout.operator else ''

            has_start_date = '2025-01-01' in formula1 or '2025' in formula1
            has_end_date = '2025-12-31' in formula2 or '2025' in formula2
            is_between = operator == 'between'
            covers_d_col = 'D2' in sqref_str

            if has_start_date and has_end_date and is_between and covers_d_col:
                if dv_checkout.showErrorMessage:
                    print(f"PASS: Component 3 — Checkout Date validation on D2:D76 with 2025 date range and error alert (0.20 pts)")
                    print(f"  formula1={formula1}, formula2={formula2}, operator={operator}")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 3 — Date validation found but showErrorMessage is False")
            else:
                print(f"FAIL: Component 3 — Date validation on D column found but operator/range mismatch")
                print(f"  formula1={formula1}, formula2={formula2}, operator={operator}, sqref={sqref_str}")
        else:
            print(f"FAIL: Component 3 — No date validation found for Checkout Date column (D2:D76)")
            print(f"  Available validations: {[(dv.type, str(dv.sqref)) for dv in dvs]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Return Date validation on E2:E76 (0.20 points)
    # Must be type=date, operator=between, formula1=2025-01-01, formula2=2025-12-31, showErrorMessage=True
    try:
        dv_return = None
        for dv in dvs:
            if dv.type == 'date':
                sqref_str = normalize_sqref(dv.sqref)
                if 'E2' in sqref_str:
                    dv_return = dv
                    break

        if dv_return is not None:
            formula1 = str(dv_return.formula1) if dv_return.formula1 else ''
            formula2 = str(dv_return.formula2) if dv_return.formula2 else ''
            sqref_str = normalize_sqref(dv_return.sqref)
            operator = str(dv_return.operator) if dv_return.operator else ''

            has_start_date = '2025-01-01' in formula1 or '2025' in formula1
            has_end_date = '2025-12-31' in formula2 or '2025' in formula2
            is_between = operator == 'between'
            covers_e_col = 'E2' in sqref_str

            if has_start_date and has_end_date and is_between and covers_e_col:
                if dv_return.showErrorMessage:
                    print(f"PASS: Component 4 — Return Date validation on E2:E76 with 2025 date range and error alert (0.20 pts)")
                    print(f"  formula1={formula1}, formula2={formula2}, operator={operator}")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 4 — Date validation found but showErrorMessage is False")
            else:
                print(f"FAIL: Component 4 — Date validation on E column found but operator/range mismatch")
                print(f"  formula1={formula1}, formula2={formula2}, operator={operator}, sqref={sqref_str}")
        else:
            print(f"FAIL: Component 4 — No date validation found for Return Date column (E2:E76)")
            print(f"  Available validations: {[(dv.type, str(dv.sqref)) for dv in dvs]}")
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
