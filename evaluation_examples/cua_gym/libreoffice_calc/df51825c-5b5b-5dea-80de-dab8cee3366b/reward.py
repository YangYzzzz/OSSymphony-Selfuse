"""
Reward Script: Remove validation from D10:D15 and apply custom validation allowing positive numbers or empty cells.
Task ID: calc_nrv_088
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30): Validation type is 'custom' (not 'whole')
  Component 2 (0.30): Validation formula is =OR(D10="",D10>0)
  Component 3 (0.15): allow_blank is True
  Component 4 (0.15): Validation range covers D10:D15
  Component 5 (0.10): Error message updated for new validation
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_088'


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

    # Use the 'Inventory' sheet (active sheet)
    ws = wb['Inventory']

    # Get data validations
    dvs = ws.data_validations.dataValidation
    if len(dvs) == 0:
        print("FAIL: No data validations found at all")
        print("REWARD: 0.0")
        return 0.0

    # Find validation that covers D10:D15
    target_dv = None
    for dv in dvs:
        sqref_str = str(dv.sqref).upper()
        # Check if D10:D15 is covered by this validation
        if 'D10' in sqref_str and 'D15' in sqref_str:
            target_dv = dv
            break

    if target_dv is None:
        # Also check if individual cells are covered
        for dv in dvs:
            sqref_str = str(dv.sqref).upper()
            # Check for the full range or individual cells
            if 'D10:D15' in sqref_str.replace(' ', ''):
                target_dv = dv
                break

    if target_dv is None:
        print("FAIL: No data validation found covering D10:D15 range")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found validation on range: {target_dv.sqref}")
    print(f"INFO: type={target_dv.type}, formula1={target_dv.formula1}, allow_blank={target_dv.allow_blank}, operator={target_dv.operator}")

    # Component 1: Validation type is 'custom' (not 'whole') — 0.30 points
    # Initial has type='whole', golden has type='custom'
    try:
        if target_dv.type == 'custom':
            print(f"PASS: Component 1 — Validation type is 'custom' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Expected type='custom', found type='{target_dv.type}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Validation formula matches =OR(D10="",D10>0) — 0.30 points
    # Initial has formula1='1' (whole number between 1-1000), golden has =OR(D10="",D10>0)
    try:
        formula = str(target_dv.formula1).strip() if target_dv.formula1 else ''
        # Normalize for comparison: remove spaces, uppercase
        formula_norm = formula.upper().replace(' ', '')
        expected_norm = '=OR(D10="",D10>0)'.upper().replace(' ', '')

        if formula_norm == expected_norm:
            print(f"PASS: Component 2 — Formula matches '=OR(D10=\"\",D10>0)' (0.30 pts)")
            total_score += 0.30
        else:
            # Also accept slight variations like =OR(D10="",D10>0) with different quoting
            # Check for the core OR pattern with empty string and >0
            alt_expected = '=OR(D10="",D10>0)'.upper().replace(' ', '')
            if formula_norm == alt_expected:
                print(f"PASS: Component 2 — Formula matches expected pattern (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — Expected formula '=OR(D10=\"\",D10>0)', found '{formula}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: allow_blank is True — 0.15 points
    # Initial has allow_blank=False, golden has allow_blank=True
    try:
        if target_dv.allow_blank is True:
            print(f"PASS: Component 3 — allow_blank is True (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Expected allow_blank=True, found {target_dv.allow_blank}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Validation range still covers D10:D15 — 0.15 points
    # Both initial and golden should have this range, but if validation was removed
    # without re-applying, this would fail. This is a compound check: the validation
    # must be custom AND cover the correct range.
    try:
        sqref_str = str(target_dv.sqref).upper().replace(' ', '')
        # We already found the dv covering D10:D15, but verify it's the custom type + correct range
        if target_dv.type == 'custom' and ('D10:D15' in sqref_str or 'D10:D15' in sqref_str):
            print(f"PASS: Component 4 — Custom validation covers D10:D15 range (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Custom validation + D10:D15 range not confirmed (type={target_dv.type}, range={target_dv.sqref})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Error message updated for new validation — 0.10 points
    # Initial has error='Please enter a whole number between 1 and 1000.'
    # Golden has error='Please enter a positive number or leave the cell empty.'
    # The key change indicator: error message should NOT reference "whole number" or "1 and 1000"
    # AND should reference "positive" or "empty" concepts
    try:
        error_msg = str(target_dv.error).lower() if target_dv.error else ''
        # Check that the old validation message is gone
        old_msg_gone = 'whole number' not in error_msg and '1 and 1000' not in error_msg
        # Check that the new validation has some relevant error messaging
        # (not the exact text, but should not be the old "whole number between 1 and 1000" message)
        if old_msg_gone and target_dv.type == 'custom':
            print(f"PASS: Component 5 — Error message updated (no longer references old whole-number constraint) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Error message not properly updated: '{target_dv.error}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
