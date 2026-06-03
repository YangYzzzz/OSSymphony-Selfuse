"""
Reward Script: Create a bubble chart where X-axis is market size, Y-axis is growth rate,
               and bubble size represents our current revenue in each segment.
Task ID: calc_chart_scatter_bubble_064
Domain: libreoffice_calc
Scoring:
  - Component 1: BubbleChart exists on 'MarketAnalysis' sheet (0.30)
  - Component 2: Chart title is 'Market Opportunity Analysis' (0.20)
  - Component 3: X-axis title is 'Market Size ($B)', Y-axis title is 'Growth Rate %' (0.20)
  - Component 4: 5 series present with bubble size from column D (Our Revenue) (0.20)
  - Component 5: Series X values from column B, Y values from column C (0.10)
"""

import os
import re

import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_scatter_bubble_064'


def get_title_text(title_obj):
    """Extract plain text from an openpyxl chart title object."""
    if title_obj is None:
        return None
    # Try tx.rich paragraph run
    try:
        return title_obj.tx.rich.p[0].r[0].t
    except Exception:
        pass
    # Fallback: regex on string repr
    try:
        s = str(title_obj)
        m = re.search(r"t='([^']+)'", s)
        if m:
            return m.group(1)
    except Exception:
        pass
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must load
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'MarketAnalysis' sheet must exist
    if 'MarketAnalysis' not in wb.sheetnames:
        print("CRITICAL: Sheet 'MarketAnalysis' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['MarketAnalysis']

    # Component 1: BubbleChart exists on 'MarketAnalysis' sheet (0.30 points)
    # Initial file has 0 charts; golden file has 1 BubbleChart.
    bubble_chart = None
    try:
        charts = ws._charts
        bubble_charts = [c for c in charts if type(c).__name__ == 'BubbleChart']
        if len(bubble_charts) >= 1:
            bubble_chart = bubble_charts[0]
            print(f"PASS: Component 1 — BubbleChart found on 'MarketAnalysis' (0.30 pts)")
            total_score += 0.30
        else:
            # Also accept ScatterChart as partial proxy, but strictly require BubbleChart
            if len(charts) >= 1:
                print(f"FAIL: Component 1 — Chart found but type is {type(charts[0]).__name__}, expected BubbleChart")
            else:
                print("FAIL: Component 1 — No charts found on 'MarketAnalysis' sheet")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Chart title is 'Market Opportunity Analysis' (0.20 points)
    try:
        if bubble_chart is None:
            print("SKIP: Component 2 — No BubbleChart available to check title")
        else:
            title_text = get_title_text(bubble_chart.title)
            if title_text and title_text.strip() == 'Market Opportunity Analysis':
                print(f"PASS: Component 2 — Chart title is 'Market Opportunity Analysis' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — Expected title 'Market Opportunity Analysis', found: {repr(title_text)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Axis titles correct — X='Market Size ($B)', Y='Growth Rate %' (0.20 points)
    try:
        if bubble_chart is None:
            print("SKIP: Component 3 — No BubbleChart available to check axis titles")
        else:
            x_title = get_title_text(bubble_chart.x_axis.title)
            y_title = get_title_text(bubble_chart.y_axis.title)
            x_ok = x_title and x_title.strip() == 'Market Size ($B)'
            y_ok = y_title and y_title.strip() == 'Growth Rate %'
            if x_ok and y_ok:
                print(f"PASS: Component 3 — X-axis='Market Size ($B)', Y-axis='Growth Rate %' (0.20 pts)")
                total_score += 0.20
            else:
                if not x_ok:
                    print(f"FAIL: Component 3 — X-axis title: expected 'Market Size ($B)', found: {repr(x_title)}")
                if not y_ok:
                    print(f"FAIL: Component 3 — Y-axis title: expected 'Growth Rate %', found: {repr(y_title)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 5 series with bubble size (zVal) referencing column D (Our Revenue) (0.20 points)
    # Each series must have zVal referencing column D of MarketAnalysis ($D$2 through $D$6)
    try:
        if bubble_chart is None:
            print("SKIP: Component 4 — No BubbleChart available to check series")
        else:
            series = bubble_chart.series
            if len(series) == 5:
                bad_bubble_count = 0
                for i, s in enumerate(series):
                    try:
                        z_ref = s.zVal.numRef.f
                        # Must reference column D of MarketAnalysis
                        if '$D$' not in z_ref and 'D' not in z_ref.upper():
                            print(f"FAIL: Component 4 — Series {i} bubbleSize ref '{z_ref}' does not reference column D")
                            bad_bubble_count += 1
                    except Exception as se:
                        print(f"FAIL: Component 4 — Series {i} has no valid bubbleSize (zVal) reference: {se}")
                        bad_bubble_count += 1
                if bad_bubble_count == 0:
                    print(f"PASS: Component 4 — 5 series, all bubble sizes reference column D (Our Revenue) (0.20 pts)")
                    total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Expected 5 series, found {len(series)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Series X values from column B (Market Size), Y values from column C (Growth Rate) (0.10 points)
    try:
        if bubble_chart is None:
            print("SKIP: Component 5 — No BubbleChart available to check series data mapping")
        else:
            series = bubble_chart.series
            if len(series) == 5:
                bad_xy_count = 0
                for i, s in enumerate(series):
                    try:
                        x_ref = s.xVal.numRef.f
                        y_ref = s.yVal.numRef.f
                        # X must reference column B, Y must reference column C
                        if '$B$' not in x_ref and 'B' not in x_ref.upper():
                            print(f"FAIL: Component 5 — Series {i} xVal ref '{x_ref}' does not reference column B")
                            bad_xy_count += 1
                        if '$C$' not in y_ref and 'C' not in y_ref.upper():
                            print(f"FAIL: Component 5 — Series {i} yVal ref '{y_ref}' does not reference column C")
                            bad_xy_count += 1
                    except Exception as se:
                        print(f"FAIL: Component 5 — Series {i} missing xVal/yVal reference: {se}")
                        bad_xy_count += 1
                if bad_xy_count == 0:
                    print(f"PASS: Component 5 — All series X values from column B, Y values from column C (0.10 pts)")
                    total_score += 0.10
            else:
                print(f"SKIP: Component 5 — Series count not 5, skipping axis mapping check")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {round(total_score, 2)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
