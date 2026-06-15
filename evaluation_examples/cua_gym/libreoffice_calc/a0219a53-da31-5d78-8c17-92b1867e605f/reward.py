"""
Reward Script: Set up named ranges for customer segments and commission rate table,
               then update summary formulas to use named ranges.
Task ID: calc_sales_customer_named_ranges_025
Domain: libreoffice_calc
Scoring:
  Component 1: Named range 'CommissionRates' defined for CommRates.$A$1:$B$5    (0.25 pts)
  Component 2: Named range(s) for Customers data defined (CustomerData/PlatinumList) (0.25 pts)
  Component 3: Summary B2 formula references a named range instead of cell refs  (0.25 pts)
  Component 4: Summary B3 formula references a named range instead of cell refs  (0.25 pts)
Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_sales_customer_named_ranges_025'


def get_defined_names(wb):
    """Return dict of {upper_name: (orig_name, destinations_list)} for all defined names."""
    result = {}
    for name, nr in wb.defined_names.items():
        result[name.upper()] = (name, list(nr.destinations))
    return result


def has_commission_rates_range(defined_names):
    """
    Check if a named range exists for CommRates sheet with 'Commission' in the name.
    Returns (found: bool, found_name: str, found_ref: str)
    """
    for upper_name, (orig_name, destinations) in defined_names.items():
        if 'COMMISSION' in upper_name or upper_name == 'COMMISSIONRATES':
            for sheet_name, ref in destinations:
                if sheet_name == 'CommRates' and 'A' in ref and 'B' in ref:
                    return (orig_name, ref)
    return None


def get_customer_ranges(defined_names):
    """
    Return list of (orig_name, ref) for named ranges covering the Customers sheet.
    """
    customer_names = {'CUSTOMERDATA', 'PLATINUMLIST', 'GOLDLIST', 'CUSTOMERLIST'}
    found = []
    for upper_name, (orig_name, destinations) in defined_names.items():
        if upper_name in customer_names or 'CUSTOMER' in upper_name or 'PLATINUM' in upper_name or 'GOLD' in upper_name:
            for sheet_name, ref in destinations:
                if sheet_name == 'Customers':
                    found.append((orig_name, ref))
                    break
    return found


def formula_uses_named_range(formula, defined_names):
    """
    Return the first named range referenced in formula, or None if none found.
    """
    if not formula or not isinstance(formula, str):
        return None
    formula_upper = formula.upper().replace(' ', '')
    for upper_name in defined_names:
        if upper_name in formula_upper:
            return defined_names[upper_name][0]  # return original name
    return None


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

    # Precondition gate: required sheets must exist
    required_sheets = ['Customers', 'CommRates', 'Summary']
    for sheet in required_sheets:
        if sheet not in wb.sheetnames:
            print(f"CRITICAL: Required sheet '{sheet}' is missing. Cannot proceed.")
            print("REWARD: 0.0")
            return 0.0

    defined_names = get_defined_names(wb)

    # Component 1: Named range 'CommissionRates' for CommRates sheet (0.25 points)
    # This FAILS on initial (no named ranges) -> PASSES on golden
    try:
        commission_result = has_commission_rates_range(defined_names)
        if commission_result is not None:
            orig_name, ref = commission_result
            print(f"PASS: Component 1 — Named range '{orig_name}' found for CommRates "
                  f"(ref: {ref}) (0.25 pts)")
            total_score += 0.25
        else:
            commrates_ranges = [(n, dests) for n, (_, dests) in defined_names.items()
                                if any(s == 'CommRates' for s, _ in dests)]
            if commrates_ranges:
                print(f"FAIL: Component 1 — Found CommRates-linked range but name doesn't include "
                      f"'Commission'. Found: {[n for n, _ in commrates_ranges]}")
            else:
                print("FAIL: Component 1 — No named range defined for CommRates sheet. "
                      "Expected 'CommissionRates' covering $A$1:$B$5.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Named range(s) for Customers data defined (0.25 points)
    # This FAILS on initial (no named ranges) -> PASSES on golden
    try:
        customer_ranges = get_customer_ranges(defined_names)
        if len(customer_ranges) >= 1:
            print(f"PASS: Component 2 — {len(customer_ranges)} named range(s) defined for "
                  f"Customers sheet: {customer_ranges} (0.25 pts)")
            total_score += 0.25
        else:
            print("FAIL: Component 2 — No named ranges defined for Customers sheet. "
                  "Expected at least 'CustomerData' (Customers.$A$1:$F$201) or "
                  "'PlatinumList' (Customers.$A$2:$F$201).")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Summary B2 formula references a named range (0.25 points)
    # Initial B2: =SUMIF(Customers.E:E,"Platinum",Customers.D:D) — no named ranges
    # Golden B2: uses a defined name like CustomerData
    try:
        ws_summary = wb['Summary']
        b2_value = ws_summary['B2'].value
        b2_named_range = formula_uses_named_range(b2_value, defined_names)
        if b2_named_range is not None:
            print(f"PASS: Component 3 — Summary B2 uses named range '{b2_named_range}' "
                  f"(formula: {repr(b2_value)}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Summary B2 does not use a named range. "
                  f"Formula: {repr(b2_value)}. Expected formula to reference a defined name "
                  f"(e.g., CustomerData) instead of raw cell references.")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Summary B3 formula references a named range (0.25 points)
    # Initial B3: =SUMIF(Customers.E:E,"Gold",Customers.D:D) — no named ranges
    # Golden B3: uses a defined name like CustomerData
    try:
        ws_summary = wb['Summary']
        b3_value = ws_summary['B3'].value
        b3_named_range = formula_uses_named_range(b3_value, defined_names)
        if b3_named_range is not None:
            print(f"PASS: Component 4 — Summary B3 uses named range '{b3_named_range}' "
                  f"(formula: {repr(b3_value)}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Summary B3 does not use a named range. "
                  f"Formula: {repr(b3_value)}. Expected formula to reference a defined name "
                  f"(e.g., CustomerData) instead of raw cell references.")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
