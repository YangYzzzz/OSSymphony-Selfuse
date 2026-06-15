"""
Reward Script: Apply conditional formatting for cancelled orders
Task ID: calc_gcv_018
Domain: libreoffice_calc

Scoring Rubric:
  Component 1 (0.30): Conditional formatting rule exists on range A2:J60
  Component 2 (0.25): Formula is $J2="Cancelled" (or equivalent)
  Component 3 (0.25): Font color is gray (#808080)
  Component 4 (0.20): Strikethrough is enabled
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_018'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify conditional formatting on cancelled order rows.
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

    # Find all conditional formatting rules
    cf_rules_list = list(ws.conditional_formatting)
    print(f"INFO: Found {len(cf_rules_list)} conditional formatting rule group(s)")

    if len(cf_rules_list) == 0:
        print("FAIL: No conditional formatting rules found at all")
        print("REWARD: 0.0")
        return 0.0

    # Search for a rule that targets the cancelled rows
    # We look for a formula-based rule referencing "Cancelled" in column J
    target_rule = None
    target_range = None

    for cf in cf_rules_list:
        for rule in cf.rules:
            if rule.type == 'expression' and rule.formula:
                formula_str = str(rule.formula[0]).upper().replace(" ", "")
                # Check if formula references "CANCELLED" and column J
                if 'CANCELLED' in formula_str and 'J' in formula_str:
                    target_rule = rule
                    target_range = str(cf)
                    print(f"INFO: Found matching rule — range: {target_range}, formula: {rule.formula}")
                    break
        if target_rule:
            break

    if target_rule is None:
        # Broader search: any expression rule with "Cancelled"
        for cf in cf_rules_list:
            for rule in cf.rules:
                if rule.type == 'expression' and rule.formula:
                    formula_str = str(rule.formula[0]).upper()
                    if 'CANCELLED' in formula_str:
                        target_rule = rule
                        target_range = str(cf)
                        print(f"INFO: Found broader matching rule — range: {target_range}, formula: {rule.formula}")
                        break
            if target_rule:
                break

    if target_rule is None:
        print("FAIL: No conditional formatting rule with 'Cancelled' formula found")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: CF rule exists and covers range A2:J60 (0.30 points)
    # The range must cover at minimum A2:J60
    try:
        range_str = target_range.replace("<ConditionalFormatting ", "").replace(">", "").strip()
        print(f"INFO: CF range string: '{range_str}'")

        # Parse the range to check coverage
        from openpyxl.utils import range_boundaries
        try:
            min_col, min_row, max_col, max_row = range_boundaries(range_str)
            # A=1, J=10; row 2 to 60
            covers_a2_j60 = (min_col <= 1 and min_row <= 2 and max_col >= 10 and max_row >= 60)
        except Exception:
            # If range_boundaries fails, do string check
            range_upper = range_str.upper()
            covers_a2_j60 = ('A2' in range_upper and 'J60' in range_upper)

        if covers_a2_j60:
            print(f"PASS: Component 1 — CF rule covers A2:J60 range ({range_str}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — CF range '{range_str}' does not cover A2:J60")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Formula checks $J column for "Cancelled" (0.25 points)
    try:
        formula_str = str(target_rule.formula[0])
        formula_normalized = formula_str.upper().replace(" ", "")
        # Accept variants: $J2="Cancelled", $J2="CANCELLED", etc.
        # The key pattern is referencing column J (absolute or relative) and "Cancelled"
        has_j_ref = ('$J' in formula_normalized or '=J' in formula_normalized
                     or formula_normalized.startswith('J'))
        has_cancelled = '"CANCELLED"' in formula_normalized

        if has_j_ref and has_cancelled:
            print(f"PASS: Component 2 — Formula correctly references column J and 'Cancelled': {formula_str} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Formula '{formula_str}' missing J reference ({has_j_ref}) or 'Cancelled' ({has_cancelled})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Font color is gray #808080 (0.25 points)
    try:
        dxf = target_rule.dxf
        if dxf and dxf.font and dxf.font.color:
            color_rgb = dxf.font.color.rgb
            print(f"INFO: DXF font color rgb: {color_rgb}")
            # Accept FF808080 or 00808080 (openpyxl may store either alpha prefix)
            if color_rgb and '808080' in str(color_rgb).upper():
                print(f"PASS: Component 3 — Font color is gray (#808080): {color_rgb} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Font color is {color_rgb}, expected #808080")
        else:
            print(f"FAIL: Component 3 — No font color defined in conditional formatting rule")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Strikethrough is enabled (0.20 points)
    try:
        dxf = target_rule.dxf
        if dxf and dxf.font and dxf.font.strike:
            print(f"PASS: Component 4 — Strikethrough enabled: {dxf.font.strike} (0.20 pts)")
            total_score += 0.20
        else:
            strike_val = dxf.font.strike if (dxf and dxf.font) else None
            print(f"FAIL: Component 4 — Strikethrough not enabled (strike={strike_val})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
