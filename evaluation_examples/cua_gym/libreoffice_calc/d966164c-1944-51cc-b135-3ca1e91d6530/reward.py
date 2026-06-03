"""
Reward Script: Highlight overdue and upcoming performance reviews with conditional formatting
Task ID: calc_hr_conditional_overdue_reviews_016
Domain: libreoffice_calc

Scoring:
- Component 1: CF rule exists on Reviews!A2:E98 (0.3 pts)
- Component 2: Overdue rule correct — formula AND(D2<TODAY(),E2="Pending"), red fill #FF0000, white font #FFFFFF (0.4 pts)
- Component 3: Due-soon rule correct — formula AND(D2>=TODAY(),D2<=TODAY()+7,E2="Pending"), yellow fill #FFFF00 (0.3 pts)
Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_hr_conditional_overdue_reviews_016'


def normalize_formula(f):
    """Normalize formula string for comparison: strip quotes, uppercase, remove spaces."""
    return f.upper().replace(' ', '').replace('"', '"').replace('"', '"')


def formulas_match(actual, expected):
    """Check if a formula string matches expected (case-insensitive, space-insensitive)."""
    a = actual.upper().replace(' ', '').replace('"', '"').replace('"', '"').replace("'", '"')
    e = expected.upper().replace(' ', '').replace('"', '"').replace('"', '"').replace("'", '"')
    return a == e


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

    # Gate: check that 'Reviews' sheet exists
    if 'Reviews' not in wb.sheetnames:
        print("FAIL: 'Reviews' sheet not found in workbook")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    ws = wb['Reviews']

    # Component 1: Conditional formatting rules exist on A2:E98 (0.3 points)
    # This FAILS on initial (no CF rules) and PASSES on golden (CF rules present)
    try:
        cf_rules_found = False
        target_range_key = None
        target_rules = []

        # Look for CF rules applied to A2:E98 (or containing that range)
        for cf_range, rules in ws.conditional_formatting._cf_rules.items():
            cf_str = str(cf_range)
            # Check if this CF range covers A2:E98
            if 'A2:E98' in cf_str or 'A2' in cf_str:
                cf_rules_found = len(rules) >= 1
                target_range_key = cf_range
                target_rules = list(rules)
                break

        if cf_rules_found and len(target_rules) >= 2:
            print(f"PASS: Component 1 — CF rules found on range covering A2:E98, {len(target_rules)} rule(s) present (0.3 pts)")
            total_score += 0.3
        elif cf_rules_found and len(target_rules) >= 1:
            print(f"PARTIAL: Component 1 — CF rules found on range, but only {len(target_rules)} rule (expected 2); awarding partial 0.15 pts")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — No conditional formatting rules found on Reviews sheet (expected rules on A2:E98)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Overdue rule — formula AND(D2<TODAY(),E2="Pending"), red fill FFFF0000, white font FFFFFFFF (0.4 points)
    # This FAILS on initial (no CF rules) and PASSES on golden
    try:
        overdue_formula_ok = False
        overdue_fill_ok = False
        overdue_font_ok = False

        expected_overdue_formula = 'AND(D2<TODAY(),E2="Pending")'

        for cf_range, rules in ws.conditional_formatting._cf_rules.items():
            for rule in rules:
                if rule.type == 'expression' and rule.formula:
                    formula_str = rule.formula[0] if rule.formula else ''
                    if formulas_match(formula_str, expected_overdue_formula):
                        overdue_formula_ok = True
                        # Check fill color: red FFFF0000
                        if rule.dxf and rule.dxf.fill and rule.dxf.fill.fgColor:
                            fill_rgb = rule.dxf.fill.fgColor.rgb
                            # Accept FFFF0000 (8-char ARGB) or FF0000 (6-char)
                            if fill_rgb in ('FFFF0000', '00FF0000'):
                                overdue_fill_ok = True
                            else:
                                print(f"  INFO: overdue rule fill color = {fill_rgb} (expected FFFF0000)")
                        # Check font color: white FFFFFFFF
                        if rule.dxf and rule.dxf.font and rule.dxf.font.color:
                            font_rgb = rule.dxf.font.color.rgb
                            if font_rgb in ('FFFFFFFF', '00FFFFFF'):
                                overdue_font_ok = True
                            else:
                                print(f"  INFO: overdue rule font color = {font_rgb} (expected FFFFFFFF)")
                        break

        comp2_score = 0.0
        if overdue_formula_ok:
            comp2_score += 0.2
            print(f"  PASS: Overdue formula correct: AND(D2<TODAY(),E2=\"Pending\")")
        else:
            print(f"  FAIL: Overdue formula not found (expected AND(D2<TODAY(),E2=\"Pending\"))")

        if overdue_fill_ok:
            comp2_score += 0.1
            print(f"  PASS: Overdue fill color is red (#FF0000 / FFFF0000)")
        else:
            if overdue_formula_ok:
                print(f"  FAIL: Overdue fill color incorrect (expected red FFFF0000)")

        if overdue_font_ok:
            comp2_score += 0.1
            print(f"  PASS: Overdue font color is white (#FFFFFF / FFFFFFFF)")
        else:
            if overdue_formula_ok:
                print(f"  FAIL: Overdue font color incorrect (expected white FFFFFFFF)")

        if comp2_score >= 0.4:
            print(f"PASS: Component 2 — Overdue rule fully correct ({comp2_score} pts)")
        elif comp2_score > 0:
            print(f"PARTIAL: Component 2 — Overdue rule partially correct ({comp2_score} pts)")
        else:
            print(f"FAIL: Component 2 — Overdue rule not found or incorrect (0.0 pts)")

        total_score += comp2_score

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Due-soon rule — formula AND(D2>=TODAY(),D2<=TODAY()+7,E2="Pending"), yellow fill FFFFFF00 (0.3 points)
    # This FAILS on initial (no CF rules) and PASSES on golden
    try:
        duesoon_formula_ok = False
        duesoon_fill_ok = False

        expected_duesoon_formula = 'AND(D2>=TODAY(),D2<=TODAY()+7,E2="Pending")'

        for cf_range, rules in ws.conditional_formatting._cf_rules.items():
            for rule in rules:
                if rule.type == 'expression' and rule.formula:
                    formula_str = rule.formula[0] if rule.formula else ''
                    if formulas_match(formula_str, expected_duesoon_formula):
                        duesoon_formula_ok = True
                        # Check fill color: yellow FFFFFF00
                        if rule.dxf and rule.dxf.fill and rule.dxf.fill.fgColor:
                            fill_rgb = rule.dxf.fill.fgColor.rgb
                            if fill_rgb in ('FFFFFF00', '00FFFF00'):
                                duesoon_fill_ok = True
                            else:
                                print(f"  INFO: due-soon rule fill color = {fill_rgb} (expected FFFFFF00)")
                        break

        comp3_score = 0.0
        if duesoon_formula_ok:
            comp3_score += 0.2
            print(f"  PASS: Due-soon formula correct: AND(D2>=TODAY(),D2<=TODAY()+7,E2=\"Pending\")")
        else:
            print(f"  FAIL: Due-soon formula not found (expected AND(D2>=TODAY(),D2<=TODAY()+7,E2=\"Pending\"))")

        if duesoon_fill_ok:
            comp3_score += 0.1
            print(f"  PASS: Due-soon fill color is yellow (#FFFF00 / FFFFFF00)")
        else:
            if duesoon_formula_ok:
                print(f"  FAIL: Due-soon fill color incorrect (expected yellow FFFFFF00)")

        if comp3_score >= 0.3:
            print(f"PASS: Component 3 — Due-soon rule fully correct ({comp3_score} pts)")
        elif comp3_score > 0:
            print(f"PARTIAL: Component 3 — Due-soon rule partially correct ({comp3_score} pts)")
        else:
            print(f"FAIL: Component 3 — Due-soon rule not found or incorrect (0.0 pts)")

        total_score += comp3_score

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Bonus check: priority ordering (overdue rule must have lower priority number = higher precedence)
    # This is informational only; does not add to score but validates ordering
    try:
        overdue_priority = None
        duesoon_priority = None
        expected_overdue = 'AND(D2<TODAY(),E2="Pending")'
        expected_duesoon = 'AND(D2>=TODAY(),D2<=TODAY()+7,E2="Pending")'

        for cf_range, rules in ws.conditional_formatting._cf_rules.items():
            for rule in rules:
                if rule.type == 'expression' and rule.formula:
                    f = rule.formula[0] if rule.formula else ''
                    if formulas_match(f, expected_overdue):
                        overdue_priority = rule.priority
                    elif formulas_match(f, expected_duesoon):
                        duesoon_priority = rule.priority

        if overdue_priority is not None and duesoon_priority is not None:
            if overdue_priority < duesoon_priority:
                print(f"INFO: Priority ordering correct — overdue (priority={overdue_priority}) takes precedence over due-soon (priority={duesoon_priority})")
            else:
                print(f"INFO: Priority ordering may be wrong — overdue priority={overdue_priority}, due-soon priority={duesoon_priority} (overdue should have lower number)")
    except Exception as e:
        print(f"INFO: Could not verify priority ordering: {e}")

    final_score = min(total_score, 1.0)
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
