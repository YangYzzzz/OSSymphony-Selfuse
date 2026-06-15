"""
Reward Script: Crop all pages of scanned_book.pdf to remove 1-inch (72pt) border from all sides
Task ID: pdf_gf2_031
Domain: pdf
Scoring:
  - Component 1 (0.2): Page count remains 30
  - Component 2 (0.5): All pages have CropBox set to (72, 72, 540, 720)
  - Component 3 (0.3): Visible page dimensions are ~468x648 points
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_031'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must be loadable
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page count is 30 (0.2 points)
    # The task requires all 30 pages to be preserved after cropping.
    # Initial file has no cropped output, so this fails on initial_env.
    try:
        page_count = doc.page_count
        if page_count == 30:
            print(f"PASS: Component 1 — Page count is 30 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected 30 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All pages have CropBox set to (72, 72, 540, 720) (0.5 points)
    # This is the core verification: each page must be cropped by 72pt on all sides.
    # Expected CropBox: x0=72, y0=72, x1=540 (612-72), y1=720 (792-72)
    # Partial credit: proportional to fraction of correctly cropped pages.
    try:
        correctly_cropped = 0
        total_pages = doc.page_count
        tolerance = 2.0  # allow small floating-point differences

        for i in range(total_pages):
            page = doc[i]
            cb = page.cropbox
            if (abs(cb.x0 - 72) <= tolerance and
                abs(cb.y0 - 72) <= tolerance and
                abs(cb.x1 - 540) <= tolerance and
                abs(cb.y1 - 720) <= tolerance):
                correctly_cropped += 1

        if correctly_cropped == total_pages and total_pages == 30:
            print(f"PASS: Component 2 — All {total_pages} pages have correct CropBox (72, 72, 540, 720) (0.5 pts)")
            total_score += 0.5
        elif correctly_cropped > 0:
            partial = 0.5 * (correctly_cropped / 30)
            print(f"PARTIAL: Component 2 — {correctly_cropped}/{total_pages} pages correctly cropped ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages have the expected CropBox (72, 72, 540, 720)")
            if total_pages > 0:
                sample_cb = doc[0].cropbox
                print(f"  Sample page 0 CropBox: ({sample_cb.x0}, {sample_cb.y0}, {sample_cb.x1}, {sample_cb.y1})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Visible page dimensions are ~468x648 (0.3 points)
    # After cropping 72pt from each side of 612x792, visible area should be 468x648.
    # This checks the effective rendering dimensions (page.rect).
    try:
        correct_dims = 0
        dim_tolerance = 5.0  # allow small differences

        for i in range(doc.page_count):
            page = doc[i]
            w = page.rect.width
            h = page.rect.height
            if (abs(w - 468) <= dim_tolerance and
                abs(h - 648) <= dim_tolerance):
                correct_dims += 1

        if correct_dims == 30:
            print(f"PASS: Component 3 — All 30 pages have visible dimensions ~468x648 (0.3 pts)")
            total_score += 0.3
        elif correct_dims > 0:
            partial = 0.3 * (correct_dims / 30)
            print(f"PARTIAL: Component 3 — {correct_dims}/30 pages have correct visible dimensions ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages have expected visible dimensions (~468x648)")
            if doc.page_count > 0:
                sample_rect = doc[0].rect
                print(f"  Sample page 0 rect: {sample_rect.width}x{sample_rect.height}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/scanned_book_cropped.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
