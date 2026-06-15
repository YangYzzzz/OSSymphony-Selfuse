"""
Reward Script: Add minor gridlines on the Y-axis to the existing line chart
Task ID: calc_chart_gridlines_023
Domain: libreoffice_calc
Scoring:
  Component 1: Y-axis minor gridlines added (0.6 pts) — minorGridlines is not None
  Component 2: Major gridlines preserved AND minor gridlines confirmed (0.4 pts)
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_gridlines_023'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Add minor gridlines on the Y-axis to the existing line chart.
    Initial state: y_axis.minorGridlines is None, y_axis.majorGridlines is set
    Golden state: y_axis.minorGridlines is a ChartLines object (not None), major gridlines still set
    """
    total_score = 0.0

    # Precondition gate: file must be loadable
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: 'Humidity' sheet must exist
    if 'Humidity' not in wb.sheetnames:
        print("FAIL: 'Humidity' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Humidity']

    # Precondition gate: chart must exist
    if not ws._charts:
        print("FAIL: No charts found in 'Humidity' sheet")
        print("REWARD: 0.0")
        return 0.0

    chart = ws._charts[0]

    # Component 1: Minor gridlines added to Y-axis (0.6 points)
    # This is the core change: initial has minorGridlines=None, golden has a ChartLines object
    try:
        minor_gl = chart.y_axis.minorGridlines
        if minor_gl is not None:
            print(f"PASS: Component 1 — Y-axis minor gridlines are present (type: {type(minor_gl).__name__}) (0.6 pts)")
            total_score += 0.6
        else:
            print("FAIL: Component 1 — Y-axis minor gridlines are None (not added)")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check y_axis.minorGridlines: {e}")

    # Component 2: Major gridlines preserved AND minor gridlines confirmed (0.4 points)
    # This compound check ensures the task was done correctly:
    #   - minor gridlines must be present (the new change)
    #   - major gridlines must still be present (unchanged from initial, but combined with minor check)
    # Since this requires minor gridlines to be present, it FAILS on initial file
    try:
        minor_gl = chart.y_axis.minorGridlines
        major_gl = chart.y_axis.majorGridlines
        if minor_gl is not None and major_gl is not None:
            print(f"PASS: Component 2 — Both minor and major Y-axis gridlines are present (0.4 pts)")
            total_score += 0.4
        elif minor_gl is None:
            print("FAIL: Component 2 — Minor gridlines not present; cannot confirm correct implementation")
        elif major_gl is None:
            print("FAIL: Component 2 — Minor gridlines added but major gridlines were removed (incorrect)")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check gridlines: {e}")

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
