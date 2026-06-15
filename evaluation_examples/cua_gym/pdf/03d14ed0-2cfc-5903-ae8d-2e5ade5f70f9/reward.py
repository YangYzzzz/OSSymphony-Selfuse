"""
Reward Script: Crop all pages in scanned_book.pdf to remove 50-point border
Task ID: pdf_pw_044
Domain: pdf
Scoring:
  Component 1 (0.3): Output file exists with correct page count (120 pages)
  Component 2 (0.5): CropBox set to (50, 50, 562, 742) on ALL pages
  Component 3 (0.2): Visible page area is 512x692 points
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_044'

# Expected values from task context
EXPECTED_PAGE_COUNT = 120
EXPECTED_CROPBOX = (50.0, 50.0, 562.0, 742.0)
EXPECTED_WIDTH = 512.0   # 562 - 50
EXPECTED_HEIGHT = 692.0  # 742 - 50
TOLERANCE = 1.0  # points


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
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has correct page count (0.3 points)
    # This checks that the cropped file was created with all 120 pages preserved.
    # On initial_env, scanned_book_cropped.pdf does not exist, so we never reach here.
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 1 - Page count is {page_count} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 - Expected {EXPECTED_PAGE_COUNT} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: CropBox set to (50, 50, 562, 742) on ALL pages (0.5 points)
    # Check every page's cropbox matches the expected trimmed area.
    # Award partial credit: proportional to fraction of pages with correct cropbox.
    try:
        correct_pages = 0
        sample_failures = []
        for i in range(doc.page_count):
            page = doc[i]
            cb = page.cropbox
            if (abs(cb.x0 - EXPECTED_CROPBOX[0]) < TOLERANCE and
                abs(cb.y0 - EXPECTED_CROPBOX[1]) < TOLERANCE and
                abs(cb.x1 - EXPECTED_CROPBOX[2]) < TOLERANCE and
                abs(cb.y1 - EXPECTED_CROPBOX[3]) < TOLERANCE):
                correct_pages += 1
            else:
                if len(sample_failures) < 3:
                    sample_failures.append(
                        f"  Page {i}: cropbox=({cb.x0}, {cb.y0}, {cb.x1}, {cb.y1})"
                    )

        if correct_pages == doc.page_count:
            print(f"PASS: Component 2 - All {doc.page_count} pages have correct cropbox (0.5 pts)")
            total_score += 0.5
        elif correct_pages > 0:
            # Partial credit proportional to correct pages
            partial = 0.5 * (correct_pages / doc.page_count)
            if partial > 0:
                total_score += partial
                print(f"PARTIAL: Component 2 - {correct_pages}/{doc.page_count} pages correct ({partial:.2f} pts)")
                for f in sample_failures:
                    print(f)
        else:
            print(f"FAIL: Component 2 - No pages have correct cropbox")
            for f in sample_failures:
                print(f)
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Visible page dimensions are 512x692 points (0.2 points)
    # Verify the effective visible area after cropping on a sample of pages.
    try:
        dims_correct = 0
        check_pages = [0, 59, 119]  # first, middle, last
        for i in check_pages:
            page = doc[i]
            cb = page.cropbox
            width = cb.x1 - cb.x0
            height = cb.y1 - cb.y0
            if (abs(width - EXPECTED_WIDTH) < TOLERANCE and
                abs(height - EXPECTED_HEIGHT) < TOLERANCE):
                dims_correct += 1
            else:
                print(f"  Page {i}: visible area {width}x{height}, expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}")

        if dims_correct == len(check_pages):
            print(f"PASS: Component 3 - Visible area is {EXPECTED_WIDTH}x{EXPECTED_HEIGHT} on sampled pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 - {dims_correct}/{len(check_pages)} sampled pages have correct dimensions")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical output path
file_path = f'{WORKDIR}/Documents/scanned_book_cropped.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
