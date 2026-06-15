"""
Reward Script: Data validation on budget spreadsheet
Task ID: calc_gcv_077
Domain: libreoffice_calc
Scoring:
  C1 (0.25): Data validation exists on D2:D35 with type=custom
  C2 (0.25): Formula is =D2<=C2
  C3 (0.15): Error style is 'stop'
  C4 (0.15): Error title is 'Over Budget'
  C5 (0.20): Error message matches expected text
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_077'


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
    Verify data validation on D2:D35 with progressive scoring.
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

    # Find the relevant data validation (if any) that covers D2:D35
    dvs = ws.data_validations.dataValidation
    target_dv = None

    for dv in dvs:
        sqref_str = str(dv.sqref).upper().replace(" ", "")
        # Check if the validation covers D2:D35 (exactly or as part of ranges)
        if "D2:D35" in sqref_str:
            target_dv = dv
            break

    # Component 1: Data validation exists on D2:D35 with type=custom (0.25 pts)
    try:
        if target_dv is not None and target_dv.type == "custom":
            print(f"PASS: Component 1 — Custom data validation found on D2:D35 (0.25 pts)")
            total_score += 0.25
        elif target_dv is not None:
            print(f"FAIL: Component 1 — Data validation found but type is '{target_dv.type}', expected 'custom'")
        else:
            print(f"FAIL: Component 1 — No data validation found covering D2:D35 (found {len(dvs)} validations total)")
            for i, dv in enumerate(dvs):
                print(f"  DV {i}: type={dv.type}, sqref={dv.sqref}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Formula is =D2<=C2 (0.25 pts)
    try:
        if target_dv is not None:
            formula = str(target_dv.formula1).strip() if target_dv.formula1 else ""
            # Normalize: remove leading = if present, compare case-insensitively
            normalized = formula.upper().replace(" ", "")
            # Accept both "=D2<=C2" and "D2<=C2" (openpyxl may store with or without =)
            if normalized in ("=D2<=C2", "D2<=C2"):
                print(f"PASS: Component 2 — Formula is '{formula}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — Formula is '{formula}', expected '=D2<=C2'")
        else:
            print(f"FAIL: Component 2 — No target validation found, cannot check formula")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error style is 'stop' (0.15 pts)
    try:
        if target_dv is not None:
            error_style = str(target_dv.errorStyle).lower() if target_dv.errorStyle else ""
            if error_style == "stop":
                print(f"PASS: Component 3 — Error style is 'stop' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Error style is '{error_style}', expected 'stop'")
        else:
            print(f"FAIL: Component 3 — No target validation found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Error title is 'Over Budget' (0.15 pts)
    try:
        if target_dv is not None:
            title = str(target_dv.errorTitle).strip() if target_dv.errorTitle else ""
            if title == "Over Budget":
                print(f"PASS: Component 4 — Error title is 'Over Budget' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Error title is '{title}', expected 'Over Budget'")
        else:
            print(f"FAIL: Component 4 — No target validation found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Error message matches expected text (0.20 pts)
    try:
        if target_dv is not None:
            msg = str(target_dv.error).strip() if target_dv.error else ""
            expected_msg = "Requested budget cannot exceed allocated amount."
            if msg == expected_msg:
                print(f"PASS: Component 5 — Error message matches exactly (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 — Error message is '{msg}', expected '{expected_msg}'")
        else:
            print(f"FAIL: Component 5 — No target validation found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
