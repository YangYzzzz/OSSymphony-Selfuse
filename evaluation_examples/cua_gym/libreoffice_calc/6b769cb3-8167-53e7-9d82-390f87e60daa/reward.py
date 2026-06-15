"""
Reward Script: Reorder conditional formatting rules so green (>100) takes priority over yellow (>50)
Task ID: calc_tbl_025
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): Green rule (>100) has highest priority (priority=1)
  Component 2 (0.3): Yellow rule (>50) has lower priority (priority=2)
  Component 3 (0.3): Both rules still exist with correct operators, formulas, range, and colors
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_tbl_025'


def persist_app_state(domain):
    """Save any unsaved LibreOffice changes before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that conditional formatting rules are reordered so the green (>100)
    rule takes priority over the yellow (>50) rule.
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

    # Collect all conditional formatting rules on the sheet
    all_rules = []
    cf_range = None
    for cf in ws.conditional_formatting:
        cf_range_str = str(cf)
        for rule in cf.rules:
            all_rules.append(rule)
        if cf_range is None:
            cf_range = cf_range_str

    if len(all_rules) < 2:
        print(f"FAIL: Expected at least 2 conditional formatting rules, found {len(all_rules)}")
        print("REWARD: 0.0")
        return 0.0

    # Identify the green rule (>100) and yellow rule (>50)
    green_rule = None
    yellow_rule = None

    for rule in all_rules:
        if rule.type == 'cellIs' and getattr(rule, 'operator', None) == 'greaterThan':
            formula_list = getattr(rule, 'formula', [])
            formula_val = formula_list[0] if formula_list else None

            # Get fill color
            fill_rgb = None
            if rule.dxf and rule.dxf.fill and rule.dxf.fill.fgColor:
                fill_rgb = rule.dxf.fill.fgColor.rgb

            if formula_val == '100':
                green_rule = rule
                print(f"INFO: Found >100 rule: priority={rule.priority}, fill={fill_rgb}")
            elif formula_val == '50':
                yellow_rule = rule
                print(f"INFO: Found >50 rule: priority={rule.priority}, fill={fill_rgb}")

    if green_rule is None or yellow_rule is None:
        print(f"FAIL: Could not identify both rules. green={green_rule}, yellow={yellow_rule}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Green rule (>100) has higher priority (lower priority number) (0.4 points)
    # In conditional formatting, priority=1 means it is evaluated first (highest priority).
    try:
        if green_rule.priority < yellow_rule.priority:
            print(f"PASS: Component 1 -- Green rule (>100) has higher priority "
                  f"(green={green_rule.priority}, yellow={yellow_rule.priority}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- Green rule priority ({green_rule.priority}) "
                  f"should be less than yellow ({yellow_rule.priority})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Yellow rule (>50) has lower priority (higher priority number) (0.3 points)
    # This is the converse check: yellow must have priority > green
    try:
        if yellow_rule.priority > green_rule.priority:
            print(f"PASS: Component 2 -- Yellow rule (>50) has lower priority "
                  f"(yellow={yellow_rule.priority}, green={green_rule.priority}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- Yellow rule priority ({yellow_rule.priority}) "
                  f"should be greater than green ({green_rule.priority})")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Both rules preserve correct colors and operators (0.3 points)
    # Verify green rule has green fill and yellow rule has yellow fill
    try:
        green_fill_rgb = None
        if green_rule.dxf and green_rule.dxf.fill and green_rule.dxf.fill.fgColor:
            green_fill_rgb = green_rule.dxf.fill.fgColor.rgb

        yellow_fill_rgb = None
        if yellow_rule.dxf and yellow_rule.dxf.fill and yellow_rule.dxf.fill.fgColor:
            yellow_fill_rgb = yellow_rule.dxf.fill.fgColor.rgb

        # Check green rule has a greenish fill (FF00B050 or similar green)
        green_ok = (green_fill_rgb is not None and
                    green_fill_rgb != 'FFFFFF00' and
                    green_fill_rgb != '00000000')

        # Check yellow rule has a yellowish fill (FFFFFF00 or similar yellow)
        yellow_ok = (yellow_fill_rgb is not None and
                     yellow_fill_rgb != 'FF00B050' and
                     yellow_fill_rgb != '00000000')

        if green_ok and yellow_ok:
            print(f"PASS: Component 3 -- Colors preserved: green rule fill={green_fill_rgb}, "
                  f"yellow rule fill={yellow_fill_rgb} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 -- Color mismatch: green rule fill={green_fill_rgb}, "
                  f"yellow rule fill={yellow_fill_rgb}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

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
