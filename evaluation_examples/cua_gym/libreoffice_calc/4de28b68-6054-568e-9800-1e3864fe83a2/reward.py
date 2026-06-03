"""
Reward Script: Add a polynomial (degree 3) trendline to the scatter chart showing
               the relationship between age and memory test score.
Task ID: calc_chart_trendline_polynomial_060
Domain: libreoffice_calc
Scoring:
  - Component 1: Trendline exists on the scatter chart series             (0.3 pts)
  - Component 2: Trendline type is polynomial ('poly')                    (0.4 pts)
  - Component 3: Polynomial order/degree is 3 (cubic)                    (0.2 pts)
  - Component 4: Equation display is enabled (dispEq=True)               (0.1 pts)
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_trendline_polynomial_060'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must be loadable
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'MemoryStudy' sheet must exist
    if 'MemoryStudy' not in wb.sheetnames:
        print("CRITICAL: Sheet 'MemoryStudy' not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['MemoryStudy']

    # Precondition: chart must exist on the sheet
    if not ws._charts:
        print("CRITICAL: No charts found on 'MemoryStudy' sheet")
        print("REWARD: 0.0")
        return 0.0

    chart = ws._charts[0]

    # Precondition: at least one series in the chart
    if not chart.series:
        print("CRITICAL: No series found in chart")
        print("REWARD: 0.0")
        return 0.0

    series = chart.series[0]

    # Component 1: Trendline exists on the chart series (0.3 points)
    # The initial file has trendline=None; the golden file has a Trendline object.
    # This check FAILS on initial and PASSES on golden.
    try:
        trendline = series.trendline
        if trendline is not None:
            print(f"PASS: Component 1 — Trendline object exists on series (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No trendline found on series (expected a Trendline object, got None)")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check trendline existence: {e}")

    # Component 2: Trendline type is polynomial ('poly') (0.4 points)
    # The task requires a polynomial trendline, not linear/exponential/etc.
    # This check FAILS on initial (no trendline) and PASSES on golden.
    try:
        trendline = series.trendline
        if trendline is not None:
            tl_type = trendline.trendlineType
            if tl_type == 'poly':
                print(f"PASS: Component 2 — Trendline type is 'poly' (polynomial) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Expected trendline type 'poly', found: {repr(tl_type)}")
        else:
            print(f"FAIL: Component 2 — No trendline present to check type")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check trendline type: {e}")

    # Component 3: Polynomial order/degree is 3 (cubic) (0.2 points)
    # The task specifically requires degree 3, not degree 2 (quadratic) or other.
    # This check FAILS on initial and PASSES on golden (order=3).
    try:
        trendline = series.trendline
        if trendline is not None and trendline.trendlineType == 'poly':
            order = trendline.order
            if order == 3:
                print(f"PASS: Component 3 — Polynomial order is 3 (cubic) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Expected polynomial order 3, found: {repr(order)}")
        else:
            print(f"FAIL: Component 3 — Trendline is not polynomial; cannot verify order")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not check polynomial order: {e}")

    # Component 4: Equation display is enabled (dispEq=True) (0.1 points)
    # The task requires the trendline equation to be shown on the chart.
    # This check FAILS on initial and PASSES on golden (dispEq=True).
    try:
        trendline = series.trendline
        if trendline is not None:
            disp_eq = trendline.dispEq
            if disp_eq is True:
                print(f"PASS: Component 4 — Equation display enabled (dispEq=True) (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 4 — Expected dispEq=True, found: {repr(disp_eq)}")
        else:
            print(f"FAIL: Component 4 — No trendline present to check equation display")
    except Exception as e:
        print(f"ERROR: Component 4 — Could not check equation display setting: {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {round(total_score, 4)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
