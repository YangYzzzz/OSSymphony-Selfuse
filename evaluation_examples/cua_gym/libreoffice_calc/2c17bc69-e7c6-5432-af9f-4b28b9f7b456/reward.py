"""
Reward Script: Set columns A and B as repeating print title columns
Task ID: calc_gfl_085
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): print_title_cols is set and includes column A
  Component 2 (0.5): print_title_cols is exactly $A:$B (both columns A and B)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gfl_085'


def persist_app_state(domain: str):
    """Save any unsaved changes in LibreOffice before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
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
    total_score = 0.0

    # Load workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Sheet 'Data' must exist
    if 'Data' not in wb.sheetnames:
        print("FAIL: Sheet 'Data' not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Data']
    print_cols = ws.print_title_cols
    print(f"INFO: print_title_cols = {print_cols!r}")

    # Component 1: print_title_cols is set and includes column A (0.5 points)
    # This checks that at least column A is part of the repeating columns.
    try:
        if print_cols is not None:
            # Normalize: remove $ signs and spaces, uppercase
            normalized = print_cols.replace('$', '').replace(' ', '').upper()
            # Parse the column range, e.g. "A:B" -> start="A", end="B"
            parts = normalized.split(':')
            if len(parts) == 2:
                start_col = parts[0]
                end_col = parts[1]
                # Column A must be included: start_col must be 'A'
                if start_col == 'A':
                    print(f"PASS: Component 1 — print_title_cols includes column A (start={start_col}, end={end_col}) (0.5 pts)")
                    total_score += 0.5
                else:
                    print(f"FAIL: Component 1 — print_title_cols starts at column {start_col}, expected A")
            else:
                print(f"FAIL: Component 1 — print_title_cols has unexpected format: {print_cols}")
        else:
            print("FAIL: Component 1 — print_title_cols is not set (None)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: print_title_cols is exactly $A:$B (0.5 points)
    # This checks that both columns A and B are set as repeating columns.
    try:
        if print_cols is not None:
            normalized = print_cols.replace('$', '').replace(' ', '').upper()
            if normalized == 'A:B':
                print(f"PASS: Component 2 — print_title_cols is exactly A:B (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 — print_title_cols is '{print_cols}', expected '$A:$B'")
        else:
            print("FAIL: Component 2 — print_title_cols is not set (None)")
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
