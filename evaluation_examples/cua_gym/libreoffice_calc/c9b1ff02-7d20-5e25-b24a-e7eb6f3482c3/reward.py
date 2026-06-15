"""
Reward Script: Apply 4-arrow icon set conditional formatting to F2:F35
Task ID: calc_gcv_011
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): CF rule exists on range F2:F35 with type iconSet
  Component 2 (0.3): Icon set is 4Arrows
  Component 3 (0.2): Correct cfvo thresholds (0, 0.25, 0.5, 0.75)
  Component 4 (0.2): Correct cfvo types (all 'num') and 4 thresholds
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_011'


def persist_app_state(domain: str):
    """Attempt to save any unsaved GUI state via Ctrl+S."""
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
    Verify that a 4-arrow icon set conditional formatting rule has been
    applied to F2:F35 with correct thresholds.
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

    # Find iconSet CF rules on the target range
    icon_set_rule = None
    icon_set_range = None

    for cf in ws.conditional_formatting:
        cf_range_str = str(cf)
        for rule in cf.rules:
            if rule.type == 'iconSet' and hasattr(rule, 'iconSet') and rule.iconSet is not None:
                icon_set_rule = rule
                icon_set_range = cf_range_str
                break
        if icon_set_rule:
            break

    # Component 1: CF rule of type iconSet exists on F2:F35 (0.3 points)
    try:
        if icon_set_rule is not None:
            # Check the range covers F2:F35
            # Normalize: remove spaces, compare case-insensitively
            range_str = icon_set_range.replace('<ConditionalFormatting ', '').replace('>', '').strip()
            if 'F2:F35' in range_str.upper():
                print(f"PASS: Component 1 — iconSet CF rule found on range {range_str} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — iconSet CF rule found but on range '{range_str}', expected F2:F35")
        else:
            print("FAIL: Component 1 — No iconSet conditional formatting rule found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Icon set type is 4Arrows (0.3 points)
    try:
        if icon_set_rule is not None and icon_set_rule.iconSet is not None:
            icon_set_name = icon_set_rule.iconSet.iconSet
            if icon_set_name == '4Arrows':
                print(f"PASS: Component 2 — Icon set is '4Arrows' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Icon set is '{icon_set_name}', expected '4Arrows'")
        else:
            print("FAIL: Component 2 — No iconSet rule to check")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct cfvo thresholds: 0, 0.25, 0.5, 0.75 (0.2 points)
    try:
        if icon_set_rule is not None and icon_set_rule.iconSet is not None:
            ics = icon_set_rule.iconSet
            if hasattr(ics, 'cfvo') and ics.cfvo:
                vals = [float(cfvo.val) if cfvo.val is not None else None for cfvo in ics.cfvo]
                expected_vals = [0.0, 0.25, 0.5, 0.75]
                if len(vals) == 4 and vals == expected_vals:
                    print(f"PASS: Component 3 — cfvo thresholds are {vals} (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — cfvo thresholds are {vals}, expected {expected_vals}")
            else:
                print("FAIL: Component 3 — No cfvo entries found")
        else:
            print("FAIL: Component 3 — No iconSet rule to check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Correct cfvo types (all 'num') and exactly 4 entries (0.2 points)
    try:
        if icon_set_rule is not None and icon_set_rule.iconSet is not None:
            ics = icon_set_rule.iconSet
            if hasattr(ics, 'cfvo') and ics.cfvo:
                types = [cfvo.type for cfvo in ics.cfvo]
                if len(types) == 4 and all(t == 'num' for t in types):
                    print(f"PASS: Component 4 — All 4 cfvo types are 'num' (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 4 — cfvo types are {types}, expected all 'num' with 4 entries")
            else:
                print("FAIL: Component 4 — No cfvo entries found")
        else:
            print("FAIL: Component 4 — No iconSet rule to check")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved state before verifying
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
