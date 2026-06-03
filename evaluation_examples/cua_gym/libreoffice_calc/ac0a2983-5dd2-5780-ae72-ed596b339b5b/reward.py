"""
Reward Script: Create a scatter (XY) chart to visualize the relationship between
               advertising spend and sales revenue.
Task ID: calc_chart_scatter_012
Domain: libreoffice_calc
Scoring:
  Component 1: Scatter chart exists on 'AdSpend' sheet        (0.40 pts)
  Component 2: Chart title is 'Advertising Spend vs Sales Revenue' (0.20 pts)
  Component 3: X-axis and Y-axis labels are correct           (0.20 pts)
  Component 4: Chart data range covers A2:A9 (x) and B2:B9 (y) (0.20 pts)
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_scatter_012'


def get_title_text(title_obj):
    """Extract plain text from an openpyxl chart title object."""
    try:
        if title_obj is None:
            return None
        text_obj = title_obj.tx
        if text_obj and text_obj.rich:
            paragraphs = text_obj.rich.p
            texts = []
            for p in paragraphs:
                for r in (p.r or []):
                    texts.append(r.t)
            return ' '.join(texts).strip()
    except Exception:
        pass
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must be loadable
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: 'AdSpend' sheet must exist
    if 'AdSpend' not in wb.sheetnames:
        print("CRITICAL: Sheet 'AdSpend' not found. Cannot verify chart.")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['AdSpend']

    # Component 1: A ScatterChart exists on the 'AdSpend' sheet (0.40 pts)
    # The initial file has 0 charts; the golden file has 1 ScatterChart.
    # This component FAILS on initial and PASSES on golden.
    scatter_chart = None
    try:
        charts = ws._charts
        scatter_charts = [c for c in charts if type(c).__name__ == 'ScatterChart']
        if scatter_charts:
            scatter_chart = scatter_charts[0]
            print(f"PASS: Component 1 — ScatterChart exists on 'AdSpend' sheet "
                  f"({len(scatter_charts)} scatter chart(s) found) (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 — No ScatterChart found on 'AdSpend' sheet "
                  f"(total charts: {len(charts)})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Chart title is 'Advertising Spend vs Sales Revenue' (0.20 pts)
    # Only verifiable if Component 1 passed.
    if scatter_chart is not None:
        try:
            title_text = get_title_text(scatter_chart.title)
            expected_title = 'Advertising Spend vs Sales Revenue'
            if title_text == expected_title:
                print(f"PASS: Component 2 — Chart title is '{title_text}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — Expected chart title '{expected_title}', "
                      f"found '{title_text}'")
        except Exception as e:
            print(f"ERROR: Component 2 — {e}")
    else:
        print("SKIP: Component 2 — No scatter chart to inspect for title")

    # Component 3: X-axis labeled 'Ad Spend ($000)' AND Y-axis labeled 'Sales Revenue ($000)' (0.20 pts)
    # Both axis labels must be correct to earn this component's points.
    if scatter_chart is not None:
        try:
            x_axis_text = get_title_text(scatter_chart.x_axis.title)
            y_axis_text = get_title_text(scatter_chart.y_axis.title)
            expected_x = 'Ad Spend ($000)'
            expected_y = 'Sales Revenue ($000)'
            if x_axis_text == expected_x and y_axis_text == expected_y:
                print(f"PASS: Component 3 — X-axis='{x_axis_text}', "
                      f"Y-axis='{y_axis_text}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — "
                      f"X-axis expected '{expected_x}', found '{x_axis_text}'; "
                      f"Y-axis expected '{expected_y}', found '{y_axis_text}'")
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")
    else:
        print("SKIP: Component 3 — No scatter chart to inspect for axis labels")

    # Component 4: Chart data range covers A2:A9 (x-values) and B2:B9 (y-values) (0.20 pts)
    # This verifies the chart references the correct data range A1:B9 (header in row 1,
    # data rows 2-9 → x: A2:A9, y: B2:B9).
    if scatter_chart is not None:
        try:
            series = scatter_chart.series
            if series:
                s = series[0]
                x_ref = None
                y_ref = None
                if hasattr(s, 'xVal') and s.xVal and hasattr(s.xVal, 'numRef') and s.xVal.numRef:
                    x_ref = s.xVal.numRef.f
                if hasattr(s, 'yVal') and s.yVal and hasattr(s.yVal, 'numRef') and s.yVal.numRef:
                    y_ref = s.yVal.numRef.f

                # Normalize reference: strip quotes, sheet name, dollar signs for comparison
                def normalize_ref(ref):
                    if ref is None:
                        return None
                    # Remove sheet name prefix like 'AdSpend'! or AdSpend!
                    import re
                    ref = re.sub(r"^'?[^'!]+'?!", '', ref)
                    # Remove dollar signs
                    ref = ref.replace('$', '')
                    return ref.upper()

                x_norm = normalize_ref(x_ref)
                y_norm = normalize_ref(y_ref)

                expected_x_range = 'A2:A9'
                expected_y_range = 'B2:B9'

                if x_norm == expected_x_range and y_norm == expected_y_range:
                    print(f"PASS: Component 4 — Data range correct: "
                          f"x={x_ref}, y={y_ref} (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 4 — Data range mismatch: "
                          f"x_norm='{x_norm}' (expected '{expected_x_range}'), "
                          f"y_norm='{y_norm}' (expected '{expected_y_range}')")
            else:
                print("FAIL: Component 4 — Scatter chart has no series data")
        except Exception as e:
            print(f"ERROR: Component 4 — {e}")
    else:
        print("SKIP: Component 4 — No scatter chart to inspect for data range")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
