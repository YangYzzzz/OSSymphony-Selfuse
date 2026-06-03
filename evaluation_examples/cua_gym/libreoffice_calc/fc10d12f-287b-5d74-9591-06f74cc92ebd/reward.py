"""
Reward Script: Alternating row shading via conditional formatting
Task ID: calc_gg3_017
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): CF rules exist on range covering A2:G31
  Component 2 (0.25): Odd-row rule with MOD(ROW(),2)=1 formula present
  Component 3 (0.25): Odd-row rule uses light blue fill (#D6EAF8)
  Component 4 (0.25): Even-row rule with MOD(ROW(),2)=0 and white fill (#FFFFFF)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gg3_017'


def persist_app_state(domain):
    """Save any unsaved LibreOffice state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify alternating row shading conditional formatting.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Roster' sheet must exist
    if 'Roster' not in wb.sheetnames:
        print("CRITICAL: 'Roster' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Roster']

    # Collect all conditional formatting rules
    cf_list = list(ws.conditional_formatting)
    all_rules = []
    matching_range_count = 0

    for cf in cf_list:
        cf_range_str = str(cf)
        # Check if this CF range covers A2:G31
        # We accept any range that includes A2:G31 (could be exact or larger)
        for rule in cf.rules:
            all_rules.append((cf_range_str, rule))

        # Check if the range covers A2:G31
        # Parse the range string - it could be "A2:G31" or similar
        if 'A2' in cf_range_str and 'G31' in cf_range_str:
            matching_range_count += 1

    # Component 1: CF rules exist on a range covering A2:G31 (0.25 points)
    try:
        if matching_range_count > 0 and len(all_rules) >= 2:
            print(f"PASS: Component 1 — CF rules found covering A2:G31 with {len(all_rules)} rules (0.25 pts)")
            total_score += 0.25
        elif len(all_rules) >= 2:
            # Rules exist but maybe on a different range notation
            print(f"PARTIAL: Component 1 — CF rules found but range may not match A2:G31 exactly. Ranges: {[r[0] for r in all_rules]}")
            # Still give partial if rules exist
        else:
            print(f"FAIL: Component 1 — Expected >= 2 CF rules covering A2:G31, found {len(all_rules)} total rules")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Identify the odd-row and even-row rules
    odd_rule = None
    even_rule = None
    for range_str, rule in all_rules:
        if rule.type == 'expression' and rule.formula:
            formula = rule.formula[0].upper().replace(' ', '')
            if 'MOD(ROW(),2)=1' in formula or 'MOD(ROW(),2)=1' in formula.replace('ROW()', 'ROW()'):
                odd_rule = rule
            elif 'MOD(ROW(),2)=0' in formula:
                even_rule = rule

    # Component 2: Odd-row rule with MOD(ROW(),2)=1 formula (0.25 points)
    try:
        if odd_rule is not None:
            print(f"PASS: Component 2 — Odd-row rule found with formula MOD(ROW(),2)=1 (0.25 pts)")
            total_score += 0.25
        else:
            # Check if maybe reversed
            formulas_found = [r.formula for _, r in all_rules if r.formula]
            print(f"FAIL: Component 2 — No rule with MOD(ROW(),2)=1 formula. Found formulas: {formulas_found}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Odd-row rule has light blue fill #D6EAF8 (0.25 points)
    try:
        if odd_rule is not None and odd_rule.dxf and odd_rule.dxf.fill:
            fill = odd_rule.dxf.fill
            fg_rgb = None
            try:
                fg_rgb = fill.fgColor.rgb
            except:
                pass
            bg_rgb = None
            try:
                bg_rgb = fill.bgColor.rgb
            except:
                pass

            # Check if the fill color is D6EAF8 (with FF alpha prefix)
            target_color = 'FFD6EAF8'
            if fg_rgb == target_color or bg_rgb == target_color:
                print(f"PASS: Component 3 — Odd-row fill is light blue #D6EAF8 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Odd-row fill color mismatch. fgColor={fg_rgb}, bgColor={bg_rgb}, expected {target_color}")
        else:
            print(f"FAIL: Component 3 — No fill found on odd-row rule")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Even-row rule with MOD(ROW(),2)=0 and white fill #FFFFFF (0.25 points)
    try:
        if even_rule is not None and even_rule.dxf and even_rule.dxf.fill:
            fill = even_rule.dxf.fill
            fg_rgb = None
            try:
                fg_rgb = fill.fgColor.rgb
            except:
                pass
            bg_rgb = None
            try:
                bg_rgb = fill.bgColor.rgb
            except:
                pass

            target_color = 'FFFFFFFF'
            if fg_rgb == target_color or bg_rgb == target_color:
                print(f"PASS: Component 4 — Even-row rule with MOD(ROW(),2)=0 and white fill #FFFFFF (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — Even-row fill color mismatch. fgColor={fg_rgb}, bgColor={bg_rgb}, expected {target_color}")
        elif even_rule is not None:
            print(f"FAIL: Component 4 — Even-row rule found but no fill defined")
        else:
            formulas_found = [r.formula for _, r in all_rules if r.formula]
            print(f"FAIL: Component 4 — No rule with MOD(ROW(),2)=0 formula. Found formulas: {formulas_found}")
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
