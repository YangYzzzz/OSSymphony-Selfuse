"""
Reward Script: Apply custom formula validation on C2 for email '@' check
Task ID: calc_nrv_063
Domain: libreoffice_calc
Scoring:
  Component 1 (0.40): C2 has a custom data validation applied
  Component 2 (0.35): Validation formula checks for '@' character using FIND/SEARCH
  Component 3 (0.25): Error message is enabled with meaningful text
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_063'


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

    ws = wb.active

    # Find data validation that covers C2
    dv_for_c2 = None
    for dv in ws.data_validations.dataValidation:
        sqref_str = str(dv.sqref)
        # Check if C2 is within the sqref ranges
        if 'C2' in sqref_str or 'C:C' in sqref_str:
            dv_for_c2 = dv
            break
        # Also check range patterns like C2:C100
        if re.search(r'C\d+:C\d+', sqref_str):
            # Parse the range to see if C2 is included
            match = re.search(r'C(\d+):C(\d+)', sqref_str)
            if match:
                start_row, end_row = int(match.group(1)), int(match.group(2))
                if start_row <= 2 <= end_row:
                    dv_for_c2 = dv
                    break

    # Component 1: C2 has a custom data validation (0.40 points)
    try:
        if dv_for_c2 is not None and dv_for_c2.type == "custom":
            print(f"PASS: Component 1 - C2 has custom data validation (type={dv_for_c2.type}) (0.40 pts)")
            total_score += 0.40
        elif dv_for_c2 is not None:
            print(f"PARTIAL: Component 1 - C2 has data validation but type is '{dv_for_c2.type}', expected 'custom'")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - No data validation found covering C2")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Validation formula checks for '@' using FIND or SEARCH (0.35 points)
    try:
        if dv_for_c2 is not None and dv_for_c2.formula1:
            formula = str(dv_for_c2.formula1).upper().replace(" ", "")
            # Check for FIND("@",...) or SEARCH("@",...) pattern
            has_at_check = (
                ('FIND("@"' in formula.replace("'", '"'))
                or ('SEARCH("@"' in formula.replace("'", '"'))
                or ("FIND(\"@\"" in formula)
                or ("SEARCH(\"@\"" in formula)
            )
            # Also check for references to C2 in the formula
            has_c2_ref = 'C2' in formula

            if has_at_check and has_c2_ref:
                print(f"PASS: Component 2 - Formula checks '@' in C2: {dv_for_c2.formula1} (0.35 pts)")
                total_score += 0.35
            elif has_at_check:
                print(f"PARTIAL: Component 2 - Formula checks '@' but doesn't reference C2: {dv_for_c2.formula1}")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 - Formula does not check for '@': {dv_for_c2.formula1}")
        else:
            print(f"FAIL: Component 2 - No formula found for validation on C2")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Error message is enabled (0.25 points)
    try:
        if dv_for_c2 is not None and dv_for_c2.showErrorMessage:
            error_text = str(dv_for_c2.error or "").lower()
            error_title = str(dv_for_c2.errorTitle or "").lower()
            combined = error_text + " " + error_title
            # Check that there is some error message content
            if len(error_text.strip()) > 0 or len(error_title.strip()) > 0:
                print(f"PASS: Component 3 - Error message enabled: title='{dv_for_c2.errorTitle}', msg='{dv_for_c2.error}' (0.25 pts)")
                total_score += 0.25
            else:
                # showErrorMessage is True but no custom text — still partial credit
                print(f"PARTIAL: Component 3 - showErrorMessage=True but no custom error text (0.10 pts)")
                total_score += 0.10
        elif dv_for_c2 is not None:
            print(f"FAIL: Component 3 - showErrorMessage is not enabled")
        else:
            print(f"FAIL: Component 3 - No validation found on C2")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

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
