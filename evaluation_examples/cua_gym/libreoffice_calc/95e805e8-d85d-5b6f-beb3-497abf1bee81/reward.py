"""
Reward Script: Rotate pie chart so 'Electronics' slice starts from 12 o'clock position
Task ID: calc_chart_pie_start_angle_051
Domain: libreoffice_calc
Scoring:
  Component 1: firstSliceAng changed from default (90 degrees) — 0.4 pts
  Component 2: firstSliceAng == 0 exactly (12 o'clock / top position) — 0.6 pts
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_pie_start_angle_051'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    Task: Rotate the pie chart so the 'Electronics' slice (largest) starts from
    the top (12 o'clock position). In xlsx/openpyxl terms, this means setting
    firstSliceAng to 0 (which corresponds to the top / 12 o'clock position).

    Initial state: firstSliceAng = 90 (3 o'clock / right side = default)
    Golden state:  firstSliceAng = 0 (12 o'clock / top position)

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: load the workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: check CategorySales sheet exists
    if 'CategorySales' not in wb.sheetnames:
        print("FAIL: 'CategorySales' sheet not found in workbook")
        print(f"Score: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['CategorySales']

    # Precondition: check that a pie chart exists
    charts = ws._charts
    if not charts:
        print("FAIL: No charts found on 'CategorySales' sheet")
        print(f"Score: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    pie_chart = None
    for chart in charts:
        if type(chart).__name__ == 'PieChart':
            pie_chart = chart
            break

    if pie_chart is None:
        print("FAIL: No PieChart found on 'CategorySales' sheet")
        print(f"Score: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: firstSliceAng has changed from the default 90 degrees (0.4 pts)
    # In the initial state, firstSliceAng = 90 (3 o'clock / default position).
    # Any rotation away from 90 indicates the agent attempted to rotate the chart.
    # This FAILS on initial (90 == 90 => not changed) and PASSES on golden (0 != 90).
    try:
        current_angle = pie_chart.firstSliceAng
        if current_angle is not None and float(current_angle) != 90.0:
            print(f"PASS: Component 1 — firstSliceAng changed from default 90 degrees "
                  f"(current value: {current_angle}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — firstSliceAng is still at default 90 degrees "
                  f"(current value: {current_angle}); chart has not been rotated")
    except Exception as e:
        print(f"ERROR: Component 1 — could not read firstSliceAng: {e}")

    # Component 2: firstSliceAng == 0 exactly (12 o'clock / top position) (0.6 pts)
    # The task specifically requires the Electronics slice to start from the top
    # (12 o'clock). In xlsx convention, 0 degrees = top position.
    # This FAILS on initial (90 != 0) and PASSES on golden (0 == 0).
    try:
        current_angle = pie_chart.firstSliceAng
        if current_angle is not None and float(current_angle) == 0.0:
            print(f"PASS: Component 2 — firstSliceAng == 0 (12 o'clock / top position) "
                  f"(current value: {current_angle}) (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 2 — expected firstSliceAng == 0 (12 o'clock), "
                  f"found: {current_angle}")
    except Exception as e:
        print(f"ERROR: Component 2 — could not verify firstSliceAng == 0: {e}")

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
