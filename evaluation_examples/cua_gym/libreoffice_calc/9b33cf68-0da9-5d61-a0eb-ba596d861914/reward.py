"""
Reward Script: Dropdown list validation with dependent cascading dropdowns
Task ID: calc_gcv_063
Domain: libreoffice_calc
Scoring:
  Component 1 (0.35): B2:B30 has a list data validation with Q1,Q2,Q3,Q4
  Component 2 (0.35): C2:C30 has a list data validation using INDIRECT formula
  Component 3 (0.15): The B-column validation covers the correct range (B2:B30)
  Component 4 (0.15): The C-column validation covers the correct range (C2:C30)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_063'

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

    # Find the main sheet (Quarterly_Report or first sheet)
    ws = None
    for name in ['Quarterly_Report', 'Sheet1']:
        if name in wb.sheetnames:
            ws = wb[name]
            break
    if ws is None:
        ws = wb.worksheets[0]
    print(f"Using sheet: {ws.title}")

    # Get all data validations
    validations = ws.data_validations.dataValidation
    print(f"Found {len(validations)} data validation(s)")

    if len(validations) == 0:
        print("FAIL: No data validations found — task not started")
        print("REWARD: 0.0")
        return 0.0

    # Categorize validations: find the quarter dropdown (B column) and month dropdown (C column)
    quarter_dv = None
    month_dv = None

    for dv in validations:
        sqref_str = str(dv.sqref).upper()
        formula1_str = str(dv.formula1) if dv.formula1 else ""

        # Identify quarter validation: list type with Q1-Q4 values, applied to B column
        if dv.type == "list":
            # Check if it references B column cells
            has_b_col = any('B' in part.split(':')[0] for part in sqref_str.replace(' ', ',').split(','))
            # Check if it references C column cells
            has_c_col = any('C' in part.split(':')[0] for part in sqref_str.replace(' ', ',').split(','))

            # Quarter validation: contains Q1,Q2,Q3,Q4 in some form
            formula_upper = formula1_str.upper().replace(' ', '')
            has_quarter_values = all(q in formula_upper for q in ['Q1', 'Q2', 'Q3', 'Q4'])

            # Month/dependent validation: uses INDIRECT
            has_indirect = 'INDIRECT' in formula_upper

            if has_b_col and has_quarter_values:
                quarter_dv = dv
                print(f"  Identified quarter DV: type={dv.type}, formula1={dv.formula1}, sqref={dv.sqref}")
            elif has_c_col and has_indirect:
                month_dv = dv
                print(f"  Identified month DV: type={dv.type}, formula1={dv.formula1}, sqref={dv.sqref}")
            elif has_b_col and has_indirect:
                # Might be swapped
                print(f"  Found DV on B with INDIRECT (unexpected): formula1={dv.formula1}, sqref={dv.sqref}")
            elif has_c_col and has_quarter_values:
                # Might be swapped
                print(f"  Found DV on C with quarter values (unexpected): formula1={dv.formula1}, sqref={dv.sqref}")
            else:
                print(f"  Unclassified DV: type={dv.type}, formula1={dv.formula1}, sqref={dv.sqref}")

    # Component 1: Quarter dropdown validation on B column (0.35 points)
    # This checks that B2:B30 has a list validation with Q1,Q2,Q3,Q4 options
    try:
        if quarter_dv is not None:
            formula_clean = str(quarter_dv.formula1).upper().replace(' ', '')
            # Accept various separators: comma, semicolon
            has_all_quarters = all(q in formula_clean for q in ['Q1', 'Q2', 'Q3', 'Q4'])
            if has_all_quarters:
                print(f"PASS: Component 1 — Quarter dropdown has Q1-Q4 values: {quarter_dv.formula1} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — Quarter dropdown missing some Q values: {quarter_dv.formula1}")
        else:
            print("FAIL: Component 1 — No quarter dropdown validation found on B column")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Dependent month dropdown using INDIRECT on C column (0.35 points)
    # This checks that C2:C30 has a list validation using INDIRECT formula
    try:
        if month_dv is not None:
            formula_str = str(month_dv.formula1).upper().replace(' ', '')
            if 'INDIRECT' in formula_str:
                # INDIRECT formula found — this is the dependent dropdown mechanism
                print(f"PASS: Component 2 — Dependent dropdown uses INDIRECT formula: {month_dv.formula1} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — Month dropdown does not use INDIRECT: {month_dv.formula1}")
        else:
            print("FAIL: Component 2 — No dependent month dropdown validation found on C column")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Quarter validation covers correct range B2:B30 (0.15 points)
    try:
        if quarter_dv is not None:
            sqref_str = str(quarter_dv.sqref).upper().replace(' ', '')
            # Check that the range starts at B2 and goes to at least B30
            if 'B2' in sqref_str and 'B30' in sqref_str:
                print(f"PASS: Component 3 — Quarter validation range is correct: {quarter_dv.sqref} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Quarter validation range incorrect: {quarter_dv.sqref} (expected B2:B30)")
        else:
            print("FAIL: Component 3 — No quarter validation to check range")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Month validation covers correct range C2:C30 (0.15 points)
    try:
        if month_dv is not None:
            sqref_str = str(month_dv.sqref).upper().replace(' ', '')
            if 'C2' in sqref_str and 'C30' in sqref_str:
                print(f"PASS: Component 4 — Month validation range is correct: {month_dv.sqref} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Month validation range incorrect: {month_dv.sqref} (expected C2:C30)")
        else:
            print("FAIL: Component 4 — No month validation to check range")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_calc")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entrypoint
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
