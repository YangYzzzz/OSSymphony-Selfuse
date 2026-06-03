"""
Reward Script: Update SUM formula range to include all data rows after row insertion
Task ID: calc_tbl_057
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5 pts): B56 formula references an end row beyond B50 (range was extended)
  Component 2 (0.5 pts): B56 formula is exactly =SUM(B2:B55) (precise correct formula)
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_tbl_057'


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


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: After inserting 5 new rows in the middle of a data table, the totaling
    formula at the bottom still references the old range and misses the new rows.
    Update the formula range to include all rows.

    Initial state: B56 has =SUM(B2:B50) — misses rows 51-55
    Golden state:  B56 has =SUM(B2:B55) — includes all data rows
    """
    total_score = 0.0

    # Load workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb.active

    # Get the formula in B56
    b56_value = ws['B56'].value
    print(f"INFO: B56 raw value = {b56_value}")

    # Parse the SUM formula to extract the range
    formula_match = None
    end_row = None
    start_row = None
    if isinstance(b56_value, str):
        # Match patterns like =SUM(B2:B55), =sum(b2:b55), etc.
        formula_match = re.match(
            r'^=\s*SUM\s*\(\s*B(\d+)\s*:\s*B(\d+)\s*\)\s*$',
            b56_value.strip(),
            re.IGNORECASE
        )
        if formula_match:
            start_row = int(formula_match.group(1))
            end_row = int(formula_match.group(2))
            print(f"INFO: Parsed SUM range — start_row={start_row}, end_row={end_row}")

    # Component 1: B56 formula references an end row beyond B50 (0.5 points)
    # The old broken formula ends at B50. The fix must extend beyond that.
    # This FAILS on initial (end_row=50, not >50), PASSES on golden (end_row=55).
    try:
        if formula_match and end_row is not None and end_row > 50:
            print(f"PASS: Component 1 — SUM formula end row ({end_row}) is beyond B50 (0.5 pts)")
            total_score += 0.5
        else:
            if formula_match:
                print(f"FAIL: Component 1 — SUM formula end row ({end_row}) is not beyond B50")
            else:
                print(f"FAIL: Component 1 — B56 does not contain a valid SUM(Bn:Bm) formula, found: {b56_value}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: B56 formula is exactly =SUM(B2:B55) (0.5 points)
    # The precise correct formula covers B2 through B55 (all 54 data rows).
    # This FAILS on initial (=SUM(B2:B50)), PASSES on golden (=SUM(B2:B55)).
    try:
        if formula_match and start_row == 2 and end_row == 55:
            print(f"PASS: Component 2 — B56 formula is exactly =SUM(B2:B55) (0.5 pts)")
            total_score += 0.5
        else:
            if formula_match:
                print(f"FAIL: Component 2 — Expected =SUM(B2:B55), got =SUM(B{start_row}:B{end_row})")
            else:
                print(f"FAIL: Component 2 — B56 is not a valid SUM formula, found: {b56_value}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification (LibreOffice may have unsaved edits)
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
