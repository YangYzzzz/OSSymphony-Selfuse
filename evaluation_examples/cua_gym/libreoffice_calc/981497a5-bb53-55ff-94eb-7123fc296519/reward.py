"""
Reward Script: Conditional formatting with competing rules on D2:D25
Task ID: calc_gcv_030
Domain: libreoffice_calc
Scoring:
  Component 1 (0.20): Two conditional formatting rules exist on range D2:D25
  Component 2 (0.25): CellIs rule: values > 1000 with green background #00B050
  Component 3 (0.30): Formula rule: =$E2="Refunded" with gray background #C0C0C0 and strikethrough
  Component 4 (0.25): Priority ordering: Refunded rule has higher priority than >1000 rule
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_030'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            import time
            time.sleep(0.8)
            print("PERSIST: ctrl+s sent for libreoffice_calc")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


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

    ws = wb.active

    # Collect all conditional formatting rules that apply to D2:D25
    cf_rules_on_target = []
    for cf in ws.conditional_formatting:
        range_str = str(cf).upper()
        # Check if this CF block covers D2:D25
        if 'D2:D25' in range_str or 'D2' in range_str:
            for rule in cf.rules:
                cf_rules_on_target.append(rule)

    print(f"INFO: Found {len(cf_rules_on_target)} conditional formatting rule(s) on D2:D25 range")

    # Identify the two expected rules
    cellis_rule = None
    formula_rule = None

    for rule in cf_rules_on_target:
        if rule.type == 'cellIs' and rule.operator == 'greaterThan':
            # Check if formula references 1000
            if rule.formula and any('1000' in str(f) for f in rule.formula):
                cellis_rule = rule
        elif rule.type == 'expression':
            # Check if formula references Refunded
            if rule.formula and any('Refunded' in str(f) for f in rule.formula):
                formula_rule = rule

    # Component 1: Two CF rules exist on D2:D25 (0.20 points)
    try:
        if len(cf_rules_on_target) >= 2 and cellis_rule is not None and formula_rule is not None:
            print(f"PASS: Component 1 — Two CF rules found on D2:D25 (cellIs + expression) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected 2 rules (cellIs + expression), found {len(cf_rules_on_target)} total, cellIs={'found' if cellis_rule else 'missing'}, formula={'found' if formula_rule else 'missing'}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: CellIs rule: values > 1000 with green background #00B050 (0.25 points)
    try:
        if cellis_rule is not None:
            has_green_fill = False
            if cellis_rule.dxf and cellis_rule.dxf.fill:
                fg_rgb = None
                if cellis_rule.dxf.fill.fgColor and cellis_rule.dxf.fill.fgColor.rgb:
                    fg_rgb = str(cellis_rule.dxf.fill.fgColor.rgb).upper()
                bg_rgb = None
                if cellis_rule.dxf.fill.bgColor and cellis_rule.dxf.fill.bgColor.rgb:
                    bg_rgb = str(cellis_rule.dxf.fill.bgColor.rgb).upper()
                # Check for #00B050 in either fg or bg (ARGB format: FF00B050)
                target_color = '00B050'
                if (fg_rgb and target_color in fg_rgb) or (bg_rgb and target_color in bg_rgb):
                    has_green_fill = True
                print(f"  DEBUG: cellIs rule fill fgColor={fg_rgb}, bgColor={bg_rgb}")

            if has_green_fill:
                print(f"PASS: Component 2 — CellIs > 1000 with green #00B050 fill (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — CellIs rule found but green fill #00B050 not detected")
        else:
            print(f"FAIL: Component 2 — No cellIs > 1000 rule found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Formula rule: =$E2="Refunded" with gray #C0C0C0 and strikethrough (0.30 points)
    try:
        if formula_rule is not None:
            has_gray_fill = False
            has_strikethrough = False

            # Check gray fill
            if formula_rule.dxf and formula_rule.dxf.fill:
                fg_rgb = None
                if formula_rule.dxf.fill.fgColor and formula_rule.dxf.fill.fgColor.rgb:
                    fg_rgb = str(formula_rule.dxf.fill.fgColor.rgb).upper()
                bg_rgb = None
                if formula_rule.dxf.fill.bgColor and formula_rule.dxf.fill.bgColor.rgb:
                    bg_rgb = str(formula_rule.dxf.fill.bgColor.rgb).upper()
                target_color = 'C0C0C0'
                if (fg_rgb and target_color in fg_rgb) or (bg_rgb and target_color in bg_rgb):
                    has_gray_fill = True
                print(f"  DEBUG: formula rule fill fgColor={fg_rgb}, bgColor={bg_rgb}")

            # Check strikethrough
            if formula_rule.dxf and formula_rule.dxf.font:
                if formula_rule.dxf.font.strike or formula_rule.dxf.font.strikethrough:
                    has_strikethrough = True
                print(f"  DEBUG: formula rule font strike={formula_rule.dxf.font.strike}, strikethrough={formula_rule.dxf.font.strikethrough}")

            sub_score = 0.0
            if has_gray_fill:
                sub_score += 0.15
                print(f"  PASS: Gray fill #C0C0C0 detected")
            else:
                print(f"  FAIL: Gray fill #C0C0C0 not detected")

            if has_strikethrough:
                sub_score += 0.15
                print(f"  PASS: Strikethrough detected")
            else:
                print(f"  FAIL: Strikethrough not detected")

            if sub_score > 0:
                print(f"PASS: Component 3 — Formula rule for Refunded ({sub_score} of 0.30 pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 3 — Formula rule found but neither gray fill nor strikethrough detected")
        else:
            print(f"FAIL: Component 3 — No formula rule referencing 'Refunded' found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Priority ordering — Refunded rule has higher priority (lower number) (0.25 points)
    try:
        if cellis_rule is not None and formula_rule is not None:
            cellis_priority = cellis_rule.priority
            formula_priority = formula_rule.priority
            print(f"  DEBUG: formula rule priority={formula_priority}, cellIs rule priority={cellis_priority}")

            # Lower priority number = higher priority in CF
            if formula_priority < cellis_priority:
                print(f"PASS: Component 4 — Refunded rule (priority {formula_priority}) has higher priority than >1000 rule (priority {cellis_priority}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — Refunded rule priority ({formula_priority}) should be < cellIs priority ({cellis_priority})")
        else:
            print(f"FAIL: Component 4 — Cannot check priority, missing one or both rules")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
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
