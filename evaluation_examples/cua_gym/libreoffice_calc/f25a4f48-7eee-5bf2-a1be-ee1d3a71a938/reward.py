"""
Reward Script: Verify data bar conditional formatting on Performance Index column
Task ID: calc_gcv_023
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): DataBar CF rule exists on H2:H70
  Component 2 (0.3): DataBar fill color is #70AD47 (ARGB FF70AD47)
  Component 3 (0.2): showValue is False (bar only, values hidden)
  Component 4 (0.2): cfvo min/max are automatic (type='min' and type='max')
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_023'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice edits before verification."""
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
    Verify data bar conditional formatting on H2:H70.
    Returns: float between 0.0 and 1.0
    """
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb.active

    # Find the dataBar rule targeting H2:H70
    databar_rule = None
    databar_range = None

    try:
        for cf in ws.conditional_formatting:
            cf_range_str = str(cf)
            for rule in cf.rules:
                if rule.type == 'dataBar' and rule.dataBar is not None:
                    # Check if the range covers H2:H70
                    # Accept exact match or containing range on column H
                    range_str = cf_range_str.replace('<ConditionalFormatting ', '').rstrip('>')
                    if 'H2' in range_str and 'H70' in range_str:
                        databar_rule = rule
                        databar_range = range_str
                        break
            if databar_rule:
                break
    except Exception as e:
        print(f"ERROR: Could not iterate conditional formatting: {e}")

    # Component 1: DataBar CF rule exists on H2:H70 (0.3 points)
    try:
        if databar_rule is not None:
            print(f"PASS: Component 1 -- DataBar rule found on range {databar_range} (0.3 pts)")
            total_score += 0.3
        else:
            # Check if any dataBar exists at all (for diagnostics)
            other_db_ranges = []
            for cf in ws.conditional_formatting:
                for rule in cf.rules:
                    if rule.type == 'dataBar':
                        other_db_ranges.append(str(cf))
            if len(other_db_ranges) == 0:
                print(f"FAIL: Component 1 -- No dataBar conditional formatting found")
            else:
                print(f"FAIL: Component 1 -- DataBar exists on {other_db_ranges} but not on H2:H70")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # All remaining components require the dataBar rule to exist
    if databar_rule is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    db = databar_rule.dataBar

    # Component 2: DataBar fill color is #70AD47 (0.3 points)
    try:
        color_rgb = db.color.rgb if db.color else None
        # Normalize: accept both FF70AD47 and 70AD47
        if color_rgb is not None:
            color_upper = str(color_rgb).upper()
            if color_upper == 'FF70AD47' or color_upper == '0070AD47' or color_upper == '70AD47':
                print(f"PASS: Component 2 -- DataBar color is {color_rgb} (matches #70AD47) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- Expected color FF70AD47, found {color_rgb}")
        else:
            print(f"FAIL: Component 2 -- DataBar color is None")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: showValue is False (bar only, values hidden) (0.2 points)
    try:
        show_val = db.showValue
        if show_val is False or show_val == 0:
            print(f"PASS: Component 3 -- showValue={show_val} (bar only) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- Expected showValue=False, found {show_val}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: cfvo min/max automatic (type='min' and type='max') (0.2 points)
    try:
        cfvos = db.cfvo
        if cfvos and len(cfvos) >= 2:
            min_type = cfvos[0].type
            max_type = cfvos[1].type
            if min_type == 'min' and max_type == 'max':
                print(f"PASS: Component 4 -- cfvo types are min/max (automatic) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 -- Expected cfvo types min/max, found {min_type}/{max_type}")
        else:
            print(f"FAIL: Component 4 -- cfvo list missing or fewer than 2 entries")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved state before scoring
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
