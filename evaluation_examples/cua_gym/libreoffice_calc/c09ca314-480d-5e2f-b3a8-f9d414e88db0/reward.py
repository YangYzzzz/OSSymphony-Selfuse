"""
Reward Script: Conditional formatting on Budget Variance column
Task ID: calc_gsd_019
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.25): At least 2 conditional formatting rules exist on a range covering D2:D21
  - Component 2 (0.25): "Less than 0" rule with red background (FFFF0000)
  - Component 3 (0.25): "Greater than 0" rule with green background (FF70AD47)
  - Component 4 (0.25): Both rules have white font color (FFFFFF)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gsd_019'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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


def verify_task(file_path):
    """
    Verify conditional formatting on D2:D21.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Budget vs Actual'] if 'Budget vs Actual' in wb.sheetnames else wb.active

    # Collect all conditional formatting rules that cover D2:D21
    cf_rules_on_d = []
    for cf in ws.conditional_formatting:
        range_str = str(cf)
        # Check if D2:D21 is covered (could be exact or a superset)
        # We accept ranges that include D column rows 2-21
        for rule in cf.rules:
            cf_rules_on_d.append({
                'range': range_str,
                'rule': rule
            })

    # Filter to rules that actually target the D column area
    relevant_rules = []
    for cf in ws.conditional_formatting:
        range_str = str(cf)
        # Check if range includes D column (column 4)
        # Parse the range to see if it covers D2:D21
        covers_d = False
        # ConditionalFormatting object has .cells attribute or we parse string
        cf_str = str(cf).upper()
        # Accept ranges like D2:D21, D:D, D1:D100, $D$2:$D$21, etc.
        if 'D' in cf_str:
            covers_d = True
        if covers_d:
            for rule in cf.rules:
                relevant_rules.append({
                    'range': range_str,
                    'rule': rule
                })

    print(f"INFO: Found {len(relevant_rules)} conditional formatting rule(s) covering D column")

    # Component 1: At least 2 conditional formatting rules exist (0.25 points)
    try:
        has_less_than_rule = False
        has_greater_than_rule = False
        less_than_rule = None
        greater_than_rule = None

        for item in relevant_rules:
            rule = item['rule']
            if rule.type == 'cellIs':
                if rule.operator == 'lessThan' and rule.formula and '0' in str(rule.formula):
                    has_less_than_rule = True
                    less_than_rule = rule
                elif rule.operator == 'greaterThan' and rule.formula and '0' in str(rule.formula):
                    has_greater_than_rule = True
                    greater_than_rule = rule

        if has_less_than_rule and has_greater_than_rule:
            print(f"PASS: Component 1 -- Two conditional formatting rules found (lessThan 0 and greaterThan 0) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- Expected both lessThan and greaterThan rules, found lessThan={has_less_than_rule}, greaterThan={has_greater_than_rule}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: "Less than 0" rule has red background FFFF0000 (0.25 points)
    try:
        if less_than_rule and less_than_rule.dxf and less_than_rule.dxf.fill:
            fill_color = None
            if less_than_rule.dxf.fill.fgColor and less_than_rule.dxf.fill.fgColor.rgb:
                fill_color = str(less_than_rule.dxf.fill.fgColor.rgb).upper()
            # Accept FFFF0000 (opaque red) or variations
            if fill_color and 'FF0000' in fill_color:
                print(f"PASS: Component 2 -- LessThan rule has red fill: {fill_color} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- Expected red fill (FF0000), found: {fill_color}")
        else:
            print(f"FAIL: Component 2 -- LessThan rule has no fill defined")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: "Greater than 0" rule has green background FF70AD47 (0.25 points)
    try:
        if greater_than_rule and greater_than_rule.dxf and greater_than_rule.dxf.fill:
            fill_color = None
            if greater_than_rule.dxf.fill.fgColor and greater_than_rule.dxf.fill.fgColor.rgb:
                fill_color = str(greater_than_rule.dxf.fill.fgColor.rgb).upper()
            # Accept FF70AD47 or close green variants
            # Be somewhat flexible: accept common greens
            is_green = False
            if fill_color:
                # Check for the specific green or common green variants
                if '70AD47' in fill_color:
                    is_green = True
                elif fill_color in ('FF00FF00', '0000FF00', 'FF00B050', 'FF92D050'):
                    is_green = True
                # Also accept any color where G channel is dominant
                # Parse ARGB: positions [2:4]=R, [4:6]=G, [6:8]=B
                if len(fill_color) == 8:
                    try:
                        r = int(fill_color[2:4], 16)
                        g = int(fill_color[4:6], 16)
                        b = int(fill_color[6:8], 16)
                        if g > r and g > b and g >= 100:
                            is_green = True
                    except ValueError:
                        pass

            if is_green:
                print(f"PASS: Component 3 -- GreaterThan rule has green fill: {fill_color} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Expected green fill (70AD47 or similar), found: {fill_color}")
        else:
            print(f"FAIL: Component 3 -- GreaterThan rule has no fill defined")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Both rules have white font color (0.25 points)
    try:
        white_count = 0
        for label, rule in [('lessThan', less_than_rule), ('greaterThan', greater_than_rule)]:
            if rule and rule.dxf and rule.dxf.font and rule.dxf.font.color:
                font_rgb = str(rule.dxf.font.color.rgb).upper() if rule.dxf.font.color.rgb else None
                if font_rgb and 'FFFFFF' in font_rgb:
                    white_count += 1
                    print(f"INFO: {label} rule has white font: {font_rgb}")
                else:
                    print(f"INFO: {label} rule font color: {font_rgb} (not white)")
            else:
                print(f"INFO: {label} rule has no font color defined")

        if white_count == 2:
            print(f"PASS: Component 4 -- Both rules have white font color (0.25 pts)")
            total_score += 0.25
        elif white_count == 1:
            print(f"PARTIAL: Component 4 -- Only 1 of 2 rules has white font (0.125 pts)")
            total_score += 0.125
        else:
            print(f"FAIL: Component 4 -- Neither rule has white font color")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
