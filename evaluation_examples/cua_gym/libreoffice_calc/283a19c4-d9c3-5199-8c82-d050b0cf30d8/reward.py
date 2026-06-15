"""
Reward Script: Combination chart (Bar + Line) with secondary Y-axis
Task ID: calc_gg5_018
Domain: libreoffice_calc
Scoring:
  Component 1 (0.20): Chart exists on Output sheet
  Component 2 (0.30): Combination chart with Bar + Line sub-charts
  Component 3 (0.20): Correct data references (Bar=col B, Line=col C)
  Component 4 (0.20): Secondary Y-axis for Line series
  Component 5 (0.10): Legend present
"""

import os
import openpyxl
from openpyxl.chart import BarChart, LineChart

WORKDIR = '/home/user'
TASK_ID = 'calc_gg5_018'


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

    # Precondition: 'Output' sheet must exist
    if 'Output' not in wb.sheetnames:
        print("FAIL: 'Output' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Output']

    # Component 1: At least one chart exists on the Output sheet (0.20 points)
    try:
        chart_count = len(ws._charts)
        if chart_count >= 1:
            print(f"PASS: Component 1 — {chart_count} chart(s) found on Output sheet (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — No charts found on Output sheet")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if len(ws._charts) == 0:
        # No chart means nothing else to check
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    chart = ws._charts[0]

    # Component 2: Combination chart — must contain both a BarChart and a LineChart
    # sub-chart (via chart._charts overlay mechanism) (0.30 points)
    try:
        has_bar_sub = False
        has_line_sub = False
        sub_charts = getattr(chart, '_charts', [])

        for sub in sub_charts:
            if isinstance(sub, BarChart):
                has_bar_sub = True
            if isinstance(sub, LineChart):
                has_line_sub = True

        # Also check the main chart type itself if _charts is empty or has only one
        if isinstance(chart, BarChart):
            has_bar_sub = True
        if isinstance(chart, LineChart):
            has_line_sub = True

        if has_bar_sub and has_line_sub:
            print(f"PASS: Component 2 — Combination chart with Bar and Line sub-charts (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Expected Bar+Line combination. Bar={has_bar_sub}, Line={has_line_sub}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct data references (0.20 points)
    # Bar series should reference column B (Production Volume)
    # Line series should reference column C (Efficiency Rate)
    try:
        bar_refs_b = False
        line_refs_c = False
        sub_charts = getattr(chart, '_charts', [])

        for sub in sub_charts:
            for s in sub.series:
                val_ref = ''
                if hasattr(s, 'val') and s.val and s.val.numRef:
                    val_ref = s.val.numRef.f.upper()

                if isinstance(sub, BarChart) and ('$B$' in val_ref or '!B' in val_ref.replace('$', '')):
                    bar_refs_b = True
                if isinstance(sub, LineChart) and ('$C$' in val_ref or '!C' in val_ref.replace('$', '')):
                    line_refs_c = True

        # Also check main chart series if not covered by sub-charts
        if not bar_refs_b and isinstance(chart, BarChart):
            for s in chart.series:
                if hasattr(s, 'val') and s.val and s.val.numRef:
                    val_ref = s.val.numRef.f.upper()
                    if '$B$' in val_ref or '!B' in val_ref.replace('$', ''):
                        bar_refs_b = True

        if bar_refs_b and line_refs_c:
            print(f"PASS: Component 3 — Bar references col B, Line references col C (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Bar refs B={bar_refs_b}, Line refs C={line_refs_c}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Secondary Y-axis — Line sub-chart uses a different y_axis axId
    # than the Bar sub-chart (0.20 points)
    try:
        bar_y_ax_id = None
        line_y_ax_id = None
        sub_charts = getattr(chart, '_charts', [])

        for sub in sub_charts:
            if isinstance(sub, BarChart):
                bar_y_ax_id = sub.y_axis.axId
            if isinstance(sub, LineChart):
                line_y_ax_id = sub.y_axis.axId

        if bar_y_ax_id is not None and line_y_ax_id is not None and bar_y_ax_id != line_y_ax_id:
            print(f"PASS: Component 4 — Secondary Y-axis present (bar axId={bar_y_ax_id}, line axId={line_y_ax_id}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — No secondary axis. bar_y={bar_y_ax_id}, line_y={line_y_ax_id}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Legend is present (0.10 points)
    try:
        if chart.legend is not None:
            print(f"PASS: Component 5 — Legend is present (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — No legend found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point — test against the canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
