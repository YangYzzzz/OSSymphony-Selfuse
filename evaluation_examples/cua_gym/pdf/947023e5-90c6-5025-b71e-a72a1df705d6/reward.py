"""
Reward Script: Redact credit card numbers from expense report PDF
Task ID: pdf_fin_019
Domain: pdf
Scoring:
  Component 1 — Redacted file exists (0.15)
  Component 2 — Page count preserved at 10 (0.15)
  Component 3 — No credit card patterns remain in text (0.40)
  Component 4 — '[REDACTED]' appears exactly 18 times (0.30)
"""

import os
import re
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_019'
REDACTED_PATH = os.path.join(WORKDIR, 'finance', 'expense_report_q1_redacted.pdf')

# Patterns for credit card numbers:
#   XXXX-XXXX-XXXX-XXXX (with hyphens)
#   XXXXXXXXXXXXXXXX (16 consecutive digits)
CC_PATTERN_HYPHEN = re.compile(r'\b\d{4}-\d{4}-\d{4}-\d{4}\b')
CC_PATTERN_PLAIN = re.compile(r'\b\d{16}\b')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Redacted file exists at correct path (0.15 points)
    try:
        if os.path.isfile(REDACTED_PATH):
            print(f"PASS: Component 1 — Redacted file exists at {REDACTED_PATH} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Redacted file not found at {REDACTED_PATH}")
            print("REWARD: 0.0")
            return 0.0  # No point continuing if file doesn't exist
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load the PDF
    try:
        doc = fitz.open(REDACTED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {REDACTED_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Page count is 10 (0.15 points)
    try:
        page_count = doc.page_count
        if page_count == 10:
            print(f"PASS: Component 2 — Page count is 10 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected 10 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Extract all text from the PDF
    all_text = ""
    try:
        for page in doc:
            all_text += page.get_text("text")
    except Exception as e:
        print(f"ERROR: Text extraction failed — {e}")

    # Component 3: No credit card patterns remain in extracted text (0.40 points)
    try:
        cc_hyphen_matches = CC_PATTERN_HYPHEN.findall(all_text)
        cc_plain_matches = CC_PATTERN_PLAIN.findall(all_text)
        total_cc_found = len(cc_hyphen_matches) + len(cc_plain_matches)

        if total_cc_found == 0:
            print(f"PASS: Component 3 — No credit card patterns found in text (0.40 pts)")
            total_score += 0.40
        else:
            # Partial credit: proportional to how many were redacted out of 18
            remaining_ratio = total_cc_found / 18.0
            partial = max(0.0, 0.40 * (1.0 - remaining_ratio))
            print(f"FAIL: Component 3 — Found {total_cc_found} credit card patterns still in text")
            if cc_hyphen_matches:
                print(f"  Hyphenated: {cc_hyphen_matches[:3]}...")
            if cc_plain_matches:
                print(f"  Plain: {cc_plain_matches[:3]}...")
            if partial > 0:
                print(f"  Partial credit: {partial:.2f} pts")
                total_score += partial
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: '[REDACTED]' appears 18 times (0.30 points)
    try:
        redacted_count = all_text.count('[REDACTED]')
        if redacted_count == 18:
            print(f"PASS: Component 4 — '[REDACTED]' appears exactly 18 times (0.30 pts)")
            total_score += 0.30
        elif redacted_count > 0:
            # Partial credit proportional to correct count
            ratio = min(redacted_count, 18) / 18.0
            partial = 0.30 * ratio
            print(f"FAIL: Component 4 — '[REDACTED]' appears {redacted_count} times, expected 18 (partial: {partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — '[REDACTED]' not found in text (0 occurrences)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
