"""
Reward Script: Create conditional formatting rules for weekday/weekend highlighting
Task ID: osworld_calc_conditional_format_weekday_010
Domain: libreoffice_calc
Scoring:
  Component 1: At least 2 CF rules exist                              (0.2 pts)
  Component 2: Weekday rule (WEEKDAY formula + green fill)            (0.4 pts)
  Component 3: Weekend rule (WEEKDAY formula + red fill)              (0.4 pts)
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'osworld_calc_conditional_format_weekday_010'


def _is_greenish(rgb_hex: str) -> bool:
    """Check if an 8-char ARGB color is greenish (G component dominant)."""
    try:
        if len(rgb_hex) == 8:
            r = int(rgb_hex[2:4], 16)
            g = int(rgb_hex[4:6], 16)
            b = int(rgb_hex[6:8], 16)
            # Green dominant and reasonably light (pastel/light green)
            return g > r and g > b and g > 150
        return False
    except Exception:
        return False


def _is_reddish(rgb_hex: str) -> bool:
    """Check if an 8-char ARGB color is reddish (R component dominant)."""
    try:
        if len(rgb_hex) == 8:
            r = int(rgb_hex[2:4], 16)
            g = int(rgb_hex[4:6], 16)
            b = int(rgb_hex[6:8], 16)
            # Red dominant and reasonably light (pastel/light red)
            return r > g and r > b and r > 150
        return False
    except Exception:
        return False


def _is_weekday_formula(formula_str: str) -> bool:
    """
    Check if formula is WEEKDAY-based condition for weekdays (Mon-Fri).
    Accepts: WEEKDAY($A2,2)<=5, WEEKDAY($A2,2)<6, etc.
    """
    f = formula_str.upper().replace(' ', '')
    if 'WEEKDAY' not in f:
        return False
    # Mode 2: Mon=1..Fri=5..Sat=6..Sun=7 — weekday condition: <=5 or <6
    if '<=5' in f or '<6' in f:
        return True
    return False


def _is_weekend_formula(formula_str: str) -> bool:
    """
    Check if formula is WEEKDAY-based condition for weekends (Sat-Sun).
    Accepts: WEEKDAY($A2,2)>=6, WEEKDAY($A2,2)>5, etc.
    """
    f = formula_str.upper().replace(' ', '')
    if 'WEEKDAY' not in f:
        return False
    # Mode 2: Mon=1..Fri=5..Sat=6..Sun=7 — weekend condition: >=6 or >5
    if '>=6' in f or '>5' in f:
        return True
    # Mode 1: Sun=1..Sat=7 — weekend condition: =1 or =7 (Sunday=1, Saturday=7)
    if '=1' in f and '=7' in f:
        return True
    return False


def _get_matching_weekday_rule(all_rules):
    """Return first rule matching weekday formula + green fill, or None."""
    for rule in all_rules:
        if rule.type != 'expression':
            continue
        formulas = rule.formula if rule.formula else []
        if not any(_is_weekday_formula(str(f)) for f in formulas):
            continue
        try:
            fill_color = rule.dxf.fill.fgColor.rgb if (rule.dxf and rule.dxf.fill) else None
        except Exception:
            fill_color = None
        if fill_color and _is_greenish(fill_color):
            return rule, fill_color
    return None, None


def _get_matching_weekend_rule(all_rules):
    """Return first rule matching weekend formula + red fill, or None."""
    for rule in all_rules:
        if rule.type != 'expression':
            continue
        formulas = rule.formula if rule.formula else []
        if not any(_is_weekend_formula(str(f)) for f in formulas):
            continue
        try:
            fill_color = rule.dxf.fill.fgColor.rgb if (rule.dxf and rule.dxf.fill) else None
        except Exception:
            fill_color = None
        if fill_color and _is_reddish(fill_color):
            return rule, fill_color
    return None, None


def verify_task(file_path: str) -> float:
    """
    Verify conditional formatting rules for weekday/weekend highlighting.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Load workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get active sheet (or sheet named 'Shift Schedule')
    try:
        if 'Shift Schedule' in wb.sheetnames:
            ws = wb['Shift Schedule']
        else:
            ws = wb.active
        print(f"INFO: Checking sheet '{ws.title}'")
    except Exception as e:
        print(f"CRITICAL: Cannot access sheet: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all CF rules across all ranges
    all_rules = []
    try:
        cf_formatting = ws.conditional_formatting
        for cf_range in cf_formatting:
            for rule in cf_range.rules:
                all_rules.append(rule)
        print(f"INFO: Found {len(all_rules)} total CF rule(s)")
    except Exception as e:
        print(f"ERROR: Cannot read conditional formatting: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: At least 2 CF rules exist (0.2 points)
    # Both weekday and weekend rules must be present
    try:
        if len(all_rules) >= 2:
            print(f"PASS: Component 1 — At least 2 CF rules exist ({len(all_rules)} found) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected >= 2 CF rules, found {len(all_rules)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Weekday rule using WEEKDAY formula with green fill (0.4 points)
    # Must have formula testing Mon-Fri (e.g. WEEKDAY($A2,2)<=5) + greenish background fill
    try:
        matched_rule, fill_color = _get_matching_weekday_rule(all_rules)
        if matched_rule is not None:
            print(f"PASS: Component 2 — Weekday rule found: formula={matched_rule.formula}, fill={fill_color} (0.4 pts)")
            total_score += 0.4
        else:
            for rule in all_rules:
                formulas = rule.formula if rule.formula else []
                try:
                    fc = rule.dxf.fill.fgColor.rgb if (rule.dxf and rule.dxf.fill) else None
                except Exception:
                    fc = None
                print(f"  DEBUG rule: type={rule.type}, formula={formulas}, fill={fc}")
            print("FAIL: Component 2 — No weekday WEEKDAY formula rule with green fill found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Weekend rule using WEEKDAY formula with red fill (0.4 points)
    # Must have formula testing Sat-Sun (e.g. WEEKDAY($A2,2)>=6) + reddish background fill
    try:
        matched_rule, fill_color = _get_matching_weekend_rule(all_rules)
        if matched_rule is not None:
            print(f"PASS: Component 3 — Weekend rule found: formula={matched_rule.formula}, fill={fill_color} (0.4 pts)")
            total_score += 0.4
        else:
            for rule in all_rules:
                formulas = rule.formula if rule.formula else []
                try:
                    fc = rule.dxf.fill.fgColor.rgb if (rule.dxf and rule.dxf.fill) else None
                except Exception:
                    fc = None
                print(f"  DEBUG rule: type={rule.type}, formula={formulas}, fill={fc}")
            print("FAIL: Component 3 — No weekend WEEKDAY formula rule with red fill found")
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
