"""
Reward Script: Employee Satisfaction Survey - 100% Stacked Horizontal Bar Chart
Task ID: calc_gcp_076
Domain: libreoffice_calc
Scoring:
  Component 1 (0.20): Chart exists on SurveyViz sheet
  Component 2 (0.20): Chart is horizontal bar type
  Component 3 (0.20): Chart uses percent-stacked grouping
  Component 4 (0.20): Chart has exactly 5 series (one per response category)
  Component 5 (0.20): Chart has legend and a title
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcp_076'


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

    # Precondition: SurveyViz sheet must exist
    if 'SurveyViz' not in wb.sheetnames:
        print("FAIL: Sheet 'SurveyViz' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['SurveyViz']
    charts = ws._charts

    # Component 1: Chart exists on SurveyViz sheet (0.20 points)
    try:
        if len(charts) >= 1:
            print(f"PASS: Component 1 — Found {len(charts)} chart(s) on SurveyViz (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — No charts found on SurveyViz (expected >= 1)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If no charts, remaining checks cannot proceed
    if len(charts) < 1:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    chart = charts[0]

    # Component 2: Chart is a horizontal bar chart (0.20 points)
    # In openpyxl: BarChart with type="bar" means horizontal bars
    try:
        is_bar_chart = type(chart).__name__ == 'BarChart'
        is_horizontal = False
        if is_bar_chart:
            is_horizontal = (chart.type == 'bar')

        if is_bar_chart and is_horizontal:
            print(f"PASS: Component 2 — Chart is horizontal bar (BarChart type='bar') (0.20 pts)")
            total_score += 0.20
        elif is_bar_chart:
            print(f"FAIL: Component 2 — Chart is BarChart but type='{chart.type}' (expected 'bar' for horizontal)")
        else:
            print(f"FAIL: Component 2 — Chart is {type(chart).__name__}, expected BarChart")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chart uses percent-stacked grouping (0.20 points)
    try:
        grouping = getattr(chart, 'grouping', None)
        if grouping == 'percentStacked':
            print(f"PASS: Component 3 — Chart grouping is percentStacked (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Chart grouping is '{grouping}', expected 'percentStacked'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Chart has exactly 5 series (one per response category) (0.20 points)
    try:
        series_count = len(chart.series)
        if series_count == 5:
            print(f"PASS: Component 4 — Chart has 5 series (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Chart has {series_count} series, expected 5")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Chart has a legend and a title (0.20 points)
    try:
        has_legend = chart.legend is not None
        has_title = chart.title is not None
        if has_legend and has_title:
            print(f"PASS: Component 5 — Chart has legend and title (0.20 pts)")
            total_score += 0.20
        elif has_legend:
            print(f"FAIL: Component 5 — Chart has legend but no title")
        elif has_title:
            print(f"FAIL: Component 5 — Chart has title but no legend")
        else:
            print(f"FAIL: Component 5 — Chart has neither legend nor title")
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
