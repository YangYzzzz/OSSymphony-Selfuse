"""
Reward Script: Create a column chart arranged as a histogram showing distribution of student exam scores
Task ID: calc_chart_histogram_072
Domain: libreoffice_calc
Scoring:
  - Component 1: A BarChart (column type) exists in the ScoreDistribution sheet (0.4 pts)
  - Component 2: Chart title is 'Exam Score Distribution' (0.2 pts)
  - Component 3: Chart data range covers B2:B11 (counts) with categories A2:A11 (score ranges) (0.2 pts)
  - Component 4: Gap width is 0 (histogram appearance - no gaps between bars) (0.2 pts)
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_histogram_072'
SHEET_NAME = 'ScoreDistribution'


def extract_title_text(title_obj):
    """
    Extract text string from an openpyxl chart Title object.
    Traverses the rich text structure to find the text run.
    Returns the text string or None if not found.
    """
    try:
        if title_obj is None:
            return None
        for p in title_obj.tx.rich.p:
            for r in p.r:
                if r.t:
                    return r.t
    except Exception:
        pass
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The initial file has 0 charts in the ScoreDistribution sheet.
    The golden file has 1 BarChart (col type) with:
      - Title: 'Exam Score Distribution'
      - Y-axis: shows count of students (Number of Students)
      - X-axis: shows score ranges
      - Data range: B2:B11 (values), A2:A11 (categories)
      - gapWidth: 0 (no gaps between bars, histogram appearance)
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: sheet must exist
    if SHEET_NAME not in wb.sheetnames:
        print(f"CRITICAL: Sheet '{SHEET_NAME}' not found in workbook.")
        print("REWARD: 0.0")
        return 0.0

    ws = wb[SHEET_NAME]
    charts = ws._charts

    # Component 1: A column chart (BarChart with type='col') exists (0.4 pts)
    # Fails on initial (0 charts) — passes on golden (1 BarChart col)
    try:
        col_charts = [c for c in charts if type(c).__name__ == 'BarChart' and getattr(c, 'type', None) == 'col']
        if len(col_charts) >= 1:
            print(f"PASS: Component 1 — Column chart (BarChart col type) exists ({len(col_charts)} found) (0.4 pts)")
            total_score += 0.4
        else:
            all_chart_types = [f"{type(c).__name__}({getattr(c,'type','?')})" for c in charts]
            print(f"FAIL: Component 1 — Expected a BarChart with type='col', found: {all_chart_types if all_chart_types else 'no charts'}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # For remaining components, we need at least one column chart
    chart = None
    try:
        col_charts = [c for c in charts if type(c).__name__ == 'BarChart' and getattr(c, 'type', None) == 'col']
        if col_charts:
            chart = col_charts[0]
    except Exception:
        pass

    # Component 2: Chart title is 'Exam Score Distribution' (0.2 pts)
    # Fails on initial (no chart) — passes on golden (chart with correct title)
    try:
        if chart is not None:
            title_text = extract_title_text(chart.title)
            if title_text and title_text.strip() == 'Exam Score Distribution':
                print(f"PASS: Component 2 — Chart title is 'Exam Score Distribution' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — Expected chart title 'Exam Score Distribution', found: {repr(title_text)}")
        else:
            print(f"FAIL: Component 2 — No column chart found to check title")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chart data range covers B2:B11 (count values) with categories A2:A11 (0.2 pts)
    # The task requires data range A1:B11. The actual golden uses B2:B11 for values and A2:A11 for categories.
    # Fails on initial (no chart) — passes on golden (chart with correct data ranges)
    try:
        if chart is not None and len(chart.series) >= 1:
            series = chart.series[0]
            val_ref = None
            cat_ref = None
            try:
                val_ref = series.val.numRef.f if series.val and series.val.numRef else None
            except Exception:
                pass
            try:
                cat_ref = series.cat.numRef.f if series.cat and series.cat.numRef else None
            except Exception:
                pass

            # Check that values reference column B rows 2-11 (the Count column)
            # and categories reference column A rows 2-11 (Score Range column)
            val_ok = val_ref is not None and '$B$2:$B$11' in val_ref
            cat_ok = cat_ref is not None and '$A$2:$A$11' in cat_ref

            if val_ok and cat_ok:
                print(f"PASS: Component 3 — Data range correct: values={val_ref}, categories={cat_ref} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Data range incorrect. Values={repr(val_ref)} (need '$B$2:$B$11'), Categories={repr(cat_ref)} (need '$A$2:$A$11')")
        else:
            print(f"FAIL: Component 3 — No column chart with series found to check data range")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Gap width is 0 (histogram appearance — no gaps between bars) (0.2 pts)
    # Fails on initial (no chart) — passes on golden (gapWidth=0.0)
    try:
        if chart is not None:
            gap_width = getattr(chart, 'gapWidth', None)
            # gapWidth == 0 or 0.0 means no gap between bars (histogram style)
            if gap_width is not None and float(gap_width) == 0.0:
                print(f"PASS: Component 4 — Gap width is 0 (histogram appearance: no gaps between bars) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — Expected gapWidth=0 for histogram appearance, found: {repr(gap_width)}")
        else:
            print(f"FAIL: Component 4 — No column chart found to check gap width")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
