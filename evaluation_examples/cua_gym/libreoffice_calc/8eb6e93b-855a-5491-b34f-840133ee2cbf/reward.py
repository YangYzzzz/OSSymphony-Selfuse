"""
Reward Script: Color monthly sheet tabs and freeze first row + first column
Task ID: calc_sht_multiop_003
Domain: libreoffice_calc

Scoring Rubric (total = 1.0):
  Component 1: January tab color == #4472C4 (FF4472C4)          — 0.15 pts
  Component 2: February tab color == #70AD47 (FF70AD47)         — 0.15 pts
  Component 3: March tab color == #ED7D31 (FFED7D31)            — 0.15 pts
  Component 4: January freeze panes == B2 (row1 + colA frozen)  — 0.15 pts
  Component 5: February freeze panes == B2                      — 0.15 pts
  Component 6: March freeze panes == B2                         — 0.15 pts
  Component 7: Summary sheet unchanged (no color, no freeze)    — 0.10 pts
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_sht_multiop_003'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: ensure the file can be loaded
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: required sheets must exist
    required_sheets = ['Summary', 'January', 'February', 'March']
    for sheet_name in required_sheets:
        if sheet_name not in wb.sheetnames:
            print(f"CRITICAL: Required sheet '{sheet_name}' not found in workbook")
            print("REWARD: 0.0")
            return 0.0

    # Component 1: January tab color == #4472C4 (0.15 points)
    # Initial: no tab color set; Golden: FF4472C4
    try:
        ws_jan = wb['January']
        tab_color = ws_jan.sheet_properties.tabColor
        actual_color = tab_color.rgb if tab_color else None
        expected_jan = 'FF4472C4'
        if actual_color and actual_color.upper() == expected_jan.upper():
            print(f"PASS: Component 1 — January tab color is {actual_color} (expected {expected_jan}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — January tab color expected {expected_jan}, found {actual_color}")
    except Exception as e:
        print(f"ERROR: Component 1 — January tab color check: {e}")

    # Component 2: February tab color == #70AD47 (0.15 points)
    # Initial: no tab color set; Golden: FF70AD47
    try:
        ws_feb = wb['February']
        tab_color = ws_feb.sheet_properties.tabColor
        actual_color = tab_color.rgb if tab_color else None
        expected_feb = 'FF70AD47'
        if actual_color and actual_color.upper() == expected_feb.upper():
            print(f"PASS: Component 2 — February tab color is {actual_color} (expected {expected_feb}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — February tab color expected {expected_feb}, found {actual_color}")
    except Exception as e:
        print(f"ERROR: Component 2 — February tab color check: {e}")

    # Component 3: March tab color == #ED7D31 (0.15 points)
    # Initial: no tab color set; Golden: FFED7D31
    try:
        ws_mar = wb['March']
        tab_color = ws_mar.sheet_properties.tabColor
        actual_color = tab_color.rgb if tab_color else None
        expected_mar = 'FFED7D31'
        if actual_color and actual_color.upper() == expected_mar.upper():
            print(f"PASS: Component 3 — March tab color is {actual_color} (expected {expected_mar}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — March tab color expected {expected_mar}, found {actual_color}")
    except Exception as e:
        print(f"ERROR: Component 3 — March tab color check: {e}")

    # Component 4: January freeze panes == B2 (first row + first column frozen) (0.15 points)
    # Initial: freeze_panes is None; Golden: freeze_panes == 'B2'
    try:
        ws_jan = wb['January']
        freeze = ws_jan.freeze_panes
        if freeze == 'B2':
            print(f"PASS: Component 4 — January freeze panes is B2 (row1+colA frozen) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — January freeze panes expected B2, found {freeze}")
    except Exception as e:
        print(f"ERROR: Component 4 — January freeze panes check: {e}")

    # Component 5: February freeze panes == B2 (0.15 points)
    # Initial: freeze_panes is None; Golden: freeze_panes == 'B2'
    try:
        ws_feb = wb['February']
        freeze = ws_feb.freeze_panes
        if freeze == 'B2':
            print(f"PASS: Component 5 — February freeze panes is B2 (row1+colA frozen) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — February freeze panes expected B2, found {freeze}")
    except Exception as e:
        print(f"ERROR: Component 5 — February freeze panes check: {e}")

    # Component 6: March freeze panes == B2 (0.15 points)
    # Initial: freeze_panes is None; Golden: freeze_panes == 'B2'
    try:
        ws_mar = wb['March']
        freeze = ws_mar.freeze_panes
        if freeze == 'B2':
            print(f"PASS: Component 6 — March freeze panes is B2 (row1+colA frozen) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — March freeze panes expected B2, found {freeze}")
    except Exception as e:
        print(f"ERROR: Component 6 — March freeze panes check: {e}")

    # Component 7: Summary sheet unchanged — no tab color, no freeze panes (0.10 points)
    # The task says Summary should have no changes; this is an integrity check.
    # Initial: no color, no freeze; Golden: same (no color, no freeze).
    # This component only awards points when ALL 6 task changes are present,
    # combined with the Summary being unmodified. We score it only if all
    # six task components already passed (making it a cap/integrity bonus).
    try:
        ws_sum = wb['Summary']
        tab_color_sum = ws_sum.sheet_properties.tabColor
        sum_color = tab_color_sum.rgb if tab_color_sum else None
        sum_freeze = ws_sum.freeze_panes

        # Summary must have no tab color and no freeze panes
        sum_unchanged = (sum_color is None) and (sum_freeze is None)

        # Award the 0.10 pts only if all 6 primary components also passed
        # (total_score will be 0.90 at this point if all passed)
        if sum_unchanged and abs(total_score - 0.90) < 0.001:
            print(f"PASS: Component 7 — Summary sheet unchanged (no color, no freeze) (0.10 pts)")
            total_score += 0.10
        elif not sum_unchanged:
            print(f"FAIL: Component 7 — Summary sheet was modified: color={sum_color}, freeze={sum_freeze}")
        else:
            # Sum unchanged but earlier components failed — don't award
            print(f"SKIP: Component 7 — Summary unchanged but earlier components failed; not awarding integrity bonus")
    except Exception as e:
        print(f"ERROR: Component 7 — Summary sheet check: {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
