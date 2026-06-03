"""
Reward Script: Apply red tab color to expense group sheets
Task ID: calc_gsi_072
Domain: libreoffice_calc
Scoring: 5 components (0.2 each) — one per expense sheet that needs a red tab color applied
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_072'

# The 5 sheets that need red tab colors applied (task-introduced changes only)
# 'Expenses' already has red in initial_env — it is a precondition, not scored.
TARGET_SHEETS = ['Travel', 'Meals', 'Supplies', 'Equipment', 'Other']
POINTS_PER_SHEET = 0.2


def is_red_tab_color(ws):
    """
    Check if a worksheet has a red tab color.
    openpyxl stores tab color in ws.sheet_properties.tabColor.
    Red = FF0000 in RGB. openpyxl may store as '00FF0000' (ARGB with alpha=00)
    or 'FFFF0000' (ARGB with alpha=FF).
    We check that the RGB portion is 'FF0000'.
    """
    try:
        tab_color = ws.sheet_properties.tabColor
        if tab_color is None:
            return False
        rgb = tab_color.rgb
        if rgb is None:
            return False
        # rgb is an ARGB string like '00FF0000' or 'FFFF0000'
        # Extract last 6 chars for the RGB portion
        rgb_str = str(rgb)
        if len(rgb_str) >= 6:
            color_part = rgb_str[-6:].upper()
            return color_part == 'FF0000'
        return False
    except Exception:
        return False


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

    # Precondition gate: all target sheets must exist
    existing_sheets = wb.sheetnames
    for sheet_name in TARGET_SHEETS:
        if sheet_name not in existing_sheets:
            print(f"CRITICAL: Required sheet '{sheet_name}' not found in workbook. Sheets: {existing_sheets}")
            print("REWARD: 0.0")
            return 0.0

    # Score each target sheet for having a red tab color
    for sheet_name in TARGET_SHEETS:
        try:
            ws = wb[sheet_name]
            if is_red_tab_color(ws):
                print(f"PASS: Sheet '{sheet_name}' has red tab color ({POINTS_PER_SHEET} pts)")
                total_score += POINTS_PER_SHEET
            else:
                tab_color = ws.sheet_properties.tabColor
                color_info = tab_color.rgb if tab_color else 'None'
                print(f"FAIL: Sheet '{sheet_name}' — expected red tab color, found: {color_info}")
        except Exception as e:
            print(f"ERROR: Could not check sheet '{sheet_name}': {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
