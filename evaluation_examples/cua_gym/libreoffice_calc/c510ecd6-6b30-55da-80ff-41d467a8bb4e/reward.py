"""
Reward Script: Highlight weekend rows using WEEKDAY conditional formatting
Task ID: osworld_calc_conditional_format_weekday_008
Domain: libreoffice_calc

Scoring Rubric:
  Component 1 (0.4 pts): A formula-based conditional formatting rule exists
                          that covers data rows (A2:E21 or similar) and uses WEEKDAY formula
  Component 2 (0.35 pts): The formula correctly identifies weekends using WEEKDAY
                           with column $A reference and checks for day=1 (Sunday) or day=7 (Saturday)
  Component 3 (0.25 pts): The conditional formatting rule applies a light blue fill
                           (color close to ADD8E6 / lightblue)
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'osworld_calc_conditional_format_weekday_008'


def normalize_formula(formula):
    """Normalize a formula string for comparison: strip whitespace, uppercase."""
    if not formula:
        return ''
    return re.sub(r'\s+', '', formula.upper())


def color_distance(hex1, hex2):
    """
    Calculate distance between two RGB hex colors.
    Accepts 6-char or 8-char hex strings (ignores alpha).
    Returns sum of absolute differences of R, G, B channels.
    """
    def to_rgb(h):
        h = h.upper().lstrip('#')
        if len(h) == 8:  # ARGB
            h = h[2:]  # strip alpha
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
        return r, g, b

    try:
        r1, g1, b1 = to_rgb(hex1)
        r2, g2, b2 = to_rgb(hex2)
        return abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)
    except Exception:
        return 999


def find_weekday_cf_rules(ws):
    """
    Find all conditional formatting rules that are formula-based (type='expression'),
    reference a WEEKDAY formula, and apply to the data area with $A column reference.
    Returns a list of (cf_range_str, rule, formula_text) tuples.
    """
    candidates = []
    for cf in ws.conditional_formatting:
        cf_range_str = str(cf)
        for rule in cf.rules:
            if rule.type != 'expression':
                continue
            formulas = getattr(rule, 'formula', None)
            if not formulas:
                continue
            formula_text = formulas[0] if isinstance(formulas, list) else str(formulas)
            normalized = normalize_formula(formula_text)
            if 'WEEKDAY' not in normalized:
                continue
            # Must reference column $A (the appointment date column)
            if '$A' not in normalized and 'A2' not in normalized:
                continue
            candidates.append((cf_range_str, rule, formula_text))
    return candidates


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns float between 0.0 and 1.0.

    The task asks to apply a conditional formatting rule using WEEKDAY formula
    to highlight entire rows in light blue for weekend appointments.
    """
    total_score = 0.0

    # --- Precondition gate ---
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb.active
    if ws is None:
        print("CRITICAL: No active sheet found.")
        print("REWARD: 0.0")
        return 0.0

    # Count total CF rules for debugging
    all_cf_count = sum(1 for cf in ws.conditional_formatting for _ in cf.rules)
    print(f"Total conditional formatting rules found: {all_cf_count}")

    # Gather candidates (formula-based rules referencing WEEKDAY)
    candidates = find_weekday_cf_rules(ws)

    # ------------------------------------------------------------------
    # Component 1 (0.4 pts):
    # A formula-based ('expression') conditional formatting rule exists
    # that covers the data area (rows 2+) and references a WEEKDAY formula.
    # ------------------------------------------------------------------
    try:
        if len(candidates) > 0:
            print(f"PASS: Component 1 — Found {len(candidates)} WEEKDAY formula conditional formatting rule(s) (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 — No formula-based conditional formatting rule with WEEKDAY formula found")
            # Debug: print what rules exist
            for cf in ws.conditional_formatting:
                for rule in cf.rules:
                    print(f"  DEBUG: Found rule type={rule.type}, formula={getattr(rule, 'formula', None)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2 (0.35 pts):
    # The formula correctly identifies weekends:
    # - Must check for WEEKDAY value = 1 (Sunday) AND WEEKDAY value = 7 (Saturday)
    # - The $A column reference is present (anchored to Appointment Date column)
    # ------------------------------------------------------------------
    try:
        comp2_found = False
        for cf_range_str, rule, formula_text in candidates:
            normalized = normalize_formula(formula_text)
            print(f"  Checking formula: {formula_text}")
            print(f"  Normalized: {normalized}")

            # Weekend detection requires both:
            #   - Sunday marker: WEEKDAY=1 (mode 1, Sun=1..Sat=7) or WEEKDAY=7 (mode 2, Mon=1..Sun=7)
            #   - Saturday marker: WEEKDAY=7 (mode 1) or WEEKDAY=6 (mode 2)
            # Accept mode 1: day=1 (Sunday) AND day=7 (Saturday) -- most common
            # Accept mode 2: day=7 (Sunday) AND day=6 (Saturday)
            mode1_weekend = ('=1' in normalized and '=7' in normalized)
            mode2_weekend = ('=7' in normalized and '=6' in normalized)
            has_dollar_a = '$A' in normalized

            if (mode1_weekend or mode2_weekend) and has_dollar_a:
                comp2_found = True
                print(f"PASS: Component 2 — Formula correctly detects weekends with $A reference (0.35 pts)")
                break

        if comp2_found:
            total_score += 0.35
        elif len(candidates) == 0:
            print("FAIL: Component 2 — No candidate rules to check")
        else:
            print("FAIL: Component 2 — Formula found but does not correctly encode both weekend days with $A")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3 (0.25 pts):
    # The conditional formatting rule applies a light blue fill.
    # Light blue (CSS "lightblue") = #ADD8E6 = ARGB FFADD8E6
    # We accept any color close to light blue (within distance threshold).
    # ------------------------------------------------------------------
    # Tolerance: allow reasonable deviation from exact light blue
    # ADD8E6 = (173, 216, 230). We accept within 80 total channel distance.
    LIGHT_BLUE_ARGB = 'FFADD8E6'
    COLOR_TOLERANCE = 80

    try:
        comp3_found = False
        for cf_range_str, rule, formula_text in candidates:
            dxf = getattr(rule, 'dxf', None)
            if dxf is None:
                print("FAIL: Component 3 — Rule has no DifferentialStyle (dxf)")
                continue
            fill = getattr(dxf, 'fill', None)
            if fill is None:
                print("FAIL: Component 3 — DifferentialStyle has no fill")
                continue

            try:
                fg_color = fill.fgColor
                if fg_color is None:
                    print("FAIL: Component 3 — Fill has no fgColor")
                    continue
                actual_argb = fg_color.rgb
                print(f"  Fill fgColor ARGB: {actual_argb}")
                dist = color_distance(actual_argb, LIGHT_BLUE_ARGB)
                print(f"  Color distance from light blue ({LIGHT_BLUE_ARGB}): {dist}")
                if dist <= COLOR_TOLERANCE:
                    comp3_found = True
                    print(f"PASS: Component 3 — Light blue fill applied (color={actual_argb}, distance={dist}) (0.25 pts)")
                    break
                else:
                    print(f"FAIL: Component 3 — Fill color {actual_argb} not close to light blue (distance {dist} > {COLOR_TOLERANCE})")
            except Exception as e:
                print(f"ERROR: Component 3 inner — {e}")

        if comp3_found:
            total_score += 0.25
        elif len(candidates) == 0:
            print("FAIL: Component 3 — No candidate rules to check")
        else:
            print("FAIL: Component 3 — No matching light blue fill found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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
