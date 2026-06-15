"""
Reward Script: Name cell B1 as 'InterestRate'
Task ID: calc_nrv_009
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): Named range 'InterestRate' exists
  Component 2 (0.3): Named range refers to $B$1 on 'Loan Parameters'
  Component 3 (0.2): B1 still contains 0.045 (data preserved after naming)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_009'


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
    Verify that a named range 'InterestRate' has been created
    pointing to $B$1 on the 'Loan Parameters' sheet,
    and that B1 still contains 0.045.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Named range 'InterestRate' exists (0.5 points)
    try:
        defined_names = dict(wb.defined_names)
        matching_names = [k for k in defined_names if k.lower() == 'interestrate']

        if len(matching_names) > 0:
            print(f"PASS: Component 1 — Named range 'InterestRate' exists (0.5 pts)")
            total_score += 0.5
        else:
            all_names = list(defined_names.keys())
            print(f"FAIL: Component 1 — Named range 'InterestRate' not found. Existing names: {all_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Named range refers to $B$1 on 'Loan Parameters' sheet (0.3 points)
    try:
        dn_obj = None
        for name_key, dn in wb.defined_names.items():
            if name_key.lower() == 'interestrate':
                dn_obj = dn
                break

        if dn_obj is not None:
            attr_text = dn_obj.attr_text
            # Expected format: 'Loan Parameters'!$B$1
            # Normalize: remove quotes and spaces for comparison
            normalized = attr_text.replace("'", "").replace(" ", "").upper()
            # Check it references $B$1 on the correct sheet
            if "$B$1" in normalized and "LOANPARAMETERS" in normalized:
                print(f"PASS: Component 2 — Named range refers to correct cell: {attr_text} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Named range refers to '{attr_text}', expected reference to 'Loan Parameters'!$B$1")
        else:
            print(f"FAIL: Component 2 — Cannot check reference, named range not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: B1 still contains 0.045 (0.2 points)
    # This is a compound check: data integrity AND the named range exists.
    # Without the named range existing (Component 1), this should not award points.
    try:
        if total_score >= 0.5:  # Only check if named range exists (anchored to task change)
            ws = wb['Loan Parameters']
            b1_val = ws['B1'].value
            if b1_val is not None and abs(float(b1_val) - 0.045) < 0.0001:
                print(f"PASS: Component 3 — B1 contains {b1_val}, data preserved after naming (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — B1 value is {b1_val}, expected 0.045")
        else:
            print(f"FAIL: Component 3 — Skipped (named range not found, so data integrity check is moot)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI state
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
