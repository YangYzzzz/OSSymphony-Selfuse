"""
Reward Script: Add image watermark to every page of a PDF at 20% opacity, centered.
Task ID: pdf_fm_071
Domain: pdf
Scoring:
  Component 1: Output file exists with 12 pages (0.2 pts)
  Component 2: Every page has at least one image (watermark) (0.3 pts)
  Component 3: Watermark images are centered on each page (0.25 pts)
  Component 4: Watermark opacity is approximately 20% (smask max ~51) (0.25 pts)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_071'

BRANDED_PATH = os.path.join(WORKDIR, 'Documents', 'official_doc_branded.pdf')
EXPECTED_PAGES = 12


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has 12 pages (0.2 points)
    try:
        page_count = len(doc)
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — PDF has {page_count} pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Every page has at least one image (watermark) (0.3 points)
    try:
        pages_with_images = 0
        for i in range(len(doc)):
            imgs = doc[i].get_images()
            if len(imgs) >= 1:
                pages_with_images += 1

        if pages_with_images == EXPECTED_PAGES:
            print(f"PASS: Component 2 — All {EXPECTED_PAGES} pages have images (0.3 pts)")
            total_score += 0.3
        elif pages_with_images > 0:
            # Partial credit: fraction of pages with images
            partial = 0.3 * (pages_with_images / EXPECTED_PAGES)
            print(f"PARTIAL: Component 2 — {pages_with_images}/{EXPECTED_PAGES} pages have images ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages have images (expected all {EXPECTED_PAGES})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Watermark images are centered on each page (0.25 points)
    # The image bbox center should be close to the page center (within 30pt tolerance)
    try:
        centered_count = 0
        tolerance = 30.0  # points

        for i in range(len(doc)):
            page = doc[i]
            page_cx = page.rect.width / 2.0
            page_cy = page.rect.height / 2.0

            img_info_list = page.get_image_info()
            if not img_info_list:
                continue

            # Check the first image on the page
            img_info = img_info_list[0]
            bbox = img_info.get('bbox', None)
            if bbox is None:
                continue

            img_cx = (bbox[0] + bbox[2]) / 2.0
            img_cy = (bbox[1] + bbox[3]) / 2.0

            dx = abs(img_cx - page_cx)
            dy = abs(img_cy - page_cy)

            if dx <= tolerance and dy <= tolerance:
                centered_count += 1
            else:
                print(f"  Page {i}: image center ({img_cx:.1f},{img_cy:.1f}) vs page center ({page_cx:.1f},{page_cy:.1f}), offset=({dx:.1f},{dy:.1f})")

        if centered_count == EXPECTED_PAGES:
            print(f"PASS: Component 3 — All {EXPECTED_PAGES} images are centered (0.25 pts)")
            total_score += 0.25
        elif centered_count > 0:
            partial = 0.25 * (centered_count / EXPECTED_PAGES)
            print(f"PARTIAL: Component 3 — {centered_count}/{EXPECTED_PAGES} images centered ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No images are centered")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Watermark opacity ~20% via smask (0.25 points)
    # 20% opacity => smask max pixel value near 51 (255*0.2)
    # We check the first page's first image smask
    try:
        page = doc[0]
        imgs = page.get_images(full=True)

        if not imgs:
            print(f"FAIL: Component 4 — No images on page 0 to check opacity")
        else:
            xref = imgs[0][0]
            smask_xref = imgs[0][1]

            if smask_xref <= 0:
                print(f"FAIL: Component 4 — Image has no soft mask (no transparency/opacity applied)")
            else:
                smask_data = doc.extract_image(smask_xref)
                from PIL import Image
                import io
                import numpy as np

                smask_img = Image.open(io.BytesIO(smask_data['image']))
                arr = np.array(smask_img)
                max_val = int(arr.max())

                # 20% opacity => max around 51 (tolerance: 30-75 to account for
                # different implementation approaches)
                expected_opacity_val = 51  # 255 * 0.2
                lower_bound = 25   # ~10% opacity
                upper_bound = 80   # ~31% opacity

                if lower_bound <= max_val <= upper_bound:
                    print(f"PASS: Component 4 — Smask max={max_val} (expected ~{expected_opacity_val} for 20% opacity) (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 4 — Smask max={max_val}, expected {lower_bound}-{upper_bound} for ~20% opacity")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(BRANDED_PATH):
    print(f"File not found: {BRANDED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(BRANDED_PATH)
