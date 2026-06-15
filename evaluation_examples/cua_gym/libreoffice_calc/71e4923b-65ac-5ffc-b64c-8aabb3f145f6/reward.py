"""
Reward Script: Conditional formatting with WEEKDAY formula to highlight weekends
Task ID: osworld_calc_conditional_format_weekday_003
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): A conditional formatting rule exists on the worksheet
  Component 2 (0.3): The rule uses a WEEKDAY formula targeting column A and covers all 4 columns (A-D)
  Component 3 (0.4): The rule applies a yellow background fill
  Total: 1.0
"""

import os
import re

import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'osworld_calc_conditional_format_weekday_003'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns a float between 0.0 and 1.0.

    Task: Apply conditional formatting with a WEEKDAY formula to highlight all rows
    where the attendance date (column A) is a Saturday or Sunday, using yellow background.
    Applies to columns A-D (entire row), rows 2-101 (data rows).
    """
    total_score = 0.0

    # Precondition: load the file
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Access the Attendance sheet
    try:
        if 'Attendance' in wb.sheetnames:
            ws = wb['Attendance']
        else:
            ws = wb.active
    except Exception as e:
        print(f"CRITICAL: Cannot access worksheet: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: At least one conditional formatting rule exists (0.3 points)
    # This FAILS on initial_env (no CF rules) and PASSES on golden_env (has a CF rule)
    # -----------------------------------------------------------------------
    try:
        cf_rules_found = list(ws.conditional_formatting)
        rule_count = sum(len(list(ws.conditional_formatting[cf])) for cf in cf_rules_found)

        if rule_count > 0:
            print(f"PASS: Component 1 — {rule_count} conditional formatting rule(s) found (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 — No conditional formatting rules found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: The rule uses a WEEKDAY formula targeting column A,
    #              and covers at least columns A through D (0.3 points)
    # -----------------------------------------------------------------------
    try:
        weekday_formula_found = False
        covers_abcd = False

        for cf in ws.conditional_formatting:
            # Use .sqref attribute which gives the clean range string like "A2:D101"
            try:
                cf_sqref = str(cf.sqref)
            except AttributeError:
                cf_sqref = str(cf)

            # Check the range string covers columns A through D for multiple rows
            # Accept "A2:D101" or similar: starts at A<row>, ends at D<row>
            range_covers_ad = False
            range_match = re.match(r'^A\d+:D\d+$', cf_sqref.strip())
            if range_match:
                range_covers_ad = True

            for rule in ws.conditional_formatting[cf]:
                if rule.type == 'expression' and rule.formula:
                    formula_str = rule.formula[0].upper() if rule.formula else ''
                    # Check that formula contains WEEKDAY and references column A ($A or A)
                    if 'WEEKDAY' in formula_str and ('$A' in formula_str or ',A' in formula_str or '(A' in formula_str):
                        weekday_formula_found = True
                        if range_covers_ad:
                            covers_abcd = True

        if weekday_formula_found and covers_abcd:
            print("PASS: Component 2 — WEEKDAY formula found targeting column A, covering A:D range (0.3 pts)")
            total_score += 0.3
        elif weekday_formula_found:
            print("FAIL: Component 2 — WEEKDAY formula found but range does not cover A2:D<n> (columns A through D)")
        else:
            print("FAIL: Component 2 — No conditional formatting rule with WEEKDAY formula targeting column A found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: The rule applies a yellow background fill (0.4 points)
    # Yellow is typically FFFFFF00 (ARGB), FFFF00 (RGB), or similar yellow shades.
    # -----------------------------------------------------------------------
    try:
        yellow_fill_found = False

        for cf in ws.conditional_formatting:
            for rule in ws.conditional_formatting[cf]:
                if rule.type == 'expression' and rule.formula:
                    formula_str = rule.formula[0].upper() if rule.formula else ''
                    if 'WEEKDAY' not in formula_str:
                        continue
                    # Check for yellow fill
                    if rule.dxf and rule.dxf.fill:
                        try:
                            fg_color = rule.dxf.fill.fgColor.rgb
                            # Yellow colors: FFFFFF00 (8-char ARGB), FFFF00 (6-char RGB)
                            # Allow variations of yellow: pure yellow = FF in RGB channels for R+G, 00 for B
                            # FFFFFF00 -> alpha=FF, R=FF, G=FF, B=00 (yellow)
                            # Also accept colors where high R+G and low B indicates yellow
                            if fg_color:
                                fg_upper = fg_color.upper()
                                # Primary match: FFFFFF00 (pure yellow ARGB)
                                if fg_upper == 'FFFFFF00':
                                    yellow_fill_found = True
                                # Also accept 6-char FFFF00 (though openpyxl usually returns 8-char)
                                elif fg_upper == 'FFFF00':
                                    yellow_fill_found = True
                                # Broad yellow check: ARGB where last two chars (Blue) are 00
                                # and first two hex pairs after alpha are high (RR GG close to FF)
                                elif len(fg_upper) == 8:
                                    alpha = fg_upper[0:2]
                                    red = fg_upper[2:4]
                                    green = fg_upper[4:6]
                                    blue = fg_upper[6:8]
                                    # Yellow: red high, green high, blue low
                                    r_val = int(red, 16)
                                    g_val = int(green, 16)
                                    b_val = int(blue, 16)
                                    if r_val >= 200 and g_val >= 200 and b_val <= 50:
                                        yellow_fill_found = True
                                        print(f"  Note: Yellow fill detected with color {fg_upper}")
                        except Exception as color_e:
                            print(f"  WARNING: Could not read fill color: {color_e}")
                    else:
                        print("  WARNING: WEEKDAY rule found but has no DXF fill")

        if yellow_fill_found:
            print("PASS: Component 3 — Yellow background fill (FFFFFF00) applied in WEEKDAY conditional format rule (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 3 — No yellow fill found in the WEEKDAY conditional formatting rule")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: test against canonical artifact path on the VM
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
