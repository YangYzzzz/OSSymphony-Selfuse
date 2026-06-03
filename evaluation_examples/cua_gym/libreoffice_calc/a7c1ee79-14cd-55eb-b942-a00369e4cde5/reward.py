"""
Reward Script: Add conditional formatting to highlight weekend dates in orange
Task ID: osworld_calc_conditional_format_weekday_002
Domain: libreoffice_calc
Scoring:
  Component 1: Conditional formatting rule exists in column B (0.5 pts)
  Component 2: CF formula uses WEEKDAY to identify Saturday/Sunday (0.3 pts)
  Component 3: CF fill color is orange (0.2 pts)
  Total: 1.0
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'osworld_calc_conditional_format_weekday_002'


def verify_task(file_path):
    """
    Verify that conditional formatting was correctly applied to column B
    to highlight weekend dates using the WEEKDAY function with an orange fill.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: load workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        ws = wb.active
    except Exception as e:
        print(f"CRITICAL: Cannot access active sheet: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Conditional formatting rule exists on column B (0.5 points)
    # The task requires adding CF to the Date column (column B).
    # This is the primary task-introduced change (initial_env has no CF on col B).
    try:
        cf_rules_in_col_b = []
        for cf_range in ws.conditional_formatting:
            range_str = str(cf_range)
            # Check if the range covers column B cells (B2 through BN)
            # Acceptable ranges: "B2:B16", "B:B", "B2:B100", etc.
            if re.match(r'^B\d+:B\d+$', range_str) or re.match(r'^B:B$', range_str) or 'B' in range_str:
                # Verify it actually starts/applies to column B
                # Parse the range to confirm it includes column B
                col_b_match = re.search(r'B(\d+):B(\d+)', range_str)
                if col_b_match or range_str.startswith('B'):
                    rules = ws.conditional_formatting[cf_range]
                    if rules:
                        cf_rules_in_col_b.extend(rules)

        if cf_rules_in_col_b:
            print(f"PASS: Component 1 — Conditional formatting rule(s) found in column B ({len(cf_rules_in_col_b)} rule(s)) (0.5 pts)")
            total_score += 0.5
        else:
            print("FAIL: Component 1 — No conditional formatting rules found in column B")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check CF rules: {e}")

    # Component 2: CF formula uses WEEKDAY function to check for Saturday/Sunday (0.3 points)
    # The formula should use WEEKDAY() and check for weekend values (6 and/or 7 for Sat/Sun).
    # Acceptable formulas include: WEEKDAY(B2,2)=6, WEEKDAY(B2,2)=7, OR(...=6,...=7),
    # or similar patterns using different WEEKDAY modes (e.g., mode 1: 1=Sun,7=Sat; mode 2: 6=Sat,7=Sun).
    try:
        formula_ok = False
        formula_found = None
        for cf_range in ws.conditional_formatting:
            range_str = str(cf_range)
            if 'B' in range_str:
                rules = ws.conditional_formatting[cf_range]
                for rule in rules:
                    formula_list = getattr(rule, 'formula', None)
                    if formula_list:
                        for formula in formula_list:
                            formula_upper = formula.upper()
                            formula_found = formula
                            # Must use WEEKDAY function AND reference weekend days
                            # WEEKDAY mode 2: 6=Saturday, 7=Sunday
                            # WEEKDAY mode 1 (default): 1=Sunday, 7=Saturday
                            # WEEKDAY mode 3: 5=Saturday, 6=Sunday
                            # We check: uses WEEKDAY() and checks for at least two distinct values
                            # that correspond to Saturday and Sunday in any mode, OR uses OR(...) / AND(...)
                            has_weekday = 'WEEKDAY' in formula_upper
                            # Check it references at least two day-values or has OR with weekday
                            has_weekend_check = (
                                re.search(r'WEEKDAY.*[=<>].*\d', formula_upper) is not None
                                and (
                                    'OR(' in formula_upper
                                    or re.search(r'WEEKDAY.*=6.*WEEKDAY.*=7', formula_upper) is not None
                                    or re.search(r'WEEKDAY.*=1.*WEEKDAY.*=7', formula_upper) is not None
                                    or re.search(r'WEEKDAY.*=7', formula_upper) is not None  # Saturday in mode 1
                                    or re.search(r'WEEKDAY.*=6', formula_upper) is not None  # Saturday in mode 2
                                )
                            )
                            if has_weekday and has_weekend_check:
                                formula_ok = True
                                break
                    if formula_ok:
                        break
            if formula_ok:
                break

        if formula_ok:
            print(f"PASS: Component 2 — CF formula uses WEEKDAY to identify weekend days: '{formula_found}' (0.3 pts)")
            total_score += 0.3
        else:
            if formula_found:
                print(f"FAIL: Component 2 — CF formula found but doesn't properly use WEEKDAY for weekends: '{formula_found}'")
            else:
                print("FAIL: Component 2 — No formula-based CF rule found in column B")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check CF formula: {e}")

    # Component 3: CF fill color is orange (0.2 points)
    # The task specifically says "highlight in orange".
    # Orange ARGB: FFFF6600 is a standard orange. Accept any orange-ish color.
    try:
        orange_fill_found = False
        fill_color_found = None
        for cf_range in ws.conditional_formatting:
            range_str = str(cf_range)
            if 'B' in range_str:
                rules = ws.conditional_formatting[cf_range]
                for rule in rules:
                    try:
                        dxf = rule.dxf
                        if dxf and dxf.fill:
                            fgColor = dxf.fill.fgColor
                            color_rgb = fgColor.rgb
                            fill_color_found = color_rgb
                            # Check for orange: FFFF6600 (standard orange)
                            # Also accept nearby oranges: high red, medium-high green, low blue
                            # Typical orange range in ARGB: FF=alpha, FF=R, 66~CC=G, 00~33=B
                            if color_rgb:
                                color_upper = color_rgb.upper()
                                # Remove alpha (first 2 chars)
                                rgb_only = color_upper[2:] if len(color_upper) == 8 else color_upper
                                if len(rgb_only) == 6:
                                    r_val = int(rgb_only[0:2], 16)
                                    g_val = int(rgb_only[2:4], 16)
                                    b_val = int(rgb_only[4:6], 16)
                                    # Orange: high red (>180), medium green (50-220), low blue (<80)
                                    if r_val > 180 and 50 <= g_val <= 220 and b_val < 80:
                                        orange_fill_found = True
                    except Exception as inner_e:
                        # If dxf or fill doesn't have color info, skip
                        pass
                    if orange_fill_found:
                        break
            if orange_fill_found:
                break

        if orange_fill_found:
            print(f"PASS: Component 3 — CF fill color is orange: '{fill_color_found}' (0.2 pts)")
            total_score += 0.2
        else:
            if fill_color_found:
                print(f"FAIL: Component 3 — CF fill color is not orange: found '{fill_color_found}', expected orange (e.g., FFFF6600)")
            else:
                print("FAIL: Component 3 — No CF fill color found in column B rules")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not check CF fill color: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
