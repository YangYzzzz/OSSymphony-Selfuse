"""
Reward Script: Set up list validation on D2 from Lookup sheet range
Task ID: calc_nrv_062
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): D2 has a data validation of type "list"
  Component 2 (0.4): Validation formula1 references Lookup.$A$2:$A$30
  Component 3 (0.3): Validation applies specifically to cell D2
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_062'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
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
        import openpyxl
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Main' sheet must exist
    if 'Main' not in wb.sheetnames:
        print("FAIL: 'Main' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Main']

    # Get all data validations on the Main sheet
    dvs = ws.data_validations.dataValidation if ws.data_validations else []
    print(f"INFO: Found {len(dvs)} data validation(s) on 'Main' sheet")

    if len(dvs) == 0:
        print("FAIL: No data validations found on 'Main' sheet")
        print("REWARD: 0.0")
        return 0.0

    # Find a validation that applies to D2
    target_dv = None
    for dv in dvs:
        sqref_str = str(dv.sqref).upper()
        # Check if D2 is covered by this validation's sqref
        # sqref can be "D2", "D2:D100", "$D$2", etc.
        if 'D2' in sqref_str.replace('$', ''):
            target_dv = dv
            break

    if target_dv is None:
        print("FAIL: No data validation found that applies to cell D2")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found validation on D2: type={target_dv.type}, formula1={target_dv.formula1}, sqref={target_dv.sqref}")

    # Component 1: D2 has a data validation of type "list" (0.3 points)
    try:
        if target_dv.type == "list":
            print(f"PASS: Component 1 -- D2 has list-type validation (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- Expected type='list', found type='{target_dv.type}'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Validation formula1 references Lookup.$A$2:$A$30 (0.4 points)
    # Accept various forms: Lookup.$A$2:$A$30, Lookup!$A$2:$A$30, 'Lookup'.$A$2:$A$30, etc.
    try:
        formula1 = str(target_dv.formula1) if target_dv.formula1 else ""
        # Normalize: strip quotes, replace ! with ., uppercase, remove $
        normalized = formula1.upper().replace("'", "").replace("!", ".").replace("$", "")
        expected_normalized = "LOOKUP.A2:A30"
        if normalized == expected_normalized:
            print(f"PASS: Component 2 -- formula1 references Lookup A2:A30 (value: {formula1}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 -- Expected formula1 referencing 'Lookup.$A$2:$A$30', found: '{formula1}' (normalized: '{normalized}')")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Validation applies specifically to cell D2 (0.3 points)
    # Verify that D2 is in the sqref of this validation
    try:
        sqref_str = str(target_dv.sqref).upper().replace("$", "")
        # D2 should be in the sqref range. Accept "D2", "D2:D100", etc.
        # The key requirement is D2 is covered
        if 'D2' in sqref_str:
            print(f"PASS: Component 3 -- Validation applies to D2 (sqref: {target_dv.sqref}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 -- D2 not found in validation sqref: {target_dv.sqref}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
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
