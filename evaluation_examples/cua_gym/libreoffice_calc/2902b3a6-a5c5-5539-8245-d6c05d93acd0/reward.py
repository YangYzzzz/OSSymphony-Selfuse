"""
Reward Script: Conditional formatting rule on Employees sheet
Task ID: calc_gg2_009
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30): CF rule exists on correct range A2:G101
  Component 2 (0.35): Formula is =$G2="Engineering" (expression type)
  Component 3 (0.35): Fill style is solid light blue
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gg2_009'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice edits before verification."""
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


def normalize_formula(f):
    """Normalize a CF formula for comparison: strip whitespace, uppercase."""
    return f.strip().upper().replace(" ", "")


def is_light_blue(rgb_str):
    """
    Check if a color is 'light blue'.
    Accept FFADD8E6 (LightBlue CSS) and similar light-blue shades.
    We parse the RGB components and verify:
      - Blue channel is high (>= 0xC0)
      - Red and Green are moderate-to-high (light tint)
      - Blue >= Red and Blue >= Green (it's blue-ish)
    Also accept exact match to common light blue codes.
    """
    if not rgb_str or len(rgb_str) < 6:
        return False
    # Strip alpha if 8-char ARGB
    hex_rgb = rgb_str[-6:]  # last 6 chars = RRGGBB
    try:
        r = int(hex_rgb[0:2], 16)
        g = int(hex_rgb[2:4], 16)
        b = int(hex_rgb[4:6], 16)
    except ValueError:
        return False

    # Known light blue values
    known_light_blues = {
        "ADD8E6",  # CSS LightBlue
        "BDD7EE",  # Excel light blue
        "9BC2E6",  # Excel accent blue lighter
        "D6E4F0",  # very light blue
        "DAEEF3",  # light blue tint
        "CCE5FF",  # light blue
        "B4C6E7",  # blue tint
    }
    if hex_rgb.upper() in known_light_blues:
        return True

    # Heuristic: light blue has high blue, relatively high R and G (light), blue dominant
    if b >= 180 and r >= 100 and g >= 100 and b >= r and b >= g:
        return True

    return False


def verify_task(file_path):
    """
    Verify conditional formatting rule on Employees sheet.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Employees sheet must exist
    if 'Employees' not in wb.sheetnames:
        print("FAIL: 'Employees' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Employees']

    # Gather all CF rules
    cf_list = list(ws.conditional_formatting)
    print(f"INFO: Found {len(cf_list)} conditional formatting rule set(s)")

    # Find CF rules that cover A2:G101 range
    target_range_str = "A2:G101"
    matching_cf = None
    matching_rule = None

    for cf in cf_list:
        cf_range_str = str(cf).strip()
        for rule in cf.rules:
            # Check if it's an expression/formula type rule
            if rule.type == 'expression' and rule.formula:
                formula_str = rule.formula[0] if isinstance(rule.formula, (list, tuple)) else str(rule.formula)
                normalized = normalize_formula(formula_str)
                # Check if formula references $G and "Engineering"
                if '$G' in normalized.upper() and 'ENGINEERING' in normalized.upper():
                    matching_cf = cf
                    matching_rule = rule
                    break
        if matching_rule:
            break

    # Component 1: CF rule exists on correct range A2:G101 (0.30 points)
    try:
        if matching_cf is not None:
            # Extract actual cell ranges from the ConditionalFormatting object
            # matching_cf.cells gives us a CellRange or MultiCellRange
            try:
                cf_cells = matching_cf.cells
                # Convert to comparable form
                from openpyxl.utils import range_boundaries
                # cf_cells may be a MultiCellRange; iterate over its ranges
                range_ok = False
                for cr in cf_cells.ranges if hasattr(cf_cells, 'ranges') else [cf_cells]:
                    min_col, min_row, max_col, max_row = range_boundaries(str(cr))
                    if min_col == 1 and min_row == 2 and max_col == 7 and max_row == 101:
                        range_ok = True
                        break
                if range_ok:
                    print(f"PASS: Component 1 — CF rule covers correct range A2:G101 (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"PARTIAL: Component 1 — CF rule found but range {cf_cells} != A2:G101 (0.15 pts)")
                    total_score += 0.15
            except Exception as parse_e:
                # Fallback: check string representation
                cf_str = str(matching_cf)
                if 'A2:G101' in cf_str:
                    print(f"PASS: Component 1 — CF rule on A2:G101 (string match) (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"PARTIAL: Component 1 — CF rule found but range parse error: {parse_e} (0.15 pts)")
                    total_score += 0.15
        else:
            if len(cf_list) > 0:
                print(f"FAIL: Component 1 — CF rules exist but none match Engineering formula")
            else:
                print(f"FAIL: Component 1 — No conditional formatting rules found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Formula is =$G2="Engineering" (0.35 points)
    try:
        if matching_rule is not None:
            formula_str = matching_rule.formula[0] if isinstance(matching_rule.formula, (list, tuple)) else str(matching_rule.formula)
            normalized = normalize_formula(formula_str)
            expected_normalized = normalize_formula('$G2="Engineering"')

            if normalized == expected_normalized:
                print(f"PASS: Component 2 — Formula is exactly {formula_str} (0.35 pts)")
                total_score += 0.35
            else:
                # Check if it's close (e.g. uses $G$2 instead of $G2, or different quoting)
                if '$G' in normalized and 'ENGINEERING' in normalized and '=' in normalized:
                    print(f"PARTIAL: Component 2 — Formula {formula_str} is close but not exact match to =$G2=\"Engineering\" (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 2 — Formula {formula_str} does not match expected")
        else:
            print(f"FAIL: Component 2 — No matching expression rule found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Fill style is solid light blue (0.35 points)
    try:
        if matching_rule is not None and matching_rule.dxf is not None:
            dxf = matching_rule.dxf
            if dxf.fill is not None:
                fill = dxf.fill
                pattern_type = fill.patternType
                fg_rgb = None
                try:
                    if fill.fgColor and fill.fgColor.rgb:
                        fg_rgb = str(fill.fgColor.rgb)
                except Exception:
                    pass

                # Also check bgColor as fallback
                bg_rgb = None
                try:
                    if fill.bgColor and fill.bgColor.rgb:
                        bg_rgb = str(fill.bgColor.rgb)
                except Exception:
                    pass

                color_to_check = fg_rgb or bg_rgb
                is_solid = pattern_type == 'solid'
                is_blue = is_light_blue(color_to_check) if color_to_check else False

                if is_solid and is_blue:
                    print(f"PASS: Component 3 — Fill is solid light blue (color: {color_to_check}) (0.35 pts)")
                    total_score += 0.35
                elif is_blue and not is_solid:
                    print(f"PARTIAL: Component 3 — Color is light blue ({color_to_check}) but pattern is '{pattern_type}' not 'solid' (0.20 pts)")
                    total_score += 0.20
                elif is_solid and not is_blue:
                    print(f"PARTIAL: Component 3 — Fill is solid but color {color_to_check} is not light blue (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 3 — Fill: pattern={pattern_type}, fgColor={fg_rgb}, bgColor={bg_rgb}")
            else:
                print(f"FAIL: Component 3 — No fill defined in differential style")
        elif matching_rule is not None:
            print(f"FAIL: Component 3 — No differential style (dxf) on matching rule")
        else:
            print(f"FAIL: Component 3 — No matching rule to check fill")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
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
