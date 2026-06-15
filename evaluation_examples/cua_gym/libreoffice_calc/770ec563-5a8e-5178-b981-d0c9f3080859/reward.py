"""
Reward Script: Apply a 3-arrow icon set to the trend column (D2:D20)
Task ID: calc_fmt_condfmt_iconset_047
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): Conditional formatting rule of type 'iconSet' exists on range D2:D20
  Component 2 (0.3): The icon set type is '3Arrows' (3-arrow variant)
  Component 3 (0.3): The thresholds correctly split values at 0 (num/0 boundary for zero/negative split)
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_fmt_condfmt_iconset_047'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Apply a 3-arrows icon set conditional formatting to D2:D20 where:
      - Values > 0 → up arrow (green)
      - Values = 0 → right arrow (yellow)
      - Values < 0 → down arrow (red)
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: sheet 'Trend Analysis' must exist
    if 'Trend Analysis' not in wb.sheetnames:
        print("CRITICAL: Sheet 'Trend Analysis' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Trend Analysis']

    # Component 1: iconSet conditional formatting rule exists on D2:D20 (0.4 points)
    # This fails on initial (no CF rules) and passes on golden (has iconSet rule on D2:D20)
    try:
        found_iconset_rule = False
        iconset_rule = None
        iconset_range = None

        for cf in ws.conditional_formatting:
            # Convert range to string for comparison
            cf_range_str = str(cf).replace('<ConditionalFormatting ', '').replace('>', '').strip()
            for rule in cf.rules:
                if rule.type == 'iconSet':
                    found_iconset_rule = True
                    iconset_rule = rule
                    iconset_range = cf_range_str

        if found_iconset_rule:
            # Verify it applies to D2:D20
            if iconset_range and 'D2:D20' in iconset_range:
                print(f"PASS: Component 1 — iconSet conditional formatting rule found on D2:D20 (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — iconSet rule found but range is '{iconset_range}', expected D2:D20")
        else:
            print(f"FAIL: Component 1 — No iconSet conditional formatting rule found on sheet")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The icon set uses '3Arrows' variant (0.3 points)
    # This fails on initial (no CF) and passes on golden (3Arrows icon set)
    try:
        if iconset_rule is not None and hasattr(iconset_rule, 'iconSet') and iconset_rule.iconSet is not None:
            icon_set_obj = iconset_rule.iconSet
            icon_set_name = icon_set_obj.iconSet  # The icon set style name

            # Accept '3Arrows' or '3ArrowsGray' as valid 3-arrow icon sets
            # The task specifies colors (green/yellow/red) so '3Arrows' (colored) is preferred
            three_arrows_variants = ['3Arrows', '3ArrowsGray']
            if icon_set_name in three_arrows_variants:
                print(f"PASS: Component 2 — 3-arrow icon set found: '{icon_set_name}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Expected a 3Arrows icon set, found: '{icon_set_name}'")
        else:
            print(f"FAIL: Component 2 — No iconSet rule found or iconSet object is None")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The thresholds correctly split values at 0 for zero/negative boundary (0.3 points)
    # The task requires: values > 0 = up arrow, values = 0 = right arrow, values < 0 = down arrow
    # This means there must be a threshold with type='num' and val=0 to distinguish zero from negative
    # This fails on initial (no CF) and passes on golden (has num/0 threshold)
    try:
        if iconset_rule is not None and hasattr(iconset_rule, 'iconSet') and iconset_rule.iconSet is not None:
            icon_set_obj = iconset_rule.iconSet
            cfvo_list = icon_set_obj.cfvo

            # Look for a threshold with type='num' and val=0 (separates zero from negative)
            # Also check the icon set has exactly 3 thresholds (for 3 icons)
            has_num_zero_threshold = False
            has_correct_count = len(cfvo_list) == 3

            for cfvo in cfvo_list:
                if cfvo.type == 'num':
                    try:
                        val = float(cfvo.val)
                        if val == 0.0:
                            has_num_zero_threshold = True
                    except (ValueError, TypeError):
                        pass

            if has_correct_count and has_num_zero_threshold:
                print(f"PASS: Component 3 — 3 threshold values with num/0 boundary correctly separating zero from negative (0.3 pts)")
                total_score += 0.3
            elif not has_correct_count:
                print(f"FAIL: Component 3 — Expected 3 threshold values (cfvo), found {len(cfvo_list)}")
            else:
                print(f"FAIL: Component 3 — No num/0 threshold found to correctly distinguish values=0 from values<0")
                cfvo_details = [(c.type, c.val) for c in cfvo_list]
                print(f"  Actual thresholds: {cfvo_details}")
        else:
            print(f"FAIL: Component 3 — No iconSet rule found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
