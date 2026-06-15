"""
Reward Script: Apply 3-color scale conditional formatting on quota attainment percentages
Task ID: calc_sales_043
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): Conditional formatting colorScale exists on range B2:B8
  Component 2 (0.3): Rule is colorScale with 3 stops (min/midpoint/max)
  Component 3 (0.3): Colors are red-yellow-green (low-mid-high)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_sales_043'


def parse_rgb(argb_str):
    """Parse ARGB string to (R, G, B) tuple."""
    s = str(argb_str)
    if len(s) == 8:
        return (int(s[2:4], 16), int(s[4:6], 16), int(s[6:8], 16))
    elif len(s) == 6:
        return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
    return None


def find_color_scale_rules(ws):
    """Find all colorScale conditional formatting rules on the worksheet."""
    results = []
    for cf in ws.conditional_formatting:
        for rule in cf.rules:
            if rule.type == 'colorScale' and rule.colorScale:
                results.append((cf, rule))
    return results


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

    # Precondition: 'Attainment' sheet must exist
    if 'Attainment' not in wb.sheetnames:
        print("FAIL: 'Attainment' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Attainment']
    cs_rules = find_color_scale_rules(ws)

    # Component 1: Conditional formatting colorScale exists on range covering B2:B8 (0.4 points)
    try:
        range_match = [
            (cf, rule) for cf, rule in cs_rules
            if 'B2:B8' in str(cf.sqref) or 'B2' in str(cf.sqref)
        ]
        if len(range_match) > 0:
            print(f"PASS: Component 1 — colorScale conditional formatting on B2:B8 (0.4 pts)")
            total_score += 0.4
        elif len(cs_rules) > 0:
            print(f"FAIL: Component 1 — colorScale found but on wrong range: {cs_rules[0][0].sqref}")
        else:
            print(f"FAIL: Component 1 — No colorScale conditional formatting found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Rule is colorScale with 3 stops (min/midpoint/max) (0.3 points)
    try:
        three_stop_match = [
            (cf, rule) for cf, rule in cs_rules
            if len(rule.colorScale.cfvo) == 3
            and rule.colorScale.cfvo[0].type in ('min', 'num')
            and rule.colorScale.cfvo[2].type in ('max', 'num')
        ]
        if len(three_stop_match) > 0:
            types = [c.type for c in three_stop_match[0][1].colorScale.cfvo]
            print(f"PASS: Component 2 — 3-color scale with types {types} (0.3 pts)")
            total_score += 0.3
        elif len(cs_rules) > 0:
            cfvo_count = len(cs_rules[0][1].colorScale.cfvo)
            print(f"FAIL: Component 2 — colorScale has {cfvo_count} stops (expected 3 with min/*/max)")
        else:
            print(f"FAIL: Component 2 — No colorScale rule found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Colors are red-yellow-green (low-mid-high) (0.3 points)
    try:
        color_match_found = False
        for cf, rule in cs_rules:
            cs = rule.colorScale
            if len(cs.color) == 3:
                rgb1 = parse_rgb(cs.color[0].rgb) if cs.color[0].rgb else None
                rgb2 = parse_rgb(cs.color[1].rgb) if cs.color[1].rgb else None
                rgb3 = parse_rgb(cs.color[2].rgb) if cs.color[2].rgb else None

                if rgb1 and rgb2 and rgb3:
                    # First color should be reddish (R dominant)
                    is_red = rgb1[0] > rgb1[1] and rgb1[0] > rgb1[2]
                    # Second color should be yellowish (R high, G high, B low)
                    is_yellow = rgb2[0] > 150 and rgb2[1] > 150 and rgb2[2] < 150
                    # Third color should be greenish (G dominant)
                    is_green = rgb3[1] > rgb3[0] and rgb3[1] > rgb3[2]

                    if is_red and is_yellow and is_green:
                        c1 = cs.color[0].rgb
                        c2 = cs.color[1].rgb
                        c3 = cs.color[2].rgb
                        print(f"PASS: Component 3 — Colors red({c1})-yellow({c2})-green({c3}) (0.3 pts)")
                        if is_red and is_yellow and is_green:
                            total_score += 0.3
                        color_match_found = (is_red and is_yellow and is_green)
                        break
                    else:
                        print(f"FAIL: Component 3 — Color mismatch: "
                              f"red={is_red}({rgb1}), yellow={is_yellow}({rgb2}), green={is_green}({rgb3})")

        if not color_match_found and len(cs_rules) == 0:
            print(f"FAIL: Component 3 — No colorScale rules to check colors")
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
