"""
Reward Script: Create a chart on the 'Summary' sheet that combines revenue data from Q1 and Q2 sheets
Task ID: calc_chart_multi_sheet_series_068
Domain: libreoffice_calc
Scoring:
  Component 1: Chart exists on Summary sheet (0.3 points)
  Component 2: Chart has 2 series referencing both Q1 and Q2 sheets (0.4 points)
  Component 3: Chart title is 'H1 2024 Monthly Revenue' (0.3 points)
  Total: 1.0
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_multi_sheet_series_068'


def get_chart_title_text(chart):
    """Extract text from a chart title object."""
    try:
        if chart.title is None:
            return None
        # Try direct title text attribute
        if hasattr(chart.title, 'tx') and chart.title.tx:
            rich = chart.title.tx.rich
            if rich and rich.p:
                parts = []
                for para in rich.p:
                    if para.r:
                        for run in para.r:
                            if run.t:
                                parts.append(run.t)
                if parts:
                    return ''.join(parts)
        # Fallback: parse string representation
        title_str = str(chart.title)
        matches = re.findall(r"t='([^']+)'", title_str)
        if matches:
            return ''.join(matches)
        return None
    except Exception as e:
        print(f"  Error extracting title: {e}")
        return None


def get_series_ref(ser):
    """Extract the value reference formula from a series."""
    try:
        if ser.val and ser.val.numRef:
            return ser.val.numRef.f
        return None
    except Exception:
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Scoring rubric:
    - Component 1: A chart exists on the 'Summary' sheet (0.3 points)
    - Component 2: Chart has 2 series, one referencing Q1 data and one referencing Q2 data (0.4 points)
    - Component 3: Chart title equals 'H1 2024 Monthly Revenue' (0.3 points)
    """
    total_score = 0.0

    # Load the workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Summary' sheet must exist
    if 'Summary' not in wb.sheetnames:
        print("FAIL: 'Summary' sheet not found in workbook")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    ws_summary = wb['Summary']

    # Component 1: A chart exists on the 'Summary' sheet (0.3 points)
    try:
        charts = ws_summary._charts
        if charts and len(charts) >= 1:
            print(f"PASS: Component 1 — Chart exists on 'Summary' sheet ({len(charts)} chart(s) found) (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 — No chart found on 'Summary' sheet (expected at least 1)")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check charts on Summary sheet: {e}")

    # Only proceed to component 2 and 3 if there's at least one chart
    if total_score < 0.3:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    chart = ws_summary._charts[0]

    # Component 2: Chart has 2 series from Q1 and Q2 sheets (0.4 points)
    try:
        series_list = chart.series
        if len(series_list) < 2:
            print(f"FAIL: Component 2 — Chart has {len(series_list)} series, expected 2 (one for Q1 and one for Q2)")
        else:
            # Check that the series reference data from BOTH Q1 and Q2 sheets
            refs_q1 = []
            refs_q2 = []
            for ser in series_list:
                ref = get_series_ref(ser)
                if ref:
                    if 'Q1' in ref or "'Q1'" in ref:
                        refs_q1.append(ref)
                    if 'Q2' in ref or "'Q2'" in ref:
                        refs_q2.append(ref)

            has_q1 = len(refs_q1) >= 1
            has_q2 = len(refs_q2) >= 1

            if has_q1 and has_q2:
                print(f"PASS: Component 2 — Chart has {len(series_list)} series referencing both Q1 ({refs_q1}) and Q2 ({refs_q2}) (0.4 pts)")
                total_score += 0.4
            elif has_q1 and not has_q2:
                print(f"FAIL: Component 2 — Chart references Q1 data but no Q2 data found in series refs. Q1={refs_q1}, series count={len(series_list)}")
            elif has_q2 and not has_q1:
                print(f"FAIL: Component 2 — Chart references Q2 data but no Q1 data found in series refs. Q2={refs_q2}, series count={len(series_list)}")
            else:
                # Check in a looser way: title references
                all_refs = [get_series_ref(ser) for ser in series_list if get_series_ref(ser)]
                print(f"FAIL: Component 2 — Chart series do not reference Q1 or Q2 sheets. Refs found: {all_refs}")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not verify series references: {e}")

    # Component 3: Chart title is 'H1 2024 Monthly Revenue' (0.3 points)
    try:
        title_text = get_chart_title_text(chart)
        expected_title = 'H1 2024 Monthly Revenue'
        if title_text and title_text.strip() == expected_title:
            print(f"PASS: Component 3 — Chart title is '{title_text}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Expected chart title '{expected_title}', found: '{title_text}'")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not verify chart title: {e}")

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
