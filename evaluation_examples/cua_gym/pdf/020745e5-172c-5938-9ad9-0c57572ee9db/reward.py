"""
Reward Script: PDF Document Assembly with TOC and Bookmarks
Task ID: pdf_aw_050
Domain: pdf
Scoring:
  Component 1 (0.25): final_book.pdf exists with 65 pages
  Component 2 (0.35): TOC on page 2 lists 5 chapters with correct page numbers
  Component 3 (0.25): 5 bookmarks at correct page numbers
  Component 4 (0.15): Source content preserved (spot-check chapter text)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_050'
FILE_PATH = os.path.join(WORKDIR, 'assembly', 'final_book.pdf')

# Expected TOC entries: (chapter_label_substring, page_number)
EXPECTED_TOC_ENTRIES = [
    ('Chapter 1', 3),
    ('Chapter 2', 15),
    ('Chapter 3', 30),
    ('Chapter 4', 40),
    ('Chapter 5', 48),
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz
    except ImportError:
        try:
            import pymupdf as fitz
        except ImportError:
            print("CRITICAL: Neither fitz nor pymupdf available")
            print("REWARD: 0.0")
            return 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page count is 65 (0.25 points)
    # Initial env has no final_book.pdf, so this only passes on golden.
    try:
        page_count = doc.page_count
        if page_count == 65:
            print(f"PASS: Component 1 — Page count is 65 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 65 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: TOC text on page 2 lists chapters with correct page numbers (0.35 points)
    # Page 2 is index 1. Check that it contains chapter names and page numbers.
    try:
        if doc.page_count >= 2:
            toc_page = doc[1]
            toc_text = toc_page.get_text()
            matched_entries = 0
            for ch_label, ch_page in EXPECTED_TOC_ENTRIES:
                # Check that the chapter label and page number both appear on this page
                # The text format has chapter name on one line and page number nearby
                if ch_label in toc_text and str(ch_page) in toc_text:
                    matched_entries += 1
                else:
                    print(f"  DETAIL: Missing TOC entry for '{ch_label}' -> page {ch_page}")

            if matched_entries == 5:
                print(f"PASS: Component 2 — All 5 TOC entries found with correct page numbers (0.35 pts)")
                total_score += 0.35
            elif matched_entries >= 3:
                partial = round(0.35 * (matched_entries / 5), 2)
                print(f"PARTIAL: Component 2 — {matched_entries}/5 TOC entries correct ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — Only {matched_entries}/5 TOC entries found")
        else:
            print(f"FAIL: Component 2 — PDF has fewer than 2 pages, no TOC page")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Bookmarks (outline/TOC entries) for 5 chapters at correct pages (0.25 points)
    try:
        toc = doc.get_toc()  # [[level, title, page_num], ...]
        if len(toc) >= 5:
            bookmark_matches = 0
            for ch_label, ch_page in EXPECTED_TOC_ENTRIES:
                for entry in toc:
                    level, title, page_num = entry[0], entry[1], entry[2]
                    if ch_label in title and page_num == ch_page:
                        bookmark_matches += 1
                        break
            if bookmark_matches == 5:
                print(f"PASS: Component 3 — All 5 bookmarks found at correct pages (0.25 pts)")
                total_score += 0.25
            elif bookmark_matches >= 3:
                partial = round(0.25 * (bookmark_matches / 5), 2)
                print(f"PARTIAL: Component 3 — {bookmark_matches}/5 bookmarks correct ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {bookmark_matches}/5 bookmarks match")
        else:
            print(f"FAIL: Component 3 — Expected at least 5 TOC/bookmark entries, found {len(toc)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Source content preserved — spot check text from chapter pages (0.15 points)
    # Verify that pages from chapters contain non-trivial text (not blank).
    # Check a page from each chapter at the expected start position.
    try:
        chapter_starts = [2, 14, 29, 39, 47]  # 0-indexed: page 3->idx 2, page 15->idx 14, etc.
        chapters_with_content = 0
        for i, page_idx in enumerate(chapter_starts):
            if page_idx < doc.page_count:
                page = doc[page_idx]
                text = page.get_text().strip()
                if len(text) > 20:  # non-trivial content
                    chapters_with_content += 1
                else:
                    print(f"  DETAIL: Chapter {i+1} start page (index {page_idx}) has insufficient text ({len(text)} chars)")
            else:
                print(f"  DETAIL: Page index {page_idx} out of range")

        if chapters_with_content == 5:
            print(f"PASS: Component 4 — All 5 chapter start pages have content (0.15 pts)")
            total_score += 0.15
        elif chapters_with_content >= 3:
            partial = round(0.15 * (chapters_with_content / 5), 2)
            print(f"PARTIAL: Component 4 — {chapters_with_content}/5 chapters have content ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Only {chapters_with_content}/5 chapter pages have content")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
