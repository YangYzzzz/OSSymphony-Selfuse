"""
Reward Script: Apply data validation dropdown to B2:B30 from Categories sheet
Task ID: calc_nrv_086
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): List validation exists on B2:B30
  Component 2 (0.3): Formula1 references Categories!$A$2:$A$15
  Component 3 (0.2): Error style is 'stop' with title 'Invalid Category'
  Component 4 (0.2): Error message is correct
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_086'


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
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the main sheet (Sheet1) with the data
    ws = None
    for sheet_name in wb.sheetnames:
        s = wb[sheet_name]
        if s['A1'].value == 'Transaction' and s['B1'].value == 'Category':
            ws = s
            break

    if ws is None:
        print("FAIL: Could not find main sheet with Transaction/Category headers")
        print("REWARD: 0.0")
        return 0.0

    # Get all data validations
    validations = ws.data_validations.dataValidation
    print(f"INFO: Found {len(validations)} data validation(s) on sheet '{ws.title}'")

    # Find the list validation that covers B2:B30
    target_dv = None
    for dv in validations:
        if dv.type == "list":
            # Check if it covers B2:B30 range
            sqref_str = str(dv.sqref).upper().replace(" ", "")
            if "B2:B30" in sqref_str:
                target_dv = dv
                break

    # Component 1: List validation exists on B2:B30 (0.3 points)
    try:
        if target_dv is not None:
            print(f"PASS: Component 1 - List validation found on range {target_dv.sqref} (0.3 pts)")
            total_score += 0.3
        else:
            # Check if there's any list validation at all (even on wrong range)
            any_list = [dv for dv in validations if dv.type == "list"]
            if any_list:
                print(f"FAIL: Component 1 - List validation found but on wrong range: {any_list[0].sqref}, expected B2:B30")
            else:
                print(f"FAIL: Component 1 - No list data validation found on B2:B30")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Formula1 references Categories!$A$2:$A$15 (0.3 points)
    try:
        if target_dv is not None:
            formula = str(target_dv.formula1).strip() if target_dv.formula1 else ""
            # Normalize for comparison: remove leading '=', uppercase, remove spaces
            norm_formula = formula.upper().replace(" ", "").lstrip("=")
            expected_variants = [
                "CATEGORIES!$A$2:$A$15",
                "=CATEGORIES!$A$2:$A$15",
                "'CATEGORIES'!$A$2:$A$15",
                "CATEGORIES!$A$2:$A$15",
            ]
            norm_expected = [v.upper().replace(" ", "").lstrip("=") for v in expected_variants]

            if norm_formula in norm_expected:
                print(f"PASS: Component 2 - Formula1 correctly references Categories sheet: {formula} (0.3 pts)")
                total_score += 0.3
            else:
                # Partial: at least references Categories sheet
                if "CATEGORIES" in norm_formula:
                    print(f"PARTIAL: Component 2 - References Categories but formula differs: {formula}")
                    total_score += 0.1
                else:
                    print(f"FAIL: Component 2 - Formula1 is '{formula}', expected reference to Categories!$A$2:$A$15")
        else:
            print(f"FAIL: Component 2 - No target validation found, cannot check formula")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Error style is 'stop' and title is 'Invalid Category' (0.2 points)
    try:
        if target_dv is not None:
            error_style = str(target_dv.errorStyle).lower().strip() if target_dv.errorStyle else ""
            error_title = str(target_dv.errorTitle).strip() if target_dv.errorTitle else ""

            style_ok = error_style == "stop"
            title_ok = error_title == "Invalid Category"

            if style_ok and title_ok:
                print(f"PASS: Component 3 - Error style='stop', title='Invalid Category' (0.2 pts)")
                total_score += 0.2
            elif style_ok or title_ok:
                print(f"PARTIAL: Component 3 - style='{error_style}' (expect 'stop'), title='{error_title}' (expect 'Invalid Category')")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3 - style='{error_style}', title='{error_title}'")
        else:
            print(f"FAIL: Component 3 - No target validation found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Error message is correct (0.2 points)
    try:
        if target_dv is not None:
            error_msg = str(target_dv.error).strip() if target_dv.error else ""
            expected_msg = "Please select a valid category from the dropdown."

            if error_msg == expected_msg:
                print(f"PASS: Component 4 - Error message matches exactly (0.2 pts)")
                total_score += 0.2
            elif error_msg.lower() == expected_msg.lower():
                print(f"PARTIAL: Component 4 - Error message matches (case-insensitive): '{error_msg}'")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 - Error message is '{error_msg}', expected '{expected_msg}'")
        else:
            print(f"FAIL: Component 4 - No target validation found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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
