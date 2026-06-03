"""
Reward Script: Add running headers to thesis PDF
Task ID: pdf_res_062
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists with correct page count
  Component 2 (0.10): Page 1 has no header
  Component 3 (0.30): Even pages have thesis title on the left
  Component 4 (0.30): Odd pages have chapter title on the right
  Component 5 (0.15): Chapter titles match correct chapter per page range
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_062'
OUTPUT_PATH = os.path.join(WORKDIR, 'thesis', 'long_thesis_headers.pdf')

# Chapter mapping: page number (1-indexed) -> chapter number
# Ch1: p1-19, Ch2: p20-39, Ch3: p40-59, Ch4: p60-74, Ch5: p75-85
CHAPTER_BREAKS = [(1, 1), (20, 2), (40, 3), (60, 4), (75, 5)]

THESIS_TITLE = 'Machine Learning for Climate Science'
HEADER_Y_THRESHOLD = 60  # Points from top — header text should be within this


def get_chapter_for_page(page_num_1indexed):
    """Return the chapter number for a given 1-indexed page number."""
    chapter = 1
    for start_page, ch_num in CHAPTER_BREAKS:
        if page_num_1indexed >= start_page:
            chapter = ch_num
    return chapter


def get_header_text_and_position(page):
    """Extract header text blocks from the top strip of the page.
    Returns list of (text, x0, x1, page_width) tuples."""
    pw = page.rect.width
    blocks = page.get_text('blocks')
    header_blocks = []
    for b in blocks:
        x0, y0, x1, y1, text, blk_no, blk_type = b
        if y0 < HEADER_Y_THRESHOLD and blk_type == 0:  # text block in header area
            header_blocks.append((text.strip(), x0, x1, pw))
    return header_blocks


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
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

    # Component 1: Output file has 85 pages (0.15 points)
    try:
        page_count = len(doc)
        if page_count == 85:
            print(f"PASS: Component 1 — Page count is 85 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 85 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page 1 has no header (0.10 points)
    try:
        page1 = doc[0]
        header_blocks = get_header_text_and_position(page1)
        # Filter for any text that looks like a header (thesis title or chapter title)
        header_texts = [t for t, x0, x1, pw in header_blocks
                        if THESIS_TITLE.lower() in t.lower() or 'chapter' in t.lower()]
        if len(header_texts) == 0:
            print(f"PASS: Component 2 — Page 1 has no running header (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Page 1 has header text: {header_texts}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Even pages (2,4,6,...) have thesis title on the LEFT (0.30 points)
    try:
        even_pages = [i for i in range(1, len(doc)) if (i + 1) % 2 == 0]  # 0-indexed for even page numbers
        even_pass = 0
        even_total = len(even_pages)
        for pg_idx in even_pages:
            header_blocks = get_header_text_and_position(doc[pg_idx])
            if any(THESIS_TITLE.lower() in text.lower() and x0 < pw / 2
                   for text, x0, x1, pw in header_blocks):
                even_pass += 1
        ratio = even_pass / even_total if even_total > 0 else 0
        pts = round(0.30 * ratio, 4)
        if ratio >= 0.95:
            print(f"PASS: Component 3 — {even_pass}/{even_total} even pages have thesis title on left ({pts} pts)")
            total_score += 0.30
        elif ratio > 0:
            print(f"PARTIAL: Component 3 — {even_pass}/{even_total} even pages have thesis title on left ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 3 — No even pages have thesis title on left")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Odd pages (3,5,7,...) have chapter title on the RIGHT (0.30 points)
    try:
        odd_pages = [i for i in range(2, len(doc)) if (i + 1) % 2 == 1]  # 0-indexed for odd page numbers >= 3
        odd_pass = 0
        odd_total = len(odd_pages)
        for pg_idx in odd_pages:
            header_blocks = get_header_text_and_position(doc[pg_idx])
            if any('chapter' in text.lower() and x0 >= pw / 2
                   for text, x0, x1, pw in header_blocks):
                odd_pass += 1
        ratio = odd_pass / odd_total if odd_total > 0 else 0
        pts = round(0.30 * ratio, 4)
        if ratio >= 0.95:
            print(f"PASS: Component 4 — {odd_pass}/{odd_total} odd pages have chapter title on right ({pts} pts)")
            total_score += 0.30
        elif ratio > 0:
            print(f"PARTIAL: Component 4 — {odd_pass}/{odd_total} odd pages have chapter title on right ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 4 — No odd pages have chapter title on right")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Chapter titles match correct chapter for each page range (0.15 points)
    # Ch1: p1-19, Ch2: p20-39, Ch3: p40-59, Ch4: p60-74, Ch5: p75-85
    try:
        odd_pages = [i for i in range(2, len(doc)) if (i + 1) % 2 == 1]
        correct_ch = 0
        checked = 0
        for pg_idx in odd_pages:
            page_num = pg_idx + 1  # 1-indexed
            expected_ch = get_chapter_for_page(page_num)
            expected_text = f"Chapter {expected_ch}"
            header_blocks = get_header_text_and_position(doc[pg_idx])
            checked += 1
            if any(expected_text.lower() in text.lower()
                   for text, x0, x1, pw in header_blocks):
                correct_ch += 1
        ratio = correct_ch / checked if checked > 0 else 0
        pts = round(0.15 * ratio, 4)
        if ratio >= 0.95:
            print(f"PASS: Component 5 — {correct_ch}/{checked} odd pages have correct chapter number ({pts} pts)")
            total_score += 0.15
        elif ratio > 0:
            print(f"PARTIAL: Component 5 — {correct_ch}/{checked} odd pages have correct chapter number ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 5 — No odd pages have correct chapter number")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
