"""
Reward Script: Conditional formatting for duplicate IDs with pink background
Task ID: calc_gg3_041
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): CF rule exists on range covering A2:A101
  Component 2 (0.4): Rule uses COUNTIF-based duplicate detection formula
  Component 3 (0.3): Fill color is pink (FFFFC0CB or close variant)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_gg3_041'


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

    # Precondition: 'Submissions' sheet must exist
    if 'Submissions' not in wb.sheetnames:
        print("FAIL: 'Submissions' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Submissions']

    # Collect all conditional formatting rules
    cf_list = list(ws.conditional_formatting)

    # Component 1: CF rule exists on range covering A2:A101 (0.3 points)
    try:
        found_cf_on_range = False
        matching_cf = None
        matching_rule = None

        for cf in cf_list:
            cf_range_str = str(cf).upper()
            # Check if the CF range covers A2:A101 (exact or superset)
            # Accept various formats: "A2:A101", "<ConditionalFormatting A2:A101>"
            if 'A2:A101' in cf_range_str or 'A2:A101' in cf_range_str.replace(' ', ''):
                found_cf_on_range = True
                matching_cf = cf
                break

        if found_cf_on_range:
            print(f"PASS: Component 1 — CF rule found on range A2:A101 (0.3 pts)")
            total_score += 0.3
        else:
            # Also check if there's any CF covering the range with slightly different notation
            all_ranges = [str(cf) for cf in cf_list]
            print(f"FAIL: Component 1 — No CF rule on A2:A101. Found ranges: {all_ranges}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Rule uses COUNTIF-based duplicate detection formula (0.4 points)
    try:
        found_countif_formula = False

        for cf in cf_list:
            for rule in cf.rules:
                # Check for expression/formula type rule
                if rule.type == 'expression' and rule.formula:
                    formula_str = str(rule.formula[0]).upper().replace(' ', '')
                    # The expected formula: COUNTIF($A$2:A2,A2)>1
                    # Accept variants with different anchoring styles
                    if 'COUNTIF' in formula_str and '>1' in formula_str:
                        found_countif_formula = True
                        print(f"  Formula found: {rule.formula[0]}")
                        break
                # Also accept 'duplicateValues' type if LibreOffice uses that
                elif rule.type == 'duplicateValues':
                    found_countif_formula = True
                    print(f"  DuplicateValues rule type found")
                    break
            if found_countif_formula:
                break

        if found_countif_formula:
            print(f"PASS: Component 2 — Duplicate detection formula/rule found (0.4 pts)")
            total_score += 0.4
        else:
            rule_details = []
            for cf in cf_list:
                for rule in cf.rules:
                    rule_details.append(f"type={rule.type}, formula={getattr(rule, 'formula', 'N/A')}")
            print(f"FAIL: Component 2 — No COUNTIF duplicate formula. Rules: {rule_details}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Fill color is pink (0.3 points)
    try:
        found_pink_fill = False

        # Pink color variants (ARGB format)
        pink_colors = {
            'FFFFC0CB',  # standard pink
            'FFFF69B4',  # hot pink
            'FFFFC0CB',  # pink
            'FFFF91A4',  # salmon pink
            'FFFFB6C1',  # light pink
            'FFFF1493',  # deep pink
        }

        for cf in cf_list:
            for rule in cf.rules:
                if hasattr(rule, 'dxf') and rule.dxf and rule.dxf.fill:
                    fill = rule.dxf.fill
                    fill_color = None
                    try:
                        fill_color = fill.fgColor.rgb
                    except:
                        pass
                    if not fill_color:
                        try:
                            fill_color = fill.start_color.rgb
                        except:
                            pass

                    if fill_color:
                        fill_color_upper = str(fill_color).upper()
                        print(f"  Fill color found: {fill_color_upper}")
                        # Check if it's a pink shade
                        # Pink typically has high R, medium-low G, medium-low B
                        if fill_color_upper in pink_colors:
                            found_pink_fill = True
                        elif len(fill_color_upper) == 8:
                            # Parse ARGB and check if it's pinkish
                            try:
                                r = int(fill_color_upper[2:4], 16)
                                g = int(fill_color_upper[4:6], 16)
                                b = int(fill_color_upper[6:8], 16)
                                # Pink: high red (>180), green and blue moderate but not too high
                                # FFC0CB = R:255 G:192 B:203 (classic pink)
                                if r >= 180 and g < r and b < r and (g > 50 or b > 50):
                                    found_pink_fill = True
                                    print(f"  Recognized as pink: R={r} G={g} B={b}")
                            except:
                                pass

        if found_pink_fill:
            print(f"PASS: Component 3 — Pink fill color applied (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Pink fill not found in CF rules")
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
