"""
Reward Script: Correlation Matrix Visualization Chart
Task ID: calc_gcp_071
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): Chart exists on the Correlations sheet
  Component 2 (0.15): Chart is a bar/column type (clustered)
  Component 3 (0.15): Chart has a meaningful title referencing correlation
  Component 4 (0.20): Chart has multiple series referencing the correlation data
  Component 5 (0.15): Data labels are enabled (values shown on chart)
  Component 6 (0.10): Axis titles are present
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcp_071'


def persist_app_state(domain: str):
    """Attempt to save any unsaved state in LibreOffice."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def get_title_text(title_obj):
    """Extract plain text from an openpyxl chart title object."""
    if title_obj is None:
        return None
    try:
        if title_obj.tx and title_obj.tx.rich:
            texts = []
            for p in title_obj.tx.rich.p:
                for r in p.r:
                    if r.t:
                        texts.append(r.t)
            return ' '.join(texts)
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

    # Verify precondition: Correlations sheet exists
    if 'Correlations' not in wb.sheetnames:
        print("FAIL: 'Correlations' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Correlations']

    # Component 1: Chart exists on the Correlations sheet (0.25 points)
    # This is the primary task-introduced change: initial has 0 charts, golden has >= 1
    try:
        charts = ws._charts
        if len(charts) >= 1:
            print(f"PASS: Component 1 — Chart exists on Correlations sheet ({len(charts)} chart(s)) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — No charts found on Correlations sheet")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If no chart at all, remaining components are moot
    if total_score == 0.0:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    chart = ws._charts[0]

    # Component 2: Chart is a bar/column type (0.15 points)
    # Task asks for a bar chart showing correlation coefficients
    try:
        chart_type = chart.type  # 'col' for column, 'bar' for horizontal bar
        if chart_type in ('col', 'bar'):
            print(f"PASS: Component 2 — Chart type is '{chart_type}' (bar/column) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected bar/col chart type, found: {chart_type}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chart has a meaningful title referencing correlation (0.15 points)
    # Task says to create a chart showing "correlation matrix visually"
    try:
        title_text = get_title_text(chart.title)
        if title_text and 'correlat' in title_text.lower():
            print(f"PASS: Component 3 — Chart title contains 'correlation': '{title_text}' (0.15 pts)")
            total_score += 0.15
        elif title_text:
            # Partial: has a title but doesn't mention correlation
            print(f"PARTIAL: Component 3 — Chart has title '{title_text}' but no 'correlation' keyword (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 3 — No chart title found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Chart has multiple series referencing correlation data (0.20 points)
    # The correlation matrix has 6 variables, so we expect multiple series
    try:
        series_count = len(chart.series)
        if series_count >= 4:
            # Good coverage of the correlation matrix
            print(f"PASS: Component 4 — Chart has {series_count} series (>= 4, good coverage) (0.20 pts)")
            total_score += 0.20
        elif series_count >= 2:
            # Some coverage
            print(f"PARTIAL: Component 4 — Chart has {series_count} series (>= 2 but < 4) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — Chart has only {series_count} series, expected multiple")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Data labels are enabled (values shown on chart) (0.15 points)
    # Task says "Values are labeled on the chart"
    try:
        labels_found = False
        # Check series-level data labels
        for i, s in enumerate(chart.series):
            if hasattr(s, 'dLbls') and s.dLbls is not None:
                if s.dLbls.showVal:
                    labels_found = True
                    break
        # Check chart-level data labels
        if not labels_found and hasattr(chart, 'dataLabels') and chart.dataLabels is not None:
            if chart.dataLabels.showVal:
                labels_found = True

        if labels_found:
            print(f"PASS: Component 5 — Data labels (showVal) are enabled (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — No data labels with showVal found on chart")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Axis titles are present (0.10 points)
    # A well-labeled chart should have at least one axis title
    try:
        y_title = get_title_text(chart.y_axis.title) if chart.y_axis and chart.y_axis.title else None
        x_title = get_title_text(chart.x_axis.title) if chart.x_axis and chart.x_axis.title else None

        axis_count = 0
        if y_title:
            axis_count += 1
        if x_title:
            axis_count += 1

        if axis_count == 2:
            print(f"PASS: Component 6 — Both axis titles present (x='{x_title}', y='{y_title}') (0.10 pts)")
            total_score += 0.10
        elif axis_count == 1:
            title_found = y_title or x_title
            print(f"PARTIAL: Component 6 — One axis title present: '{title_found}' (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 6 — No axis titles found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_calc")

file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
