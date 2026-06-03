"""
Reward Script: Data validation dropdown on B2 sourced from A2:A100
Task ID: calc_nrv_089
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Data validation exists targeting B2
  Component 2 (0.3): Validation type is 'list'
  Component 3 (0.4): Validation formula1 references $A$2:$A$100
"""

import os

import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_089'


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
    Verify that cell B2 has a list data validation with source $A$2:$A$100.
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

    # Collect all data validations that apply to B2
    dvs = ws.data_validations.dataValidation
    b2_dv = None
    for dv in dvs:
        # sqref can contain multiple ranges; check if B2 is covered
        sqref_str = str(dv.sqref).upper()
        # Simple check: B2 in the sqref string, or the range covers B2
        if 'B2' in sqref_str:
            b2_dv = dv
            break

    # Component 1: Data validation exists targeting B2 (0.3 points)
    try:
        if b2_dv is not None:
            print(f"PASS: Component 1 — Data validation found on B2 (sqref: {b2_dv.sqref}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No data validation found targeting B2. Found {len(dvs)} validations total.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Validation type is 'list' (0.3 points)
    try:
        if b2_dv is not None and b2_dv.type == 'list':
            print(f"PASS: Component 2 — Validation type is 'list' (0.3 pts)")
            total_score += 0.3
        elif b2_dv is not None:
            print(f"FAIL: Component 2 — Expected type 'list', found '{b2_dv.type}'")
        else:
            print(f"FAIL: Component 2 — No validation on B2 to check type")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Formula1 references $A$2:$A$100 (0.4 points)
    try:
        if b2_dv is not None:
            formula1 = str(b2_dv.formula1).strip() if b2_dv.formula1 else ''
            # Normalize: remove quotes, spaces, and compare case-insensitively
            normalized = formula1.replace("'", "").replace('"', '').replace(' ', '').upper()
            expected = '$A$2:$A$100'
            if normalized == expected:
                print(f"PASS: Component 3 — formula1 is '{formula1}' matching {expected} (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 3 — Expected formula1 '{expected}', found '{formula1}' (normalized: '{normalized}')")
        else:
            print(f"FAIL: Component 3 — No validation on B2 to check formula1")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved state, then verify
persist_app_state("libreoffice_calc")

file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
