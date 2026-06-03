"""
Reward Script: Delete three obsolete named ranges from spreadsheet
Task ID: calc_nrv_031
Domain: libreoffice_calc
Scoring:
  - Component 1: 'test_range' named range deleted (0.25)
  - Component 2: 'backup_data' named range deleted (0.25)
  - Component 3: 'old_summary' named range deleted (0.25)
  - Component 4: 'ActiveData' and 'Config' named ranges preserved (0.25)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_031'


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

    # Get all defined names
    try:
        defined_names = set(wb.defined_names)
        print(f"INFO: Found defined names: {defined_names}")
    except Exception as e:
        print(f"ERROR: Cannot read defined names: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'test_range' named range is deleted (0.25 points)
    try:
        if 'test_range' not in defined_names:
            print(f"PASS: Component 1 — 'test_range' has been deleted (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — 'test_range' still exists, expected it to be deleted")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'backup_data' named range is deleted (0.25 points)
    try:
        if 'backup_data' not in defined_names:
            print(f"PASS: Component 2 — 'backup_data' has been deleted (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — 'backup_data' still exists, expected it to be deleted")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'old_summary' named range is deleted (0.25 points)
    try:
        if 'old_summary' not in defined_names:
            print(f"PASS: Component 3 — 'old_summary' has been deleted (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — 'old_summary' still exists, expected it to be deleted")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Exactly 2 named ranges remain ('ActiveData' and 'Config') (0.25 points)
    # This checks that ONLY the correct ranges survive — no extras, no missing keepers
    try:
        active_exists = 'ActiveData' in defined_names
        config_exists = 'Config' in defined_names
        total_count = len(defined_names)

        if active_exists and config_exists and total_count == 2:
            print(f"PASS: Component 4 — Exactly 2 named ranges remain: 'ActiveData' and 'Config' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Expected exactly {{'ActiveData', 'Config'}}, found {defined_names} (count={total_count})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_calc")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
