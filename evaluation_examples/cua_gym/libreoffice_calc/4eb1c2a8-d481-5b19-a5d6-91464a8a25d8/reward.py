"""
Reward Script: Data validation on C2:C20 with custom duplicate-check formula
Task ID: calc_gcv_061
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): Data validation exists on C2:C20 with type 'custom'
  Component 2 (0.30): Formula is =COUNTIF($C$2:$C$20,C2)<=1
  Component 3 (0.15): Error style is 'stop'
  Component 4 (0.15): Error title is 'Duplicate Found'
  Component 5 (0.15): Error message is 'This value already exists in the column.'
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_061'


def persist_app_state(domain: str):
    """Best-effort save of any unsaved GUI edits."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            import time
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def normalize_formula(f):
    """Normalize a formula string for comparison: uppercase, strip spaces."""
    if f is None:
        return ""
    return str(f).upper().replace(" ", "")


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

    # Find the relevant data validation targeting C2:C20
    validations = ws.data_validations.dataValidation
    target_dv = None

    for dv in validations:
        # Check if this validation covers C2:C20
        sqref_str = str(dv.sqref).upper().replace(" ", "")
        if "C2:C20" in sqref_str:
            target_dv = dv
            break

    # Component 1: Data validation exists on C2:C20 with type 'custom' (0.25 points)
    try:
        if target_dv is not None and target_dv.type == "custom":
            print(f"PASS: Component 1 - Custom data validation found on C2:C20 (0.25 pts)")
            total_score += 0.25
        elif target_dv is not None:
            print(f"FAIL: Component 1 - Data validation on C2:C20 exists but type is '{target_dv.type}', expected 'custom'")
        else:
            print(f"FAIL: Component 1 - No data validation found covering C2:C20 (found {len(validations)} validations total)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    if target_dv is None:
        # No point checking further components without the validation
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Formula is =COUNTIF($C$2:$C$20,C2)<=1 (0.30 points)
    try:
        expected_formula = normalize_formula("=COUNTIF($C$2:$C$20,C2)<=1")
        actual_formula = normalize_formula(target_dv.formula1)
        if actual_formula == expected_formula:
            print(f"PASS: Component 2 - Formula matches: {target_dv.formula1} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 - Formula mismatch. Expected: =COUNTIF($C$2:$C$20,C2)<=1, Found: {target_dv.formula1}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Error style is 'stop' (0.15 points)
    try:
        error_style = target_dv.errorStyle
        if error_style is not None and error_style.lower() == "stop":
            print(f"PASS: Component 3 - Error style is 'stop' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - Error style is '{error_style}', expected 'stop'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Error title is 'Duplicate Found' (0.15 points)
    try:
        error_title = target_dv.errorTitle
        if error_title is not None and error_title.strip() == "Duplicate Found":
            print(f"PASS: Component 4 - Error title is 'Duplicate Found' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 - Error title is '{error_title}', expected 'Duplicate Found'")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Error message is 'This value already exists in the column.' (0.15 points)
    try:
        error_msg = target_dv.error
        if error_msg is not None and error_msg.strip() == "This value already exists in the column.":
            print(f"PASS: Component 5 - Error message matches (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 - Error message is '{error_msg}', expected 'This value already exists in the column.'")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI state before verification
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
