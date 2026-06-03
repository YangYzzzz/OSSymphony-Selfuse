"""
Reward Script: Create a bar chart showing grade distribution for a class of students.
Task ID: calc_gpm_004
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): Chart exists and is a column chart
  Component 2 (0.25): Chart title is 'Class Grade Distribution - Math 101'
  Component 3 (0.20): Data labels are shown (showVal=True)
  Component 4 (0.15): Legend is removed (None)
  Component 5 (0.15): 5 data points with distinct colors assigned
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gpm_004'


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

    # Precondition: 'Distribution' sheet must exist
    if 'Distribution' not in wb.sheetnames:
        print("FAIL: 'Distribution' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Distribution']

    # Component 1: A column chart exists on the sheet (0.25 points)
    try:
        charts = ws._charts
        if len(charts) >= 1:
            chart = charts[0]
            # Check it is a column chart (type == 'col')
            chart_type = getattr(chart, 'type', None)
            if chart_type == 'col':
                print(f"PASS: Component 1 — Column chart exists (type={chart_type}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — Chart exists but type is '{chart_type}', expected 'col'")
        else:
            print(f"FAIL: Component 1 — No charts found on 'Distribution' sheet (count={len(charts)})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Chart title is 'Class Grade Distribution - Math 101' (0.25 points)
    try:
        charts = ws._charts
        if len(charts) >= 1:
            chart = charts[0]
            title_text = None
            if chart.title and hasattr(chart.title, 'tx') and chart.title.tx:
                tx = chart.title.tx
                if hasattr(tx, 'rich') and tx.rich:
                    # Extract text from rich text paragraphs
                    parts = []
                    for p in tx.rich.p:
                        for r in p.r:
                            if r.t:
                                parts.append(r.t)
                    title_text = ''.join(parts)
                elif hasattr(tx, 'strRef') and tx.strRef:
                    title_text = str(tx.strRef)

            expected_title = 'Class Grade Distribution - Math 101'
            if title_text and title_text.strip() == expected_title:
                print(f"PASS: Component 2 — Chart title matches: '{title_text}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — Expected title '{expected_title}', found '{title_text}'")
        else:
            print("FAIL: Component 2 — No charts found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Data labels showing count values (showVal=True) (0.20 points)
    try:
        charts = ws._charts
        if len(charts) >= 1:
            chart = charts[0]
            # Check series-level data labels first, then chart-level
            series_has_labels = (
                len(chart.series) > 0
                and hasattr(chart.series[0], 'dLbls')
                and chart.series[0].dLbls
                and chart.series[0].dLbls.showVal
            )
            chart_has_labels = (
                hasattr(chart, 'dLbls')
                and chart.dLbls
                and chart.dLbls.showVal
            )
            if series_has_labels or chart_has_labels:
                print(f"PASS: Component 3 — Data labels showVal enabled (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — Data labels showVal is not True")
        else:
            print("FAIL: Component 3 — No charts found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Legend is removed (0.15 points)
    try:
        charts = ws._charts
        if len(charts) >= 1:
            chart = charts[0]
            if chart.legend is None:
                print(f"PASS: Component 4 — Legend is removed (None) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Legend is present, expected None")
        else:
            print("FAIL: Component 4 — No charts found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: 5 data points with distinct fill colors (0.15 points)
    try:
        charts = ws._charts
        if len(charts) >= 1:
            chart = charts[0]
            if len(chart.series) > 0:
                s = chart.series[0]
                dp_list = s.data_points
                colored_points = 0
                colors_seen = set()
                for dp in dp_list:
                    gp = dp.graphicalProperties
                    if gp and gp.solidFill:
                        color = getattr(gp.solidFill, 'srgbClr', None)
                        if color:
                            colored_points += 1
                            colors_seen.add(str(color))

                if colored_points >= 5 and len(colors_seen) >= 5:
                    print(f"PASS: Component 5 — {colored_points} data points with {len(colors_seen)} distinct colors (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 5 — Found {colored_points} colored points, {len(colors_seen)} distinct colors (need 5 each)")
            else:
                print("FAIL: Component 5 — No series in chart")
        else:
            print("FAIL: Component 5 — No charts found")
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
