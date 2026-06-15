"""
Reward Script: Weekday date validation on column B (B2:B50)
Task ID: calc_nrv_073
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30): Custom data validation exists on the worksheet
  Component 2 (0.30): Validation covers the range B2:B50
  Component 3 (0.25): Formula checks weekday (WEEKDAY(B2,2)<=5 or equivalent)
  Component 4 (0.15): Error message is configured with stop style
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_073'


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
    import openpyxl

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
        dvs = ws.data_validations.dataValidation
    except Exception as e:
        print(f"CRITICAL: Cannot access data validations: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: A custom data validation exists (0.30 points)
    # The initial file has zero validations, so any custom validation is task-introduced.
    try:
        custom_dv = None
        for dv in dvs:
            if dv.type == "custom":
                custom_dv = dv
                break
        if custom_dv is not None:
            print(f"PASS: Component 1 — Custom data validation found (type={custom_dv.type}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — No custom data validation found. Found {len(dvs)} validations with types: {[d.type for d in dvs]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Validation covers range B2:B50 (0.30 points)
    # Check that the custom validation's sqref includes B2:B50
    try:
        if custom_dv is not None:
            sqref_str = str(custom_dv.sqref).upper().replace(" ", "")
            # The range could be expressed as "B2:B50" exactly, or as multiple ranges
            # We check that it covers all of B2:B50
            # Parse the sqref ranges to check coverage
            target_rows = set(range(2, 51))  # rows 2 through 50
            covered_rows = set()
            for rng in sqref_str.split():
                # Handle both single cell and range
                if ':' in rng:
                    parts = rng.split(':')
                    # Extract column letter and row number
                    match_start = re.match(r'([A-Z]+)(\d+)', parts[0])
                    match_end = re.match(r'([A-Z]+)(\d+)', parts[1])
                    if match_start and match_end:
                        col_s, row_s = match_start.group(1), int(match_start.group(2))
                        col_e, row_e = match_end.group(1), int(match_end.group(2))
                        if col_s == 'B' and col_e == 'B':
                            for r in range(row_s, row_e + 1):
                                covered_rows.add(r)
                else:
                    match_cell = re.match(r'([A-Z]+)(\d+)', rng)
                    if match_cell and match_cell.group(1) == 'B':
                        covered_rows.add(int(match_cell.group(2)))

            if target_rows.issubset(covered_rows):
                print(f"PASS: Component 2 — Validation covers B2:B50 (sqref={sqref_str}) (0.30 pts)")
                total_score += 0.30
            else:
                missing = target_rows - covered_rows
                print(f"FAIL: Component 2 — Validation does not cover all of B2:B50. sqref={sqref_str}, missing rows: {sorted(missing)[:10]}...")
        else:
            print(f"FAIL: Component 2 — No custom validation found to check range")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Formula checks weekday via WEEKDAY function (0.25 points)
    # Expected: =WEEKDAY(B2,2)<=5 or similar variants
    try:
        if custom_dv is not None:
            formula = str(custom_dv.formula1).upper().replace(" ", "") if custom_dv.formula1 else ""
            # Check that the formula uses WEEKDAY function and checks <=5
            has_weekday = "WEEKDAY(" in formula
            has_comparison = "<=5" in formula or "<6" in formula
            # Also accept WEEKDAY(B2,2) specifically
            has_b2_ref = "B2" in formula
            if has_weekday and has_comparison and has_b2_ref:
                print(f"PASS: Component 3 — Formula uses WEEKDAY with <=5 check (formula={custom_dv.formula1}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Formula does not match expected pattern. formula={custom_dv.formula1}, has_weekday={has_weekday}, has_comparison={has_comparison}, has_b2_ref={has_b2_ref}")
        else:
            print(f"FAIL: Component 3 — No custom validation found to check formula")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Error handling is configured with stop style (0.15 points)
    # The validation should show an error message and use "stop" style
    try:
        if custom_dv is not None:
            show_error = custom_dv.showErrorMessage
            error_style = str(custom_dv.errorStyle).lower() if custom_dv.errorStyle else ""
            if show_error and error_style == "stop":
                print(f"PASS: Component 4 — Error message enabled with stop style (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — showErrorMessage={show_error}, errorStyle={error_style}")
        else:
            print(f"FAIL: Component 4 — No custom validation found to check error config")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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
