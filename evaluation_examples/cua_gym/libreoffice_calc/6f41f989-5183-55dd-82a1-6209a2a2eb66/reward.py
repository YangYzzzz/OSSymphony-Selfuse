"""
Reward Script: Dynamic data validation with OFFSET named range for vendor dropdown
Task ID: calc_gcv_094
Domain: libreoffice_calc
Scoring:
  Component 1: Named range 'ApprovedVendors' exists (0.3 pts)
  Component 2: Named range formula uses OFFSET+COUNTA dynamic pattern (0.3 pts)
  Component 3: Data validation on E2:E20 referencing 'ApprovedVendors' (0.4 pts)
"""

import os
import re

import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcv_094'


def persist_app_state(domain: str):
    """Best-effort save of any unsaved GUI state."""
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

    # ---------------------------------------------------------------
    # Component 1: Named range 'ApprovedVendors' exists (0.3 points)
    # ---------------------------------------------------------------
    try:
        defined_names = {n.lower(): wb.defined_names[n] for n in wb.defined_names}
        if 'approvedvendors' in defined_names:
            print(f"PASS: Component 1 — Named range 'ApprovedVendors' exists (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Named range 'ApprovedVendors' not found. "
                  f"Found names: {list(wb.defined_names)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Component 2: Named range formula uses OFFSET+COUNTA dynamic
    #              pattern referencing column H (0.3 points)
    # ---------------------------------------------------------------
    try:
        dn = defined_names.get('approvedvendors')
        if dn is not None:
            formula = dn.attr_text.upper().replace(" ", "")
            print(f"  DEBUG: Named range formula = {dn.attr_text}")

            has_offset = 'OFFSET(' in formula
            has_counta = 'COUNTA(' in formula
            refs_h = '$H$1' in formula or '$H:$H' in formula or 'H1' in formula.replace('$', '')

            if has_offset and has_counta and refs_h:
                print(f"PASS: Component 2 — Formula uses OFFSET+COUNTA referencing H column (0.3 pts)")
                total_score += 0.3
            else:
                missing = []
                if not has_offset:
                    missing.append("OFFSET")
                if not has_counta:
                    missing.append("COUNTA")
                if not refs_h:
                    missing.append("H column reference")
                print(f"FAIL: Component 2 — Formula missing: {', '.join(missing)}. "
                      f"Formula: {dn.attr_text}")
        else:
            print(f"FAIL: Component 2 — Cannot check formula; named range not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: Data validation on E2:E20, type=list,
    #              referencing 'ApprovedVendors' (0.4 points)
    # ---------------------------------------------------------------
    try:
        validations = ws.data_validations.dataValidation
        found_valid_dv = False

        for dv in validations:
            dv_type = dv.type
            dv_formula = str(dv.formula1).strip() if dv.formula1 else ""
            dv_range = str(dv.sqref).upper().replace(" ", "")

            print(f"  DEBUG: Validation — type={dv_type}, formula1={dv_formula}, range={dv_range}")

            # Check type is list
            if dv_type != "list":
                continue

            # Check formula references ApprovedVendors (case-insensitive)
            if "APPROVEDVENDORS" not in dv_formula.upper():
                continue

            # Check range covers E2:E20
            # The range may be expressed as E2:E20 or multiple sub-ranges
            # We need E2:E20 to be covered
            if "E2:E20" in dv_range:
                found_valid_dv = True
                break

        if found_valid_dv:
            print(f"PASS: Component 3 — Data validation list on E2:E20 referencing ApprovedVendors (0.4 pts)")
            total_score += 0.4
        else:
            if len(validations) == 0:
                print(f"FAIL: Component 3 — No data validations found on the sheet")
            else:
                print(f"FAIL: Component 3 — No matching validation (list type on E2:E20 referencing ApprovedVendors)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
