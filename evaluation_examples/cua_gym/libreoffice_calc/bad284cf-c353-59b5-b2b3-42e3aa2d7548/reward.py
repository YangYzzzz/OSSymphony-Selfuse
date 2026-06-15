"""
Reward Script: Conditional formatting on D2:D50 for stale data flagging
Task ID: calc_gcv_045
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): CF rule exists covering D2:D50
  Component 2 (0.4): Formula checks TODAY()-$C2>90
  Component 3 (0.3): Fill color is amber #FFBF00 (ARGB FFFFBF00)
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_045'


def verify_task(file_path):
    """
    Verify conditional formatting task completion with progressive scoring.
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

    # Collect all conditional formatting rules
    cf_rules_list = list(ws.conditional_formatting)

    if len(cf_rules_list) == 0:
        print("FAIL: No conditional formatting rules found at all")
        print("REWARD: 0.0")
        return 0.0

    # Find CF rules that cover D2:D50 range
    # We look for rules whose range includes D2:D50 (or a superset)
    matching_cf = None
    matching_rule = None

    for cf in cf_rules_list:
        cf_range_str = str(cf).strip()
        for rule in cf.rules:
            # Check if the range covers D2:D50
            # Accept exact match or ranges that encompass D2:D50
            if _range_covers_d2_d50(cf_range_str):
                matching_cf = cf
                matching_rule = rule
                break
        if matching_rule is not None:
            break

    # Component 1: CF rule exists covering D2:D50 (0.3 points)
    try:
        if matching_rule is not None:
            print(f"PASS: Component 1 — CF rule found covering D2:D50 (range: {matching_cf}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No CF rule found covering D2:D50. Found ranges: {[str(cf) for cf in cf_rules_list]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Formula checks TODAY()-$C2>90 (0.4 points)
    try:
        if matching_rule is not None and matching_rule.type == 'expression':
            formula_list = matching_rule.formula
            if formula_list and len(formula_list) > 0:
                formula = str(formula_list[0]).strip()
                # Normalize: remove spaces, uppercase
                normalized = formula.upper().replace(" ", "")
                # Accept variants: TODAY()-$C2>90, TODAY()-C2>90
                # Core pattern: TODAY() minus C column reference > 90
                if re.search(r'TODAY\(\)\s*-\s*\$?C\d+\s*>\s*90', formula, re.IGNORECASE):
                    print(f"PASS: Component 2 — Formula matches: '{formula}' (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 2 — Formula does not match expected pattern. Found: '{formula}'")
            else:
                print(f"FAIL: Component 2 — Rule has no formula")
        else:
            if matching_rule is None:
                print(f"FAIL: Component 2 — No matching CF rule found")
            else:
                print(f"FAIL: Component 2 — Rule type is '{matching_rule.type}', expected 'expression'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Fill color is amber #FFBF00 (ARGB FFFFBF00) (0.3 points)
    try:
        if matching_rule is not None and hasattr(matching_rule, 'dxf') and matching_rule.dxf:
            dxf = matching_rule.dxf
            if dxf.fill and dxf.fill.fgColor:
                color_rgb = dxf.fill.fgColor.rgb
                # Accept FFFFBF00 (with alpha) or 00FFBF00
                if color_rgb is not None:
                    color_upper = str(color_rgb).upper()
                    # The expected ARGB is FFFFBF00
                    # Also accept just the RGB portion FFBF00 at the end
                    if color_upper == 'FFFFBF00' or color_upper.endswith('FFBF00'):
                        print(f"PASS: Component 3 — Fill color is amber FFBF00 (ARGB: {color_rgb}) (0.3 pts)")
                        total_score += 0.3
                    else:
                        print(f"FAIL: Component 3 — Fill color mismatch. Expected FFFFBF00, found: {color_rgb}")
                else:
                    print(f"FAIL: Component 3 — Fill fgColor.rgb is None")
            else:
                print(f"FAIL: Component 3 — No fill defined in CF rule's differential style")
        else:
            if matching_rule is None:
                print(f"FAIL: Component 3 — No matching CF rule found")
            else:
                print(f"FAIL: Component 3 — No differential style on the CF rule")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


def _range_covers_d2_d50(range_str):
    """
    Check if the given range string covers D2:D50.
    Accepts exact D2:D50 or supersets like D1:D100.
    Also handles multi-range strings separated by spaces.
    """
    # Handle ConditionalFormatting string representation
    # It may look like "<ConditionalFormatting D2:D50>" or just "D2:D50"
    range_str = range_str.replace('<ConditionalFormatting ', '').replace('>', '').strip()

    # Split multi-ranges by space
    parts = range_str.split()
    for part in parts:
        part = part.strip().upper()
        # Match patterns like D2:D50, D1:D100, $D$2:$D$50
        # Remove $ signs for easier parsing
        clean = part.replace('$', '')
        match = re.match(r'^([A-Z]+)(\d+):([A-Z]+)(\d+)$', clean)
        if match:
            col_start, row_start, col_end, row_end = match.groups()
            row_start, row_end = int(row_start), int(row_end)
            # Must cover column D, rows 2-50
            if col_start == 'D' and col_end == 'D' and row_start <= 2 and row_end >= 50:
                return True
    return False


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
