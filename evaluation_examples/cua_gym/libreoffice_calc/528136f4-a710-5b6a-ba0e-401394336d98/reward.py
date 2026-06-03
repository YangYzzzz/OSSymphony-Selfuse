"""
Reward Script: Configure a 100% stacked bar chart with percentage data labels and updated title
Task ID: calc_gg2_033
Domain: libreoffice_calc
Scoring:
  Component 1: Chart type changed to 'bar' (0.25 pts)
  Component 2: Chart grouping changed to 'percentStacked' (0.25 pts)
  Component 3: Chart title updated to 'Budget Allocation by Department (% of Total)' (0.25 pts)
  Component 4: Data labels showing percentages on all 3 series (0.25 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'calc_gg2_033'


def get_chart_title_text(chart):
    """Extract the plain text from a chart title object."""
    try:
        if chart.title and chart.title.tx and chart.title.tx.rich:
            texts = []
            for p in chart.title.tx.rich.p:
                for r in p.r:
                    texts.append(r.t)
            return ''.join(texts)
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
        import openpyxl
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Budget Overview' sheet must exist
    if 'Budget Overview' not in wb.sheetnames:
        print("FAIL: 'Budget Overview' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Budget Overview']

    # Precondition: at least one chart must exist
    if len(ws._charts) == 0:
        print("FAIL: No charts found on 'Budget Overview' sheet")
        print("REWARD: 0.0")
        return 0.0

    chart = ws._charts[0]

    # Component 1: Chart type is 'bar' (horizontal bars for 100% stacked bar) (0.25 pts)
    # Initial state: type='col' (clustered column). Golden: type='bar'.
    try:
        chart_type = chart.type
        if chart_type == 'bar':
            print(f"PASS: Component 1 — Chart type is 'bar' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected chart type 'bar', found '{chart_type}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Chart grouping is 'percentStacked' (0.25 pts)
    # Initial state: grouping='clustered'. Golden: grouping='percentStacked'.
    try:
        grouping = chart.grouping
        if grouping == 'percentStacked':
            print(f"PASS: Component 2 — Chart grouping is 'percentStacked' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected grouping 'percentStacked', found '{grouping}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chart title is 'Budget Allocation by Department (% of Total)' (0.25 pts)
    # Initial state: title='Budget Allocation by Department'. Golden has the updated title.
    try:
        title_text = get_chart_title_text(chart)
        expected_title = 'Budget Allocation by Department (% of Total)'
        if title_text and title_text.strip() == expected_title:
            print(f"PASS: Component 3 — Chart title matches expected (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Expected title '{expected_title}', found '{title_text}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Data labels showing percentages on all series (0.25 pts)
    # Initial state: no data labels (dLbls=None). Golden: all 3 series have showPercent=True.
    try:
        series_count = len(chart.series)
        if series_count == 0:
            print("FAIL: Component 4 — No series found in chart")
        else:
            series_with_pct_labels = 0
            for i, s in enumerate(chart.series):
                if s.dLbls is not None and s.dLbls.showPercent is True:
                    series_with_pct_labels += 1
                else:
                    show_pct = s.dLbls.showPercent if s.dLbls else None
                    print(f"  Series {i}: dLbls showPercent = {show_pct}")

            if series_with_pct_labels == series_count:
                print(f"PASS: Component 4 — All {series_count} series have percentage data labels (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — {series_with_pct_labels}/{series_count} series have percentage labels")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
