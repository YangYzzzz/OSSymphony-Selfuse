"""
Reward Script: Set print area to A1:G45 and repeating rows 1-2 on 'Invoice' sheet
Task ID: calc_gg1_017
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): Print area is set to exactly A1:G45
  Component 2 (0.5): Rows 1-2 are configured as repeating title rows
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gg1_017'


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

    # Precondition: 'Invoice' sheet must exist
    if 'Invoice' not in wb.sheetnames:
        print("FAIL: 'Invoice' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Invoice']

    # Component 1: Print area is set to exactly A1:G45 (0.5 points)
    try:
        print_area = ws.print_area
        # print_area can be a string like "'Invoice'!$A$1:$G$45" or "$A$1:$G$45" or a list
        # Normalize: extract the cell range portion, strip sheet name prefix, dollar signs
        if print_area:
            # Handle list form
            if isinstance(print_area, list):
                pa_str = print_area[0] if print_area else ''
            else:
                pa_str = str(print_area)

            # Remove sheet name prefix like "'Invoice'!" or "Invoice!"
            pa_clean = re.sub(r"^'?[^'!]+'?!", '', pa_str)
            # Remove dollar signs for comparison
            pa_clean = pa_clean.replace('$', '').strip()

            if pa_clean.upper() == 'A1:G45':
                print(f"PASS: Component 1 — Print area is A1:G45 (raw: {print_area}) (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — Print area is '{pa_clean}', expected 'A1:G45' (raw: {print_area})")
        else:
            print(f"FAIL: Component 1 — No print area is defined (print_area={print_area})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Rows 1-2 set as repeating title rows (0.5 points)
    try:
        title_rows = ws.print_title_rows
        # Expected: '$1:$2' or '1:2'
        if title_rows:
            tr_clean = str(title_rows).replace('$', '').strip()
            if tr_clean == '1:2':
                print(f"PASS: Component 2 — Repeating rows set to 1:2 (raw: {title_rows}) (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 — Repeating rows are '{tr_clean}', expected '1:2' (raw: {title_rows})")
        else:
            print(f"FAIL: Component 2 — No repeating title rows defined (print_title_rows={title_rows})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
