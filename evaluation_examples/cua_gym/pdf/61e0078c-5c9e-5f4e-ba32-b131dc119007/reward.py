"""
Reward Script: Crop top 100 points from every page of workshop_slides.pdf
Task ID: pdf_res_076
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists at /home/user/papers/workshop_slides_cropped.pdf
  Component 2 (0.15): Correct page count (30 pages)
  Component 3 (0.50): All pages have cropbox y0 == 100 (top 100 points cropped)
  Component 4 (0.20): All pages retain correct dimensions (x0=0, x1=612, y1=792)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_076'
OUTPUT_PATH = os.path.join(WORKDIR, 'papers', 'workshop_slides_cropped.pdf')

# Expected values
EXPECTED_PAGE_COUNT = 30
EXPECTED_CROPBOX_Y0 = 100.0
EXPECTED_CROPBOX_X0 = 0.0
EXPECTED_CROPBOX_X1 = 612.0
EXPECTED_CROPBOX_Y1 = 792.0
TOLERANCE = 1.0  # points tolerance for floating point


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at correct path (0.15 points)
    # This is a task-introduced change: the cropped file does not exist in initial_env.
    try:
        if not os.path.exists(file_path):
            print(f"FAIL: Component 1 — Output file not found at {file_path}")
            print("REWARD: 0.0")
            return 0.0
        file_size = os.path.getsize(file_path)
        if file_size > 0:
            print(f"PASS: Component 1 — Output file exists ({file_size} bytes) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Output file is empty")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load the PDF
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Correct page count (0.15 points)
    try:
        page_count = len(doc)
        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 2 — Page count is {page_count} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected {EXPECTED_PAGE_COUNT} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All pages have cropbox y0 == 100 (0.50 points)
    # This is the core task: cropping the top 100 points from every page.
    # Award proportional credit based on how many pages are correctly cropped.
    try:
        pages_cropped = 0
        pages_checked = len(doc)
        for i in range(pages_checked):
            page = doc[i]
            cb = page.cropbox
            if abs(cb.y0 - EXPECTED_CROPBOX_Y0) < TOLERANCE:
                pages_cropped += 1
            else:
                if i < 5 or i == pages_checked - 1:
                    # Print details for first few and last page for debugging
                    print(f"  INFO: Page {i} cropbox.y0 = {cb.y0} (expected ~{EXPECTED_CROPBOX_Y0})")

        if pages_checked > 0:
            ratio = pages_cropped / pages_checked
            crop_score = round(0.50 * ratio, 4)
            if pages_cropped == pages_checked:
                print(f"PASS: Component 3 — All {pages_checked} pages cropped at y0={EXPECTED_CROPBOX_Y0} (0.50 pts)")
            else:
                print(f"PARTIAL: Component 3 — {pages_cropped}/{pages_checked} pages correctly cropped ({crop_score} pts)")
            total_score += crop_score
        else:
            print(f"FAIL: Component 3 — No pages to check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All pages retain correct width and bottom dimensions (0.20 points)
    # Verifies that cropping didn't alter the x0, x1, or y1 coordinates.
    try:
        pages_correct_dims = 0
        for i in range(len(doc)):
            page = doc[i]
            cb = page.cropbox
            if (abs(cb.x0 - EXPECTED_CROPBOX_X0) < TOLERANCE and
                abs(cb.x1 - EXPECTED_CROPBOX_X1) < TOLERANCE and
                abs(cb.y1 - EXPECTED_CROPBOX_Y1) < TOLERANCE):
                pages_correct_dims += 1
            else:
                if i < 3:
                    print(f"  INFO: Page {i} cropbox dims: x0={cb.x0}, x1={cb.x1}, y1={cb.y1}")

        if len(doc) > 0:
            ratio = pages_correct_dims / len(doc)
            dim_score = round(0.20 * ratio, 4)
            if pages_correct_dims == len(doc):
                print(f"PASS: Component 4 — All pages have correct dimensions (0.20 pts)")
            else:
                print(f"PARTIAL: Component 4 — {pages_correct_dims}/{len(doc)} pages correct dims ({dim_score} pts)")
            total_score += dim_score
        else:
            print(f"FAIL: Component 4 — No pages to check")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
