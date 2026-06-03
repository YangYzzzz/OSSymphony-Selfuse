"""
Reward Script: Named ranges for weighted scores
Task ID: calc_nrv_041
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): RawScores named range refers to $B$2:$B$20
  Component 2 (0.3): Weights named range refers to $C$2:$C$20
  Component 3 (0.4): WeightedScores is a formula-based named range (=RawScores*Weights or equivalent)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_041'


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
    Strips sheet prefix, whitespace, and converts to uppercase.
    """
    s = ref_str.strip().upper()
    # Remove common sheet prefixes like "Sheet1!" or "'Sheet1'!"
    s = re.sub(r"^'?[^'!]+'?!", "", s)
    return s


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

    # Collect all defined names into a dict for easy lookup
    defined_names = {}
    try:
        for name, defn in wb.defined_names.items():
            defined_names[name.upper()] = defn.attr_text
            print(f"  Found defined name: {name} = {defn.attr_text}")
    except Exception as e:
        print(f"ERROR: Could not iterate defined names: {e}")

    if not defined_names:
        print("FAIL: No defined names found in the workbook")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: RawScores named range refers to $B$2:$B$20 (0.3 points)
    try:
        if "RAWSCORES" in defined_names:
            raw_ref = normalize_ref(defined_names["RAWSCORES"])
            expected = "$B$2:$B$20"
            if raw_ref == expected:
                print(f"PASS: Component 1 — RawScores refers to {defined_names['RAWSCORES']} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — RawScores refers to '{raw_ref}', expected '{expected}'")
        else:
            print("FAIL: Component 1 — 'RawScores' named range not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Weights named range refers to $C$2:$C$20 (0.3 points)
    try:
        if "WEIGHTS" in defined_names:
            wt_ref = normalize_ref(defined_names["WEIGHTS"])
            expected = "$C$2:$C$20"
            if wt_ref == expected:
                print(f"PASS: Component 2 — Weights refers to {defined_names['WEIGHTS']} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Weights refers to '{wt_ref}', expected '{expected}'")
        else:
            print("FAIL: Component 2 — 'Weights' named range not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: WeightedScores is a formula-based named range (0.4 points)
    # It should be a formula like =RawScores*Weights or =$B$2:$B$20*$C$2:$C$20
    try:
        if "WEIGHTEDSCORES" in defined_names:
            ws_ref = defined_names["WEIGHTEDSCORES"].strip()
            ws_upper = ws_ref.upper().replace(" ", "")

            # Check if it's a formula (contains * for multiplication) rather than a cell range
            is_formula = "*" in ws_upper

            if is_formula:
                # Verify it references the correct ranges (by name or by cell reference)
                refs_rawscores = ("RAWSCORES" in ws_upper or "$B$2:$B$20" in ws_upper
                                  or "B2:B20" in ws_upper)
                refs_weights = ("WEIGHTS" in ws_upper or "$C$2:$C$20" in ws_upper
                                or "C2:C20" in ws_upper)

                if refs_rawscores and refs_weights:
                    print(f"PASS: Component 3 — WeightedScores is formula-based: '{ws_ref}' (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 3 — WeightedScores formula '{ws_ref}' does not reference both RawScores and Weights ranges")
            else:
                print(f"FAIL: Component 3 — WeightedScores is not formula-based (no multiplication): '{ws_ref}'")
        else:
            print("FAIL: Component 3 — 'WeightedScores' named range not found")
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
