"""
Reward Script: General Ledger Summary PDF
Task ID: pdf_fin_061
Domain: pdf (libreoffice_calc)
Scoring:
  Component 1: PDF exists and is readable (0.1)
  Component 2: All 8 accounts present with correct names/numbers (0.3)
  Component 3: Debit amounts correct for debit accounts (0.25)
  Component 4: Credit amounts correct for credit accounts (0.2)
  Component 5: Totals row shows balanced $348,500 (0.15)
"""

import os
import re
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    print("CRITICAL: PyMuPDF (fitz) not available")
    print("REWARD: 0.0")
    sys.exit(0)

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_061'
FILE_PATH = os.path.join(WORKDIR, 'finance', 'gl_summary_march.pdf')

# Expected accounts: (account_number, account_name, debit_amount_or_None, credit_amount_or_None)
EXPECTED_ACCOUNTS = [
    ("1000", "Cash", 125000, None),
    ("1200", "Accounts Receivable", 45800, None),
    ("1400", "Inventory", 67300, None),
    ("2000", "Accounts Payable", None, 38500),
    ("2500", "Long-term Debt", None, 100000),
    ("4000", "Revenue", None, 210000),
    ("5000", "COGS", 89400, None),
    ("6000", "Operating Expenses", 21000, None),
]

EXPECTED_TOTAL = 348500


def extract_amount(text, pattern):
    """Extract a dollar amount from text near a pattern. Returns integer or None."""
    # Find all dollar amounts in the text
    amounts = re.findall(r'\$[\d,]+(?:\.\d+)?', text)
    return amounts


def parse_amount(s):
    """Parse a dollar string like '$125,000' or '$125,000.00' to integer."""
    s = s.replace('$', '').replace(',', '').strip()
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: PDF file exists and is readable (0.1 points)
    try:
        if not os.path.exists(file_path):
            print(f"FAIL: Component 1 -- PDF file not found at {file_path}")
            print("REWARD: 0.0")
            return 0.0

        doc = fitz.open(file_path)
        if doc.page_count < 1:
            print("FAIL: Component 1 -- PDF has no pages")
            print("REWARD: 0.0")
            return 0.0

        # Extract all text from the PDF
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()

        if len(full_text.strip()) < 50:
            print(f"FAIL: Component 1 -- PDF has very little text content ({len(full_text)} chars)")
            print("REWARD: 0.0")
            return 0.0

        print(f"PASS: Component 1 -- PDF exists and has {len(full_text)} chars of text (0.1 pts)")
        total_score += 0.1
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: All 8 accounts present with correct names and numbers (0.3 points)
    try:
        accounts_found = 0
        text_upper = full_text.upper()
        text_clean = full_text

        for acct_num, acct_name, _, _ in EXPECTED_ACCOUNTS:
            # Check if account number is present
            num_present = acct_num in text_clean
            # Check if account name is present (case-insensitive)
            name_present = acct_name.upper() in text_upper
            if num_present and name_present:
                accounts_found += 1
                print(f"  Found account: {acct_num} - {acct_name}")
            else:
                print(f"  Missing account: {acct_num} - {acct_name} (num={num_present}, name={name_present})")

        if accounts_found == 8:
            print(f"PASS: Component 2 -- All 8 accounts found (0.3 pts)")
            total_score += 0.3
        elif accounts_found >= 6:
            partial = round(0.3 * (accounts_found / 8), 2)
            print(f"PARTIAL: Component 2 -- {accounts_found}/8 accounts found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- Only {accounts_found}/8 accounts found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Debit amounts correct (0.25 points)
    # Debit accounts: Cash 125000, AR 45800, Inventory 67300, COGS 89400, OpEx 21000
    try:
        debit_accounts = [(n, name, d) for n, name, d, c in EXPECTED_ACCOUNTS if d is not None]
        debit_correct = 0

        # Extract all dollar amounts from the text
        all_amounts = [parse_amount(a) for a in re.findall(r'\$[\d,]+(?:\.\d+)?', full_text)]
        all_amounts = [a for a in all_amounts if a is not None]

        for acct_num, acct_name, expected_debit in debit_accounts:
            if expected_debit in all_amounts:
                debit_correct += 1
                print(f"  Debit OK: {acct_name} = ${expected_debit:,}")
            else:
                print(f"  Debit MISSING: {acct_name} expected ${expected_debit:,}")

        if debit_correct == 5:
            print(f"PASS: Component 3 -- All 5 debit amounts correct (0.25 pts)")
            total_score += 0.25
        elif debit_correct >= 3:
            partial = round(0.25 * (debit_correct / 5), 2)
            print(f"PARTIAL: Component 3 -- {debit_correct}/5 debit amounts correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- Only {debit_correct}/5 debit amounts correct")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Credit amounts correct (0.2 points)
    # Credit accounts: AP 38500, LTD 100000, Revenue 210000
    try:
        credit_accounts = [(n, name, c) for n, name, d, c in EXPECTED_ACCOUNTS if c is not None]
        credit_correct = 0

        for acct_num, acct_name, expected_credit in credit_accounts:
            if expected_credit in all_amounts:
                credit_correct += 1
                print(f"  Credit OK: {acct_name} = ${expected_credit:,}")
            else:
                print(f"  Credit MISSING: {acct_name} expected ${expected_credit:,}")

        if credit_correct == 3:
            print(f"PASS: Component 4 -- All 3 credit amounts correct (0.2 pts)")
            total_score += 0.2
        elif credit_correct >= 2:
            partial = round(0.2 * (credit_correct / 3), 2)
            print(f"PARTIAL: Component 4 -- {credit_correct}/3 credit amounts correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- Only {credit_correct}/3 credit amounts correct")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Totals row shows balanced $348,500 (0.15 points)
    try:
        # Check that the total amount 348500 appears in the text
        # It should appear at least twice (once for total debits, once for total credits)
        total_str_variations = ["348,500", "348500"]
        total_occurrences = 0
        for var in total_str_variations:
            total_occurrences += full_text.count(var)

        # Also check for "Total" keyword
        has_total_label = "total" in full_text.lower()

        if total_occurrences >= 2 and has_total_label:
            print(f"PASS: Component 5 -- Total $348,500 appears {total_occurrences} times with Total label (0.15 pts)")
            total_score += 0.15
        elif total_occurrences >= 1 and has_total_label:
            print(f"PARTIAL: Component 5 -- Total $348,500 appears {total_occurrences} time(s), expected 2 (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 5 -- Total $348,500 not found (occurrences={total_occurrences}, label={has_total_label})")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
