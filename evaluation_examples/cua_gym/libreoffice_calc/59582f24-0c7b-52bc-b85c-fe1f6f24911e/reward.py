"""
Reward Script: Highlight statistical outliers in F2:F55 with magenta background
Task ID: calc_gcv_043
Domain: libreoffice_calc
Scoring:
  Component 1 (0.35): Conditional formatting rule exists on range F2:F55
  Component 2 (0.35): Formula checks >2 standard deviations from mean
  Component 3 (0.30): Fill color is bright magenta (#FF00FF / ARGB FFFF00FF)
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_043'


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

    # Precondition: sheet should be 'Statistical_Outliers' and have data in F column
    if ws.title != 'Statistical_Outliers':
        # Try to find the right sheet
        for name in wb.sheetnames:
            if 'outlier' in name.lower() or 'statistical' in name.lower():
                ws = wb[name]
                break

    # Collect all conditional formatting rules
    cf_list = list(ws.conditional_formatting)

    # Component 1: Conditional formatting rule exists on range F2:F55 (0.35 points)
    try:
        found_cf_on_range = False
        matching_cf = None
        matching_rule = None

        for cf in cf_list:
            cf_range_str = str(cf).upper()
            for rule in cf.rules:
                # Check if the range covers F2:F55 (could be written various ways)
                # Accept ranges that include F2:F55
                if 'F2' in cf_range_str and 'F55' in cf_range_str:
                    found_cf_on_range = True
                    matching_cf = cf
                    matching_rule = rule
                    break
                # Also accept if the range is F2:F55 exactly
                if cf_range_str.replace(' ', '') in ['F2:F55', 'F55:F2', '$F$2:$F$55']:
                    found_cf_on_range = True
                    matching_cf = cf
                    matching_rule = rule
                    break
            if found_cf_on_range:
                break

        if found_cf_on_range:
            print(f"PASS: Component 1 — Conditional formatting found on range including F2:F55 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — No conditional formatting on F2:F55. Found {len(cf_list)} CF rules: {[str(cf) for cf in cf_list]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Formula checks >2 standard deviations from mean (0.35 points)
    try:
        if matching_rule is not None:
            rule_type = matching_rule.type
            formula_list = getattr(matching_rule, 'formula', None)
            formula_str = ''
            if formula_list:
                formula_str = str(formula_list[0]).upper().replace(' ', '')

            print(f"  DEBUG: rule type={rule_type}, formula={formula_str}")

            # The formula should reference ABS, AVERAGE, STDEV, and use 2* multiplier
            has_abs = 'ABS(' in formula_str
            has_average = 'AVERAGE(' in formula_str
            has_stdev = 'STDEV(' in formula_str or 'STDEV.S(' in formula_str
            has_2x = '2*STDEV' in formula_str or '2*STDEV.S' in formula_str or 'STDEV*2' in formula_str or 'STDEV.S*2' in formula_str
            has_f_ref = 'F2' in formula_str or '$F$2' in formula_str or 'F$2' in formula_str or '$F2' in formula_str

            # Check that the formula is an expression type (FormulaRule)
            is_expression = rule_type == 'expression'

            if is_expression and has_abs and has_average and has_stdev and has_2x and has_f_ref:
                print(f"PASS: Component 2 — Formula correctly checks >2 SD from mean (0.35 pts)")
                total_score += 0.35
            elif is_expression and has_average and has_stdev and has_f_ref:
                # Partial: has the right functions but maybe different threshold structure
                print(f"PARTIAL: Component 2 — Formula has AVERAGE/STDEV but structure differs. Formula: {formula_str} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Formula doesn't match expected pattern. Type={rule_type}, Formula={formula_str}")
                print(f"  has_abs={has_abs}, has_average={has_average}, has_stdev={has_stdev}, has_2x={has_2x}, has_f_ref={has_f_ref}, is_expression={is_expression}")
        else:
            print(f"FAIL: Component 2 — No matching rule found (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Fill color is bright magenta #FF00FF (ARGB: FFFF00FF) (0.30 points)
    try:
        if matching_rule is not None:
            dxf = matching_rule.dxf
            if dxf and dxf.fill:
                fg_rgb = None
                bg_rgb = None
                try:
                    fg_rgb = dxf.fill.fgColor.rgb if dxf.fill.fgColor else None
                except:
                    pass
                try:
                    bg_rgb = dxf.fill.bgColor.rgb if dxf.fill.bgColor else None
                except:
                    pass

                print(f"  DEBUG: dxf fill fgColor={fg_rgb}, bgColor={bg_rgb}")

                # Check if either fg or bg color is magenta FFFF00FF
                magenta_argb = 'FFFF00FF'
                color_match = False
                if fg_rgb and fg_rgb.upper() == magenta_argb:
                    color_match = True
                if bg_rgb and bg_rgb.upper() == magenta_argb:
                    color_match = True

                if color_match:
                    print(f"PASS: Component 3 — Fill color is magenta #FF00FF (0.30 pts)")
                    total_score += 0.30
                else:
                    # Check for close variants (e.g. 00FF00FF without alpha)
                    fg_hex = (fg_rgb or '').upper()
                    bg_hex = (bg_rgb or '').upper()
                    if 'FF00FF' in fg_hex or 'FF00FF' in bg_hex:
                        print(f"PARTIAL: Component 3 — Fill contains FF00FF but alpha may differ. fg={fg_rgb}, bg={bg_rgb} (0.15 pts)")
                        total_score += 0.15
                    else:
                        print(f"FAIL: Component 3 — Fill color is not magenta. fg={fg_rgb}, bg={bg_rgb}")
            else:
                print(f"FAIL: Component 3 — No fill defined in conditional formatting rule")
        else:
            print(f"FAIL: Component 3 — No matching rule found (depends on Component 1)")
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
