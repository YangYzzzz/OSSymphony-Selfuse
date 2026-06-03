"""
Reward Script: Create two charts from patient data
Task ID: osworld_calc_dual_chart_separate_tables_008
Domain: libreoffice_calc
Scoring:
  - Component 1: Two charts exist on the 'Patient Data' sheet (0.3 pts)
  - Component 2: A BarChart with title 'Treatment Count by Ward' exists (0.35 pts)
  - Component 3: A LineChart with title 'Weekly Patient Admissions' exists (0.35 pts)
"""

import os
import openpyxl
from openpyxl.chart import BarChart, LineChart

WORKDIR = '/home/user'
TASK_ID = 'osworld_calc_dual_chart_separate_tables_008'


def get_chart_title(chart):
    """Extract the title string from a chart's Title object, handling nested structure."""
    try:
        # The title is stored as a nested RichText object
        # Access path: chart.title.tx.rich.p[0].r[0].t
        title_obj = chart.title
        if title_obj is None:
            return None
        tx = title_obj.tx
        if tx is None:
            return None
        # Try rich text path
        if tx.rich is not None:
            for para in tx.rich.p:
                for run in para.r:
                    if run.t:
                        return run.t
        # Try strRef path
        if tx.strRef is not None and tx.strRef.v is not None:
            return tx.strRef.v
        return None
    except Exception as e:
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load workbook — gate: if file missing or corrupt, return 0.0
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gate: the 'Patient Data' sheet must exist
    if 'Patient Data' not in wb.sheetnames:
        print("CRITICAL: Sheet 'Patient Data' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Patient Data']
    charts = ws._charts

    # Component 1: Two charts exist on the sheet (0.3 points)
    # Initial env has 0 charts; golden env has 2 charts.
    try:
        if len(charts) >= 2:
            print(f"PASS: Component 1 — 2 charts found on 'Patient Data' sheet (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected at least 2 charts, found {len(charts)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: A BarChart (column chart) exists with title containing "Treatment Count by Ward" (0.35 points)
    # The bar chart should source from the ward summary table (Table 1, rows 2-8).
    try:
        matching_bar_charts = [
            chart for chart in charts
            if isinstance(chart, BarChart) and get_chart_title(chart) is not None
            and "Treatment Count by Ward" in get_chart_title(chart)
        ]
        if len(matching_bar_charts) >= 1:
            found_title = get_chart_title(matching_bar_charts[0])
            print(f"PASS: Component 2 — BarChart with title '{found_title}' found (0.35 pts)")
            total_score += 0.35
        else:
            # Report what was found to aid debugging
            found_info = [f"{type(c).__name__}:'{get_chart_title(c)}'" for c in charts]
            print(f"FAIL: Component 2 — No BarChart with title 'Treatment Count by Ward' found. Found: {found_info}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: A LineChart exists with title containing "Weekly Patient Admissions" (0.35 points)
    # The line chart should source from the weekly admissions table (Table 2, rows 11-24).
    try:
        matching_line_charts = [
            chart for chart in charts
            if isinstance(chart, LineChart) and get_chart_title(chart) is not None
            and "Weekly Patient Admissions" in get_chart_title(chart)
        ]
        if len(matching_line_charts) >= 1:
            found_title = get_chart_title(matching_line_charts[0])
            print(f"PASS: Component 3 — LineChart with title '{found_title}' found (0.35 pts)")
            total_score += 0.35
        else:
            found_info = [f"{type(c).__name__}:'{get_chart_title(c)}'" for c in charts]
            print(f"FAIL: Component 3 — No LineChart with title 'Weekly Patient Admissions' found. Found: {found_info}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path on the VM
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
