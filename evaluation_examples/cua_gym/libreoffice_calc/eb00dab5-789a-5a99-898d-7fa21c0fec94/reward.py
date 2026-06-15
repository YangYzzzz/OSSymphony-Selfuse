"""
Reward Script: Set print area to chart only (E1:L20), excluding data table
Task ID: calc_chart_print_area_chart_078
Domain: libreoffice_calc

Scoring:
  Component 1: Print area is set to E1:L20 (chart only, excludes A1:C8 data table) — 0.6 pts
  Component 2: Chart is preserved and present in the 'Report' sheet — 0.4 pts
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_print_area_chart_078'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    Task: Set up the chart so that it is the only thing that prints —
    define a print area that includes just the chart (E1:L20) and
    excludes the source data table (A1:C8).

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: verify the 'Report' sheet exists
    if 'Report' not in wb.sheetnames:
        print("FAIL: 'Report' sheet not found in workbook")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    ws = wb['Report']

    # -----------------------------------------------------------------------
    # Component 1: Print area is set to E1:L20 (chart only) (0.6 points)
    # The task requires the print area to be narrowed from A1:L20 to E1:L20
    # so that only the chart area is printed, excluding the data table (A:C).
    # This FAILS on the initial file (print area is A1:L20)
    # and PASSES on the golden file (print area is E1:L20).
    # -----------------------------------------------------------------------
    try:
        print_area = ws.print_area
        print(f"INFO: Current print_area = {print_area!r}")

        # Normalize: strip sheet-prefix and dollar signs for comparison
        # Accepted forms: "'Report'!$E$1:$L$20" or "$E$1:$L$20" or "E1:L20"
        if print_area:
            # Remove sheet prefix if present
            normalized = print_area.split('!')[-1] if '!' in print_area else print_area
            # Remove dollar signs
            normalized = normalized.replace('$', '').strip()
        else:
            normalized = ''

        expected = 'E1:L20'
        if normalized.upper() == expected.upper():
            print(f"PASS: Component 1 — Print area correctly set to {expected} (chart only) (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — Expected print area {expected}, found {normalized!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check print area: {e}")

    # -----------------------------------------------------------------------
    # Component 2: Chart is preserved in the 'Report' sheet (0.4 points)
    # The task says "the chart itself should remain unchanged". We verify
    # that exactly one chart is present and it is a BarChart (clustered column).
    # This FAILS on the initial file only if combined with Component 1 check;
    # here it independently verifies the chart was NOT deleted/replaced.
    # NOTE: The initial file also has a chart, so we ONLY award these points
    # if Component 1 ALSO passes (print area changed), making this a compound
    # check anchored to the task change.
    # -----------------------------------------------------------------------
    try:
        charts = ws._charts
        chart_count = len(charts)
        print(f"INFO: Chart count = {chart_count}")

        if chart_count >= 1:
            chart = charts[0]
            chart_type = type(chart).__name__
            print(f"INFO: Chart type = {chart_type}")

            # Verify it is still a BarChart (clustered column chart as required)
            if chart_type == 'BarChart':
                # Only award this component if the print area was ALSO changed
                # (ensures we score task-introduced changes, not pre-existing state)
                if total_score > 0:
                    print(f"PASS: Component 2 — Chart preserved (BarChart, count={chart_count}) (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 2 — Chart exists but print area was not updated; "
                          f"not awarding chart preservation points without the primary task change")
            else:
                print(f"FAIL: Component 2 — Chart type changed: expected BarChart, found {chart_type}")
        else:
            print(f"FAIL: Component 2 — No chart found in 'Report' sheet (count={chart_count})")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check chart: {e}")

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
