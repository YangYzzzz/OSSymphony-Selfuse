"""
Reward Script: Data validation on cell C2 — uppercase-only custom formula
Task ID: calc_nrv_069
Domain: libreoffice_calc
Scoring:
  Component 1 (0.35): Custom data validation exists targeting C2
  Component 2 (0.35): Formula is =EXACT(C2,UPPER(C2))
  Component 3 (0.15): Error message is configured
  Component 4 (0.15): Input prompt is configured
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_069'


def persist_app_state(domain: str):
    """Best-effort save via Ctrl+S in case file is still open in LibreOffice."""
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


def find_validation_for_c2(ws):
    """Find the data validation rule that applies to cell C2."""
    dvs = ws.data_validations.dataValidation
    for dv in dvs:
        sqref_str = str(dv.sqref).upper()
        # Check if C2 is explicitly in the sqref range
        if 'C2' in sqref_str:
            return dv
    return None


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

    # Find data validation targeting C2
    dv = find_validation_for_c2(ws)

    # Component 1: Custom data validation exists on C2 (0.35 points)
    try:
        if dv is not None and dv.type == 'custom':
            print(f"PASS: Component 1 — Custom data validation found on C2 (type={dv.type}) (0.35 pts)")
            total_score += 0.35
        elif dv is not None:
            print(f"FAIL: Component 1 — Data validation on C2 exists but type is '{dv.type}', expected 'custom'")
        else:
            print(f"FAIL: Component 1 — No data validation found targeting C2")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Formula is =EXACT(C2,UPPER(C2)) (0.35 points)
    try:
        if dv is not None and dv.formula1 is not None:
            formula = str(dv.formula1).strip()
            # Normalize for comparison: remove spaces and uppercase
            formula_norm = formula.upper().replace(" ", "")
            expected_norm = "=EXACT(C2,UPPER(C2))".upper().replace(" ", "")
            if formula_norm == expected_norm:
                print(f"PASS: Component 2 — Formula matches: {formula} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — Formula is '{formula}', expected '=EXACT(C2,UPPER(C2))'")
        else:
            print(f"FAIL: Component 2 — No formula found on C2 validation")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error message is configured (0.15 points)
    # showErrorMessage should be True AND error text should be non-empty
    try:
        if dv is not None:
            has_error_msg = (dv.showErrorMessage is True or dv.showErrorMessage is None) and dv.error and len(str(dv.error).strip()) > 0
            if has_error_msg:
                print(f"PASS: Component 3 — Error message configured: '{dv.error}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Error message not properly configured (showErrorMessage={dv.showErrorMessage}, error='{dv.error}')")
        else:
            print(f"FAIL: Component 3 — No data validation found on C2")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Input prompt is configured (0.15 points)
    # showInputMessage should be True AND prompt text should be non-empty
    try:
        if dv is not None:
            has_prompt = (dv.showInputMessage is True or dv.showInputMessage is None) and dv.prompt and len(str(dv.prompt).strip()) > 0
            if has_prompt:
                print(f"PASS: Component 4 — Input prompt configured: '{dv.prompt}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Input prompt not properly configured (showInputMessage={dv.showInputMessage}, prompt='{dv.prompt}')")
        else:
            print(f"FAIL: Component 4 — No data validation found on C2")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
persist_app_state("libreoffice_calc")

file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
