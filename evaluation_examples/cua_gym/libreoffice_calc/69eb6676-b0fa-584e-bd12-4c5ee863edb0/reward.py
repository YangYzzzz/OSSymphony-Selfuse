"""
Reward Script: Data validation on E2:E25 for dates in 2026
Task ID: calc_gcv_059
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): Data validation exists with type=date on E2:E25
  Component 2 (0.25): Date range between 2026-01-01 and 2026-12-31
  Component 3 (0.25): Input message title='Date Entry' and prompt text
  Component 4 (0.25): Error alert style=warning, title='Date Out of Range'
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_059'


def persist_app_state(domain):
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
    Verify data validation setup on E2:E25 with progressive scoring.
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

    # Find the relevant data validation (if any) that covers E2:E25
    dvs = ws.data_validations.dataValidation
    target_dv = None
    for dv in dvs:
        sqref_str = str(dv.sqref).upper()
        # Check if validation covers E2:E25
        if 'E2:E25' in sqref_str or 'E2' in sqref_str:
            target_dv = dv
            break

    if target_dv is None:
        print(f"FAIL: No data validation found covering E2:E25 (found {len(dvs)} validations)")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Data validation exists with type=date on E2:E25 (0.25 points)
    try:
        dv_type = target_dv.type
        sqref_str = str(target_dv.sqref).upper()
        if dv_type == 'date' and 'E2:E25' in sqref_str:
            print(f"PASS: Component 1 - Data validation type=date on E2:E25 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - Expected type=date on E2:E25, got type={dv_type} on {sqref_str}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Date range between 2026-01-01 and 2026-12-31 (0.25 points)
    try:
        formula1 = str(target_dv.formula1) if target_dv.formula1 is not None else ''
        formula2 = str(target_dv.formula2) if target_dv.formula2 is not None else ''
        operator = target_dv.operator

        # Check operator is 'between' and dates match
        f1_ok = '2026-01-01' in formula1 or '2026-1-1' in formula1
        f2_ok = '2026-12-31' in formula2
        op_ok = operator == 'between'

        if f1_ok and f2_ok and op_ok:
            print(f"PASS: Component 2 - Date range 2026-01-01 to 2026-12-31 with operator=between (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - formula1={formula1}, formula2={formula2}, operator={operator}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Input message title='Date Entry' and prompt text (0.25 points)
    try:
        prompt_title = target_dv.promptTitle or ''
        prompt_msg = target_dv.prompt or ''
        show_input = target_dv.showInputMessage

        title_ok = prompt_title.strip() == 'Date Entry'
        msg_ok = 'date within the year 2026' in prompt_msg.lower() or 'enter a date' in prompt_msg.lower()

        if title_ok and msg_ok:
            print(f"PASS: Component 3 - Input message title='Date Entry', prompt present (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - promptTitle='{prompt_title}', prompt='{prompt_msg}', showInputMessage={show_input}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Error alert style=warning, title='Date Out of Range' (0.25 points)
    try:
        error_style = target_dv.errorStyle or ''
        error_title = target_dv.errorTitle or ''
        show_error = target_dv.showErrorMessage

        style_ok = error_style.lower() == 'warning'
        title_ok = error_title.strip() == 'Date Out of Range'

        if style_ok and title_ok:
            print(f"PASS: Component 4 - Error style=warning, title='Date Out of Range' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 - errorStyle='{error_style}', errorTitle='{error_title}', showErrorMessage={show_error}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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
