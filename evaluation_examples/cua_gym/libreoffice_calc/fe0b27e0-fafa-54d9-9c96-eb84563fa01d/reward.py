"""
Reward Script: Data validation on B2:B25 with custom formula for name format
Task ID: calc_gcv_080
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25) - Data validation exists on correct range B2:B25
  Component 2 (0.35) - Validation type is 'custom' with correct formula
  Component 3 (0.20) - Error style is 'stop'
  Component 4 (0.20) - Error title and message match expected values
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_080'


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

    ws = wb.active

    # Get all data validations
    dvs = ws.data_validations.dataValidation

    if len(dvs) == 0:
        print("FAIL: No data validations found at all")
        print("REWARD: 0.0")
        return 0.0

    # Find a custom validation that covers B2:B25
    target_dv = None
    for dv in dvs:
        sqref_str = str(dv.sqref).replace(" ", "")
        # Check if sqref covers B2:B25 (could be written in different forms)
        if "B2:B25" in sqref_str or "B2:B25" == sqref_str:
            target_dv = dv
            break

    # Component 1: Data validation exists on correct range B2:B25 (0.25 points)
    try:
        if target_dv is not None:
            print(f"PASS: Component 1 - Data validation found on range B2:B25 (0.25 pts)")
            total_score += 0.25
        else:
            # Check if there's any validation with 'custom' type that at least partially covers the range
            for dv in dvs:
                sqref_str = str(dv.sqref)
                print(f"  Found DV on range: {sqref_str}, type: {dv.type}")
            print(f"FAIL: Component 1 - No data validation found on range B2:B25")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    if target_dv is None:
        # No matching validation found - can't check remaining components
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Validation type is 'custom' with correct formula (0.35 points)
    try:
        if target_dv.type == "custom":
            formula = target_dv.formula1 or ""
            # Normalize for comparison: remove spaces and compare uppercase
            norm_formula = formula.upper().replace(" ", "")
            expected_pattern = "=AND(EXACT(LEFT(B2,1),UPPER(LEFT(B2,1))),EXACT(MID(B2,2,LEN(B2)-1),LOWER(MID(B2,2,LEN(B2)-1))))".upper().replace(" ", "")
            if norm_formula == expected_pattern:
                print(f"PASS: Component 2 - Custom validation with correct formula (0.35 pts)")
                total_score += 0.35
            else:
                # Partial credit: type is custom but formula doesn't match exactly
                # Check if formula at least contains key functions
                has_exact = "EXACT" in norm_formula
                has_left = "LEFT" in norm_formula
                has_upper = "UPPER" in norm_formula
                has_lower = "LOWER" in norm_formula
                if has_exact and has_left and has_upper and has_lower:
                    print(f"PASS (partial): Component 2 - Custom validation with similar formula (0.20 pts)")
                    print(f"  Expected: {expected_pattern}")
                    print(f"  Found:    {norm_formula}")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 2 - Custom formula does not match")
                    print(f"  Expected: {expected_pattern}")
                    print(f"  Found:    {norm_formula}")
        else:
            print(f"FAIL: Component 2 - Validation type is '{target_dv.type}', expected 'custom'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Error style is 'stop' (0.20 points)
    try:
        error_style = (target_dv.errorStyle or "").lower()
        if error_style == "stop":
            print(f"PASS: Component 3 - Error style is 'stop' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 - Error style is '{error_style}', expected 'stop'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Error title and message match expected values (0.20 points)
    try:
        error_title = target_dv.errorTitle or ""
        error_msg = target_dv.error or ""

        title_match = error_title.strip() == "Invalid Name Format"
        msg_match = error_msg.strip() == "Name must start with uppercase followed by lowercase."

        if title_match and msg_match:
            print(f"PASS: Component 4 - Error title and message match (0.20 pts)")
            total_score += 0.20
        elif title_match or msg_match:
            print(f"PARTIAL: Component 4 - Only {'title' if title_match else 'message'} matches (0.10 pts)")
            print(f"  Title: '{error_title}' (expected: 'Invalid Name Format')")
            print(f"  Message: '{error_msg}' (expected: 'Name must start with uppercase followed by lowercase.')")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 - Error title and message do not match")
            print(f"  Title: '{error_title}' (expected: 'Invalid Name Format')")
            print(f"  Message: '{error_msg}' (expected: 'Name must start with uppercase followed by lowercase.')")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
