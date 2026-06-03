"""
Reward Script: Data validation on F2:F35 for weekday-only delivery dates
Task ID: calc_gcv_089
Domain: libreoffice_calc
Scoring:
  Component 1 (0.20): Data validation exists on F2:F35 with type 'custom'
  Component 2 (0.25): Formula matches =AND(ISNUMBER(F2),WEEKDAY(F2,2)<=5)
  Component 3 (0.20): Error style is 'stop'
  Component 4 (0.15): Error title is 'Weekday Only'
  Component 5 (0.20): Error message matches expected text
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'Delivery_Schedule'

def persist_app_state():
    """Save any unsaved LibreOffice state before verification."""
    try:
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        import time
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_calc")
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

    ws = wb.active

    # Find data validations
    validations = ws.data_validations.dataValidation
    if len(validations) == 0:
        print("FAIL: No data validations found on the sheet")
        print("REWARD: 0.0")
        return 0.0

    # Find a validation that covers F2:F35
    target_dv = None
    for dv in validations:
        sqref_str = str(dv.sqref).upper().replace(" ", "")
        if "F2:F35" in sqref_str:
            target_dv = dv
            break

    # Component 1: Data validation exists on F2:F35 with type 'custom' (0.20 points)
    try:
        if target_dv is not None and target_dv.type == "custom":
            print(f"PASS: Component 1 — Custom data validation found on F2:F35 (0.20 pts)")
            total_score += 0.20
        elif target_dv is not None:
            print(f"FAIL: Component 1 — Validation on F2:F35 found but type is '{target_dv.type}', expected 'custom'")
        else:
            print(f"FAIL: Component 1 — No data validation found covering F2:F35")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if target_dv is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Formula matches =AND(ISNUMBER(F2),WEEKDAY(F2,2)<=5) (0.25 points)
    try:
        actual_formula = str(target_dv.formula1).strip() if target_dv.formula1 else ""
        expected_formula = "=AND(ISNUMBER(F2),WEEKDAY(F2,2)<=5)"
        # Normalize for comparison: uppercase and remove spaces
        actual_norm = actual_formula.upper().replace(" ", "")
        expected_norm = expected_formula.upper().replace(" ", "")
        if actual_norm == expected_norm:
            print(f"PASS: Component 2 — Formula matches: {actual_formula} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected formula '{expected_formula}', found '{actual_formula}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error style is 'stop' (0.20 points)
    try:
        actual_style = str(target_dv.errorStyle).strip().lower() if target_dv.errorStyle else ""
        if actual_style == "stop":
            print(f"PASS: Component 3 — Error style is 'stop' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Expected error style 'stop', found '{actual_style}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Error title is 'Weekday Only' (0.15 points)
    try:
        actual_title = str(target_dv.errorTitle).strip() if target_dv.errorTitle else ""
        if actual_title == "Weekday Only":
            print(f"PASS: Component 4 — Error title is 'Weekday Only' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Expected error title 'Weekday Only', found '{actual_title}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Error message matches (0.20 points)
    try:
        actual_msg = str(target_dv.error).strip() if target_dv.error else ""
        expected_msg = "Deliveries can only be scheduled on weekdays (Mon-Fri)."
        if actual_msg == expected_msg:
            print(f"PASS: Component 5 — Error message matches (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 — Expected error message '{expected_msg}', found '{actual_msg}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
