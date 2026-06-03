"""
Reward Script: Create a multi-series line chart showing mutual fund performance
Task ID: calc_chart_line_multiple_series_054
Domain: libreoffice_calc
Scoring:
  - Component 1: LineChart exists on FundPerformance sheet (0.3 pts)
  - Component 2: Chart has 4 series with correct data ranges (B-E, rows 2-9) (0.3 pts)
  - Component 3: Chart title is 'Mutual Fund Performance (Index = 100)' (0.2 pts)
  - Component 4: Y-axis minimum is set to 90 (0.2 pts)
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_line_multiple_series_054'


def extract_chart_title(chart):
    """
    Extract text from openpyxl chart title object.
    Returns the title string, or None if not found.
    """
    try:
        if chart.title is None:
            return None
        title_str = str(chart.title)
        # Extract text content from the repr string using regex
        matches = re.findall(r"t='([^']*)'", title_str)
        if matches:
            return matches[0]
        return None
    except Exception:
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Create a multi-series line chart showing the performance of 4 mutual funds
    over 8 quarters on the 'FundPerformance' sheet.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the workbook — gate check
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Verify the FundPerformance sheet exists
    if 'FundPerformance' not in wb.sheetnames:
        print("CRITICAL: 'FundPerformance' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['FundPerformance']

    # Component 1: A LineChart exists on the FundPerformance sheet (0.3 points)
    # This FAILS on initial (no charts) → PASSES on golden (has 1 LineChart)
    try:
        charts = ws._charts
        line_chart = None
        for c in charts:
            if type(c).__name__ == 'LineChart':
                line_chart = c
                break

        if line_chart is not None:
            print(f"PASS: Component 1 — LineChart found on FundPerformance sheet (0.3 pts)")
            total_score += 0.3
        else:
            chart_types = [type(c).__name__ for c in charts]
            print(f"FAIL: Component 1 — No LineChart found. Charts present: {chart_types}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        line_chart = None

    # If no line chart exists, Components 2-4 cannot pass
    if line_chart is None:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Chart has exactly 4 series with correct data ranges (0.3 points)
    # Each series should reference columns B, C, D, E from rows 2-9 of FundPerformance
    # This FAILS on initial (no chart) → PASSES on golden (4 series with correct ranges)
    try:
        series = line_chart.series
        num_series = len(series)

        if num_series == 4:
            # Verify all four data series reference the correct column ranges
            expected_val_ranges = [
                "'FundPerformance'!$B$2:$B$9",
                "'FundPerformance'!$C$2:$C$9",
                "'FundPerformance'!$D$2:$D$9",
                "'FundPerformance'!$E$2:$E$9",
            ]
            # Collect actual val ranges
            actual_val_ranges = []
            for ser in series:
                if ser.val and ser.val.numRef:
                    actual_val_ranges.append(ser.val.numRef.ref)
                else:
                    actual_val_ranges.append(None)

            # Check if all expected ranges are covered
            ranges_ok = all(
                any(
                    exp.replace("'", "").replace("$", "").upper() ==
                    (act or "").replace("'", "").replace("$", "").upper()
                    for act in actual_val_ranges
                )
                for exp in expected_val_ranges
            )

            if ranges_ok:
                print(f"PASS: Component 2 — 4 series with correct data ranges B-E rows 2-9 (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — 4 series found but data ranges mismatch.")
                print(f"  Expected: {expected_val_ranges}")
                print(f"  Found: {actual_val_ranges}")
        else:
            print(f"FAIL: Component 2 — Expected 4 series, found {num_series}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chart title is 'Mutual Fund Performance (Index = 100)' (0.2 points)
    # This FAILS on initial (no chart) → PASSES on golden (chart with correct title)
    try:
        title_text = extract_chart_title(line_chart)
        expected_title = "Mutual Fund Performance (Index = 100)"

        if title_text and title_text.strip() == expected_title:
            print(f"PASS: Component 3 — Chart title is '{title_text}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Expected title '{expected_title}', found: '{title_text}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Y-axis minimum value is set to 90 (0.2 points)
    # This FAILS on initial (no chart) → PASSES on golden (y_axis.scaling.min = 90.0)
    try:
        y_axis = line_chart.y_axis
        y_min = None
        if y_axis and y_axis.scaling:
            y_min = y_axis.scaling.min

        if y_min is not None and abs(float(y_min) - 90.0) < 0.01:
            print(f"PASS: Component 4 — Y-axis minimum is {y_min} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — Expected Y-axis min=90.0, found: {y_min}")
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
