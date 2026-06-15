"""
Reward Script: Configure error alert on cell C2's data validation
Task ID: calc_nrv_053
Domain: libreoffice_calc
Scoring:
  Component 1 (0.40): errorTitle is 'Invalid Score'
  Component 2 (0.40): error message is 'Please enter a score between 0 and 100.'
  Component 3 (0.20): errorStyle='stop' AND errorTitle set (compound check)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_053'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
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
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb.active

    # Precondition: There must be at least one data validation on the sheet
    dvs = ws.data_validations.dataValidation
    if not dvs or len(dvs) == 0:
        print("FAIL: No data validations found on active sheet")
        print("REWARD: 0.0")
        return 0.0

    # Find the data validation that covers C2
    target_dv = None
    for dv in dvs:
        sqref_str = str(dv.sqref)
        # Check if C2 is within the sqref range
        if 'C2' in sqref_str or 'C2:' in sqref_str or ':C' in sqref_str:
            target_dv = dv
            break

    # If no exact match, try checking all DVs for one that covers C2
    if target_dv is None:
        from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
        for dv in dvs:
            for cell_range in dv.sqref.ranges:
                min_col = cell_range.min_col
                max_col = cell_range.max_col
                min_row = cell_range.min_row
                max_row = cell_range.max_row
                # C2 = column 3, row 2
                if min_col <= 3 <= max_col and min_row <= 2 <= max_row:
                    target_dv = dv
                    break
            if target_dv is not None:
                break

    if target_dv is None:
        print("FAIL: No data validation covering cell C2 found")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found data validation on sqref={target_dv.sqref}, type={target_dv.type}")

    # Component 1: errorTitle is 'Invalid Score' (0.40 points)
    # Initial has errorTitle=None, golden has errorTitle='Invalid Score'
    # NOTE: errorStyle='stop' is the default and normalizes on save, so we don't
    # score it independently. We verify it as part of compound checks instead.
    try:
        error_title = target_dv.errorTitle
        if error_title is not None and str(error_title).strip() == 'Invalid Score':
            print(f"PASS: Component 1 - errorTitle is 'Invalid Score' (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 - Expected errorTitle='Invalid Score', found: {repr(error_title)}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: error message is 'Please enter a score between 0 and 100.' (0.40 points)
    # Initial has error=None, golden has the custom message
    try:
        error_msg = target_dv.error
        expected_msg = 'Please enter a score between 0 and 100.'
        if error_msg is not None and str(error_msg).strip() == expected_msg:
            print(f"PASS: Component 2 - error message matches (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 2 - Expected error='{expected_msg}', found: {repr(error_msg)}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: errorStyle is 'stop' AND errorTitle is set (compound check) (0.20 points)
    # This verifies the complete error alert configuration is correct.
    # errorStyle='stop' alone normalizes on save, so we require it WITH a custom title.
    try:
        error_style = target_dv.errorStyle
        error_title = target_dv.errorTitle
        if (error_style is not None and str(error_style).lower() == 'stop'
                and error_title is not None and str(error_title).strip() == 'Invalid Score'):
            print(f"PASS: Component 3 - errorStyle='stop' with correct title (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 - Expected errorStyle='stop' with title='Invalid Score', found style={repr(error_style)}, title={repr(error_title)}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
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
