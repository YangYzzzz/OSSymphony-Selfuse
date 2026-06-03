"""
Reward Script: Create a column chart using only product names and 2024 sales data
Task ID: calc_chart_noncontiguous_range_034
Domain: libreoffice_calc
Scoring:
  Component 1: A column (bar) chart exists in sheet 'SalesHistory'  — 0.3 pts
  Component 2: Chart data series references 2024 Sales (D2:D6) only — 0.4 pts
  Component 3: Chart title is '2024 Product Sales'                  — 0.3 pts
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'   # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_noncontiguous_range_034'


def get_title_text(chart):
    """Extract chart title text from a chart object."""
    try:
        # Try rich text title
        title_text = chart.title.tx.rich.p[0].r[0].t
        return title_text
    except Exception:
        pass
    try:
        # Try strRef title
        return chart.title.tx.rich.p[0].r[0].t
    except Exception:
        pass
    try:
        return str(chart.title)
    except Exception:
        return None


def normalize_ref(ref):
    """Normalize a cell reference string for comparison: strip quotes, dollar signs, uppercase."""
    if ref is None:
        return None
    return ref.replace("'", "").replace("$", "").replace('"', "").upper()


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Create a column chart using only the product names (column A)
    and the 2024 sales (column D), skipping columns B and C.
    Chart title must be '2024 Product Sales'.
    """
    total_score = 0.0

    # Precondition gate: file must be loadable
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: sheet 'SalesHistory' must exist
    if 'SalesHistory' not in wb.sheetnames:
        print("FAIL: Sheet 'SalesHistory' not found in workbook")
        print(f"Score: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    ws = wb['SalesHistory']

    # Component 1: A column chart exists in sheet 'SalesHistory' (0.3 points)
    # This must FAIL on initial (0 charts) and PASS on golden (1 chart of type col)
    try:
        charts = ws._charts
        column_chart = None
        for c in charts:
            # BarChart with type='col' is a column (vertical) chart
            if type(c).__name__ == 'BarChart' and getattr(c, 'type', None) == 'col':
                column_chart = c
                break
        if column_chart is not None:
            print(f"PASS: Component 1 — Column chart found in 'SalesHistory' (0.3 pts)")
            total_score += 0.3
        else:
            found_any = len(charts) if charts else 0
            print(f"FAIL: Component 1 — No column chart found in 'SalesHistory'. Charts found: {found_any}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Chart data series references 2024 Sales (D2:D6) only, NOT B or C columns (0.4 points)
    # Checks that:
    #   - exactly 1 data series is in the chart
    #   - the series val reference covers column D rows 2-6 (SalesHistory!$D$2:$D$6)
    #   - column B and C are NOT referenced (no 2022/2023 data)
    try:
        if column_chart is None:
            print("FAIL: Component 2 — No column chart to check series for")
        else:
            series = column_chart.series
            num_series = len(series)
            if num_series != 1:
                print(f"FAIL: Component 2 — Expected 1 data series, found {num_series}")
            else:
                s = series[0]
                val_ref = normalize_ref(s.val.numRef.f) if (s.val and s.val.numRef) else None
                # Expected normalized: SALESHISTORY!D2:D6
                expected_val_ref = "SALESHISTORY!D2:D6"
                # Also check categories reference A2:A6
                cat_ref = None
                if s.cat:
                    if s.cat.numRef:
                        cat_ref = normalize_ref(s.cat.numRef.f)
                    elif s.cat.strRef:
                        cat_ref = normalize_ref(s.cat.strRef.f)
                expected_cat_ref = "SALESHISTORY!A2:A6"

                val_ok = (val_ref == expected_val_ref)
                # Check B and C columns are NOT referenced (no 2022/2023 data)
                old_data_referenced = bool(val_ref and ('!B' in val_ref or '!C' in val_ref))

                if val_ok and not old_data_referenced:
                    print(f"PASS: Component 2 — Data series correctly references 2024 Sales D2:D6 (0.4 pts). Cat ref: {cat_ref}")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 2 — Data series val ref: '{val_ref}', expected '{expected_val_ref}'. old_data_referenced={old_data_referenced}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chart title is '2024 Product Sales' (0.3 points)
    try:
        if column_chart is None:
            print("FAIL: Component 3 — No column chart to check title for")
        else:
            title_text = get_title_text(column_chart)
            expected_title = "2024 Product Sales"
            if title_text is not None and title_text.strip() == expected_title:
                print(f"PASS: Component 3 — Chart title is '{title_text}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Expected title '{expected_title}', found: '{title_text}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
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
