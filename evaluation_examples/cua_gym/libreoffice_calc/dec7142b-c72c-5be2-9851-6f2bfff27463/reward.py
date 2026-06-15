"""
Reward Script: Update print area from A1:D20 to A1:F35
Task ID: calc_tbl_046
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): Print area includes all columns up to F
  Component 2 (0.4): Print area includes all rows up to 35
  Component 3 (0.2): Print area is exactly A1:F35 (precise match)
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_tbl_046'


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
    Parse openpyxl print_area string into components.
    Format examples:
      "'Inventory'!$A$1:$D$20"
      "Inventory!$A$1:$F$35"
      "$A$1:$F$35"
    Returns (start_col, start_row, end_col, end_row) as strings, e.g. ('A', '1', 'F', '35')
    or None if cannot parse.
    """
    # Remove sheet name prefix if present
    if '!' in print_area_str:
        print_area_str = print_area_str.split('!')[-1]
    # Remove $ signs
    clean = print_area_str.replace('$', '')
    # Match pattern like A1:F35
    m = re.match(r'^([A-Z]+)(\d+):([A-Z]+)(\d+)$', clean)
    if m:
        return m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
    return None


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

    ws = wb.active

    # Get print area
    print_area = ws.print_area
    print(f"INFO: Raw print_area = {print_area!r}")

    if not print_area:
        print("FAIL: No print area defined at all")
        print("REWARD: 0.0")
        return 0.0

    # print_area can be a string or a list; normalize
    if isinstance(print_area, list):
        pa_str = print_area[0] if print_area else ''
    else:
        pa_str = str(print_area)

    parsed = parse_print_area(pa_str)
    if parsed is None:
        print(f"FAIL: Could not parse print area: {pa_str}")
        print("REWARD: 0.0")
        return 0.0

    start_col, start_row, end_col, end_row = parsed
    print(f"INFO: Parsed print area: {start_col}{start_row}:{end_col}{end_row}")

    # Component 1: Print area covers all columns up to F (0.4 points)
    # The task requires columns A-F. end_col must be at least 'F'.
    try:
        # Convert column letter to number for comparison
        end_col_num = openpyxl.utils.column_index_from_string(end_col)
        target_col_num = openpyxl.utils.column_index_from_string('F')  # 6

        if end_col_num >= target_col_num:
            print(f"PASS: Component 1 — Print area end column is {end_col} (col {end_col_num}), covers all data columns (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Print area end column is {end_col} (col {end_col_num}), expected at least F (col {target_col_num})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Print area covers all rows up to 35 (0.4 points)
    # The task requires rows 1-35. end_row must be at least 35.
    try:
        if end_row >= 35:
            print(f"PASS: Component 2 — Print area end row is {end_row}, covers all data rows (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Print area end row is {end_row}, expected at least 35")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Print area is exactly A1:F35 (0.2 points)
    # Exact match: start at A1, end at F35
    try:
        if start_col == 'A' and start_row == 1 and end_col == 'F' and end_row == 35:
            print(f"PASS: Component 3 — Print area is exactly A1:F35 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Print area is {start_col}{start_row}:{end_col}{end_row}, expected exactly A1:F35")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI state before verifying
persist_app_state("libreoffice_calc")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
