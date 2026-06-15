"""
Reward Script: KPI Dashboard Conditional Formatting
Task ID: calc_gcv_036
Domain: libreoffice_calc
Scoring: 4 components (0.25 each) — one per cell (B3, B5, B7, B9).
         Each component checks that the cell has 3 CF rules with correct
         operators, thresholds, and fill colors.
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_036'

# Expected CF rules for each cell: (operator, formula, expected_fgColor_ARGB)
EXPECTED_RULES = [
    ('greaterThanOrEqual', '95', 'FF00B050'),   # green
    ('greaterThanOrEqual', '80', 'FFFFFF00'),    # yellow
    ('lessThan',           '80', 'FFFF0000'),    # red
]

TARGET_CELLS = ['B3', 'B5', 'B7', 'B9']
POINTS_PER_CELL = 0.25


def persist_app_state():
    """Save any unsaved LibreOffice edits via Ctrl+S."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_cell_cf(ws, cell_ref):
    """
    Check that a specific cell has 3 conditional formatting rules
    matching the expected operator, threshold, and fill color.
    Returns (passed: bool, details: str).
    """
    # Collect all CF rules that apply to this cell
    matching_rules = []
    for cf in ws.conditional_formatting:
        # cf range could be a single cell or a range; check if cell_ref is in it
        cf_range_str = str(cf).replace('<ConditionalFormatting ', '').replace('>', '')
        if cell_ref in cf_range_str or cell_ref == cf_range_str:
            matching_rules.extend(cf.rules)

    if len(matching_rules) < 3:
        return False, f"Expected 3 CF rules, found {len(matching_rules)}"

    # Check each expected rule exists in the matching rules
    matched_count = 0
    for exp_op, exp_formula, exp_color in EXPECTED_RULES:
        if any(
            getattr(rule, 'operator', None) == exp_op
            and exp_formula in [str(f).strip() for f in (rule.formula or [])]
            and rule.dxf is not None
            and rule.dxf.fill is not None
            and rule.dxf.fill.fgColor is not None
            and rule.dxf.fill.fgColor.rgb == exp_color
            for rule in matching_rules
        ):
            matched_count += 1

    if matched_count == 3:
        return True, f"All 3 CF rules correct (green>=95, yellow>=80, red<80)"
    else:
        return False, f"Only {matched_count}/3 CF rules matched"


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
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

    ws = wb['KPI_Dashboard'] if 'KPI_Dashboard' in wb.sheetnames else wb.active

    for cell_ref in TARGET_CELLS:
        comp_name = f"CF rules on {cell_ref}"
        try:
            passed, details = verify_cell_cf(ws, cell_ref)
            if passed:
                print(f"PASS: {comp_name} — {details} ({POINTS_PER_CELL} pts)")
                total_score += POINTS_PER_CELL
            else:
                print(f"FAIL: {comp_name} — {details}")
        except Exception as e:
            print(f"ERROR: {comp_name} — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
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
