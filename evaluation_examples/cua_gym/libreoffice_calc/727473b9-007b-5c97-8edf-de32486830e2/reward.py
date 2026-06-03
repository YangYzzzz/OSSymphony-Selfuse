"""
Reward Script: Create named ranges CommissionRate and SalesTotal, then write commission formula in C2
Task ID: calc_nrv_023
Domain: libreoffice_calc
Scoring:
  Component 1 (0.35): Named range 'CommissionRate' refers to $G$1
  Component 2 (0.30): Named range 'SalesTotal' refers to $B$2:$B$20
  Component 3 (0.35): Cell C2 contains formula =B2*CommissionRate
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_023'


def persist_app_state(domain: str):
    """Best-effort save of any open LibreOffice document."""
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
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb.active

    # Component 1: Named range 'CommissionRate' refers to $G$1 (0.35 points)
    try:
        # Build a lookup dict of defined names (case-insensitive)
        name_map = {dn.name.lower(): dn.attr_text for dn in wb.defined_names.values()}
        cr_ref = name_map.get('commissionrate')
        if cr_ref is not None:
            print(f"  Found defined name 'CommissionRate' with ref: {cr_ref}")
            # Accept variations like Sheet1!$G$1 or 'Sheet1'!$G$1
            if '$G$1' in cr_ref.upper().replace("'", ""):
                print(f"PASS: Component 1 — CommissionRate refers to $G$1 (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — CommissionRate ref is '{cr_ref}', expected ...$G$1")
        else:
            print(f"FAIL: Component 1 — Named range 'CommissionRate' not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Named range 'SalesTotal' refers to $B$2:$B$20 (0.30 points)
    try:
        st_ref = name_map.get('salestotal')
        if st_ref is not None:
            print(f"  Found defined name 'SalesTotal' with ref: {st_ref}")
            if '$B$2:$B$20' in st_ref.upper().replace("'", ""):
                print(f"PASS: Component 2 — SalesTotal refers to $B$2:$B$20 (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — SalesTotal ref is '{st_ref}', expected ...$B$2:$B$20")
        else:
            print(f"FAIL: Component 2 — Named range 'SalesTotal' not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Cell C2 contains formula =B2*CommissionRate (0.35 points)
    try:
        c2_val = ws['C2'].value
        print(f"  C2 value: {repr(c2_val)}")
        if c2_val is not None and isinstance(c2_val, str) and c2_val.startswith('='):
            # Normalize: uppercase, remove spaces
            formula_norm = c2_val.upper().replace(" ", "")
            # Accept =B2*CommissionRate or =CommissionRate*B2
            if ('B2' in formula_norm and 'COMMISSIONRATE' in formula_norm and '*' in formula_norm):
                print(f"PASS: Component 3 — C2 has formula using B2*CommissionRate (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 3 — C2 formula '{c2_val}' does not multiply B2 by CommissionRate")
        else:
            print(f"FAIL: Component 3 — C2 is not a formula, found: {repr(c2_val)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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
