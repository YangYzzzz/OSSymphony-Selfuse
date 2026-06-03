"""
Reward Script: Merge Q1/Q2 reports with cover page, page numbers, and bookmarks
Task ID: pdf_pw_030
Domain: pdf
Scoring:
  Component 1: Merged PDF exists with correct page count (34 pages) — 0.20
  Component 2: Cover page contains 'Q1-Q2 Combined Report' title text — 0.20
  Component 3: Cover page has NO page number (bottom area is empty) — 0.10
  Component 4: Pages after cover have page numbers at bottom — 0.20
  Component 5: TOC/bookmarks for Q1 Report (page 2) and Q2 Report (page 17) — 0.30
"""

import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_030'


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
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page count is 34 (1 cover + 15 Q1 + 18 Q2) — 0.20 points
    try:
        page_count = doc.page_count
        if page_count == 34:
            print(f"PASS: Component 1 -- Page count is 34 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- Expected 34 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Cover page contains 'Q1-Q2 Combined Report' title — 0.20 points
    try:
        if doc.page_count > 0:
            cover_page = doc[0]
            cover_text = cover_page.get_text("text")
            if "Q1-Q2 Combined Report" in cover_text:
                # Also verify the title is in a reasonably large font (>= 20pt)
                # by checking that the title text block spans a significant area
                blocks = cover_page.get_text("dict")
                title_found_large = False
                for block in blocks.get("blocks", []):
                    if block.get("type") == 0:  # text block
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):
                                if "Q1-Q2 Combined Report" in span.get("text", ""):
                                    if span.get("size", 0) >= 20:
                                        title_found_large = True
                if title_found_large:
                    print(f"PASS: Component 2 -- Cover has 'Q1-Q2 Combined Report' in large font (0.20 pts)")
                    total_score += 0.20
                else:
                    # Title text exists but font may be small; give partial
                    print(f"PARTIAL: Component 2 -- Title text found but font size < 20pt (0.10 pts)")
                    total_score += 0.10
            else:
                print(f"FAIL: Component 2 -- Cover page does not contain 'Q1-Q2 Combined Report'")
                print(f"  Cover text: {repr(cover_text[:200])}")
        else:
            print(f"FAIL: Component 2 -- No pages in document")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Cover page has NO page number at the bottom — 0.10 points
    try:
        if doc.page_count > 0:
            cover_page = doc[0]
            page_height = cover_page.rect.height
            page_width = cover_page.rect.width
            # Check bottom 60pts of cover page for any number text
            bottom_clip = fitz.Rect(0, page_height - 60, page_width, page_height)
            bottom_text = cover_page.get_textbox(bottom_clip).strip()
            if bottom_text == "" or not any(c.isdigit() for c in bottom_text):
                print(f"PASS: Component 3 -- Cover page has no page number at bottom (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 -- Cover page has text at bottom: {repr(bottom_text)}")
        else:
            print(f"FAIL: Component 3 -- No pages in document")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Pages 2-34 (index 1-33) have page numbers at the bottom — 0.20 points
    try:
        if doc.page_count >= 34:
            pages_with_numbers = 0
            total_checked = 0
            # Sample pages: check first Q1 page, mid Q1, first Q2, last page
            sample_indices = [1, 5, 10, 16, 20, 25, 33]
            for idx in sample_indices:
                if idx < doc.page_count:
                    total_checked += 1
                    page = doc[idx]
                    ph = page.rect.height
                    pw = page.rect.width
                    bottom_clip = fitz.Rect(0, ph - 60, pw, ph)
                    bottom_text = page.get_textbox(bottom_clip).strip()
                    # Page number should be a number (the display page number)
                    if bottom_text and any(c.isdigit() for c in bottom_text):
                        pages_with_numbers += 1

            if total_checked > 0:
                ratio = pages_with_numbers / total_checked
                if ratio >= 0.8:
                    print(f"PASS: Component 4 -- {pages_with_numbers}/{total_checked} sampled pages have page numbers (0.20 pts)")
                    total_score += 0.20
                elif ratio >= 0.5:
                    partial = round(0.10, 2)
                    print(f"PARTIAL: Component 4 -- {pages_with_numbers}/{total_checked} pages have numbers ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 4 -- Only {pages_with_numbers}/{total_checked} sampled pages have page numbers")
            else:
                print(f"FAIL: Component 4 -- No pages to check")
        else:
            print(f"FAIL: Component 4 -- Document has fewer than 34 pages")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Bookmarks/TOC — 'Q1 Report' at page 2 and 'Q2 Report' at page 17 — 0.30 points
    try:
        toc = doc.get_toc()
        if len(toc) >= 2:
            # Look for Q1 Report and Q2 Report entries
            q1_found = False
            q2_found = False
            for entry in toc:
                level, title, page_num = entry[0], entry[1], entry[2]
                title_lower = title.strip().lower()
                if "q1" in title_lower and "report" in title_lower:
                    if page_num == 2:
                        q1_found = True
                        print(f"  TOC: Found 'Q1 Report' -> page {page_num} (correct)")
                    else:
                        print(f"  TOC: Found 'Q1 Report' -> page {page_num} (expected 2)")
                if "q2" in title_lower and "report" in title_lower:
                    if page_num == 17:
                        q2_found = True
                        print(f"  TOC: Found 'Q2 Report' -> page {page_num} (correct)")
                    else:
                        print(f"  TOC: Found 'Q2 Report' -> page {page_num} (expected 17)")

            if q1_found and q2_found:
                print(f"PASS: Component 5 -- Both bookmarks correct (0.30 pts)")
                total_score += 0.30
            elif q1_found or q2_found:
                print(f"PARTIAL: Component 5 -- Only one bookmark correct (0.15 pts)")
                total_score += 0.15
            else:
                # TOC entries exist but wrong titles/pages
                print(f"FAIL: Component 5 -- TOC entries exist but don't match expected bookmarks")
                print(f"  TOC: {toc}")
        elif len(toc) == 1:
            print(f"PARTIAL: Component 5 -- Only 1 TOC entry found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 -- No TOC/bookmarks found")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
