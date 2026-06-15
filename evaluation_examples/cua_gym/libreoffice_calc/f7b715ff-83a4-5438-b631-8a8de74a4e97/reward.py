"""
Reward Script: Apply conditional formatting to range C2:C30 — top 20% green, bottom 20% red
Task ID: calc_gcv_055
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): Conditional formatting exists on range C2:C30
  Component 2 (0.35): Top 20% rule with green (#00B050) background
  Component 3 (0.35): Bottom 20% rule with red (#FF0000) background
  Component 4 (0.05): Exactly 2 rules (no extra rules)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_055'


def persist_app_state(domain):
    """Save any unsaved GUI state via Ctrl+S."""
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
    Verify conditional formatting on C2:C30:
      - Top 20% highlighted with green (#00B050)
      - Bottom 20% highlighted with red (#FF0000)
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

    # Collect all conditional formatting rules that cover C2:C30
    target_range_str = "C2:C30"
    matching_rules = []

    for cf in ws.conditional_formatting:
        cf_range = str(cf)
        # Check if the range matches C2:C30 (could be formatted differently)
        if "C2" in cf_range and "C30" in cf_range:
            for rule in cf.rules:
                matching_rules.append(rule)

    # Component 1: Conditional formatting exists on C2:C30 (0.25 points)
    try:
        if len(matching_rules) >= 2:
            print(f"PASS: Component 1 -- Found {len(matching_rules)} conditional formatting rules on C2:C30 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- Expected >= 2 conditional formatting rules on C2:C30, found {len(matching_rules)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Identify top and bottom rules
    top_rule = None
    bottom_rule = None

    for rule in matching_rules:
        if rule.type == "top10":
            is_bottom = getattr(rule, 'bottom', False)
            if is_bottom:
                bottom_rule = rule
            else:
                top_rule = rule

    # Component 2: Top 20% rule with green background (0.35 points)
    try:
        if top_rule is not None:
            rank = getattr(top_rule, 'rank', None)
            percent = getattr(top_rule, 'percent', None)
            fill_color = None
            if top_rule.dxf and top_rule.dxf.fill and top_rule.dxf.fill.fgColor:
                fill_color = top_rule.dxf.fill.fgColor.rgb

            sub_score = 0.0
            # Check it's top 20% by percentage
            if rank == 20 and percent is True:
                sub_score += 0.15
                print(f"PASS: Component 2a -- Top rule is rank=20, percent=True")
            else:
                print(f"FAIL: Component 2a -- Top rule rank={rank}, percent={percent}, expected rank=20, percent=True")

            # Check green fill color FF00B050
            if fill_color and fill_color.upper() == "FF00B050":
                sub_score += 0.20
                print(f"PASS: Component 2b -- Top rule fill color is {fill_color} (green #00B050)")
            else:
                print(f"FAIL: Component 2b -- Top rule fill color is {fill_color}, expected FF00B050")

            if sub_score > 0:
                total_score += sub_score
        else:
            print(f"FAIL: Component 2 -- No top 20% rule found (type=top10, bottom=False)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Bottom 20% rule with red background (0.35 points)
    try:
        if bottom_rule is not None:
            rank = getattr(bottom_rule, 'rank', None)
            percent = getattr(bottom_rule, 'percent', None)
            fill_color = None
            if bottom_rule.dxf and bottom_rule.dxf.fill and bottom_rule.dxf.fill.fgColor:
                fill_color = bottom_rule.dxf.fill.fgColor.rgb

            sub_score = 0.0
            # Check it's bottom 20% by percentage
            if rank == 20 and percent is True:
                sub_score += 0.15
                print(f"PASS: Component 3a -- Bottom rule is rank=20, percent=True")
            else:
                print(f"FAIL: Component 3a -- Bottom rule rank={rank}, percent={percent}, expected rank=20, percent=True")

            # Check red fill color FFFF0000
            if fill_color and fill_color.upper() == "FFFF0000":
                sub_score += 0.20
                print(f"PASS: Component 3b -- Bottom rule fill color is {fill_color} (red #FF0000)")
            else:
                print(f"FAIL: Component 3b -- Bottom rule fill color is {fill_color}, expected FFFF0000")

            if sub_score > 0:
                total_score += sub_score
        else:
            print(f"FAIL: Component 3 -- No bottom 20% rule found (type=top10, bottom=True)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Exactly 2 rules, no extras (0.05 points)
    try:
        if len(matching_rules) == 2:
            print(f"PASS: Component 4 -- Exactly 2 conditional formatting rules (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 -- Expected exactly 2 rules, found {len(matching_rules)}")
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
