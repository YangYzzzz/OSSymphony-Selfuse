"""
Reward Script: Booklet layout PDF creation
Task ID: pdf_fm_074
Domain: pdf
Scoring:
  Component 1 (0.20): book_booklet.pdf exists with exactly 100 pages
  Component 2 (0.20): Each page is A4 landscape (842 x 595 pts)
  Component 3 (0.20): 2-up layout — text blocks on both left and right halves
  Component 4 (0.25): Booklet front ordering — page 0 has original pages 200 and 1
  Component 5 (0.15): Booklet back ordering — page 1 has original pages 2 and 199
"""

import os

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_074'
BOOKLET_PATH = os.path.join(WORKDIR, 'Documents', 'book_booklet.pdf')


def extract_page_numbers(page):
    """Extract standalone numbers from a page's text (likely original page numbers)."""
    text = page.get_text()
    lines = text.strip().split('\n')
    nums = []
    for line in lines:
        stripped = line.strip()
        if stripped.isdigit():
            nums.append(int(stripped))
    return nums


def has_content_on_both_halves(page):
    """Check if a page has text blocks on both left and right halves (2-up layout)."""
    midpoint = page.rect.width / 2.0
    blocks = page.get_text("blocks")
    has_left = False
    has_right = False
    for b in blocks:
        x0, y0, x1, y1 = b[0], b[1], b[2], b[3]
        block_center_x = (x0 + x1) / 2.0
        if block_center_x < midpoint:
            has_left = True
        else:
            has_right = True
    return has_left and has_right


def verify_task(file_path):
    """
    Verify booklet PDF creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

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

    # Component 1: Booklet has exactly 100 pages (200 original / 2 per sheet = 100) (0.20 pts)
    try:
        page_count = doc.page_count
        if page_count == 100:
            print(f"PASS: Component 1 — Page count is 100 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected 100 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Pages are A4 landscape (842 x 595 pts, with tolerance) (0.20 pts)
    try:
        # Check first 5 pages and last page for consistent size
        pages_to_check = list(range(min(5, doc.page_count))) + [doc.page_count - 1]
        all_landscape = True
        for pi in pages_to_check:
            p = doc[pi]
            w, h = p.rect.width, p.rect.height
            # A4 landscape: 842 x 595 (tolerance of 5 pts)
            if not (abs(w - 842.0) < 5 and abs(h - 595.0) < 5):
                all_landscape = False
                print(f"FAIL: Component 2 — Page {pi} size is {w:.1f}x{h:.1f}, expected ~842x595")
                break
        if all_landscape:
            print(f"PASS: Component 2 — Pages are A4 landscape 842x595 (0.20 pts)")
            total_score += 0.20
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 2-up layout — text blocks on both halves of multiple pages (0.20 pts)
    try:
        sample_pages = [0, 1, doc.page_count // 2, doc.page_count - 1]
        two_up_count = 0
        for pi in sample_pages:
            if pi < doc.page_count:
                if has_content_on_both_halves(doc[pi]):
                    two_up_count += 1
        # At least 3 of 4 sampled pages must have 2-up layout
        if two_up_count >= 3:
            print(f"PASS: Component 3 — 2-up layout detected on {two_up_count}/{len(sample_pages)} sampled pages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — 2-up layout detected on only {two_up_count}/{len(sample_pages)} sampled pages")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Booklet front ordering — page 0 should contain original pages 200 and 1 (0.25 pts)
    try:
        nums_page0 = extract_page_numbers(doc[0])
        # Sheet 1 front: pages 200 (left) and 1 (right)
        if 200 in nums_page0 and 1 in nums_page0:
            print(f"PASS: Component 4 — Page 0 contains page numbers 200 and 1: {nums_page0} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Expected page numbers [200, 1] on page 0, found: {nums_page0}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Booklet back ordering — page 1 should contain original pages 2 and 199 (0.15 pts)
    try:
        nums_page1 = extract_page_numbers(doc[1])
        # Sheet 1 back: pages 2 (left) and 199 (right)
        if 2 in nums_page1 and 199 in nums_page1:
            print(f"PASS: Component 5 — Page 1 contains page numbers 2 and 199: {nums_page1} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Expected page numbers [2, 199] on page 1, found: {nums_page1}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(BOOKLET_PATH):
    print(f"File not found: {BOOKLET_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(BOOKLET_PATH)
