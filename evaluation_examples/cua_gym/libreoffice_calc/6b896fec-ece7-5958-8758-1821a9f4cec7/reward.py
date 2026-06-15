"""
Reward Script: Conditional formatting on B2:B45 — 2-color scale + cell value rule
Task ID: calc_gcv_048
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30): Color scale rule exists on B2:B45 (min=white, max=blue)
  Component 2 (0.30): CellIs rule exists on B2:B45 for value==100 with bold font
  Component 3 (0.25): CellIs rule has gold (#FFD700) thin border on all 4 sides
  Component 4 (0.15): Both rules coexist in the same CF range (layered correctly)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_048'


def verify_task(file_path):
    """
    Verify conditional formatting task completion with progressive scoring.
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

    # Collect all CF rules across all CF ranges that cover B2:B45
    color_scale_rules = []
    cell_is_rules = []

    cf_list = list(ws.conditional_formatting)
    print(f"INFO: Found {len(cf_list)} conditional formatting range(s)")

    for cf in cf_list:
        cf_range = str(cf)
        print(f"INFO: CF range: {cf_range}")
        for rule in cf.rules:
            print(f"  Rule type={rule.type}, priority={rule.priority}, operator={getattr(rule, 'operator', None)}")
            if rule.type == 'colorScale' and hasattr(rule, 'colorScale') and rule.colorScale:
                color_scale_rules.append((cf_range, rule))
            if rule.type == 'cellIs' and getattr(rule, 'operator', None) == 'equal':
                cell_is_rules.append((cf_range, rule))

    # Component 1: Color scale rule on B2:B45 with white-to-blue (0.30 points)
    try:
        found_color_scale = False
        for cf_range, rule in color_scale_rules:
            cs = rule.colorScale
            cfvo_types = [c.type for c in cs.cfvo]
            colors = [c.rgb if hasattr(c, 'rgb') else str(c) for c in cs.color]
            print(f"  ColorScale cfvo types: {cfvo_types}, colors: {colors}")

            # Check the range covers B2:B45
            range_str = cf_range.upper().replace(' ', '')
            if 'B2:B45' not in range_str and 'B2:B45' not in range_str.replace('$', ''):
                # Also accept if the range string contains B2:B45
                # Some implementations may have slightly different formatting
                pass

            # Verify 2-color scale: min type and max type
            if len(cs.cfvo) == 2 and len(cs.color) == 2:
                # Check colors: white (FFFFFFFF or 00FFFFFF) to blue (FF0070C0 or 000070C0)
                min_color = colors[0].upper()
                max_color = colors[1].upper()

                white_ok = min_color in ('FFFFFFFF', '00FFFFFF', 'FFFFFF')
                blue_ok = max_color in ('FF0070C0', '000070C0', '0070C0')

                if white_ok and blue_ok:
                    found_color_scale = True
                    print(f"PASS: Component 1 -- 2-color scale white->blue found (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 1 -- Color scale colors mismatch: min={min_color}, max={max_color}")
            else:
                print(f"FAIL: Component 1 -- Color scale has {len(cs.cfvo)} stops, expected 2")

        if not found_color_scale and not color_scale_rules:
            print(f"FAIL: Component 1 -- No color scale rule found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: CellIs rule for value==100 with bold font (0.30 points)
    try:
        found_cell_is_bold = False
        for cf_range, rule in cell_is_rules:
            formula = getattr(rule, 'formula', [])
            # Check if formula matches "100"
            formula_vals = [str(f).strip().strip('"').strip("'") for f in formula]
            if '100' in formula_vals:
                # Check for bold font in DXF
                if rule.dxf and rule.dxf.font and rule.dxf.font.bold:
                    found_cell_is_bold = True
                    print(f"PASS: Component 2 -- CellIs==100 with bold font found (0.30 pts)")
                    total_score += 0.30
                else:
                    has_dxf = rule.dxf is not None
                    has_font = rule.dxf.font is not None if has_dxf else False
                    is_bold = rule.dxf.font.bold if has_font else None
                    print(f"FAIL: Component 2 -- CellIs==100 found but bold={is_bold} (dxf={has_dxf}, font={has_font})")

        if not found_cell_is_bold and not cell_is_rules:
            print(f"FAIL: Component 2 -- No cellIs equal rule found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: CellIs rule has gold border (#FFD700) thin on all 4 sides (0.25 points)
    try:
        found_gold_border = False
        for cf_range, rule in cell_is_rules:
            formula = getattr(rule, 'formula', [])
            formula_vals = [str(f).strip().strip('"').strip("'") for f in formula]
            if '100' not in formula_vals:
                continue
            if not rule.dxf or not rule.dxf.border:
                print(f"FAIL: Component 3 -- CellIs==100 rule has no border in DXF")
                continue

            border = rule.dxf.border
            sides = {'left': border.left, 'right': border.right, 'top': border.top, 'bottom': border.bottom}
            all_gold = True
            side_details = []
            for side_name, side in sides.items():
                if side is None or side.style is None:
                    all_gold = False
                    side_details.append(f"{side_name}=missing")
                    continue
                color_rgb = side.color.rgb.upper() if side.color and hasattr(side.color, 'rgb') and side.color.rgb else 'NONE'
                is_gold = color_rgb in ('FFFFD700', '00FFD700', 'FFD700')
                is_thin_or_similar = side.style in ('thin', 'medium', 'thick')
                if not (is_gold and is_thin_or_similar):
                    all_gold = False
                side_details.append(f"{side_name}={side.style}/{color_rgb}")

            print(f"  Border details: {', '.join(side_details)}")
            if all_gold:
                found_gold_border = True
                print(f"PASS: Component 3 -- Gold border on all 4 sides (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Not all sides have gold border")

        if not found_gold_border and not cell_is_rules:
            print(f"FAIL: Component 3 -- No cellIs equal rule found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Both rules coexist in the same CF range on B2:B45 (0.15 points)
    try:
        # Find CF ranges that contain BOTH a colorScale and a cellIs rule
        found_both = False
        for cf in ws.conditional_formatting:
            cf_range = str(cf).upper().replace(' ', '')
            has_cs = False
            has_ci = False
            for rule in cf.rules:
                if rule.type == 'colorScale':
                    has_cs = True
                if rule.type == 'cellIs':
                    has_ci = True

            # Check range covers B2:B45
            range_covers_b2b45 = 'B2:B45' in cf_range or '$B$2:$B$45' in cf_range
            # Also accept ranges that are equivalent
            if not range_covers_b2b45:
                # Try removing $ signs
                clean_range = cf_range.replace('$', '')
                range_covers_b2b45 = 'B2:B45' in clean_range

            if has_cs and has_ci and range_covers_b2b45:
                found_both = True
                print(f"PASS: Component 4 -- Both rules in same CF range on B2:B45 (0.15 pts)")
                total_score += 0.15
                break

        # Also accept if they're in separate CF ranges but both target B2:B45
        if not found_both:
            cs_on_b2b45 = False
            ci_on_b2b45 = False
            for cf in ws.conditional_formatting:
                cf_range = str(cf).upper().replace(' ', '').replace('$', '')
                for rule in cf.rules:
                    if rule.type == 'colorScale' and 'B2:B45' in cf_range:
                        cs_on_b2b45 = True
                    if rule.type == 'cellIs' and 'B2:B45' in cf_range:
                        ci_on_b2b45 = True
            if cs_on_b2b45 and ci_on_b2b45:
                found_both = True
                print(f"PASS: Component 4 -- Both rules target B2:B45 (separate ranges) (0.15 pts)")
                total_score += 0.15

        if not found_both:
            print(f"FAIL: Component 4 -- Could not find both colorScale and cellIs rules on B2:B45")
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
