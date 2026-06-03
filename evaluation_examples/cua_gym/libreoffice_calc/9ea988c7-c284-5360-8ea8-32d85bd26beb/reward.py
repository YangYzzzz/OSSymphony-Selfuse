"""
Reward Script: Add conditional formatting rule to A2:A50 for unique values with light green fill
Task ID: calc_fmt_condfmt_unique_values_089
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5 pts): A CF rule of type 'uniqueValues' applied to range A2:A50 exists
  Component 2 (0.5 pts): The CF rule's fill color is #C6EFCE (ARGB: FFC6EFCE)
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_fmt_condfmt_unique_values_089'

EXPECTED_CF_RANGE = 'A2:A50'
EXPECTED_CF_TYPE = 'uniqueValues'
EXPECTED_FILL_COLOR = 'FFC6EFCE'  # ARGB: FF=alpha, C6=R, EF=G, CE=B


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Add a conditional formatting rule to A2:A50 to highlight only unique
    (non-duplicate) values with a light green (#C6EFCE) background.
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Verify the sheet exists
    if 'Product Registry' not in wb.sheetnames:
        print("FAIL: Sheet 'Product Registry' not found in workbook")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Product Registry']

    # Component 1: A conditional formatting rule of type 'uniqueValues' applied
    # to range A2:A50 must exist (0.5 points)
    # This FAILS on initial (no CF rules at all) and PASSES on golden.
    try:
        cf_rules_all = list(ws.conditional_formatting)
        unique_values_rule_found = False
        found_cf_range = None
        found_rule = None

        for cf in cf_rules_all:
            sqref_str = str(cf.sqref)
            for rule in cf.rules:
                if rule.type == EXPECTED_CF_TYPE:
                    # Accept if the range is A2:A50 (exact match)
                    if sqref_str == EXPECTED_CF_RANGE:
                        unique_values_rule_found = True
                        found_cf_range = sqref_str
                        found_rule = rule
                        break
            if unique_values_rule_found:
                break

        if unique_values_rule_found:
            print(f"PASS: Component 1 — uniqueValues CF rule found on range {found_cf_range} (0.5 pts)")
            total_score += 0.5
        else:
            # Check if any uniqueValues rule exists (wrong range)
            any_unique = any(
                rule.type == EXPECTED_CF_TYPE
                for cf in cf_rules_all
                for rule in cf.rules
            )
            if any_unique:
                print(f"FAIL: Component 1 — uniqueValues CF rule found but NOT on range {EXPECTED_CF_RANGE}")
            else:
                print(f"FAIL: Component 1 — No uniqueValues CF rule found on A2:A50. "
                      f"Total CF rules: {len(cf_rules_all)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        found_rule = None

    # Component 2: The CF rule's fill color must be #C6EFCE (ARGB: FFC6EFCE) (0.5 points)
    # This FAILS on initial (no CF rules exist) and PASSES on golden when color is correct.
    try:
        if found_rule is not None and unique_values_rule_found:
            color_matched = False
            actual_color = None

            if found_rule.dxf and found_rule.dxf.fill:
                fill = found_rule.dxf.fill
                try:
                    fg = fill.fgColor
                    if fg.type == 'rgb':
                        actual_color = fg.rgb
                        # Compare ignoring case; expected FFC6EFCE
                        if actual_color and actual_color.upper() == EXPECTED_FILL_COLOR.upper():
                            color_matched = True
                        else:
                            # Also accept 6-char hex without alpha prefix
                            if actual_color and actual_color.upper() in ('C6EFCE', '00C6EFCE'):
                                color_matched = True
                except Exception as inner_e:
                    print(f"  (color parse error: {inner_e})")

            if color_matched:
                print(f"PASS: Component 2 — Fill color is {actual_color} (matches #C6EFCE) (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 — Expected fill color ARGB={EXPECTED_FILL_COLOR}, "
                      f"found: {actual_color}")
        else:
            print("FAIL: Component 2 — Cannot check fill color: no uniqueValues rule found on A2:A50")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
