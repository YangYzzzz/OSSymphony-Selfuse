"""
Reward Script: Data validation on E2:E50 — custom formula =MOD(E2,5)=0 with Stop error alert
Task ID: calc_gcv_071
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30): Data validation exists with type=custom on range E2:E50
  Component 2 (0.30): Formula is =MOD(E2,5)=0
  Component 3 (0.20): Error style is 'stop'
  Component 4 (0.20): Error title='Invalid Value' and message='Value must be a multiple of 5.'
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_071'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice edits before verification."""
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
    Verify that data validation has been set up on E2:E50 with:
    - type: custom
    - formula: =MOD(E2,5)=0
    - error style: stop
    - error title: 'Invalid Value'
    - error message: 'Value must be a multiple of 5.'

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

    # Find a data validation that covers E2:E50 with type=custom
    dvs = ws.data_validations.dataValidation
    target_dv = None

    for dv in dvs:
        # Check if this DV covers E2:E50 (the sqref may be exactly E2:E50 or contain it)
        sqref_str = str(dv.sqref).replace(" ", "")
        if dv.type == "custom" and "E2:E50" in sqref_str.upper():
            target_dv = dv
            break

    # Component 1: Data validation exists with type=custom on E2:E50 (0.30 points)
    try:
        if target_dv is not None:
            print(f"PASS: Component 1 — Custom data validation found on {target_dv.sqref} (0.30 pts)")
            total_score += 0.30
        else:
            # Check if there's any DV at all for diagnostics
            if len(dvs) == 0:
                print("FAIL: Component 1 — No data validations found on the sheet")
            else:
                for i, dv in enumerate(dvs):
                    print(f"  Found DV {i}: type={dv.type}, sqref={dv.sqref}")
                print("FAIL: Component 1 — No custom DV covering E2:E50 found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if target_dv is None:
        # No point checking further components
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Formula is =MOD(E2,5)=0 (0.30 points)
    try:
        formula = target_dv.formula1
        if formula is not None:
            # Normalize: strip spaces, uppercase
            norm_formula = str(formula).replace(" ", "").upper()
            expected = "=MOD(E2,5)=0"
            if norm_formula == expected:
                print(f"PASS: Component 2 — Formula matches: {formula} (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — Expected formula '{expected}', found '{formula}'")
        else:
            print("FAIL: Component 2 — No formula1 set on the data validation")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error style is 'stop' (0.20 points)
    try:
        error_style = target_dv.errorStyle
        if error_style is not None and str(error_style).lower() == "stop":
            print(f"PASS: Component 3 — Error style is 'stop' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Expected errorStyle 'stop', found '{error_style}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Error title and message (0.20 points)
    try:
        actual_title = str(target_dv.errorTitle).strip() if target_dv.errorTitle else ""
        actual_msg = str(target_dv.error).strip() if target_dv.error else ""

        if actual_title == "Invalid Value" and actual_msg == "Value must be a multiple of 5.":
            print(f"PASS: Component 4 — Error title='{actual_title}', message='{actual_msg}' (0.20 pts)")
            total_score += 0.20
        else:
            if actual_title != "Invalid Value":
                print(f"FAIL: Component 4 — Expected errorTitle 'Invalid Value', found '{actual_title}'")
            if actual_msg != "Value must be a multiple of 5.":
                print(f"FAIL: Component 4 — Expected error message 'Value must be a multiple of 5.', found '{actual_msg}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
