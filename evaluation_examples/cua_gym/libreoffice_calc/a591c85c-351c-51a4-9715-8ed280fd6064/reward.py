"""
Reward Script: Name cell B2 as 'ExchangeRate' and write EUR conversion formula in E2
Task ID: calc_nrv_037
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): Named range 'ExchangeRate' exists and refers to $B$2
  Component 2 (0.5): Cell E2 contains a formula that references 'ExchangeRate' for USD->EUR conversion
"""

import os
import openpyxl
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_037'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
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

    # Component 1: Named range 'ExchangeRate' exists and refers to $B$2 (0.5 points)
    try:
        defined_names = dict(wb.defined_names)
        if 'ExchangeRate' in defined_names:
            dn = defined_names['ExchangeRate']
            attr_text = dn.attr_text
            # Should reference $B$2 on some sheet
            # Acceptable patterns: Sheet1!$B$2, 'Sheet1'!$B$2, etc.
            if '$B$2' in attr_text.upper():
                print(f"PASS: Component 1 — Named range 'ExchangeRate' found, refers to '{attr_text}' (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — Named range 'ExchangeRate' exists but refers to '{attr_text}', expected reference to $B$2")
        else:
            # Also check case-insensitively
            ci_match = next((n for n in wb.defined_names if n.lower() == 'exchangerate'), None)
            if ci_match is not None:
                dn = wb.defined_names[ci_match]
                attr_text = dn.attr_text
                if '$B$2' in attr_text.upper():
                    print(f"PASS: Component 1 — Named range '{ci_match}' found (case variant), refers to '{attr_text}' (0.5 pts)")
                    total_score += 0.5
                else:
                    print(f"FAIL: Component 1 — Named range '{ci_match}' found but refers to '{attr_text}', expected $B$2")
            else:
                print(f"FAIL: Component 1 — No named range 'ExchangeRate' found. Defined names: {list(wb.defined_names.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Cell E2 contains a formula using ExchangeRate for conversion (0.5 points)
    try:
        e2_value = ws['E2'].value
        if e2_value is None:
            print(f"FAIL: Component 2 — Cell E2 is empty")
        elif isinstance(e2_value, str) and e2_value.startswith('='):
            formula_upper = e2_value.upper().replace(' ', '')
            # The formula should reference D2 and ExchangeRate
            has_d2 = 'D2' in formula_upper
            has_exchange_rate = 'EXCHANGERATE' in formula_upper

            if has_d2 and has_exchange_rate:
                # Check it's a valid conversion formula (division or multiplication)
                # =D2/ExchangeRate or =D2*ExchangeRate are both acceptable
                if '/' in formula_upper or '*' in formula_upper:
                    print(f"PASS: Component 2 — E2 contains formula '{e2_value}' referencing D2 and ExchangeRate (0.5 pts)")
                    total_score += 0.5
                else:
                    print(f"FAIL: Component 2 — E2 has formula '{e2_value}' with D2 and ExchangeRate but no arithmetic operator (/ or *)")
            elif has_exchange_rate and not has_d2:
                print(f"FAIL: Component 2 — E2 formula '{e2_value}' references ExchangeRate but not D2")
            elif has_d2 and not has_exchange_rate:
                print(f"FAIL: Component 2 — E2 formula '{e2_value}' references D2 but not the named range ExchangeRate")
            else:
                print(f"FAIL: Component 2 — E2 formula '{e2_value}' does not reference D2 or ExchangeRate")
        else:
            print(f"FAIL: Component 2 — E2 contains '{e2_value}' which is not a formula (expected formula starting with '=')")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

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
