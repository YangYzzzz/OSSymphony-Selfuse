"""
Reward Script: Increase axis tick label font size to 12pt on both X and Y axes
Task ID: calc_chart_column_font_size_038
Domain: libreoffice_calc
Scoring:
  Component 1: X-axis tick label font size == 12pt (1200 in openpyxl units)  — 0.5 points
  Component 2: Y-axis tick label font size == 12pt (1200 in openpyxl units)  — 0.5 points
  Total: 1.0

Notes on openpyxl font size units:
  Font sizes in chart axis txPr are stored as hundredths of a point.
  9pt  = 900.0
  12pt = 1200.0
  The target size is 12pt = 1200.0 in these units.
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — reward script runs on the VM
TASK_ID = 'calc_chart_column_font_size_038'

TARGET_FONT_SIZE = 1200.0   # 12pt expressed in hundredths of a point
TARGET_PT = 12              # human-readable 12pt


def get_axis_tick_font_size(axis):
    """
    Extract the tick label font size from an openpyxl chart axis txPr.
    Returns the sz value (in hundredths of a point) or None if not set.
    """
    try:
        if axis.txPr is None:
            return None
        if not axis.txPr.p:
            return None
        for p in axis.txPr.p:
            if p.pPr and p.pPr.defRPr:
                sz = p.pPr.defRPr.sz
                if sz is not None:
                    return sz
    except Exception:
        return None
    return None


def verify_task(file_path):
    """
    Verify task completion: both X and Y axis tick label font sizes must be 12pt (1200 units).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load workbook — precondition gate
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'PrintReport' sheet exists
    if 'PrintReport' not in wb.sheetnames:
        print("CRITICAL: Sheet 'PrintReport' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['PrintReport']

    # Precondition: chart exists on the sheet
    if not ws._charts:
        print("CRITICAL: No chart found on 'PrintReport' sheet")
        print("REWARD: 0.0")
        return 0.0

    chart = ws._charts[0]

    # Component 1: X-axis tick label font size == 12pt (0.5 points)
    try:
        x_sz = get_axis_tick_font_size(chart.x_axis)
        if x_sz is not None and abs(x_sz - TARGET_FONT_SIZE) < 1.0:
            print(f"PASS: Component 1 — X-axis tick label font size is {x_sz} units ({x_sz/100:.0f}pt), expected {TARGET_PT}pt (0.5 pts)")
            total_score += 0.5
        else:
            actual_pt = f"{x_sz/100:.0f}pt" if x_sz is not None else "None/default"
            print(f"FAIL: Component 1 — X-axis tick label font size is {x_sz} ({actual_pt}), expected {TARGET_FONT_SIZE} ({TARGET_PT}pt)")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check X-axis font size: {e}")

    # Component 2: Y-axis tick label font size == 12pt (0.5 points)
    try:
        y_sz = get_axis_tick_font_size(chart.y_axis)
        if y_sz is not None and abs(y_sz - TARGET_FONT_SIZE) < 1.0:
            print(f"PASS: Component 2 — Y-axis tick label font size is {y_sz} units ({y_sz/100:.0f}pt), expected {TARGET_PT}pt (0.5 pts)")
            total_score += 0.5
        else:
            actual_pt = f"{y_sz/100:.0f}pt" if y_sz is not None else "None/default"
            print(f"FAIL: Component 2 — Y-axis tick label font size is {y_sz} ({actual_pt}), expected {TARGET_FONT_SIZE} ({TARGET_PT}pt)")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check Y-axis font size: {e}")

    final_score = min(total_score, 1.0)
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
