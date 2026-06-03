"""
Reward Script: Conditional formatting — Top 15 bold orange + Bottom 10 strikethrough gray
Task ID: calc_ggf_049
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.15): CF rules exist on range E2:E101
  - Component 2 (0.25): Top N rule exists with rank=15 and bottom=False
  - Component 3 (0.20): Top rule has bold orange font (FFFF8C00)
  - Component 4 (0.25): Bottom N rule exists with rank=10 and bottom=True
  - Component 5 (0.15): Bottom rule has strikethrough gray font (FF808080)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ggf_049'


def persist_app_state(domain: str):
    """Attempt to save any unsaved LibreOffice state."""
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
    Verify conditional formatting rules on E2:E101.
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

    # Collect all CF rules that cover E2:E101
    cf_rules_on_target = []
    for cf in ws.conditional_formatting:
        range_str = str(cf)
        # Check if the CF range covers E2:E101 (may be written as E2:E101 or similar)
        if 'E2' in range_str and 'E101' in range_str:
            for rule in cf.rules:
                cf_rules_on_target.append(rule)

    # Also check for individual CF entries that each target E2:E101
    if not cf_rules_on_target:
        for cf in ws.conditional_formatting:
            range_str = str(cf)
            # Broader check: the range includes column E rows 2-101
            if 'E2:E101' in range_str or 'e2:e101' in range_str.lower():
                for rule in cf.rules:
                    cf_rules_on_target.append(rule)

    # Categorize rules
    top_rule = None
    bottom_rule = None
    for rule in cf_rules_on_target:
        if getattr(rule, 'type', None) == 'top10':
            is_bottom = getattr(rule, 'bottom', False)
            if is_bottom:
                bottom_rule = rule
            else:
                top_rule = rule

    # Component 1: CF rules exist on E2:E101 (0.15 points)
    try:
        if len(cf_rules_on_target) >= 2:
            print(f"PASS: Component 1 — Found {len(cf_rules_on_target)} CF rules on E2:E101 (0.15 pts)")
            total_score += 0.15
        elif len(cf_rules_on_target) == 1:
            print(f"PARTIAL: Component 1 — Found only 1 CF rule on E2:E101, expected 2 (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 1 — No CF rules found on E2:E101")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Top N rule with rank=15 and bottom=False (0.25 points)
    try:
        if top_rule is not None:
            rank = getattr(top_rule, 'rank', None)
            if rank == 15:
                print(f"PASS: Component 2 — Top rule with rank=15, bottom=False (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — Top rule has rank={rank}, expected 15")
        else:
            print(f"FAIL: Component 2 — No top10 rule (bottom=False) found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Top rule has bold orange font (0.20 points)
    try:
        if top_rule is not None and hasattr(top_rule, 'dxf') and top_rule.dxf:
            dxf = top_rule.dxf
            font = dxf.font
            if font:
                is_bold = font.bold == True
                font_color = getattr(font.color, 'rgb', None) if font.color else None
                # Accept orange variants: FFFF8C00 (dark orange) or similar orange shades
                ORANGE_VARIANTS = ('FFFF8C00', '00FF8C00', 'FF8C00', 'FFFFA500', '00FFA500', 'FFFF6600', '00FF6600')
                fc_upper = font_color.upper() if font_color else ''
                is_orange = fc_upper in ORANGE_VARIANTS

                if is_bold and is_orange:
                    print(f"PASS: Component 3 — Top rule: bold=True, color={font_color} (orange) (0.20 pts)")
                    total_score += 0.20
                elif is_bold:
                    print(f"PARTIAL: Component 3 — Top rule: bold=True but color={font_color} not orange (0.10 pts)")
                    total_score += 0.10
                elif is_orange:
                    print(f"PARTIAL: Component 3 — Top rule: color is orange but bold={font.bold} (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 3 — Top rule: bold={font.bold}, color={font_color}")
            else:
                print(f"FAIL: Component 3 — Top rule has no font in dxf")
        else:
            print(f"FAIL: Component 3 — No top rule or no dxf style")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Bottom N rule with rank=10 and bottom=True (0.25 points)
    try:
        if bottom_rule is not None:
            rank = getattr(bottom_rule, 'rank', None)
            if rank == 10:
                print(f"PASS: Component 4 — Bottom rule with rank=10, bottom=True (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — Bottom rule has rank={rank}, expected 10")
        else:
            print(f"FAIL: Component 4 — No top10 rule (bottom=True) found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Bottom rule has strikethrough gray font (0.15 points)
    try:
        if bottom_rule is not None and hasattr(bottom_rule, 'dxf') and bottom_rule.dxf:
            dxf = bottom_rule.dxf
            font = dxf.font
            if font:
                is_strike = font.strike == True
                font_color = getattr(font.color, 'rgb', None) if font.color else None
                GRAY_VARIANTS = ('FF808080', '00808080', '808080', 'FFA9A9A9', 'FF999999', 'FF888888', 'FF777777', 'FF666666')
                fc_upper = font_color.upper() if font_color else ''
                is_gray = fc_upper in GRAY_VARIANTS

                if is_strike and is_gray:
                    print(f"PASS: Component 5 — Bottom rule: strike=True, color={font_color} (gray) (0.15 pts)")
                    total_score += 0.15
                elif is_strike:
                    print(f"PARTIAL: Component 5 — Bottom rule: strike=True but color={font_color} not gray (0.07 pts)")
                    total_score += 0.07
                elif is_gray:
                    print(f"PARTIAL: Component 5 — Bottom rule: color is gray but strike={font.strike} (0.07 pts)")
                    total_score += 0.07
                else:
                    print(f"FAIL: Component 5 — Bottom rule: strike={font.strike}, color={font_color}")
            else:
                print(f"FAIL: Component 5 — Bottom rule has no font in dxf")
        else:
            print(f"FAIL: Component 5 — No bottom rule or no dxf style")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
