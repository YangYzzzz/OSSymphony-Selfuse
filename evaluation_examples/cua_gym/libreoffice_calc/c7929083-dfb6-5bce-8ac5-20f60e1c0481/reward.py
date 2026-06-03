"""
Reward Script: Define named ranges StockPrices and SharesHeld, then create SUMPRODUCT formula in F2
Task ID: calc_nrv_030
Domain: libreoffice_calc
Scoring:
  Component 1 (0.35): Named range 'StockPrices' refers to $C$2:$C$25
  Component 2 (0.35): Named range 'SharesHeld' refers to $D$2:$D$25
  Component 3 (0.30): F2 contains SUMPRODUCT formula referencing the named ranges
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_030'


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


def normalize_ref(ref_str):
    """Normalize a defined name reference for comparison.
    Removes sheet prefix and dollar signs, lowercases."""
    # Remove sheet name prefix like 'Sheet1!'
    ref = re.sub(r"^[^!]+!", "", ref_str)
    # Remove dollar signs
    ref = ref.replace("$", "")
    return ref.upper()


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

    # Collect defined names into a dict for easy lookup
    defined_names = {}
    try:
        for name, dn in wb.defined_names.items():
            defined_names[name.lower()] = dn.attr_text
            print(f"INFO: Found defined name '{name}' -> '{dn.attr_text}'")
    except Exception as e:
        print(f"INFO: Error reading defined names: {e}")

    # Component 1: Named range 'StockPrices' refers to C2:C25 (0.35 points)
    try:
        if "stockprices" in defined_names:
            ref = defined_names["stockprices"]
            norm = normalize_ref(ref)
            if norm == "C2:C25":
                print(f"PASS: Component 1 — StockPrices defined as '{ref}' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — StockPrices ref is '{ref}', normalized to '{norm}', expected 'C2:C25'")
        else:
            print(f"FAIL: Component 1 — Named range 'StockPrices' not found. Defined names: {list(defined_names.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Named range 'SharesHeld' refers to D2:D25 (0.35 points)
    try:
        if "sharesheld" in defined_names:
            ref = defined_names["sharesheld"]
            norm = normalize_ref(ref)
            if norm == "D2:D25":
                print(f"PASS: Component 2 — SharesHeld defined as '{ref}' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — SharesHeld ref is '{ref}', normalized to '{norm}', expected 'D2:D25'")
        else:
            print(f"FAIL: Component 2 — Named range 'SharesHeld' not found. Defined names: {list(defined_names.keys())}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: F2 contains SUMPRODUCT formula using the named ranges (0.30 points)
    try:
        f2_val = ws["F2"].value
        if f2_val and isinstance(f2_val, str) and f2_val.startswith("="):
            formula_upper = f2_val.upper().replace(" ", "")
            # Check that it uses SUMPRODUCT
            if "SUMPRODUCT" in formula_upper:
                # Check that it references both named ranges (or their cell equivalents)
                uses_stock = "STOCKPRICES" in formula_upper or "C2:C25" in formula_upper.replace("$", "")
                uses_shares = "SHARESHELD" in formula_upper or "D2:D25" in formula_upper.replace("$", "")
                if uses_stock and uses_shares:
                    print(f"PASS: Component 3 — F2 formula '{f2_val}' uses SUMPRODUCT with both ranges (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 3 — F2 formula '{f2_val}' uses SUMPRODUCT but missing range references (stock={uses_stock}, shares={uses_shares})")
            else:
                print(f"FAIL: Component 3 — F2 formula '{f2_val}' does not use SUMPRODUCT")
        else:
            print(f"FAIL: Component 3 — F2 does not contain a formula (value: {f2_val})")
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
