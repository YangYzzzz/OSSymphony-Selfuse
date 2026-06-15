"""
Reward Script: Add accessibility alt-text annotations to images in a PDF
Task ID: pdf_pw_048
Domain: pdf
Scoring:
  Component 1: Output file exists at correct path (0.10 pts)
  Component 2: Page count preserved at 15 pages (0.10 pts)
  Component 3: All 12 images preserved in output (0.15 pts)
  Component 4: Text annotations present near images, >= 10 of 12 (0.30 pts)
  Component 5: Annotation content quality - starts with 'Alt-text:' and has descriptive text (0.35 pts)
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_048'
OUTPUT_PATH = os.path.join(WORKDIR, 'publishing', 'accessible_guide_tagged.pdf')
EXPECTED_PAGE_COUNT = 15
EXPECTED_IMAGE_COUNT = 12
# Pages (0-indexed) that have images in the original document
IMAGE_PAGES = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
# Page 12 has 2 images, all others have 1


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at correct path (0.10 pts)
    try:
        if os.path.exists(OUTPUT_PATH) and os.path.getsize(OUTPUT_PATH) > 10000:
            print("PASS: Component 1 -- Output file exists at %s (0.10 pts)" % OUTPUT_PATH)
            total_score += 0.10
        else:
            print("FAIL: Component 1 -- Output file missing or too small at %s" % OUTPUT_PATH)
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print("ERROR: Component 1 -- %s" % e)
        print("REWARD: 0.0")
        return 0.0

    # Load the document
    try:
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print("CRITICAL: Cannot load file %s: %s" % (OUTPUT_PATH, e))
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Page count preserved at 15 pages (0.10 pts)
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_PAGE_COUNT:
            print("PASS: Component 2 -- Page count is %d as expected (0.10 pts)" % page_count)
            total_score += 0.10
        else:
            print("FAIL: Component 2 -- Expected %d pages, found %d" % (EXPECTED_PAGE_COUNT, page_count))
    except Exception as e:
        print("ERROR: Component 2 -- %s" % e)

    # Component 3: All 12 images preserved in output (0.15 pts)
    try:
        total_images = 0
        for i in range(doc.page_count):
            page = doc[i]
            imgs = page.get_images()
            total_images += len(imgs)

        if total_images >= EXPECTED_IMAGE_COUNT:
            print("PASS: Component 3 -- Found %d images (expected >= %d) (0.15 pts)" % (total_images, EXPECTED_IMAGE_COUNT))
            total_score += 0.15
        else:
            print("FAIL: Component 3 -- Expected >= %d images, found %d" % (EXPECTED_IMAGE_COUNT, total_images))
    except Exception as e:
        print("ERROR: Component 3 -- %s" % e)

    # Component 4: Text annotations present near images (0.30 pts)
    # Each image should have a nearby Text (sticky note) or FreeText annotation
    # We check pages that have images and count how many have at least one annotation
    try:
        pages_with_image_annots = 0
        total_annots_near_images = 0

        for page_idx in IMAGE_PAGES:
            if page_idx >= doc.page_count:
                continue
            page = doc[page_idx]
            imgs = page.get_images()
            annots = list(page.annots()) if page.annots() else []

            # Filter for Text or FreeText annotations (tooltip/alt-text types)
            relevant_annots = [a for a in annots if a.type[1] in ("Text", "FreeText")]

            if len(relevant_annots) >= len(imgs) and len(imgs) > 0:
                pages_with_image_annots += 1
                total_annots_near_images += len(relevant_annots)

        # We expect annotations on all 11 image-containing pages (page 12 has 2 images, 2 annots)
        # Award partial credit: proportional to pages covered
        expected_pages = len(IMAGE_PAGES)  # 11 pages have images
        coverage_ratio = pages_with_image_annots / expected_pages if expected_pages > 0 else 0

        if coverage_ratio >= 0.9:
            print("PASS: Component 4 -- %d/%d image pages have annotations, %d total annots (0.30 pts)" % (
                pages_with_image_annots, expected_pages, total_annots_near_images))
            total_score += 0.30
        elif coverage_ratio >= 0.5:
            partial = 0.30 * (coverage_ratio / 0.9)
            print("PARTIAL: Component 4 -- %d/%d image pages have annotations (%.2f pts)" % (
                pages_with_image_annots, expected_pages, partial))
            total_score += partial
        else:
            print("FAIL: Component 4 -- Only %d/%d image pages have annotations" % (
                pages_with_image_annots, expected_pages))
    except Exception as e:
        print("ERROR: Component 4 -- %s" % e)

    # Component 5: Annotation content quality (0.35 pts)
    # Annotations should have 'Alt-text:' prefix and meaningful descriptive content
    try:
        quality_annots = 0
        total_image_annots = 0

        for page_idx in IMAGE_PAGES:
            if page_idx >= doc.page_count:
                continue
            page = doc[page_idx]
            annots = list(page.annots()) if page.annots() else []

            for annot in annots:
                if annot.type[1] not in ("Text", "FreeText"):
                    continue
                total_image_annots += 1
                annot_content = annot.info.get("content", "")
                # Check: starts with Alt-text: and has meaningful length (>30 chars total)
                if annot_content.startswith("Alt-text:") and len(annot_content) > 30:
                    quality_annots += 1

        if total_image_annots == 0:
            print("FAIL: Component 5 -- No text/freetext annotations found on image pages")
        else:
            quality_ratio = quality_annots / total_image_annots
            if quality_ratio >= 0.9:
                print("PASS: Component 5 -- %d/%d annotations have proper alt-text format and content (0.35 pts)" % (
                    quality_annots, total_image_annots))
                total_score += 0.35
            elif quality_ratio >= 0.5:
                partial = 0.35 * (quality_ratio / 0.9)
                print("PARTIAL: Component 5 -- %d/%d annotations have proper format (%.2f pts)" % (
                    quality_annots, total_image_annots, partial))
                total_score += partial
            else:
                print("FAIL: Component 5 -- Only %d/%d annotations have proper alt-text format" % (
                    quality_annots, total_image_annots))
    except Exception as e:
        print("ERROR: Component 5 -- %s" % e)

    doc.close()

    final_score = min(total_score, 1.0)
    print("\nScore: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print("File not found: %s" % OUTPUT_PATH)
    print("REWARD: 0.0")
else:
    verify_task()
