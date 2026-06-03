"""
Reward Script: Overlay company logo on every page of a PDF
Task ID: pdf_pw_046
Domain: pdf
Scoring:
  Component 1 (0.3): Branded file exists with correct page count (22 pages)
  Component 2 (0.4): Every page has exactly 1 image (logo added to all pages)
  Component 3 (0.3): Logo images positioned at approx (450, 20) with size ~100x50 pts
"""

import os
import pymupdf  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_046'

BRANDED_PATH = os.path.join(WORKDIR, 'Documents', 'company_report_branded.pdf')
EXPECTED_PAGES = 22
# Expected logo rect: (450, 20, 550, 70) — tolerance of 10 pts
LOGO_X0, LOGO_Y0 = 450.0, 20.0
LOGO_X1, LOGO_Y1 = 550.0, 70.0
POS_TOLERANCE = 15.0  # points


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
        doc = pymupdf.open(BRANDED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open branded PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = len(doc)

    # Component 1: Branded file has exactly 22 pages (0.3 points)
    # This checks that the output file preserves all original pages.
    # Initial env has no branded file at all, so this fails on initial.
    try:
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — Branded PDF has {page_count} pages (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Every page has at least 1 image (logo overlay) (0.4 points)
    # Initial PDF has 0 images on all pages, so this is a task-introduced change.
    # Award partial credit proportional to how many pages have the logo.
    try:
        pages_with_image = 0
        for i in range(page_count):
            imgs = doc[i].get_images()
            if len(imgs) >= 1:
                pages_with_image += 1

        if pages_with_image == page_count and page_count == EXPECTED_PAGES:
            print(f"PASS: Component 2 — All {page_count} pages have logo image (0.4 pts)")
            total_score += 0.4
        elif pages_with_image > 0:
            fraction = pages_with_image / EXPECTED_PAGES
            partial = round(0.4 * fraction, 2)
            if partial > 0:
                print(f"PARTIAL: Component 2 — {pages_with_image}/{EXPECTED_PAGES} pages have logo ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages have images (logo not added)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Logo images are positioned at approximately (450, 20, 550, 70) (0.3 points)
    # Verify position on a sample of pages. This checks the specific placement requirement.
    try:
        sample_pages = [0, 5, 10, 15, 21]  # sample across the document
        valid_sample = [p for p in sample_pages if p < page_count]
        correct_positions = 0

        for pn in valid_sample:
            page = doc[pn]
            img_info_list = page.get_image_info()
            if len(img_info_list) == 0:
                continue

            # Check the first (and expected only) image
            info = img_info_list[0]
            bbox = info["bbox"]  # (x0, y0, x1, y1)
            x0, y0, x1, y1 = bbox

            if (abs(x0 - LOGO_X0) <= POS_TOLERANCE and
                abs(y0 - LOGO_Y0) <= POS_TOLERANCE and
                abs(x1 - LOGO_X1) <= POS_TOLERANCE and
                abs(y1 - LOGO_Y1) <= POS_TOLERANCE):
                correct_positions += 1
            else:
                print(f"  Page {pn}: logo at ({x0:.1f}, {y0:.1f}, {x1:.1f}, {y1:.1f}) — expected ~({LOGO_X0}, {LOGO_Y0}, {LOGO_X1}, {LOGO_Y1})")

        if len(valid_sample) > 0 and correct_positions == len(valid_sample):
            print(f"PASS: Component 3 — Logo correctly positioned on all {len(valid_sample)} sampled pages (0.3 pts)")
            total_score += 0.3
        elif correct_positions > 0:
            fraction = correct_positions / len(valid_sample)
            partial = round(0.3 * fraction, 2)
            if partial > 0:
                print(f"PARTIAL: Component 3 — {correct_positions}/{len(valid_sample)} sampled pages have correct position ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 3 — Logo not at expected position on any sampled page")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
