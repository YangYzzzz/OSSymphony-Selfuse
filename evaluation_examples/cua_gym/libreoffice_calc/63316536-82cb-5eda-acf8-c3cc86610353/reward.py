"""
Reward Script: Freeze the header row in all five regional sheets
Task ID: calc_sht_freeze_row_003
Domain: libreoffice_calc

Task: Freeze the header row (row 1) in all five regional sheets —
      APAC, EMEA, AMER, LATAM, MEA — so users can scroll without losing context.
      Global Summary should remain unchanged (no freeze).

Scoring Rubric (5 independent components, 0.2 pts each = 1.0 total):
  Component 1: APAC sheet has freeze_panes == 'A2'   (0.2 pts)
  Component 2: EMEA sheet has freeze_panes == 'A2'   (0.2 pts)
  Component 3: AMER sheet has freeze_panes == 'A2'   (0.2 pts)
  Component 4: LATAM sheet has freeze_panes == 'A2'  (0.2 pts)
  Component 5: MEA sheet has freeze_panes == 'A2'    (0.2 pts)

Each component FAILS on the initial file (freeze_panes is None on all sheets)
and PASSES on the golden file (freeze_panes is 'A2' on each regional sheet).
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_sht_freeze_row_003'

# The five regional sheets that must have their header row frozen at row 2
REGIONAL_SHEETS = ['APAC', 'EMEA', 'AMER', 'LATAM', 'MEA']
EXPECTED_FREEZE = 'A2'
POINTS_PER_SHEET = 0.2


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Checks that each of the five regional sheets has freeze_panes == 'A2',
    meaning row 1 (the header row) is frozen.
    """
    total_score = 0.0

    # Precondition: load the workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file {}: {}".format(file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Precondition: verify expected sheets exist
    missing_sheets = [s for s in REGIONAL_SHEETS if s not in wb.sheetnames]
    if missing_sheets:
        print("CRITICAL: Missing expected sheets: {}".format(missing_sheets))
        print("REWARD: 0.0")
        return 0.0

    # Component 1: APAC sheet has freeze_panes == 'A2' (0.2 points)
    try:
        ws = wb['APAC']
        actual = ws.freeze_panes
        if actual == EXPECTED_FREEZE:
            print("PASS: Component 1 — APAC freeze_panes == 'A2' ({} pts)".format(POINTS_PER_SHEET))
            total_score += POINTS_PER_SHEET
        else:
            print("FAIL: Component 1 — APAC expected freeze_panes='A2', found: {}".format(repr(actual)))
    except Exception as e:
        print("ERROR: Component 1 — APAC check failed: {}".format(e))

    # Component 2: EMEA sheet has freeze_panes == 'A2' (0.2 points)
    try:
        ws = wb['EMEA']
        actual = ws.freeze_panes
        if actual == EXPECTED_FREEZE:
            print("PASS: Component 2 — EMEA freeze_panes == 'A2' ({} pts)".format(POINTS_PER_SHEET))
            total_score += POINTS_PER_SHEET
        else:
            print("FAIL: Component 2 — EMEA expected freeze_panes='A2', found: {}".format(repr(actual)))
    except Exception as e:
        print("ERROR: Component 2 — EMEA check failed: {}".format(e))

    # Component 3: AMER sheet has freeze_panes == 'A2' (0.2 points)
    try:
        ws = wb['AMER']
        actual = ws.freeze_panes
        if actual == EXPECTED_FREEZE:
            print("PASS: Component 3 — AMER freeze_panes == 'A2' ({} pts)".format(POINTS_PER_SHEET))
            total_score += POINTS_PER_SHEET
        else:
            print("FAIL: Component 3 — AMER expected freeze_panes='A2', found: {}".format(repr(actual)))
    except Exception as e:
        print("ERROR: Component 3 — AMER check failed: {}".format(e))

    # Component 4: LATAM sheet has freeze_panes == 'A2' (0.2 points)
    try:
        ws = wb['LATAM']
        actual = ws.freeze_panes
        if actual == EXPECTED_FREEZE:
            print("PASS: Component 4 — LATAM freeze_panes == 'A2' ({} pts)".format(POINTS_PER_SHEET))
            total_score += POINTS_PER_SHEET
        else:
            print("FAIL: Component 4 — LATAM expected freeze_panes='A2', found: {}".format(repr(actual)))
    except Exception as e:
        print("ERROR: Component 4 — LATAM check failed: {}".format(e))

    # Component 5: MEA sheet has freeze_panes == 'A2' (0.2 points)
    try:
        ws = wb['MEA']
        actual = ws.freeze_panes
        if actual == EXPECTED_FREEZE:
            print("PASS: Component 5 — MEA freeze_panes == 'A2' ({} pts)".format(POINTS_PER_SHEET))
            total_score += POINTS_PER_SHEET
        else:
            print("FAIL: Component 5 — MEA expected freeze_panes='A2', found: {}".format(repr(actual)))
    except Exception as e:
        print("ERROR: Component 5 — MEA check failed: {}".format(e))

    final_score = min(round(total_score, 2), 1.0)
    print("\nScore: {}/1.0".format(total_score))
    print("REWARD: {}".format(final_score))
    return final_score


# Default: test against golden file (path on VM)
file_path = '{}/{}_initial.xlsx'.format(WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print("File not found: {}".format(file_path))
    print("REWARD: 0.0")
else:
    verify_task(file_path)
