"""
Reward Script: Add header and footer to every page of a PDF
Task ID: pdf_fm_091
Domain: pdf
Scoring:
  Component 1 (0.3) — Header "Company XYZ - Quarterly Report" in top region of all 22 pages
  Component 2 (0.3) — Footer "Confidential | Page X/22" in bottom region of all 22 pages
  Component 3 (0.2) — Page numbering sequential and correct (1/22 through 22/22)
  Component 4 (0.2) — Output PDF has exactly 22 pages (same as source)
"""

import os
import re
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_091'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'quarterly_q3_final.pdf')

EXPECTED_PAGE_COUNT = 22
HEADER_TEXT = "Company XYZ - Quarterly Report"
FOOTER_PREFIX = "Confidential | Page"


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = doc.page_count

    # Component 4: Output PDF has exactly 22 pages (0.2 points)
    # This checks the output wasn't corrupted or pages lost/added
    try:
        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 4 — PDF has {page_count} pages as expected (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — Expected {EXPECTED_PAGE_COUNT} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 1: Header text on all pages (0.3 points)
    # Check that "Company XYZ - Quarterly Report" appears in the top 60pt of each page
    try:
        header_pass_count = 0
        header_fail_pages = []
        for i in range(page_count):
            page = doc[i]
            page_height = page.rect.height
            page_width = page.rect.width
            # Top region: top 60 points
            top_clip = pymupdf.Rect(0, 0, page_width, 60)
            top_text = page.get_textbox(top_clip).strip()
            if HEADER_TEXT in top_text:
                header_pass_count += 1
            else:
                header_fail_pages.append(i + 1)

        if header_pass_count == page_count:
            print(f"PASS: Component 1 — Header found on all {page_count} pages (0.3 pts)")
            total_score += 0.3
        elif header_pass_count > 0:
            # Partial credit: proportional to pages with correct header
            partial = 0.3 * (header_pass_count / page_count)
            print(f"PARTIAL: Component 1 — Header found on {header_pass_count}/{page_count} pages ({partial:.3f} pts). Missing on pages: {header_fail_pages[:5]}")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Header not found on any page. Expected '{HEADER_TEXT}' in top region")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Footer text on all pages (0.3 points)
    # Check that "Confidential | Page X/22" (or X/N) appears in the bottom 60pt of each page
    try:
        footer_pass_count = 0
        footer_fail_pages = []
        for i in range(page_count):
            page = doc[i]
            page_height = page.rect.height
            page_width = page.rect.width
            # Bottom region: bottom 60 points
            bottom_clip = pymupdf.Rect(0, page_height - 60, page_width, page_height)
            bottom_text = page.get_textbox(bottom_clip).strip()
            # Check for "Confidential | Page" pattern
            if FOOTER_PREFIX in bottom_text:
                footer_pass_count += 1
            else:
                footer_fail_pages.append(i + 1)

        if footer_pass_count == page_count:
            print(f"PASS: Component 2 — Footer found on all {page_count} pages (0.3 pts)")
            total_score += 0.3
        elif footer_pass_count > 0:
            partial = 0.3 * (footer_pass_count / page_count)
            print(f"PARTIAL: Component 2 — Footer found on {footer_pass_count}/{page_count} pages ({partial:.3f} pts). Missing on pages: {footer_fail_pages[:5]}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Footer not found on any page. Expected '{FOOTER_PREFIX} X/Y' in bottom region")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page numbering is sequential and correct (0.2 points)
    # Verify each page has the correct "Page X/22" where X goes from 1 to 22
    try:
        numbering_pass_count = 0
        numbering_fail_pages = []
        for i in range(page_count):
            page = doc[i]
            page_height = page.rect.height
            page_width = page.rect.width
            # Check bottom region for page number
            bottom_clip = pymupdf.Rect(0, page_height - 60, page_width, page_height)
            bottom_text = page.get_textbox(bottom_clip).strip()
            expected_page_num = f"Page {i + 1}/{EXPECTED_PAGE_COUNT}"
            if expected_page_num in bottom_text:
                numbering_pass_count += 1
            else:
                numbering_fail_pages.append((i + 1, bottom_text))

        if numbering_pass_count == page_count:
            print(f"PASS: Component 3 — Correct page numbering on all {page_count} pages (0.2 pts)")
            total_score += 0.2
        elif numbering_pass_count > 0:
            partial = 0.2 * (numbering_pass_count / page_count)
            print(f"PARTIAL: Component 3 — Correct numbering on {numbering_pass_count}/{page_count} pages ({partial:.3f} pts). Issues on pages: {numbering_fail_pages[:3]}")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No correct page numbering found. Expected 'Page X/{EXPECTED_PAGE_COUNT}' pattern")
            if numbering_fail_pages:
                print(f"  Sample footer text on page 1: '{numbering_fail_pages[0][1]}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

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
