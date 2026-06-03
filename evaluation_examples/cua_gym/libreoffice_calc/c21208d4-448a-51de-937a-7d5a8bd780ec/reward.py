"""
Reward Script: Highlight URGENT cells with conditional formatting
Task ID: calc_gcv_016
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): Conditional formatting rule exists on B2:B40
  Component 2 (0.25): Rule uses formula LEFT(B2,6)="URGENT" (expression type)
  Component 3 (0.25): Fill is yellow (#FFFF00) with solid pattern
  Component 4 (0.25): Font is bold and red (#FF0000)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_016'


def persist_app_state(domain: str):
    """Best-effort save of any open LibreOffice document."""
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
    Verify task completion with progressive scoring.
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

    # Find the conditional formatting rule targeting B2:B40
    target_rule = None

    cf_list = list(ws.conditional_formatting)
    for cf in cf_list:
        range_str = str(cf).replace("<ConditionalFormatting ", "").rstrip(">").strip()
        # Normalize: check if B2:B40 is covered
        if "B2:B40" in range_str.upper().replace(" ", ""):
            if cf.rules:
                target_rule = cf.rules[0]
            break

    # Component 1: Conditional formatting rule exists on range B2:B40 (0.25 points)
    try:
        if target_rule is not None:
            print(f"PASS: Component 1 -- CF rule found on B2:B40 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- No conditional formatting rule found on B2:B40. "
                  f"Total CF rules: {len(cf_list)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Rule uses formula =LEFT(B2,6)="URGENT" (expression type) (0.25 points)
    try:
        if target_rule is not None:
            rule_type = target_rule.type
            rule_formula = target_rule.formula if hasattr(target_rule, 'formula') else []
            formula_str = rule_formula[0] if rule_formula else ""
            # Normalize for comparison
            norm_formula = formula_str.upper().replace(" ", "").replace("'", "").replace('"', '"')
            # Accept variants: LEFT(B2,6)="URGENT" or LEFT(B2,7)="URGENT:" etc.
            is_expression = (rule_type == "expression")
            has_left_formula = ('LEFT(B2,6)="URGENT"' in norm_formula.upper().replace('"', '"')
                               or 'LEFT(B2,6)="URGENT"' in norm_formula)
            if is_expression and has_left_formula:
                print(f"PASS: Component 2 -- Formula rule: {formula_str} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- Expected expression type with LEFT(B2,6)=\"URGENT\", "
                      f"got type={rule_type}, formula={formula_str}")
        else:
            print(f"FAIL: Component 2 -- No rule to check formula on")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Fill is yellow (#FFFF00) with solid pattern (0.25 points)
    try:
        if target_rule is not None and target_rule.dxf and target_rule.dxf.fill:
            fill = target_rule.dxf.fill
            fg_rgb = fill.fgColor.rgb if fill.fgColor else None
            pattern_type = fill.patternType
            # Accept FFFFFF00 (8-char ARGB) or FFFF00 (6-char)
            is_yellow = False
            if fg_rgb is not None:
                fg_upper = str(fg_rgb).upper()
                is_yellow = fg_upper in ("FFFFFF00", "00FFFF00", "FFFF00")
            is_solid = (pattern_type == "solid")
            if is_yellow and is_solid:
                print(f"PASS: Component 3 -- Fill yellow (#FFFF00) solid (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Expected yellow solid fill, got fg={fg_rgb}, pattern={pattern_type}")
        else:
            print(f"FAIL: Component 3 -- No fill defined in the CF rule DXF")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Font is bold and red (#FF0000) (0.25 points)
    try:
        if target_rule is not None and target_rule.dxf and target_rule.dxf.font:
            font = target_rule.dxf.font
            is_bold = (font.bold is True)
            font_color_rgb = font.color.rgb if font.color else None
            is_red = False
            if font_color_rgb is not None:
                fc_upper = str(font_color_rgb).upper()
                is_red = fc_upper in ("FFFF0000", "00FF0000", "FF0000")
            if is_bold and is_red:
                print(f"PASS: Component 4 -- Font bold=True, color red (#FF0000) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 -- Expected bold red font, got bold={is_bold}, color={font_color_rgb}")
        else:
            print(f"FAIL: Component 4 -- No font defined in the CF rule DXF")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
