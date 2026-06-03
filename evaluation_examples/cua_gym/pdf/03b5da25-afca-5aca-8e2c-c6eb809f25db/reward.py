"""
Reward Script: Add semi-transparent image watermark on every page of a PDF
Task ID: pdf_gf2_005
Domain: pdf
Scoring:
  Component 1 (0.20): Output file exists and has 12 pages
  Component 2 (0.30): Every page contains at least one image (watermark on all pages)
  Component 3 (0.25): Watermark images are centered on each page (within tolerance)
  Component 4 (0.25): Watermark images have semi-transparency (~30% opacity via smask)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_005'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = len(doc)

    # Component 1: Output file has exactly 12 pages (0.2 points)
    # The task says page count must remain 12.
    try:
        if page_count == 12:
            print(f"PASS: Component 1 — Page count is 12 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected 12 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Every page has at least one image (watermark on all 12 pages) (0.3 points)
    # Initial brochure has 0 images on all pages, so this checks the watermark was added.
    try:
        pages_with_images = 0
        for i in range(page_count):
            imgs = doc[i].get_images()
            if len(imgs) >= 1:
                pages_with_images += 1

        if pages_with_images == page_count and page_count == 12:
            print(f"PASS: Component 2 — All {page_count} pages have watermark images (0.3 pts)")
            total_score += 0.3
        elif pages_with_images > 0:
            # Partial credit: proportional to pages with watermarks
            partial = 0.3 * (pages_with_images / 12)
            print(f"PARTIAL: Component 2 — {pages_with_images}/{page_count} pages have images ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages contain watermark images")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Watermark images are centered on each page (0.25 points)
    # Check that the image center is within 20 pts of the page center on each page.
    try:
        centered_count = 0
        tolerance = 20.0  # points tolerance for center alignment
        for i in range(page_count):
            page = doc[i]
            pw = page.rect.width
            ph = page.rect.height
            page_cx = pw / 2.0
            page_cy = ph / 2.0
            imgs = page.get_images()
            if len(imgs) == 0:
                continue
            # Check first image (the watermark)
            xref = imgs[0][0]
            rects = page.get_image_rects(xref)
            if len(rects) == 0:
                continue
            r = rects[0]
            img_cx = (r.x0 + r.x1) / 2.0
            img_cy = (r.y0 + r.y1) / 2.0
            dx = abs(img_cx - page_cx)
            dy = abs(img_cy - page_cy)
            if dx <= tolerance and dy <= tolerance:
                centered_count += 1

        if centered_count == 12:
            print(f"PASS: Component 3 — All 12 pages have centered watermark (0.25 pts)")
            total_score += 0.25
        elif centered_count > 0:
            partial = 0.25 * (centered_count / 12)
            print(f"PARTIAL: Component 3 — {centered_count}/12 pages have centered watermark ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages have centered watermark")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Watermark has semi-transparency (~30% opacity) (0.25 points)
    # Check that images have an smask (soft mask) with pixel values indicating ~30% opacity.
    # 30% of 255 ~= 76.5. Accept max smask value in range [50, 110] as reasonable.
    try:
        import io
        import numpy as np
        from PIL import Image

        transparent_count = 0
        for i in range(page_count):
            imgs = doc[i].get_images()
            if len(imgs) == 0:
                continue
            smask_xref = imgs[0][1]
            if smask_xref <= 0:
                # No smask means no transparency
                continue
            smask_data = doc.extract_image(smask_xref)
            smask_img = Image.open(io.BytesIO(smask_data['image']))
            arr = np.array(smask_img)
            max_val = int(arr.max())
            # 30% opacity: max smask value should be around 76 (0.3 * 255)
            # Accept range [50, 110] to allow some flexibility
            if 50 <= max_val <= 110:
                transparent_count += 1

        if transparent_count == 12:
            print(f"PASS: Component 4 — All 12 pages have semi-transparent watermark (~30% opacity) (0.25 pts)")
            total_score += 0.25
        elif transparent_count > 0:
            partial = 0.25 * (transparent_count / 12)
            print(f"PARTIAL: Component 4 — {transparent_count}/12 pages have correct transparency ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No pages have semi-transparent watermark (smask max not in [50, 110])")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/marketing/brochure_watermarked.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
