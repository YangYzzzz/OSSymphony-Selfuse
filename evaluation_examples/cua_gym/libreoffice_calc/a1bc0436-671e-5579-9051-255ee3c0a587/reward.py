"""
Reward Script: Enable data table display below chart in LibreOffice Calc
Task ID: calc_chart_data_table_below_062
Domain: libreoffice_calc
Scoring:
  Component 1: Chart has a data table (dTable element present in chart XML) — 0.6 pts
  Component 2: Data table includes legend keys (showKeys=1) — 0.2 pts
  Component 3: Data table shows borders (showHorzBorder + showVertBorder or showOutline) — 0.2 pts
"""

import os
import zipfile

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_data_table_below_062'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires enabling the data table display (dTable) inside the chart area
    of the clustered column chart on the 'Presentation' sheet.
    The dTable element must be present in the chart XML with appropriate display settings.
    """
    total_score = 0.0

    # Precondition: file must be openable as a valid xlsx (zip)
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            chart_files = [f for f in z.namelist() if 'chart' in f.lower() and f.endswith('.xml')]
            if not chart_files:
                print("CRITICAL: No chart XML files found in the workbook")
                print("REWARD: 0.0")
                return 0.0
            # Read the first (and expected only) chart XML
            chart_xml = z.read(chart_files[0]).decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Data table element (dTable) is present in the chart XML (0.6 points)
    # This is the primary requirement: the chart must have a <dTable> element inside <plotArea>
    # which enables the data table display below the chart visuals.
    try:
        has_dtable = '<dTable>' in chart_xml or '<c:dTable>' in chart_xml
        if has_dtable:
            print("PASS: Component 1 — dTable element found in chart XML (data table is enabled) (0.6 pts)")
            total_score += 0.6
        else:
            print("FAIL: Component 1 — No dTable element found in chart XML (data table is not enabled)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Data table shows legend keys (showKeys=1) (0.2 points)
    # Legend keys in the data table allow readers to identify each series.
    # The context says "legend can be removed if data table includes legend keys".
    try:
        if has_dtable:
            has_show_keys = 'showKeys' in chart_xml and (
                'showKeys val="1"' in chart_xml or
                'showKeys val="true"' in chart_xml or
                'showKeys val="True"' in chart_xml
            )
            if has_show_keys:
                print("PASS: Component 2 — Data table includes legend keys (showKeys=1) (0.2 pts)")
                total_score += 0.2
            else:
                print("FAIL: Component 2 — Data table does not show legend keys (showKeys not set to 1)")
        else:
            print("SKIP: Component 2 — No dTable present, skipping legend keys check")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Data table shows borders (showHorzBorder and showVertBorder or showOutline) (0.2 points)
    # Proper borders make the data table readable and visually distinct.
    try:
        if has_dtable:
            has_horz_border = 'showHorzBorder val="1"' in chart_xml or 'showHorzBorder val="true"' in chart_xml
            has_vert_border = 'showVertBorder val="1"' in chart_xml or 'showVertBorder val="true"' in chart_xml
            has_outline = 'showOutline val="1"' in chart_xml or 'showOutline val="true"' in chart_xml
            has_borders = (has_horz_border and has_vert_border) or has_outline
            if has_borders:
                border_details = []
                if has_horz_border:
                    border_details.append("horzBorder")
                if has_vert_border:
                    border_details.append("vertBorder")
                if has_outline:
                    border_details.append("outline")
                print(f"PASS: Component 3 — Data table borders enabled: {', '.join(border_details)} (0.2 pts)")
                total_score += 0.2
            else:
                print("FAIL: Component 3 — Data table borders not enabled (showHorzBorder, showVertBorder, showOutline not set)")
        else:
            print("SKIP: Component 3 — No dTable present, skipping borders check")
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
