"""
Reward Script: Apply data validation to Price column (D2:D200) for decimal numbers
Task ID: calc_dop_validate_decimal_022
Domain: libreoffice_calc
Scoring:
  Component 1: Data validation exists on D2:D200 (0.3 pts)
  Component 2: DV type is decimal, operator between, range 0.01 to 9999.99 (0.4 pts)
  Component 3: Error alert is Warning type with correct title and message (0.3 pts)
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_dop_validate_decimal_022'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the PriceList sheet
    try:
        if 'PriceList' not in wb.sheetnames:
            print("FAIL: Sheet 'PriceList' not found in workbook")
            print("REWARD: 0.0")
            return 0.0
        ws = wb['PriceList']
    except Exception as e:
        print(f"CRITICAL: Cannot access PriceList sheet: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Data validation exists on D2:D200 (0.3 points)
    # Initial file has NO data validations; golden has exactly 1 on D2:D200
    try:
        dvs = ws.data_validations.dataValidation
        # Find a DV that covers D2:D200
        dv_on_price_col = None
        for dv in dvs:
            sqref_str = str(dv.sqref)
            if 'D2:D200' in sqref_str:
                dv_on_price_col = dv
                break
        if dv_on_price_col is not None:
            print(f"PASS: Component 1 — Data validation found on D2:D200 (0.3 pts)")
            total_score += 0.3
        else:
            dvs_list = [str(dv.sqref) for dv in dvs]
            print(f"FAIL: Component 1 — No data validation on D2:D200. Found: {dvs_list}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: DV type is 'decimal', operator is 'between', range 0.01 to 9999.99 (0.4 points)
    # This verifies the exact constraint: decimal numbers > 0 and <= 9999.99
    # The golden uses operator='between' with formula1=0.01 and formula2=9999.99
    try:
        if dv_on_price_col is not None:
            dv = dv_on_price_col
            dv_type = dv.type
            dv_operator = dv.operator
            try:
                dv_formula1 = float(dv.formula1) if dv.formula1 is not None else None
            except (ValueError, TypeError):
                dv_formula1 = dv.formula1
            try:
                dv_formula2 = float(dv.formula2) if dv.formula2 is not None else None
            except (ValueError, TypeError):
                dv_formula2 = dv.formula2

            type_ok = (dv_type == 'decimal')
            operator_ok = (dv_operator in ('between', 'greaterThan', 'greaterThanOrEqual'))
            # Accept 'between' with 0.01/9999.99 OR greaterThan/greaterThanOrEqual with suitable values
            # The golden file uses 'between' with formula1=0.01 and formula2=9999.99
            range_ok = False
            if dv_operator == 'between':
                range_ok = (
                    dv_formula1 is not None and abs(float(dv_formula1) - 0.01) < 0.001 and
                    dv_formula2 is not None and abs(float(dv_formula2) - 9999.99) < 0.01
                )
            elif dv_operator == 'greaterThan':
                # >0 with no upper bound: partial credit only if type+range are otherwise correct
                range_ok = (dv_formula1 is not None and abs(float(dv_formula1) - 0) < 0.001)
            elif dv_operator == 'greaterThanOrEqual':
                range_ok = (dv_formula1 is not None and abs(float(dv_formula1) - 0.01) < 0.001)

            if type_ok and range_ok:
                print(f"PASS: Component 2 — DV type={dv_type}, operator={dv_operator}, "
                      f"formula1={dv_formula1}, formula2={dv_formula2} (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Expected decimal/between/0.01/9999.99, "
                      f"got type={dv_type}, operator={dv_operator}, "
                      f"formula1={dv_formula1}, formula2={dv_formula2}")
        else:
            print("FAIL: Component 2 — Cannot check range/type; no DV found on D2:D200")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error alert style is 'warning' with correct title and message (0.3 points)
    # Golden: errorStyle=warning, errorTitle='Price Out of Range',
    #         error='Price should be between 0.01 and 9999.99. Do you want to continue?'
    try:
        if dv_on_price_col is not None:
            dv = dv_on_price_col
            error_style_ok = (dv.errorStyle == 'warning')
            error_title_ok = (dv.errorTitle is not None and
                              'Price Out of Range' in dv.errorTitle)
            error_msg_ok = (dv.error is not None and
                            'Price should be between 0.01 and 9999.99' in dv.error and
                            'continue' in dv.error.lower())

            if error_style_ok and error_title_ok and error_msg_ok:
                print(f"PASS: Component 3 — Warning alert with correct title and message (0.3 pts)")
                total_score += 0.3
            else:
                issues = []
                if not error_style_ok:
                    issues.append(f"errorStyle={dv.errorStyle!r} (expected 'warning')")
                if not error_title_ok:
                    issues.append(f"errorTitle={dv.errorTitle!r} (expected 'Price Out of Range')")
                if not error_msg_ok:
                    issues.append(f"error={dv.error!r} (expected message about 0.01-9999.99 and continue)")
                print(f"FAIL: Component 3 — {'; '.join(issues)}")
        else:
            print("FAIL: Component 3 — Cannot check alert style; no DV found on D2:D200")
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
