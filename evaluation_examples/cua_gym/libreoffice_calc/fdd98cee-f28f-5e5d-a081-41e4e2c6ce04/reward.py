"""
Reward Script: Add chart title 'Annual Revenue Trend' to the column chart
Task ID: calc_chart_title_add_016
Domain: libreoffice_calc
Scoring:
  Component 1: Chart has a title object set (not None)     — 0.4 pts
  Component 2: Chart title text matches 'Annual Revenue Trend' — 0.6 pts
  Total: 1.0 pts
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_title_add_016'


def get_chart_title_text(chart):
    """
    Extract plain-text title from an openpyxl chart object.
    The title may be stored as a rich-text structure:
      chart.title.tx.rich.p[*].r[*].t
    or as a simple string reference.
    Returns the concatenated text string, or None if not found.
    """
    try:
        title_obj = chart.title
        if title_obj is None:
            return None

        tx = getattr(title_obj, 'tx', None)
        if tx is None:
            return None

        # Rich text path: tx.rich.p[*].r[*].t
        rich = getattr(tx, 'rich', None)
        if rich is not None:
            paragraphs = getattr(rich, 'p', [])
            parts = []
            for para in paragraphs:
                runs = getattr(para, 'r', [])
                for run in runs:
                    t = getattr(run, 't', None)
                    if t is not None:
                        parts.append(str(t))
            if parts:
                return ''.join(parts)

        # String reference path: tx.strRef.f or tx.strRef.strCache
        str_ref = getattr(tx, 'strRef', None)
        if str_ref is not None:
            f = getattr(str_ref, 'f', None)
            if f:
                return str(f)

        return None
    except Exception:
        return None


def verify_task(file_path):
    """
    Verify that the column chart on the 'Revenue' sheet has been given
    the title 'Annual Revenue Trend'.

    Scoring:
      Component 1: Chart title object exists (not None)          — 0.4 pts
      Component 2: Title text equals 'Annual Revenue Trend'      — 0.6 pts

    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Load workbook — precondition gate
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Sheet presence — precondition gate (no points)
    if 'Revenue' not in wb.sheetnames:
        print("FAIL: Sheet 'Revenue' not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Revenue']

    # Chart presence — precondition gate (no points)
    charts = ws._charts
    if not charts:
        print("FAIL: No charts found on sheet 'Revenue'")
        print("REWARD: 0.0")
        return 0.0

    chart = charts[0]

    # Component 1: Chart title object exists (not None) — 0.4 points
    # The initial file has chart.title == None; the golden file has a Title object.
    try:
        if chart.title is not None:
            print("PASS: Component 1 — Chart title object is set (not None) (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 — Chart title is None; expected a Title object")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Title text equals 'Annual Revenue Trend' — 0.6 points
    # This is the core requirement of the task.
    try:
        EXPECTED_TITLE = 'Annual Revenue Trend'
        title_text = get_chart_title_text(chart)
        if title_text is not None and title_text.strip() == EXPECTED_TITLE:
            print(f"PASS: Component 2 — Chart title text is '{title_text}' (0.6 pts)")
            total_score += 0.6
        else:
            print(
                f"FAIL: Component 2 — Expected title '{EXPECTED_TITLE}', "
                f"found: {repr(title_text)}"
            )
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
