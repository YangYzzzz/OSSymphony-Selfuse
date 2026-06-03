"""
Reward Script: Custom validation on C2:C20 for multiples of 5
Task ID: calc_nrv_085
Domain: libreoffice_calc
Scoring:
  Component 1 (0.35): Data validation exists on C2:C20 with type "custom"
  Component 2 (0.35): Formula checks MOD(x,5)=0
  Component 3 (0.15): showErrorMessage is enabled
  Component 4 (0.15): Error text/title are meaningful (mention "multiple" or "5")
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_085'


def persist_app_state(domain: str):
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
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb.active

    # Get all data validations
    validations = ws.data_validations.dataValidation
    print(f"INFO: Found {len(validations)} data validation(s) on sheet '{ws.title}'")

    # Find a custom validation that covers C2:C20
    target_dv = None
    for dv in validations:
        sqref_str = str(dv.sqref).upper().replace(" ", "")
        # Check if validation covers C2:C20 (exact or superset)
        if dv.type == "custom":
            # Check if sqref includes C2:C20
            if "C2:C20" in sqref_str:
                target_dv = dv
                break

    # Component 1: Custom data validation exists on C2:C20 (0.35 points)
    try:
        if target_dv is not None:
            print(f"PASS: Component 1 -- Custom validation found on {target_dv.sqref} (0.35 pts)")
            total_score += 0.35
        else:
            # Check if there's ANY validation covering C2:C20 even if not exact match
            found_covering_dv = None
            for dv in validations:
                sqref_str = str(dv.sqref).upper().replace(" ", "")
                if "C2" in sqref_str and "C20" in sqref_str:
                    found_covering_dv = dv
                    target_dv = dv
                    print(f"PARTIAL: Component 1 -- Found validation on {dv.sqref} but type is '{dv.type}' (expected 'custom')")
                    break
            if found_covering_dv is None:
                print(f"FAIL: Component 1 -- No custom validation found covering C2:C20")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Formula checks MOD(x,5)=0 (0.35 points)
    try:
        if target_dv is not None and target_dv.formula1:
            formula = str(target_dv.formula1).upper().replace(" ", "")
            print(f"INFO: Validation formula = '{target_dv.formula1}'")
            # Check for MOD(...,5)=0 pattern
            # Acceptable forms: =MOD(C2,5)=0, MOD(C2,5)=0, =MOD(INDIRECT("RC",FALSE),5)=0, etc.
            has_mod = "MOD(" in formula
            has_5 = ",5)" in formula
            has_eq_0 = "=0" in formula
            if has_mod and has_5 and has_eq_0:
                print(f"PASS: Component 2 -- Formula correctly checks MOD(x,5)=0 (0.35 pts)")
                total_score += 0.35
            elif has_mod and has_eq_0:
                # Partial: has MOD and =0 but divisor might differ
                print(f"PARTIAL: Component 2 -- Formula has MOD and =0 but divisor check uncertain")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 -- Formula does not match MOD(x,5)=0 pattern: '{target_dv.formula1}'")
        else:
            print(f"FAIL: Component 2 -- No validation or formula to check")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: showErrorMessage is enabled (0.15 points)
    try:
        if target_dv is not None:
            if target_dv.showErrorMessage:
                print(f"PASS: Component 3 -- showErrorMessage is True (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- showErrorMessage is {target_dv.showErrorMessage}")
        else:
            print(f"FAIL: Component 3 -- No validation to check showErrorMessage")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Error text/title are meaningful (0.15 points)
    try:
        if target_dv is not None:
            error_text = str(target_dv.error or "").lower()
            error_title = str(target_dv.errorTitle or "").lower()
            combined = error_text + " " + error_title
            # Check if error messaging mentions multiples or 5
            mentions_multiple = "multiple" in combined or "divisible" in combined or "mod" in combined
            mentions_5 = "5" in combined
            if mentions_multiple or mentions_5:
                print(f"PASS: Component 4 -- Error text is meaningful: error='{target_dv.error}', title='{target_dv.errorTitle}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- Error text does not mention multiples/5: error='{target_dv.error}', title='{target_dv.errorTitle}'")
        else:
            print(f"FAIL: Component 4 -- No validation to check error text")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
