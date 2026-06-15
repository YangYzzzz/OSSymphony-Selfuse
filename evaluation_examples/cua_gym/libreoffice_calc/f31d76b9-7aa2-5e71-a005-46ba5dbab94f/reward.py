"""
Reward Script: Add formula-based conditional formatting to highlight 'Complete' rows
Task ID: calc_fmt_conditional_formula_based_081
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.4 pts): Formula-based CF rule exists on A2:E20 with =$E2="Complete"
  - Component 2 (0.4 pts): CF rule fill uses light gray background #D9D9D9 (ARGB: FFD9D9D9)
  - Component 3 (0.2 pts): Exactly one CF rule exists on the sheet (no extra rules)
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_fmt_conditional_formula_based_081'

EXPECTED_RANGE = 'A2:E20'
EXPECTED_FORMULA = '=$E2="Complete"'
EXPECTED_FILL_COLOR = 'FFD9D9D9'


def normalize_formula(formula_str):
    """Normalize formula for comparison: strip spaces, lowercase, strip surrounding quotes."""
    return formula_str.strip().upper().replace(' ', '')


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

    # Verify sheet 'Project Tasks' exists
    if 'Project Tasks' not in wb.sheetnames:
        print("FAIL: Sheet 'Project Tasks' not found in workbook")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    ws = wb['Project Tasks']

    # Collect all CF rules from the sheet
    # Note: iterating ws.conditional_formatting yields ConditionalFormatting objects;
    # use cf.sqref to get the actual range string (not str(cf) which includes class name)
    all_rules = []
    for cf in ws.conditional_formatting:
        range_str = str(cf.sqref)
        for rule in cf.rules:
            all_rules.append((range_str, rule))

    # Component 1: A formula-based CF rule exists on A2:E20 with formula =$E2="Complete" (0.4 points)
    try:
        found_formula_rule = False
        target_rule = None
        target_range_str = None

        for range_str, rule in all_rules:
            # Check if this rule covers A2:E20
            range_matches = (range_str.upper().replace(' ', '') == EXPECTED_RANGE.upper())
            # Check rule type is expression/formula
            is_formula_rule = (rule.type == 'expression')
            # Check formula content
            if rule.formula and len(rule.formula) > 0:
                actual_formula = normalize_formula(rule.formula[0])
                expected_normalized = normalize_formula(EXPECTED_FORMULA)
                # Also accept =$E2='Complete' with single quotes
                formula_matches = (actual_formula == expected_normalized)
            else:
                formula_matches = False

            if range_matches and is_formula_rule and formula_matches:
                found_formula_rule = True
                target_rule = rule
                target_range_str = range_str
                break

        if found_formula_rule:
            print(f"PASS: Component 1 — Formula-based CF rule found on '{target_range_str}' with formula '{target_rule.formula[0]}' (0.4 pts)")
            total_score += 0.4
        else:
            # Provide diagnostic info
            if len(all_rules) == 0:
                print(f"FAIL: Component 1 — No conditional formatting rules found on sheet 'Project Tasks'")
            else:
                for range_str, rule in all_rules:
                    formula_str = rule.formula[0] if rule.formula else 'None'
                    print(f"FAIL: Component 1 — Found rule: range='{range_str}', type='{rule.type}', formula='{formula_str}'")
                    print(f"  Expected range='{EXPECTED_RANGE}', type='expression', formula='{EXPECTED_FORMULA}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The CF rule uses light gray fill #D9D9D9 (ARGB: FFD9D9D9) (0.4 points)
    try:
        if target_rule is not None:
            # Check the differential format fill color
            fill_color_ok = False
            if hasattr(target_rule, 'dxf') and target_rule.dxf is not None:
                dxf = target_rule.dxf
                if dxf.fill is not None:
                    try:
                        fgcolor_rgb = dxf.fill.fgColor.rgb
                        # Accept both with and without alpha prefix, case insensitive
                        fgcolor_upper = fgcolor_rgb.upper()
                        if fgcolor_upper == EXPECTED_FILL_COLOR.upper():
                            fill_color_ok = True
                        # Also accept 6-char version D9D9D9 (without alpha)
                        elif fgcolor_upper.endswith('D9D9D9'):
                            fill_color_ok = True
                    except Exception:
                        pass

                if fill_color_ok:
                    print(f"PASS: Component 2 — CF rule fill color is #{EXPECTED_FILL_COLOR} (light gray) (0.4 pts)")
                    total_score += 0.4
                else:
                    actual_color = 'unknown'
                    try:
                        actual_color = dxf.fill.fgColor.rgb if dxf.fill else 'no fill'
                    except Exception:
                        pass
                    print(f"FAIL: Component 2 — Expected fill color #{EXPECTED_FILL_COLOR}, found: #{actual_color}")
            else:
                print(f"FAIL: Component 2 — CF rule has no differential format (dxf) or no fill defined")
        else:
            print(f"FAIL: Component 2 — No valid formula CF rule found to check fill color")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Exactly one CF rule exists on the sheet (no extra rules added) (0.2 points)
    try:
        total_rules_count = len(all_rules)
        if total_rules_count == 1:
            print(f"PASS: Component 3 — Exactly 1 CF rule on the sheet (0.2 pts)")
            total_score += 0.2
        elif total_rules_count == 0:
            print(f"FAIL: Component 3 — No CF rules found (0 rules, expected 1)")
        else:
            print(f"FAIL: Component 3 — Expected exactly 1 CF rule, found {total_rules_count} rules")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
