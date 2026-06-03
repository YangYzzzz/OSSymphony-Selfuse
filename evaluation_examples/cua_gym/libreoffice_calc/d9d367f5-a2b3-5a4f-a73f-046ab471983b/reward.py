"""
Reward Script: Add data bars to cells C2:C15 with solid blue (#4472C4)
Task ID: calc_fmt_condfmt_databar_044
Domain: libreoffice_calc
Scoring:
  - Component 1: A dataBar conditional formatting rule exists on the sheet (0.4 pts)
  - Component 2: The CF rule is applied to range C2:C15 (0.3 pts)
  - Component 3: The data bar color is solid blue #4472C4 / FF4472C4 (0.3 pts)
Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_fmt_condfmt_databar_044'


def verify_task(file_path):
    """
    Verify that the task has been completed:
    - Data bar conditional formatting applied to C2:C15
    - Color is solid blue (#4472C4, ARGB: FF4472C4)

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must be loadable
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: sheet 'Budget Overview' must exist
    if 'Budget Overview' not in wb.sheetnames:
        print("CRITICAL: Sheet 'Budget Overview' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Budget Overview']
    cf_rules = ws.conditional_formatting

    # Collect all dataBar rules with their ranges
    # Each entry: (rule_object, range_string)
    databar_entries = []

    try:
        for cf_obj in cf_rules:
            for rule in cf_obj.rules:
                if rule.type == 'dataBar':
                    databar_entries.append((rule, str(cf_obj.sqref)))
    except Exception as e:
        print(f"ERROR: Could not iterate conditional formatting: {e}")

    # Component 1: A dataBar CF rule exists (0.4 points)
    # This FAILS on initial (no CF rules) and PASSES on golden (has dataBar rule)
    try:
        num_databar = len(databar_entries)
        if num_databar > 0:
            print(f"PASS: Component 1 — dataBar CF rule exists ({num_databar} rule(s) found) (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 — No dataBar conditional formatting rule found on the sheet")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The CF rule is applied to range C2:C15 (0.3 points)
    # At least one dataBar rule must target C2:C15 (case-insensitive, whitespace-tolerant)
    try:
        ranges_with_c2c15 = [
            rng for (_, rng) in databar_entries
            if 'C2:C15' in rng.strip().upper()
        ]
        if len(ranges_with_c2c15) > 0:
            print(f"PASS: Component 2 — dataBar CF range covers C2:C15 (found: {ranges_with_c2c15[0]}) (0.3 pts)")
            total_score += 0.3
        else:
            found_ranges = [rng for (_, rng) in databar_entries] or ["none"]
            print(f"FAIL: Component 2 — Expected dataBar on C2:C15, found ranges: {found_ranges}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The data bar color is solid blue #4472C4 (0.3 points)
    # The last 6 hex chars of the color RGB must be 4472C4
    # (ARGB format: FF4472C4 — alpha + R + G + B)
    try:
        colors_with_correct_hue = [
            db.color.rgb
            for (rule, _) in databar_entries
            if (hasattr(rule, 'dataBar') and rule.dataBar is not None
                and hasattr(rule.dataBar, 'color') and rule.dataBar.color is not None
                and rule.dataBar.color.rgb is not None
                and rule.dataBar.color.rgb.upper()[-6:] == '4472C4')
            for db in [rule.dataBar]
        ]
        if len(colors_with_correct_hue) > 0:
            print(f"PASS: Component 3 — data bar color is #4472C4 (found: {colors_with_correct_hue[0]}) (0.3 pts)")
            total_score += 0.3
        else:
            found_colors = [
                rule.dataBar.color.rgb
                for (rule, _) in databar_entries
                if (hasattr(rule, 'dataBar') and rule.dataBar is not None
                    and hasattr(rule.dataBar, 'color') and rule.dataBar.color is not None)
            ]
            print(f"FAIL: Component 3 — Expected data bar color #4472C4 (FF4472C4), "
                  f"found: {found_colors if found_colors else 'none'}")
            if not databar_entries:
                print("  (No dataBar rules exist — Component 1 already failed)")
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
