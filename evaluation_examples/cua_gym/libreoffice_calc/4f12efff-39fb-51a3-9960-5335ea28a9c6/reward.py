"""
Reward Script: Format each bar in the column chart to have a distinct color
Task ID: calc_chart_column_color_each_071
Domain: libreoffice_calc
Scoring:
  Component 1: Chart series has data points with individual color formatting (0.3 pts)
  Component 2: Exactly 5 data points exist (one per bar/category) (0.3 pts)
  Component 3: Each data point has the exact required color in order (0.4 pts)
               idx0=FF0000 (Red), idx1=0000FF (Blue), idx2=00AA00 (Green),
               idx3=FF8C00 (Orange), idx4=800080 (Purple)
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_column_color_each_071'

# Expected colors per data point index (0-based)
# North=idx0: Red, South=idx1: Blue, East=idx2: Green, West=idx3: Orange, Central=idx4: Purple
EXPECTED_COLORS = {
    0: 'FF0000',   # North -> Red
    1: '0000FF',   # South -> Blue
    2: '00AA00',   # East  -> Green
    3: 'FF8C00',   # West  -> Orange
    4: '800080',   # Central -> Purple
}

CATEGORY_NAMES = ['North', 'South', 'East', 'West', 'Central']


def get_dp_color(dp):
    """Extract the srgbClr value from a data point's solidFill, or None if not set."""
    try:
        if dp.spPr and dp.spPr.solidFill and dp.spPr.solidFill.srgbClr:
            return dp.spPr.solidFill.srgbClr.upper()
    except Exception:
        pass
    return None


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

    # Precondition gate: required sheet must exist
    if 'ColorBars' not in wb.sheetnames:
        print("CRITICAL: Sheet 'ColorBars' not found in workbook.")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['ColorBars']

    # Precondition gate: chart must exist
    if not ws._charts:
        print("CRITICAL: No chart found on sheet 'ColorBars'.")
        print("REWARD: 0.0")
        return 0.0

    chart = ws._charts[0]

    # Precondition gate: chart must have at least one series
    if not chart.series:
        print("CRITICAL: Chart has no series.")
        print("REWARD: 0.0")
        return 0.0

    series = chart.series[0]

    # Component 1: Chart series has individual data point color formatting (0.3 pts)
    # This FAILS on initial (dPt is empty) and PASSES on golden (dPt has 5 entries)
    try:
        dpt_count = len(series.dPt)
        if dpt_count > 0:
            print(f"PASS: Component 1 — Series has {dpt_count} individual data point(s) with color formatting (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No individual data point color formatting found (dPt is empty); all bars use default color")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check data points: {e}")

    # Component 2: Exactly 5 data points exist (one per category/bar) (0.3 pts)
    # This FAILS on initial (0 dPts) and PASSES on golden (5 dPts)
    try:
        dpt_count = len(series.dPt)
        if dpt_count == 5:
            print(f"PASS: Component 2 — Exactly 5 data points found, matching the 5 categories {CATEGORY_NAMES} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected 5 data points (one per bar), found {dpt_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check data point count: {e}")

    # Component 3: Each data point has the exact required color (0.4 pts)
    # Checked per-point; full 0.4 only if ALL 5 are correct.
    # This FAILS on initial (no data points at all) and PASSES on golden (all 5 correct).
    try:
        dpts = series.dPt
        if len(dpts) == 5:
            # Build a map from idx -> color for the data points present
            idx_to_color = {}
            for dp in dpts:
                color = get_dp_color(dp)
                idx_to_color[dp.idx] = color

            correct_count = 0
            for idx, expected_color in EXPECTED_COLORS.items():
                actual_color = idx_to_color.get(idx)
                category = CATEGORY_NAMES[idx]
                if actual_color and actual_color.upper() == expected_color.upper():
                    print(f"  PASS: dp idx={idx} ({category}): color={actual_color} (expected {expected_color})")
                    correct_count += 1
                else:
                    print(f"  FAIL: dp idx={idx} ({category}): found {actual_color!r}, expected {expected_color!r}")

            if correct_count == 5:
                print(f"PASS: Component 3 — All 5 data points have correct colors (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 3 — Only {correct_count}/5 data points have correct colors; no partial credit for this component")
        else:
            print(f"FAIL: Component 3 — Cannot check colors: need exactly 5 data points, got {len(dpts)}")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not verify per-point colors: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
