"""
Reward Script: Remove header row from chart data range
Task ID: calc_tbl_063
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): Chart value data range starts at row 2 (excludes header)
  Component 2 (0.4): Chart category range starts at row 2 (excludes header)
  Component 3 (0.2): Chart series has a title/label (from header row)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_tbl_063'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice edits before verification."""
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


def parse_range_start_row(formula_str):
    """
    Extract the start row number from a chart reference formula.
    E.g. "'Sales'!$B$1:$B$13" -> 1
         "'Sales'!$A$2:$A$13" -> 2
    Returns None if cannot parse.
    """
    if not formula_str:
        return None
    # Match patterns like $B$1:$B$13 or $A$2:$A$13
    m = re.search(r'\$[A-Z]+\$(\d+):\$[A-Z]+\$(\d+)', formula_str)
    if m:
        return int(m.group(1))
    # Also handle single cell references like $B$2 (no range)
    m = re.search(r'\$[A-Z]+\$(\d+)', formula_str)
    if m:
        return int(m.group(1))
    return None


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

    # Precondition: chart must exist
    ws = wb.active
    if ws is None:
        print("CRITICAL: No active sheet found")
        print("REWARD: 0.0")
        return 0.0

    charts = ws._charts
    if not charts or len(charts) == 0:
        print("CRITICAL: No charts found on active sheet")
        print("REWARD: 0.0")
        return 0.0

    chart = charts[0]
    if not chart.series or len(chart.series) == 0:
        print("CRITICAL: Chart has no data series")
        print("REWARD: 0.0")
        return 0.0

    series = chart.series[0]

    # Component 1: Chart value data range starts at row 2 (0.4 points)
    # Initial has $B$1:$B$13 (start row 1), golden should have $B$2:$B$13 (start row 2)
    try:
        val_ref_str = None
        if hasattr(series, 'val') and series.val is not None:
            if hasattr(series.val, 'numRef') and series.val.numRef is not None:
                val_ref_str = series.val.numRef.f
            elif hasattr(series.val, 'f'):
                val_ref_str = series.val.f

        if val_ref_str is None:
            print("FAIL: Component 1 -- Could not extract value reference from series")
        else:
            start_row = parse_range_start_row(val_ref_str)
            if start_row is not None and start_row >= 2:
                print(f"PASS: Component 1 -- Value data range starts at row {start_row} (ref: {val_ref_str}) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 -- Value data range starts at row {start_row}, expected >= 2 (ref: {val_ref_str})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Chart category range starts at row 2 (0.4 points)
    # Initial has $A$1:$A$13 (start row 1), golden should have $A$2:$A$13 (start row 2)
    try:
        cat_ref_str = None
        if hasattr(series, 'cat') and series.cat is not None:
            if hasattr(series.cat, 'numRef') and series.cat.numRef is not None:
                cat_ref_str = series.cat.numRef.f
            elif hasattr(series.cat, 'strRef') and series.cat.strRef is not None:
                cat_ref_str = series.cat.strRef.f
            elif hasattr(series.cat, 'f'):
                cat_ref_str = series.cat.f

        if cat_ref_str is None:
            print("FAIL: Component 2 -- Could not extract category reference from series")
        else:
            start_row = parse_range_start_row(cat_ref_str)
            if start_row is not None and start_row >= 2:
                print(f"PASS: Component 2 -- Category range starts at row {start_row} (ref: {cat_ref_str}) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 -- Category range starts at row {start_row}, expected >= 2 (ref: {cat_ref_str})")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Chart series has a title/label (0.2 points)
    # Initial has title=None, golden has title referencing B1 header cell
    # This verifies the header row is used as label, not as data
    try:
        # Check if series title is a non-empty string, or a SeriesLabel with strRef/v
        title_obj = series.title
        title_is_valid = (
            (isinstance(title_obj, str) and len(title_obj.strip()) > 0)
            or (title_obj is not None and hasattr(title_obj, 'strRef') and title_obj.strRef is not None)
            or (title_obj is not None and hasattr(title_obj, 'v') and title_obj.v is not None)
        )
        if title_is_valid:
            print(f"PASS: Component 3 -- Series has a title/label ({title_obj}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- Series has no title/label (title={title_obj})")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

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
