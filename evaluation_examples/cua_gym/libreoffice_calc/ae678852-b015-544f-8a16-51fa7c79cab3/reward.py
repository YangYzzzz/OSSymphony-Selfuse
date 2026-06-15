"""
Reward Script: Add error bars to the line chart showing ±1 SD for each data point
Task ID: calc_chart_error_bars_069
Domain: libreoffice_calc
Scoring:
  Component 1: Error bars exist on the chart series (0.4 pts)
  Component 2: Error bar direction='y', type='both', valType='cust' (0.3 pts)
  Component 3: Error bar values reference Std Dev column C (rows 2-6) (0.2 pts)
  Component 4: Chart title 'Experimental Results' preserved (0.1 pts)
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_error_bars_069'


def get_chart_title_text(chart):
    """Extract chart title text from openpyxl chart object."""
    try:
        if chart.title is None:
            return None
        title_obj = chart.title
        tx = title_obj.tx
        if tx and tx.rich:
            for p in tx.rich.p:
                for r in p.r:
                    return r.t
    except Exception:
        pass
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Add error bars (±1 SD) to the line chart in 'Experiment' sheet.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must be loadable
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Experiment' sheet must exist
    if 'Experiment' not in wb.sheetnames:
        print("FAIL: 'Experiment' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Experiment']

    # Precondition: at least one chart must exist on the sheet
    charts = ws._charts
    if not charts:
        print("FAIL: No charts found on 'Experiment' sheet")
        print("REWARD: 0.0")
        return 0.0

    chart = charts[0]

    # Precondition: chart must have at least one data series
    if not chart.series:
        print("FAIL: Chart has no data series")
        print("REWARD: 0.0")
        return 0.0

    series = chart.series[0]

    # Component 1: Error bars exist on the data series (0.4 points)
    # This FAILS on initial (errBars=None) and PASSES on golden (errBars is ErrorBars object)
    try:
        if series.errBars is not None:
            print(f"PASS: Component 1 — Error bars found on data series (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No error bars on series (errBars is None)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Error bar properties are correct (0.3 points)
    # errDir='y' (Y-axis), errBarType='both' (up and down), errValType='cust' (custom values)
    # This FAILS on initial (no errBars) and PASSES on golden
    try:
        eb = series.errBars
        if eb is not None:
            dir_ok = (eb.errDir == 'y')
            type_ok = (eb.errBarType == 'both')
            val_type_ok = (eb.errValType == 'cust')
            if dir_ok and type_ok and val_type_ok:
                print(f"PASS: Component 2 — errDir='{eb.errDir}', errBarType='{eb.errBarType}', errValType='{eb.errValType}' (0.3 pts)")
                total_score += 0.3
            else:
                details = []
                if not dir_ok:
                    details.append(f"errDir='{eb.errDir}' (expected 'y')")
                if not type_ok:
                    details.append(f"errBarType='{eb.errBarType}' (expected 'both')")
                if not val_type_ok:
                    details.append(f"errValType='{eb.errValType}' (expected 'cust')")
                print(f"FAIL: Component 2 — Incorrect error bar properties: {', '.join(details)}")
        else:
            print(f"FAIL: Component 2 — Cannot check properties (errBars is None)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error bar values reference Std Dev column C (C2:C6) (0.2 points)
    # The plus and minus references should point to 'Experiment'!$C$2:$C$6
    # This FAILS on initial (no errBars) and PASSES on golden
    try:
        eb = series.errBars
        if eb is not None:
            plus_ref = None
            minus_ref = None
            if eb.plus and eb.plus.numRef:
                plus_ref = eb.plus.numRef.f
            if eb.minus and eb.minus.numRef:
                minus_ref = eb.minus.numRef.f

            # Check that both plus and minus reference column C rows 2-6
            # Allow for minor formatting differences (with or without $ signs, sheet name quoting)
            def ref_points_to_c2_c6(ref):
                if ref is None:
                    return False
                # Normalize: remove $ signs and quotes, lowercase
                norm = ref.replace('$', '').replace("'", '').lower()
                # Must reference Experiment sheet and column C rows 2-6
                return 'experiment' in norm and 'c2' in norm and 'c6' in norm

            plus_ok = ref_points_to_c2_c6(plus_ref)
            minus_ok = ref_points_to_c2_c6(minus_ref)

            if plus_ok and minus_ok:
                print(f"PASS: Component 3 — plus ref='{plus_ref}', minus ref='{minus_ref}' both reference Std Dev column (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Error bar refs don't correctly reference C2:C6: plus='{plus_ref}', minus='{minus_ref}'")
        else:
            print(f"FAIL: Component 3 — Cannot check refs (errBars is None)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Chart title 'Experimental Results' is preserved (0.1 points)
    # The title must remain unchanged after adding error bars
    # This PASSES on both initial and golden — used as integrity check
    # NOTE: Since this passes on the initial file too, we only award this point
    # if error bars are also present (compound condition to keep initial score at 0.0)
    try:
        eb = series.errBars
        title_text = get_chart_title_text(chart)
        title_ok = (title_text == 'Experimental Results')
        errbar_present = (eb is not None)

        if errbar_present and title_ok:
            print(f"PASS: Component 4 — Chart title '{title_text}' preserved with error bars present (0.1 pts)")
            total_score += 0.1
        elif not errbar_present:
            print(f"FAIL: Component 4 — Error bars absent (title preservation only scored when error bars present)")
        elif not title_ok:
            print(f"FAIL: Component 4 — Chart title is '{title_text}', expected 'Experimental Results'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 10)
    print(f"\nScore: {round(total_score, 4)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
