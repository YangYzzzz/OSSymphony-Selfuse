"""
Reward Script: Delete pages 4 and 7 from a 10-page PDF and save as report_cleaned.pdf
Task ID: pdf_gf1_033
Domain: pdf
Scoring:
  - Component 1 (0.30): Correct page count (8 pages)
  - Component 2 (0.20): Page 3 content preserved (output page 3 == input page 3)
  - Component 3 (0.25): Page 4 of output has content from original page 5 (skip deleted page 4)
  - Component 4 (0.25): Page 6 of output has content from original page 8 (skip deleted page 7)
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_033'

# Paths
RESULT_PATH = os.path.join(WORKDIR, 'Documents', 'report_cleaned.pdf')
SOURCE_PATH = os.path.join(WORKDIR, 'Documents', 'report_with_blanks.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(RESULT_PATH):
        print(f"CRITICAL: Result file not found: {RESULT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be a valid PDF
    try:
        doc = pymupdf.open(RESULT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open result PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Correct page count — 8 pages (0.30 points)
    try:
        page_count = doc.page_count
        if page_count == 8:
            print(f"PASS: Component 1 — Page count is 8 (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Expected 8 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # For content mapping checks, we compare text from result pages against known content
    # from the original source. We use distinctive text snippets that uniquely identify pages.
    #
    # Original page mapping (1-indexed):
    #   Input page 1 -> Output page 1
    #   Input page 2 -> Output page 2
    #   Input page 3 -> Output page 3
    #   Input page 4 -> DELETED
    #   Input page 5 -> Output page 4
    #   Input page 6 -> Output page 5
    #   Input page 7 -> DELETED
    #   Input page 8 -> Output page 6
    #   Input page 9 -> Output page 7
    #   Input page 10 -> Output page 8

    # Component 2: Output page 3 matches input page 3 — "Revenue Breakdown by Division" (0.20 pts)
    # This verifies content is preserved and pages weren't shifted incorrectly before the deletion point.
    try:
        if doc.page_count >= 3:
            text_p3 = doc[2].get_text("text")  # 0-indexed page 2 = page 3
            if "Revenue Breakdown by Division" in text_p3:
                print(f"PASS: Component 2 — Output page 3 contains 'Revenue Breakdown by Division' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — Output page 3 missing expected content. Found: {text_p3[:80]!r}")
        else:
            print(f"FAIL: Component 2 — Not enough pages (need >=3, have {doc.page_count})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Output page 4 matches input page 5 — "Customer Acquisition & Retention" (0.25 pts)
    # After deleting input page 4, input page 5 should become output page 4.
    try:
        if doc.page_count >= 4:
            text_p4 = doc[3].get_text("text")  # 0-indexed page 3 = page 4
            if "Customer Acquisition & Retention" in text_p4:
                print(f"PASS: Component 3 — Output page 4 contains 'Customer Acquisition & Retention' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Output page 4 has wrong content. Found: {text_p4[:80]!r}")
        else:
            print(f"FAIL: Component 3 — Not enough pages (need >=4, have {doc.page_count})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Output page 6 matches input page 8 — "Financial Projections" (0.25 pts)
    # After deleting input pages 4 and 7, input page 8 should become output page 6.
    try:
        if doc.page_count >= 6:
            text_p6 = doc[5].get_text("text")  # 0-indexed page 5 = page 6
            if "Financial Projections" in text_p6:
                print(f"PASS: Component 4 — Output page 6 contains 'Financial Projections' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — Output page 6 has wrong content. Found: {text_p6[:80]!r}")
        else:
            print(f"FAIL: Component 4 — Not enough pages (need >=6, have {doc.page_count})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
