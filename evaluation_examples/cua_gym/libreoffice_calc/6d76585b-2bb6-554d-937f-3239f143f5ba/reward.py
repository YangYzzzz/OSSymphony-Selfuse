"""
Reward Script: Create dropdown validation in B2:B15 using named range 'Priorities'
Task ID: calc_nrv_075
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): List-type data validation exists on B2:B15
  Component 2 (0.3): Validation formula references 'Priorities' named range
  Component 3 (0.3): Validation covers the full B2:B15 range exactly
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_075'


def persist_app_state(domain: str):
    """Attempt to save any unsaved LibreOffice state via Ctrl+S."""
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

    ws = wb.active

    # Precondition: Named range 'Priorities' must still exist referencing F1:F4
    try:
        if 'Priorities' not in wb.defined_names:
            print("PRECONDITION FAIL: Named range 'Priorities' does not exist")
            print("REWARD: 0.0")
            return 0.0
        else:
            print("PRECONDITION: Named range 'Priorities' exists")
    except Exception as e:
        print(f"ERROR: Could not check named ranges: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the relevant data validation(s) that cover B2:B15
    validations = ws.data_validations.dataValidation
    target_dv = None

    for dv in validations:
        # Check if this validation covers any cells in B2:B15
        sqref_str = str(dv.sqref)
        # Parse cell ranges to see if B2:B15 is covered
        if 'B' in sqref_str:
            target_dv = dv
            break

    # Component 1: A list-type data validation exists that covers B column cells (0.4 points)
    try:
        if target_dv is not None and target_dv.type == 'list':
            print(f"PASS: Component 1 -- List-type data validation found (type={target_dv.type}) (0.4 pts)")
            total_score += 0.4
        else:
            if target_dv is None:
                print("FAIL: Component 1 -- No data validation found covering B column cells")
            else:
                print(f"FAIL: Component 1 -- Validation type is '{target_dv.type}', expected 'list'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Validation formula references 'Priorities' named range (0.3 points)
    try:
        if target_dv is not None:
            formula = str(target_dv.formula1) if target_dv.formula1 else ''
            # Accept 'Priorities' or '=Priorities' or 'Priorities' (case-insensitive)
            formula_clean = formula.strip().lstrip('=').strip()
            if formula_clean.lower() == 'priorities':
                print(f"PASS: Component 2 -- Formula references 'Priorities' named range (formula1={target_dv.formula1}) (0.3 pts)")
                total_score += 0.3
            else:
                # Also accept if formula references $F$1:$F$4 directly (functionally equivalent)
                if '$F$1:$F$4' in formula or 'F1:F4' in formula:
                    print(f"PASS: Component 2 -- Formula references F1:F4 range directly (formula1={target_dv.formula1}) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 -- Expected formula referencing 'Priorities', found: '{target_dv.formula1}'")
        else:
            print("FAIL: Component 2 -- No target validation found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Validation covers the full B2:B15 range (0.3 points)
    try:
        if target_dv is not None:
            sqref_str = str(target_dv.sqref).replace(' ', '')
            # Check that B2:B15 is covered
            # Accept exact match or equivalent representations
            # Parse cells covered by the validation
            from openpyxl.utils import range_boundaries
            covered_cells = set()
            for rng in str(target_dv.sqref).split():
                try:
                    min_col, min_row, max_col, max_row = range_boundaries(rng)
                    for r in range(min_row, max_row + 1):
                        for c in range(min_col, max_col + 1):
                            covered_cells.add((r, c))
                except Exception:
                    pass

            # B column = column 2, rows 2-15
            required_cells = set()
            for r in range(2, 16):
                required_cells.add((r, 2))

            if required_cells.issubset(covered_cells):
                print(f"PASS: Component 3 -- Validation covers full B2:B15 range (sqref={target_dv.sqref}) (0.3 pts)")
                total_score += 0.3
            else:
                missing = required_cells - covered_cells
                print(f"FAIL: Component 3 -- Validation does not cover all of B2:B15. Missing {len(missing)} cells. Sqref: {target_dv.sqref}")
        else:
            print("FAIL: Component 3 -- No target validation found")
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
