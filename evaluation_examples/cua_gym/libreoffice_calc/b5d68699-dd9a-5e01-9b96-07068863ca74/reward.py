"""
Reward Script: Conditional formatting to highlight max value per row with gold background
Task ID: calc_gcv_041
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Conditional formatting rule exists
  Component 2 (0.3): Rule covers B2:F20 with MAX-based formula expression
  Component 3 (0.4): Fill color is gold (#FFD700)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_041'


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

    # Collect all conditional formatting rules
    cf_list = list(ws.conditional_formatting)

    # Component 1: At least one conditional formatting rule exists (0.3 points)
    # Initial file has 0 rules; golden has 1+ rule. This checks the task-introduced change.
    try:
        if len(cf_list) > 0:
            print(f"PASS: Component 1 — Found {len(cf_list)} conditional formatting rule(s) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No conditional formatting rules found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Rule covers B2:F20 with a MAX-based formula expression (0.3 points)
    # The golden rule uses formula: B2=MAX($B2:$F2) applied to B2:F20
    try:
        found_correct_rule = False
        for cf in cf_list:
            cf_range = str(cf).strip()
            for rule in cf.rules:
                # Check it is a formula/expression type rule
                if rule.type != 'expression':
                    continue
                # Check formula references MAX
                formula_strs = rule.formula if rule.formula else []
                has_max = False
                for f in formula_strs:
                    if 'MAX' in str(f).upper():
                        has_max = True
                        break
                if not has_max:
                    continue
                # Check range covers B2:F20
                # Accept various representations: "B2:F20", etc.
                if 'B2' in cf_range and 'F20' in cf_range:
                    found_correct_rule = True
                    print(f"PASS: Component 2 — Rule on range '{cf_range}' with MAX formula: {formula_strs} (0.3 pts)")
                    break
            if found_correct_rule:
                break

        if found_correct_rule:
            total_score += 0.3
        else:
            # Print diagnostic info
            for cf in cf_list:
                for rule in cf.rules:
                    print(f"  DEBUG: Range={cf}, Type={rule.type}, Formula={rule.formula}")
            print(f"FAIL: Component 2 — No rule found covering B2:F20 with MAX formula")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Fill color is gold #FFD700 (ARGB: FFFFD700) (0.4 points)
    # The golden rule applies a gold PatternFill.
    try:
        found_gold_fill = False
        for cf in cf_list:
            for rule in cf.rules:
                if rule.dxf and rule.dxf.fill:
                    fill = rule.dxf.fill
                    fg_rgb = None
                    try:
                        fg_rgb = fill.fgColor.rgb if fill.fgColor else None
                    except Exception:
                        pass
                    bg_rgb = None
                    try:
                        bg_rgb = fill.bgColor.rgb if fill.bgColor else None
                    except Exception:
                        pass

                    # Check if either fg or bg color is gold
                    gold_variants = ['FFFFD700', 'FFD700']
                    for color_val in [fg_rgb, bg_rgb]:
                        if color_val and str(color_val).upper().replace('00FFD700', 'FFFFD700') in ['FFFFD700']:
                            found_gold_fill = True
                            break
                        if color_val and str(color_val).upper() in gold_variants:
                            found_gold_fill = True
                            break

                    # Also check patternType is solid
                    if found_gold_fill and fill.patternType != 'solid':
                        print(f"  WARN: Fill pattern is '{fill.patternType}', expected 'solid'")

                    if found_gold_fill:
                        print(f"PASS: Component 3 — Gold fill color FFFFD700 found with pattern={fill.patternType} (0.4 pts)")
                        break
            if found_gold_fill:
                break

        if found_gold_fill:
            total_score += 0.4
        else:
            # Diagnostic
            for cf in cf_list:
                for rule in cf.rules:
                    if rule.dxf and rule.dxf.fill:
                        fill = rule.dxf.fill
                        try:
                            print(f"  DEBUG: fgColor={fill.fgColor.rgb}, bgColor={fill.bgColor.rgb}, pattern={fill.patternType}")
                        except Exception:
                            print(f"  DEBUG: fill object exists but color access failed")
            print(f"FAIL: Component 3 — Gold fill color FFFFD700 not found in any conditional formatting rule")
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
