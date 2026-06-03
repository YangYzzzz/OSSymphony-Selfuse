"""
Reward Script: Set up a dropdown validation for the Priority column (column C)
Task ID: osworld_calc_data_validation_dropdown_003
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.5 pts): Data validation of type 'list' on column C with all 5 required options
  - Component 2 (0.3 pts): Validation covers column C data rows (e.g. C2:C100 or similar)
  - Component 3 (0.2 pts): Input message prompt text contains 'Select task priority level'
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'osworld_calc_data_validation_dropdown_003'

REQUIRED_OPTIONS = ['Critical', 'High', 'Medium', 'Low', 'None']
REQUIRED_PROMPT = 'Select task priority level'


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

    # Locate the expected worksheet
    try:
        if 'Task Tracker' in wb.sheetnames:
            ws = wb['Task Tracker']
        else:
            ws = wb.active
    except Exception as e:
        print(f"ERROR: Cannot access worksheet: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Retrieve all data validations on the sheet
    validations = ws.data_validations.dataValidation

    # Find any list-type data validation that targets column C
    col_c_dv = None
    for dv in validations:
        if dv.type == 'list':
            # Check if any cell in the sqref covers column C
            sqref_str = str(dv.sqref)
            # sqref may be something like 'C2:C100' or 'C2:C13'
            # We look for 'C' in the sqref coordinates
            if 'C' in sqref_str.upper():
                col_c_dv = dv
                break

    # Component 1: List data validation exists on column C with all 5 required options (0.5 pts)
    try:
        if col_c_dv is None:
            print("FAIL: Component 1 — No list data validation found on column C")
        else:
            # formula1 is typically stored as '"Critical,High,Medium,Low,None"'
            formula = col_c_dv.formula1 or ''
            # Strip surrounding quotes if present
            formula_clean = formula.strip('"').strip("'")
            actual_options = [opt.strip() for opt in formula_clean.split(',')]

            all_present = all(opt in actual_options for opt in REQUIRED_OPTIONS)
            exact_count = len(actual_options) == len(REQUIRED_OPTIONS)

            if all_present and exact_count:
                print(f"PASS: Component 1 — All 5 required options found: {actual_options} (0.5 pts)")
                total_score += 0.5
            elif all_present:
                # All required options present but extra ones exist; still counts as valid
                print(f"PASS: Component 1 — All 5 required options found (extra options present): {actual_options} (0.5 pts)")
                total_score += 0.5
            else:
                missing = [opt for opt in REQUIRED_OPTIONS if opt not in actual_options]
                print(f"FAIL: Component 1 — Missing options: {missing}. Found: {actual_options}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Validation covers column C data rows (0.3 pts)
    try:
        if col_c_dv is None:
            print("FAIL: Component 2 — No list data validation found on column C (prerequisite failed)")
        else:
            sqref_str = str(col_c_dv.sqref)
            # Verify the sqref references column C specifically
            # Typical expected range: C2:C100 or C2:Cxx
            # We verify that it starts at or above row 2 and covers multiple rows
            import re
            # Match patterns like C2:C100 or C2:C13
            match = re.search(r'C(\d+):C(\d+)', sqref_str, re.IGNORECASE)
            if match:
                start_row = int(match.group(1))
                end_row = int(match.group(2))
                # Validation should start at row 2 (header is row 1) and cover enough rows
                if start_row <= 2 and end_row >= 10:
                    print(f"PASS: Component 2 — Validation covers column C rows {start_row} to {end_row} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — Validation range C{start_row}:C{end_row} does not adequately cover data rows (expected start<=2, end>=10)")
            else:
                # May be a single column reference like C:C or just C
                if re.search(r'\bC\b', sqref_str, re.IGNORECASE):
                    print(f"PASS: Component 2 — Validation covers column C (sqref: {sqref_str}) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — sqref '{sqref_str}' does not clearly target column C")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Input message prompt text contains 'Select task priority level' (0.2 pts)
    try:
        if col_c_dv is None:
            print("FAIL: Component 3 — No list data validation found on column C (prerequisite failed)")
        else:
            prompt_text = col_c_dv.prompt or ''
            if REQUIRED_PROMPT.lower() in prompt_text.lower():
                print(f"PASS: Component 3 — Input message prompt found: '{prompt_text}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Expected prompt '{REQUIRED_PROMPT}', found: '{prompt_text}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
