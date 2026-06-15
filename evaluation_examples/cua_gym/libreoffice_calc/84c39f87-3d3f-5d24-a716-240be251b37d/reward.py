"""
Reward Script: Set up dropdown validation for cells B2:B100 in 'Orders' sheet
               pulling list from ProductList.$A$2:$A$20
Task ID: calc_dop_validate_range_020
Domain: libreoffice_calc
Scoring:
  Component 1: Data validation exists on 'Orders' sheet cells in column B (0.3 pts)
  Component 2: Validation is type=list referencing ProductList!$A$2:$A$20 (0.4 pts)
  Component 3: Validation covers B2:B100 with stop error style (0.3 pts)
  Total: 1.0
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'  # VM path — reward scripts run on the VM
TASK_ID = 'calc_dop_validate_range_020'


def get_b_validations(ws):
    """Return list of data validations covering column B cells."""
    if not ws.data_validations:
        return []
    result = []
    for dv in ws.data_validations.dataValidation:
        sqref_str = str(dv.sqref)
        if re.search(r'\bB\d', sqref_str):
            result.append(dv)
    return result


def check_formula_ref(dv):
    """Return True if validation has type=list and references ProductList!$A$2:$A$20."""
    if dv.type != 'list':
        return False
    formula1 = str(dv.formula1) if dv.formula1 else ''
    formula_clean = formula1.strip("'\"").replace(' ', '').upper()
    # Accept: PRODUCTLIST!$A$2:$A$20 or PRODUCTLIST!A2:A20 variants
    return bool(re.match(r"PRODUCTLIST!\$?A\$?2:\$?A\$?20$", formula_clean))


def check_coverage_and_stop(dv):
    """Return True if validation covers B2:B100 and has errorStyle=stop."""
    sqref_str = str(dv.sqref).strip().upper().replace(' ', '')
    row_nums = [int(m) for m in re.findall(r'B(\d+)', sqref_str)]
    covers_range = (len(row_nums) >= 2 and min(row_nums) <= 2 and max(row_nums) >= 100)
    error_style = str(dv.errorStyle).lower() if dv.errorStyle else ''
    has_stop_error = (error_style == 'stop')
    return covers_range and has_stop_error


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    - B2:B100 in 'Orders' has a cell-range dropdown validation
    - The validation list points to ProductList.$A$2:$A$20
    - Invalid entries should be rejected with a Stop error
    """
    total_score = 0.0

    # Gate: load the workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gate: check 'Orders' sheet exists
    if 'Orders' not in wb.sheetnames:
        print("FAIL: 'Orders' sheet not found in workbook")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    ws_orders = wb['Orders']

    # Component 1: Data validation exists on 'Orders' sheet covering column B (0.3 points)
    # This FAILS on initial (no validations) and PASSES on golden (validation present)
    try:
        b_validations = get_b_validations(ws_orders)
        all_validations = list(ws_orders.data_validations.dataValidation) if ws_orders.data_validations else []

        if len(b_validations) > 0:
            print(f"PASS: Component 1 — Data validation found on column B of 'Orders' sheet ({len(b_validations)} validation(s)) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No data validation found on column B of 'Orders' sheet. Found validations: {[str(dv.sqref) for dv in all_validations]}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check data validations: {e}")

    # Component 2: Validation type is 'list' referencing ProductList!$A$2:$A$20 (0.4 points)
    # This FAILS on initial (no validation) and PASSES on golden (correct formula reference)
    try:
        b_validations = get_b_validations(ws_orders)
        matching_dvs = [dv for dv in b_validations if check_formula_ref(dv)]

        if len(matching_dvs) > 0:
            formula1 = str(matching_dvs[0].formula1)
            print(f"PASS: Component 2 — Validation type=list with formula1='{formula1}' correctly references ProductList!$A$2:$A$20 (0.4 pts)")
            total_score += 0.4
        elif len(b_validations) == 0:
            print("FAIL: Component 2 — No data validation on column B to check formula reference")
        else:
            for dv in b_validations:
                formula1 = str(dv.formula1) if dv.formula1 else ''
                print(f"FAIL: Component 2 — Validation on column B has type='{dv.type}', formula1='{formula1}', expected type=list and reference to ProductList!$A$2:$A$20")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check validation formula: {e}")

    # Component 3: Validation covers B2:B100 with stop error style (0.3 points)
    # This FAILS on initial (no validation) and PASSES on golden (correct sqref + errorStyle=stop)
    try:
        b_validations = get_b_validations(ws_orders)
        cov_stop_dvs = [dv for dv in b_validations if check_coverage_and_stop(dv)]

        if len(cov_stop_dvs) > 0:
            sqref_str = str(cov_stop_dvs[0].sqref)
            print(f"PASS: Component 3 — Validation covers B2:B100 (sqref='{sqref_str}') with errorStyle='stop' (0.3 pts)")
            total_score += 0.3
        elif len(b_validations) == 0:
            print("FAIL: Component 3 — No data validation found on column B")
        else:
            for dv in b_validations:
                sqref_str = str(dv.sqref)
                sqref_clean = sqref_str.strip().upper().replace(' ', '')
                row_nums = [int(m) for m in re.findall(r'B(\d+)', sqref_clean)]
                covers_range = (len(row_nums) >= 2 and min(row_nums) <= 2 and max(row_nums) >= 100)
                error_style = str(dv.errorStyle).lower() if dv.errorStyle else ''
                if not covers_range:
                    print(f"FAIL: Component 3 — Validation sqref='{sqref_str}' does not fully cover B2:B100")
                elif error_style != 'stop':
                    print(f"FAIL: Component 3 — Validation errorStyle='{error_style}', expected 'stop'")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not check validation coverage/error style: {e}")

    final_score = round(min(total_score, 1.0), 2)
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
