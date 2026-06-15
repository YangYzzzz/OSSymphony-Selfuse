"""
Reward Script: Fix conditional formatting range from entire column A to A2:A100
Task ID: calc_tbl_026
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): CF range is exactly A2:A100 (not entire column)
  Component 2 (0.3): Exactly 1 CF rule total (no duplicates)
  Component 3 (0.3): Rule formula correctly references A2 (not A1)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_tbl_026'


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
    Verify that conditional formatting on column A has been fixed:
    - Range narrowed from A1:A1048576 to A2:A100
    - Duplicate rules removed (only 1 rule remains)
    - Formula correctly references A2 (the start of the data range)

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Employees']

    # Collect all CF entries that apply to column A
    cf_list = list(ws.conditional_formatting)

    # Find CF entries that involve column A ranges
    col_a_cfs = []
    for cf in cf_list:
        range_str = str(cf)
        # Check if any range in this CF touches column A
        # Ranges like "A2:A100", "A1:A1048576", etc.
        if 'A' in range_str:
            col_a_cfs.append(cf)

    print(f"INFO: Total CF entries: {len(cf_list)}, Column-A CF entries: {len(col_a_cfs)}")
    for i, cf in enumerate(col_a_cfs):
        print(f"  CF {i}: range='{cf}', rules={len(cf.rules)}")
        for j, rule in enumerate(cf.rules):
            print(f"    Rule {j}: type={rule.type}, formula={getattr(rule, 'formula', None)}")

    # Component 1: CF range is exactly A2:A100 (0.4 points)
    # The initial state has A1:A1048576 (entire column). The fix narrows it to A2:A100.
    # This FAILS on initial (range is A1:A1048576), PASSES on golden (range is A2:A100).
    try:
        found_correct_range = False
        found_broad_range = False

        for cf in col_a_cfs:
            # cf.sqref gives the CellRange; str(cf) wraps it in <ConditionalFormatting ...>
            # Extract the actual range string from the sqref attribute
            range_str = str(cf.sqref).strip().upper() if hasattr(cf, 'sqref') else str(cf).upper()
            # Fallback: parse from repr if needed
            if '<' in range_str:
                import re
                m = re.search(r'A\d+:A\d+', range_str)
                range_str = m.group(0) if m else range_str

            print(f"  Parsed range: '{range_str}'")
            # Check for the correct narrow range
            if range_str == 'A2:A100':
                found_correct_range = True
            # Check for overly broad ranges (entire column or very large)
            if 'A1:A1048576' in range_str or range_str == 'A:A':
                found_broad_range = True

        if found_correct_range and not found_broad_range:
            print(f"PASS: Component 1 -- CF range is A2:A100, no broad range found (0.4 pts)")
            total_score += 0.4
        elif found_correct_range and found_broad_range:
            print(f"FAIL: Component 1 -- A2:A100 found but broad range still exists")
        elif found_broad_range:
            print(f"FAIL: Component 1 -- Broad range (entire column) still present")
        else:
            # Check if there's any CF at all
            if len(col_a_cfs) == 0:
                print(f"FAIL: Component 1 -- No conditional formatting found on column A")
            else:
                ranges = [str(cf) for cf in col_a_cfs]
                print(f"FAIL: Component 1 -- Expected range A2:A100, found: {ranges}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Exactly 1 CF rule total on column A (no duplicates) (0.3 points)
    # Initial state has 2 duplicate rules. Golden has exactly 1.
    # This FAILS on initial (2 rules), PASSES on golden (1 rule).
    try:
        total_rules = sum(len(cf.rules) for cf in col_a_cfs)
        if len(col_a_cfs) == 1 and total_rules == 1:
            print(f"PASS: Component 2 -- Exactly 1 CF entry with 1 rule (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- Expected 1 CF entry with 1 rule, found {len(col_a_cfs)} entries with {total_rules} total rules")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Rule formula correctly references A2 (not A1) (0.3 points)
    # Initial state formula references A1 (for entire column). Golden references A2 (data start).
    # This FAILS on initial (formula refs A1), PASSES on golden (formula refs A2).
    try:
        formula_correct = False
        for cf in col_a_cfs:
            for rule in cf.rules:
                formulas = getattr(rule, 'formula', None)
                if formulas:
                    for f in formulas:
                        f_upper = f.upper().replace(' ', '')
                        # The correct formula should reference A2, not A1
                        # Expected: ISNUMBER(SEARCH("son",A2))
                        if 'A2' in f_upper and 'SEARCH' in f_upper and 'ISNUMBER' in f_upper:
                            formula_correct = True
                            print(f"  Found correct formula: {f}")

        if formula_correct:
            print(f"PASS: Component 3 -- Formula correctly references A2 (0.3 pts)")
            total_score += 0.3
        else:
            # Show what formulas exist
            all_formulas = []
            for cf in col_a_cfs:
                for rule in cf.rules:
                    if getattr(rule, 'formula', None):
                        all_formulas.extend(rule.formula)
            print(f"FAIL: Component 3 -- Expected formula referencing A2, found: {all_formulas}")
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
