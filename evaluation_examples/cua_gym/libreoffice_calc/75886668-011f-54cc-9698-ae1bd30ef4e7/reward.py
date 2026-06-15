"""
Reward Script: Change the 'Competitors' slice color in the pie chart to bright red (#FF0000)
Task ID: calc_chart_pie_slice_color_036
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.7): 'Competitors' slice (dPt index 1) has solidFill srgbClr == 'FF0000'
  - Component 2 (0.3): Exactly 1 custom data point override exists (other slices unchanged)
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_chart_pie_slice_color_036'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    The task requires changing the 'Competitors' slice (index 1, 0-based) of the pie chart
    on the 'MarketShare' sheet to bright red (#FF0000).

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the workbook — gate: if file cannot be loaded, return 0.0
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gate: 'MarketShare' sheet must exist
    if 'MarketShare' not in wb.sheetnames:
        print("FAIL: Sheet 'MarketShare' not found in workbook.")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['MarketShare']

    # Gate: at least one chart must exist on the sheet
    charts = ws._charts
    if not charts:
        print("FAIL: No charts found on 'MarketShare' sheet.")
        print("REWARD: 0.0")
        return 0.0

    chart = charts[0]

    # Gate: chart must have at least one series
    if not chart.series:
        print("FAIL: Pie chart has no series.")
        print("REWARD: 0.0")
        return 0.0

    series = chart.series[0]

    # Component 1: 'Competitors' slice (data point index 1) is colored #FF0000 (0.7 points)
    # The Competitors row is row 3 in the sheet (0-indexed: index 1 in chart data).
    # In the initial file, dPt is empty. After the task, dPt has an entry at idx=1 with solidFill FF0000.
    try:
        competitors_dpt = None

        if hasattr(series, 'dPt') and series.dPt:
            for pt in series.dPt:
                if pt.idx == 1:
                    competitors_dpt = pt
                    break

        if competitors_dpt is not None:
            # Check the spPr has a solidFill with srgbClr == 'FF0000'
            spPr = competitors_dpt.spPr
            if (spPr is not None
                    and spPr.solidFill is not None
                    and hasattr(spPr.solidFill, 'srgbClr')
                    and spPr.solidFill.srgbClr is not None
                    and str(spPr.solidFill.srgbClr).upper().strip() == 'FF0000'):
                print(f"PASS: Component 1 — Competitors slice (dPt idx=1) has solidFill srgbClr='FF0000' (0.7 pts)")
                total_score += 0.7
            else:
                actual_color = (str(spPr.solidFill.srgbClr) if spPr and spPr.solidFill and hasattr(spPr.solidFill, 'srgbClr') else 'N/A')
                print(f"FAIL: Component 1 — Competitors slice color='{actual_color}', expected 'FF0000'")
        else:
            dpt_indices = [pt.idx for pt in series.dPt] if hasattr(series, 'dPt') else []
            print(f"FAIL: Component 1 — No data point override found for Competitors slice (idx=1). dPt indices: {dpt_indices}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Exactly 1 data point override exists (other slices not altered) (0.3 points)
    # In the initial file, dPt is empty ([]). After the task, exactly 1 override for idx=1 should exist.
    # This verifies that the agent only changed the Competitors slice and left others untouched.
    try:
        dpt_list = series.dPt if hasattr(series, 'dPt') else []
        dpt_count = len(dpt_list)

        if dpt_count == 1:
            # There is exactly 1 data point override
            only_pt = dpt_list[0]
            if only_pt.idx == 1:
                print(f"PASS: Component 2 — Exactly 1 custom data point override at idx=1 (other slices unchanged) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — 1 data point override exists, but it targets idx={only_pt.idx}, not idx=1 (Competitors)")
        elif dpt_count == 0:
            print(f"FAIL: Component 2 — No data point overrides found (dPt is empty)")
        else:
            # Multiple overrides — check if idx=1 exists and is the only red one
            idx_list = [pt.idx for pt in dpt_list]
            if 1 in idx_list:
                print(f"FAIL: Component 2 — {dpt_count} data point overrides found (expected exactly 1). Indices: {idx_list}")
            else:
                print(f"FAIL: Component 2 — {dpt_count} data point overrides found but none at idx=1. Indices: {idx_list}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

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
