"""
Reward Script: Apply data validation to C2:C45 (dropdown list) and D2:D45 (whole number 1-5)
Task ID: calc_gcv_082
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30): List validation exists on C2:C45 with correct items
  Component 2 (0.20): List validation dropdown items match exactly
  Component 3 (0.30): Whole number validation on D2:D45, between 1-5
  Component 4 (0.20): Input prompt on D validation: Title='Numeric Rating', Message='Enter 1-5 matching the text rating.'
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_082'


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
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb.active
    dvs = ws.data_validations.dataValidation

    # Identify the list and whole-number validations
    list_dv = None
    whole_dv = None
    for dv in dvs:
        if dv.type == "list":
            list_dv = dv
        elif dv.type == "whole":
            whole_dv = dv

    # Component 1: List validation exists on C2:C45 (0.30 points)
    try:
        if list_dv is not None:
            sqref_str = str(list_dv.sqref).replace(" ", "")
            # Accept C2:C45 in any form
            if "C2:C45" in sqref_str.upper():
                print(f"PASS: Component 1 -- List validation on C2:C45 found (sqref={sqref_str}) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 -- List validation exists but sqref={sqref_str}, expected C2:C45")
        else:
            print("FAIL: Component 1 -- No list-type data validation found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: List validation has the correct 5 dropdown items (0.20 points)
    try:
        if list_dv is not None and list_dv.formula1:
            formula = list_dv.formula1.strip('"').strip("'")
            expected_items = [
                "Excellent (5)",
                "Good (4)",
                "Average (3)",
                "Below Average (2)",
                "Poor (1)",
            ]
            actual_items = [item.strip() for item in formula.split(",")]
            if actual_items == expected_items:
                print(f"PASS: Component 2 -- Dropdown items match exactly (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 -- Dropdown items mismatch. Expected: {expected_items}, Got: {actual_items}")
        else:
            print("FAIL: Component 2 -- No list validation or formula1 is empty")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Whole number validation on D2:D45, between 1 and 5 (0.30 points)
    try:
        if whole_dv is not None:
            sqref_str = str(whole_dv.sqref).replace(" ", "")
            if "D2:D45" not in sqref_str.upper():
                print(f"FAIL: Component 3 -- Whole number validation exists but sqref={sqref_str}, expected D2:D45")
            else:
                # Check operator and range
                op = whole_dv.operator
                f1 = str(whole_dv.formula1).strip() if whole_dv.formula1 else ""
                f2 = str(whole_dv.formula2).strip() if whole_dv.formula2 else ""
                if op == "between" and f1 == "1" and f2 == "5":
                    print(f"PASS: Component 3 -- Whole number between 1-5 on D2:D45 (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 3 -- Whole number validation has operator={op}, f1={f1}, f2={f2}; expected between/1/5")
        else:
            print("FAIL: Component 3 -- No whole-number data validation found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Input prompt on D validation: Title='Numeric Rating', Message='Enter 1-5 matching the text rating.' (0.20 points)
    try:
        if whole_dv is not None:
            title = (whole_dv.promptTitle or "").strip()
            msg = (whole_dv.prompt or "").strip()
            title_ok = title == "Numeric Rating"
            msg_ok = msg == "Enter 1-5 matching the text rating."
            if title_ok and msg_ok:
                print(f"PASS: Component 4 -- Input prompt correct: title='{title}', msg='{msg}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 -- Input prompt mismatch. Title='{title}' (expected 'Numeric Rating'), Msg='{msg}' (expected 'Enter 1-5 matching the text rating.')")
        else:
            print("FAIL: Component 4 -- No whole-number validation to check prompt on")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
