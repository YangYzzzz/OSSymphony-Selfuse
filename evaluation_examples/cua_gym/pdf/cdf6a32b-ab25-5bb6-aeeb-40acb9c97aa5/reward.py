"""
Reward Script: Convert scanned will to searchable PDF using OCR
Task ID: pdf_legal_061
Domain: pdf
Scoring:
  - Component 1: Correct page count (8 pages) — 0.15 pts
  - Component 2: Text layer present on all 8 pages — 0.40 pts
  - Component 3: Key OCR content accuracy — 0.25 pts
  - Component 4: Original images preserved on all pages — 0.20 pts
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_061'

# The task output file
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'estate', 'will_searchable.pdf')

# Minimum text length per page to consider the text layer present
# Golden pages have 850-1400 chars; use a low threshold to be flexible
MIN_TEXT_LENGTH = 50


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must be loadable as PDF
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Correct page count — 8 pages (0.15 points)
    try:
        page_count = doc.page_count
        if page_count == 8:
            print(f"PASS: Component 1 — Page count is 8 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 8 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Text layer present on all 8 pages (0.40 points)
    # Each page with text layer contributes 0.05 points (0.05 * 8 = 0.40)
    try:
        pages_with_text = 0
        for i in range(min(doc.page_count, 8)):
            page = doc[i]
            text = page.get_text("text").strip()
            if len(text) >= MIN_TEXT_LENGTH:
                pages_with_text += 1
                print(f"  Page {i}: text layer present (len={len(text)})")
            else:
                print(f"  Page {i}: NO text layer or insufficient text (len={len(text)})")

        text_score = pages_with_text * 0.05
        if pages_with_text == 8:
            print(f"PASS: Component 2 — Text layer on all 8 pages ({text_score} pts)")
            total_score += text_score
        elif pages_with_text > 0:
            print(f"PARTIAL: Component 2 — Text layer on {pages_with_text}/8 pages ({text_score} pts)")
            total_score += text_score
        else:
            print(f"FAIL: Component 2 — No text layer found on any page")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Key OCR content accuracy (0.25 points)
    # Verify specific strings that should appear in the OCR'd text
    # These are from the typed portions of the will document
    try:
        all_text = ""
        for i in range(doc.page_count):
            all_text += doc[i].get_text("text")

        key_strings = [
            ("LAST WILL AND TESTAMENT", 0.05),
            ("MARGARET ELEANOR WHITFIELD", 0.05),
            ("ARTICLE", 0.05),  # Multiple articles in the will
            ("ATTESTATION CLAUSE", 0.05),
            ("Personal Representative", 0.05),
        ]

        content_score = 0.0
        for search_str, points in key_strings:
            if search_str.lower() in all_text.lower():
                print(f"  FOUND: '{search_str}' (+{points} pts)")
                content_score += points
            else:
                print(f"  MISSING: '{search_str}'")

        if content_score >= 0.25:
            print(f"PASS: Component 3 — All key content found ({content_score} pts)")
            total_score += content_score
        elif content_score > 0:
            print(f"PARTIAL: Component 3 — Some content found ({content_score} pts)")
            total_score += content_score
        else:
            print(f"FAIL: Component 3 — No key content found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Original images preserved on all pages (0.20 points)
    # The scanned PDF should retain the original page images
    # Each page with at least one image contributes 0.025 points (0.025 * 8 = 0.20)
    try:
        pages_with_images = 0
        for i in range(min(doc.page_count, 8)):
            page = doc[i]
            images = page.get_images()
            if len(images) >= 1:
                pages_with_images += 1
                print(f"  Page {i}: {len(images)} image(s) found")
            else:
                print(f"  Page {i}: NO images found")

        image_score = pages_with_images * 0.025
        if pages_with_images == 8:
            print(f"PASS: Component 4 — Images preserved on all 8 pages ({image_score} pts)")
            total_score += image_score
        elif pages_with_images > 0:
            print(f"PARTIAL: Component 4 — Images on {pages_with_images}/8 pages ({image_score} pts)")
            total_score += image_score
        else:
            print(f"FAIL: Component 4 — No images found on any page")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
