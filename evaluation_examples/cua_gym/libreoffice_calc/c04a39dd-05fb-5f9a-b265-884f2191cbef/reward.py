"""
Reward Script: Define named ranges and SUMPRODUCT formula
Task ID: calc_nrv_019
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Named range 'CostCenter' = $A$2:$A$50
  Component 2 (0.3): Named range 'Expenses' = $C$2:$C$50
  Component 3 (0.4): F2 contains SUMPRODUCT formula using CostCenter, "Marketing", Expenses
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_019'


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


def normalize_range_ref(ref_str):
    """
    Normalize a defined name value like "Expenses!$A$2:$A$50" to a
    canonical form for comparison. Returns (sheet, col1, row1, col2, row2).
    """
    # Strip sheet name prefix if present
    if '!' in ref_str:
        ref_str = ref_str.split('!')[-1]
    # Remove $ signs
    ref_str = ref_str.replace('$', '')
    # Parse e.g. "A2:A50"
    match = re.match(r'^([A-Z]+)(\d+):([A-Z]+)(\d+)$', ref_str.upper())
    if match:
        return (match.group(1), int(match.group(2)), match.group(3), int(match.group(4)))
    return None


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

    # Component 1: Named range 'CostCenter' defined as $A$2:$A$50 (0.3 points)
    try:
        found_cost_center = False
        for name, dn in wb.defined_names.items():
            if name.lower() == 'costcenter':
                ref = dn.attr_text
                parsed = normalize_range_ref(ref)
                if parsed and parsed == ('A', 2, 'A', 50):
                    found_cost_center = True
                    print(f"PASS: Component 1 -- Named range 'CostCenter' found: {ref} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 1 -- Named range 'CostCenter' has wrong range: {ref} (expected $A$2:$A$50)")
                break
        if not found_cost_center and total_score < 0.3:
            print("FAIL: Component 1 -- Named range 'CostCenter' not found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Named range 'Expenses' defined as $C$2:$C$50 (0.3 points)
    try:
        found_expenses = False
        for name, dn in wb.defined_names.items():
            if name.lower() == 'expenses':
                ref = dn.attr_text
                parsed = normalize_range_ref(ref)
                if parsed and parsed == ('C', 2, 'C', 50):
                    found_expenses = True
                    print(f"PASS: Component 2 -- Named range 'Expenses' found: {ref} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 -- Named range 'Expenses' has wrong range: {ref} (expected $C$2:$C$50)")
                break
        if not found_expenses and total_score < 0.6:
            print("FAIL: Component 2 -- Named range 'Expenses' not found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: F2 contains SUMPRODUCT formula referencing CostCenter, "Marketing", Expenses (0.4 points)
    try:
        ws = wb.active
        f2_val = ws["F2"].value
        if f2_val and isinstance(f2_val, str) and f2_val.startswith('='):
            formula_upper = f2_val.upper().replace(" ", "")
            # Check that the formula uses SUMPRODUCT
            has_sumproduct = 'SUMPRODUCT' in formula_upper
            # Check references to the named ranges (case-insensitive)
            has_costcenter = 'COSTCENTER' in formula_upper
            has_expenses = 'EXPENSES' in formula_upper
            # Check that "Marketing" is referenced
            has_marketing = 'MARKETING' in formula_upper

            if has_sumproduct and has_costcenter and has_expenses and has_marketing:
                print(f"PASS: Component 3 -- F2 contains correct SUMPRODUCT formula: {f2_val} (0.4 pts)")
                total_score += 0.4
            else:
                missing = []
                if not has_sumproduct:
                    missing.append("SUMPRODUCT function")
                if not has_costcenter:
                    missing.append("CostCenter named range")
                if not has_expenses:
                    missing.append("Expenses named range")
                if not has_marketing:
                    missing.append("Marketing criterion")
                print(f"FAIL: Component 3 -- F2 formula missing: {', '.join(missing)}. Found: {f2_val}")
        else:
            print(f"FAIL: Component 3 -- F2 does not contain a formula. Found: {f2_val}")
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
