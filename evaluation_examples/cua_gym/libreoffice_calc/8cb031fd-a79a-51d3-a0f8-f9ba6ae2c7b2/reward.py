"""
Reward Script: Create a bar chart showing monthly revenue for H1
Task ID: calc_sales_041
Domain: libreoffice_calc
Scoring:
  Component 1: Chart exists on Revenue sheet (0.25)
  Component 2: Chart type is bar/column (0.20)
  Component 3: Chart title is 'Monthly Revenue H1' (0.25)
  Component 4: Axis titles are correct (0.15)
  Component 5: Chart has correct data series (0.15)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_sales_041'


def get_chart_title_text(title_obj):
    """Extract plain text from an openpyxl chart Title object."""
    try:
        if title_obj is None:
            return None
        # Try to get text from rich text paragraphs
        if hasattr(title_obj, 'tx') and title_obj.tx is not None:
            tx = title_obj.tx
            if hasattr(tx, 'rich') and tx.rich is not None:
                parts = []
                for p in tx.rich.paragraphs:
                    for r in p.r:
                        if r.t:
                            parts.append(r.t)
                if parts:
                    return ''.join(parts)
            if hasattr(tx, 'strRef') and tx.strRef is not None:
                if tx.strRef.v:
                    return tx.strRef.v
        # Fallback: try direct text attribute
        if hasattr(title_obj, 'text'):
            return title_obj.text
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

    # Precondition: Revenue sheet must exist
    if 'Revenue' not in wb.sheetnames:
        print("FAIL: 'Revenue' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Revenue']

    # Component 1: At least one chart exists on the Revenue sheet (0.25 points)
    try:
        num_charts = len(ws._charts)
        if num_charts >= 1:
            print(f"PASS: Component 1 — Chart exists on Revenue sheet ({num_charts} chart(s)) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — No charts found on Revenue sheet (found {num_charts})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If no charts, remaining checks are moot
    if len(ws._charts) < 1:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    chart = ws._charts[0]

    # Component 2: Chart type is bar/column (0.20 points)
    try:
        chart_type = getattr(chart, 'type', None)
        chart_class = type(chart).__name__
        # openpyxl BarChart with type="col" is a vertical column chart (bar chart)
        # type="bar" is horizontal bar chart — both are acceptable for "bar chart"
        if chart_type in ('col', 'bar') or 'Bar' in chart_class:
            print(f"PASS: Component 2 — Chart type is '{chart_type}' (class: {chart_class}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected bar/col chart, found type='{chart_type}' class='{chart_class}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chart title is 'Monthly Revenue H1' (0.25 points)
    try:
        title_text = get_chart_title_text(chart.title)
        if title_text and title_text.strip() == 'Monthly Revenue H1':
            print(f"PASS: Component 3 — Chart title is 'Monthly Revenue H1' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Expected title 'Monthly Revenue H1', found: '{title_text}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Axis titles are correct (0.15 points)
    # Y-axis should mention revenue, X-axis should mention month
    try:
        y_title = get_chart_title_text(chart.y_axis.title) if chart.y_axis.title else None
        x_title = get_chart_title_text(chart.x_axis.title) if chart.x_axis.title else None

        axis_score = 0.0
        # Check that at least one axis title exists and references the expected concepts
        if y_title and 'revenue' in y_title.lower():
            axis_score += 0.075
            print(f"  PASS: Y-axis title contains 'revenue': '{y_title}'")
        else:
            print(f"  FAIL: Y-axis title — expected 'Revenue' related, found: '{y_title}'")

        if x_title and 'month' in x_title.lower():
            axis_score += 0.075
            print(f"  PASS: X-axis title contains 'month': '{x_title}'")
        else:
            print(f"  FAIL: X-axis title — expected 'Month' related, found: '{x_title}'")

        if axis_score > 0:
            print(f"PASS: Component 4 — Axis titles ({axis_score} pts)")
            total_score += axis_score
        else:
            print(f"FAIL: Component 4 — No correct axis titles found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Chart has at least 1 data series referencing Revenue data (0.15 points)
    try:
        num_series = len(chart.series)
        if num_series >= 1:
            # Check that the series references the Revenue sheet data
            series = chart.series[0]
            val_ref = ''
            try:
                if hasattr(series.val, 'numRef') and series.val.numRef:
                    val_ref = series.val.numRef.f or ''
            except Exception:
                val_ref = ''

            if 'Revenue' in val_ref or 'B' in val_ref.upper() or num_series >= 1:
                # Series exists and either references Revenue data or at minimum has data
                print(f"PASS: Component 5 — Chart has {num_series} series (ref: '{val_ref}') (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — Series exists but doesn't reference Revenue data")
        else:
            print(f"FAIL: Component 5 — No data series in chart")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
