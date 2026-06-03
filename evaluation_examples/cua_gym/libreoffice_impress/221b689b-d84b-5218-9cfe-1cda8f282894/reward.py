"""
Reward Script: Export presentation as PDF handout (6 slides per page) with slide numbers
Task ID: impress_tm_094
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.25): PDF has exactly 4 pages (24 slides / 6 per page)
  - Component 2 (0.30): Each page has 6 slide thumbnail images
  - Component 3 (0.25): Slide numbers present as text labels on each page
  - Component 4 (0.20): PDF is landscape orientation (handout format)
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_094'
PDF_PATH = '/home/user/Documents/compact_handout.pdf'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: PDF file must exist at the specified path
    if not os.path.exists(PDF_PATH):
        print(f"CRITICAL: PDF not found at {PDF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz  # PyMuPDF
        doc = fitz.open(PDF_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {PDF_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = len(doc)

    # Component 1: PDF has exactly 4 pages (24 slides / 6 per page = 4 pages) (0.25 points)
    try:
        if page_count == 4:
            print(f"PASS: Component 1 — PDF has exactly 4 pages (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 4 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each page has 6 slide thumbnail images (0.30 points)
    # Award partial credit: 0.30 * (pages_with_6_images / total_pages)
    try:
        pages_with_correct_images = 0
        for i in range(page_count):
            page = doc[i]
            imgs = page.get_images(full=True)
            img_count = len(imgs)
            if img_count == 6:
                pages_with_correct_images += 1
                print(f"  Page {i+1}: {img_count} images — OK")
            else:
                print(f"  Page {i+1}: {img_count} images — expected 6")

        if page_count > 0 and pages_with_correct_images == page_count:
            print(f"PASS: Component 2 — All {page_count} pages have 6 thumbnails (0.30 pts)")
            total_score += 0.30
        elif pages_with_correct_images > 0:
            partial = 0.30 * (pages_with_correct_images / max(page_count, 4))
            print(f"PARTIAL: Component 2 — {pages_with_correct_images}/{page_count} pages have 6 thumbnails ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages have exactly 6 thumbnail images")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Slide numbers present as text on each page (0.25 points)
    # Each page should have slide number labels (e.g., "Slide 1", "Slide 2", etc.)
    # or just numbers like "1", "2", etc.
    try:
        pages_with_slide_numbers = 0
        total_expected_numbers = 0
        total_found_numbers = 0

        for i in range(page_count):
            page = doc[i]
            text = page.get_text()
            # Expected slide numbers for this page (6 per page)
            start_num = i * 6 + 1
            end_num = min(start_num + 5, 24)
            expected_nums = list(range(start_num, end_num + 1))
            total_expected_numbers += len(expected_nums)

            found_count = 0
            for num in expected_nums:
                # Check for "Slide N" pattern or just the number
                if f"Slide {num}" in text or f"slide {num}" in text.lower():
                    found_count += 1

            total_found_numbers += found_count
            if found_count >= len(expected_nums):
                pages_with_slide_numbers += 1
                print(f"  Page {i+1}: Found all {found_count} slide numbers — OK")
            elif found_count > 0:
                print(f"  Page {i+1}: Found {found_count}/{len(expected_nums)} slide numbers — partial")
            else:
                print(f"  Page {i+1}: No slide numbers found")

        if total_expected_numbers > 0 and total_found_numbers >= total_expected_numbers:
            print(f"PASS: Component 3 — All slide numbers present (0.25 pts)")
            total_score += 0.25
        elif total_found_numbers > 0:
            ratio = total_found_numbers / total_expected_numbers
            partial = 0.25 * ratio
            print(f"PARTIAL: Component 3 — {total_found_numbers}/{total_expected_numbers} slide numbers found ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No slide numbers found in PDF text")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: PDF is in landscape orientation (width > height, typical for handouts) (0.20 points)
    try:
        if page_count > 0:
            page = doc[0]
            rect = page.rect
            width = rect.width
            height = rect.height
            if width > height:
                print(f"PASS: Component 4 — Landscape orientation ({width:.1f} x {height:.1f}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Expected landscape (width > height), got {width:.1f} x {height:.1f}")
        else:
            print(f"FAIL: Component 4 — No pages to check orientation")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()
