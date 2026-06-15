"""
Reward Script: Create letterhead header in GIMP and apply to PDF
Task ID: pdf_cross_086
Domain: pdf (cross-domain with GIMP)
Scoring:
  - Component 1: letterhead_header.png exists with correct 2100x300 dimensions (0.20)
  - Component 2: letterhead_header.png has navy-to-white gradient (navy at left, white at right) (0.20)
  - Component 3: letter_with_header.pdf exists and has 3 pages (0.20)
  - Component 4: All 3 pages of letter_with_header.pdf contain exactly 1 image placed at the top (0.30)
  - Component 5: The embedded header image in PDF is 2100x300 pixels (0.10)
Total: 1.0
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

PIL_IMPORT_ERROR = None
try:
    from PIL import Image
    import numpy as np
except ImportError as _e:
    PIL_IMPORT_ERROR = str(_e)

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_086'

HEADER_PNG = os.path.join(WORKDIR, 'letterhead_header.png')
RESULT_PDF = os.path.join(WORKDIR, 'letter_with_header.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: letterhead_header.png must exist (not scored on its own)
    if not os.path.exists(HEADER_PNG):
        print(f"FAIL: letterhead_header.png not found at {HEADER_PNG}")
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: letterhead_header.png has correct dimensions 2100x300 (0.20 points)
    try:
        if PIL_IMPORT_ERROR is None:
            img = Image.open(HEADER_PNG)
            w, h = img.size
            if w == 2100 and h == 300:
                print(f"PASS: Component 1 — letterhead_header.png is {w}x{h} (correct 2100x300) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — expected 2100x300, got {w}x{h}")
        else:
            print(f"ERROR: Component 1 — PIL not available: {PIL_IMPORT_ERROR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: letterhead_header.png has navy-to-white gradient (0.20 points)
    # Navy (#000080) is at the left edge, white (#FFFFFF) at the right edge.
    # Check: top-left pixel is navy-ish (R<30, G<30, B>100), right side has light/white pixels.
    try:
        if PIL_IMPORT_ERROR is None:
            img = Image.open(HEADER_PNG)
            arr = np.array(img)
            # Top-left pixel should be close to navy (0, 0, 128)
            tl = arr[0, 0, :]
            navy_ok = int(tl[0]) < 30 and int(tl[1]) < 30 and int(tl[2]) > 80
            # Top-right pixel should be close to white (>200 in all channels)
            tr = arr[0, -1, :]
            white_ok = int(tr[0]) > 200 and int(tr[1]) > 200 and int(tr[2]) > 200
            if navy_ok and white_ok:
                print(f"PASS: Component 2 — gradient from navy {tuple(tl)} (left) to white {tuple(tr)} (right) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — left pixel: {tuple(tl)}, right pixel: {tuple(tr)}, expected navy->white gradient")
        else:
            print(f"ERROR: Component 2 — PIL not available: {PIL_IMPORT_ERROR}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Precondition gate: letter_with_header.pdf must exist
    if not os.path.exists(RESULT_PDF):
        print(f"FAIL: letter_with_header.pdf not found at {RESULT_PDF}")
        print("\nScore: {:.1f}/1.0".format(total_score))
        print(f"REWARD: {total_score:.1f}")
        return total_score

    # Component 3: letter_with_header.pdf exists and has exactly 3 pages (0.20 points)
    try:
        doc = pymupdf.open(RESULT_PDF)
        page_count = doc.page_count
        if page_count == 3:
            print(f"PASS: Component 3 — letter_with_header.pdf has {page_count} pages (correct) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — expected 3 pages, got {page_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — cannot open PDF: {e}")
        print("\nScore: {:.1f}/1.0".format(total_score))
        print(f"REWARD: {min(total_score, 1.0):.1f}")
        return min(total_score, 1.0)

    # Component 4: All 3 pages have exactly 1 image, placed at the top (0.30 points)
    # "At the top" = the image's top y-coordinate (bbox[1]) is within 10 points of 0
    try:
        pages_with_top_image = 0
        for i in range(doc.page_count):
            page = doc[i]
            blocks = page.get_text('dict')['blocks']
            img_blocks = [b for b in blocks if b['type'] == 1]
            if len(img_blocks) == 1:
                bbox = img_blocks[0]['bbox']
                top_y = bbox[1]
                if top_y < 10.0:
                    pages_with_top_image += 1
                else:
                    print(f"  FAIL: Page {i} image top y={top_y:.2f} (not at top of page)")
            else:
                print(f"  FAIL: Page {i} has {len(img_blocks)} image blocks (expected 1)")

        if pages_with_top_image == 3:
            print(f"PASS: Component 4 — all 3 pages have 1 header image at page top (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 4 — {pages_with_top_image}/3 pages have header image at top")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: The embedded header image is 2100x300 pixels (0.10 points)
    # Check the first image on page 0
    try:
        page0 = doc[0]
        images = page0.get_images(full=True)
        if images:
            xref = images[0][0]
            img_info = doc.extract_image(xref)
            img_w = img_info['width']
            img_h = img_info['height']
            if img_w == 2100 and img_h == 300:
                print(f"PASS: Component 5 — embedded header image is {img_w}x{img_h} (correct 2100x300) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — embedded image is {img_w}x{img_h}, expected 2100x300")
        else:
            print("FAIL: Component 5 — no images found on page 0")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
