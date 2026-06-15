"""
Reward Script: Delete erroneous blue conditional formatting rule
Task ID: calc_tbl_027
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.4): Exactly 3 CF rules remain (down from 4) AND no blue/catch-all rule
  - Component 2 (0.3): 3 rules AND red rule (lessThan 0) preserved
  - Component 3 (0.3): 3 rules AND yellow (between 0-50) + green (>50) rules preserved
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_tbl_027'


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

    ws = wb.active

    # Collect all CF rules from the worksheet
    all_rules = []
    cf_list = list(ws.conditional_formatting)
    for cf in cf_list:
        for rule in cf.rules:
            all_rules.append(rule)

    print(f"INFO: Found {len(all_rules)} total CF rules across {len(cf_list)} CF groups")

    # Helper: get all fill colors from a rule (both fgColor and bgColor)
    # LibreOffice may store the visible color in either field depending on save format
    def get_rule_fill_colors(rule):
        """Extract all fill color RGBs from a rule's differential style.
        Returns a set of non-trivial color strings found in fgColor and bgColor."""
        colors = set()
        try:
            if rule.dxf and rule.dxf.fill:
                fill = rule.dxf.fill
                if fill.fgColor and fill.fgColor.rgb:
                    c = str(fill.fgColor.rgb).upper()
                    if c != '00000000':  # skip transparent/default
                        colors.add(c)
                if fill.bgColor and fill.bgColor.rgb:
                    c = str(fill.bgColor.rgb).upper()
                    if c != '00000000':
                        colors.add(c)
        except Exception:
            pass
        return colors

    # Pre-compute: is the blue/catch-all rule absent?
    blue_present = False
    for rule in all_rules:
        colors = get_rule_fill_colors(rule)
        op = getattr(rule, 'operator', None)
        formula = getattr(rule, 'formula', None)
        if any('4472C4' in c for c in colors):
            blue_present = True
            break
        if (rule.type == 'cellIs' and op == 'greaterThanOrEqual'
                and formula and '-99999' in str(formula)):
            blue_present = True
            break

    # Pre-compute: rule count
    rule_count = len(all_rules)
    blue_deleted = (rule_count == 3 and not blue_present)

    # Component 1: Exactly 3 CF rules remain AND no blue/catch-all rule (0.4 points)
    # This is the core task change: deleting the blue rule reduces count from 4 to 3
    try:
        if blue_deleted:
            print(f"PASS: Component 1 — 3 CF rules, no blue/catch-all rule (0.4 pts)")
            total_score += 0.4
        else:
            if rule_count != 3:
                print(f"FAIL: Component 1 — Expected 3 CF rules, found {rule_count}")
            if blue_present:
                print(f"FAIL: Component 1 — Blue/catch-all CF rule still present")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Blue deleted AND red rule (lessThan 0) preserved (0.3 points)
    # Anchored to the task change: only scores if blue is gone AND red is intact
    try:
        if blue_deleted:
            red_found = False
            for rule in all_rules:
                colors = get_rule_fill_colors(rule)
                op = getattr(rule, 'operator', None)
                formula = getattr(rule, 'formula', None)
                if (rule.type == 'cellIs' and op == 'lessThan'
                        and formula and '0' in formula
                        and any('FF0000' in c for c in colors)):
                    red_found = True
                    break
            if red_found:
                print(f"PASS: Component 2 — Blue deleted AND red rule preserved (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Blue deleted but red rule (lessThan 0) missing")
        else:
            print(f"FAIL: Component 2 — Blue rule not deleted; cannot verify red preservation")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Blue deleted AND yellow+green rules preserved (0.3 points)
    # Anchored to the task change: only scores if blue is gone AND yellow+green intact
    try:
        if blue_deleted:
            yellow_found = False
            green_found = False
            for rule in all_rules:
                colors = get_rule_fill_colors(rule)
                op = getattr(rule, 'operator', None)
                if (rule.type == 'cellIs' and op == 'between'
                        and any('FFFF00' in c for c in colors)):
                    yellow_found = True
                if (rule.type == 'cellIs' and op == 'greaterThan'
                        and any('00B050' in c for c in colors)):
                    green_found = True

            if yellow_found and green_found:
                print(f"PASS: Component 3 — Blue deleted AND yellow+green rules preserved (0.3 pts)")
                total_score += 0.3
            else:
                details = []
                if not yellow_found:
                    details.append("yellow (between 0-50) missing")
                if not green_found:
                    details.append("green (>50) missing")
                print(f"FAIL: Component 3 — Blue deleted but {', '.join(details)}")
        else:
            print(f"FAIL: Component 3 — Blue rule not deleted; cannot verify yellow+green preservation")
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
