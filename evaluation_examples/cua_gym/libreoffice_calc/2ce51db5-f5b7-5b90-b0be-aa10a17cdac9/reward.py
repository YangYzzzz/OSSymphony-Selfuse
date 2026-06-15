"""
Reward Script: Apply data validation dropdown to B2 with 'Yes'/'No' and input message
Task ID: calc_nrv_083
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Data validation exists on B2 with type 'list'
  Component 2 (0.3): Validation formula contains exactly 'Yes' and 'No'
  Component 3 (0.2): Input message title is 'Confirm Attendance'
  Component 4 (0.2): Input message text is 'Select Yes or No'
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_083'


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


def find_validation_for_b2(validations):
    """Find a data validation that covers cell B2."""
    for dv in validations:
        sqref_str = str(dv.sqref)
        # sqref can be "B2", "B2:B100", "$B$2", etc.
        # Check if B2 is within the validation range
        if 'B2' in sqref_str.upper().replace('$', ''):
            return dv
    return None


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

    # Get all data validations
    try:
        validations = ws.data_validations.dataValidation
    except Exception as e:
        print(f"ERROR: Cannot access data validations: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find a validation that applies to B2
    dv = find_validation_for_b2(validations)

    # Component 1: Data validation exists on B2 with type 'list' (0.3 points)
    try:
        if dv is not None and dv.type == "list":
            print(f"PASS: Component 1 - List validation found on B2 (type={dv.type}) (0.3 pts)")
            total_score += 0.3
        elif dv is not None:
            print(f"FAIL: Component 1 - Validation found on B2 but type is '{dv.type}', expected 'list'")
        else:
            print(f"FAIL: Component 1 - No data validation found covering cell B2")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Formula contains exactly 'Yes' and 'No' (0.3 points)
    try:
        if dv is not None and dv.formula1 is not None:
            formula = str(dv.formula1).strip().strip('"')
            # Normalize: split by comma or semicolon, strip whitespace, compare as sets
            items = [item.strip() for item in formula.replace(';', ',').split(',')]
            items_lower = sorted([item.lower() for item in items])
            if items_lower == ['no', 'yes']:
                print(f"PASS: Component 2 - Validation list contains 'Yes' and 'No' (formula1={dv.formula1}) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 - Expected items ['No', 'Yes'], found {items}")
        else:
            print(f"FAIL: Component 2 - No validation or no formula1 for B2 validation")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Input message title is 'Confirm Attendance' (0.2 points)
    try:
        if dv is not None and dv.promptTitle is not None:
            actual_title = str(dv.promptTitle).strip()
            if actual_title == "Confirm Attendance":
                print(f"PASS: Component 3 - Input message title is 'Confirm Attendance' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 - Expected promptTitle 'Confirm Attendance', found '{actual_title}'")
        else:
            print(f"FAIL: Component 3 - No promptTitle set on B2 validation")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Input message text is 'Select Yes or No' (0.2 points)
    try:
        if dv is not None and dv.prompt is not None:
            actual_prompt = str(dv.prompt).strip()
            if actual_prompt == "Select Yes or No":
                print(f"PASS: Component 4 - Input message text is 'Select Yes or No' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 - Expected prompt 'Select Yes or No', found '{actual_prompt}'")
        else:
            print(f"FAIL: Component 4 - No prompt set on B2 validation")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification (data validation is a GUI operation)
persist_app_state("libreoffice_calc")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
