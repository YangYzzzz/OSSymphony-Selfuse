"""
Reward Script: Conditional formatting for overdue rows in task manager
Task ID: calc_gfl_088
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.20): Conditional formatting rule exists on Tasks sheet
  - Component 2 (0.20): CF rule covers correct range (A2:G35)
  - Component 3 (0.35): CF formula references $D column and TODAY() comparison
  - Component 4 (0.25): CF fill is a red/pink solid background
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gfl_088'


def verify_task(file_path):
    """
    Verify that conditional formatting was applied to highlight overdue rows.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Tasks sheet exists
    if 'Tasks' not in wb.sheetnames:
        print("FAIL: 'Tasks' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Tasks']

    # Gather all conditional formatting rules
    cf_list = list(ws.conditional_formatting)
    print(f"INFO: Found {len(cf_list)} conditional formatting rule group(s)")

    # Component 1: At least one conditional formatting rule exists (0.20 points)
    try:
        if len(cf_list) > 0:
            print(f"PASS: Component 1 -- Conditional formatting exists ({len(cf_list)} group(s)) (0.20 pts)")
            total_score += 0.20
        else:
            print("FAIL: Component 1 -- No conditional formatting rules found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Find the relevant CF rule (the one with a TODAY() formula)
    target_cf = None
    target_rule = None
    for cf in cf_list:
        for rule in cf.rules:
            if rule.type == 'expression' and rule.formula:
                formula_str = str(rule.formula[0]).upper().replace(' ', '')
                if 'TODAY()' in formula_str:
                    target_cf = cf
                    target_rule = rule
                    break
        if target_rule:
            break

    if target_rule is None:
        # Check if there are any rules at all that we might have missed
        for cf in cf_list:
            for rule in cf.rules:
                print(f"  DEBUG: rule type={rule.type}, formula={getattr(rule, 'formula', None)}")
        if len(cf_list) > 0:
            print("FAIL: Found CF rules but none use a TODAY()-based formula")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    print(f"INFO: Found target CF rule -- formula: {target_rule.formula}")

    # Component 2: CF rule covers correct range A2:G35 (0.20 points)
    try:
        cf_range_str = str(target_cf).strip()
        print(f"INFO: CF range string: '{cf_range_str}'")

        # Parse the range -- accept various formats
        # The range should cover at minimum A2:G35 (all data rows, all columns)
        # Normalize: check if the range covers A2:G35 or equivalent
        # Could be written as A2:G35, $A$2:$G$35, A2:G1048576, etc.
        import re
        cf_upper = cf_range_str.upper().replace('$', '')

        # Check that it starts at row 2 and column A, and ends at column G and row >= 35
        end_row_match = re.search(r'G(\d+)', cf_upper) if ('A2' in cf_upper and 'G' in cf_upper) else None
        end_row = int(end_row_match.group(1)) if end_row_match else 0

        if end_row >= 35:
            print(f"PASS: Component 2 -- CF range covers A2:G{end_row} (includes A2:G35) (0.20 pts)")
            total_score += 0.20
        elif end_row > 0:
            print(f"FAIL: Component 2 -- CF range ends at row {end_row}, expected >= 35")
        else:
            print(f"FAIL: Component 2 -- CF range '{cf_range_str}' does not cover A2:G* area")

    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: CF formula uses $D<row> < TODAY() comparison (0.35 points)
    try:
        formula_raw = str(target_rule.formula[0])
        formula_norm = formula_raw.upper().replace(' ', '')
        print(f"INFO: CF formula raw: '{formula_raw}', normalized: '{formula_norm}'")

        # The formula should reference column D (with $ anchor) and TODAY()
        # Expected patterns: $D2<TODAY(), $D2<TODAY(), etc.
        has_d_ref = ('$D' in formula_norm or 'D2' in formula_norm.replace('$', ''))
        has_today = 'TODAY()' in formula_norm
        has_less_than = '<' in formula_norm

        if has_d_ref and has_today and has_less_than:
            print(f"PASS: Component 3 -- Formula references column D and compares with TODAY() (0.35 pts)")
            total_score += 0.35
        else:
            missing = []
            if not has_d_ref:
                missing.append("column D reference")
            if not has_today:
                missing.append("TODAY() function")
            if not has_less_than:
                missing.append("less-than operator")
            print(f"FAIL: Component 3 -- Formula missing: {', '.join(missing)}")

    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: CF fill is a red/pink solid background (0.25 points)
    try:
        dxf = target_rule.dxf
        if dxf and dxf.fill:
            fill = dxf.fill
            fill_type = fill.patternType
            fg_rgb = None
            try:
                fg_rgb = fill.fgColor.rgb if fill.fgColor else None
            except:
                pass

            print(f"INFO: CF fill -- patternType={fill_type}, fgColor.rgb={fg_rgb}")

            # Check for solid fill
            is_solid = (fill_type == 'solid')

            # Check for red/pink color family
            # Common red/pink ARGB values: FFFF0000 (pure red), FFFFC7CE (light red),
            # FFFF9999, FFFF6666, FFFF4444, FFFF7C80, FFF2DCDB, etc.
            # Determine if color is in red/pink family
            # Red/pink: R is dominant (R > G and R > B), R >= 200
            # Also accept near-max R (>= 240) with lower G and B
            r_val, g_val, b_val = 0, 0, 0
            if fg_rgb and len(fg_rgb) >= 6:
                hex_rgb = fg_rgb[-6:]
                r_val = int(hex_rgb[0:2], 16)
                g_val = int(hex_rgb[2:4], 16)
                b_val = int(hex_rgb[4:6], 16)
                print(f"INFO: RGB values -- R={r_val}, G={g_val}, B={b_val}")

            is_red_family = (
                (r_val >= 200 and r_val > g_val and r_val > b_val) or
                (r_val >= 240 and g_val <= 220 and b_val <= 220)
            )

            if is_solid and is_red_family:
                print(f"PASS: Component 4 -- Solid red/pink fill applied (0.25 pts)")
                total_score += 0.25
            elif is_red_family and not is_solid:
                print(f"PARTIAL: Component 4 -- Red/pink color detected but fill type is '{fill_type}', not solid (0.10 pts)")
                total_score += 0.10
            elif is_solid and not is_red_family:
                print(f"FAIL: Component 4 -- Solid fill but color {fg_rgb} is not in red/pink family")
            else:
                print(f"FAIL: Component 4 -- Fill not solid red/pink (type={fill_type}, color={fg_rgb})")
        else:
            print("FAIL: Component 4 -- No fill defined in CF rule's differential style")

    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
