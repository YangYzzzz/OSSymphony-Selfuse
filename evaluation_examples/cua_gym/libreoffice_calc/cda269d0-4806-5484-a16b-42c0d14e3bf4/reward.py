"""
Reward Script: Freeze Panes Adjustment
Task ID: calc_tbl_070
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): Old freeze (C5) removed from 'Regional Sales'
  Component 2 (0.5): New freeze set to B2 on 'Regional Sales'
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_tbl_070'


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
    Verify that freeze panes on 'Regional Sales' sheet changed from C5 to B2.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import openpyxl
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check that 'Regional Sales' sheet exists
    if 'Regional Sales' not in wb.sheetnames:
        print("CRITICAL: 'Regional Sales' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Regional Sales']
    freeze_value = ws.freeze_panes

    # Component 1: Old freeze (C5) has been removed (0.5 points)
    # This checks that the agent removed the original C5 freeze.
    # On initial_env: freeze_panes == "C5", so "C5" != "C5" is False => FAIL (correct)
    # On golden_env: freeze_panes == "B2", so "B2" != "C5" is True => PASS (correct)
    try:
        if freeze_value != "C5":
            print(f"PASS: Component 1 — Old freeze C5 removed (current: {freeze_value}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Freeze is still C5, expected it to be changed")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: New freeze set to exactly B2 (0.5 points)
    # On initial_env: freeze_panes == "C5", so "C5" == "B2" is False => FAIL (correct)
    # On golden_env: freeze_panes == "B2", so "B2" == "B2" is True => PASS (correct)
    try:
        if freeze_value == "B2":
            print(f"PASS: Component 2 — Freeze panes correctly set to B2 (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — Expected freeze_panes='B2', found: {freeze_value}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

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
