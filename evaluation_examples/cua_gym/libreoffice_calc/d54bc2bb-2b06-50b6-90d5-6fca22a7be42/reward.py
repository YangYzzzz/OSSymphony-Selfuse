"""
Reward Script: Remove sheet protection from 'Budget' sheet
Task ID: calc_gsi_017
Domain: libreoffice_calc
Scoring:
  Component 1 (0.6): Budget sheet protection is disabled (sheet=False)
  Component 2 (0.4): Budget sheet password is cleared (password=None)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_017'


def persist_app_state(domain: str):
    """Best-effort save of any open LibreOffice instance."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for", domain)
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that the Budget sheet protection has been removed.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Budget sheet must exist
    if 'Budget' not in wb.sheetnames:
        print("CRITICAL: 'Budget' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Budget']

    # Component 1: Budget sheet protection is disabled (0.6 points)
    # Initial: ws.protection.sheet == True  -> FAIL
    # Golden:  ws.protection.sheet == False -> PASS
    try:
        protection_enabled = ws.protection.sheet
        if protection_enabled is False or protection_enabled is None:
            print(f"PASS: Component 1 — Budget sheet protection is disabled (sheet={protection_enabled}) (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — Budget sheet is still protected (sheet={protection_enabled})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Budget sheet password is cleared (0.4 points)
    # Initial: ws.protection.password == '90F8' (hashed) -> FAIL
    # Golden:  ws.protection.password == None             -> PASS
    try:
        pwd = ws.protection.password
        if pwd is None or pwd == '' or pwd == 0:
            print(f"PASS: Component 2 — Budget sheet password is cleared (password={pwd!r}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Budget sheet still has a password set (password={pwd!r})")
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
