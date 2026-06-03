"""
Reward Script: Data validation on D2 for Q1 dates
Task ID: calc_nrv_082
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): Data validation exists targeting D2
  Component 2 (0.35): Validation is custom type with formula referencing MONTH and YEAR
  Component 3 (0.20): Formula enforces month range 1-3 (Q1 check)
  Component 4 (0.20): Error message is configured (showErrorMessage=True)
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_082'


def persist_app_state(domain: str):
    """Best-effort save of any open LibreOffice document."""
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


def find_dv_for_d2(validations):
    """Find a DataValidation rule that covers cell D2."""
    from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
    for dv in validations:
        sqref_str = str(dv.sqref)
        # sqref can be like "D2" or "D2:D100" or "D2 E3" etc.
        for part in sqref_str.split():
            if ':' in part:
                # Range like D2:D100
                start, end = part.split(':')
                s_col_letter, s_row = coordinate_from_string(start)
                e_col_letter, e_row = coordinate_from_string(end)
                s_col = column_index_from_string(s_col_letter)
                e_col = column_index_from_string(e_col_letter)
                # D=4, row 2
                if s_col <= 4 <= e_col and s_row <= 2 <= e_row:
                    return dv
            else:
                # Single cell like D2
                if part.upper() == 'D2':
                    return dv
    return None


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

    # Component 1: Data validation exists targeting D2 (0.25 points)
    dv_d2 = None
    try:
        dvs = ws.data_validations.dataValidation
        dv_d2 = find_dv_for_d2(dvs)
        if dv_d2 is not None:
            print(f"PASS: Component 1 -- Data validation found covering D2, sqref={dv_d2.sqref} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- No data validation found covering cell D2 (found {len(dvs)} validations total)")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if dv_d2 is None:
        # No validation at all, remaining checks cannot pass
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Validation is custom type with formula referencing MONTH and YEAR (0.35 points)
    try:
        formula = str(dv_d2.formula1 or '').upper()
        vtype = str(dv_d2.type or '').lower()
        has_custom_type = vtype == 'custom'
        has_month_ref = 'MONTH' in formula
        has_year_ref = 'YEAR' in formula

        if has_custom_type and has_month_ref and has_year_ref:
            print(f"PASS: Component 2 -- Custom validation with MONTH+YEAR formula: {dv_d2.formula1} (0.35 pts)")
            total_score += 0.35
        else:
            reasons = []
            if not has_custom_type:
                reasons.append(f"type is '{vtype}' not 'custom'")
            if not has_month_ref:
                reasons.append("formula missing MONTH reference")
            if not has_year_ref:
                reasons.append("formula missing YEAR reference")
            print(f"FAIL: Component 2 -- {'; '.join(reasons)}. formula1={dv_d2.formula1!r}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Formula enforces month range 1-3 for Q1 (0.20 points)
    try:
        formula = str(dv_d2.formula1 or '').upper().replace(' ', '')
        # Check that the formula constrains MONTH to be between 1 and 3
        # Common patterns: MONTH(D2)>=1,MONTH(D2)<=3 or MONTH(D2)<=3,MONTH(D2)>=1
        has_lower_bound = bool(re.search(r'MONTH\([^)]+\)\s*>=?\s*1', formula))
        has_upper_bound = bool(re.search(r'MONTH\([^)]+\)\s*<=?\s*3', formula))

        if has_lower_bound and has_upper_bound:
            print(f"PASS: Component 3 -- Formula checks month in range 1-3 (Q1) (0.20 pts)")
            total_score += 0.20
        else:
            reasons = []
            if not has_lower_bound:
                reasons.append("no MONTH>=1 check found")
            if not has_upper_bound:
                reasons.append("no MONTH<=3 check found")
            print(f"FAIL: Component 3 -- {'; '.join(reasons)}. formula={formula}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Error message is configured (showErrorMessage=True) (0.20 points)
    try:
        show_error = dv_d2.showErrorMessage
        has_error_text = bool(dv_d2.error and len(str(dv_d2.error).strip()) > 0)

        if show_error and has_error_text:
            print(f"PASS: Component 4 -- Error messaging enabled, error='{dv_d2.error}' (0.20 pts)")
            total_score += 0.20
        else:
            reasons = []
            if not show_error:
                reasons.append("showErrorMessage is not True")
            if not has_error_text:
                reasons.append("no error message text set")
            print(f"FAIL: Component 4 -- {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI state before verification
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
