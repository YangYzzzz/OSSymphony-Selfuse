"""
Reward Script: Create dynamic named range 'DataColumn' for column B
Task ID: calc_nrv_034
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): Named range 'DataColumn' exists
  Component 2 (0.3): Formula anchors to $B$2 as start cell
  Component 3 (0.3): Formula uses dynamic expansion (OFFSET+COUNTA or INDIRECT+COUNTA)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_034'


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_calc")
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

    # Find the 'DataColumn' defined name (case-insensitive search)
    data_column_defn = None
    for name, defn in wb.defined_names.items():
        if name.lower() == 'datacolumn':
            data_column_defn = defn
            break

    # Component 1: Named range 'DataColumn' exists (0.4 points)
    try:
        if data_column_defn is not None:
            print(f"PASS: Component 1 — Named range 'DataColumn' exists (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No named range 'DataColumn' found. Defined names: {list(wb.defined_names.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Formula anchors to $B$2 as the start cell (0.3 points)
    # The named range formula should reference B2 as the starting point
    try:
        if data_column_defn is not None:
            formula_text = data_column_defn.attr_text.upper().replace(" ", "")
            # Check for $B$2 reference (with or without sheet prefix)
            # Patterns: $B$2, SensorReadings.$B$2, Sheet1.$B$2, etc.
            has_b2_anchor = bool(re.search(r'\$B\$2', formula_text))
            if has_b2_anchor:
                print(f"PASS: Component 2 — Formula anchors to $B$2 (0.3 pts). Formula: {data_column_defn.attr_text}")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Formula does not anchor to $B$2. Formula: {data_column_defn.attr_text}")
        else:
            print(f"FAIL: Component 2 — No named range to check (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Formula uses dynamic expansion pattern (0.3 points)
    # Valid patterns:
    #   OFFSET($B$2, 0, 0, COUNTA($B:$B)-1, 1)
    #   $B$2:INDIRECT("B"&COUNTA($B:$B)+1)
    #   Any formula combining OFFSET or INDIRECT with COUNTA for dynamic sizing
    try:
        if data_column_defn is not None:
            formula_text = data_column_defn.attr_text.upper().replace(" ", "")
            has_counta = 'COUNTA(' in formula_text
            has_offset = 'OFFSET(' in formula_text
            has_indirect = 'INDIRECT(' in formula_text

            if has_counta and (has_offset or has_indirect):
                print(f"PASS: Component 3 — Formula uses dynamic expansion (COUNTA + {'OFFSET' if has_offset else 'INDIRECT'}) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Formula lacks dynamic expansion pattern (need COUNTA + OFFSET/INDIRECT). Formula: {data_column_defn.attr_text}")
        else:
            print(f"FAIL: Component 3 — No named range to check (depends on Component 1)")
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
