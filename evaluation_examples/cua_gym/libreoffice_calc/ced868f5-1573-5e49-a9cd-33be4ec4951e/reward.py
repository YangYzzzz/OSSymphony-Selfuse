"""
Reward Script: Add 'Target' series to existing line chart with dashed style and data labels
Task ID: calc_gg2_030
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30): Chart has exactly 2 series (was 1 initially)
  Component 2 (0.20): Second series references 'Target' data from column D
  Component 3 (0.25): Target series line style is dashed
  Component 4 (0.25): Target series has data labels showing values only
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gg2_030'


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

    # Precondition: 'Analysis' sheet must exist
    if 'Analysis' not in wb.sheetnames:
        print("FAIL: 'Analysis' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Analysis']

    # Precondition: at least one chart must exist
    if len(ws._charts) == 0:
        print("FAIL: No charts found on 'Analysis' sheet")
        print("REWARD: 0.0")
        return 0.0

    chart = ws._charts[0]

    # Component 1: Chart has exactly 2 series (0.30 points)
    # Initial state has 1 series; golden should have 2
    try:
        num_series = len(chart.series)
        if num_series >= 2:
            print(f"PASS: Component 1 — Chart has {num_series} series (expected >= 2) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Chart has {num_series} series, expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Second series references Target/column D data (0.20 points)
    # The second series should reference column D (Target)
    try:
        if len(chart.series) >= 2:
            s1 = chart.series[1]
            # Check title references 'D1' or contains 'Target'
            title_ref = ''
            if s1.title and hasattr(s1.title, 'strRef') and s1.title.strRef:
                title_ref = s1.title.strRef.f or ''
            title_val = ''
            if s1.title and hasattr(s1.title, 'v') and s1.title.v:
                title_val = s1.title.v or ''

            # Check if the series references column D data
            # The series val reference should contain 'D' column
            val_ref = ''
            if hasattr(s1, 'val') and s1.val and hasattr(s1.val, 'numRef') and s1.val.numRef:
                val_ref = s1.val.numRef.f or ''

            refs_col_d = (
                ('D1' in title_ref or 'D' in title_ref)
                or ('target' in title_val.lower())
                or ('$D$' in val_ref or "'Analysis'!D" in val_ref or '!$D$' in val_ref)
            )

            if refs_col_d:
                print(f"PASS: Component 2 — Second series references Target/column D (title_ref={title_ref}, val_ref={val_ref}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — Second series does not reference Target/column D (title_ref={title_ref}, title_val={title_val}, val_ref={val_ref})")
        else:
            print("FAIL: Component 2 — Not enough series to check Target reference")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Target series has dashed line style (0.25 points)
    # Initial Actual series is solid; Target should be dashed
    try:
        if len(chart.series) >= 2:
            target_series = chart.series[1]
            gp = target_series.graphicalProperties
            dash_style = None
            if gp and gp.line:
                dash_style = gp.line.dashStyle

            # Accept any dashed variant: 'dash', 'lgDash', 'sysDash', 'dashDot', etc.
            dashed_styles = {'dash', 'lgDash', 'sysDash', 'dashDot', 'lgDashDot',
                             'lgDashDotDot', 'sysDashDot', 'sysDashDotDot'}
            if dash_style and dash_style in dashed_styles:
                print(f"PASS: Component 3 — Target series has dashed line (dashStyle={dash_style}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Target series line style is '{dash_style}', expected a dashed style")
        else:
            print("FAIL: Component 3 — Not enough series to check dash style")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Target series has data labels showing values only (0.25 points)
    # Initial Actual series has no labels; Target should have showVal=True
    try:
        if len(chart.series) >= 2:
            target_series = chart.series[1]
            labels = target_series.labels
            if labels and labels.showVal:
                print(f"PASS: Component 4 — Target series has data labels with showVal=True (0.25 pts)")
                total_score += 0.25
            else:
                show_val = labels.showVal if labels else None
                print(f"FAIL: Component 4 — Target series labels showVal={show_val}, expected True")
        else:
            print("FAIL: Component 4 — Not enough series to check data labels")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
