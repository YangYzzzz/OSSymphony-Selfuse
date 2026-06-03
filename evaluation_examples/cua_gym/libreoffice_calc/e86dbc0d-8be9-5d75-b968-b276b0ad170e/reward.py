"""
Reward Script: Conditional formatting with three-tier color coding on Sales sheet
Task ID: calc_gg2_001
Domain: libreoffice_calc
Scoring:
  Component 1 (0.20): CF rules exist on a range covering A2:F51
  Component 2 (0.30): Red rule for $F2<0.10
  Component 3 (0.25): Yellow rule for AND($F2>=0.10,$F2<=0.20)
  Component 4 (0.25): Green rule for $F2>0.20
"""

import os
import re
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gg2_001'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_calc")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def normalize_formula(f):
    """Normalize a formula string for comparison: uppercase, strip spaces."""
    if not f:
        return ""
    return f.upper().replace(" ", "")


def is_red_color(rgb):
    """Check if color is red-ish (high R, low G, low B)."""
    if not rgb or len(rgb) < 6:
        return False
    # Take last 6 chars (RGB portion of ARGB)
    rgb6 = rgb[-6:]
    r, g, b = int(rgb6[0:2], 16), int(rgb6[2:4], 16), int(rgb6[4:6], 16)
    return r >= 180 and g < 100 and b < 100


def is_yellow_color(rgb):
    """Check if color is yellow-ish (high R, high G, low B)."""
    if not rgb or len(rgb) < 6:
        return False
    rgb6 = rgb[-6:]
    r, g, b = int(rgb6[0:2], 16), int(rgb6[2:4], 16), int(rgb6[4:6], 16)
    return r >= 180 and g >= 180 and b < 100


def is_green_color(rgb):
    """Check if color is green-ish (low R, high G, low B)."""
    if not rgb or len(rgb) < 6:
        return False
    rgb6 = rgb[-6:]
    r, g, b = int(rgb6[0:2], 16), int(rgb6[2:4], 16), int(rgb6[4:6], 16)
    return r < 100 and g >= 128 and b < 100


def ranges_cover_target(cf_range_str, target_min_row=2, target_max_row=51, target_min_col=1, target_max_col=6):
    """
    Check if a conditional formatting range string covers the target area A2:F51.
    Accepts ranges like 'A2:F51', 'A2:G51' (superset OK), etc.
    """
    from openpyxl.utils import range_boundaries
    try:
        min_col, min_row, max_col, max_row = range_boundaries(str(cf_range_str))
        # The CF range must cover at least A2:F51
        if (min_col <= target_min_col and max_col >= target_max_col and
                min_row <= target_min_row and max_row >= target_max_row):
            return True
    except Exception:
        pass
    return False


def verify_task(file_path):
    """
    Verify conditional formatting task completion with progressive scoring.
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

    # Check 'Sales' sheet exists
    if 'Sales' not in wb.sheetnames:
        print("FAIL: 'Sales' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Sales']

    # Collect all CF rules that apply to the target range A2:F51
    target_rules = []
    has_target_range = False

    for cf in ws.conditional_formatting:
        # Use cf.sqref (MultiCellRange) for range checking, not str(cf)
        sqref_str = str(cf.sqref)
        if ranges_cover_target(sqref_str):
            has_target_range = True
            for rule in cf.rules:
                target_rules.append(rule)

    # Component 1: CF rules exist on range covering A2:F51 (0.20 points)
    try:
        if has_target_range and len(target_rules) >= 3:
            print(f"PASS: Component 1 - Found {len(target_rules)} CF rules covering A2:F51 (0.20 pts)")
            total_score += 0.20
        elif has_target_range and len(target_rules) > 0:
            print(f"PARTIAL: Component 1 - Found {len(target_rules)} CF rules (expected 3) covering A2:F51 (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 - No CF rules found covering A2:F51 (found {len(target_rules)} rules, has_target_range={has_target_range})")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Classify rules by their formula and fill color
    red_rule_found = False
    yellow_rule_found = False
    green_rule_found = False

    for rule in target_rules:
        if rule.type != 'expression':
            continue

        formulas = rule.formula if rule.formula else []
        if not formulas:
            continue

        norm_f = normalize_formula(formulas[0])
        fill_rgb = None
        if rule.dxf and rule.dxf.fill and rule.dxf.fill.fgColor:
            try:
                fill_rgb = rule.dxf.fill.fgColor.rgb
            except Exception:
                pass

        print(f"  DEBUG: Rule formula='{formulas[0]}' normalized='{norm_f}' fill_rgb={fill_rgb}")

        # Check for red rule: $F2<0.10 or $F2<0.1
        red_formulas = ['$F2<0.10', '$F2<0.1', '$F2<10%']
        if any(normalize_formula(rf) == norm_f for rf in red_formulas):
            if fill_rgb and is_red_color(fill_rgb):
                red_rule_found = True
                print(f"  -> Matched RED rule")
            else:
                print(f"  -> Formula matches red but fill color {fill_rgb} is not red")

        # Check for yellow rule: AND($F2>=0.10,$F2<=0.20)
        yellow_formulas = [
            'AND($F2>=0.10,$F2<=0.20)', 'AND($F2>=0.1,$F2<=0.2)',
            'AND($F2>=0.10,$F2<=0.2)', 'AND($F2>=0.1,$F2<=0.20)',
            'AND($F2>=10%,$F2<=20%)',
        ]
        if any(normalize_formula(yf) == norm_f for yf in yellow_formulas):
            if fill_rgb and is_yellow_color(fill_rgb):
                yellow_rule_found = True
                print(f"  -> Matched YELLOW rule")
            else:
                print(f"  -> Formula matches yellow but fill color {fill_rgb} is not yellow")

        # Check for green rule: $F2>0.20 or $F2>0.2
        green_formulas = ['$F2>0.20', '$F2>0.2', '$F2>20%']
        if any(normalize_formula(gf) == norm_f for gf in green_formulas):
            if fill_rgb and is_green_color(fill_rgb):
                green_rule_found = True
                print(f"  -> Matched GREEN rule")
            else:
                print(f"  -> Formula matches green but fill color {fill_rgb} is not green")

    # Component 2: Red rule for low margins (0.30 points)
    try:
        if red_rule_found:
            print(f"PASS: Component 2 - Red rule ($F2<0.10) with red fill found (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 - Red rule ($F2<0.10 with red fill) not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Yellow rule for mid-range margins (0.25 points)
    try:
        if yellow_rule_found:
            print(f"PASS: Component 3 - Yellow rule (AND($F2>=0.10,$F2<=0.20)) with yellow fill found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - Yellow rule (AND($F2>=0.10,$F2<=0.20) with yellow fill) not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Green rule for high margins (0.25 points)
    try:
        if green_rule_found:
            print(f"PASS: Component 4 - Green rule ($F2>0.20) with green fill found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 - Green rule ($F2>0.20 with green fill) not found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
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
