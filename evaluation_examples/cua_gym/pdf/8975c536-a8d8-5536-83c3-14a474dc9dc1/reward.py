"""
Reward Script: Resize A3 PDF to A4 with proportional scaling
Task ID: pdf_pw_028
Domain: pdf
Scoring:
  Component 1: Output file exists at correct path (0.15)
  Component 2: Page count matches original (8 pages) (0.15)
  Component 3: All pages have A4 landscape dimensions (0.40)
  Component 4: Content preserved — text present on all pages (0.30)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_028'

# Expected A4 landscape dimensions in points (tolerance for floating point)
A4_LANDSCAPE_WIDTH = 841.89
A4_LANDSCAPE_HEIGHT = 595.28
DIM_TOLERANCE = 1.0  # 1 point tolerance for page dimensions
EXPECTED_PAGE_COUNT = 8


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file is a valid PDF with at least 1 page (0.15 points)
    # This component verifies the output file was created as a valid PDF.
    # Fails on initial_env because a3_drawings_a4.pdf does not exist there.
    try:
        page_count = len(doc)
        if page_count > 0:
            print(f"PASS: Component 1 — Valid PDF with {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — PDF has 0 pages")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page count is exactly 8 (matching original) (0.15 points)
    try:
        page_count = len(doc)
        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 2 — Page count is {page_count} as expected (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected {EXPECTED_PAGE_COUNT} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All pages have A4 landscape dimensions (0.40 points)
    # Each page contributes proportionally (0.05 per page)
    try:
        pages_correct = 0
        for i in range(len(doc)):
            page = doc[i]
            r = page.rect
            w, h = r.width, r.height

            width_ok = abs(w - A4_LANDSCAPE_WIDTH) < DIM_TOLERANCE
            height_ok = abs(h - A4_LANDSCAPE_HEIGHT) < DIM_TOLERANCE

            if width_ok and height_ok:
                pages_correct += 1
            else:
                print(f"  Page {i}: dimensions {w:.2f} x {h:.2f} — expected ~{A4_LANDSCAPE_WIDTH} x {A4_LANDSCAPE_HEIGHT}")

        if pages_correct == len(doc) and len(doc) == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 3 — All {pages_correct}/{len(doc)} pages have correct A4 landscape dimensions (0.40 pts)")
            total_score += 0.40
        elif pages_correct > 0:
            partial = round(0.40 * (pages_correct / EXPECTED_PAGE_COUNT), 2)
            print(f"PARTIAL: Component 3 — {pages_correct}/{len(doc)} pages have correct dimensions ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages have correct A4 landscape dimensions")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Content preserved — text present on all pages (0.30 points)
    # Verify that text content from the engineering drawings is present after resize.
    # Each page contributes proportionally.
    try:
        pages_with_content = 0
        for i in range(len(doc)):
            page = doc[i]
            text = page.get_text().strip()
            # Check that meaningful text is present (at minimum "ACME" or "Drawing" or "Sheet")
            if len(text) > 50 and ("ACME" in text or "Drawing" in text or "Sheet" in text):
                pages_with_content += 1
            else:
                print(f"  Page {i}: insufficient text content (len={len(text)})")

        if pages_with_content == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 4 — All {pages_with_content}/{EXPECTED_PAGE_COUNT} pages have preserved text content (0.30 pts)")
            total_score += 0.30
        elif pages_with_content > 0:
            partial = round(0.30 * (pages_with_content / EXPECTED_PAGE_COUNT), 2)
            print(f"PARTIAL: Component 4 — {pages_with_content}/{EXPECTED_PAGE_COUNT} pages have text content ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No pages have preserved text content")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/a3_drawings_a4.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
