"""
Reward Script: Navigate to 'December' sheet using Navigator
Task ID: calc_gsi_074
Domain: libreoffice_calc
Scoring:
  Component 1 (0.6): Active sheet is 'December'
  Component 2 (0.4): Workbook view activeTab == 11 (December's index)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_074'


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
    Verify that the user navigated to the 'December' sheet.
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

    # Component 1: Active sheet is 'December' (0.6 points)
    # In initial_env, active sheet is 'January' -> FAIL
    # In golden_env, active sheet is 'December' -> PASS
    try:
        active_title = wb.active.title
        if active_title == "December":
            print(f"PASS: Component 1 -- Active sheet is 'December' (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 -- Expected active sheet 'December', found '{active_title}'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Workbook view activeTab == 11 (December is the 12th sheet, 0-indexed = 11) (0.4 points)
    # In initial_env, activeTab is 0 -> FAIL
    # In golden_env, activeTab is 11 -> PASS
    try:
        active_tab = wb.views[0].activeTab if wb.views else None
        if active_tab == 11:
            print(f"PASS: Component 2 -- activeTab is 11 (December index) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 -- Expected activeTab=11, found activeTab={active_tab}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist GUI state before verification
persist_app_state("libreoffice_calc")

# Test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
