"""
Reward Script: Redact credit card numbers in PDF
Task ID: pdf_ro_016
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists and is a valid PDF with 8 pages
  Component 2 (0.45): No credit card numbers remain in the document
  Component 3 (0.30): [REDACTED] replacement markers present (expect ~20)
  Component 4 (0.10): Non-CC content preserved (dates, amounts, merchant names)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_016'

# Credit card pattern: XXXX-XXXX-XXXX-XXXX
CC_PATTERN = re.compile(r'\d{4}-\d{4}-\d{4}-\d{4}')
REDACTED_PATTERN = re.compile(r'\[REDACTED\]')

# Expected values from task context
EXPECTED_PAGES = 8
EXPECTED_REDACTIONS = 20  # approximately 20 CC numbers


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz
    except ImportError:
        import pymupdf as fitz

    # Precondition: file must exist and be a valid PDF
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gather all text from the document
    all_text = ""
    page_texts = []
    for page in doc:
        text = page.get_text()
        page_texts.append(text)
        all_text += text + "\n"

    # Component 1: Valid PDF with 8 pages (0.15 points)
    # This component checks that the output file is structurally correct.
    # On initial_env, transactions_redacted.pdf does not exist, so we never reach here.
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — PDF has {page_count} pages as expected (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No credit card numbers remain (0.45 points)
    # This is the core redaction verification. CC numbers should be fully removed.
    try:
        cc_matches = CC_PATTERN.findall(all_text)
        cc_count = len(cc_matches)
        if cc_count == 0:
            print(f"PASS: Component 2 — Zero credit card numbers found in document (0.45 pts)")
            total_score += 0.45
        else:
            # Partial credit: score based on proportion removed
            # If some but not all are removed, give proportional credit
            removal_ratio = max(0, 1.0 - (cc_count / EXPECTED_REDACTIONS))
            partial = round(0.45 * removal_ratio, 3)
            print(f"FAIL: Component 2 — Found {cc_count} remaining CC numbers (expected 0). Partial: {partial}")
            total_score += partial
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: [REDACTED] replacement markers present (0.30 points)
    # Each CC number should be replaced with [REDACTED]. Expect ~20 occurrences.
    try:
        redacted_matches = REDACTED_PATTERN.findall(all_text)
        redacted_count = len(redacted_matches)
        if redacted_count >= EXPECTED_REDACTIONS:
            print(f"PASS: Component 3 — Found {redacted_count} [REDACTED] markers (expected ~{EXPECTED_REDACTIONS}) (0.30 pts)")
            total_score += 0.30
        elif redacted_count > 0:
            # Partial credit based on how many redactions were made
            ratio = redacted_count / EXPECTED_REDACTIONS
            partial = round(0.30 * ratio, 3)
            print(f"PARTIAL: Component 3 — Found {redacted_count}/{EXPECTED_REDACTIONS} [REDACTED] markers. Partial: {partial}")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No [REDACTED] markers found (expected ~{EXPECTED_REDACTIONS})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Non-CC content preserved (0.10 points)
    # Verify that transaction details like dates, amounts, merchant names remain.
    try:
        # Check for key content that should survive redaction
        preserved_markers = [
            r'Transaction',       # Transaction headers or references
            r'\$[\d,]+\.\d{2}',  # Dollar amounts
            r'2025-\d{2}-\d{2}', # Dates in YYYY-MM-DD format
        ]
        markers_found = 0
        for marker_pat in preserved_markers:
            if re.search(marker_pat, all_text):
                markers_found += 1

        if markers_found >= 2:
            print(f"PASS: Component 4 — {markers_found}/3 content preservation markers found (0.10 pts)")
            total_score += 0.10
        elif markers_found >= 1:
            partial = 0.05
            print(f"PARTIAL: Component 4 — Only {markers_found}/3 preservation markers found. Partial: {partial}")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No preservation markers found; content may be corrupted")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/finance/transactions_redacted.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
