"""
Reward Script: Redact bank account numbers and SSNs in payroll PDF
Task ID: pdf_fin_004
Domain: pdf
Scoring:
  Component 1 (0.15): Redacted output file exists at correct path
  Component 2 (0.15): Redacted file has 20 pages (matching original)
  Component 3 (0.35): No SSN patterns (XXX-XX-XXXX) in text extraction
  Component 4 (0.35): No bank account patterns (XXXX-XXXX-XXXX / 10-digit) in text extraction
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_004'

REDACTED_PATH = os.path.join(WORKDIR, 'finance', 'payroll_march2024_redacted.pdf')
ORIGINAL_PATH = os.path.join(WORKDIR, 'finance', 'payroll_march2024.pdf')

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Redacted file exists at the correct output path (0.15 points)
    # This is task-introduced: initial_env has no redacted file
    try:
        if os.path.exists(REDACTED_PATH):
            file_size = os.path.getsize(REDACTED_PATH)
            if file_size > 1000:  # Must be a real PDF, not empty/tiny
                print(f"PASS: Component 1 — Redacted file exists at {REDACTED_PATH} ({file_size} bytes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — File exists but too small ({file_size} bytes), likely not a valid PDF")
        else:
            print(f"FAIL: Component 1 — Redacted file not found at {REDACTED_PATH}")
            # If redacted file doesn't exist, no point checking further
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Load the redacted PDF for remaining checks
    try:
        import pymupdf
        doc = pymupdf.open(REDACTED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot load redacted PDF: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Redacted file has 20 pages (matching the original) (0.15 points)
    try:
        page_count = doc.page_count
        if page_count == 20:
            print(f"PASS: Component 2 — Page count is 20 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected 20 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No SSN patterns (XXX-XX-XXXX) in text extraction (0.35 points)
    try:
        ssn_pattern = r'\d{3}-\d{2}-\d{4}'
        ssn_total = 0
        ssn_pages = []
        for i in range(doc.page_count):
            page = doc[i]
            text = page.get_text()
            matches = re.findall(ssn_pattern, text)
            if matches:
                ssn_total += len(matches)
                ssn_pages.append(i)

        if ssn_total == 0:
            print(f"PASS: Component 3 — No SSN patterns found in any page (0.35 pts)")
            total_score += 0.35
        else:
            # Partial credit: proportional to how many were removed
            # Original has 25 SSNs; credit for percentage removed
            original_count = 25
            removed = max(0, original_count - ssn_total)
            partial = 0.35 * (removed / original_count)
            print(f"FAIL: Component 3 — Found {ssn_total} SSN patterns on pages {ssn_pages} (expected 0). Partial: {partial:.3f}")
            if partial > 0:
                total_score += partial
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: No bank account patterns in text extraction (0.35 points)
    # Check both XXXX-XXXX-XXXX and 10-digit patterns
    try:
        bank_dash_pattern = r'\d{4}-\d{4}-\d{4}'
        bank_10digit_pattern = r'\b\d{10}\b'
        bank_total = 0
        bank_pages = []
        for i in range(doc.page_count):
            page = doc[i]
            text = page.get_text()
            dash_matches = re.findall(bank_dash_pattern, text)
            digit_matches = re.findall(bank_10digit_pattern, text)
            page_matches = len(dash_matches) + len(digit_matches)
            if page_matches > 0:
                bank_total += page_matches
                bank_pages.append(i)

        if bank_total == 0:
            print(f"PASS: Component 4 — No bank account patterns found in any page (0.35 pts)")
            total_score += 0.35
        else:
            # Partial credit: proportional to how many were removed
            # Original has 8 dash-format + 7 ten-digit = 15 total
            original_count = 15
            removed = max(0, original_count - bank_total)
            partial = 0.35 * (removed / original_count)
            print(f"FAIL: Component 4 — Found {bank_total} bank account patterns on pages {bank_pages} (expected 0). Partial: {partial:.3f}")
            if partial > 0:
                total_score += partial
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(REDACTED_PATH):
    print(f"File not found: {REDACTED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
