"""
Reward Script: Apply two-color scale conditional formatting to B2:B30
Task ID: calc_gfl_072
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): A colorScale conditional formatting rule exists
  Component 2 (0.3): The rule targets range B2:B30
  Component 3 (0.3): Colors are white (min) and dark blue (max)
"""

import os

import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gfl_072'


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

    # Precondition: 'NPS Scores' sheet must exist
    if 'NPS Scores' not in wb.sheetnames:
        print("FAIL: Sheet 'NPS Scores' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['NPS Scores']

    # Collect all colorScale rules from all conditional formatting entries
    color_scale_rules = []
    color_scale_ranges = []
    for cf in ws.conditional_formatting:
        for rule in cf.rules:
            if rule.type == 'colorScale' and rule.colorScale is not None:
                color_scale_rules.append(rule)
                # cf.sqref gives the actual cell range(s) as a string
                color_scale_ranges.append(str(cf.sqref))

    # Component 1: A colorScale conditional formatting rule exists (0.4 points)
    try:
        if len(color_scale_rules) >= 1:
            print(f"PASS: Component 1 -- colorScale rule found ({len(color_scale_rules)} rule(s)) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- no colorScale conditional formatting found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: The rule applies to range B2:B30 (0.3 points)
    try:
        # Check if any colorScale rule covers B2:B30
        target_found = False
        for range_str in color_scale_ranges:
            # The range string from ConditionalFormatting may be e.g. "B2:B30"
            normalized = range_str.strip().upper().replace('$', '')
            if normalized == 'B2:B30':
                target_found = True
                break
        if target_found:
            print(f"PASS: Component 2 -- colorScale applied to B2:B30 (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- colorScale range mismatch, found: {color_scale_ranges}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Colors are white (min) and dark blue (max) (0.3 points)
    try:
        color_correct = False
        for rule in color_scale_rules:
            cs = rule.colorScale
            cfvo_types = [c.type for c in cs.cfvo]
            colors = []
            for c in cs.color:
                if hasattr(c, 'rgb') and c.rgb:
                    colors.append(str(c.rgb).upper())
                else:
                    colors.append(str(c).upper())

            print(f"  DEBUG: cfvo_types={cfvo_types}, colors={colors}")

            # Verify it's a two-color scale (min, max)
            if len(cfvo_types) != 2:
                continue
            if cfvo_types[0] != 'min' or cfvo_types[1] != 'max':
                continue

            if len(colors) < 2:
                continue

            # Check min color is white-ish
            min_color = colors[0]
            # White variants: FFFFFFFF, 00FFFFFF, FFFFFF
            is_white = min_color in ('FFFFFFFF', '00FFFFFF', 'FFFFFF')

            # Check max color is dark blue-ish
            max_color = colors[1]
            # Dark blue: FF00008B (DarkBlue), FF000080 (Navy), FF00008B, FF191970 (MidnightBlue)
            # Also accept close variants
            dark_blue_variants = {
                'FF00008B',  # DarkBlue
                '0000008B',
                'FF000080',  # Navy
                '00000080',
                'FF191970',  # MidnightBlue
                'FF00006B',  # close variant
                'FF000066',  # close variant
                'FF0000AA',  # medium-dark blue
                'FF0000CD',  # MediumBlue
            }

            # More flexible: check if R <= 0x33, G <= 0x33, B >= 0x66
            is_dark_blue = max_color in dark_blue_variants
            if not is_dark_blue and len(max_color) == 8:
                try:
                    r = int(max_color[2:4], 16)
                    g = int(max_color[4:6], 16)
                    b = int(max_color[6:8], 16)
                    # Dark blue: low red, low green, high blue
                    if r <= 0x40 and g <= 0x40 and b >= 0x60:
                        is_dark_blue = True
                except ValueError:
                    pass

            if is_white and is_dark_blue:
                color_correct = True
                break

        if color_correct:
            print(f"PASS: Component 3 -- min=white, max=dark blue (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 -- color mismatch. Expected white->dark blue.")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

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
