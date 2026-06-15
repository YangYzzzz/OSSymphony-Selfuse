"""
Reward Script: Rename named range 'data_2023' to 'data_2024' and update reference
Task ID: calc_nrv_022
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): 'data_2023' named range no longer exists
  Component 2 (0.3): 'data_2024' named range exists
  Component 3 (0.4): 'data_2024' references Sheet1!$B$2:$B$60
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_022'


def persist_app_state():
    """Attempt to save any unsaved LibreOffice state via Ctrl+S."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_calc")
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

    # Get all defined names
    defined_names = dict(wb.defined_names)
    print(f"INFO: Found defined names: {list(defined_names.keys())}")

    # Component 1: 'data_2023' named range no longer exists (0.3 points)
    # This FAILS on initial (data_2023 exists) -> PASSES on golden (data_2023 removed)
    try:
        if 'data_2023' not in defined_names:
            print("PASS: Component 1 -- 'data_2023' no longer exists (0.3 pts)")
            total_score += 0.3
        else:
            ref = defined_names['data_2023'].attr_text
            print(f"FAIL: Component 1 -- 'data_2023' still exists with ref: {ref}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: 'data_2024' named range exists (0.3 points)
    # This FAILS on initial (no data_2024) -> PASSES on golden (data_2024 created)
    try:
        if 'data_2024' in defined_names:
            print("PASS: Component 2 -- 'data_2024' exists (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- 'data_2024' not found in defined names")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: 'data_2024' references Sheet1!$B$2:$B$60 (0.4 points)
    # This FAILS on initial (no data_2024) -> PASSES on golden (correct reference)
    try:
        if 'data_2024' in defined_names:
            ref = defined_names['data_2024'].attr_text
            # Normalize: remove quotes, uppercase for comparison
            normalized_ref = ref.replace("'", "").upper()
            expected_ref = "SHEET1!$B$2:$B$60"
            if normalized_ref == expected_ref:
                print(f"PASS: Component 3 -- 'data_2024' references {ref} (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 3 -- 'data_2024' references {ref}, expected Sheet1!$B$2:$B$60")
        else:
            print("FAIL: Component 3 -- 'data_2024' does not exist, cannot check reference")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
