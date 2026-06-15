"""
Reward Script: Cash Flow Statement PDF Verification
Task ID: pdf_fin_029
Domain: pdf
Scoring:
  - Component 1 (0.30): Operating Activities section with correct line items
  - Component 2 (0.20): Investing Activities section with correct line items
  - Component 3 (0.20): Financing Activities section with correct line items
  - Component 4 (0.15): Correct subtotals and net change in cash
  - Component 5 (0.15): Correct beginning and ending cash balances
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_029'
FILE_PATH = os.path.join(WORKDIR, 'finance', 'cashflow_q4_2024.pdf')


def normalize_text(text):
    """Normalize whitespace for easier matching."""
    return re.sub(r'\s+', ' ', text).strip()


def check_text_contains(text, target):
    """Case-insensitive check if target appears in text."""
    return target.lower() in text.lower()


def extract_dollar_values(text):
    """Extract all dollar values from text, returning them as floats.
    Handles $500,000, ($45,000), $1,200,000, $1,440,000, etc."""
    values = {}
    # Match patterns like $500,000 or ($45,000) or -$200,000
    # We'll store them keyed by surrounding context
    return text


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: File must exist and be a valid PDF
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all text from the PDF
    try:
        all_text = ""
        for page in doc:
            all_text += page.get_text("text") + "\n"
        doc.close()
    except Exception as e:
        print(f"CRITICAL: Cannot extract text from PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    text_norm = normalize_text(all_text)

    # Component 1: Operating Activities section (0.30 points)
    # Must contain: Net Income $500K, Depreciation +$80K, AR Change -$45K, AP Change +$30K
    try:
        op_checks = 0
        op_total = 4

        # Check for Net Income $500,000
        if check_text_contains(text_norm, "Net Income") and re.search(r'500[,.]?000', all_text):
            op_checks += 1
            print("PASS: Operating - Net Income $500,000 found")
        else:
            print("FAIL: Operating - Net Income $500,000 not found")

        # Check for Depreciation $80,000
        if (check_text_contains(text_norm, "Depreciation") or check_text_contains(text_norm, "Deprec")) and re.search(r'80[,.]?000', all_text):
            op_checks += 1
            print("PASS: Operating - Depreciation $80,000 found")
        else:
            print("FAIL: Operating - Depreciation $80,000 not found")

        # Check for Accounts Receivable change ($45,000)
        if (check_text_contains(text_norm, "Receivable") or check_text_contains(text_norm, "AR")) and re.search(r'45[,.]?000', all_text):
            op_checks += 1
            print("PASS: Operating - AR Change $45,000 found")
        else:
            print("FAIL: Operating - AR Change $45,000 not found")

        # Check for Accounts Payable change $30,000
        if (check_text_contains(text_norm, "Payable") or check_text_contains(text_norm, "AP")) and re.search(r'30[,.]?000', all_text):
            op_checks += 1
            print("PASS: Operating - AP Change $30,000 found")
        else:
            print("FAIL: Operating - AP Change $30,000 not found")

        if op_checks == op_total:
            print(f"PASS: Component 1 - All operating items present (0.30 pts)")
            total_score += 0.30
        elif op_checks > 0:
            partial = round(0.30 * (op_checks / op_total), 2)
            print(f"PARTIAL: Component 1 - {op_checks}/{op_total} operating items ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 1 - No operating items found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Investing Activities section (0.20 points)
    # Must contain: Equipment Purchase -$200K, Investment Sales +$50K
    try:
        inv_checks = 0
        inv_total = 2

        # Equipment Purchase $200,000
        if check_text_contains(text_norm, "Equipment") and re.search(r'200[,.]?000', all_text):
            inv_checks += 1
            print("PASS: Investing - Equipment Purchase $200,000 found")
        else:
            print("FAIL: Investing - Equipment Purchase $200,000 not found")

        # Investment Sales $50,000
        if check_text_contains(text_norm, "Investment") and re.search(r'50[,.]?000', all_text):
            inv_checks += 1
            print("PASS: Investing - Investment Sales $50,000 found")
        else:
            print("FAIL: Investing - Investment Sales $50,000 not found")

        if inv_checks == inv_total:
            print(f"PASS: Component 2 - All investing items present (0.20 pts)")
            total_score += 0.20
        elif inv_checks > 0:
            partial = round(0.20 * (inv_checks / inv_total), 2)
            print(f"PARTIAL: Component 2 - {inv_checks}/{inv_total} investing items ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 2 - No investing items found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Financing Activities section (0.20 points)
    # Must contain: Loan Repayment -$100K, Dividends -$75K
    try:
        fin_checks = 0
        fin_total = 2

        # Loan Repayment $100,000
        if check_text_contains(text_norm, "Loan") and re.search(r'100[,.]?000', all_text):
            fin_checks += 1
            print("PASS: Financing - Loan Repayment $100,000 found")
        else:
            print("FAIL: Financing - Loan Repayment $100,000 not found")

        # Dividends $75,000
        if check_text_contains(text_norm, "Dividend") and re.search(r'75[,.]?000', all_text):
            fin_checks += 1
            print("PASS: Financing - Dividends $75,000 found")
        else:
            print("FAIL: Financing - Dividends $75,000 not found")

        if fin_checks == fin_total:
            print(f"PASS: Component 3 - All financing items present (0.20 pts)")
            total_score += 0.20
        elif fin_checks > 0:
            partial = round(0.20 * (fin_checks / fin_total), 2)
            print(f"PARTIAL: Component 3 - {fin_checks}/{fin_total} financing items ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 3 - No financing items found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Correct subtotals and net change (0.15 points)
    # Operating total $565,000, Investing total -$150,000, Financing total -$175,000, Net change $240,000
    try:
        sub_checks = 0
        sub_total = 4

        if re.search(r'565[,.]?000', all_text):
            sub_checks += 1
            print("PASS: Subtotal - Operating total $565,000 found")
        else:
            print("FAIL: Subtotal - Operating total $565,000 not found")

        if re.search(r'150[,.]?000', all_text):
            sub_checks += 1
            print("PASS: Subtotal - Investing total ($150,000) found")
        else:
            print("FAIL: Subtotal - Investing total ($150,000) not found")

        if re.search(r'175[,.]?000', all_text):
            sub_checks += 1
            print("PASS: Subtotal - Financing total ($175,000) found")
        else:
            print("FAIL: Subtotal - Financing total ($175,000) not found")

        if re.search(r'240[,.]?000', all_text):
            sub_checks += 1
            print("PASS: Subtotal - Net change $240,000 found")
        else:
            print("FAIL: Subtotal - Net change $240,000 not found")

        if sub_checks == sub_total:
            print(f"PASS: Component 4 - All subtotals correct (0.15 pts)")
            total_score += 0.15
        elif sub_checks > 0:
            partial = round(0.15 * (sub_checks / sub_total), 2)
            print(f"PARTIAL: Component 4 - {sub_checks}/{sub_total} subtotals ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 4 - No subtotals found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Beginning and ending cash balances (0.15 points)
    # Beginning: $1,200,000, Ending: $1,440,000
    try:
        bal_checks = 0
        bal_total = 2

        # Beginning cash $1,200,000
        if check_text_contains(text_norm, "Beginning") and re.search(r'1[,.]?200[,.]?000', all_text):
            bal_checks += 1
            print("PASS: Balance - Beginning cash $1,200,000 found")
        else:
            print("FAIL: Balance - Beginning cash $1,200,000 not found")

        # Ending cash $1,440,000
        if check_text_contains(text_norm, "Ending") and re.search(r'1[,.]?440[,.]?000', all_text):
            bal_checks += 1
            print("PASS: Balance - Ending cash $1,440,000 found")
        else:
            print("FAIL: Balance - Ending cash $1,440,000 not found")

        if bal_checks == bal_total:
            print(f"PASS: Component 5 - Both balances correct (0.15 pts)")
            total_score += 0.15
        elif bal_checks > 0:
            partial = round(0.15 * (bal_checks / bal_total), 2)
            print(f"PARTIAL: Component 5 - {bal_checks}/{bal_total} balances ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 5 - No balances found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

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
