"""
Reward Script: Apply custom data validation to cell C2
Task ID: calc_nrv_074
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Custom data validation exists on C2
  Component 2 (0.4): Formula contains OR/AND logic for integers 1-999 and "N/A"
  Component 3 (0.3): Error/input messages properly configured
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_074'


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

    # Component 1: Custom data validation exists on C2 (0.3 points)
    try:
        validations = ws.data_validations.dataValidation
        c2_dv = None
        for dv in validations:
            sqref_str = str(dv.sqref)
            # Check if C2 is in the sqref range
            if 'C2' in sqref_str:
                c2_dv = dv
                break

        if c2_dv is not None and c2_dv.type == 'custom':
            print(f"PASS: Component 1 — Custom data validation found on C2 (type={c2_dv.type}) (0.3 pts)")
            total_score += 0.3
        elif c2_dv is not None:
            print(f"PARTIAL: Component 1 — Data validation found on C2 but type is '{c2_dv.type}', expected 'custom' (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — No data validation found on C2. Found {len(validations)} validations total.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Formula contains OR/AND logic for integers 1-999 and "N/A" (0.4 points)
    try:
        if c2_dv is not None and c2_dv.formula1:
            formula = str(c2_dv.formula1).upper().replace(" ", "")
            print(f"  DEBUG: formula1 = {c2_dv.formula1}")

            has_or = 'OR(' in formula
            has_and = 'AND(' in formula
            has_isnumber = 'ISNUMBER(' in formula
            has_int_check = 'INT(' in formula
            has_ge_1 = '>=1' in formula or '>0' in formula
            has_le_999 = '<=999' in formula or '<1000' in formula
            has_na = '"N/A"' in formula or "'N/A'" in formula.replace('"', "'")

            sub_score = 0.0
            # OR function present (enables dual-condition logic)
            if has_or:
                sub_score += 0.1
            # AND with integer validation (ISNUMBER + INT check)
            if has_and and has_isnumber and has_int_check:
                sub_score += 0.1
            # Range bounds 1-999
            if has_ge_1 and has_le_999:
                sub_score += 0.1
            # N/A text acceptance
            if has_na:
                sub_score += 0.1

            if sub_score > 0:
                print(f"PASS: Component 2 — Formula logic verified (OR={has_or}, AND={has_and}, ISNUMBER={has_isnumber}, INT={has_int_check}, range=[{has_ge_1},{has_le_999}], N/A={has_na}) ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 — Formula does not contain expected logic components")
        else:
            print(f"FAIL: Component 2 — No formula1 found on C2 validation")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error and input messages configured (0.3 points)
    try:
        if c2_dv is not None:
            sub_score = 0.0

            # Error message enabled and non-empty
            if c2_dv.showErrorMessage and c2_dv.error:
                sub_score += 0.15
                print(f"  PASS: Error message configured: '{c2_dv.error}'")
            else:
                print(f"  FAIL: Error message not configured (showErrorMessage={c2_dv.showErrorMessage}, error={c2_dv.error!r})")

            # Input/prompt message enabled and non-empty
            if c2_dv.showInputMessage and c2_dv.prompt:
                sub_score += 0.15
                print(f"  PASS: Input message configured: '{c2_dv.prompt}'")
            else:
                print(f"  FAIL: Input message not configured (showInputMessage={c2_dv.showInputMessage}, prompt={c2_dv.prompt!r})")

            if sub_score > 0:
                print(f"PASS: Component 3 — Messages configured ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 3 — No messages configured")
        else:
            print(f"FAIL: Component 3 — No validation to check messages on")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
