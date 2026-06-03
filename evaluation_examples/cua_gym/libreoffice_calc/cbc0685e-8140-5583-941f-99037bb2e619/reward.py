"""
Reward Script: Define named range 'PrintArea_Report' for A1:G30 and set as print range
Task ID: calc_nrv_014
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): Named range 'PrintArea_Report' exists and references $A$1:$G$30
  Component 2 (0.3): Sheet print area is set to $A$1:$G$30
  Component 3 (0.3): Named range and print area are consistent (both cover A1:G30)
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_014'


def normalize_range_ref(ref_str):
    """
    Extract the cell range (e.g. '$A$1:$G$30') from a possibly sheet-qualified
    reference like "'Financial Report'!$A$1:$G$30".
    Returns the cell range portion in uppercase without dollar signs for comparison.
    """
    if not ref_str:
        return ''
    # Remove sheet qualifier (anything up to and including '!')
    if '!' in ref_str:
        ref_str = ref_str.split('!')[-1]
    # Remove dollar signs and uppercase
    return ref_str.replace('$', '').upper().strip()


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

    named_range_ref = None
    print_area_ref = None

    # Component 1: Named range 'PrintArea_Report' exists and references $A$1:$G$30 (0.4 points)
    try:
        defined_names = dict(wb.defined_names)
        if 'PrintArea_Report' in defined_names:
            defn = defined_names['PrintArea_Report']
            raw_ref = defn.attr_text
            named_range_ref = normalize_range_ref(raw_ref)
            expected_range = 'A1:G30'
            if named_range_ref == expected_range:
                print(f"PASS: Component 1 — Named range 'PrintArea_Report' found with correct reference: {raw_ref} (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — Named range 'PrintArea_Report' exists but references '{raw_ref}' (normalized: '{named_range_ref}'), expected A1:G30")
        else:
            # Check case-insensitive
            ci_match = next(
                ((name, defn) for name, defn in defined_names.items()
                 if name.lower() == 'printarea_report'),
                None
            )
            if ci_match is not None:
                ci_name, ci_defn = ci_match
                raw_ref = ci_defn.attr_text
                named_range_ref = normalize_range_ref(raw_ref)
                expected_range = 'A1:G30'
                if named_range_ref == expected_range:
                    print(f"PASS: Component 1 — Named range '{ci_name}' found (case-insensitive match) with correct reference: {raw_ref} (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 1 — Named range '{ci_name}' exists but references '{raw_ref}' (normalized: '{named_range_ref}'), expected A1:G30")
            else:
                print(f"FAIL: Component 1 — No named range 'PrintArea_Report' found. Defined names: {list(defined_names.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Print area is set to $A$1:$G$30 (0.3 points)
    try:
        ws = wb.active
        raw_print_area = ws.print_area
        if raw_print_area:
            print_area_ref = normalize_range_ref(raw_print_area)
            expected_range = 'A1:G30'
            if print_area_ref == expected_range:
                print(f"PASS: Component 2 — Print area set to '{raw_print_area}' (normalized: '{print_area_ref}') (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Print area is '{raw_print_area}' (normalized: '{print_area_ref}'), expected A1:G30")
        else:
            print(f"FAIL: Component 2 — No print area set on active sheet '{ws.title}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Named range and print area are consistent — both cover A1:G30 (0.3 points)
    # This verifies the task was done cohesively: named range defined AND used as print area
    try:
        if named_range_ref and print_area_ref:
            if named_range_ref == 'A1:G30' and print_area_ref == 'A1:G30':
                print(f"PASS: Component 3 — Named range and print area are consistent, both reference A1:G30 (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Inconsistent: named range='{named_range_ref}', print area='{print_area_ref}'")
        else:
            missing = []
            if not named_range_ref:
                missing.append("named range not found or incorrect")
            if not print_area_ref:
                missing.append("print area not set or incorrect")
            print(f"FAIL: Component 3 — Cannot verify consistency: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
