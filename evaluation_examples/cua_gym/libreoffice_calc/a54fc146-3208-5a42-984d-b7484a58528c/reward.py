"""
Reward Script: Data validation on D2:D31 for dates between 2024-01-01 and 2025-12-31
Task ID: calc_ggf_020
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Date-type data validation exists covering D2:D31
  Component 2 (0.3): Date range is 2024-01-01 to 2025-12-31
  Component 3 (0.2): Input message matches expected text
  Component 4 (0.2): Error alert style is 'warning'
"""

import os
import datetime

import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ggf_020'


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


def verify_task(file_path):
    """
    Verify data validation on D2:D31 in the 'Projects' sheet.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check 'Projects' sheet exists
    if 'Projects' not in wb.sheetnames:
        print("CRITICAL: 'Projects' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Projects']
    validations = ws.data_validations.dataValidation

    # Find the date validation covering D2:D31
    target_dv = None
    for dv in validations:
        # Check if this validation covers D2:D31 (or a superset)
        sqref_str = str(dv.sqref).upper()
        if dv.type == 'date' and 'D2' in sqref_str:
            target_dv = dv
            break

    # Component 1: Date-type data validation exists covering D2:D31 (0.3 points)
    try:
        if target_dv is not None:
            sqref_str = str(target_dv.sqref).upper()
            # Check that it covers D2:D31
            if 'D2:D31' in sqref_str or 'D2:D31' == sqref_str:
                print(f"PASS: Component 1 - Date validation exists on {target_dv.sqref} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 - Date validation exists but covers {target_dv.sqref}, not D2:D31")
        else:
            print(f"FAIL: Component 1 - No date-type data validation found covering D2:D31")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Date range is 2024-01-01 to 2025-12-31 (0.3 points)
    try:
        if target_dv is not None:
            f1 = str(target_dv.formula1).strip()
            f2 = str(target_dv.formula2).strip()

            # Normalize date representations - could be date objects or strings
            min_ok = False
            max_ok = False

            # Check minimum date (2024-01-01)
            min_variants = ['2024-01-01', '2024-1-1', '01/01/2024', '1/1/2024']
            if any(v in f1 for v in min_variants):
                min_ok = True
            elif hasattr(target_dv.formula1, 'year'):
                # It's a date object
                dt = target_dv.formula1
                if dt.year == 2024 and dt.month == 1 and dt.day == 1:
                    min_ok = True

            # Check maximum date (2025-12-31)
            max_variants = ['2025-12-31', '31/12/2025', '12/31/2025']
            if any(v in f2 for v in max_variants):
                max_ok = True
            elif hasattr(target_dv.formula2, 'year'):
                dt = target_dv.formula2
                if dt.year == 2025 and dt.month == 12 and dt.day == 31:
                    max_ok = True

            if min_ok and max_ok:
                print(f"PASS: Component 2 - Date range {f1} to {f2} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 - Date range: formula1={f1} (min_ok={min_ok}), formula2={f2} (max_ok={max_ok})")
        else:
            print(f"FAIL: Component 2 - No target validation to check date range")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Input message matches expected text (0.2 points)
    try:
        if target_dv is not None:
            expected_prompt = "Enter a project date between Jan 2024 and Dec 2025."
            actual_prompt = str(target_dv.prompt).strip() if target_dv.prompt else ""
            show_input = target_dv.showInputMessage

            if actual_prompt == expected_prompt and show_input:
                print(f"PASS: Component 3 - Input message correct: '{actual_prompt}' (0.2 pts)")
                total_score += 0.2
            elif expected_prompt.lower() in actual_prompt.lower() or actual_prompt.lower() in expected_prompt.lower():
                # Partial credit for close match
                print(f"PARTIAL: Component 3 - Input message close: '{actual_prompt}' (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3 - Expected prompt: '{expected_prompt}', found: '{actual_prompt}', showInputMessage={show_input}")
        else:
            print(f"FAIL: Component 3 - No target validation to check input message")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Error alert style is 'warning' (0.2 points)
    try:
        if target_dv is not None:
            error_style = str(target_dv.errorStyle).strip().lower() if target_dv.errorStyle else ""
            show_error = target_dv.showErrorMessage

            if error_style == 'warning' and show_error:
                print(f"PASS: Component 4 - Error style is 'warning' with showErrorMessage=True (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 - Expected errorStyle='warning' with showErrorMessage=True, found errorStyle='{error_style}', showErrorMessage={show_error}")
        else:
            print(f"FAIL: Component 4 - No target validation to check error style")
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
