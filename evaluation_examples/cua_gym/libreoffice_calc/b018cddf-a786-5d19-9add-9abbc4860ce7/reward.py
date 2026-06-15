"""
Reward Script: Combination chart (bar + line) with secondary Y-axis
Task ID: calc_gg2_013
Domain: libreoffice_calc
Scoring:
  Component 1: Chart exists on Performance sheet (0.15 pts)
  Component 2: BarChart sub-chart with Revenue series (0.25 pts)
  Component 3: LineChart sub-chart with Growth Rate series (0.25 pts)
  Component 4: Secondary Y-axis for line chart (0.20 pts)
  Component 5: Legend present on chart (0.15 pts)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gg2_013'


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

    # Precondition: Performance sheet must exist
    if 'Performance' not in wb.sheetnames:
        print("FAIL: 'Performance' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Performance']

    # Component 1: At least one chart exists on Performance sheet (0.15 pts)
    # Initial state has 0 charts; golden state has 1 chart.
    try:
        chart_count = len(ws._charts)
        if chart_count >= 1:
            print(f"PASS: Component 1 — Chart exists on Performance sheet (count={chart_count}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — No charts found on Performance sheet")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If no charts, remaining components cannot pass
    if len(ws._charts) < 1:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    chart = ws._charts[0]

    # Component 2: Combination chart has a BarChart sub-chart with Revenue series (0.25 pts)
    # A combination chart in openpyxl stores sub-charts in chart._charts.
    # We look for a BarChart sub-chart whose series references column B (Revenue).
    try:
        from openpyxl.chart import BarChart as BarChartType
        bar_found = False
        sub_charts = chart._charts
        for sub in sub_charts:
            if isinstance(sub, BarChartType):
                # Check if any series references Revenue data (column B)
                for s in sub.series:
                    try:
                        title_ref = s.title.strRef.f if s.title and s.title.strRef else ''
                    except:
                        title_ref = ''
                    try:
                        val_ref = s.val.numRef.f if s.val and s.val.numRef else ''
                    except:
                        val_ref = ''
                    # Revenue series should reference B1 for title or B column for data
                    if 'B1' in title_ref or '$B$' in val_ref or '!B' in val_ref:
                        bar_found = True
                        print(f"PASS: Component 2 — BarChart sub-chart with Revenue series found (title_ref={title_ref}, val_ref={val_ref}) (0.25 pts)")
                        break
                if bar_found:
                    break
        if not bar_found:
            # Also check if the main chart itself is a BarChart with Revenue series
            # (non-combination chart case)
            if isinstance(chart, BarChartType) and len(sub_charts) <= 1:
                for s in chart.series:
                    try:
                        title_ref = s.title.strRef.f if s.title and s.title.strRef else ''
                    except:
                        title_ref = ''
                    try:
                        val_ref = s.val.numRef.f if s.val and s.val.numRef else ''
                    except:
                        val_ref = ''
                    if 'B1' in title_ref or '$B$' in val_ref:
                        bar_found = True
                        print(f"PASS: Component 2 — Main BarChart with Revenue series found (but not combination) (0.25 pts)")
                        break
            if not bar_found:
                print(f"FAIL: Component 2 — No BarChart sub-chart with Revenue series found")
        if bar_found:
            total_score += 0.25
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Combination chart has a LineChart sub-chart with Growth Rate series (0.25 pts)
    try:
        from openpyxl.chart import LineChart as LineChartType
        line_found = False
        sub_charts = chart._charts
        for sub in sub_charts:
            if isinstance(sub, LineChartType):
                for s in sub.series:
                    try:
                        title_ref = s.title.strRef.f if s.title and s.title.strRef else ''
                    except:
                        title_ref = ''
                    try:
                        val_ref = s.val.numRef.f if s.val and s.val.numRef else ''
                    except:
                        val_ref = ''
                    # Growth Rate series should reference C1 for title or C column for data
                    if 'C1' in title_ref or '$C$' in val_ref or '!C' in val_ref:
                        line_found = True
                        print(f"PASS: Component 3 — LineChart sub-chart with Growth Rate series found (title_ref={title_ref}, val_ref={val_ref}) (0.25 pts)")
                        break
                if line_found:
                    break
        if not line_found:
            print(f"FAIL: Component 3 — No LineChart sub-chart with Growth Rate series found")
        else:
            total_score += 0.25
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Secondary Y-axis exists for the line chart (0.20 pts)
    # In a combination chart, the line chart uses a different y-axis (axId != primary bar y-axis).
    # The bar chart uses axId pair [x, primary_y] and the line chart uses [x, secondary_y].
    try:
        from openpyxl.chart import BarChart as BarChartType
        from openpyxl.chart import LineChart as LineChartType
        secondary_axis_found = False
        bar_y_axes = set()
        line_y_axes = set()

        for sub in chart._charts:
            if isinstance(sub, BarChartType):
                # axId is a list; second element is typically the y-axis
                if hasattr(sub, 'axId') and len(sub.axId) >= 2:
                    bar_y_axes.add(sub.axId[1])
            elif isinstance(sub, LineChartType):
                if hasattr(sub, 'axId') and len(sub.axId) >= 2:
                    line_y_axes.add(sub.axId[1])

        # Secondary axis = line y-axis is different from bar y-axis
        if line_y_axes and bar_y_axes and line_y_axes != bar_y_axes:
            secondary_axis_found = True
            print(f"PASS: Component 4 — Secondary Y-axis found (bar y-axes={bar_y_axes}, line y-axes={line_y_axes}) (0.20 pts)")
            total_score += 0.20
        elif line_y_axes and not bar_y_axes:
            # Edge case: only line chart found, check if its axis differs from chart.y_axis
            primary_y_id = chart.y_axis.axId if hasattr(chart, 'y_axis') else None
            if primary_y_id and line_y_axes and primary_y_id not in line_y_axes:
                secondary_axis_found = True
                print(f"PASS: Component 4 — Secondary Y-axis found (primary={primary_y_id}, line={line_y_axes}) (0.20 pts)")
                total_score += 0.20
        if not secondary_axis_found:
            print(f"FAIL: Component 4 — No secondary Y-axis detected (bar_y={bar_y_axes}, line_y={line_y_axes})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Chart has a legend (0.15 pts)
    # The task requires the chart legend to show both series.
    try:
        if chart.legend is not None:
            print(f"PASS: Component 5 — Legend present on chart (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — No legend found on chart")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
