"""
Reward Script: Apply conditional formatting for duplicate emails
Task ID: calc_ggf_012
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): CF rule exists covering A2:A101
  Component 2 (0.3): CF rule uses COUNTIF-based duplicate detection formula
  Component 3 (0.4): CF rule applies orange background fill
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_ggf_012'


def verify_task(file_path):
    """
    Verify conditional formatting for duplicate email highlighting.
    Returns: float between 0.0 and 1.0
    """
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Contacts' sheet must exist
    if 'Contacts' not in wb.sheetnames:
        print("FAIL: 'Contacts' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Contacts']

    # Gather all conditional formatting rules
    cf_list = list(ws.conditional_formatting)

    # Component 1: CF rule exists covering the A2:A101 range (0.3 points)
    # We check that at least one CF rule covers A2:A101 (or a superset)
    try:
        target_found = False
        matching_cf = None
        matching_rule = None

        for cf in cf_list:
            # cf is a ConditionalFormatting object; str(cf) or cf.sqref gives the range
            range_str = str(cf.sqref) if hasattr(cf, 'sqref') else str(cf)
            # Check if A2:A101 is covered
            # The range might be exactly "A2:A101" or might encompass it
            # Accept common variants: A2:A101, $A$2:$A$101, A:A (whole column)
            normalized = range_str.replace('$', '').upper()
            if 'A2:A101' in normalized or 'A1:A101' in normalized or 'A:A' in normalized:
                target_found = True
                matching_cf = cf
                break

        if target_found:
            print(f"PASS: Component 1 — CF rule found covering A2:A101 (0.3 pts)")
            total_score += 0.3
        else:
            # Fallback: check if any CF rule covers at least most of A2:A101
            for cf in cf_list:
                range_str = str(cf.sqref) if hasattr(cf, 'sqref') else str(cf)
                normalized = range_str.replace('$', '').upper()
                if normalized.startswith('A') and ':' in normalized:
                    # Some CF rule on column A exists
                    target_found = True
                    matching_cf = cf
                    print(f"PASS: Component 1 — CF rule found on column A range: {range_str} (0.3 pts)")
                    total_score += 0.3
                    break

            if not target_found:
                print(f"FAIL: Component 1 — No CF rule found on A2:A101. Found {len(cf_list)} CF rules total.")
                for cf in cf_list:
                    print(f"  Existing CF range: {cf.sqref if hasattr(cf, 'sqref') else cf}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: CF rule uses a COUNTIF-based formula for duplicate detection (0.3 points)
    try:
        formula_ok = False
        if matching_cf is not None:
            for rule in matching_cf.rules:
                # Check rule type is expression or formula-based
                rule_formulas = rule.formula if hasattr(rule, 'formula') and rule.formula else []
                for f in rule_formulas:
                    f_upper = str(f).upper().replace(' ', '')
                    # The formula should use COUNTIF on the A column range and check >1
                    if 'COUNTIF' in f_upper and '>1' in f_upper:
                        formula_ok = True
                        print(f"PASS: Component 2 — COUNTIF duplicate formula found: {f} (0.3 pts)")
                        matching_rule = rule
                        break
                if formula_ok:
                    break

        if not formula_ok:
            # Also search all CF rules if matching_cf didn't have the formula
            for cf in cf_list:
                for rule in cf.rules:
                    rule_formulas = rule.formula if hasattr(rule, 'formula') and rule.formula else []
                    for f in rule_formulas:
                        f_upper = str(f).upper().replace(' ', '')
                        if 'COUNTIF' in f_upper and '>1' in f_upper:
                            formula_ok = True
                            matching_rule = rule
                            matching_cf = cf
                            print(f"PASS: Component 2 — COUNTIF duplicate formula found: {f} (0.3 pts)")
                            break
                    if formula_ok:
                        break
                if formula_ok:
                    break

        if formula_ok:
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No COUNTIF-based duplicate detection formula found")
            for cf in cf_list:
                for rule in cf.rules:
                    print(f"  Rule type={rule.type}, formula={rule.formula}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: CF rule applies an orange background fill (0.4 points)
    try:
        fill_ok = False
        rule_to_check = matching_rule

        # If no matching rule from component 2, check all rules
        rules_to_check = []
        if rule_to_check:
            rules_to_check.append(rule_to_check)
        else:
            for cf in cf_list:
                for rule in cf.rules:
                    rules_to_check.append(rule)

        for rule in rules_to_check:
            if rule.dxf and rule.dxf.fill:
                fill = rule.dxf.fill
                # Check fgColor for orange tones
                fg_rgb = None
                if fill.fgColor and fill.fgColor.rgb:
                    fg_rgb = str(fill.fgColor.rgb)
                elif fill.bgColor and fill.bgColor.rgb:
                    fg_rgb = str(fill.bgColor.rgb)

                if fg_rgb:
                    # Extract RGB components (ARGB format: AARRGGBB)
                    rgb_hex = fg_rgb[-6:]  # last 6 chars are RRGGBB
                    r = int(rgb_hex[0:2], 16)
                    g = int(rgb_hex[2:4], 16)
                    b = int(rgb_hex[4:6], 16)

                    # Orange hue check: R should be high, G moderate, B low
                    # Common orange values: FF8C00 (dark orange), FFA500 (orange),
                    # FF6600, FF9900, FFC000, etc.
                    is_orange = (r >= 200 and g >= 80 and g <= 220 and b <= 100)
                    # Also accept broader warm orange/amber tones
                    is_warm_orange = (r >= 180 and r > b and r > g and g >= 50 and b <= 120)

                    if is_orange or is_warm_orange:
                        fill_ok = True
                        print(f"PASS: Component 3 — Orange fill detected: {fg_rgb} (R={r},G={g},B={b}) (0.4 pts)")
                        break
                    else:
                        print(f"INFO: Fill color found but not orange: {fg_rgb} (R={r},G={g},B={b})")

        if fill_ok:
            total_score += 0.4
        else:
            print(f"FAIL: Component 3 — No orange background fill found on CF rule")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
