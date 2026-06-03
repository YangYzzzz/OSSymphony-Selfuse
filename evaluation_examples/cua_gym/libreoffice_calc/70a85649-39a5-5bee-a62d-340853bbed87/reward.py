"""
Reward Script: Create named range 'HeaderRow' for A1:L1
Task ID: calc_nrv_042
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): Named range 'HeaderRow' exists
  Component 2 (0.4): Named range refers to correct range ($A$1:$L$1 on active sheet)
  Component 3 (0.2): Print title rows set to row 1 ($1:$1)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_042'


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
    sheet_name = ws.title

    # Component 1: Named range 'HeaderRow' exists (0.4 points)
    try:
        defined_names = list(wb.defined_names)
        # Case-insensitive check for 'HeaderRow'
        header_row_name = None
        for name_key in defined_names:
            if name_key.lower() == 'headerrow':
                header_row_name = name_key
                break

        if header_row_name is not None:
            print(f"PASS: Component 1 — Named range 'HeaderRow' exists (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Named range 'HeaderRow' not found. Defined names: {defined_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Named range refers to correct range $A$1:$L$1 on the sheet (0.4 points)
    try:
        if header_row_name is not None:
            dn = wb.defined_names[header_row_name]
            attr_text = dn.attr_text
            print(f"  Named range value: {attr_text}")

            # Normalize: remove quotes around sheet name if present, compare case-insensitively
            # Expected patterns:
            #   Employees!$A$1:$L$1
            #   'Employees'!$A$1:$L$1
            normalized = attr_text.replace("'", "").upper()
            expected_upper = f"{sheet_name.upper()}!$A$1:$L$1"

            if normalized == expected_upper:
                print(f"PASS: Component 2 — Range correctly refers to {sheet_name}!$A$1:$L$1 (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Expected '{expected_upper}', got '{normalized}'")
        else:
            print(f"FAIL: Component 2 — Cannot check range, named range does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Print title rows set to row 1 (0.2 points)
    # This is the optional part from the task context: "rows to repeat at top is set to row 1"
    try:
        print_title_rows = ws.print_title_rows
        if print_title_rows is not None:
            # Expected: '$1:$1' or '1:1'
            normalized_ptr = print_title_rows.replace("$", "")
            if normalized_ptr == "1:1":
                print(f"PASS: Component 3 — Print title rows set to row 1: {print_title_rows} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Print title rows is '{print_title_rows}', expected '$1:$1'")
        else:
            print(f"FAIL: Component 3 — Print title rows not set (None)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
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
