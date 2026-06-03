"""
Reward Script: Correct VLOOKUP typo in cell D5
Task ID: calc_tbl_066
Domain: libreoffice_calc
Scoring:
  Component 1 (0.6): D5 contains =VLOOKUP (corrected from =VLOKUP)
  Component 2 (0.4): Full formula matches =VLOOKUP(A5,B:C,2,0) exactly (correct function + preserved arguments)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_tbl_066'


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
    Verify that D5's formula has been corrected from =VLOKUP to =VLOOKUP.
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

    # Get D5 value
    d5_value = ws["D5"].value

    if d5_value is None:
        print(f"FAIL: D5 is empty (None)")
        print("REWARD: 0.0")
        return 0.0

    d5_str = str(d5_value).strip()
    d5_upper = d5_str.upper().replace(" ", "")

    # Component 1: D5 contains VLOOKUP (not VLOKUP or other misspelling) (0.6 points)
    # This FAILS on initial (has VLOKUP) and PASSES on golden (has VLOOKUP)
    try:
        if "VLOOKUP" in d5_upper and "VLOKUP" not in d5_upper:
            print(f"PASS: Component 1 - D5 contains corrected VLOOKUP function (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 - D5 does not contain corrected VLOOKUP. Found: {d5_str}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Full formula is exactly =VLOOKUP(A5,B:C,2,0) (0.4 points)
    # This anchors on the VLOOKUP correction AND verifies arguments are preserved.
    # FAILS on initial (has VLOKUP), PASSES on golden (has VLOOKUP with correct args)
    try:
        expected_formula = "=VLOOKUP(A5,B:C,2,0)"
        if d5_upper == expected_formula.upper().replace(" ", ""):
            print(f"PASS: Component 2 - Full formula matches exactly: {expected_formula} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 - Expected exact formula {expected_formula}, found: {d5_str}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

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
