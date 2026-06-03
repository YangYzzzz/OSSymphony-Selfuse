"""
Reward Script: Succession Planning Matrix Setup
Task ID: calc_hr_succession_planning_068
Domain: libreoffice_calc
Scoring:
  - Data validation on D2:D28 (Readiness dropdown): 0.25 pts
  - Data validation on F2:F28 (Readiness S2 dropdown): 0.25 pts
  - Data validation on G2:G28 (Risk Level dropdown): 0.20 pts
  - Conditional formatting: Critical+No Successor -> red fill, white font: 0.15 pts
  - Conditional formatting: Critical+covered -> amber fill: 0.10 pts
  - Conditional formatting: Ready Now -> green fill: 0.05 pts
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_hr_succession_planning_068'


def normalize_sqref(sqref):
    """Normalize sqref to a set of range strings for comparison."""
    if sqref is None:
        return set()
    s = str(sqref).strip()
    return set(s.split())


def check_data_validation(ws, expected_range, expected_formula1_options):
    """
    Check if a data validation with list type exists covering the expected range,
    with the expected list options (as a comma-separated string).
    Returns True if found, False otherwise.
    """
    validations = ws.data_validations.dataValidation
    expected_range_normalized = expected_range.replace(' ', '').upper()

    for dv in validations:
        if dv.type != 'list':
            continue
        # Check sqref covers the expected range
        sqref_str = str(dv.sqref).replace(' ', '').upper()
        if expected_range_normalized not in sqref_str and sqref_str not in expected_range_normalized:
            # Try splitting by space (multiple ranges in sqref)
            sqref_parts = str(dv.sqref).replace(' ', ',').upper()
            if expected_range_normalized not in sqref_parts:
                continue

        # Check formula1 contains the expected options
        # formula1 is typically like '"Ready Now,1-2 Years,3+ Years,No Successor"'
        if dv.formula1 is None:
            continue
        formula_str = dv.formula1.strip('"').strip("'").strip()
        # Parse actual options from formula
        actual_options = [o.strip() for o in formula_str.split(',')]
        # Parse expected options
        expected_options = [o.strip() for o in expected_formula1_options.split(',')]

        if actual_options == expected_options:
            return True

    return False


def check_cf_rule_exists(ws, formula_fragment, fill_color_argb=None, font_color_argb=None):
    """
    Check if a conditional formatting rule exists on the worksheet with the given formula fragment.
    Optionally check that the fill color and font color match.
    Returns True if matching rule found, False otherwise.
    """
    for cf_range in ws.conditional_formatting:
        rules = ws.conditional_formatting[cf_range]
        for rule in rules:
            if rule.type != 'expression':
                continue
            if not hasattr(rule, 'formula') or not rule.formula:
                continue
            # Check if formula fragment is in any of the rule formulas
            formula_match = any(formula_fragment.upper() in f.upper() for f in rule.formula)
            if not formula_match:
                continue

            # If fill color check required
            if fill_color_argb is not None:
                if not (hasattr(rule, 'dxf') and rule.dxf and rule.dxf.fill):
                    continue
                try:
                    actual_fill = rule.dxf.fill.fgColor.rgb
                    if actual_fill.upper() != fill_color_argb.upper():
                        continue
                except Exception:
                    continue

            # If font color check required
            if font_color_argb is not None:
                if not (hasattr(rule, 'dxf') and rule.dxf and rule.dxf.font):
                    continue
                try:
                    actual_font_color = rule.dxf.font.color.rgb
                    if actual_font_color.upper() != font_color_argb.upper():
                        continue
                except Exception:
                    continue

            return True

    return False


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

    # Check sheet exists
    if 'Succession Plan' not in wb.sheetnames:
        print("CRITICAL: Sheet 'Succession Plan' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Succession Plan']

    # Component 1: Data validation on D2:D28 — Readiness dropdown (0.25 points)
    # Expected: 'Ready Now,1-2 Years,3+ Years,No Successor'
    try:
        dv_d_found = False
        expected_d_options = 'Ready Now,1-2 Years,3+ Years,No Successor'
        for dv in ws.data_validations.dataValidation:
            if dv.type != 'list':
                continue
            sqref_str = str(dv.sqref).upper()
            if 'D2:D28' not in sqref_str and 'D2' not in sqref_str:
                continue
            if dv.formula1 is None:
                continue
            formula_str = dv.formula1.strip('"').strip("'").strip()
            actual_options = [o.strip() for o in formula_str.split(',')]
            expected_options = [o.strip() for o in expected_d_options.split(',')]
            if actual_options == expected_options:
                dv_d_found = True
                break

        if dv_d_found:
            print(f"PASS: Component 1 — D2:D28 Readiness dropdown validated correctly (0.25 pts)")
            total_score += 0.25
        else:
            # Try a more lenient check: does D column have any list validation?
            for dv in ws.data_validations.dataValidation:
                if dv.type == 'list' and dv.formula1:
                    sqref_str = str(dv.sqref).upper()
                    formula_str = dv.formula1.strip('"').strip("'").strip()
                    if 'D2' in sqref_str and 'NO SUCCESSOR' in formula_str.upper():
                        print(f"PASS: Component 1 — D2:D28 Readiness dropdown found (partial match, formula={dv.formula1}) (0.25 pts)")
                        total_score += 0.25
                        dv_d_found = True
                        break
            if not dv_d_found:
                print(f"FAIL: Component 1 — D2:D28 Readiness dropdown not found or incorrect options")
                # Show what validations exist for debugging
                for dv in ws.data_validations.dataValidation:
                    print(f"  Found DV: type={dv.type}, sqref={dv.sqref}, formula1={dv.formula1}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Data validation on F2:F28 — Readiness S2 dropdown (0.25 points)
    # Expected: 'Ready Now,1-2 Years,3+ Years,No Successor,N/A'
    try:
        dv_f_found = False
        expected_f_options = 'Ready Now,1-2 Years,3+ Years,No Successor,N/A'
        for dv in ws.data_validations.dataValidation:
            if dv.type != 'list':
                continue
            sqref_str = str(dv.sqref).upper()
            if 'F2:F28' not in sqref_str and 'F2' not in sqref_str:
                continue
            if dv.formula1 is None:
                continue
            formula_str = dv.formula1.strip('"').strip("'").strip()
            actual_options = [o.strip() for o in formula_str.split(',')]
            expected_options = [o.strip() for o in expected_f_options.split(',')]
            if actual_options == expected_options:
                dv_f_found = True
                break

        if dv_f_found:
            print(f"PASS: Component 2 — F2:F28 Readiness(S2) dropdown validated correctly (0.25 pts)")
            total_score += 0.25
        else:
            # Lenient check
            for dv in ws.data_validations.dataValidation:
                if dv.type == 'list' and dv.formula1:
                    sqref_str = str(dv.sqref).upper()
                    formula_str = dv.formula1.strip('"').strip("'").strip()
                    if 'F2' in sqref_str and 'N/A' in formula_str.upper():
                        print(f"PASS: Component 2 — F2:F28 Readiness(S2) dropdown found (partial match) (0.25 pts)")
                        total_score += 0.25
                        dv_f_found = True
                        break
            if not dv_f_found:
                print(f"FAIL: Component 2 — F2:F28 Readiness(S2) dropdown not found or incorrect options")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Data validation on G2:G28 — Risk Level dropdown (0.20 points)
    # Expected: 'Critical,High,Medium,Low'
    try:
        dv_g_found = False
        expected_g_options = 'Critical,High,Medium,Low'
        for dv in ws.data_validations.dataValidation:
            if dv.type != 'list':
                continue
            sqref_str = str(dv.sqref).upper()
            if 'G2:G28' not in sqref_str and 'G2' not in sqref_str:
                continue
            if dv.formula1 is None:
                continue
            formula_str = dv.formula1.strip('"').strip("'").strip()
            actual_options = [o.strip() for o in formula_str.split(',')]
            expected_options = [o.strip() for o in expected_g_options.split(',')]
            if actual_options == expected_options:
                dv_g_found = True
                break

        if dv_g_found:
            print(f"PASS: Component 3 — G2:G28 Risk Level dropdown validated correctly (0.20 pts)")
            total_score += 0.20
        else:
            # Lenient check
            for dv in ws.data_validations.dataValidation:
                if dv.type == 'list' and dv.formula1:
                    sqref_str = str(dv.sqref).upper()
                    formula_str = dv.formula1.strip('"').strip("'").strip()
                    if 'G2' in sqref_str and 'CRITICAL' in formula_str.upper():
                        print(f"PASS: Component 3 — G2:G28 Risk Level dropdown found (partial match) (0.20 pts)")
                        total_score += 0.20
                        dv_g_found = True
                        break
            if not dv_g_found:
                print(f"FAIL: Component 3 — G2:G28 Risk Level dropdown not found or incorrect options")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Conditional formatting — Critical + No Successor -> red fill, white font (0.15 points)
    # Formula: AND($G2="Critical",$D2="No Successor") -> fill #FF0000, font #FFFFFF
    try:
        cf_critical_no_successor_found = False
        for cf_range in ws.conditional_formatting:
            rules = ws.conditional_formatting[cf_range]
            for rule in rules:
                if rule.type != 'expression':
                    continue
                if not hasattr(rule, 'formula') or not rule.formula:
                    continue
                formula_str = rule.formula[0].upper()
                # Check formula references Critical and No Successor
                if 'CRITICAL' not in formula_str or 'NO SUCCESSOR' not in formula_str:
                    continue
                # Check fill color is red (#FF0000 as ARGB = FFFF0000)
                if not (hasattr(rule, 'dxf') and rule.dxf and rule.dxf.fill):
                    continue
                try:
                    fill_color = rule.dxf.fill.fgColor.rgb.upper()
                    if 'FF0000' not in fill_color:
                        continue
                except Exception:
                    continue
                # Also check for white font (bonus reporting, but not required to pass this component)
                has_white_font = False
                if rule.dxf.font:
                    try:
                        font_color = rule.dxf.font.color.rgb.upper()
                        has_white_font = ('FFFFFF' in font_color)
                    except Exception:
                        pass
                if has_white_font:
                    print(f"PASS: Component 4 — Critical+No Successor CF rule: red fill + white font (0.15 pts)")
                else:
                    print(f"PASS: Component 4 — Critical+No Successor CF rule: red fill found (font color not checked) (0.15 pts)")
                cf_critical_no_successor_found = True
                break
            if cf_critical_no_successor_found:
                break

        if cf_critical_no_successor_found:
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Critical+No Successor conditional formatting rule not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Conditional formatting — Critical + covered -> amber fill #FFC000 (0.10 points)
    # Formula: AND($G2="Critical",$D2<>"No Successor") -> fill #FFC000
    try:
        cf_critical_covered_found = False
        for cf_range in ws.conditional_formatting:
            rules = ws.conditional_formatting[cf_range]
            for rule in rules:
                if rule.type != 'expression':
                    continue
                if not hasattr(rule, 'formula') or not rule.formula:
                    continue
                formula_str = rule.formula[0].upper()
                # Check formula references Critical and has <> "No Successor" (or just Critical without No Successor)
                if 'CRITICAL' not in formula_str:
                    continue
                # Must have the "covered" variant (with <> condition or without "No Successor")
                # The formula should have <> for "not equal"
                if '<>' not in formula_str and 'NO SUCCESSOR' in formula_str:
                    continue  # This is the "no successor" rule, not the "covered" rule
                if 'NO SUCCESSOR' in formula_str and '<>' not in formula_str:
                    continue
                # Ensure it's not the "No Successor" rule (which uses = not <>)
                # Check fill color is amber (#FFC000 as ARGB = FFFFC000)
                if not (hasattr(rule, 'dxf') and rule.dxf and rule.dxf.fill):
                    continue
                try:
                    fill_color = rule.dxf.fill.fgColor.rgb.upper()
                    if 'FFC000' not in fill_color:
                        continue
                except Exception:
                    continue
                cf_critical_covered_found = True
                print(f"PASS: Component 5 — Critical+covered CF rule: amber fill (#FFC000) (0.10 pts)")
                break
            if cf_critical_covered_found:
                break

        if cf_critical_covered_found:
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Critical+covered (amber) conditional formatting rule not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Conditional formatting — Ready Now -> green fill #70AD47 (0.05 points)
    # Formula: $D2="Ready Now" -> fill #70AD47
    try:
        cf_ready_now_found = False
        for cf_range in ws.conditional_formatting:
            rules = ws.conditional_formatting[cf_range]
            for rule in rules:
                if rule.type != 'expression':
                    continue
                if not hasattr(rule, 'formula') or not rule.formula:
                    continue
                formula_str = rule.formula[0].upper()
                if 'READY NOW' not in formula_str:
                    continue
                # Check fill color is green (#70AD47 as ARGB = FF70AD47)
                if not (hasattr(rule, 'dxf') and rule.dxf and rule.dxf.fill):
                    continue
                try:
                    fill_color = rule.dxf.fill.fgColor.rgb.upper()
                    if '70AD47' not in fill_color:
                        continue
                except Exception:
                    continue
                cf_ready_now_found = True
                print(f"PASS: Component 6 — Ready Now CF rule: green fill (#70AD47) (0.05 pts)")
                break
            if cf_ready_now_found:
                break

        if cf_ready_now_found:
            total_score += 0.05
        else:
            print(f"FAIL: Component 6 — Ready Now (green) conditional formatting rule not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

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
