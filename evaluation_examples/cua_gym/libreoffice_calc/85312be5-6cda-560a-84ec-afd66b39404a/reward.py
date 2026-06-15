"""
Reward Script: Verify Data Bar conditional formatting on Sales sheet C2:C26
Task ID: calc_gg3_018
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30): DataBar conditional formatting rule exists on range C2:C26
  Component 2 (0.30): DataBar color is blue (FF4472C4 or similar blue shade)
  Component 3 (0.20): DataBar minLength=0 and maxLength=100
  Component 4 (0.20): DataBar uses min/max cfvo types and showValue=True
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gg3_018'


def _check_blue(rgb_str):
    """Return whether an ARGB hex string represents a blue shade."""
    if len(rgb_str) < 6:
        return False
    hex_part = rgb_str[-6:]
    try:
        r = int(hex_part[0:2], 16)
        g = int(hex_part[2:4], 16)
        b = int(hex_part[4:6], 16)
        # Blue means B channel is dominant and significant
        return b > r and b >= g and b >= 100
    except ValueError:
        return False


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
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

    # Precondition: 'Sales' sheet must exist
    if 'Sales' not in wb.sheetnames:
        print("FAIL: 'Sales' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Sales']

    # Find the DataBar rule targeting C2:C26
    databar_rule = None
    databar_range = None
    for cf in ws.conditional_formatting:
        for rule in cf.rules:
            if rule.type == 'dataBar' and rule.dataBar is not None:
                # Check if the range covers C2:C26
                range_str = str(cf).strip()
                # Normalize: the range string from openpyxl looks like "C2:C26"
                # but could have formatting wrapper text
                if 'C2' in range_str and 'C26' in range_str:
                    databar_rule = rule
                    databar_range = range_str
                    break
        if databar_rule:
            break

    # Component 1: DataBar conditional formatting rule exists on C2:C26 (0.30 points)
    try:
        if databar_rule is not None:
            print(f"PASS: Component 1 - DataBar rule found on range containing C2:C26 (range: {databar_range}) (0.30 pts)")
            total_score += 0.30
        else:
            # Check if there's any dataBar at all, for diagnostics
            found_other_databars = []
            for cf in ws.conditional_formatting:
                for rule in cf.rules:
                    if rule.type == 'dataBar':
                        found_other_databars.append(str(cf))
                        print(f"  INFO: Found dataBar on range {cf} but not matching C2:C26")
            if len(found_other_databars) == 0:
                print(f"FAIL: Component 1 - No DataBar conditional formatting found on Sales sheet")
            else:
                print(f"FAIL: Component 1 - DataBar found but not on expected range C2:C26")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Components 2-4 only checked if we found the DataBar rule
    if databar_rule is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    db = databar_rule.dataBar

    # Component 2: DataBar color is blue (0.30 points)
    # Blue shades: FF4472C4 (standard blue), FF0000FF (pure blue), FF0070C0, FF5B9BD5, etc.
    try:
        color_rgb = None
        if db.color is not None:
            color_rgb = db.color.rgb if hasattr(db.color, 'rgb') else str(db.color)

        if color_rgb is not None:
            # Parse ARGB to check if it's a blue shade
            rgb_str = str(color_rgb)
            color_is_blue = _check_blue(rgb_str)

            if color_is_blue:
                print(f"PASS: Component 2 - DataBar color is blue (RGB: {color_rgb}) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 - DataBar color is not blue (RGB: {color_rgb})")
        else:
            print(f"FAIL: Component 2 - DataBar color not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: minLength=0 and maxLength=100 (0.20 points)
    try:
        min_len = db.minLength
        max_len = db.maxLength
        if min_len == 0 and max_len == 100:
            print(f"PASS: Component 3 - minLength={min_len}, maxLength={max_len} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 - minLength={min_len} (expected 0), maxLength={max_len} (expected 100)")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: cfvo uses min/max types and showValue=True (0.20 points)
    try:
        # Check cfvo types directly
        has_min_max_cfvo = (
            hasattr(db, 'cfvo')
            and db.cfvo is not None
            and len(db.cfvo) >= 2
            and 'min' in [fo.type for fo in db.cfvo]
            and 'max' in [fo.type for fo in db.cfvo]
        )

        # showValue defaults to True; None means default (True)
        has_show_value = (db.showValue is not False)

        if has_min_max_cfvo and has_show_value:
            print(f"PASS: Component 4 - cfvo types: min/max, showValue: {db.showValue} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 - has_min_max_cfvo={has_min_max_cfvo}, showValue={db.showValue}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved state
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
