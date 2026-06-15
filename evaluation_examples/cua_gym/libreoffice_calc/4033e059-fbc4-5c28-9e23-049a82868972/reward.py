"""
Reward Script: Configure page setup to center printed content horizontally and vertically
Task ID: calc_gfl_087
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): Horizontal centering enabled
  Component 2 (0.5): Vertical centering enabled
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gfl_087'


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
    Verify that the page setup has horizontal and vertical centering enabled.
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

    # Get the Certificate sheet (active/first sheet)
    try:
        ws = wb['Certificate']
    except KeyError:
        ws = wb.active
        print(f"WARNING: 'Certificate' sheet not found, using active sheet: {ws.title}")

    # Component 1: Horizontal centering enabled (0.5 points)
    try:
        h_centered = ws.print_options.horizontalCentered
        if h_centered is True:
            print(f"PASS: Component 1 — horizontalCentered is True (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected horizontalCentered=True, found: {h_centered}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Vertical centering enabled (0.5 points)
    try:
        v_centered = ws.print_options.verticalCentered
        if v_centered is True:
            print(f"PASS: Component 2 — verticalCentered is True (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — expected verticalCentered=True, found: {v_centered}")
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
