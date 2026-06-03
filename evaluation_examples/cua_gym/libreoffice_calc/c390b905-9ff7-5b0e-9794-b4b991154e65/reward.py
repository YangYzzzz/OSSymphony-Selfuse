"""
Reward Script: Extract billing amounts and due dates from PDFs and enter into bills_tracker.xlsx
Task ID: osworld_multi_apps_receipt_to_calc_003
Domain: libreoffice_calc
Scoring:
  - Component 1: Three new rows added for current month (March) with all 3 utilities (0.30 pts)
  - Component 2: Electric bill row has correct amount (127.45) and due date (2026-03-25) (0.25 pts)
  - Component 3: Water bill row has correct amount (43.8) and due date (2026-03-28) (0.25 pts)
  - Component 4: Internet bill row has correct amount (89.99) and due date (2026-03-22) (0.20 pts)
Total: 1.0
"""

import os
import openpyxl
from datetime import datetime

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_receipt_to_calc_003'

# Ground truth values from context/golden state
EXPECTED_MONTH = 'March'
EXPECTED_BILLS = {
    'Electric': {'amount': 127.45, 'due_date': '2026-03-25', 'paid': 'No'},
    'Water':    {'amount': 43.8,   'due_date': '2026-03-28', 'paid': 'No'},
    'Internet': {'amount': 89.99,  'due_date': '2026-03-22', 'paid': 'No'},
}


def normalize_date(val):
    """Convert various date formats to 'YYYY-MM-DD' string for comparison."""
    if val is None:
        return None
    if isinstance(val, datetime):
        return val.strftime('%Y-%m-%d')
    s = str(val).strip()
    # Try common date formats
    for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%B %d, %Y', '%b %d, %Y'):
        try:
            return datetime.strptime(s, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return s


def normalize_amount(val):
    """Convert amount to float, stripping currency symbols."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace('$', '').replace(',', '')
    try:
        return float(s)
    except ValueError:
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that 3 new rows for March bills were added to the spreadsheet
    with correct utility names, amounts, due dates, and Paid status.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load workbook - fail fast if unreadable
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get active sheet (expected: 'Bills')
    try:
        ws = wb.active
        if ws is None:
            print("CRITICAL: No active sheet found.")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot access sheet: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------
    # Pre-scan: collect all rows that belong to EXPECTED_MONTH
    # We look for utility name in column B, matching rows by month in col A
    # -------------------------------------------------------------------
    march_rows = {}  # utility_name -> row dict {amount, due_date, paid}

    try:
        for row in ws.iter_rows(min_row=2, values_only=True):
            month_val, utility_val, amount_val, date_val, paid_val = row[:5]
            if month_val is None:
                continue
            month_str = str(month_val).strip()
            if month_str.lower() == EXPECTED_MONTH.lower():
                if utility_val is not None:
                    utility_str = str(utility_val).strip()
                    march_rows[utility_str] = {
                        'amount': normalize_amount(amount_val),
                        'due_date': normalize_date(date_val),
                        'paid': str(paid_val).strip() if paid_val is not None else None,
                    }
    except Exception as e:
        print(f"ERROR: Could not scan rows: {e}")

    # -------------------------------------------------------------------
    # Component 1: Three new rows for current month (March) with all 3 utilities (0.30 pts)
    # This FAILS on initial (no March rows) and PASSES on golden (3 March rows)
    # -------------------------------------------------------------------
    try:
        expected_utilities = set(EXPECTED_BILLS.keys())
        found_utilities = set(march_rows.keys()) & expected_utilities
        if len(found_utilities) == 3:
            print(f"PASS: Component 1 — all 3 March utility rows found: {sorted(found_utilities)} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — expected 3 March utility rows (Electric, Water, Internet), "
                  f"found {len(found_utilities)}: {sorted(found_utilities)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------
    # Component 2: Electric bill — correct amount (127.45) and due date (2026-03-25) (0.25 pts)
    # FAILS on initial (no Electric March row) and PASSES on golden
    # -------------------------------------------------------------------
    try:
        electric = march_rows.get('Electric')
        if electric is None:
            print("FAIL: Component 2 — Electric bill row for March not found")
        else:
            amount_ok = (electric['amount'] is not None and
                         abs(electric['amount'] - EXPECTED_BILLS['Electric']['amount']) < 0.01)
            date_ok = (electric['due_date'] == EXPECTED_BILLS['Electric']['due_date'])
            paid_ok = (electric['paid'] is not None and
                       electric['paid'].lower() == EXPECTED_BILLS['Electric']['paid'].lower())
            if amount_ok and date_ok and paid_ok:
                print(f"PASS: Component 2 — Electric bill: amount={electric['amount']}, "
                      f"due_date={electric['due_date']}, paid={electric['paid']} (0.25 pts)")
                total_score += 0.25
            else:
                details = []
                if not amount_ok:
                    details.append(f"amount expected=127.45, got={electric['amount']}")
                if not date_ok:
                    details.append(f"due_date expected=2026-03-25, got={electric['due_date']}")
                if not paid_ok:
                    details.append(f"paid expected=No, got={electric['paid']}")
                print(f"FAIL: Component 2 — Electric bill issues: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------
    # Component 3: Water bill — correct amount (43.8) and due date (2026-03-28) (0.25 pts)
    # FAILS on initial (no Water March row) and PASSES on golden
    # -------------------------------------------------------------------
    try:
        water = march_rows.get('Water')
        if water is None:
            print("FAIL: Component 3 — Water bill row for March not found")
        else:
            amount_ok = (water['amount'] is not None and
                         abs(water['amount'] - EXPECTED_BILLS['Water']['amount']) < 0.01)
            date_ok = (water['due_date'] == EXPECTED_BILLS['Water']['due_date'])
            paid_ok = (water['paid'] is not None and
                       water['paid'].lower() == EXPECTED_BILLS['Water']['paid'].lower())
            if amount_ok and date_ok and paid_ok:
                print(f"PASS: Component 3 — Water bill: amount={water['amount']}, "
                      f"due_date={water['due_date']}, paid={water['paid']} (0.25 pts)")
                total_score += 0.25
            else:
                details = []
                if not amount_ok:
                    details.append(f"amount expected=43.8, got={water['amount']}")
                if not date_ok:
                    details.append(f"due_date expected=2026-03-28, got={water['due_date']}")
                if not paid_ok:
                    details.append(f"paid expected=No, got={water['paid']}")
                print(f"FAIL: Component 3 — Water bill issues: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------
    # Component 4: Internet bill — correct amount (89.99) and due date (2026-03-22) (0.20 pts)
    # FAILS on initial (no Internet March row) and PASSES on golden
    # -------------------------------------------------------------------
    try:
        internet = march_rows.get('Internet')
        if internet is None:
            print("FAIL: Component 4 — Internet bill row for March not found")
        else:
            amount_ok = (internet['amount'] is not None and
                         abs(internet['amount'] - EXPECTED_BILLS['Internet']['amount']) < 0.01)
            date_ok = (internet['due_date'] == EXPECTED_BILLS['Internet']['due_date'])
            paid_ok = (internet['paid'] is not None and
                       internet['paid'].lower() == EXPECTED_BILLS['Internet']['paid'].lower())
            if amount_ok and date_ok and paid_ok:
                print(f"PASS: Component 4 — Internet bill: amount={internet['amount']}, "
                      f"due_date={internet['due_date']}, paid={internet['paid']} (0.20 pts)")
                total_score += 0.20
            else:
                details = []
                if not amount_ok:
                    details.append(f"amount expected=89.99, got={internet['amount']}")
                if not date_ok:
                    details.append(f"due_date expected=2026-03-22, got={internet['due_date']}")
                if not paid_ok:
                    details.append(f"paid expected=No, got={internet['paid']}")
                print(f"FAIL: Component 4 — Internet bill issues: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Canonical file path on the VM
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
