"""
Reward Script: Conditional formatting with formula on C2:C45
Task ID: calc_gcv_022
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): CF rule exists targeting C2:C45
  Component 2 (0.3): Formula is C2>B2*1.2 (expression type)
  Component 3 (0.2): Fill background is purple #7030A0 (ARGB FF7030A0)
  Component 4 (0.2): Font color is white #FFFFFF (ARGB 00FFFFFF)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_022'


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
    Verify conditional formatting task completion with progressive scoring.
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

    # Collect all conditional formatting rules
    cf_list = list(ws.conditional_formatting)

    # We need to find a CF rule that covers C2:C45 with formula C2>B2*1.2
    # and has purple fill + white font
    matched_rule = None
    matched_range = None

    for cf in cf_list:
        range_str = str(cf).strip()
        for rule in cf.rules:
            if rule.type == 'expression' and rule.formula:
                matched_rule = rule
                matched_range = range_str
                break
        if matched_rule:
            break

    # Component 1: CF rule exists targeting C2:C45 (0.3 points)
    try:
        if matched_rule is not None:
            # Check that the range covers C2:C45
            # Normalize: the range string might be "C2:C45" or "<ConditionalFormatting C2:C45>"
            range_upper = matched_range.upper()
            if 'C2:C45' in range_upper or 'C2:C45' in range_upper.replace(' ', ''):
                print(f"PASS: Component 1 — CF rule found on range C2:C45 (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — CF rule found but range is '{matched_range}', expected C2:C45")
        else:
            print(f"FAIL: Component 1 — No expression-type conditional formatting rule found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Formula is C2>B2*1.2 (0.3 points)
    try:
        if matched_rule is not None and matched_rule.formula:
            formula_str = matched_rule.formula[0] if isinstance(matched_rule.formula, list) else str(matched_rule.formula)
            # Normalize: remove spaces and uppercase
            normalized = formula_str.upper().replace(' ', '')
            expected_variants = ['C2>B2*1.2', 'C2>(B2*1.2)', 'C2>1.2*B2', 'C2>(1.2*B2)']
            formula_matched = any(normalized == v.upper().replace(' ', '') for v in expected_variants)
            if formula_matched:
                print(f"PASS: Component 2 — Formula is '{formula_str}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Formula is '{formula_str}', expected C2>B2*1.2")
        else:
            print(f"FAIL: Component 2 — No formula found in rule")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Fill background is purple #7030A0 (0.2 points)
    try:
        if matched_rule is not None and matched_rule.dxf and matched_rule.dxf.fill:
            fill = matched_rule.dxf.fill
            fg_rgb = getattr(fill.fgColor, 'rgb', None)
            # Accept both FF7030A0 (standard ARGB) and variations
            if fg_rgb is not None:
                fg_upper = str(fg_rgb).upper()
                if '7030A0' in fg_upper:
                    print(f"PASS: Component 3 — Fill color is {fg_rgb} (purple) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — Fill color is {fg_rgb}, expected FF7030A0 (purple)")
            else:
                print(f"FAIL: Component 3 — Fill fgColor.rgb is None")
        else:
            print(f"FAIL: Component 3 — No fill defined in CF rule")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Font color is white #FFFFFF (0.2 points)
    try:
        if matched_rule is not None and matched_rule.dxf and matched_rule.dxf.font:
            font = matched_rule.dxf.font
            font_color_rgb = getattr(font.color, 'rgb', None)
            if font_color_rgb is not None:
                fc_upper = str(font_color_rgb).upper()
                if 'FFFFFF' in fc_upper:
                    print(f"PASS: Component 4 — Font color is {font_color_rgb} (white) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 4 — Font color is {font_color_rgb}, expected white (FFFFFF)")
            else:
                print(f"FAIL: Component 4 — Font color.rgb is None")
        else:
            print(f"FAIL: Component 4 — No font defined in CF rule")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
