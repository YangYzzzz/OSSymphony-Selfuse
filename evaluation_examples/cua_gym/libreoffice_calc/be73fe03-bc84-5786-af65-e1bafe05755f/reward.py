"""
Reward Script: Protect workbook structure with password
Task ID: calc_gsi_018
Domain: libreoffice_calc
Scoring:
  Component 1 (0.6): lockStructure is True
  Component 2 (0.4): workbookPassword is set (non-None, non-empty)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_018'


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
    Verify workbook structure protection with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: lockStructure is True (0.6 points)
    # This checks that the workbook structure is locked, preventing
    # sheets from being added, deleted, moved, or renamed.
    try:
        security = wb.security
        if security and security.lockStructure is True:
            print(f"PASS: Component 1 - lockStructure is True (0.6 pts)")
            total_score += 0.6
        else:
            lock_val = security.lockStructure if security else None
            print(f"FAIL: Component 1 - lockStructure expected True, found: {lock_val}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: workbookPassword is set (0.4 points)
    # A password must be applied to enforce the protection.
    # Without a password, structure protection can be trivially removed.
    try:
        security = wb.security
        if security and security.workbookPassword and len(str(security.workbookPassword).strip()) > 0:
            print(f"PASS: Component 2 - workbookPassword is set (hash present) (0.4 pts)")
            total_score += 0.4
        else:
            pwd_val = security.workbookPassword if security else None
            print(f"FAIL: Component 2 - workbookPassword expected non-empty, found: {pwd_val}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state("libreoffice_calc")
    verify_task(file_path)
