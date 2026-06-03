"""
Reward Script: Fix filtered dataset total formula
Task ID: calc_tbl_024
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): D101 uses SUBTOTAL function instead of SUM
  Component 2 (0.3): SUBTOTAL uses function_num 109 (SUM ignoring hidden rows)
  Component 3 (0.3): SUBTOTAL references the correct range D2:D100
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_tbl_024'


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

    The task requires changing D101 from =SUM(D2:D100) to =SUBTOTAL(109,D2:D100)
    so the total only sums visible (filtered) rows.
    """
    total_score = 0.0

    # Load workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the active/first sheet
    try:
        ws = wb.active
        if ws is None:
            ws = wb.worksheets[0]
    except Exception as e:
        print(f"CRITICAL: Cannot access worksheet: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Read the formula in D101
    d101_value = ws['D101'].value
    print(f"INFO: D101 raw value = {repr(d101_value)}")

    if d101_value is None or not isinstance(d101_value, str):
        print("FAIL: D101 is empty or not a formula")
        print("REWARD: 0.0")
        return 0.0

    # Normalize: strip spaces, uppercase for comparison
    formula_clean = d101_value.strip().upper().replace(" ", "")

    # Component 1: D101 uses SUBTOTAL function instead of SUM (0.4 points)
    # This is the core change — must use SUBTOTAL, not SUM
    try:
        if formula_clean.startswith("=SUBTOTAL("):
            print(f"PASS: Component 1 — D101 uses SUBTOTAL function (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — D101 does not use SUBTOTAL. Found: {d101_value}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: SUBTOTAL uses function_num 109 (0.3 points)
    # 109 = SUM ignoring manually hidden rows (correct for filtered data)
    # Also accept 9 which is the basic SUM variant of SUBTOTAL
    try:
        # Parse the function number from =SUBTOTAL(num, range)
        match = re.match(r'^=SUBTOTAL\((\d+),', formula_clean)
        if match:
            func_num = int(match.group(1))
            if func_num == 109:
                print(f"PASS: Component 2 — SUBTOTAL function_num is 109 (0.3 pts)")
                total_score += 0.3
            elif func_num == 9:
                # 9 is acceptable but less precise than 109
                print(f"PARTIAL: Component 2 — SUBTOTAL function_num is 9 (acceptable, 0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Expected function_num 109, found {func_num}")
        else:
            print(f"FAIL: Component 2 — Could not parse SUBTOTAL function_num from: {d101_value}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: SUBTOTAL references correct range D2:D100 (0.3 points)
    try:
        # Parse the range from =SUBTOTAL(num, range)
        match = re.match(r'^=SUBTOTAL\(\d+,(.*)\)$', formula_clean)
        if match:
            range_ref = match.group(1).strip()
            if range_ref == "D2:D100":
                print(f"PASS: Component 3 — SUBTOTAL range is D2:D100 (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Expected range D2:D100, found {range_ref}")
        else:
            print(f"FAIL: Component 3 — Could not parse SUBTOTAL range from: {d101_value}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved state before verification
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
