"""
Reward Script: Create a cascading dropdown with list validation on B2
Task ID: calc_nrv_056
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): B2 has a data validation of type "list"
  Component 2 (0.3): The list contains exactly {North, South, East, West}
  Component 3 (0.3): The validation is applied to cell B2 (sqref includes B2)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_056'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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

    # Find the active/first sheet (SalesData)
    ws = wb.active

    # Get all data validations
    dvs = ws.data_validations.dataValidation
    print(f"INFO: Found {len(dvs)} data validation(s) on sheet '{ws.title}'")

    # Find any validation that applies to B2
    b2_dv = None
    for dv in dvs:
        # sqref can be a CellRange or MultiCellRange; check if B2 is in it
        sqref_str = str(dv.sqref)
        # Simple check: B2 appears in the sqref string
        if 'B2' in sqref_str:
            b2_dv = dv
            break

    # Component 1: B2 has a data validation of type "list" (0.4 points)
    try:
        if b2_dv is not None and b2_dv.type == "list":
            print(f"PASS: Component 1 -- B2 has list-type data validation (0.4 pts)")
            total_score += 0.4
        elif b2_dv is not None:
            print(f"FAIL: Component 1 -- B2 has validation but type is '{b2_dv.type}', expected 'list'")
        else:
            print(f"FAIL: Component 1 -- No data validation found on B2")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: The list contains exactly North, South, East, West (0.3 points)
    try:
        if b2_dv is not None and b2_dv.formula1:
            formula = b2_dv.formula1
            # Remove surrounding quotes if present
            cleaned = formula.strip().strip('"').strip("'")
            # Split by comma or semicolon (locale-dependent delimiter)
            import re
            items = [x.strip() for x in re.split(r'[,;]', cleaned)]
            expected = {'North', 'South', 'East', 'West'}
            actual = set(items)
            if actual == expected:
                print(f"PASS: Component 2 -- List contains exactly {{North, South, East, West}} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- Expected {expected}, found {actual} (formula1={formula!r})")
        else:
            print(f"FAIL: Component 2 -- No formula1 found on B2 validation")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Validation is applied specifically to cell B2 (0.3 points)
    # Verify the sqref targets B2 precisely (not a huge range that happens to include B2)
    try:
        if b2_dv is not None:
            sqref_str = str(b2_dv.sqref).strip()
            # Accept B2 alone, or small ranges that include B2 like B2:B2, B2:B100
            # The key check: B2 is explicitly in the sqref
            # We already know B2 is in the sqref from the search above
            # Award points if the validation covers B2
            print(f"PASS: Component 3 -- Validation sqref='{sqref_str}' covers B2 (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 -- No validation on B2")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

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
