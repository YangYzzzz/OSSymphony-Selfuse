"""
Reward Script: Create two charts from two financial tables in a spreadsheet
Task ID: osworld_calc_dual_chart_separate_tables_004
Domain: libreoffice_calc

Task: Create two charts from the two financial tables:
  - A bar chart for the operating expenses table, titled "Operating Expenses by Category"
  - A line chart for the revenue trend table, titled "Monthly Revenue Trend"
  Both charts must have descriptive titles.

Scoring Rubric:
  Component 1: A BarChart exists in the worksheet                          (0.30 pts)
  Component 2: The BarChart title is "Operating Expenses by Category"       (0.20 pts)
  Component 3: A LineChart exists in the worksheet                          (0.30 pts)
  Component 4: The LineChart title is "Monthly Revenue Trend"               (0.20 pts)
  Total: 1.0
"""

import os
import openpyxl
from openpyxl.chart import BarChart, LineChart

WORKDIR = '/home/user'
TASK_ID = 'osworld_calc_dual_chart_separate_tables_004'

BAR_CHART_TITLE = "Operating Expenses by Category"
LINE_CHART_TITLE = "Monthly Revenue Trend"


def extract_chart_title(chart):
    """Extract plain text title from an openpyxl chart object."""
    try:
        # Most common path for programmatically created charts
        return chart.title.tx.rich.p[0].r[0].t
    except Exception:
        pass
    try:
        # Fallback: title may be a plain string
        if isinstance(chart.title, str):
            return chart.title
    except Exception:
        pass
    return None


def verify_task(file_path):
    """
    Verify task completion: two charts exist with correct types and descriptive titles.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the active sheet (task uses a single sheet)
    # Collect all charts across all sheets
    all_charts = []
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        for chart in ws._charts:
            all_charts.append((sheet_name, chart))

    bar_charts = [(s, c) for s, c in all_charts if isinstance(c, BarChart)]
    line_charts = [(s, c) for s, c in all_charts if isinstance(c, LineChart)]

    # Component 1: A BarChart exists (0.30 points)
    # This should FAIL on initial_env (no charts) and PASS on golden_env
    try:
        if len(bar_charts) >= 1:
            print(f"PASS: Component 1 — BarChart found ({len(bar_charts)} bar chart(s)) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — No BarChart found (total charts: {len(all_charts)})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The BarChart title is "Operating Expenses by Category" (0.20 points)
    # This should FAIL on initial_env (no charts) and PASS on golden_env
    try:
        if len(bar_charts) >= 1:
            bar_title = extract_chart_title(bar_charts[0][1])
            if bar_title and bar_title.strip() == BAR_CHART_TITLE:
                print(f"PASS: Component 2 — BarChart title is '{BAR_CHART_TITLE}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — BarChart title expected '{BAR_CHART_TITLE}', found '{bar_title}'")
        else:
            print(f"FAIL: Component 2 — No BarChart to check title for")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: A LineChart exists (0.30 points)
    # This should FAIL on initial_env (no charts) and PASS on golden_env
    try:
        if len(line_charts) >= 1:
            print(f"PASS: Component 3 — LineChart found ({len(line_charts)} line chart(s)) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — No LineChart found (total charts: {len(all_charts)})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: The LineChart title is "Monthly Revenue Trend" (0.20 points)
    # This should FAIL on initial_env (no charts) and PASS on golden_env
    try:
        if len(line_charts) >= 1:
            line_title = extract_chart_title(line_charts[0][1])
            if line_title and line_title.strip() == LINE_CHART_TITLE:
                print(f"PASS: Component 4 — LineChart title is '{LINE_CHART_TITLE}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — LineChart title expected '{LINE_CHART_TITLE}', found '{line_title}'")
        else:
            print(f"FAIL: Component 4 — No LineChart to check title for")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path on the VM
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
