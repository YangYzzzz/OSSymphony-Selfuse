"""
Reward Script: Add university logo stamp to every page of a PDF
Task ID: pdf_res_065
Domain: pdf
Scoring:
  Component 1 (0.2): Branded PDF exists and has 20 pages
  Component 2 (0.4): Every page contains at least one image (the logo)
  Component 3 (0.4): Logo image is positioned in the top-left corner within ~50x50 pt rect on all pages
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_065'

BRANDED_PATH = os.path.join(WORKDIR, 'papers', 'official_report_branded.pdf')
ORIGINAL_PATH = os.path.join(WORKDIR, 'papers', 'official_report.pdf')
EXPECTED_PAGES = 20


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: branded file must exist
    if not os.path.exists(BRANDED_PATH):
        print(f"CRITICAL: Branded file not found: {BRANDED_PATH}")
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
        doc = fitz.open(BRANDED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open branded PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = len(doc)

    # Component 1: Branded PDF has correct page count (0.2 points)
    # This checks that the branded file was created AND preserves all 20 pages.
    # The branded file does NOT exist on initial_env, so this is a task-introduced change.
    try:
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — Branded PDF has {page_count} pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Every page has at least one image (0.4 points)
    # Initial PDF has 0 images per page. Golden should have >= 1 image on each page.
    # Award partial credit proportional to pages with images.
    try:
        pages_with_images = 0
        for i in range(page_count):
            page = doc[i]
            images = page.get_images()
            if len(images) >= 1:
                pages_with_images += 1

        if page_count > 0:
            ratio = pages_with_images / page_count
        else:
            ratio = 0.0

        component2_score = round(0.4 * ratio, 4)
        if pages_with_images == page_count and page_count == EXPECTED_PAGES:
            print(f"PASS: Component 2 — All {page_count} pages have images ({component2_score} pts)")
            total_score += component2_score
        elif pages_with_images > 0:
            print(f"PARTIAL: Component 2 — {pages_with_images}/{page_count} pages have images ({component2_score} pts)")
            total_score += component2_score
        else:
            print(f"FAIL: Component 2 — No pages have images")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Logo positioned in top-left corner within ~50x50 pt rect on all pages (0.4 points)
    # The task specifies a 50x50 point image in the top-left corner.
    # We verify that each page has an image whose bounding box is roughly (0, 0, 50, 50).
    # Allow tolerance of 10 points for position and 15 points for size.
    try:
        pages_with_correct_logo = 0
        TOLERANCE_POS = 10.0   # top-left corner position tolerance
        TOLERANCE_SIZE = 15.0  # size tolerance around 50x50

        for i in range(page_count):
            page = doc[i]
            img_info_list = page.get_image_info()
            matching_count = 0
            for img_info in img_info_list:
                bbox = img_info.get('bbox', (999, 999, 999, 999))
                x0, y0, x1, y1 = bbox
                width = x1 - x0
                height = y1 - y0
                # Check: top-left corner (x0, y0 near 0,0) and size ~50x50
                if (x0 <= TOLERANCE_POS and y0 <= TOLERANCE_POS and
                        35.0 <= width <= 50.0 + TOLERANCE_SIZE and
                        35.0 <= height <= 50.0 + TOLERANCE_SIZE):
                    matching_count += 1
                    break
            if matching_count > 0:
                pages_with_correct_logo += 1

        if page_count > 0:
            ratio = pages_with_correct_logo / page_count
        else:
            ratio = 0.0

        component3_score = round(0.4 * ratio, 4)
        if pages_with_correct_logo == page_count and page_count == EXPECTED_PAGES:
            print(f"PASS: Component 3 — All {page_count} pages have correctly positioned logo ({component3_score} pts)")
            total_score += component3_score
        elif pages_with_correct_logo > 0:
            print(f"PARTIAL: Component 3 — {pages_with_correct_logo}/{page_count} pages have correct logo placement ({component3_score} pts)")
            total_score += component3_score
        else:
            print(f"FAIL: Component 3 — No pages have correctly positioned logo")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
