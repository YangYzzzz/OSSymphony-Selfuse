"""
Reward Script: Print scaling and repeating header row
Task ID: calc_tbl_047
Domain: libreoffice_calc
Scoring:
  Component 1 (0.35): fitToPage enabled
  Component 2 (0.30): fitToWidth == 1 and fitToHeight == 0 (fit columns on one page, unlimited rows)
  Component 3 (0.35): Row 1 set as repeating print title row
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_tbl_047'


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

    ws = wb.active

    # Component 1: fitToPage is enabled (0.35 points)
    # In initial_env this is None/False; in golden_env it should be True
    try:
        fit_to_page = False
        if ws.sheet_properties.pageSetUpPr is not None:
            fit_to_page = bool(ws.sheet_properties.pageSetUpPr.fitToPage)

        if fit_to_page:
            print(f"PASS: Component 1 — fitToPage is enabled (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — fitToPage is not enabled (value: {fit_to_page})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: fitToWidth == 1 and fitToHeight == 0 (0.30 points)
    # This means "fit all columns on 1 page wide, allow unlimited pages for rows"
    # In initial_env these are None; in golden_env fitToWidth=1 and fitToHeight=0
    try:
        ps = ws.page_setup
        fit_w = ps.fitToWidth
        fit_h = ps.fitToHeight

        width_ok = (fit_w is not None and int(fit_w) == 1)
        # fitToHeight must be 0 (unlimited) to allow multiple pages for rows
        height_ok = (fit_h is not None and int(fit_h) == 0)

        if width_ok and height_ok:
            print(f"PASS: Component 2 — fitToWidth={fit_w}, fitToHeight={fit_h} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — fitToWidth={fit_w} (expect 1), fitToHeight={fit_h} (expect 0)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Row 1 is set as repeating print title row (0.35 points)
    # In initial_env print_title_rows is None; in golden_env it should be '$1:$1'
    try:
        title_rows = ws.print_title_rows

        if title_rows is not None and '1' in str(title_rows):
            # Verify it specifically references row 1
            # Common formats: '$1:$1', '1:1'
            title_str = str(title_rows).replace('$', '').replace(' ', '')
            if '1:1' in title_str:
                print(f"PASS: Component 3 — print_title_rows={title_rows} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 3 — print_title_rows={title_rows} does not match row 1 pattern")
        else:
            print(f"FAIL: Component 3 — print_title_rows is not set (value: {title_rows})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
