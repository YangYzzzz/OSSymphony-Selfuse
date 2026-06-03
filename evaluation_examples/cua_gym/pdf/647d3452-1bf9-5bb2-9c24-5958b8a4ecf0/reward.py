"""
Reward Script: Analyze invoice_batch.pdf and write invoice_summary.txt
Task ID: pdf_cr_063
Domain: pdf
Scoring:
  Component 1 (0.25): invoice_summary.txt exists and contains all 5 invoice numbers
  Component 2 (0.25): All 5 invoice totals are correctly extracted
  Component 3 (0.15): Page numbers correctly associated with each invoice
  Component 4 (0.15): Total invoices count line present and correct
  Component 5 (0.20): Grand total line present and correct
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_063'

# Ground truth from golden state
EXPECTED_INVOICES = {
    '1047': {'page': 1, 'total': 29444.00},
    '1048': {'page': 2, 'total': 33745.66},
    '1053': {'page': 3, 'total': 34478.12},
    '1061': {'page': 4, 'total': 45681.50},
    '1072': {'page': 5, 'total': 41012.50},
}
EXPECTED_COUNT = 5
EXPECTED_GRAND_TOTAL = 184361.78


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist (not scored, but required)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    lines = content.strip().split('\n')

    # Component 1: All 5 invoice numbers are listed (0.25 points)
    # Check that each expected invoice number appears in the text
    try:
        found_invoices = set()
        for inv_num in EXPECTED_INVOICES:
            # Look for the invoice number pattern (e.g., #1047 or 1047)
            if re.search(r'#?' + inv_num, content):
                found_invoices.add(inv_num)

        invoice_ratio = len(found_invoices) / len(EXPECTED_INVOICES)
        if invoice_ratio == 1.0:
            print(f"PASS: Component 1 — All 5 invoice numbers found: {sorted(found_invoices)} (0.25 pts)")
            total_score += 0.25
        elif invoice_ratio > 0:
            partial = round(0.25 * invoice_ratio, 3)
            print(f"PARTIAL: Component 1 — {len(found_invoices)}/5 invoice numbers found: {sorted(found_invoices)} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No invoice numbers found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 5 invoice totals correctly extracted (0.25 points)
    # Look for dollar amounts associated with each invoice
    try:
        correct_totals = 0
        for inv_num, info in EXPECTED_INVOICES.items():
            expected_total = info['total']
            # Find lines mentioning this invoice number
            inv_pattern = re.compile(r'.*#?' + inv_num + r'.*', re.IGNORECASE)
            for line in lines:
                if inv_pattern.match(line):
                    # Extract dollar amounts from this line
                    amounts = re.findall(r'\$?([\d,]+\.?\d*)', line)
                    for amt_str in amounts:
                        amt_val = float(amt_str.replace(',', ''))
                        if abs(amt_val - expected_total) < 0.01:
                            correct_totals += 1
                            break
                    break  # Only check first matching line per invoice

        total_ratio = correct_totals / len(EXPECTED_INVOICES)
        if total_ratio == 1.0:
            print(f"PASS: Component 2 — All 5 invoice totals correct (0.25 pts)")
            total_score += 0.25
        elif total_ratio > 0:
            partial = round(0.25 * total_ratio, 3)
            print(f"PARTIAL: Component 2 — {correct_totals}/5 totals correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No correct totals found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page numbers correctly associated with invoices (0.15 points)
    # Each invoice line should mention the correct page number
    try:
        correct_pages = 0
        for inv_num, info in EXPECTED_INVOICES.items():
            expected_page = info['page']
            inv_pattern = re.compile(r'.*#?' + inv_num + r'.*', re.IGNORECASE)
            for line in lines:
                if inv_pattern.match(line):
                    # Look for page number
                    page_match = re.search(r'[Pp]age\s*(\d+)', line)
                    if page_match and int(page_match.group(1)) == expected_page:
                        correct_pages += 1
                    break

        page_ratio = correct_pages / len(EXPECTED_INVOICES)
        if page_ratio == 1.0:
            print(f"PASS: Component 3 — All 5 page associations correct (0.15 pts)")
            total_score += 0.15
        elif page_ratio > 0:
            partial = round(0.15 * page_ratio, 3)
            print(f"PARTIAL: Component 3 — {correct_pages}/5 page associations correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No correct page associations found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Total invoices count line (0.15 points)
    # Should contain "Total invoices found: 5" or similar
    try:
        count_match = re.search(r'[Tt]otal\s+invoices\s*(?:found)?\s*:\s*(\d+)', content)
        if count_match and int(count_match.group(1)) == EXPECTED_COUNT:
            print(f"PASS: Component 4 — Invoice count correct: {EXPECTED_COUNT} (0.15 pts)")
            total_score += 0.15
        elif count_match:
            print(f"FAIL: Component 4 — Invoice count wrong: found {count_match.group(1)}, expected {EXPECTED_COUNT}")
        else:
            print(f"FAIL: Component 4 — No invoice count line found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Grand total line (0.20 points)
    # Should contain "Grand total: $184,361.78" or similar
    try:
        grand_match = re.search(r'[Gg]rand\s+total\s*:\s*\$?([\d,]+\.?\d*)', content)
        if grand_match:
            grand_val = float(grand_match.group(1).replace(',', ''))
            if abs(grand_val - EXPECTED_GRAND_TOTAL) < 0.01:
                print(f"PASS: Component 5 — Grand total correct: ${EXPECTED_GRAND_TOTAL:,.2f} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 — Grand total wrong: found ${grand_val:,.2f}, expected ${EXPECTED_GRAND_TOTAL:,.2f}")
        else:
            print(f"FAIL: Component 5 — No grand total line found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/Desktop/invoice_summary.txt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
