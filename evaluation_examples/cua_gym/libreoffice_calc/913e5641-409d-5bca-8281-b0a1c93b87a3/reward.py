"""
Reward Script: Conditional formatting (Greater Than 5000) on D2:D81 with green fill / dark green text
Task ID: calc_ggf_001
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): CF rule exists covering D2:D81
  Component 2 (0.4): Rule is cellIs/greaterThan with threshold 5000
  Component 3 (0.3): Fill is green and font is dark green
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ggf_001'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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
    Verify conditional formatting on D2:D81: greaterThan 5000, green fill, dark green font.
    Returns float 0.0 - 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if 'Sales' not in wb.sheetnames:
        print("FAIL: 'Sales' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Sales']

    # Collect all conditional formatting rules
    cf_list = list(ws.conditional_formatting)
    print(f"INFO: Found {len(cf_list)} conditional formatting block(s)")

    # --- Component 1: CF rule exists covering D2:D81 (0.3 points) ---
    try:
        matching_cf = None
        matching_rule = None
        for cf in cf_list:
            cf_str = str(cf).upper()
            # Check if the range covers D2:D81 (may appear as "D2:D81" or similar)
            for rule in cf.rules:
                if rule.type == 'cellIs':
                    # Check that the range includes D2:D81
                    # The range string from openpyxl is like "<ConditionalFormatting D2:D81>"
                    # or the cells attribute contains the range
                    range_str = str(cf)
                    # Extract just the range part
                    if 'D2:D81' in range_str.upper().replace(' ', ''):
                        matching_cf = cf
                        matching_rule = rule
                        break
                    # Also check individual cell ranges in the cf object
                    try:
                        for cell_range in cf.cells.ranges:
                            cr_str = str(cell_range).upper()
                            if 'D2' in cr_str and 'D81' in cr_str:
                                matching_cf = cf
                                matching_rule = rule
                                break
                    except Exception:
                        pass
            if matching_rule:
                break

        if matching_rule:
            print(f"PASS: Component 1 — CF rule found covering D2:D81 (0.3 pts)")
            total_score += 0.3
        else:
            # Partial: any cellIs CF rule on column D at all
            any_d_rule = False
            for cf in cf_list:
                for rule in cf.rules:
                    if rule.type == 'cellIs' and 'D' in str(cf).upper():
                        any_d_rule = True
                        matching_rule = rule
                        matching_cf = cf
                        break
                if any_d_rule:
                    break
            if any_d_rule:
                print(f"PARTIAL: Component 1 — CF cellIs rule found on column D but range is {str(matching_cf)}, expected D2:D81 (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — No cellIs conditional formatting rule found covering D2:D81")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: Rule is greaterThan with threshold 5000 (0.4 points) ---
    try:
        if matching_rule:
            operator_ok = matching_rule.operator == 'greaterThan'
            formula_ok = False
            if matching_rule.formula:
                for f in matching_rule.formula:
                    try:
                        if float(f) == 5000.0:
                            formula_ok = True
                            break
                    except (ValueError, TypeError):
                        if '5000' in str(f):
                            formula_ok = True
                            break

            if operator_ok and formula_ok:
                print(f"PASS: Component 2 — Operator=greaterThan, threshold=5000 (0.4 pts)")
                total_score += 0.4
            elif operator_ok:
                print(f"PARTIAL: Component 2 — Operator correct (greaterThan) but threshold is {matching_rule.formula}, expected 5000 (0.2 pts)")
                total_score += 0.2
            elif formula_ok:
                print(f"PARTIAL: Component 2 — Threshold is 5000 but operator is '{matching_rule.operator}', expected 'greaterThan' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — Operator='{matching_rule.operator}' (expected greaterThan), formula={matching_rule.formula} (expected 5000)")
        else:
            print(f"FAIL: Component 2 — No matching CF rule to check operator/threshold")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: Green fill and dark green font (0.3 points) ---
    try:
        if matching_rule and matching_rule.dxf:
            dxf = matching_rule.dxf
            fill_ok = False
            font_ok = False

            # Check fill — should be a green fill (solid pattern with green-ish fgColor)
            if dxf.fill and dxf.fill.fgColor:
                fill_rgb = None
                try:
                    fill_rgb = dxf.fill.fgColor.rgb
                except Exception:
                    pass
                if fill_rgb:
                    # Accept various green fills: C6EFCE (standard), 00FF00, 92D050, etc.
                    # Extract RGB components (skip alpha)
                    rgb_hex = fill_rgb[-6:]  # last 6 chars = RRGGBB
                    r = int(rgb_hex[0:2], 16)
                    g = int(rgb_hex[2:4], 16)
                    b = int(rgb_hex[4:6], 16)
                    # Green fill: G channel should dominate
                    if g > r and g > b:
                        fill_ok = True
                        print(f"  Fill color: {fill_rgb} — green (R={r}, G={g}, B={b})")
                    else:
                        print(f"  Fill color: {fill_rgb} — NOT green (R={r}, G={g}, B={b})")
                else:
                    print(f"  Fill fgColor rgb is None/empty")
            else:
                print(f"  No fill or no fgColor in DXF")

            # Check font — should be dark green
            if dxf.font and dxf.font.color:
                font_rgb = None
                try:
                    font_rgb = dxf.font.color.rgb
                except Exception:
                    pass
                if font_rgb:
                    rgb_hex = font_rgb[-6:]
                    r = int(rgb_hex[0:2], 16)
                    g = int(rgb_hex[2:4], 16)
                    b = int(rgb_hex[4:6], 16)
                    # Dark green: G channel should be present and dominate, overall dark
                    if g > r and g > b and g <= 200:
                        font_ok = True
                        print(f"  Font color: {font_rgb} — dark green (R={r}, G={g}, B={b})")
                    elif g > r and g > b:
                        font_ok = True
                        print(f"  Font color: {font_rgb} — green (R={r}, G={g}, B={b})")
                    else:
                        print(f"  Font color: {font_rgb} — NOT green (R={r}, G={g}, B={b})")
                else:
                    print(f"  Font color rgb is None/empty")
            else:
                print(f"  No font color in DXF")

            if fill_ok and font_ok:
                print(f"PASS: Component 3 — Green fill + dark green font (0.3 pts)")
                total_score += 0.3
            elif fill_ok:
                print(f"PARTIAL: Component 3 — Green fill but font color not dark green (0.15 pts)")
                total_score += 0.15
            elif font_ok:
                print(f"PARTIAL: Component 3 — Dark green font but fill not green (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Neither green fill nor dark green font found")
        else:
            print(f"FAIL: Component 3 — No DXF style in the matching rule")
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
