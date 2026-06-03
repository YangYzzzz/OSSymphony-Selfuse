"""
Reward Script: Edit named range 'Expenses' to expand from C2:C10 to C2:C15
Task ID: calc_cop_named_range_003
Domain: libreoffice_calc

Scoring Rubric:
  Component 1 (0.7 pts): Named range 'Expenses' refers to Budget!$C$2:$C$15
                          (the core task: expanding from C2:C10 to C2:C15)
  Component 2 (0.3 pts): Named range 'Expenses' correctly expanded AND
                          Revenue/NetProfit named ranges remain unchanged
                          (compound check — only awarded when Expenses was also updated)
  Total: 1.0

  NOTE on Component 2: This is a COMPOUND check requiring Expenses = C2:C15 FIRST.
  Revenue and NetProfit being unchanged is verified only to confirm no accidental
  corruption occurred during the required Expenses edit. Without Component 1 passing,
  Component 2 cannot be awarded.
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_cop_named_range_003'

# Expected named range definitions after task completion
EXPECTED_EXPENSES = 'Budget!$C$2:$C$15'
EXPECTED_REVENUE = 'Budget!$B$2:$B$10'
EXPECTED_NETPROFIT = 'Budget!$D$2:$D$10'


def normalize_range(range_str):
    """Normalize a named range value for comparison."""
    return range_str.strip().upper().replace(' ', '')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: ensure file can be loaded
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: verify 'Budget' sheet exists
    if 'Budget' not in wb.sheetnames:
        print("CRITICAL: Sheet 'Budget' not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    defined_names = wb.defined_names
    expenses_updated = False

    # Component 1: Named range 'Expenses' refers to Budget!$C$2:$C$15 (0.7 points)
    # This is the core task: expanding the range from C2:C10 to C2:C15.
    # The initial file has Expenses = Budget!$C$2:$C$10, so this FAILS on initial
    # and PASSES only on golden.
    try:
        if 'Expenses' not in defined_names:
            print("FAIL: Component 1 — Named range 'Expenses' does not exist in workbook")
        else:
            expenses_defn = defined_names['Expenses']
            expenses_value = expenses_defn.value
            if normalize_range(expenses_value) == normalize_range(EXPECTED_EXPENSES):
                print(f"PASS: Component 1 — 'Expenses' named range correctly refers to '{expenses_value}' (0.7 pts)")
                total_score += 0.7
                expenses_updated = True
            else:
                print(f"FAIL: Component 1 — Expected 'Expenses' = '{EXPECTED_EXPENSES}', found '{expenses_value}'")
                print(f"      Range was not updated (initial was Budget!$C$2:$C$10, needs to be Budget!$C$2:$C$15)")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check 'Expenses' named range: {e}")

    # Component 2: 'Expenses' was correctly updated AND other named ranges are intact (0.3 points)
    # This is a COMPOUND check: only awarded when:
    #   (a) Expenses equals exactly Budget!$C$2:$C$15 (already confirmed by expenses_updated), AND
    #   (b) Revenue and NetProfit are still at their original values
    # Because this requires expenses_updated to be True, this component ALSO FAILS on the
    # initial file (where Expenses is still C2:C10). This prevents awarding points for
    # pre-existing Revenue/NetProfit values when the main task hasn't been done.
    try:
        if not expenses_updated:
            print("SKIP: Component 2 — Skipped because Expenses range was not correctly updated (Component 1 failed)")
        else:
            revenue_ok = False
            netprofit_ok = False

            if 'Revenue' not in defined_names:
                print("FAIL: Component 2 — Named range 'Revenue' missing (accidentally deleted?)")
            else:
                revenue_value = defined_names['Revenue'].value
                if normalize_range(revenue_value) == normalize_range(EXPECTED_REVENUE):
                    print(f"PASS: Component 2a — 'Revenue' named range unchanged: '{revenue_value}'")
                    revenue_ok = True
                else:
                    print(f"FAIL: Component 2a — 'Revenue' changed: expected '{EXPECTED_REVENUE}', found '{revenue_value}'")

            if 'NetProfit' not in defined_names:
                print("FAIL: Component 2 — Named range 'NetProfit' missing (accidentally deleted?)")
            else:
                netprofit_value = defined_names['NetProfit'].value
                if normalize_range(netprofit_value) == normalize_range(EXPECTED_NETPROFIT):
                    print(f"PASS: Component 2b — 'NetProfit' named range unchanged: '{netprofit_value}'")
                    netprofit_ok = True
                else:
                    print(f"FAIL: Component 2b — 'NetProfit' changed: expected '{EXPECTED_NETPROFIT}', found '{netprofit_value}'")

            if revenue_ok and netprofit_ok:
                print("PASS: Component 2 — Expenses correctly expanded AND Revenue/NetProfit are intact (0.3 pts)")
                total_score += 0.3
            elif revenue_ok or netprofit_ok:
                print("PARTIAL: Component 2 — One of Revenue/NetProfit was accidentally modified (0.15 pts)")
                total_score += 0.15
            else:
                print("FAIL: Component 2 — Both Revenue and NetProfit were accidentally modified")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check Revenue/NetProfit named ranges: {e}")

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
