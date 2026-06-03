"""
Reward Script: Data validation rule on B2:B26 (text length 5-50)
Task ID: calc_ggf_047
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Validation exists on B2:B26 with type=textLength, operator=between
  Component 2 (0.2): Min=5, Max=50
  Component 3 (0.2): Input message matches expected text
  Component 4 (0.3): Error style is Stop and error message matches expected text
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ggf_047'


def persist_app_state(domain: str):
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

    # Precondition: 'Schedule' sheet must exist
    if 'Schedule' not in wb.sheetnames:
        print("FAIL: 'Schedule' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Schedule']

    # Find a textLength validation covering B2:B26
    dvs = ws.data_validations.dataValidation
    target_dv = None
    for dv in dvs:
        # Check if this validation covers B2:B26
        sqref_str = str(dv.sqref).upper()
        if dv.type == 'textLength' and 'B2:B26' in sqref_str:
            target_dv = dv
            break

    if target_dv is None:
        # Also try if the range is expressed differently but equivalent
        for dv in dvs:
            if dv.type == 'textLength':
                # Check if all cells B2 through B26 are covered
                sqref_str = str(dv.sqref).upper()
                if 'B2' in sqref_str and 'B26' in sqref_str:
                    target_dv = dv
                    break

    # Component 1: Validation exists on B2:B26 with type=textLength, operator=between (0.3 pts)
    try:
        if target_dv is not None and target_dv.operator == 'between':
            print(f"PASS: Component 1 - textLength validation with operator 'between' found on {target_dv.sqref} (0.3 pts)")
            total_score += 0.3
        elif target_dv is not None:
            print(f"FAIL: Component 1 - textLength validation found but operator is '{target_dv.operator}', expected 'between'")
        else:
            print(f"FAIL: Component 1 - No textLength validation found covering B2:B26. Found {len(dvs)} validation(s).")
            for i, dv in enumerate(dvs):
                print(f"  DV {i}: type={dv.type}, sqref={dv.sqref}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Min=5, Max=50 (0.2 pts)
    try:
        if target_dv is not None:
            f1 = str(target_dv.formula1).strip() if target_dv.formula1 is not None else None
            f2 = str(target_dv.formula2).strip() if target_dv.formula2 is not None else None
            if f1 == '5' and f2 == '50':
                print(f"PASS: Component 2 - Min=5, Max=50 (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 - Expected min=5, max=50, found min={f1}, max={f2}")
        else:
            print("FAIL: Component 2 - No target validation found, skipping min/max check")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Input message matches (0.2 pts)
    try:
        if target_dv is not None:
            prompt_text = target_dv.prompt if target_dv.prompt else ''
            show_input = target_dv.showInputMessage
            expected_prompt = 'Enter between 5 and 50 characters.'
            if prompt_text.strip() == expected_prompt and show_input:
                print(f"PASS: Component 3 - Input message correct: '{prompt_text}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 - Expected prompt='{expected_prompt}' (showInput=True), found prompt='{prompt_text}' (showInput={show_input})")
        else:
            print("FAIL: Component 3 - No target validation found, skipping prompt check")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Error style is Stop and error message matches (0.3 pts)
    try:
        if target_dv is not None:
            error_style = target_dv.errorStyle if target_dv.errorStyle else ''
            error_msg = target_dv.error if target_dv.error else ''
            show_error = target_dv.showErrorMessage
            # The expected error message uses an en-dash (U+2013), not a hyphen
            expected_error = 'Text must be 5\u201350 characters long.'
            # Also accept a regular hyphen variant
            expected_error_alt = 'Text must be 5-50 characters long.'

            style_ok = error_style.lower() == 'stop'
            msg_ok = error_msg.strip() in (expected_error, expected_error_alt)
            show_ok = show_error

            if style_ok and msg_ok and show_ok:
                print(f"PASS: Component 4 - Error style='stop', message correct, showError=True (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 4 - style='{error_style}' (expect 'stop'), msg='{error_msg}' (expect '{expected_error}'), showError={show_error}")
        else:
            print("FAIL: Component 4 - No target validation found, skipping error check")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved state from LibreOffice if applicable
persist_app_state('libreoffice_calc')

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
