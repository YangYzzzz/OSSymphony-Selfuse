"""
Reward Script: Data validation on D2:D30 for Q2 2026 dates
Task ID: calc_gcv_081
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): Data validation exists on D2:D30 with type=date
  Component 2 (0.25): Operator=between with date range 2026-04-01 to 2026-06-30
  Component 3 (0.20): Input message configured correctly
  Component 4 (0.20): Error alert configured with Stop action
  Component 5 (0.10): showInputMessage and showErrorMessage enabled
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_081'


def verify_task(file_path):
    """
    Verify data validation setup with progressive scoring.
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

    # Find the relevant data validation (if any) that applies to column D
    dvs = ws.data_validations.dataValidation
    target_dv = None
    for dv in dvs:
        sqref_str = str(dv.sqref).upper()
        # Check if this validation covers D2:D30 (could be exact or contain it)
        if 'D2' in sqref_str and 'D30' in sqref_str:
            target_dv = dv
            break

    if target_dv is None:
        print("FAIL: No data validation found covering D2:D30")
        print(f"  Found {len(dvs)} validation(s): {[str(d.sqref) for d in dvs]}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 1: Data validation exists on D2:D30 with type=date (0.25 points)
    try:
        dv_type = target_dv.type
        sqref_str = str(target_dv.sqref).upper().replace(' ', '')
        # Check type is date
        if dv_type == 'date':
            # Check range covers D2:D30
            if 'D2:D30' in sqref_str or sqref_str == 'D2:D30':
                print(f"PASS: Component 1 — DV type=date on {target_dv.sqref} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — DV sqref is {target_dv.sqref}, expected D2:D30")
        else:
            print(f"FAIL: Component 1 — DV type is '{dv_type}', expected 'date'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Operator=between, formula1=2026-04-01, formula2=2026-06-30 (0.25 points)
    try:
        operator = target_dv.operator
        f1 = str(target_dv.formula1).strip() if target_dv.formula1 else ''
        f2 = str(target_dv.formula2).strip() if target_dv.formula2 else ''

        operator_ok = (operator == 'between')
        # Accept common date representations
        f1_ok = ('2026-04-01' in f1 or '2026/04/01' in f1 or '46113' in f1)
        f2_ok = ('2026-06-30' in f2 or '2026/06/30' in f2 or '46204' in f2)

        if operator_ok and f1_ok and f2_ok:
            print(f"PASS: Component 2 — operator={operator}, f1={f1}, f2={f2} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — operator={operator} (exp: between), f1={f1} (exp: 2026-04-01), f2={f2} (exp: 2026-06-30)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Input message configured (0.20 points)
    try:
        prompt_title = str(target_dv.promptTitle).strip() if target_dv.promptTitle else ''
        prompt_msg = str(target_dv.prompt).strip() if target_dv.prompt else ''

        title_ok = ('q2' in prompt_title.lower() and 'date' in prompt_title.lower())
        msg_ok = ('april' in prompt_msg.lower() and 'june' in prompt_msg.lower() and '2026' in prompt_msg)

        if title_ok and msg_ok:
            print(f"PASS: Component 3 — promptTitle='{prompt_title}', prompt='{prompt_msg}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — promptTitle='{prompt_title}' (exp contains 'Q2'+'Date'), prompt='{prompt_msg}' (exp mentions April, June, 2026)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Error alert with Stop action and title 'Out of Q2 Range' (0.20 points)
    try:
        error_style = str(target_dv.errorStyle).strip().lower() if target_dv.errorStyle else ''
        error_title = str(target_dv.errorTitle).strip() if target_dv.errorTitle else ''

        style_ok = (error_style == 'stop')
        title_ok = ('q2' in error_title.lower() and 'range' in error_title.lower())

        if style_ok and title_ok:
            print(f"PASS: Component 4 — errorStyle='{error_style}', errorTitle='{error_title}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — errorStyle='{error_style}' (exp: stop), errorTitle='{error_title}' (exp contains 'Q2'+'Range')")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: showInputMessage=True and showErrorMessage=True (0.10 points)
    try:
        show_input = target_dv.showInputMessage
        show_error = target_dv.showErrorMessage

        if show_input and show_error:
            print(f"PASS: Component 5 — showInputMessage={show_input}, showErrorMessage={show_error} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — showInputMessage={show_input}, showErrorMessage={show_error} (both should be True)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
