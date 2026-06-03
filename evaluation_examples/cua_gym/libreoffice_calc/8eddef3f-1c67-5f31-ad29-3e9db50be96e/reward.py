"""
Reward Script: Fix VLOOKUP approximate match to exact match
Task ID: calc_tbl_041
Domain: libreoffice_calc
Scoring:
  Component 1 (0.6): D2 formula uses exact match (last arg is 0 or FALSE)
  Component 2 (0.4): D2 formula uses exact match AND the full VLOOKUP structure is intact
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_tbl_041'


def persist_app_state(domain: str):
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
    Verify that the VLOOKUP in D2 was changed from approximate match (1/TRUE)
    to exact match (0/FALSE).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the Orders sheet (precondition gate)
    try:
        ws = wb["Orders"]
    except KeyError:
        print("CRITICAL: 'Orders' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    d2_formula = ws["D2"].value
    print(f"DEBUG: D2 raw value = {repr(d2_formula)}")

    # Precondition: D2 must contain a formula
    if not isinstance(d2_formula, str) or not d2_formula.startswith("="):
        print("FAIL: D2 does not contain a formula")
        print("REWARD: 0.0")
        return 0.0

    # Normalize for comparison: uppercase, strip spaces
    formula_norm = d2_formula.upper().replace(" ", "")

    # Component 1: D2 formula uses exact match — last argument is 0 or FALSE (0.6 points)
    # This is THE key change: initial has ,1) or ,TRUE), golden has ,0) or ,FALSE)
    try:
        uses_exact_match = formula_norm.endswith(",0)") or formula_norm.endswith(",FALSE)")

        if uses_exact_match:
            print(f"PASS: Component 1 — D2 uses exact match (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — D2 does not use exact match. Formula: {d2_formula}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: D2 uses exact match AND the VLOOKUP structure is correct (0.4 points)
    # This is a compound check: exact match is required (anchored to the change),
    # PLUS the lookup range, column index, and lookup value are correct.
    # This ensures the agent didn't break the formula while fixing the match type.
    try:
        has_correct_range = "PRODUCTS.A:C" in formula_norm or "PRODUCTS.A1:C" in formula_norm
        has_correct_col_index = ",3," in formula_norm
        has_vlookup = formula_norm.startswith("=VLOOKUP(")
        has_widget_b = '"WIDGETB"' in formula_norm or "'WIDGETB'" in formula_norm
        uses_exact = formula_norm.endswith(",0)") or formula_norm.endswith(",FALSE)")

        # All conditions must hold, including exact match (the task-introduced change)
        if uses_exact and has_vlookup and has_correct_range and has_correct_col_index and has_widget_b:
            print(f"PASS: Component 2 — exact match + correct VLOOKUP structure (0.4 pts)")
            total_score += 0.4
        else:
            details = []
            if not uses_exact:
                details.append("not exact match")
            if not has_vlookup:
                details.append("not a VLOOKUP")
            if not has_correct_range:
                details.append("wrong range")
            if not has_correct_col_index:
                details.append("wrong col_index")
            if not has_widget_b:
                details.append("wrong lookup value")
            print(f"FAIL: Component 2 — issues: {', '.join(details)}. Formula: {d2_formula}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
