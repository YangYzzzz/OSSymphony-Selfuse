"""
Reward Script: Data validation on G2:G51 for dates in 2024 with information alert
Task ID: calc_gg3_043
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): Date-type validation exists targeting G2:G51
  Component 2 (0.30): Operator 'between' with dates 2024-01-01 to 2024-12-31
  Component 3 (0.20): Error style is 'information'
  Component 4 (0.25): Alert title 'Date Range' and message 'Please enter a date in 2024.'
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gg3_043'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
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

    # Precondition: 'Schedule' sheet must exist
    if 'Schedule' not in wb.sheetnames:
        print("FAIL: 'Schedule' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Schedule']

    # Find the date validation targeting G2:G51
    dvs = ws.data_validations.dataValidation
    target_dv = None
    for dv in dvs:
        # Check if this validation covers G2:G51 (exact match or superset)
        sqref_str = str(dv.sqref).replace(' ', '')
        if 'G2:G51' in sqref_str or sqref_str == 'G2:G51':
            target_dv = dv
            break

    # Component 1: Date-type validation exists targeting G2:G51 (0.25 points)
    try:
        if target_dv is not None and target_dv.type == 'date':
            print(f"PASS: Component 1 — Date validation found on {target_dv.sqref}, type={target_dv.type} (0.25 pts)")
            total_score += 0.25
        elif target_dv is not None:
            print(f"FAIL: Component 1 — Validation found on {target_dv.sqref} but type is '{target_dv.type}', expected 'date'")
        else:
            # Try broader search - maybe range is slightly different
            date_dvs = [dv for dv in dvs if dv.type == 'date']
            if date_dvs:
                print(f"FAIL: Component 1 — Date validation found but on range '{date_dvs[0].sqref}', expected 'G2:G51'")
            else:
                print(f"FAIL: Component 1 — No date validation found on G2:G51 (total validations: {len(dvs)})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Operator 'between' with correct date range (0.30 points)
    try:
        if target_dv is not None and target_dv.type == 'date':
            operator_ok = (target_dv.operator == 'between')
            # Check date formulas - openpyxl may represent them as strings
            f1 = str(target_dv.formula1).strip() if target_dv.formula1 else ''
            f2 = str(target_dv.formula2).strip() if target_dv.formula2 else ''

            # Normalize date representations: could be '2024-01-01' or '45292' (serial) etc.
            date_start_ok = ('2024-01-01' in f1 or '2024-1-1' in f1)
            date_end_ok = ('2024-12-31' in f2)

            if operator_ok and date_start_ok and date_end_ok:
                print(f"PASS: Component 2 — operator='{target_dv.operator}', range {f1} to {f2} (0.30 pts)")
                total_score += 0.30
            else:
                issues = []
                if not operator_ok:
                    issues.append(f"operator='{target_dv.operator}' (expected 'between')")
                if not date_start_ok:
                    issues.append(f"formula1='{f1}' (expected contains '2024-01-01')")
                if not date_end_ok:
                    issues.append(f"formula2='{f2}' (expected contains '2024-12-31')")
                print(f"FAIL: Component 2 — {'; '.join(issues)}")
        else:
            print("FAIL: Component 2 — No valid date validation to check operator/range")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error style is 'information' (0.20 points)
    try:
        if target_dv is not None:
            style = target_dv.errorStyle
            if style == 'information':
                print(f"PASS: Component 3 — errorStyle='{style}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — errorStyle='{style}', expected 'information'")
        else:
            print("FAIL: Component 3 — No validation found to check error style")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Alert title 'Date Range' and message 'Please enter a date in 2024.' (0.25 points)
    try:
        if target_dv is not None:
            title = target_dv.errorTitle
            message = target_dv.error
            title_ok = (title is not None and str(title).strip() == 'Date Range')
            message_ok = (message is not None and str(message).strip() == 'Please enter a date in 2024.')

            if title_ok and message_ok:
                print(f"PASS: Component 4 — errorTitle='{title}', error='{message}' (0.25 pts)")
                total_score += 0.25
            else:
                issues = []
                if not title_ok:
                    issues.append(f"errorTitle='{title}' (expected 'Date Range')")
                if not message_ok:
                    issues.append(f"error='{message}' (expected 'Please enter a date in 2024.')")
                print(f"FAIL: Component 4 — {'; '.join(issues)}")
        else:
            print("FAIL: Component 4 — No validation found to check alert text")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state("libreoffice_calc")
    verify_task(file_path)
