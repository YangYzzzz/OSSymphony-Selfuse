"""
Reward Script: Apply conditional formatting with 3-color scale to salary data
Task ID: calc_hr_037
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.35): Conditional formatting rule exists on range C2:C21
  - Component 2 (0.30): Rule is a 3-color scale (colorScale type with 3 colors)
  - Component 3 (0.35): Colors match red/yellow/green pattern for min/mid/max
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_hr_037'


def persist_app_state(domain: str):
    """Attempt to save any unsaved GUI state."""
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
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check that SalaryMap sheet exists
    if 'SalaryMap' not in wb.sheetnames:
        print("FAIL: Sheet 'SalaryMap' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['SalaryMap']

    # Component 1: Conditional formatting rule exists targeting C2:C21 (0.35 points)
    # This should FAIL on initial (no CF rules) and PASS on golden
    try:
        cf_rules_list = list(ws.conditional_formatting)
        has_cf_on_salary_range = False
        matching_cf = None

        for cf in cf_rules_list:
            # Check if the range covers C2:C21 (the salary cells)
            cf_range_str = str(cf)
            # The range string from openpyxl looks like "<ConditionalFormatting C2:C21>"
            if 'C2' in cf_range_str and 'C21' in cf_range_str:
                has_cf_on_salary_range = True
                matching_cf = cf
                break

        if has_cf_on_salary_range:
            print(f"PASS: Component 1 -- Conditional formatting found on salary range C2:C21 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- No conditional formatting found on C2:C21. Found {len(cf_rules_list)} CF rules total.")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: The rule is a colorScale type with exactly 3 colors (0.30 points)
    # This should FAIL on initial (no rules at all) and PASS on golden
    try:
        color_scale_rule = None
        if matching_cf is not None:
            for rule in matching_cf.rules:
                if rule.type == 'colorScale' and hasattr(rule, 'colorScale') and rule.colorScale is not None:
                    cs = rule.colorScale
                    if len(cs.color) == 3:
                        color_scale_rule = rule
                        break

        if color_scale_rule is not None:
            print(f"PASS: Component 2 -- 3-color scale rule found (0.30 pts)")
            total_score += 0.30
        else:
            if matching_cf is not None:
                rule_types = [r.type for r in matching_cf.rules]
                print(f"FAIL: Component 2 -- Expected 3-color scale rule, found rule types: {rule_types}")
            else:
                print(f"FAIL: Component 2 -- No matching CF to inspect (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Color scale uses red(min)/yellow(mid)/green(max) pattern (0.35 points)
    # Verify the CFVO types are min/percentile/max and colors approximate red/yellow/green
    try:
        if color_scale_rule is not None:
            cs = color_scale_rule.colorScale
            cfvo_types = [(v.type, v.val) for v in cs.cfvo]

            # Check CFVO structure: min, percentile(50), max
            cfvo_ok = (
                len(cs.cfvo) == 3
                and cs.cfvo[0].type == 'min'
                and cs.cfvo[1].type == 'percentile'
                and cs.cfvo[2].type == 'max'
            )

            # Check colors are approximately red, yellow, green
            # Extract RGB values from color objects
            colors_rgb = []
            for c in cs.color:
                rgb_str = c.rgb  # ARGB like "FFF8696B"
                if rgb_str and len(rgb_str) == 8:
                    r = int(rgb_str[2:4], 16)
                    g = int(rgb_str[4:6], 16)
                    b = int(rgb_str[6:8], 16)
                    colors_rgb.append((r, g, b))
                else:
                    colors_rgb.append(None)

            # Red-ish: high R, low G and B relative to R
            # Yellow-ish: high R and G, low B
            # Green-ish: high G, lower R
            color_ok = False
            if len(colors_rgb) == 3 and all(c is not None for c in colors_rgb):
                r0, g0, b0 = colors_rgb[0]  # should be reddish
                r1, g1, b1 = colors_rgb[1]  # should be yellowish
                r2, g2, b2 = colors_rgb[2]  # should be greenish

                is_reddish = r0 > 150 and r0 > g0
                is_yellowish = r1 > 150 and g1 > 150 and b1 < 150
                is_greenish = g2 > 100 and g2 > r2

                color_ok = is_reddish and is_yellowish and is_greenish
                print(f"  Color 0 (min): RGB=({r0},{g0},{b0}) reddish={is_reddish}")
                print(f"  Color 1 (mid): RGB=({r1},{g1},{b1}) yellowish={is_yellowish}")
                print(f"  Color 2 (max): RGB=({r2},{g2},{b2}) greenish={is_greenish}")

            if cfvo_ok and color_ok:
                print(f"PASS: Component 3 -- Red/Yellow/Green color scale with min/percentile/max (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 3 -- CFVO structure ok={cfvo_ok}, colors ok={color_ok}")
                print(f"  CFVO: {cfvo_types}")
        else:
            print(f"FAIL: Component 3 -- No color scale rule to inspect (depends on Component 2)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
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
