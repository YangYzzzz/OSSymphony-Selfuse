"""
Reward Script: Conditional formatting on defect rate column
Task ID: calc_ops_023
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): Conditional formatting rules exist on D2:D6
  Component 2 (0.2): Green rule for < 1% (0.01)
  Component 3 (0.2): Yellow rule for 1%-3% (between 0.01 and 0.03)
  Component 4 (0.2): Red rule for > 3% (0.03)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ops_023'


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

    # Precondition: QC sheet must exist
    if 'QC' not in wb.sheetnames:
        print("FAIL: 'QC' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['QC']

    # Collect all conditional formatting rules that apply to D2:D6 range
    cf_rules_on_d = []
    for cf in ws.conditional_formatting:
        range_str = str(cf)
        # Check if the conditional formatting covers D2:D6
        if 'D2' in range_str and 'D6' in range_str:
            for rule in cf.rules:
                cf_rules_on_d.append(rule)

    # Component 1: At least 3 conditional formatting rules exist on D2:D6 (0.4 points)
    try:
        if len(cf_rules_on_d) >= 3:
            print(f"PASS: Component 1 -- Found {len(cf_rules_on_d)} conditional formatting rules on D2:D6 (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- Expected >= 3 CF rules on D2:D6, found {len(cf_rules_on_d)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Helper: check if a rule matches given criteria
    def find_rule(rules, operator, formula_contains, fill_rgb_prefix):
        """Find a rule matching operator, formula substring, and fill color."""
        for rule in rules:
            op = getattr(rule, 'operator', None)
            if op != operator:
                continue
            # Check formula
            formula_match = False
            if rule.formula:
                for f in rule.formula:
                    if formula_contains in str(f):
                        formula_match = True
                        break
            if not formula_match:
                continue
            # Check fill color
            if rule.dxf and rule.dxf.fill:
                try:
                    fg_rgb = rule.dxf.fill.fgColor.rgb
                    if fg_rgb and fg_rgb.upper().startswith(fill_rgb_prefix.upper()):
                        return True
                except Exception:
                    pass
        return False

    # Component 2: Green rule for < 0.01 (0.2 points)
    # Expected: cellIs, lessThan, formula contains 0.01, fill green (FF00FF00 or similar green)
    try:
        green_found = False
        for rule in cf_rules_on_d:
            op = getattr(rule, 'operator', None)
            if op == 'lessThan' and rule.formula:
                formula_val = str(rule.formula[0]).strip()
                if '0.01' in formula_val:
                    if rule.dxf and rule.dxf.fill:
                        try:
                            fg_rgb = rule.dxf.fill.fgColor.rgb
                            if fg_rgb:
                                fg_upper = fg_rgb.upper()
                                # Check for green: high G, low R/B
                                # Accept FF00FF00, FF00B050, or similar green shades
                                r_val = int(fg_upper[2:4], 16)
                                g_val = int(fg_upper[4:6], 16)
                                b_val = int(fg_upper[6:8], 16)
                                if g_val > 128 and g_val > r_val and g_val > b_val:
                                    green_found = True
                        except Exception:
                            pass
        if green_found:
            print(f"PASS: Component 2 -- Green fill rule for < 0.01 found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- No green fill rule for lessThan 0.01 found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Yellow rule for between 0.01 and 0.03 (0.2 points)
    try:
        yellow_found = False
        for rule in cf_rules_on_d:
            op = getattr(rule, 'operator', None)
            if op == 'between' and rule.formula:
                formulas_str = ' '.join(str(f) for f in rule.formula)
                if '0.01' in formulas_str and '0.03' in formulas_str:
                    if rule.dxf and rule.dxf.fill:
                        try:
                            fg_rgb = rule.dxf.fill.fgColor.rgb
                            if fg_rgb:
                                fg_upper = fg_rgb.upper()
                                r_val = int(fg_upper[2:4], 16)
                                g_val = int(fg_upper[4:6], 16)
                                b_val = int(fg_upper[6:8], 16)
                                # Yellow: high R and G, low B
                                if r_val > 128 and g_val > 128 and b_val < 128:
                                    yellow_found = True
                        except Exception:
                            pass
        if yellow_found:
            print(f"PASS: Component 3 -- Yellow fill rule for between 0.01 and 0.03 found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- No yellow fill rule for between 0.01-0.03 found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Red rule for > 0.03 (0.2 points)
    try:
        red_found = False
        for rule in cf_rules_on_d:
            op = getattr(rule, 'operator', None)
            if op == 'greaterThan' and rule.formula:
                formula_val = str(rule.formula[0]).strip()
                if '0.03' in formula_val:
                    if rule.dxf and rule.dxf.fill:
                        try:
                            fg_rgb = rule.dxf.fill.fgColor.rgb
                            if fg_rgb:
                                fg_upper = fg_rgb.upper()
                                r_val = int(fg_upper[2:4], 16)
                                g_val = int(fg_upper[4:6], 16)
                                b_val = int(fg_upper[6:8], 16)
                                # Red: high R, low G and B
                                if r_val > 128 and r_val > g_val and r_val > b_val:
                                    red_found = True
                        except Exception:
                            pass
        if red_found:
            print(f"PASS: Component 4 -- Red fill rule for > 0.03 found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 -- No red fill rule for greaterThan 0.03 found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
