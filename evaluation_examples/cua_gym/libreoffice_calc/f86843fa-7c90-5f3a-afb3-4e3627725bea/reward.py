"""
Reward Script: Apply data validation to F2:F100 with custom formula F2>E2
Task ID: calc_gao_038
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Data validation exists on F2:F100 with type 'custom'
  Component 2 (0.3): Formula is F2>E2 (correct relative reference)
  Component 3 (0.2): Error style is 'stop' (rejects invalid entries)
  Component 4 (0.2): Error message about selling price > cost price
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gao_038'


def persist_app_state(domain):
    """Save any unsaved GUI state before verification."""
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
    Verify data validation on F2:F100 with custom formula F2>E2.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the Products sheet
    ws = None
    if 'Products' in wb.sheetnames:
        ws = wb['Products']
    else:
        ws = wb.active
    print(f"INFO: Checking sheet '{ws.title}'")

    dvs = ws.data_validations.dataValidation
    print(f"INFO: Found {len(dvs)} data validation(s)")

    if len(dvs) == 0:
        print("FAIL: No data validations found")
        print("REWARD: 0.0")
        return 0.0

    # Find the relevant data validation covering F2:F100
    target_dv = None
    for dv in dvs:
        sqref_str = str(dv.sqref).upper()
        # Check if F2:F100 is covered (exact match or superset)
        if 'F2:F100' in sqref_str or 'F2' in sqref_str:
            target_dv = dv
            break

    if target_dv is None:
        # Fallback: pick first DV that applies to column F
        for dv in dvs:
            sqref_str = str(dv.sqref).upper()
            if 'F' in sqref_str:
                target_dv = dv
                break

    if target_dv is None:
        print("FAIL: No data validation found covering column F")
        print("REWARD: 0.0")
        return 0.0

    dv = target_dv
    print(f"INFO: Found DV — type={dv.type}, formula1={dv.formula1}, sqref={dv.sqref}")
    print(f"INFO: errorStyle={dv.errorStyle}, error={dv.error}")

    # Component 1: Data validation exists on F2:F100 with type 'custom' (0.3 points)
    try:
        sqref_str = str(dv.sqref).upper().replace(' ', '')
        dv_type = str(dv.type).lower() if dv.type else ''
        range_ok = 'F2:F100' in sqref_str
        type_ok = dv_type == 'custom'
        if range_ok and type_ok:
            print(f"PASS: Component 1 — DV type=custom on F2:F100 (0.3 pts)")
            total_score += 0.3
        else:
            if not range_ok:
                print(f"FAIL: Component 1 — sqref is '{dv.sqref}', expected F2:F100")
            if not type_ok:
                print(f"FAIL: Component 1 — type is '{dv.type}', expected 'custom'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Formula is F2>E2 (0.3 points)
    try:
        formula = str(dv.formula1).upper().replace(' ', '') if dv.formula1 else ''
        # Accept variants: F2>E2, =F2>E2
        expected_variants = ['F2>E2', '=F2>E2']
        if formula in [v.upper() for v in expected_variants]:
            print(f"PASS: Component 2 — Formula is '{dv.formula1}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Formula is '{dv.formula1}', expected 'F2>E2'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error style is 'stop' (0.2 points)
    try:
        err_style = str(dv.errorStyle).lower() if dv.errorStyle else ''
        if err_style == 'stop':
            print(f"PASS: Component 3 — errorStyle=stop (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — errorStyle='{dv.errorStyle}', expected 'stop'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Error message mentions selling price > cost price (0.2 points)
    try:
        err_msg = str(dv.error).lower() if dv.error else ''
        # Check that the message conveys the constraint
        has_selling = 'selling' in err_msg or 'sell' in err_msg
        has_cost = 'cost' in err_msg
        has_greater = 'greater' in err_msg or 'more' in err_msg or 'exceed' in err_msg or 'above' in err_msg
        if has_selling and has_cost and has_greater:
            print(f"PASS: Component 4 — Error message: '{dv.error}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — Error message '{dv.error}' doesn't convey 'selling price must be greater than cost price'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
