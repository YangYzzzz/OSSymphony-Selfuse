"""
Reward Script: Conditional formatting on Inventory sheet stock quantities
Task ID: calc_gg2_012
Domain: libreoffice_calc
Scoring:
  Component 1 (0.15): CF rules exist on correct range D2:D201
  Component 2 (0.30): Red fill rule for value == 0
  Component 3 (0.30): Orange fill rule for value between 1 and 10
  Component 4 (0.25): Green fill rule for value > 50
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gg2_012'


def normalize_color(rgb_str):
    """Normalize a color string to uppercase 8-char ARGB."""
    if rgb_str is None:
        return None
    s = str(rgb_str).upper().strip()
    # If 6 chars, prepend FF
    if len(s) == 6:
        s = 'FF' + s
    return s


def is_red(rgb_str):
    """Check if color is red (FFFF0000 or close variants)."""
    c = normalize_color(rgb_str)
    if c is None:
        return False
    # Accept FFFF0000 (pure red)
    return c == 'FFFF0000'


def is_orange(rgb_str):
    """Check if color is orange (FFFFA500 or close variants)."""
    c = normalize_color(rgb_str)
    if c is None:
        return False
    # Accept FFFFA500 (standard orange) or FFFF8C00 (dark orange) or FFFFC000
    return c in ('FFFFA500', 'FFFF8C00', 'FFFFC000', 'FFED7D31')


def is_green(rgb_str):
    """Check if color is green (FF00FF00 or close variants)."""
    c = normalize_color(rgb_str)
    if c is None:
        return False
    # Accept FF00FF00 (lime green), FF00B050, FF92D050
    return c in ('FF00FF00', 'FF00B050', 'FF92D050', 'FF70AD47')


def verify_task(file_path):
    """
    Verify conditional formatting rules on D2:D201 in the Inventory sheet.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check that 'Inventory' sheet exists (precondition gate)
    if 'Inventory' not in wb.sheetnames:
        print("CRITICAL: 'Inventory' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Inventory']

    # Gather all conditional formatting rules
    cf_list = list(ws.conditional_formatting)

    # Component 1: CF rules exist on correct range D2:D201 (0.15 points)
    try:
        # Find CF rules that cover D2:D201
        target_range_found = False
        relevant_rules = []
        for cf in cf_list:
            range_str = str(cf).upper().replace(' ', '')
            # Check if the range covers D2:D201 (could be written as $D$2:$D$201 too)
            range_clean = range_str.replace('$', '').replace('<CONDITIONALFORMATTING', '').replace('>', '').strip()
            if 'D2:D201' in range_clean:
                target_range_found = True
                relevant_rules.extend(cf.rules)

        if target_range_found and len(relevant_rules) >= 3:
            print(f"PASS: Component 1 — CF rules found on D2:D201 with {len(relevant_rules)} rules (0.15 pts)")
            total_score += 0.15
        elif target_range_found:
            print(f"FAIL: Component 1 — CF range found but only {len(relevant_rules)} rules (need >= 3)")
        else:
            # Also check if rules are spread across multiple CF entries covering the same range
            all_rules_for_d = []
            for cf in cf_list:
                range_str = str(cf).upper().replace('$', '')
                if 'D2' in range_str and 'D201' in range_str:
                    all_rules_for_d.extend(cf.rules)
            if len(all_rules_for_d) >= 3:
                print(f"PASS: Component 1 — CF rules found covering D2:D201 across entries ({len(all_rules_for_d)} rules) (0.15 pts)")
                total_score += 0.15
                relevant_rules = all_rules_for_d
            else:
                print(f"FAIL: Component 1 — No CF rules found on range D2:D201")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        relevant_rules = []

    # If no relevant rules found at all, gather all rules for further checks
    if not relevant_rules:
        for cf in cf_list:
            relevant_rules.extend(cf.rules)

    # Component 2: Red fill rule for cells equal to 0 (0.30 points)
    try:
        red_rule_found = False
        for rule in relevant_rules:
            if rule.type == 'cellIs' and rule.operator == 'equal':
                formulas = [str(f).strip() for f in (rule.formula or [])]
                if '0' in formulas:
                    # Check fill color is red
                    if rule.dxf and rule.dxf.fill and rule.dxf.fill.fgColor:
                        color = rule.dxf.fill.fgColor.rgb
                        if is_red(color):
                            red_rule_found = True
                            print(f"PASS: Component 2 — Red fill rule for value==0 found (color={color}) (0.30 pts)")
                            total_score += 0.30
                        else:
                            print(f"FAIL: Component 2 — Rule for ==0 found but fill color is {color}, not red")
                    else:
                        print(f"FAIL: Component 2 — Rule for ==0 found but no fill color defined")
        if not red_rule_found and total_score < 0.30:
            print(f"FAIL: Component 2 — No cellIs/equal/0 rule with red fill found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Orange fill rule for cells between 1 and 10 (0.30 points)
    try:
        orange_rule_found = False
        for rule in relevant_rules:
            if rule.type == 'cellIs' and rule.operator == 'between':
                formulas = [str(f).strip() for f in (rule.formula or [])]
                if len(formulas) >= 2 and formulas[0] == '1' and formulas[1] == '10':
                    if rule.dxf and rule.dxf.fill and rule.dxf.fill.fgColor:
                        color = rule.dxf.fill.fgColor.rgb
                        if is_orange(color):
                            orange_rule_found = True
                            print(f"PASS: Component 3 — Orange fill rule for between 1 and 10 found (color={color}) (0.30 pts)")
                            total_score += 0.30
                        else:
                            print(f"FAIL: Component 3 — Rule for between 1-10 found but fill color is {color}, not orange")
                    else:
                        print(f"FAIL: Component 3 — Rule for between 1-10 found but no fill color defined")
        if not orange_rule_found and total_score < 0.60:
            print(f"FAIL: Component 3 — No cellIs/between/1,10 rule with orange fill found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Green fill rule for cells greater than 50 (0.25 points)
    try:
        green_rule_found = False
        for rule in relevant_rules:
            if rule.type == 'cellIs' and rule.operator == 'greaterThan':
                formulas = [str(f).strip() for f in (rule.formula or [])]
                if '50' in formulas:
                    if rule.dxf and rule.dxf.fill and rule.dxf.fill.fgColor:
                        color = rule.dxf.fill.fgColor.rgb
                        if is_green(color):
                            green_rule_found = True
                            print(f"PASS: Component 4 — Green fill rule for value>50 found (color={color}) (0.25 pts)")
                            total_score += 0.25
                        else:
                            print(f"FAIL: Component 4 — Rule for >50 found but fill color is {color}, not green")
                    else:
                        print(f"FAIL: Component 4 — Rule for >50 found but no fill color defined")
        if not green_rule_found and total_score < 0.85:
            print(f"FAIL: Component 4 — No cellIs/greaterThan/50 rule with green fill found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
