"""
Reward Script: OCR Text Extraction from Scanned PDF
Task ID: pdf_gf1_010
Domain: pdf
Scoring:
  Component 1 (0.25): invoice_text.txt exists and is non-empty
  Component 2 (0.30): Contains page separators '--- Page 1 ---' and '--- Page 2 ---'
  Component 3 (0.30): Contains invoice-related keywords (invoice, amount/total, dollar values)
  Component 4 (0.15): File is valid UTF-8 encoded text
"""

import os

WORKDIR = '/home/user/Documents'
TARGET_FILE = os.path.join(WORKDIR, 'invoice_text.txt')


def verify_task():
    """
    Verify OCR text extraction task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: invoice_text.txt exists and is non-empty (0.25 points)
    try:
        if not os.path.exists(TARGET_FILE):
            print(f"FAIL: Component 1 — {TARGET_FILE} does not exist")
            # No file means nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        raw_bytes = open(TARGET_FILE, 'rb').read()
        if len(raw_bytes) < 10:
            print(f"FAIL: Component 1 — file exists but too small ({len(raw_bytes)} bytes)")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        print(f"PASS: Component 1 — invoice_text.txt exists and has {len(raw_bytes)} bytes (0.25 pts)")
        total_score += 0.25
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Contains page separators (0.30 points)
    # Both '--- Page 1 ---' and '--- Page 2 ---' must be present
    try:
        content = raw_bytes.decode('utf-8', errors='replace')
        has_page1 = '--- Page 1 ---' in content
        has_page2 = '--- Page 2 ---' in content

        if has_page1 and has_page2:
            print(f"PASS: Component 2 — both page separators found (0.30 pts)")
            total_score += 0.30
        elif has_page1 or has_page2:
            found = 'Page 1' if has_page1 else 'Page 2'
            missing = 'Page 2' if has_page1 else 'Page 1'
            print(f"PARTIAL: Component 2 — found '--- {found} ---' but missing '--- {missing} ---' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — no page separators found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Contains invoice-related keywords (0.30 points)
    # Check for words that indicate invoice content was extracted
    try:
        content_lower = content.lower()

        # Check for invoice-related terms
        invoice_keywords = ['invoice', 'inv-']
        amount_keywords = ['total', 'subtotal', 'amount', 'due']
        dollar_pattern_found = '$' in content

        has_invoice_word = any(kw in content_lower for kw in invoice_keywords)
        has_amount_word = any(kw in content_lower for kw in amount_keywords)

        checks_passed = sum([has_invoice_word, has_amount_word, dollar_pattern_found])

        if checks_passed >= 3:
            print(f"PASS: Component 3 — invoice keywords ({checks_passed}/3 checks: invoice_word={has_invoice_word}, amount_word={has_amount_word}, dollar_sign={dollar_pattern_found}) (0.30 pts)")
            total_score += 0.30
        elif checks_passed >= 2:
            print(f"PARTIAL: Component 3 — {checks_passed}/3 keyword checks passed (0.20 pts)")
            total_score += 0.20
        elif checks_passed >= 1:
            print(f"PARTIAL: Component 3 — {checks_passed}/3 keyword checks passed (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — no invoice-related keywords found in extracted text")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: File is valid UTF-8 (0.15 points)
    try:
        # Try strict UTF-8 decode
        raw_bytes.decode('utf-8')
        print(f"PASS: Component 4 — file is valid UTF-8 (0.15 pts)")
        total_score += 0.15
    except UnicodeDecodeError as e:
        print(f"FAIL: Component 4 — file is not valid UTF-8: {e}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
