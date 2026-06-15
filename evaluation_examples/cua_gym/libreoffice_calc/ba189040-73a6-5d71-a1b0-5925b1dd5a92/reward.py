"""
Reward Script: Apply 3-color scale conditional formatting to performance scores (D2:D41)
Task ID: calc_gsd_012
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30): Conditional formatting rule exists on D2:D41
  Component 2 (0.30): Rule is colorScale type with 3 cfvo stops (min, percentile 50, max)
  Component 3 (0.25): Colors match red/yellow/green spec
  Component 4 (0.15): Data integrity — scores unchanged AND CF present (compound check)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gsd_012'

# Expected D-column values (from initial file, must be preserved)
EXPECTED_D_VALUES = [
    92, 78, 85, 67, 91, 73, 88, 56, 95, 62,
    98, 71, 83, 45, 76, 89, 94, 58, 87, 69,
    82, 91, 74, 63, 86, 77, 96, 52, 90, 65,
    81, 72, 84, 48, 79, 93, 68, 55, 87, 60,
]


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

    try:
        ws = wb['Performance']
    except KeyError:
        print("CRITICAL: Sheet 'Performance' not found")
        print("REWARD: 0.0")
        return 0.0

    # Track whether CF exists for compound checks
    cf_found = False
    color_scale_rule = None

    # Component 1: Conditional formatting rule exists on D2:D41 (0.30 points)
    try:
        cf_list = list(ws.conditional_formatting)
        target_range_found = False
        for cf in cf_list:
            # Check if any CF covers D2:D41
            cf_range_str = str(cf).replace('<ConditionalFormatting ', '').replace('>', '').strip()
            # Normalize: check if D2:D41 is covered
            if 'D2:D41' in cf_range_str or 'D2:D41' in str(cf.sqref):
                target_range_found = True
                # Check for colorScale rules within this CF
                for rule in cf.rules:
                    if rule.type == 'colorScale':
                        color_scale_rule = rule
                        break
                break

        if target_range_found:
            cf_found = True
            print(f"PASS: Component 1 — Conditional formatting found on D2:D41 (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — No conditional formatting on D2:D41. Found {len(cf_list)} CF rules: {[str(cf) for cf in cf_list]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Rule is colorScale type with 3 stops (min, percentile 50, max) (0.30 points)
    try:
        if color_scale_rule is not None:
            cs = color_scale_rule.colorScale
            cfvo_list = cs.cfvo
            if len(cfvo_list) == 3:
                types = [(c.type, c.val) for c in cfvo_list]
                # Expect: min, percentile 50, max
                type_check = (
                    types[0][0] == 'min' and
                    types[1][0] == 'percentile' and
                    abs(float(types[1][1] or 0) - 50.0) < 0.01 and
                    types[2][0] == 'max'
                )
                if type_check:
                    print(f"PASS: Component 2 — ColorScale with 3 stops: min, percentile(50), max (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 2 — ColorScale stops mismatch. Found: {types}")
            else:
                print(f"FAIL: Component 2 — Expected 3 cfvo stops, found {len(cfvo_list)}")
        else:
            print(f"FAIL: Component 2 — No colorScale rule found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Colors match red (#FF0000), yellow (#FFFF00), green (#00B050) (0.25 points)
    try:
        if color_scale_rule is not None:
            cs = color_scale_rule.colorScale
            colors = cs.color
            if len(colors) >= 3:
                # Get RGB values (8-char ARGB format)
                color_rgbs = []
                for c in colors:
                    if hasattr(c, 'rgb') and c.rgb:
                        color_rgbs.append(str(c.rgb).upper())
                    else:
                        color_rgbs.append(None)

                # Expected colors (ARGB): FFFF0000 (red), FFFFFF00 (yellow), FF00B050 (green)
                # Allow some flexibility: check the RGB portion (last 6 chars)
                red_ok = color_rgbs[0] is not None and color_rgbs[0][-6:] == 'FF0000'
                yellow_ok = color_rgbs[1] is not None and color_rgbs[1][-6:] == 'FFFF00'
                green_ok = color_rgbs[2] is not None and color_rgbs[2][-6:] == '00B050'

                if red_ok and yellow_ok and green_ok:
                    print(f"PASS: Component 3 — Colors correct: red={color_rgbs[0]}, yellow={color_rgbs[1]}, green={color_rgbs[2]} (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 — Color mismatch. Found: {color_rgbs}, expected red/yellow/green")
            else:
                print(f"FAIL: Component 3 — Expected 3 colors, found {len(colors)}")
        else:
            print(f"FAIL: Component 3 — No colorScale rule to check colors")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Data integrity — D column values unchanged AND CF is present (0.15 points)
    # This is a compound check: only awards points if CF exists AND data is intact
    try:
        if cf_found:
            actual_values = [ws.cell(row=r, column=4).value for r in range(2, 42)]
            values_match = True
            for i, (actual, expected) in enumerate(zip(actual_values, EXPECTED_D_VALUES)):
                if actual != expected:
                    print(f"FAIL: Component 4 — D{i+2} value changed: expected {expected}, found {actual}")
                    values_match = False
                    break

            if values_match and len(actual_values) == len(EXPECTED_D_VALUES):
                print(f"PASS: Component 4 — All 40 D-column values intact with CF applied (0.15 pts)")
                total_score += 0.15
            elif not values_match:
                pass  # already printed
            else:
                print(f"FAIL: Component 4 — Expected 40 values, found {len(actual_values)}")
        else:
            print(f"FAIL: Component 4 — CF not found, compound check fails")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_calc")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
persist_app_state()

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
