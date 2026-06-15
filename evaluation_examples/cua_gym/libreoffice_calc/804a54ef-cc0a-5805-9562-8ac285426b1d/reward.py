"""
Reward Script: Add Y-error bars to Experiment A series in embedded chart
Task ID: calc_gg2_003
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Experiment A series has error bars
  Component 2 (0.3): Error bars are Y-direction, both pos/neg (errDir='y', errBarType='both')
  Component 3 (0.2): Error bar type is fixedVal with val=5.0
  Component 4 (0.2): Experiment B and C have no error bars
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'calc_gg2_003'


def persist_app_state(domain):
    """Save any unsaved LibreOffice state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
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

    # Precondition: 'Lab Results' sheet must exist
    if 'Lab Results' not in wb.sheetnames:
        print("CRITICAL: 'Lab Results' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Lab Results']

    # Precondition: chart must exist
    charts = ws._charts
    if len(charts) == 0:
        print("CRITICAL: No charts found on 'Lab Results' sheet")
        print("REWARD: 0.0")
        return 0.0

    chart = charts[0]

    # Precondition: chart must have at least 3 series
    if len(chart.series) < 3:
        print(f"CRITICAL: Expected at least 3 series, found {len(chart.series)}")
        print("REWARD: 0.0")
        return 0.0

    # Identify Experiment A series (series 0, referencing column B = 'Experiment A')
    exp_a = chart.series[0]
    exp_b = chart.series[1]
    exp_c = chart.series[2]

    # Component 1: Experiment A series has error bars (0.3 points)
    # This FAILS on initial (errBars is None) and PASSES on golden (errBars present)
    try:
        eb = getattr(exp_a, 'errBars', None)
        if eb is not None:
            print(f"PASS: Component 1 — Experiment A has error bars (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Experiment A has no error bars")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Error bars are Y-direction with both positive and negative (0.3 points)
    # errDir='y' and errBarType='both'
    try:
        eb = getattr(exp_a, 'errBars', None)
        if eb is not None:
            dir_ok = (eb.errDir == 'y')
            type_ok = (eb.errBarType == 'both')
            if dir_ok and type_ok:
                print(f"PASS: Component 2 — errDir='y', errBarType='both' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — errDir={eb.errDir} (want 'y'), errBarType={eb.errBarType} (want 'both')")
        else:
            print(f"FAIL: Component 2 — No error bars on Experiment A to check direction/type")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error bar value type is fixedVal and val=5.0 (0.2 points)
    try:
        eb = getattr(exp_a, 'errBars', None)
        if eb is not None:
            val_type_ok = (eb.errValType == 'fixedVal')
            val_ok = False
            if eb.val is not None:
                val_ok = abs(float(eb.val) - 5.0) < 0.01
            if val_type_ok and val_ok:
                print(f"PASS: Component 3 — errValType='fixedVal', val={eb.val} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — errValType={eb.errValType} (want 'fixedVal'), val={eb.val} (want 5.0)")
        else:
            print(f"FAIL: Component 3 — No error bars on Experiment A to check value")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Experiment A has error bars AND Experiment B/C do NOT (0.2 points)
    # Compound check: anchored to the task change (A has errBars) + preservation (B,C unchanged)
    # This FAILS on initial (A has no errBars) and PASSES on golden (A has errBars, B/C don't)
    try:
        eb_a = getattr(exp_a, 'errBars', None)
        eb_b = getattr(exp_b, 'errBars', None)
        eb_c = getattr(exp_c, 'errBars', None)
        a_has = (eb_a is not None)
        b_clean = (eb_b is None)
        c_clean = (eb_c is None)
        if a_has and b_clean and c_clean:
            print(f"PASS: Component 4 — Exp A has error bars, Exp B and C do not (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — A has errBars={a_has}, B has errBars={not b_clean}, C has errBars={not c_clean}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before checking
persist_app_state("libreoffice_calc")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
