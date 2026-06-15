"""
Reward Script: Apply conditional formatting 'above average' rule to B2:B30
Task ID: calc_fmt_condfmt_above_average_076
Domain: libreoffice_calc

Scoring Rubric:
  Component 1: A CF rule exists on range B2:B30           — 0.4 points
  Component 2: CF rule type is 'aboveAverage'             — 0.3 points
  Component 3: CF rule background fill color is #C6EFCE   — 0.2 points
  Component 4: CF rule font color is #276221              — 0.1 points
  Total: 1.0

The initial file has NO conditional formatting. All components fail on initial (0.0).
The golden file has all components satisfied (1.0).
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_fmt_condfmt_above_average_076'
SHEET_NAME = 'Score Analysis'
TARGET_RANGE = 'B2:B30'

# Expected color values in 8-char ARGB format
EXPECTED_BG_COLOR = 'FFC6EFCE'   # background #C6EFCE with full alpha
EXPECTED_FONT_COLOR_CANDIDATES = ['FF276221', '00276221']  # openpyxl may store with 00 alpha for font


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

    # Precondition: Sheet must exist
    if SHEET_NAME not in wb.sheetnames:
        print(f"CRITICAL: Sheet '{SHEET_NAME}' not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb[SHEET_NAME]
    cf_list = list(ws.conditional_formatting)

    # Component 1: A CF rule exists on range B2:B30 (0.4 points)
    # This FAILS on initial (no CF at all) and PASSES on golden (1 CF rule on B2:B30)
    try:
        found_target_range = False
        target_cf = None
        for cf in cf_list:
            cf_range_str = str(cf.sqref)
            if 'B2:B30' in cf_range_str:
                found_target_range = True
                target_cf = cf
                break

        if found_target_range and target_cf is not None:
            print(f"PASS: Component 1 — CF rule found on range B2:B30 (0.4 pts)")
            total_score += 0.4
        else:
            all_ranges = [str(cf.sqref) for cf in cf_list]
            print(f"FAIL: Component 1 — No CF rule found on B2:B30. Found ranges: {all_ranges}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        target_cf = None

    # Component 2: CF rule type is 'aboveAverage' (0.3 points)
    # This FAILS on initial (no rules), PASSES on golden (rule type = aboveAverage)
    try:
        if target_cf is not None:
            found_above_average = False
            target_rule = None
            for rule in target_cf.rules:
                if rule.type == 'aboveAverage':
                    found_above_average = True
                    target_rule = rule
                    break

            if found_above_average:
                print(f"PASS: Component 2 — CF rule type is 'aboveAverage' (0.3 pts)")
                total_score += 0.3
            else:
                rule_types = [r.type for r in target_cf.rules]
                print(f"FAIL: Component 2 — Expected 'aboveAverage' rule type, found: {rule_types}")
                target_rule = None
        else:
            print(f"FAIL: Component 2 — Skipped, no CF on B2:B30")
            target_rule = None
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")
        target_rule = None

    # Component 3: CF rule has correct background fill color #C6EFCE (0.2 points)
    # FFC6EFCE in 8-char ARGB. FAILS on initial (no rule), PASSES on golden (fill = FFC6EFCE)
    try:
        if target_rule is not None:
            dxf = getattr(target_rule, 'dxf', None)
            bg_color_found = None
            if dxf is not None:
                fill = getattr(dxf, 'fill', None)
                if fill is not None:
                    fg = getattr(fill, 'fgColor', None)
                    if fg is not None:
                        bg_color_found = fg.rgb

            if bg_color_found == EXPECTED_BG_COLOR:
                print(f"PASS: Component 3 — Background fill color is {EXPECTED_BG_COLOR} (#C6EFCE) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Expected background {EXPECTED_BG_COLOR}, found: {bg_color_found}")
        else:
            print(f"FAIL: Component 3 — Skipped, no 'aboveAverage' rule found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: CF rule has correct font color #276221 (0.1 points)
    # 276221 may be stored as 00276221 (alpha=00 for font). FAILS on initial, PASSES on golden.
    try:
        if target_rule is not None:
            dxf = getattr(target_rule, 'dxf', None)
            font_color_found = None
            if dxf is not None:
                font = getattr(dxf, 'font', None)
                if font is not None:
                    color = getattr(font, 'color', None)
                    if color is not None:
                        font_color_found = color.rgb

            if font_color_found in EXPECTED_FONT_COLOR_CANDIDATES:
                print(f"PASS: Component 4 — Font color is {font_color_found} (#276221) (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 4 — Expected font color in {EXPECTED_FONT_COLOR_CANDIDATES}, found: {font_color_found}")
        else:
            print(f"FAIL: Component 4 — Skipped, no 'aboveAverage' rule found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
