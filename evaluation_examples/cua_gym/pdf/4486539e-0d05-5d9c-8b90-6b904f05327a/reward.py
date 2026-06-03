"""
Reward Script: Extract images from expense report and create new PDF with one image per page, centered and scaled.
Task ID: pdf_fin_067
Domain: pdf
Scoring:
  Component 1: Output PDF exists and has 7 pages (0.3 pts)
  Component 2: Each page has exactly 1 image (0.3 pts)
  Component 3: Images are centered on their pages (0.2 pts)
  Component 4: Images fit within page margins (0.2 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_067'
OUTPUT_PATH = os.path.join(WORKDIR, 'finance', 'receipt_images_only.pdf')
SOURCE_PATH = os.path.join(WORKDIR, 'finance', 'expense_with_receipts.pdf')
EXPECTED_PAGE_COUNT = 7
MARGIN = 72  # 1 inch margin in points
CENTER_TOLERANCE = 15  # tolerance in points for centering check


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist and be a valid PDF
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open output PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output PDF has exactly 7 pages (0.3 points)
    # This checks that all 7 receipt images were extracted and placed on separate pages
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 1 — PDF has {page_count} pages as expected (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGE_COUNT} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each page has exactly 1 image (0.3 points)
    # Verifies the one-image-per-page requirement
    try:
        pages_with_one_image = 0
        total_pages_to_check = min(doc.page_count, EXPECTED_PAGE_COUNT)
        for i in range(total_pages_to_check):
            page = doc[i]
            images = page.get_images(full=True)
            if len(images) == 1:
                pages_with_one_image += 1
            else:
                print(f"  Page {i}: expected 1 image, found {len(images)}")

        if total_pages_to_check > 0 and pages_with_one_image == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 2 — All {EXPECTED_PAGE_COUNT} pages have exactly 1 image (0.3 pts)")
            total_score += 0.3
        elif total_pages_to_check > 0:
            # Partial credit: proportion of pages with correct image count
            ratio = pages_with_one_image / EXPECTED_PAGE_COUNT
            partial = round(0.3 * ratio, 2)
            print(f"PARTIAL: Component 2 — {pages_with_one_image}/{EXPECTED_PAGE_COUNT} pages have exactly 1 image ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages to check")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Images are centered on their pages (0.2 points)
    # Center of each image should be close to center of page
    try:
        centered_count = 0
        total_pages_to_check = min(doc.page_count, EXPECTED_PAGE_COUNT)
        for i in range(total_pages_to_check):
            page = doc[i]
            img_info_list = page.get_image_info()
            if len(img_info_list) >= 1:
                info = img_info_list[0]
                bbox = info['bbox']
                pw, ph = page.rect.width, page.rect.height
                img_cx = (bbox[0] + bbox[2]) / 2
                img_cy = (bbox[1] + bbox[3]) / 2
                page_cx = pw / 2
                page_cy = ph / 2
                dx = abs(img_cx - page_cx)
                dy = abs(img_cy - page_cy)
                if dx <= CENTER_TOLERANCE and dy <= CENTER_TOLERANCE:
                    centered_count += 1
                else:
                    print(f"  Page {i}: image center ({img_cx:.1f},{img_cy:.1f}) off from page center ({page_cx:.1f},{page_cy:.1f}) by ({dx:.1f},{dy:.1f})")

        if total_pages_to_check > 0 and centered_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 3 — All {EXPECTED_PAGE_COUNT} images are centered (0.2 pts)")
            total_score += 0.2
        elif total_pages_to_check > 0:
            ratio = centered_count / EXPECTED_PAGE_COUNT
            partial = round(0.2 * ratio, 2)
            print(f"PARTIAL: Component 3 — {centered_count}/{EXPECTED_PAGE_COUNT} images centered ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages to check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Images are scaled to fit within page margins (0.2 points)
    # Images should not exceed the area defined by MARGIN on all sides
    try:
        within_margins_count = 0
        total_pages_to_check = min(doc.page_count, EXPECTED_PAGE_COUNT)
        for i in range(total_pages_to_check):
            page = doc[i]
            img_info_list = page.get_image_info()
            if len(img_info_list) >= 1:
                info = img_info_list[0]
                bbox = info['bbox']
                pw, ph = page.rect.width, page.rect.height
                # Check image is within margin boundaries (with small tolerance)
                tol = 5  # small tolerance in points
                if (bbox[0] >= MARGIN - tol and
                    bbox[1] >= MARGIN - tol and
                    bbox[2] <= pw - MARGIN + tol and
                    bbox[3] <= ph - MARGIN + tol):
                    within_margins_count += 1
                else:
                    print(f"  Page {i}: image bbox ({bbox[0]:.1f},{bbox[1]:.1f},{bbox[2]:.1f},{bbox[3]:.1f}) exceeds margins")

        if total_pages_to_check > 0 and within_margins_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 4 — All {EXPECTED_PAGE_COUNT} images fit within margins (0.2 pts)")
            total_score += 0.2
        elif total_pages_to_check > 0:
            ratio = within_margins_count / EXPECTED_PAGE_COUNT
            partial = round(0.2 * ratio, 2)
            print(f"PARTIAL: Component 4 — {within_margins_count}/{EXPECTED_PAGE_COUNT} images within margins ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No pages to check")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
    verify_task()
