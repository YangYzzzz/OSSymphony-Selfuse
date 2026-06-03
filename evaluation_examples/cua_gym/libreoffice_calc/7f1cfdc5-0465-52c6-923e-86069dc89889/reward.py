"""
Reward Script: Employee onboarding form data validation setup
Task ID: calc_nrv_076
Domain: libreoffice_calc
Scoring:
  Component 1 (0.35) - B3 has date validation for current year
  Component 2 (0.35) - B4 has list validation from Config sheet
  Component 3 (0.30) - B5 has decimal validation between 30000 and 500000
"""

import os
import openpyxl
from datetime import date

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_076'


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

    # Precondition: Onboarding sheet must exist
    if 'Onboarding' not in wb.sheetnames:
        print("CRITICAL: 'Onboarding' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Onboarding']
    validations = ws.data_validations.dataValidation

    # Build a lookup: cell coordinate -> data validation object
    dv_map = {}
    for dv in validations:
        sqref_str = str(dv.sqref)
        # sqref can contain multiple ranges separated by space
        for ref in sqref_str.split():
            dv_map[ref.upper()] = dv

    # Component 1: B3 has date validation for current year (0.35 points)
    try:
        dv_b3 = dv_map.get('B3')
        if dv_b3 is not None and dv_b3.type == 'date':
            # Check that formula1 and formula2 define a current-year range
            f1 = str(dv_b3.formula1)
            f2 = str(dv_b3.formula2)
            current_year = date.today().year

            # formula1/formula2 can be date objects or strings like "2026-01-01"
            year_start_ok = str(current_year) in f1 and ('01-01' in f1 or 'Jan' in f1)
            year_end_ok = str(current_year) in f2 and ('12-31' in f2 or 'Dec' in f2)

            if year_start_ok and year_end_ok:
                print(f"PASS: Component 1 - B3 has date validation for {current_year} (formula1={f1}, formula2={f2}) (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 - B3 date validation range not for current year. formula1={f1}, formula2={f2}")
        else:
            dv_type = dv_b3.type if dv_b3 else 'None'
            print(f"FAIL: Component 1 - B3 does not have date validation (found type: {dv_type})")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: B4 has list validation from Config!$A$1:$A$10 (0.35 points)
    try:
        dv_b4 = dv_map.get('B4')
        if dv_b4 is not None and dv_b4.type == 'list':
            f1 = str(dv_b4.formula1)
            # Normalize: remove leading '=' and spaces, uppercase
            f1_norm = f1.strip().lstrip('=').upper().replace(' ', '')
            # Accept various forms: Config!$A$1:$A$10, 'Config'!$A$1:$A$10, Config.$A$1:$A$10
            # Key checks: references Config sheet and range A1:A10
            has_config_ref = 'CONFIG' in f1_norm
            has_a1_a10 = ('$A$1:$A$10' in f1_norm or 'A1:A10' in f1_norm or
                          '$A$1:$A$10' in f1_norm.replace('.', '!'))

            if has_config_ref and has_a1_a10:
                print(f"PASS: Component 2 - B4 has list validation from Config sheet (formula1={f1}) (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 - B4 list validation formula does not reference Config!$A$1:$A$10. Got: {f1}")
        else:
            dv_type = dv_b4.type if dv_b4 else 'None'
            print(f"FAIL: Component 2 - B4 does not have list validation (found type: {dv_type})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: B5 has decimal validation between 30000 and 500000 (0.30 points)
    try:
        dv_b5 = dv_map.get('B5')
        if dv_b5 is not None and dv_b5.type == 'decimal':
            f1 = str(dv_b5.formula1).strip()
            f2 = str(dv_b5.formula2).strip()
            try:
                low = float(f1)
                high = float(f2)
                if abs(low - 30000) < 1 and abs(high - 500000) < 1:
                    print(f"PASS: Component 3 - B5 has decimal validation [{low}, {high}] (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 3 - B5 decimal range mismatch. Expected [30000, 500000], got [{low}, {high}]")
            except ValueError:
                print(f"FAIL: Component 3 - B5 decimal formula not numeric. formula1={f1}, formula2={f2}")
        else:
            dv_type = dv_b5.type if dv_b5 else 'None'
            print(f"FAIL: Component 3 - B5 does not have decimal validation (found type: {dv_type})")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

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
