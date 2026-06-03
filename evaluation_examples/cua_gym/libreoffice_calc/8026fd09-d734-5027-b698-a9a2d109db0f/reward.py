"""
Reward Script: Fix mismatched SUMIFS ranges
Task ID: calc_tbl_061
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): E1 contains a SUMIFS formula with A2:A100 criteria range (was A2:A50)
  Component 2 (0.3): All three ranges in SUMIFS use consistent row spans (2:100)
  Component 3 (0.3): The complete corrected formula matches expected form
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_tbl_061'


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


def parse_sumifs_ranges(formula):
    """
    Parse a SUMIFS formula and extract the ranges.
    Returns dict with keys: sum_range, criteria_range1, criteria1, criteria_range2, criteria2
    or None if parsing fails.
    """
    # Remove leading = and spaces
    f = formula.strip()
    if f.startswith('='):
        f = f[1:]

    # Match SUMIFS pattern (case insensitive)
    # SUMIFS(sum_range, criteria_range1, criteria1, criteria_range2, criteria2)
    match = re.match(
        r'SUMIFS\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^)]+)\s*\)',
        f, re.IGNORECASE
    )
    if not match:
        return None

    return {
        'sum_range': match.group(1).strip(),
        'criteria_range1': match.group(2).strip(),
        'criteria1': match.group(3).strip(),
        'criteria_range2': match.group(4).strip(),
        'criteria2': match.group(5).strip(),
    }


def extract_row_range(cell_range):
    """
    Extract start and end row from a range like 'A2:A100'.
    Returns (start_row, end_row) or None.
    """
    match = re.match(r'([A-Z]+)(\d+):([A-Z]+)(\d+)', cell_range, re.IGNORECASE)
    if not match:
        return None
    return (int(match.group(2)), int(match.group(4)))


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

    # Get the formula in E1
    e1_value = ws['E1'].value
    print(f"INFO: E1 value = {e1_value}")

    if not isinstance(e1_value, str) or not e1_value.strip().startswith('='):
        print("FAIL: E1 does not contain a formula")
        print("REWARD: 0.0")
        return 0.0

    # Parse the SUMIFS formula
    parsed = parse_sumifs_ranges(e1_value)
    if parsed is None:
        print(f"FAIL: E1 does not contain a valid SUMIFS formula: {e1_value}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Parsed SUMIFS — sum_range={parsed['sum_range']}, "
          f"criteria_range1={parsed['criteria_range1']}, criteria1={parsed['criteria1']}, "
          f"criteria_range2={parsed['criteria_range2']}, criteria2={parsed['criteria2']}")

    # Component 1 (0.4 pts): The first criteria range (Region/column A) is fixed to A2:A100
    # In initial_env this is A2:A50 — this is THE bug that needs fixing
    try:
        cr1 = parsed['criteria_range1'].upper()
        row_range = extract_row_range(cr1)
        if row_range and row_range == (2, 100):
            print(f"PASS: Component 1 — criteria_range1 is {cr1}, rows 2-100 as required (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — criteria_range1 is {cr1}, expected rows 2-100 (found {row_range})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2 (0.3 pts): All three ranges have consistent row spans (2:100)
    # sum_range=D2:D100, criteria_range1=A2:A100, criteria_range2=B2:B100
    try:
        ranges_to_check = [
            ('sum_range', parsed['sum_range']),
            ('criteria_range1', parsed['criteria_range1']),
            ('criteria_range2', parsed['criteria_range2']),
        ]
        mismatched = [name for name, rng in ranges_to_check
                      if extract_row_range(rng.upper()) != (2, 100)]
        if not mismatched:
            print(f"PASS: Component 2 — All three ranges use rows 2-100 consistently (0.3 pts)")
            total_score += 0.3
        else:
            for name in mismatched:
                rng = dict(ranges_to_check)[name]
                rr = extract_row_range(rng.upper())
                print(f"FAIL: Component 2 — {name}={rng} has rows {rr}, expected (2, 100)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3 (0.3 pts): The complete corrected formula matches expected form
    # Expected: =SUMIFS(D2:D100,A2:A100,"East",B2:B100,">1000")
    try:
        normalized = e1_value.upper().replace(" ", "")
        expected = '=SUMIFS(D2:D100,A2:A100,"EAST",B2:B100,">1000")'
        if normalized == expected:
            print(f"PASS: Component 3 — Complete formula matches expected form (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Formula: {e1_value}")
            print(f"       Expected: =SUMIFS(D2:D100,A2:A100,\"East\",B2:B100,\">1000\")")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved state
persist_app_state("libreoffice_calc")

# Execute verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
