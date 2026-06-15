"""
Reward Script: Resize all pages of a3_poster.pdf from A3 to A4 dimensions
Task ID: pdf_fm_070
Domain: pdf
Scoring:
  - Component 1 (0.4): Output file exists and has correct page count (4 pages)
  - Component 2 (0.6): All pages have A4 dimensions (595 x 842 pts, with tolerance)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_070'

# A4 dimensions in points (72 pts/inch)
A4_WIDTH = 595.0
A4_HEIGHT = 842.0
TOLERANCE = 2.0  # allow small rounding tolerance in points


def verify_task(file_path):
    """
    Verify that the output PDF has 4 pages all resized to A4 dimensions.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pymupdf
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = len(doc)

    # Component 1: Correct page count (0.4 points)
    # The original a3_poster.pdf has 4 pages; the output must also have 4 pages.
    try:
        if page_count == 4:
            print(f"PASS: Component 1 — Page count is 4 (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected 4 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All pages have A4 dimensions (0.6 points)
    # Award partial credit per page: 0.15 per page (4 pages x 0.15 = 0.6)
    try:
        a4_page_count = 0
        for i, page in enumerate(doc):
            r = page.rect
            w, h = r.width, r.height
            width_ok = abs(w - A4_WIDTH) <= TOLERANCE
            height_ok = abs(h - A4_HEIGHT) <= TOLERANCE
            if width_ok and height_ok:
                print(f"  Page {i}: {w:.1f}x{h:.1f} pts — A4 OK")
                a4_page_count += 1
            else:
                print(f"  Page {i}: {w:.1f}x{h:.1f} pts — NOT A4 (expected ~{A4_WIDTH}x{A4_HEIGHT})")

        if a4_page_count > 0:
            dim_score = a4_page_count * 0.15  # 0.15 per correctly-sized page
            print(f"PASS: Component 2 — {a4_page_count}/4 pages have A4 dimensions ({dim_score:.2f} pts)")
            if dim_score > 0:
                total_score += dim_score
        else:
            print(f"FAIL: Component 2 — No pages have A4 dimensions")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/Documents/a3_poster_a4.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
