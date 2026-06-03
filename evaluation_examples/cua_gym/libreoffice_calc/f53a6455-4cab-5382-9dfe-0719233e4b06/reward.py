"""
Reward Script: Build an HR analytics dashboard with bar, pie, and line charts
Task ID: calc_hr_095
Domain: libreoffice_calc
Scoring:
  Component 1 — Dashboard has exactly 3 charts (0.15 pts)
  Component 2 — Bar chart exists with correct type and title (0.20 pts)
  Component 3 — Bar chart has 2 data series (hires + terminations) (0.10 pts)
  Component 4 — Pie chart exists with correct type and title (0.20 pts)
  Component 5 — Pie chart has 1 data series (headcount) (0.10 pts)
  Component 6 — Line chart exists with correct type and title (0.20 pts)
  Component 7 — Line chart has 1 data series (salary distribution) (0.05 pts)
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_hr_095'


def get_chart_title_text(chart):
    """Extract plain text title from a chart object."""
    try:
        if chart.title is None:
            return None
        # Navigate the rich text structure to get the title string
        tx = chart.title.tx
        if tx is not None and tx.rich is not None:
            parts = []
            for p in tx.rich.p:
                for r in p.r:
                    if r.t:
                        parts.append(r.t)
            if parts:
                return ''.join(parts)
        # Try strRef fallback
        if tx is not None and tx.strRef is not None:
            return str(tx.strRef)
    except Exception:
        pass
    return None


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

    # Precondition: Dashboard sheet must exist
    if 'Dashboard' not in wb.sheetnames:
        print("FAIL: 'Dashboard' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Dashboard']
    charts = ws._charts

    # Component 1: Dashboard has exactly 3 charts (0.15 pts)
    try:
        num_charts = len(charts)
        if num_charts == 3:
            print(f"PASS: Component 1 — Dashboard has 3 charts (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 3 charts, found {num_charts}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Classify charts by type
    bar_charts = []
    pie_charts = []
    line_charts = []

    for chart in charts:
        ctype = type(chart).__name__
        if ctype == 'BarChart':
            bar_charts.append(chart)
        elif ctype == 'PieChart':
            pie_charts.append(chart)
        elif ctype == 'LineChart':
            line_charts.append(chart)

    # Component 2: Bar chart exists with correct type and title (0.20 pts)
    try:
        if len(bar_charts) >= 1:
            bc = bar_charts[0]
            title_text = get_chart_title_text(bc)
            # Check title contains key words
            if title_text and 'hiring' in title_text.lower() and 'turnover' in title_text.lower():
                print(f"PASS: Component 2 — Bar chart with title '{title_text}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — Bar chart title mismatch. Expected 'Monthly Hiring vs Turnover', found: '{title_text}'")
        else:
            print("FAIL: Component 2 — No bar chart found on Dashboard")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Bar chart has 2 data series (0.10 pts)
    try:
        if len(bar_charts) >= 1:
            bc = bar_charts[0]
            series_count = len(bc.series)
            if series_count == 2:
                print(f"PASS: Component 3 — Bar chart has 2 series (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — Bar chart has {series_count} series, expected 2")
        else:
            print("FAIL: Component 3 — No bar chart found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Pie chart exists with correct title (0.20 pts)
    try:
        if len(pie_charts) >= 1:
            pc = pie_charts[0]
            title_text = get_chart_title_text(pc)
            if title_text and 'headcount' in title_text.lower():
                print(f"PASS: Component 4 — Pie chart with title '{title_text}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Pie chart title mismatch. Expected 'Headcount Distribution', found: '{title_text}'")
        else:
            print("FAIL: Component 4 — No pie chart found on Dashboard")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Pie chart has 1 data series (0.10 pts)
    try:
        if len(pie_charts) >= 1:
            pc = pie_charts[0]
            series_count = len(pc.series)
            if series_count == 1:
                print(f"PASS: Component 5 — Pie chart has 1 series (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — Pie chart has {series_count} series, expected 1")
        else:
            print("FAIL: Component 5 — No pie chart found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Line chart exists with correct title (0.20 pts)
    try:
        if len(line_charts) >= 1:
            lc = line_charts[0]
            title_text = get_chart_title_text(lc)
            if title_text and 'salary' in title_text.lower():
                print(f"PASS: Component 6 — Line chart with title '{title_text}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 6 — Line chart title mismatch. Expected 'Salary Distribution', found: '{title_text}'")
        else:
            print("FAIL: Component 6 — No line chart found on Dashboard")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Line chart has 1 data series (0.05 pts)
    try:
        if len(line_charts) >= 1:
            lc = line_charts[0]
            series_count = len(lc.series)
            if series_count == 1:
                print(f"PASS: Component 7 — Line chart has 1 series (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 7 — Line chart has {series_count} series, expected 1")
        else:
            print("FAIL: Component 7 — No line chart found")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

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
