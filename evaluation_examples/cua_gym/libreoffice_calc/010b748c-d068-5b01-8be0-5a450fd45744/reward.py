"""
Reward Script: Apply Color Scale conditional formatting to column D (D2:D40)
Task ID: calc_gfl_026
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): Color scale conditional formatting exists on D2:D40
  Component 2 (0.3): Color scale has correct min/max CFVO structure
  Component 3 (0.3): Colors are red (lowest) to green (highest)
"""

import os

import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gfl_026'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_calc")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def is_reddish(rgb_str):
    """Check if an ARGB hex string represents a reddish color.
    Red channel should be dominant (high R, lower G and B).
    """
    try:
        # ARGB format: first 2 chars are alpha, then RRGGBB
        if len(rgb_str) == 8:
            r = int(rgb_str[2:4], 16)
            g = int(rgb_str[4:6], 16)
            b = int(rgb_str[6:8], 16)
        elif len(rgb_str) == 6:
            r = int(rgb_str[0:2], 16)
            g = int(rgb_str[2:4], 16)
            b = int(rgb_str[4:6], 16)
        else:
            return False
        # Red should be the dominant channel, significantly higher than green and blue
        return r > 150 and r > g and r > b
    except (ValueError, IndexError):
        return False


def is_greenish(rgb_str):
    """Check if an ARGB hex string represents a greenish color.
    Green channel should be dominant (high G, lower R).
    """
    try:
        if len(rgb_str) == 8:
            r = int(rgb_str[2:4], 16)
            g = int(rgb_str[4:6], 16)
            b = int(rgb_str[6:8], 16)
        elif len(rgb_str) == 6:
            r = int(rgb_str[0:2], 16)
            g = int(rgb_str[2:4], 16)
            b = int(rgb_str[4:6], 16)
        else:
            return False
        # Green should be dominant
        return g > 150 and g > r
    except (ValueError, IndexError):
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

    # Precondition: sheet 'Q4 Review' exists
    if 'Q4 Review' not in wb.sheetnames:
        print("FAIL: Sheet 'Q4 Review' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Q4 Review']

    # Find color scale conditional formatting on D2:D40
    color_scale_rule = None
    color_scale_range = None

    for cf in ws.conditional_formatting:
        cf_range_str = str(cf)
        for rule in cf.rules:
            if rule.type == 'colorScale' and rule.colorScale:
                # Check if the range covers D2:D40
                # The range string might be "D2:D40" or contain it
                if 'D2' in cf_range_str and 'D40' in cf_range_str:
                    color_scale_rule = rule
                    color_scale_range = cf_range_str
                    break
        if color_scale_rule:
            break

    # Component 1: Color scale conditional formatting exists on D2:D40 (0.4 points)
    try:
        if color_scale_rule is not None:
            print(f"PASS: Component 1 — Color scale CF found on range {color_scale_range} (0.4 pts)")
            total_score += 0.4
        else:
            # Check if there's any color scale at all (maybe on a slightly different range)
            wrong_range_cs = [
                str(cf) for cf in ws.conditional_formatting
                for rule in cf.rules if rule.type == 'colorScale'
            ]
            if wrong_range_cs:
                print(f"FAIL: Component 1 — Color scale found but on wrong range: {wrong_range_cs} (expected D2:D40)")
            else:
                print("FAIL: Component 1 — No color scale conditional formatting found on D2:D40")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Color scale has correct CFVO structure (min/max) (0.3 points)
    try:
        if color_scale_rule is not None:
            cs = color_scale_rule.colorScale
            cfvo_types = [cfvo.type for cfvo in cs.cfvo]
            # Accept both 2-color (min, max) and 3-color (min, percentile/mid, max) scales
            has_min = 'min' in cfvo_types
            has_max = 'max' in cfvo_types
            if has_min and has_max and len(cs.cfvo) >= 2:
                print(f"PASS: Component 2 — CFVO structure correct: {cfvo_types} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Expected min/max CFVOs, found: {cfvo_types}")
        else:
            print("FAIL: Component 2 — No color scale rule to check CFVO structure")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Colors are red (lowest/min) to green (highest/max) (0.3 points)
    try:
        if color_scale_rule is not None:
            cs = color_scale_rule.colorScale
            colors = cs.color
            cfvo_types = [cfvo.type for cfvo in cs.cfvo]

            # Find the index of min and max CFVOs
            min_idx = cfvo_types.index('min') if 'min' in cfvo_types else 0
            max_idx = cfvo_types.index('max') if 'max' in cfvo_types else len(cfvo_types) - 1

            min_color_rgb = colors[min_idx].rgb if colors[min_idx].rgb else ''
            max_color_rgb = colors[max_idx].rgb if colors[max_idx].rgb else ''

            print(f"  Min color (lowest): {min_color_rgb}")
            print(f"  Max color (highest): {max_color_rgb}")

            min_is_red = is_reddish(str(min_color_rgb))
            max_is_green = is_greenish(str(max_color_rgb))

            if min_is_red and max_is_green:
                print(f"PASS: Component 3 — Red (min={min_color_rgb}) to Green (max={max_color_rgb}) (0.3 pts)")
                total_score += 0.3
            elif min_is_red:
                print(f"FAIL: Component 3 — Min is red but max ({max_color_rgb}) is not green")
            elif max_is_green:
                print(f"FAIL: Component 3 — Max is green but min ({min_color_rgb}) is not red")
            else:
                print(f"FAIL: Component 3 — Expected red-to-green, found min={min_color_rgb}, max={max_color_rgb}")
        else:
            print("FAIL: Component 3 — No color scale rule to check colors")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
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
