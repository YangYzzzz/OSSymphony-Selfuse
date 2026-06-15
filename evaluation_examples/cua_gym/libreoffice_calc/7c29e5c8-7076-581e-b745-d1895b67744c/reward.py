"""
Reward Script: Create a Stacked Area chart from data in A1:D7 on 'Trends' sheet
Task ID: calc_gg3_032
Domain: libreoffice_calc
Scoring:
  Component 1: Chart exists on Trends sheet (0.25)
  Component 2: Chart is AreaChart with stacked grouping (0.30)
  Component 3: Chart has 3 series from correct columns B, C, D (0.25)
  Component 4: Legend present at bottom position (0.20)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gg3_032'


def persist_app_state(domain: str):
    """Attempt to save any unsaved LibreOffice changes via Ctrl+S."""
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

    # Check that 'Trends' sheet exists (precondition gate)
    if 'Trends' not in wb.sheetnames:
        print("CRITICAL: 'Trends' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Trends']
    charts = ws._charts

    # Component 1: At least one chart exists on the Trends sheet (0.25 points)
    try:
        if len(charts) >= 1:
            print(f"PASS: Component 1 — Chart exists on Trends sheet, count={len(charts)} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — No charts found on Trends sheet")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if len(charts) == 0:
        # No chart means no further checks can pass
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    chart = charts[0]

    # Component 2: Chart is an AreaChart with 'stacked' grouping (0.30 points)
    try:
        is_area = (chart.tagname == 'areaChart')
        grouping = getattr(chart, 'grouping', None)
        is_stacked = (grouping == 'stacked')

        if is_area and is_stacked:
            print(f"PASS: Component 2 — AreaChart with stacked grouping (0.30 pts)")
            total_score += 0.30
        elif is_area:
            # Partial: area chart but wrong grouping
            print(f"PARTIAL: Component 2 — AreaChart found but grouping='{grouping}', expected 'stacked' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Chart type is '{chart.tagname}', expected 'areaChart', grouping='{grouping}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chart has exactly 3 series referencing columns B, C, D (0.25 points)
    try:
        series_count = len(chart.series)
        if series_count == 3:
            # Check that series reference the correct columns (B1, C1, D1)
            expected_refs = {"'Trends'!B1", "'Trends'!C1", "'Trends'!D1"}
            actual_refs = set()
            for s in chart.series:
                if s.title and hasattr(s.title, 'strRef') and s.title.strRef:
                    actual_refs.add(s.title.strRef.f)

            if expected_refs == actual_refs:
                print(f"PASS: Component 3 — 3 series with correct column references {actual_refs} (0.25 pts)")
                total_score += 0.25
            elif len(actual_refs) == 3:
                # 3 series but different references — still partial credit
                print(f"PARTIAL: Component 3 — 3 series found but refs={actual_refs}, expected {expected_refs} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"PARTIAL: Component 3 — 3 series but could not verify refs (0.10 pts)")
                total_score += 0.10
        elif series_count > 0:
            print(f"FAIL: Component 3 — Found {series_count} series, expected 3")
        else:
            print(f"FAIL: Component 3 — No series found in chart")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Legend is present and positioned at bottom 'b' (0.20 points)
    try:
        legend = chart.legend
        if legend is not None:
            legend_pos = legend.position
            if legend_pos == 'b':
                print(f"PASS: Component 4 — Legend present at bottom position (0.20 pts)")
                total_score += 0.20
            else:
                # Legend exists but not at bottom — partial credit
                print(f"PARTIAL: Component 4 — Legend present but position='{legend_pos}', expected 'b' (0.10 pts)")
                total_score += 0.10
        else:
            print(f"FAIL: Component 4 — No legend found on chart")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_calc")

file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
