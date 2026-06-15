"""
Reward Script: Add custom asymmetric error bars to chart series
Task ID: calc_gg2_025
Domain: libreoffice_calc
Scoring:
  C1 (0.20) - Error bars exist on the Forecast series
  C2 (0.15) - Error bar type is 'both' (asymmetric positive+negative)
  C3 (0.15) - Error value type is 'cust' (custom cell range)
  C4 (0.10) - Error direction is 'y' (vertical)
  C5 (0.20) - Positive error values reference Projections D2:D13
  C6 (0.20) - Negative error values reference Projections E2:E13
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_gg2_025'


def normalize_range_ref(ref_str):
    """Normalize a cell range reference for comparison.
    Strips sheet name variants, dollar signs, and lowercases.
    Returns just the cell range like 'd2:d13'.
    """
    if not ref_str:
        return ''
    # Remove quotes around sheet name if present
    s = ref_str.strip()
    # Extract just the cell range part (after the !)
    if '!' in s:
        s = s.split('!', 1)[1]
    # Remove dollar signs and lowercase
    s = s.replace('$', '').lower()
    return s


def verify_task(file_path):
    """
    Verify that the Forecast series in the embedded chart on the Projections
    sheet has custom asymmetric error bars sourced from D2:D13 (positive)
    and E2:E13 (negative).
    Returns: float between 0.0 and 1.0
    """
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Projections sheet exists
    if 'Projections' not in wb.sheetnames:
        print("FAIL: 'Projections' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Projections']

    # Precondition: at least one chart exists
    if not ws._charts or len(ws._charts) == 0:
        print("FAIL: No charts found on 'Projections' sheet")
        print("REWARD: 0.0")
        return 0.0

    chart = ws._charts[0]

    # Find the Forecast series
    forecast_series = None
    for s in chart.series:
        # Check series title reference
        try:
            if s.title and hasattr(s.title, 'strRef') and s.title.strRef:
                ref = s.title.strRef.f
                if ref and 'B1' in ref:
                    forecast_series = s
                    break
        except Exception:
            pass
        # Also check if title value contains 'Forecast'
        try:
            if s.title and hasattr(s.title, 'v') and s.title.v:
                if 'forecast' in str(s.title.v).lower():
                    forecast_series = s
                    break
        except Exception:
            pass

    # If only one series, assume it is the Forecast series
    if forecast_series is None and len(chart.series) == 1:
        forecast_series = chart.series[0]
        print("INFO: Only one series found, assuming it is 'Forecast'")

    if forecast_series is None:
        print("FAIL: Could not find the 'Forecast' series in the chart")
        print("REWARD: 0.0")
        return 0.0

    err_bars = forecast_series.errBars

    # Component 1: Error bars exist on the Forecast series (0.20 points)
    try:
        if err_bars is not None:
            print(f"PASS: Component 1 - Error bars exist on Forecast series (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - No error bars on Forecast series (errBars is None)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    if err_bars is None:
        # No further checks possible
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Error bar type is 'both' (0.15 points)
    try:
        bar_type = err_bars.errBarType
        if bar_type == 'both':
            print(f"PASS: Component 2 - errBarType is 'both' (asymmetric) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 - errBarType is '{bar_type}', expected 'both'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Error value type is 'cust' (custom cell range) (0.15 points)
    try:
        val_type = err_bars.errValType
        if val_type == 'cust':
            print(f"PASS: Component 3 - errValType is 'cust' (custom cell range) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - errValType is '{val_type}', expected 'cust'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Error direction is 'y' (0.10 points)
    try:
        err_dir = err_bars.errDir
        if err_dir == 'y':
            print(f"PASS: Component 4 - errDir is 'y' (vertical) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 - errDir is '{err_dir}', expected 'y'")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Positive error values reference D2:D13 on Projections (0.20 points)
    try:
        plus_ref = None
        if err_bars.plus and hasattr(err_bars.plus, 'numRef') and err_bars.plus.numRef:
            plus_ref = err_bars.plus.numRef.f
        if plus_ref:
            normalized = normalize_range_ref(plus_ref)
            if normalized == 'd2:d13':
                print(f"PASS: Component 5 - Positive error range is '{plus_ref}' -> D2:D13 (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 - Positive error range normalized to '{normalized}', expected 'd2:d13' (raw: '{plus_ref}')")
        else:
            print(f"FAIL: Component 5 - No positive error range reference found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Negative error values reference E2:E13 on Projections (0.20 points)
    try:
        minus_ref = None
        if err_bars.minus and hasattr(err_bars.minus, 'numRef') and err_bars.minus.numRef:
            minus_ref = err_bars.minus.numRef.f
        if minus_ref:
            normalized = normalize_range_ref(minus_ref)
            if normalized == 'e2:e13':
                print(f"PASS: Component 6 - Negative error range is '{minus_ref}' -> E2:E13 (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 6 - Negative error range normalized to '{normalized}', expected 'e2:e13' (raw: '{minus_ref}')")
        else:
            print(f"FAIL: Component 6 - No negative error range reference found")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

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
