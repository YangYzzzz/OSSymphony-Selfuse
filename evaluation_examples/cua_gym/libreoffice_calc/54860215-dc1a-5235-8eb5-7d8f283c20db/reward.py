"""
Reward Script: Apply data validation using named range 'Countries'
Task ID: calc_gcv_069
Domain: libreoffice_calc
Scoring:
  Component 1 (0.40): Named range 'Countries' defined as Sheet2.$A$1:$A$15
  Component 2 (0.35): Data validation on Sheet1 C2:C25, type=list
  Component 3 (0.25): Data validation formula references 'Countries' named range
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_069'


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

    # Component 1: Named range 'Countries' defined as Sheet2.$A$1:$A$15 (0.40 points)
    try:
        defined_names = dict(wb.defined_names)
        if 'Countries' in defined_names:
            dn = defined_names['Countries']
            ref = dn.attr_text
            # Normalize: accept various valid forms of the reference
            ref_normalized = ref.replace("'", "").replace(" ", "").upper()
            expected_normalized = "SHEET2!$A$1:$A$15"
            if ref_normalized == expected_normalized:
                print(f"PASS: Component 1 — Named range 'Countries' = {ref} (0.40 pts)")
                total_score += 0.40
            else:
                print(f"FAIL: Component 1 — Named range 'Countries' exists but points to '{ref}', expected 'Sheet2!$A$1:$A$15'")
        else:
            print(f"FAIL: Component 1 — Named range 'Countries' not found. Defined names: {list(defined_names.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Data validation on Sheet1 C2:C25, type=list (0.35 points)
    try:
        ws = wb['Sheet1']
        validations = ws.data_validations.dataValidation
        found_validation = False
        matched_dv = None

        for dv in validations:
            # Check if this is a list-type validation
            if dv.type == 'list':
                # Check if the range covers C2:C25
                sqref_str = str(dv.sqref).upper().replace(" ", "")
                # The sqref may be "C2:C25" or contain it
                if 'C2:C25' in sqref_str:
                    found_validation = True
                    matched_dv = dv
                    break

        if found_validation:
            print(f"PASS: Component 2 — List validation found on C2:C25 (0.35 pts)")
            total_score += 0.35
        else:
            if len(validations) == 0:
                print(f"FAIL: Component 2 — No data validations found on Sheet1")
            else:
                for dv in validations:
                    print(f"  Found DV: type={dv.type}, sqref={dv.sqref}, formula1={dv.formula1}")
                print(f"FAIL: Component 2 — No list validation on C2:C25")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Data validation formula references 'Countries' named range (0.25 points)
    try:
        ws = wb['Sheet1']
        validations = ws.data_validations.dataValidation
        formula_matches = False

        for dv in validations:
            if dv.type == 'list':
                sqref_str = str(dv.sqref).upper().replace(" ", "")
                if 'C2:C25' in sqref_str:
                    formula1 = str(dv.formula1).strip() if dv.formula1 else ""
                    # The formula should reference the named range 'Countries'
                    # It could be "Countries", "=Countries", or "Sheet2!$A$1:$A$15"
                    formula_upper = formula1.upper().replace("'", "").replace(" ", "")
                    if 'COUNTRIES' in formula_upper:
                        formula_matches = True
                        print(f"PASS: Component 3 — Validation formula references 'Countries': '{formula1}' (0.25 pts)")
                        total_score += 0.25
                    elif 'SHEET2' in formula_upper and '$A$1:$A$15' in formula_upper:
                        # Also accept direct range reference to the same cells
                        formula_matches = True
                        print(f"PASS: Component 3 — Validation formula references Sheet2 range directly: '{formula1}' (0.25 pts)")
                        total_score += 0.25
                    else:
                        print(f"FAIL: Component 3 — Validation formula is '{formula1}', expected reference to 'Countries' or Sheet2!$A$1:$A$15")
                    break

        if not formula_matches and total_score < 0.6:
            # Only print if we haven't already printed about formula
            pass
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
