"""
Reward Script: Set up data validation on cell D2 for decimal discount rate (0 < value <= 1.0)
Task ID: calc_nrv_048
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Data validation exists targeting D2
  Component 2 (0.4): Validation type is decimal, operator=between, min=0, max=1
  Component 3 (0.3): Error message and input prompt are configured
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_048'


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

    # Find data validation targeting D2
    dvs = ws.data_validations.dataValidation
    target_dv = None
    for dv in dvs:
        # sqref can be a CellRange or multi-range; check if D2 is covered
        sqref_str = str(dv.sqref)
        if 'D2' in sqref_str:
            target_dv = dv
            break

    # Component 1: Data validation exists on D2 (0.3 points)
    try:
        if target_dv is not None:
            print(f"PASS: Component 1 — Data validation found targeting D2 (sqref={target_dv.sqref}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No data validation found targeting D2. Found {len(dvs)} validation(s) total.")
            for i, dv in enumerate(dvs):
                print(f"  DV {i}: sqref={dv.sqref}, type={dv.type}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Validation type=decimal, operator=between, min~0, max~1 (0.4 points)
    try:
        if target_dv is not None:
            type_ok = target_dv.type == 'decimal'
            operator_ok = target_dv.operator == 'between'

            # Check min value: should be 0 or close (e.g., 0, 0.001, etc.)
            # The key requirement is > 0 exclusive, so min could be 0 (with between meaning > min)
            # or could be a small value like 0.001
            try:
                min_val = float(target_dv.formula1) if target_dv.formula1 is not None else None
            except (ValueError, TypeError):
                min_val = None
            min_ok = min_val is not None and min_val >= 0 and min_val <= 0.01

            # Check max value: should be 1 or 1.0
            try:
                max_val = float(target_dv.formula2) if target_dv.formula2 is not None else None
            except (ValueError, TypeError):
                max_val = None
            max_ok = max_val is not None and abs(max_val - 1.0) < 0.001

            sub_score = 0.0
            if type_ok:
                sub_score += 0.15
                print(f"  PASS: type=decimal")
            else:
                print(f"  FAIL: type expected 'decimal', found '{target_dv.type}'")

            if operator_ok:
                sub_score += 0.05
                print(f"  PASS: operator=between")
            else:
                print(f"  FAIL: operator expected 'between', found '{target_dv.operator}'")

            if min_ok:
                sub_score += 0.1
                print(f"  PASS: formula1 (min)={min_val} (close to 0)")
            else:
                print(f"  FAIL: formula1 (min) expected ~0, found '{target_dv.formula1}'")

            if max_ok:
                sub_score += 0.1
                print(f"  PASS: formula2 (max)={max_val} (= 1.0)")
            else:
                print(f"  FAIL: formula2 (max) expected 1.0, found '{target_dv.formula2}'")

            if sub_score > 0:
                print(f"PASS: Component 2 — Validation parameters ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 — All validation parameter checks failed")
        else:
            print(f"FAIL: Component 2 — No target validation to check parameters")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error message and input prompt configured (0.3 points)
    try:
        if target_dv is not None:
            sub_score = 0.0

            # Check that error message is set (showErrorMessage=True and error text non-empty)
            has_error_msg = (
                target_dv.showErrorMessage
                and target_dv.error is not None
                and len(str(target_dv.error).strip()) > 0
            )
            if has_error_msg:
                sub_score += 0.15
                print(f"  PASS: Error message configured: '{target_dv.error}'")
            else:
                print(f"  FAIL: Error message not properly configured (showErrorMessage={target_dv.showErrorMessage}, error='{target_dv.error}')")

            # Check that input prompt is set (showInputMessage=True and prompt text non-empty)
            has_prompt = (
                target_dv.showInputMessage
                and target_dv.prompt is not None
                and len(str(target_dv.prompt).strip()) > 0
            )
            if has_prompt:
                sub_score += 0.15
                print(f"  PASS: Input prompt configured: '{target_dv.prompt}'")
            else:
                print(f"  FAIL: Input prompt not properly configured (showInputMessage={target_dv.showInputMessage}, prompt='{target_dv.prompt}')")

            if sub_score > 0:
                print(f"PASS: Component 3 — Messages configured ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 3 — No messages configured")
        else:
            print(f"FAIL: Component 3 — No target validation to check messages")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
