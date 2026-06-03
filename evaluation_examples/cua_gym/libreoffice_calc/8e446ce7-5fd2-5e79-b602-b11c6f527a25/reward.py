"""
Reward Script: Add text length validation to Description column (C2:C50)
Task ID: calc_dop_validate_textlen_072
Domain: libreoffice_calc
Scoring:
  Component 1 (0.35): textLength data validation exists on C2:C50
  Component 2 (0.25): Operator is 'between' with formula1=10 and formula2=150
  Component 3 (0.20): Error style is 'warning' (not 'stop' or 'information')
  Component 4 (0.20): Error/input messages match required text
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_dop_validate_textlen_072'


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

    # Precondition gate: 'ProductCatalog' sheet must exist
    if 'ProductCatalog' not in wb.sheetnames:
        print("FAIL: Sheet 'ProductCatalog' not found in workbook")
        print(f"Score: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['ProductCatalog']
    validations = ws.data_validations.dataValidation

    # Component 1: textLength data validation exists on C2:C50 (0.35 points)
    # This FAILS on initial (no DV at all) → PASSES on golden
    try:
        textlen_dv = None
        for dv in validations:
            if dv.type == 'textLength':
                # Check that the validation covers C2:C50 (or a superset range)
                sqref_str = str(dv.sqref)
                if 'C2:C50' in sqref_str or sqref_str.strip() == 'C2:C50':
                    textlen_dv = dv
                    break
        if textlen_dv is not None:
            print(f"PASS: Component 1 — textLength validation found on C2:C50 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — no textLength validation found on C2:C50 (found {len(validations)} validations total)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        textlen_dv = None

    # All subsequent components depend on finding the textLength DV
    if textlen_dv is None:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Operator is 'between' with min=10 and max=150 (0.25 points)
    # This FAILS on initial → PASSES on golden
    try:
        operator_ok = (textlen_dv.operator == 'between' or textlen_dv.operator is None)
        # When operator is 'between', openpyxl may omit it (None means between by default)
        try:
            f1 = int(textlen_dv.formula1)
            f2 = int(textlen_dv.formula2)
        except (TypeError, ValueError):
            f1, f2 = None, None

        if f1 == 10 and f2 == 150:
            print(f"PASS: Component 2 — operator=between, min=10, max=150 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected min=10, max=150 but got formula1={textlen_dv.formula1}, formula2={textlen_dv.formula2}, operator={textlen_dv.operator}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error style is 'warning' (0.20 points)
    # This FAILS on initial → PASSES on golden
    try:
        error_style = textlen_dv.errorStyle
        if error_style is not None and str(error_style).lower() == 'warning':
            print(f"PASS: Component 3 — errorStyle='warning' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — expected errorStyle='warning' but got '{error_style}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Error and input messages match required text (0.20 points)
    # This FAILS on initial → PASSES on golden
    try:
        expected_error_title = 'Description Length'
        expected_error_msg = 'Description should be between 10 and 150 characters'
        expected_prompt_title = 'Description'
        expected_prompt_msg = 'Enter a product description (10-150 characters)'

        et_ok = (textlen_dv.errorTitle is not None and
                 textlen_dv.errorTitle.strip() == expected_error_title)
        em_ok = (textlen_dv.error is not None and
                 textlen_dv.error.strip() == expected_error_msg)
        pt_ok = (textlen_dv.promptTitle is not None and
                 textlen_dv.promptTitle.strip() == expected_prompt_title)
        pm_ok = (textlen_dv.prompt is not None and
                 textlen_dv.prompt.strip() == expected_prompt_msg)

        all_messages_ok = et_ok and em_ok and pt_ok and pm_ok

        if all_messages_ok:
            print(f"PASS: Component 4 — all error/input messages match required text (0.20 pts)")
            total_score += 0.20
        else:
            details = []
            if not et_ok:
                details.append(f"errorTitle: expected '{expected_error_title}', got '{textlen_dv.errorTitle}'")
            if not em_ok:
                details.append(f"error: expected '{expected_error_msg}', got '{textlen_dv.error}'")
            if not pt_ok:
                details.append(f"promptTitle: expected '{expected_prompt_title}', got '{textlen_dv.promptTitle}'")
            if not pm_ok:
                details.append(f"prompt: expected '{expected_prompt_msg}', got '{textlen_dv.prompt}'")
            print(f"FAIL: Component 4 — message mismatches: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
