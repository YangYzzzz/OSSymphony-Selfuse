"""
Reward Script: Duplicate page 1 of flyer.pdf four times to create flyer_4copies.pdf with 4 identical pages
Task ID: pdf_ro_039
Domain: pdf
Scoring:
  - Component 1: Output has exactly 4 pages (0.4 pts)
  - Component 2: All pages have same dimensions as original (0.3 pts)
  - Component 3: All pages have identical text matching original page 1 (0.3 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_039'

OUTPUT_PATH = os.path.join(WORKDIR, 'Documents', 'flyer_4copies.pdf')
ORIGINAL_PATH = os.path.join(WORKDIR, 'Documents', 'flyer.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Gate: original file must exist (precondition)
    if not os.path.exists(ORIGINAL_PATH):
        print(f"CRITICAL: Original file not found: {ORIGINAL_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
    except ImportError:
        try:
            import pymupdf as fitz
        except ImportError:
            print("CRITICAL: Neither fitz nor pymupdf available")
            print("REWARD: 0.0")
            return 0.0

    try:
        output_doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open output PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        orig_doc = fitz.open(ORIGINAL_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open original PDF: {e}")
        output_doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Get original page properties
    orig_page = orig_doc[0]
    orig_width = orig_page.rect.width
    orig_height = orig_page.rect.height
    orig_text = orig_page.get_text()

    # Component 1: Output has exactly 4 pages (0.4 points)
    try:
        page_count = output_doc.page_count
        if page_count == 4:
            print(f"PASS: Component 1 -- Output has exactly 4 pages (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- Expected 4 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All 4 pages have same dimensions as original (0.3 points)
    try:
        dim_mismatches = 0
        for i in range(output_doc.page_count):
            p = output_doc[i]
            w = p.rect.width
            h = p.rect.height
            if abs(w - orig_width) > 1.0 or abs(h - orig_height) > 1.0:
                print(f"FAIL: Component 2 -- Page {i} dimensions ({w}x{h}) differ from original ({orig_width}x{orig_height})")
                dim_mismatches += 1
        if dim_mismatches == 0 and output_doc.page_count == 4:
            print(f"PASS: Component 2 -- All 4 pages match original dimensions {orig_width}x{orig_height} (0.3 pts)")
            total_score += 0.3
        elif dim_mismatches == 0:
            print(f"FAIL: Component 2 -- Dimensions match but page count is not 4")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All 4 pages have identical text matching original page 1 (0.3 points)
    try:
        text_mismatches = 0
        for i in range(output_doc.page_count):
            page_text = output_doc[i].get_text()
            if page_text != orig_text:
                print(f"FAIL: Component 3 -- Page {i} text does not match original (len {len(page_text)} vs {len(orig_text)})")
                text_mismatches += 1
        if text_mismatches == 0 and output_doc.page_count == 4:
            print(f"PASS: Component 3 -- All 4 pages have identical text matching original (0.3 pts)")
            total_score += 0.3
        elif text_mismatches == 0:
            print(f"FAIL: Component 3 -- Text matches but page count is not 4")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    orig_doc.close()
    output_doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
