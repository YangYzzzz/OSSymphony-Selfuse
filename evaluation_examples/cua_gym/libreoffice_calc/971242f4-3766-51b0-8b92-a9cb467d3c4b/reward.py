"""
Reward Script: Create a horizontal stacked bar chart for project time breakdown
Task ID: calc_chart_bar_horizontal_stacked_063
Domain: libreoffice_calc
Scoring:
  Component 1: Chart exists on 'ProjectTime' sheet           (0.2 pts)
  Component 2: Chart is horizontal stacked bar type          (0.3 pts)
  Component 3: Chart title is 'Project Time Breakdown (Hours)' (0.2 pts)
  Component 4: Chart has 4 series (all 4 project phases)     (0.2 pts)
  Component 5: Data references cover B-E cols, rows 2-5      (0.1 pts)
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_bar_horizontal_stacked_063'


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

    # Precondition gate: 'ProjectTime' sheet must exist
    if 'ProjectTime' not in wb.sheetnames:
        print("CRITICAL: Sheet 'ProjectTime' not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['ProjectTime']

    # Component 1: A chart exists on the 'ProjectTime' sheet (0.2 points)
    # The initial file has NO charts; the golden file must have at least one.
    try:
        charts = ws._charts
        if len(charts) >= 1:
            print(f"PASS: Component 1 — Chart exists on 'ProjectTime' sheet (found {len(charts)} chart(s)) (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 1 — No charts found on 'ProjectTime' sheet (expected at least 1)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Components 2–5 require at least one chart; skip if none found
    if total_score < 0.2:
        print(f"\nScore: {total_score}/1.0")
        final_score = min(total_score, 1.0)
        print(f"REWARD: {final_score}")
        return final_score

    chart = ws._charts[0]

    # Component 2: Chart is horizontal stacked bar type (0.3 points)
    # Horizontal bar chart: chart.type == 'bar' (not 'col') AND grouping == 'stacked'
    try:
        chart_type = getattr(chart, 'type', None)
        bar_dir = getattr(chart, 'barDir', None)
        grouping = getattr(chart, 'grouping', None)

        is_horizontal = (chart_type == 'bar') or (bar_dir == 'bar')
        is_stacked = (grouping == 'stacked')

        if is_horizontal and is_stacked:
            print(f"PASS: Component 2 — Chart is horizontal stacked bar (type={chart_type}, barDir={bar_dir}, grouping={grouping}) (0.3 pts)")
            total_score += 0.3
        elif is_horizontal and not is_stacked:
            print(f"FAIL: Component 2 — Chart is horizontal but not stacked (grouping={grouping}; expected 'stacked')")
        elif not is_horizontal and is_stacked:
            print(f"FAIL: Component 2 — Chart is stacked but not horizontal (type={chart_type}, barDir={bar_dir}; expected horizontal 'bar')")
        else:
            print(f"FAIL: Component 2 — Chart is neither horizontal nor stacked (type={chart_type}, barDir={bar_dir}, grouping={grouping})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chart title is 'Project Time Breakdown (Hours)' (0.2 points)
    expected_title = 'Project Time Breakdown (Hours)'
    try:
        title_obj = chart.title
        title_text = None
        if title_obj is not None:
            try:
                # Navigate openpyxl title object structure
                runs = title_obj.tx.rich.p[0].r
                title_text = ''.join([r.t for r in runs])
            except Exception:
                try:
                    title_text = str(title_obj.tx.rich.p[0].r[0].t)
                except Exception:
                    title_text = None

        if title_text is not None and title_text.strip() == expected_title:
            print(f"PASS: Component 3 — Chart title is '{title_text}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Expected title '{expected_title}', found: {repr(title_text)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Chart has exactly 4 series (Planning, Development, Testing, Deployment) (0.2 points)
    # Task specifies 4 phases; each series should correspond to one phase column (B, C, D, E).
    try:
        num_series = len(chart.series)
        if num_series == 4:
            print(f"PASS: Component 4 — Chart has 4 series covering all 4 project phases (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — Expected 4 series (Planning/Development/Testing/Deployment), found {num_series}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Data references cover columns B through E, rows 2-5 (all 4 projects x 4 phases) (0.1 points)
    # Each series should reference one of the 4 phase columns (B,C,D,E), rows 2–5.
    expected_data_cols = {'$B$2:$B$5', '$C$2:$C$5', '$D$2:$D$5', '$E$2:$E$5'}
    try:
        actual_data_refs = set()
        for ser in chart.series:
            try:
                ref = ser.val.numRef.ref
                # Normalize: strip sheet prefix if present (e.g. "'ProjectTime'!$B$2:$B$5" -> "$B$2:$B$5")
                if '!' in ref:
                    ref = ref.split('!')[1]
                actual_data_refs.add(ref)
            except Exception:
                pass

        if actual_data_refs == expected_data_cols:
            print(f"PASS: Component 5 — Data references match expected columns B-E rows 2-5: {actual_data_refs} (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 5 — Data references mismatch. Expected {expected_data_cols}, found {actual_data_refs}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
