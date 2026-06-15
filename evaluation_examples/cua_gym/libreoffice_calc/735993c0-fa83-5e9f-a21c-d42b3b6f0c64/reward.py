"""
Reward Script: Define print area as A1:G35
Task ID: calc_gfl_051
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3) - Print area is defined (non-empty)
  Component 2 (0.4) - Print area covers correct columns A-G (start col A, end col G)
  Component 3 (0.3) - Print area covers correct rows 1-35 (start row 1, end row 35)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_gfl_051'


def persist_app_state(domain: str):
    """Best-effort save of any unsaved GUI edits."""
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


def parse_print_area(print_area_str):
    """
    Parse an openpyxl print_area string like "'Report'!$A$1:$G$35" or "A1:G35".
    Returns (start_col, start_row, end_col, end_row) as strings, or None.
    """
    if not print_area_str:
        return None
    # Remove sheet reference like 'Report'! or Report!
    area = re.sub(r"^'?[^'!]+'?!", "", str(print_area_str))
    # Remove dollar signs
    area = area.replace("$", "")
    # Match cell range pattern like A1:G35
    m = re.match(r'^([A-Z]+)(\d+):([A-Z]+)(\d+)$', area.strip(), re.IGNORECASE)
    if m:
        return m.group(1).upper(), int(m.group(2)), m.group(3).upper(), int(m.group(4))
    return None


def verify_task(file_path):
    """
    Verify that the print area is set to A1:G35.
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

    # Get the Report sheet (or active sheet)
    if 'Report' in wb.sheetnames:
        ws = wb['Report']
    else:
        ws = wb.active
    print(f"INFO: Checking sheet '{ws.title}', print_area raw = {repr(ws.print_area)}")

    parsed = parse_print_area(ws.print_area)

    # Component 1: Print area is defined (0.3 points)
    try:
        if ws.print_area and parsed is not None:
            print(f"PASS: Component 1 - Print area is defined: {ws.print_area} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 - Print area is not defined or unparseable: {repr(ws.print_area)}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    if parsed is None:
        # No valid print area; remaining components fail
        print(f"FAIL: Component 2 - No valid print area to check columns")
        print(f"FAIL: Component 3 - No valid print area to check rows")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    start_col, start_row, end_col, end_row = parsed
    print(f"INFO: Parsed print area -> start_col={start_col}, start_row={start_row}, end_col={end_col}, end_row={end_row}")

    # Component 2: Correct columns A-G (0.4 points)
    try:
        if start_col == 'A' and end_col == 'G':
            print(f"PASS: Component 2 - Print area columns are A to G (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 - Expected columns A:G, found {start_col}:{end_col}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Correct rows 1-35 (0.3 points)
    try:
        if start_row == 1 and end_row == 35:
            print(f"PASS: Component 3 - Print area rows are 1 to 35 (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 - Expected rows 1:35, found {start_row}:{end_row}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

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
