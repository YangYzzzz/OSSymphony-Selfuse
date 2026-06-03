"""
Reward Script: Create APPROVED stamp PNG and place on purchase order PDF
Task ID: pdf_cross_077
Domain: pdf
Scoring:
  Component 1 (0.25): approved_stamp.png exists and is 200x80 pixels
  Component 2 (0.25): approved_stamp.png has green pixels (~#228B22), white pixels (text), and drop shadow pixels
  Component 3 (0.25): purchase_order_approved.pdf exists and has an image embedded on page 1
  Component 4 (0.25): The embedded image on page 1 is at position near (400, 100) with correct dimensions 200x80
"""

import os

WORKDIR = '/home/user/Documents'
STAMP_PATH = f'{WORKDIR}/approved_stamp.png'
APPROVED_PDF_PATH = f'{WORKDIR}/purchase_order_approved.pdf'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: approved_stamp.png exists and is 200x80 pixels (0.25 points)
    try:
        if not os.path.exists(STAMP_PATH):
            print(f"FAIL: Component 1 — approved_stamp.png not found at {STAMP_PATH}")
        else:
            from PIL import Image
            img = Image.open(STAMP_PATH)
            width, height = img.size
            if width == 200 and height == 80:
                print(f"PASS: Component 1 — approved_stamp.png is 200x80 pixels (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — approved_stamp.png is {width}x{height}, expected 200x80")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: approved_stamp.png has green pixels, white pixels (text), and drop shadow pixels (0.25 points)
    try:
        if not os.path.exists(STAMP_PATH):
            print(f"FAIL: Component 2 — approved_stamp.png not found, cannot check colors")
        else:
            import numpy as np
            from PIL import Image
            img = Image.open(STAMP_PATH)
            # Convert to RGBA to handle transparency
            img_rgba = img.convert('RGBA')
            arr = np.array(img_rgba)

            # Check for green pixels approximating #228B22 (R=34, G=139, B=34)
            # Be tolerant: R < 80, G > 90, B < 80, and opaque
            green_mask = (
                (arr[:, :, 0] < 80) &
                (arr[:, :, 1] > 90) &
                (arr[:, :, 2] < 80) &
                (arr[:, :, 3] > 100)
            )
            green_count = int(green_mask.sum())

            # Check for white pixels — text 'APPROVED' in white (R>200, G>200, B>200, opaque)
            white_mask = (
                (arr[:, :, 0] > 200) &
                (arr[:, :, 1] > 200) &
                (arr[:, :, 2] > 200) &
                (arr[:, :, 3] > 100)
            )
            white_count = int(white_mask.sum())

            # Check for drop shadow pixels — dark semi-transparent or dark opaque
            # Shadow: low RGB values but some alpha (RGBA) or just dark pixels
            shadow_mask = (
                (arr[:, :, 0] < 100) &
                (arr[:, :, 1] < 100) &
                (arr[:, :, 2] < 100) &
                (arr[:, :, 3] > 10) &
                (arr[:, :, 3] < 230)  # semi-transparent = shadow
            )
            shadow_count = int(shadow_mask.sum())

            checks_passed = 0
            if green_count > 500:
                print(f"  PASS: green pixels found ({green_count})")
                checks_passed += 1
            else:
                print(f"  FAIL: insufficient green pixels ({green_count}, expected >500)")

            if white_count > 50:
                print(f"  PASS: white pixels found ({white_count})")
                checks_passed += 1
            else:
                print(f"  FAIL: insufficient white pixels ({white_count}, expected >50)")

            if shadow_count > 20:
                print(f"  PASS: drop shadow pixels found ({shadow_count})")
                checks_passed += 1
            else:
                print(f"  FAIL: insufficient drop shadow pixels ({shadow_count}, expected >20)")

            if checks_passed == 3:
                print(f"PASS: Component 2 — stamp has green background, white text, and drop shadow (0.25 pts)")
                total_score += 0.25
            elif checks_passed >= 2:
                print(f"PARTIAL: Component 2 — {checks_passed}/3 color checks passed (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — only {checks_passed}/3 color checks passed")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: purchase_order_approved.pdf exists with an image on page 1 (0.25 points)
    try:
        if not os.path.exists(APPROVED_PDF_PATH):
            print(f"FAIL: Component 3 — purchase_order_approved.pdf not found at {APPROVED_PDF_PATH}")
        else:
            try:
                import pymupdf
            except ImportError:
                import fitz as pymupdf

            doc = pymupdf.open(APPROVED_PDF_PATH)
            page = doc[0]  # page 1 (0-indexed)
            images_on_page1 = page.get_images()
            doc.close()

            if len(images_on_page1) >= 1:
                print(f"PASS: Component 3 — purchase_order_approved.pdf has {len(images_on_page1)} image(s) on page 1 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — no images found on page 1 of purchase_order_approved.pdf")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: The embedded image on page 1 is at position near (400, 100) and has 200x80 dimensions (0.25 points)
    try:
        if not os.path.exists(APPROVED_PDF_PATH):
            print(f"FAIL: Component 4 — purchase_order_approved.pdf not found, cannot check image position")
        else:
            try:
                import pymupdf
            except ImportError:
                import fitz as pymupdf

            doc = pymupdf.open(APPROVED_PDF_PATH)
            page = doc[0]
            images_on_page1 = page.get_images()

            position_ok = False
            dimension_ok = False

            for img_info in images_on_page1:
                xref = img_info[0]
                img_width = img_info[2]
                img_height = img_info[3]

                # Check image dimensions match original stamp (200x80)
                if img_width == 200 and img_height == 80:
                    dimension_ok = True
                    print(f"  PASS: embedded image has correct dimensions {img_width}x{img_height}")
                else:
                    print(f"  INFO: embedded image dimensions: {img_width}x{img_height} (expected 200x80)")

                # Check image placement position
                rects = page.get_image_rects(xref)
                for rect in rects:
                    # rect is (x0, y0, x1, y1): the image is placed from (x0,y0) to (x1,y1)
                    x0, y0, x1, y1 = rect.x0, rect.y0, rect.x1, rect.y1
                    print(f"  INFO: image rect: ({x0:.1f}, {y0:.1f}, {x1:.1f}, {y1:.1f})")
                    # Position should be near (400, 100) — allow tolerance of 15 points
                    if abs(x0 - 400.0) <= 15 and abs(y0 - 100.0) <= 15:
                        position_ok = True
                        print(f"  PASS: image placed near (400, 100) — actual ({x0:.1f}, {y0:.1f})")
                    else:
                        print(f"  FAIL: image x0={x0:.1f} (expected ~400), y0={y0:.1f} (expected ~100)")

            doc.close()

            if position_ok and dimension_ok:
                print(f"PASS: Component 4 — stamp correctly positioned at ~(400,100) with 200x80 dims (0.25 pts)")
                total_score += 0.25
            elif position_ok or dimension_ok:
                print(f"PARTIAL: Component 4 — position_ok={position_ok}, dimension_ok={dimension_ok} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — stamp not positioned correctly or wrong dimensions")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()
