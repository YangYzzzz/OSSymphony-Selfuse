"""
Reward Script: Verify conditional formatting for time-off request calendar
Task ID: calc_hr_064
Domain: libreoffice_calc
Scoring:
  Component 1 (0.35): CF rule for 'A' with green fill on B2:AF5
  Component 2 (0.35): CF rule for 'P' with yellow fill on B2:AF5
  Component 3 (0.30): CF rule for 'D' with red fill on B2:AF5
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_hr_064'


def _is_green(rgb):
    """Check if color is green (allowing common green variants)."""
    if rgb is None:
        return False
    rgb = str(rgb).upper()
    # Accept pure green FF00FF00, or common greens like FF00B050, FF92D050
    green_variants = ['FF00FF00', '0000FF00', 'FF00B050', 'FF92D050', 'FF00B800']
    if rgb in green_variants:
        return True
    # General heuristic: G channel high, R and B channels low
    if len(rgb) == 8:
        try:
            r = int(rgb[2:4], 16)
            g = int(rgb[4:6], 16)
            b = int(rgb[6:8], 16)
            if g > 128 and g > r and g > b:
                return True
        except ValueError:
            pass
    return False


def _is_yellow(rgb):
    """Check if color is yellow (allowing common yellow variants)."""
    if rgb is None:
        return False
    rgb = str(rgb).upper()
    yellow_variants = ['FFFFFF00', '00FFFF00', 'FFFFC000', 'FFFFEB9C']
    if rgb in yellow_variants:
        return True
    if len(rgb) == 8:
        try:
            r = int(rgb[2:4], 16)
            g = int(rgb[4:6], 16)
            b = int(rgb[6:8], 16)
            if r > 180 and g > 180 and b < 100:
                return True
        except ValueError:
            pass
    return False


def _is_red(rgb):
    """Check if color is red (allowing common red variants)."""
    if rgb is None:
        return False
    rgb = str(rgb).upper()
    red_variants = ['FFFF0000', '00FF0000', 'FFFF4444', 'FFCC0000']
    if rgb in red_variants:
        return True
    if len(rgb) == 8:
        try:
            r = int(rgb[2:4], 16)
            g = int(rgb[4:6], 16)
            b = int(rgb[6:8], 16)
            if r > 160 and r > g * 2 and r > b * 2:
                return True
        except ValueError:
            pass
    return False


def _get_fill_color(dxf):
    """Extract fill color from a DifferentialStyle."""
    if dxf is None or dxf.fill is None:
        return None
    try:
        fg = dxf.fill.fgColor
        if fg and fg.rgb:
            return str(fg.rgb).upper()
    except Exception:
        pass
    try:
        bg = dxf.fill.bgColor
        if bg and bg.rgb:
            return str(bg.rgb).upper()
    except Exception:
        pass
    try:
        sc = dxf.fill.start_color
        if sc and sc.rgb:
            return str(sc.rgb).upper()
    except Exception:
        pass
    return None


def _check_cf_rule(rule, expected_value, color_checker, color_name):
    """
    Check if a conditional formatting rule matches the expected pattern.
    Returns True if rule is cellIs/equal for expected_value with the right color.
    """
    # Check rule type is cellIs with operator equal
    if rule.type != 'cellIs':
        return False
    if getattr(rule, 'operator', None) != 'equal':
        return False

    # Check formula matches the expected value
    formula = getattr(rule, 'formula', None)
    if formula is None:
        return False
    formula_list = list(formula) if not isinstance(formula, list) else formula
    matched_formula = False
    for f in formula_list:
        f_clean = str(f).strip().strip('"').strip("'")
        if f_clean.upper() == expected_value.upper():
            matched_formula = True
            break
        # Also check if the formula is like '"A"'
        if f.strip() == f'"{expected_value}"':
            matched_formula = True
            break
    if not matched_formula:
        return False

    # Check fill color
    fill_color = _get_fill_color(rule.dxf)
    if fill_color and color_checker(fill_color):
        return True

    return False


def verify_task(file_path):
    """
    Verify conditional formatting rules for time-off calendar.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check Calendar sheet exists
    if 'Calendar' not in wb.sheetnames:
        print("FAIL: 'Calendar' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Calendar']

    # Collect all CF rules across all ranges
    all_rules = []
    for cf in ws.conditional_formatting:
        cf_range = str(cf)
        for rule in cf.rules:
            all_rules.append((cf_range, rule))

    if not all_rules:
        print("FAIL: No conditional formatting rules found")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found {len(all_rules)} conditional formatting rule(s)")

    # Component 1: CF rule for 'A' = green (0.35 points)
    try:
        found_a = False
        for cf_range, rule in all_rules:
            if _check_cf_rule(rule, 'A', _is_green, 'green'):
                found_a = True
                fill_color = _get_fill_color(rule.dxf)
                print(f"PASS: Component 1 — 'A' = green rule found (fill: {fill_color}, range: {cf_range}) (0.35 pts)")
                total_score += 0.35
                break
        if not found_a:
            print("FAIL: Component 1 — No CF rule found for 'A' with green fill")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: CF rule for 'P' = yellow (0.35 points)
    try:
        found_p = False
        for cf_range, rule in all_rules:
            if _check_cf_rule(rule, 'P', _is_yellow, 'yellow'):
                found_p = True
                fill_color = _get_fill_color(rule.dxf)
                print(f"PASS: Component 2 — 'P' = yellow rule found (fill: {fill_color}, range: {cf_range}) (0.35 pts)")
                total_score += 0.35
                break
        if not found_p:
            print("FAIL: Component 2 — No CF rule found for 'P' with yellow fill")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: CF rule for 'D' = red (0.30 points)
    try:
        found_d = False
        for cf_range, rule in all_rules:
            if _check_cf_rule(rule, 'D', _is_red, 'red'):
                found_d = True
                fill_color = _get_fill_color(rule.dxf)
                print(f"PASS: Component 3 — 'D' = red rule found (fill: {fill_color}, range: {cf_range}) (0.30 pts)")
                total_score += 0.30
                break
        if not found_d:
            print("FAIL: Component 3 — No CF rule found for 'D' with red fill")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
