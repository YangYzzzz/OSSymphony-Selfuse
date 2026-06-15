"""
Reward Script: Multi-app workflow — create letterhead, write 5 personalized
letters, export as individual PDFs, merge to one PDF with sequential page numbers.
Task ID: pdf_cross_150
Domain: pdf
Scoring:
  Component 1: mailing_batch.pdf has exactly 5 pages (0.20 pts)
  Component 2: All 5 recipients present, one per page (0.35 pts)
  Component 3: Letterhead content present on all 5 pages (0.20 pts)
  Component 4: Sequential page numbers 1-5 present across all pages (0.25 pts)
  Total: 1.0
"""

import os
import sys

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        print("CRITICAL: Neither pymupdf nor fitz is available")
        print("REWARD: 0.0")
        sys.exit(1)

WORKDIR = '/home/user'
TASK_ID = 'pdf_cross_150'
PDF_PATH = f'{WORKDIR}/Documents/mailing_batch.pdf'

# Expected recipients (from task context, one per page in order)
RECIPIENTS = [
    ['Emily Watson', 'Stanford'],
    ['Robert Chang', 'MIT'],
    ['Laura Fisher', 'Google'],
    ["Kevin", 'Amazon'],
    ['Aisha Patel', 'Johns Hopkins'],
]

# Letterhead indicator — a company name that should appear on each page
LETTERHEAD_INDICATORS = ['Horizon Research Institute']


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be openable
    if not os.path.exists(file_path):
        print(f"FAIL (gate): mailing_batch.pdf not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = doc.page_count

    # -----------------------------------------------------------------------
    # Component 1: Exactly 5 pages (0.20 points)
    # The merged document must have exactly 5 pages (one per recipient letter).
    # -----------------------------------------------------------------------
    try:
        if page_count == 5:
            print(f"PASS: Component 1 — exactly 5 pages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — expected 5 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: All 5 recipients present, one per page (0.35 points)
    # Each page must be addressed to a specific recipient from the list.
    # 0.07 pts per recipient found on its page (or any page if order differs).
    # -----------------------------------------------------------------------
    try:
        all_text = []
        for i in range(page_count):
            try:
                page_text = doc[i].get_text("text")
                all_text.append(page_text)
            except Exception:
                all_text.append("")

        recipients_found = 0
        per_recipient_pts = 0.07
        for expected_terms in RECIPIENTS:
            # Check if any page contains at least one of the expected identifiers
            found_in_any_page = False
            for page_text in all_text:
                if all(term in page_text for term in expected_terms):
                    found_in_any_page = True
                    break
            if found_in_any_page:
                recipients_found += 1
            else:
                print(f"FAIL: Component 2 — recipient {expected_terms} not found in any page")

        awarded_2 = round(recipients_found * per_recipient_pts, 4)
        total_score += awarded_2
        if recipients_found == len(RECIPIENTS):
            print(f"PASS: Component 2 — all {len(RECIPIENTS)} recipients found ({awarded_2:.2f} pts)")
        else:
            print(f"PARTIAL: Component 2 — {recipients_found}/{len(RECIPIENTS)} recipients found ({awarded_2:.2f} pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Letterhead content on all pages (0.20 points)
    # Each page should contain the company name/letterhead indicator.
    # -----------------------------------------------------------------------
    try:
        pages_with_letterhead = 0
        for i in range(page_count):
            try:
                page_text = doc[i].get_text("text")
                if any(indicator in page_text for indicator in LETTERHEAD_INDICATORS):
                    pages_with_letterhead += 1
                else:
                    print(f"FAIL: Component 3 — page {i+1} missing letterhead indicator")
            except Exception as e2:
                print(f"WARN: Component 3 — could not read page {i+1}: {e2}")

        if pages_with_letterhead == 5:
            print(f"PASS: Component 3 — letterhead found on all 5 pages (0.20 pts)")
            total_score += 0.20
        elif pages_with_letterhead > 0:
            partial = round(pages_with_letterhead / 5 * 0.20, 4)
            total_score += partial
            print(f"PARTIAL: Component 3 — letterhead found on {pages_with_letterhead}/5 pages ({partial:.2f} pts)")
        else:
            print(f"FAIL: Component 3 — no letterhead found on any page")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Sequential page numbers 1-5 across entire document (0.25 pts)
    # The task requires adding sequential page numbers.
    # Each page should have "Page X of 5" or equivalent numbering.
    # 0.05 pts per correctly numbered page.
    # -----------------------------------------------------------------------
    try:
        pages_numbered_correctly = 0
        per_page_pts = 0.05
        for i in range(page_count):
            try:
                page_text = doc[i].get_text("text")
                page_num = i + 1
                # Accept "Page X of 5", "Page X", or just the digit as page number
                # Most flexible: look for the page number appearing as text
                has_page_num = (
                    f"Page {page_num} of 5" in page_text
                    or f"Page {page_num} of {page_count}" in page_text
                    or f"{page_num} of 5" in page_text
                    or f"{page_num} of {page_count}" in page_text
                )
                if has_page_num:
                    pages_numbered_correctly += 1
                else:
                    print(f"FAIL: Component 4 — page {page_num} missing sequential page number")
            except Exception as e2:
                print(f"WARN: Component 4 — could not read page {i+1}: {e2}")

        awarded_4 = round(pages_numbered_correctly * per_page_pts, 4)
        total_score += awarded_4
        if pages_numbered_correctly == 5:
            print(f"PASS: Component 4 — all 5 pages have sequential page numbers (0.25 pts)")
        else:
            print(f"PARTIAL: Component 4 — {pages_numbered_correctly}/5 pages have sequential numbers ({awarded_4:.2f} pts)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(PDF_PATH):
    print(f"File not found: {PDF_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(PDF_PATH)
