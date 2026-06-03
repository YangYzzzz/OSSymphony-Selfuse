"""
Reward Script: Add axis titles to the existing line chart
Task ID: calc_chart_axis_titles_018
Domain: libreoffice_calc
Scoring:
  Component 1: X-axis title set to 'Month'               — 0.5 points
  Component 2: Y-axis title set to 'Temperature (°C)'    — 0.5 points
  Total: 1.0

Precondition gate (not scored):
  - File must exist and be loadable
  - 'Climate' sheet must be present
  - Chart must exist on the 'Climate' sheet
  - Existing chart title 'Monthly Average Temperature' must be preserved

Only task-introduced changes are scored:
  - Initial file has x_axis.title=None and y_axis.title=None
  - Golden file has x_axis.title='Month' and y_axis.title='Temperature (°C)'
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_axis_titles_018'


def get_title_text(title_obj):
    """
    Extract the text string from an openpyxl chart title/axis title object.
    Navigates: title.tx.rich.p[0].r[0].t
    Returns the text string, or None if not set or extraction fails.
    """
    if title_obj is None:
        return None
    try:
        if hasattr(title_obj, 'tx') and title_obj.tx:
            rich = title_obj.tx.rich
            if rich and rich.p:
                for para in rich.p:
                    if para.r:
                        for run in para.r:
                            if hasattr(run, 't') and run.t:
                                return run.t
    except Exception:
        pass
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: load the workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: 'Climate' sheet must exist
    if 'Climate' not in wb.sheetnames:
        print("CRITICAL: 'Climate' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Climate']

    # Precondition gate: chart must exist on 'Climate' sheet
    if not hasattr(ws, '_charts') or len(ws._charts) == 0:
        print("CRITICAL: No charts found on 'Climate' sheet")
        print("REWARD: 0.0")
        return 0.0

    chart = ws._charts[0]

    # Precondition gate: original chart title must be intact (not scored)
    chart_title_text = get_title_text(chart.title)
    if chart_title_text != 'Monthly Average Temperature':
        print(f"WARNING: Original chart title changed. Expected 'Monthly Average Temperature', found: {repr(chart_title_text)}")
        # Not a hard gate for scoring — the task only asks to ADD axis titles

    # Component 1: X-axis title set to 'Month' (0.5 points)
    # Initial file: x_axis.title is None → FAILS here
    # Golden file: x_axis.title text is 'Month' → PASSES here
    try:
        x_title = get_title_text(chart.x_axis.title)
        if x_title is not None and x_title.strip() == 'Month':
            print(f"PASS: Component 1 — X-axis title is 'Month' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected X-axis title 'Month', found: {repr(x_title)}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check x_axis.title: {e}")

    # Component 2: Y-axis title set to 'Temperature (°C)' (0.5 points)
    # Initial file: y_axis.title is None → FAILS here
    # Golden file: y_axis.title text is 'Temperature (°C)' → PASSES here
    try:
        y_title = get_title_text(chart.y_axis.title)
        expected_y = 'Temperature (\u00b0C)'
        if y_title is not None and y_title.strip() == expected_y:
            print(f"PASS: Component 2 — Y-axis title is 'Temperature (\u00b0C)' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — Expected Y-axis title 'Temperature (\u00b0C)', found: {repr(y_title)}")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check y_axis.title: {e}")

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
