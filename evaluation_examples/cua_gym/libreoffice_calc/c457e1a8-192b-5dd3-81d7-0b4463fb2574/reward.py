"""
Reward Script: Apply dual conditional formatting on Metrics sheet
Task ID: calc_ggf_026
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): colorScale rule exists on C2:C121 with 3 color stops
  Component 2 (0.35): colorScale has correct percentile thresholds and colors (red/white/dark green)
  Component 3 (0.25): cellIs rule for value==0 with black background fill
  Component 4 (0.15): Both rules target the correct range C2:C121
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ggf_026'


def persist_app_state(domain):
    """Attempt to save any unsaved LibreOffice changes."""
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

    # Check that 'Metrics' sheet exists (precondition gate)
    if 'Metrics' not in wb.sheetnames:
        print("CRITICAL: 'Metrics' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Metrics']

    # Gather all conditional formatting rules
    cf_list = list(ws.conditional_formatting)

    # Find colorScale and cellIs rules
    color_scale_rule = None
    color_scale_range = None
    cell_is_rule = None
    cell_is_range = None

    for cf in cf_list:
        cf_range_str = str(cf).replace('<ConditionalFormatting ', '').replace('>', '').strip()
        for rule in cf.rules:
            if rule.type == 'colorScale' and color_scale_rule is None:
                color_scale_rule = rule
                color_scale_range = cf_range_str
            if rule.type == 'cellIs' and cell_is_rule is None:
                cell_is_rule = rule
                cell_is_range = cf_range_str

    # Component 1: A colorScale rule exists with 3 color stops (0.25 points)
    try:
        if color_scale_rule is not None:
            cs = color_scale_rule.colorScale
            if cs and len(cs.cfvo) == 3 and len(cs.color) == 3:
                print(f"PASS: Component 1 - colorScale rule with 3 stops found (0.25 pts)")
                total_score += 0.25
            else:
                cfvo_count = len(cs.cfvo) if cs else 0
                color_count = len(cs.color) if cs else 0
                print(f"FAIL: Component 1 - colorScale found but has {cfvo_count} cfvo and {color_count} colors, expected 3 each")
        else:
            print("FAIL: Component 1 - No colorScale conditional formatting rule found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: colorScale has correct percentile thresholds and colors (0.35 points)
    try:
        if color_scale_rule is not None:
            cs = color_scale_rule.colorScale
            if cs and len(cs.cfvo) == 3 and len(cs.color) == 3:
                sub_score = 0.0

                # Check cfvo types and values: percentile 10, 50, 90
                cfvo_types = [(c.type, c.val) for c in cs.cfvo]
                expected_cfvo = [('percentile', 10.0), ('percentile', 50.0), ('percentile', 90.0)]

                # Allow some flexibility: percentile values might be stored as int or float
                cfvo_mismatches = sum(
                    1 for (ct, cv), (et, ev) in zip(cfvo_types, expected_cfvo)
                    if ct != et or (cv is not None and abs(float(cv) - ev) > 0.5)
                )
                cfvo_match = (cfvo_mismatches == 0)

                if cfvo_match:
                    sub_score += 0.15
                    print(f"  PASS: percentile thresholds correct: {cfvo_types}")
                else:
                    print(f"  FAIL: percentile thresholds mismatch. Expected {expected_cfvo}, got {cfvo_types}")

                # Check colors: red, white, dark green
                colors_rgb = []
                for c in cs.color:
                    rgb = getattr(c, 'rgb', None)
                    if rgb and isinstance(rgb, str):
                        # Strip alpha prefix (first 2 chars of 8-char ARGB)
                        colors_rgb.append(rgb[-6:].upper())
                    else:
                        colors_rgb.append(None)

                # Red: FF0000, White: FFFFFF, Dark Green: 006400
                # Allow some tolerance for color values
                red_ok = colors_rgb[0] == 'FF0000' if colors_rgb[0] else False
                white_ok = colors_rgb[1] == 'FFFFFF' if colors_rgb[1] else False
                # Dark green can be 006400, 008000, or similar dark green shades
                green_ok = False
                if colors_rgb[2]:
                    r = int(colors_rgb[2][0:2], 16)
                    g = int(colors_rgb[2][2:4], 16)
                    b = int(colors_rgb[2][4:6], 16)
                    # Dark green: low red, notable green, low blue
                    green_ok = (r <= 30 and g >= 80 and b <= 30)

                color_matches = sum([red_ok, white_ok, green_ok])
                if color_matches == 3:
                    sub_score += 0.20
                    print(f"  PASS: colors correct - red={colors_rgb[0]}, white={colors_rgb[1]}, green={colors_rgb[2]}")
                elif color_matches >= 1:
                    partial = 0.20 * (color_matches / 3)
                    sub_score += partial
                    print(f"  PARTIAL: {color_matches}/3 colors match - got {colors_rgb} ({partial:.2f} pts)")
                else:
                    print(f"  FAIL: colors mismatch - got {colors_rgb}")

                if sub_score > 0:
                    print(f"PASS: Component 2 - colorScale properties verified ({sub_score:.2f} pts)")
                    total_score += sub_score
                else:
                    print("FAIL: Component 2 - colorScale properties incorrect")
            else:
                print("FAIL: Component 2 - colorScale rule missing or malformed")
        else:
            print("FAIL: Component 2 - No colorScale rule to check properties on")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: cellIs rule for value==0 with black background fill (0.25 points)
    try:
        if cell_is_rule is not None:
            op = getattr(cell_is_rule, 'operator', None)
            formula = getattr(cell_is_rule, 'formula', [])
            formula_vals = list(formula) if formula else []

            # Check operator is 'equal' and formula is '0'
            op_ok = (op == 'equal')
            formula_ok = any(str(f).strip() == '0' for f in formula_vals)

            # Check black background fill
            dxf = getattr(cell_is_rule, 'dxf', None)
            fill_ok = False
            if dxf and dxf.fill:
                fg_rgb = None
                try:
                    fg_rgb = dxf.fill.fgColor.rgb
                except:
                    pass
                if not fg_rgb:
                    try:
                        fg_rgb = dxf.fill.bgColor.rgb
                    except:
                        pass
                if fg_rgb and isinstance(fg_rgb, str):
                    # Black: 000000 (last 6 chars of ARGB)
                    fill_ok = fg_rgb[-6:].upper() == '000000'
                    print(f"  fill color: {fg_rgb}, patternType: {dxf.fill.patternType}")

            if op_ok and formula_ok and fill_ok:
                print(f"PASS: Component 3 - cellIs equal 0 with black fill (0.25 pts)")
                total_score += 0.25
            elif op_ok and formula_ok:
                print(f"PARTIAL: Component 3 - cellIs equal 0 found but fill not black (0.10 pts)")
                total_score += 0.10
            elif fill_ok:
                print(f"PARTIAL: Component 3 - black fill found but operator/formula wrong: op={op}, formula={formula_vals} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 - cellIs rule issues: op={op}, formula={formula_vals}, fill_ok={fill_ok}")
        else:
            print("FAIL: Component 3 - No cellIs conditional formatting rule found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Both rules target the correct range C2:C121 (0.15 points)
    try:
        cs_range_ok = False
        ci_range_ok = False

        if color_scale_range:
            # Normalize: remove spaces, compare
            norm_cs = color_scale_range.replace(' ', '').upper()
            cs_range_ok = 'C2:C121' in norm_cs
            print(f"  colorScale range: {color_scale_range} -> {'OK' if cs_range_ok else 'MISMATCH'}")

        if cell_is_range:
            norm_ci = cell_is_range.replace(' ', '').upper()
            ci_range_ok = 'C2:C121' in norm_ci
            print(f"  cellIs range: {cell_is_range} -> {'OK' if ci_range_ok else 'MISMATCH'}")

        if cs_range_ok and ci_range_ok:
            print(f"PASS: Component 4 - Both rules on C2:C121 (0.15 pts)")
            total_score += 0.15
        elif cs_range_ok or ci_range_ok:
            print(f"PARTIAL: Component 4 - Only one rule on correct range (0.075 pts)")
            total_score += 0.075
        else:
            print(f"FAIL: Component 4 - Neither rule targets C2:C121")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(round(total_score, 4), 1.0)
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
