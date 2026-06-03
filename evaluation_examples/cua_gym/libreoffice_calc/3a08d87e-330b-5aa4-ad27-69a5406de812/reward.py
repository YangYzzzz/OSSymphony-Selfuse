"""
Reward Script: Apply conditional formatting to B2:B20 to highlight non-standard values
Task ID: calc_gcv_049
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Conditional formatting rule exists on range covering B2:B20
  Component 2 (0.4): Formula checks against predefined list {10,20,30,40,50}
  Component 3 (0.3): Fill color is #FF4444 (ARGB: FFFF4444)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_049'


def persist_app_state(domain: str):
    """Save any unsaved changes in LibreOffice before verification."""
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
    Verify task completion with progressive scoring.
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

    # Collect all conditional formatting rules
    cf_rules_list = list(ws.conditional_formatting)

    # Component 1: Conditional formatting rule exists covering B2:B20 (0.3 points)
    # This check FAILS on initial (0 rules) and PASSES on golden (1 rule covering B2:B20)
    try:
        found_cf_on_range = False
        matching_cf = None
        matching_rule = None

        for cf in cf_rules_list:
            # Check if the CF range covers B2:B20
            cf_range_str = str(cf).strip()
            # The range could be specified as "B2:B20" or could be a superset
            for rule in cf.rules:
                # Check if B2:B20 is in the range
                # We check if the range string contains B2:B20 or is equivalent
                if 'B2:B20' in cf_range_str or 'B2:B20' in str(cf.sqref):
                    found_cf_on_range = True
                    matching_cf = cf
                    matching_rule = rule
                    break
            if found_cf_on_range:
                break

        if found_cf_on_range:
            print(f"PASS: Component 1 — Conditional formatting found on B2:B20 (0.3 pts)")
            total_score += 0.3
        else:
            # Fallback: check if there's any CF rule with expression type at all
            # covering a range in column B
            for cf in cf_rules_list:
                cf_str = str(cf.sqref) if hasattr(cf, 'sqref') else str(cf)
                if 'B' in cf_str:
                    for rule in cf.rules:
                        if rule.type == 'expression':
                            found_cf_on_range = True
                            matching_cf = cf
                            matching_rule = rule
                            break
                if found_cf_on_range:
                    break

            if found_cf_on_range:
                print(f"PASS: Component 1 — Conditional formatting found on column B range (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — No conditional formatting found on B2:B20. "
                      f"Total CF rules: {len(cf_rules_list)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Formula checks values against {10,20,30,40,50} (0.4 points)
    # Expected formula: AND(B2<>10,B2<>20,B2<>30,B2<>40,B2<>50)
    # This FAILS on initial (no CF rules) and PASSES on golden
    try:
        formula_correct = False
        if matching_rule and matching_rule.formula:
            formula_str = str(matching_rule.formula[0]).strip()
            # Normalize: uppercase, remove spaces
            normalized = formula_str.upper().replace(" ", "")
            print(f"  DEBUG: Found formula: {formula_str}")

            # Check that the formula references all 5 values: 10, 20, 30, 40, 50
            # and uses AND with <> comparisons
            has_and = 'AND(' in normalized
            has_10 = '<>10' in normalized or '<>10,' in normalized or '<>10)' in normalized
            has_20 = '<>20' in normalized or '<>20,' in normalized or '<>20)' in normalized
            has_30 = '<>30' in normalized or '<>30,' in normalized or '<>30)' in normalized
            has_40 = '<>40' in normalized or '<>40,' in normalized or '<>40)' in normalized
            has_50 = '<>50' in normalized or '<>50,' in normalized or '<>50)' in normalized

            # Make sure we're checking all 5 values
            all_values_present = has_10 and has_20 and has_30 and has_40 and has_50

            if has_and and all_values_present:
                formula_correct = True
                print(f"PASS: Component 2 — Formula correctly checks AND(<>10,<>20,<>30,<>40,<>50) (0.4 pts)")
                total_score += 0.4
            elif all_values_present:
                # Has all values but maybe different structure (OR, nested IFs, etc.)
                # Give partial credit
                print(f"PARTIAL: Component 2 — Formula has all 5 values but unexpected structure (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — Formula missing values. "
                      f"AND={has_and}, 10={has_10}, 20={has_20}, 30={has_30}, 40={has_40}, 50={has_50}")
        else:
            print(f"FAIL: Component 2 — No matching CF rule/formula found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Fill color is #FF4444 (ARGB: FFFF4444) (0.3 points)
    # This FAILS on initial (no CF rules) and PASSES on golden
    try:
        color_correct = False
        if matching_rule and matching_rule.dxf and matching_rule.dxf.fill:
            fill = matching_rule.dxf.fill
            fg_rgb = None
            if fill.fgColor and fill.fgColor.rgb:
                fg_rgb = str(fill.fgColor.rgb).upper()

            print(f"  DEBUG: Fill fgColor RGB: {fg_rgb}")

            if fg_rgb:
                # Accept FFFF4444 exactly, or close variants
                # The task says #FF4444, which in ARGB is FFFF4444
                if fg_rgb == 'FFFF4444':
                    color_correct = True
                    print(f"PASS: Component 3 — Fill color is FFFF4444 (red) (0.3 pts)")
                    total_score += 0.3
                elif 'FF4444' in fg_rgb or 'FF0000' in fg_rgb:
                    # Close red variant — partial credit
                    print(f"PARTIAL: Component 3 — Fill color {fg_rgb} is close to FFFF4444 (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 3 — Expected FFFF4444, found {fg_rgb}")
            else:
                print(f"FAIL: Component 3 — Fill fgColor RGB is None")
        else:
            print(f"FAIL: Component 3 — No matching rule with fill found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
