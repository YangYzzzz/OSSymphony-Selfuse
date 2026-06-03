"""
Reward Script: Apply custom formula validation to cell E2 (=E2>D2)
Task ID: calc_nrv_054
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Data validation exists on E2 with type 'custom'
  Component 2 (0.4): Validation formula is =E2>D2
  Component 3 (0.3): Error message configuration is correct
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_054'


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

    # Find data validation applied to E2
    dv_on_e2 = None
    if ws.data_validations and ws.data_validations.dataValidation:
        for dv in ws.data_validations.dataValidation:
            # Check if E2 is in the sqref range
            sqref_str = str(dv.sqref)
            if 'E2' in sqref_str:
                dv_on_e2 = dv
                break

    # Component 1: Data validation exists on E2 with type 'custom' (0.3 points)
    try:
        if dv_on_e2 is not None and dv_on_e2.type == 'custom':
            print(f"PASS: Component 1 — Custom data validation found on E2 (type={dv_on_e2.type}) (0.3 pts)")
            total_score += 0.3
        elif dv_on_e2 is not None:
            print(f"FAIL: Component 1 — Data validation on E2 exists but type is '{dv_on_e2.type}', expected 'custom'")
        else:
            print(f"FAIL: Component 1 — No data validation found on cell E2")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Validation formula is =E2>D2 (0.4 points)
    try:
        if dv_on_e2 is not None and dv_on_e2.formula1 is not None:
            formula = str(dv_on_e2.formula1).strip()
            # Normalize: remove spaces, uppercase for comparison
            normalized = formula.upper().replace(" ", "")
            expected_variants = ["=E2>D2", "E2>D2"]
            if normalized in [v.upper() for v in expected_variants]:
                print(f"PASS: Component 2 — Validation formula is '{formula}' (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Validation formula is '{formula}', expected '=E2>D2'")
        else:
            print(f"FAIL: Component 2 — No formula found in data validation on E2")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error message configuration (0.3 points)
    # The golden file has showErrorMessage=True and a non-empty error message
    # This ensures the validation actually shows an error when violated
    try:
        if dv_on_e2 is not None:
            has_error_msg = (
                dv_on_e2.showErrorMessage is True
                and dv_on_e2.error is not None
                and len(str(dv_on_e2.error).strip()) > 0
            )
            if has_error_msg:
                print(f"PASS: Component 3 — Error message configured: showErrorMessage={dv_on_e2.showErrorMessage}, "
                      f"error='{dv_on_e2.error}', errorTitle='{dv_on_e2.errorTitle}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Error message not properly configured: "
                      f"showErrorMessage={dv_on_e2.showErrorMessage}, error='{dv_on_e2.error}'")
        else:
            print(f"FAIL: Component 3 — No data validation on E2 to check error message")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
