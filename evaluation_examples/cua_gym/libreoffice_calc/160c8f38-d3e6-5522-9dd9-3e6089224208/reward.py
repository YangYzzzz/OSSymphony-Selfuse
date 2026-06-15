"""
Reward Script: Conditional formatting on Daily Revenue column for >10% change
Task ID: calc_gcv_032
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Conditional formatting rule exists on the C column data range
  Component 2 (0.3): Formula checks percentage change >10% from previous row
  Component 3 (0.2): Fill color is bright green (#00FF00 / ARGB FF00FF00)
  Component 4 (0.2): Rule type is expression/formula with solid fill
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_032'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
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

    ws = wb.active

    # Gather all conditional formatting rules
    cf_rules_list = list(ws.conditional_formatting)

    if len(cf_rules_list) == 0:
        print("FAIL: No conditional formatting rules found")
        print("REWARD: 0.0")
        return 0.0

    # Find the best matching rule among all CF rules
    # We look for one that applies to column C and uses a percentage change formula
    best_rule = None
    best_range_str = None

    for cf in cf_rules_list:
        range_str = str(cf)
        # Check if the range covers column C cells (e.g., C2:C40, C3:C40)
        # The range string from openpyxl looks like "<ConditionalFormatting C3:C40>"
        # Extract the cell range
        match = re.search(r'([A-Z]+\d+(?::[A-Z]+\d+)?)', range_str)
        if not match:
            continue
        cell_range = match.group(1)

        # Check that the range is in column C
        range_parts = cell_range.split(':')
        col_match_all = all(re.match(r'^C\d+$', p) for p in range_parts)
        if not col_match_all:
            continue

        for rule in cf.rules:
            best_rule = rule
            best_range_str = cell_range
            break
        if best_rule:
            break

    if best_rule is None:
        print("FAIL: No conditional formatting rule found on column C")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Conditional formatting rule exists on correct range (0.3 points)
    # The range should cover C column data rows. Task says C2:C40 or C3:C40.
    # Context clarifies C3:C40 (row 2 has no previous row for comparison).
    # Accept ranges like C2:C40 or C3:C40 (both are reasonable interpretations).
    try:
        range_match = re.match(r'^C(\d+):C(\d+)$', best_range_str)
        if range_match:
            start_row = int(range_match.group(1))
            end_row = int(range_match.group(2))
            # Start should be row 2 or 3, end should be row 40 (or close)
            if start_row in (2, 3) and end_row >= 38:
                print(f"PASS: Component 1 - CF rule on range {best_range_str} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"PARTIAL: Component 1 - CF range {best_range_str} exists on C column but rows differ from expected C2:C40 or C3:C40")
                total_score += 0.15
        else:
            print(f"FAIL: Component 1 - Range '{best_range_str}' is not a proper C column range")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Formula checks percentage change >10% (0.3 points)
    # Expected formula pattern: (Cn-Cn-1)/Cn-1>0.1 or similar
    try:
        formula_list = best_rule.formula if best_rule.formula else []
        if formula_list:
            formula = formula_list[0].upper().replace(' ', '')
            # Normalize: accept various forms of the percentage change formula
            # Core pattern: (C<n>-C<n-1>)/C<n-1>>0.1
            # Could also be ABS variant or slightly different notation
            pct_pattern = re.compile(
                r'\(C(\d+)-C(\d+)\)/C(\d+)>0\.1'
            )
            match = pct_pattern.search(formula)
            if match:
                n = int(match.group(1))
                n_minus_1 = int(match.group(2))
                denom = int(match.group(3))
                if n - n_minus_1 == 1 and denom == n_minus_1:
                    print(f"PASS: Component 2 - Formula '{formula_list[0]}' correctly checks >10% change (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"PARTIAL: Component 2 - Formula '{formula_list[0]}' has percentage pattern but row refs seem off")
                    total_score += 0.15
            else:
                # Check for alternative formulations
                if '>0.1' in formula or '>10%' in formula or '>0,1' in formula:
                    print(f"PARTIAL: Component 2 - Formula '{formula_list[0]}' contains >0.1 threshold but pattern differs")
                    total_score += 0.1
                else:
                    print(f"FAIL: Component 2 - Formula '{formula_list[0]}' does not match expected percentage change pattern")
        else:
            print("FAIL: Component 2 - No formula found in the conditional formatting rule")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Fill color is bright green #00FF00 (ARGB FF00FF00) (0.2 points)
    try:
        if best_rule.dxf and best_rule.dxf.fill:
            fill = best_rule.dxf.fill
            fg_rgb = None
            if fill.fgColor and fill.fgColor.rgb:
                fg_rgb = str(fill.fgColor.rgb).upper()

            # Accept FF00FF00 (8-char ARGB) or 0000FF00 (with alpha 00)
            if fg_rgb and '00FF00' in fg_rgb:
                print(f"PASS: Component 3 - Fill color is green: {fg_rgb} (0.2 pts)")
                total_score += 0.2
            else:
                # Also check bgColor as some implementations use that
                bg_rgb = None
                if fill.bgColor and fill.bgColor.rgb:
                    bg_rgb = str(fill.bgColor.rgb).upper()
                if bg_rgb and '00FF00' in bg_rgb:
                    print(f"PASS: Component 3 - Fill bgColor is green: {bg_rgb} (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 - Fill color {fg_rgb} / bg {bg_rgb} is not #00FF00")
        else:
            print("FAIL: Component 3 - No fill/dxf found in the conditional formatting rule")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Rule type is expression/formula with solid fill (0.2 points)
    try:
        rule_type = best_rule.type
        fill_type = None
        if best_rule.dxf and best_rule.dxf.fill:
            fill_type = best_rule.dxf.fill.fill_type

        type_ok = rule_type in ('expression', 'formula')
        fill_ok = fill_type == 'solid'

        if type_ok and fill_ok:
            print(f"PASS: Component 4 - Rule type '{rule_type}' with solid fill (0.2 pts)")
            total_score += 0.2
        elif type_ok:
            print(f"PARTIAL: Component 4 - Rule type '{rule_type}' correct but fill_type is '{fill_type}'")
            total_score += 0.1
        elif fill_ok:
            print(f"PARTIAL: Component 4 - Fill is solid but rule type is '{rule_type}' (expected expression)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 - Rule type '{rule_type}', fill_type '{fill_type}'")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
persist_app_state("libreoffice_calc")

file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
