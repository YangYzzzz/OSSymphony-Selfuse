"""
Reward Script: Change SUM formula to SUBTOTAL(109,...) to exclude hidden rows
Task ID: calc_tbl_023
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): B25 uses SUBTOTAL function instead of SUM
  Component 2 (0.3): SUBTOTAL function_num is 109 (sum, ignore hidden rows)
  Component 3 (0.3): SUBTOTAL range covers B1:B24
"""

import os
import re
import time


WORKDIR = '/home/user'
TASK_ID = 'calc_tbl_023'


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

    # Get the formula in B25
    b25_value = ws['B25'].value
    print(f"INFO: B25 raw value = {b25_value!r}")

    if b25_value is None or not isinstance(b25_value, str):
        print("FAIL: B25 does not contain a formula string")
        print("REWARD: 0.0")
        return 0.0

    # Normalize: uppercase, strip spaces
    formula = b25_value.strip().upper().replace(" ", "")

    # Component 1: B25 uses SUBTOTAL function instead of SUM (0.4 points)
    # This is the core task change: switching from =SUM(...) to =SUBTOTAL(...)
    try:
        if "SUBTOTAL(" in formula and formula.startswith("=SUBTOTAL("):
            print(f"PASS: Component 1 — B25 uses SUBTOTAL function (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — B25 does not use SUBTOTAL. Found: {b25_value}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: SUBTOTAL function_num is 109 (0.3 points)
    # 109 = SUM ignoring hidden values. Other valid alternatives could be 9 (SUM ignoring
    # nested SUBTOTAL but NOT hidden rows), but only 109 correctly excludes hidden rows.
    try:
        # Extract the function number from SUBTOTAL(num, range)
        match = re.match(r'^=SUBTOTAL\((\d+),', formula)
        if match:
            func_num = int(match.group(1))
            if func_num == 109:
                print(f"PASS: Component 2 — SUBTOTAL uses function_num 109 (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — SUBTOTAL function_num is {func_num}, expected 109")
        else:
            print(f"FAIL: Component 2 — Cannot parse SUBTOTAL function_num from: {b25_value}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: SUBTOTAL range covers B1:B24 (0.3 points)
    # The original range was B1:B24 and should be preserved in the new formula.
    try:
        match = re.match(r'^=SUBTOTAL\(\d+,(B\d+:B\d+)\)$', formula)
        if match:
            range_str = match.group(1)
            if range_str == "B1:B24":
                print(f"PASS: Component 3 — SUBTOTAL range is B1:B24 (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — SUBTOTAL range is {range_str}, expected B1:B24")
        else:
            print(f"FAIL: Component 3 — Cannot parse range from formula: {b25_value}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_calc")

# Test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
