"""
Reward Script: Bank Reconciliation Report PDF
Task ID: pdf_fin_055
Domain: pdf (libreoffice_calc in config, but task is PDF generation)
Scoring:
  Component 1 (0.20): PDF exists and has proper structure (title + 2 sections)
  Component 2 (0.20): Bank side values correct (balance, deposits total, checks total, adjusted)
  Component 3 (0.20): Book side values correct (book balance, fees, NSF, adjusted)
  Component 4 (0.20): Individual deposit-in-transit items (3 items listed)
  Component 5 (0.20): Individual outstanding check items (5 items listed)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_055'
FILE_PATH = os.path.join(WORKDIR, 'finance', 'bank_recon_march.pdf')


def extract_amounts(text):
    """Extract all dollar amounts from text as floats."""
    pattern = r'\$[\d,]+\.\d{2}'
    matches = re.findall(pattern, text)
    return [float(m.replace('$', '').replace(',', '')) for m in matches]


def verify_task(file_path):
    """
    Verify bank reconciliation report PDF with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract full text from all pages
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"
    doc.close()

    # Normalize whitespace for easier matching
    text_lower = full_text.lower()

    # Component 1: PDF structure - title + bank/book sections (0.20 points)
    try:
        has_title = "bank reconciliation" in text_lower
        has_bank_side = "bank statement balance" in text_lower or "bank side" in text_lower
        has_book_side = "book balance" in text_lower or "book side" in text_lower
        has_adjusted_bank = "adjusted bank balance" in text_lower
        has_adjusted_book = "adjusted book balance" in text_lower

        struct_checks = sum([has_title, has_bank_side, has_book_side, has_adjusted_bank, has_adjusted_book])
        if struct_checks >= 4:
            print(f"PASS: Component 1 — PDF structure verified ({struct_checks}/5 sections found) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Only {struct_checks}/5 structural elements found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Bank side values (0.20 points)
    # Bank Statement Balance: $45,230.15
    # Total Deposits in Transit: $8,500.00
    # Total Outstanding Checks: $6,120.50
    # Adjusted Bank Balance: $47,609.65
    try:
        all_amounts = extract_amounts(full_text)

        has_bank_balance = 45230.15 in all_amounts
        has_deposit_total = 8500.00 in all_amounts
        has_checks_total = 6120.50 in all_amounts
        has_adjusted_bank = 47609.65 in all_amounts

        bank_checks = sum([has_bank_balance, has_deposit_total, has_checks_total, has_adjusted_bank])
        if bank_checks == 4:
            print(f"PASS: Component 2 — All 4 bank-side values correct (0.20 pts)")
            total_score += 0.20
        elif bank_checks >= 2:
            partial = round(0.20 * bank_checks / 4, 2)
            print(f"PARTIAL: Component 2 — {bank_checks}/4 bank-side values found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {bank_checks}/4 bank-side values found. Amounts in PDF: {all_amounts[:15]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Book side values (0.20 points)
    # Book Balance: $48,109.65
    # Bank Fees: $50.00
    # NSF Check: $450.00
    # Adjusted Book Balance: $47,609.65 (already counted in bank side, but check context)
    try:
        has_book_balance = 48109.65 in all_amounts
        has_bank_fees = 50.00 in all_amounts
        has_nsf_check = 450.00 in all_amounts
        # Check both adjusted balances match
        adjusted_count = all_amounts.count(47609.65)
        both_adjusted_match = adjusted_count >= 2

        book_checks = sum([has_book_balance, has_bank_fees, has_nsf_check, both_adjusted_match])
        if book_checks == 4:
            print(f"PASS: Component 3 — All 4 book-side values correct, both adjusted balances match (0.20 pts)")
            total_score += 0.20
        elif book_checks >= 2:
            partial = round(0.20 * book_checks / 4, 2)
            print(f"PARTIAL: Component 3 — {book_checks}/4 book-side values found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {book_checks}/4 book-side values. Book bal={has_book_balance}, fees={has_bank_fees}, nsf={has_nsf_check}, match={both_adjusted_match}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Deposits in Transit - 3 individual items listed (0.20 points)
    try:
        # Look for deposit amounts: $3,200.00, $2,800.00, $2,500.00
        has_dep1 = 3200.00 in all_amounts
        has_dep2 = 2800.00 in all_amounts
        has_dep3 = 2500.00 in all_amounts

        # Also verify "deposits in transit" section exists
        has_deposit_section = "deposit" in text_lower and "transit" in text_lower

        dep_items = sum([has_dep1, has_dep2, has_dep3])
        if dep_items == 3 and has_deposit_section:
            print(f"PASS: Component 4 — All 3 deposit-in-transit items found (0.20 pts)")
            total_score += 0.20
        elif dep_items >= 1:
            partial = round(0.20 * dep_items / 3, 2)
            print(f"PARTIAL: Component 4 — {dep_items}/3 deposit items found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No deposit-in-transit items found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Outstanding Checks - 5 individual items listed (0.20 points)
    try:
        # Look for check amounts: $1,245.00, $890.50, $1,500.00, $1,235.00, $1,250.00
        has_chk1 = 1245.00 in all_amounts
        has_chk2 = 890.50 in all_amounts
        has_chk3 = 1500.00 in all_amounts
        has_chk4 = 1235.00 in all_amounts
        has_chk5 = 1250.00 in all_amounts

        # Also verify "outstanding checks" section exists
        has_check_section = "outstanding" in text_lower and "check" in text_lower

        chk_items = sum([has_chk1, has_chk2, has_chk3, has_chk4, has_chk5])
        if chk_items == 5 and has_check_section:
            print(f"PASS: Component 5 — All 5 outstanding check items found (0.20 pts)")
            total_score += 0.20
        elif chk_items >= 1:
            partial = round(0.20 * chk_items / 5, 2)
            print(f"PARTIAL: Component 5 — {chk_items}/5 check items found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No outstanding check items found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
