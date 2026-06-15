"""
Reward Script: Update chart data range to include July (row 8)
Task ID: calc_chart_data_range_change_031
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): Chart Y-value data range updated from B2:B7 to B2:B8
  Component 2 (0.3): Chart X-category range updated from A2:A7 to A2:A8
  Component 3 (0.2): Chart type (LineChart) and title remain unchanged
Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_data_range_change_031'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Update the line chart to include data from row 8 (July).
    Initial state: chart data range covers rows 2-7 (January through June).
    Golden state:  chart data range covers rows 2-8 (January through July).
    """
    total_score = 0.0

    # Load the workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: sheet 'Monthly' must exist
    try:
        if 'Monthly' not in wb.sheetnames:
            print("FAIL: Sheet 'Monthly' not found")
            print("REWARD: 0.0")
            return 0.0
        ws = wb['Monthly']
    except Exception as e:
        print(f"CRITICAL: Cannot access sheet 'Monthly': {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: at least one chart must exist
    try:
        charts = ws._charts
        if not charts:
            print("FAIL: No charts found on sheet 'Monthly'")
            print("REWARD: 0.0")
            return 0.0
        chart = charts[0]
    except Exception as e:
        print(f"CRITICAL: Cannot access charts: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Y-value data range extended to include July (B2:B8) (0.5 points)
    # Initial: 'Monthly'!$B$2:$B$7 → Golden: 'Monthly'!$B$2:$B$8
    # This fails on initial (still B$7) and passes on golden (B$8)
    try:
        if chart.series and len(chart.series) > 0:
            ser = chart.series[0]
            y_ref = None
            if hasattr(ser, 'val') and ser.val is not None and ser.val.numRef:
                y_ref = ser.val.numRef.ref
            if y_ref is not None:
                # Normalize: strip quotes, uppercase for comparison
                y_ref_normalized = y_ref.upper().replace("'MONTHLY'!", "").replace(" ", "")
                # Accept both absolute and relative forms: $B$2:$B$8 or B2:B8
                expected_variations = ["$B$2:$B$8", "B2:B8"]
                y_extended = any(v in y_ref_normalized for v in expected_variations)
                if y_extended:
                    print(f"PASS: Component 1 — Y-value data range updated to include row 8: {y_ref} (0.5 pts)")
                    total_score += 0.5
                else:
                    print(f"FAIL: Component 1 — Y-value range not extended to row 8. Found: {y_ref}")
            else:
                print("FAIL: Component 1 — Could not read Y-value reference from chart series")
        else:
            print("FAIL: Component 1 — No series found in chart")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: X-category range extended to include July (A2:A8) (0.3 points)
    # Initial: 'Monthly'!$A$2:$A$7 → Golden: 'Monthly'!$A$2:$A$8
    # This fails on initial (still A$7) and passes on golden (A$8)
    try:
        if chart.series and len(chart.series) > 0:
            ser = chart.series[0]
            cat_ref = None
            if hasattr(ser, 'cat') and ser.cat is not None:
                if hasattr(ser.cat, 'numRef') and ser.cat.numRef:
                    cat_ref = ser.cat.numRef.ref
                elif hasattr(ser.cat, 'strRef') and ser.cat.strRef:
                    cat_ref = ser.cat.strRef.ref
            if cat_ref is not None:
                cat_ref_normalized = cat_ref.upper().replace("'MONTHLY'!", "").replace(" ", "")
                expected_variations = ["$A$2:$A$8", "A2:A8"]
                cat_extended = any(v in cat_ref_normalized for v in expected_variations)
                if cat_extended:
                    print(f"PASS: Component 2 — X-category range updated to include row 8: {cat_ref} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — X-category range not extended to row 8. Found: {cat_ref}")
            else:
                print("FAIL: Component 2 — Could not read X-category reference from chart series")
        else:
            print("FAIL: Component 2 — No series found in chart")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chart type is still LineChart and title still 'Monthly Revenue' (0.2 points)
    # Both initial and golden have LineChart + 'Monthly Revenue' title
    # We use this as a compound check: the chart data was EXTENDED (from comp 1/2) AND chart type/title preserved
    # Only award if at least one of components 1/2 passed (otherwise this doesn't indicate task completion)
    try:
        chart_type_ok = isinstance(chart, openpyxl.chart.LineChart)

        # Check title text by extracting all run text and searching for expected title
        try:
            title_runs = []
            if chart.title and chart.title.tx and chart.title.tx.rich:
                for para in chart.title.tx.rich.p:
                    for run in para.r:
                        title_runs.append(run.t)
            chart_title_ok = any('Monthly Revenue' in t for t in title_runs)
        except Exception:
            chart_title_ok = False

        # This component only contributes if the data range was actually extended (otherwise we're scoring pre-existing state)
        data_range_was_extended = total_score > 0.0

        if chart_type_ok and chart_title_ok and data_range_was_extended:
            print(f"PASS: Component 3 — Chart type (LineChart) and title ('Monthly Revenue') preserved after update (0.2 pts)")
            total_score += 0.2
        elif not data_range_was_extended:
            print("FAIL: Component 3 — Skipped (data range not extended, so chart preservation is not meaningful)")
        elif not chart_type_ok:
            print(f"FAIL: Component 3 — Chart type is not LineChart: {type(chart).__name__}")
        else:
            print(f"FAIL: Component 3 — Chart title 'Monthly Revenue' not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
