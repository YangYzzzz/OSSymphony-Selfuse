"""
Reward Script: Project status tracker with conditional formatting and frozen rows
Task ID: calc_gsd_013
Domain: libreoffice_calc
Scoring:
  - Component 1: Freeze panes at A3 (rows 1-2 frozen) — 0.30 pts
  - Component 2: Conditional formatting rule for 'Complete' = green (#70AD47) on G3:G42 — 0.25 pts
  - Component 3: Conditional formatting rule for 'In Progress' = yellow (#FFFF00) on G3:G42 — 0.25 pts
  - Component 4: Conditional formatting rule for 'Blocked' = red (#FF0000) on G3:G42 — 0.20 pts
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gsd_013'


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

    # Precondition: 'Projects' sheet must exist
    if 'Projects' not in wb.sheetnames:
        print("CRITICAL: 'Projects' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Projects']

    # Component 1: Freeze panes set to A3 (rows 1-2 frozen) (0.30 points)
    try:
        freeze = ws.freeze_panes
        if freeze == 'A3':
            print(f"PASS: Component 1 — Freeze panes is 'A3' (rows 1-2 frozen) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Expected freeze panes 'A3', found: {freeze}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Gather conditional formatting rules that apply to G3:G42
    # We need to find rules for Complete=green, In Progress=yellow, Blocked=red
    cf_rules_found = {'complete_green': False, 'in_progress_yellow': False, 'blocked_red': False}

    try:
        for cf in ws.conditional_formatting:
            cf_range = str(cf).upper()
            # Check if the range covers G3:G42 (could be exact or contain it)
            if 'G3' in cf_range and 'G42' in cf_range:
                for rule in cf.rules:
                    if rule.type == 'cellIs' and rule.operator == 'equal':
                        formula_str = str(rule.formula).upper() if rule.formula else ''
                        fill_color = None
                        if rule.dxf and rule.dxf.fill and rule.dxf.fill.fgColor:
                            try:
                                fill_color = rule.dxf.fill.fgColor.rgb
                            except Exception:
                                pass

                        # Check Complete = green
                        if '"COMPLETE"' in formula_str:
                            if fill_color and fill_color.upper() in ('FF70AD47', '0070AD47', '70AD47'):
                                cf_rules_found['complete_green'] = True
                            else:
                                print(f"  INFO: 'Complete' rule found but color is {fill_color}, expected FF70AD47")

                        # Check In Progress = yellow
                        if '"IN PROGRESS"' in formula_str:
                            if fill_color and fill_color.upper() in ('FFFFFF00', '00FFFF00', 'FFFF00'):
                                cf_rules_found['in_progress_yellow'] = True
                            else:
                                print(f"  INFO: 'In Progress' rule found but color is {fill_color}, expected FFFFFF00")

                        # Check Blocked = red
                        if '"BLOCKED"' in formula_str:
                            if fill_color and fill_color.upper() in ('FFFF0000', '00FF0000', 'FF0000'):
                                cf_rules_found['blocked_red'] = True
                            else:
                                print(f"  INFO: 'Blocked' rule found but color is {fill_color}, expected FFFF0000")
    except Exception as e:
        print(f"ERROR: Conditional formatting scan — {e}")

    # Component 2: Complete = green rule (0.25 points)
    if cf_rules_found['complete_green']:
        print(f"PASS: Component 2 — 'Complete' = green (#70AD47) conditional formatting on G3:G42 (0.25 pts)")
        total_score += 0.25
    else:
        print(f"FAIL: Component 2 — 'Complete' = green (#70AD47) conditional formatting not found on G3:G42")

    # Component 3: In Progress = yellow rule (0.25 points)
    if cf_rules_found['in_progress_yellow']:
        print(f"PASS: Component 3 — 'In Progress' = yellow (#FFFF00) conditional formatting on G3:G42 (0.25 pts)")
        total_score += 0.25
    else:
        print(f"FAIL: Component 3 — 'In Progress' = yellow (#FFFF00) conditional formatting not found on G3:G42")

    # Component 4: Blocked = red rule (0.20 points)
    if cf_rules_found['blocked_red']:
        print(f"PASS: Component 4 — 'Blocked' = red (#FF0000) conditional formatting on G3:G42 (0.20 pts)")
        total_score += 0.20
    else:
        print(f"FAIL: Component 4 — 'Blocked' = red (#FF0000) conditional formatting not found on G3:G42")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
