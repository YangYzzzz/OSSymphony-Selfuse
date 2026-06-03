"""
Reward Script: Reduce DPI of embedded images in a PDF to 96 DPI max
Task ID: pdf_gf1_036
Domain: pdf
Scoring:
  Component 1: Compressed file exists and is valid PDF (0.15)
  Component 2: Compressed file has 5 pages (0.15)
  Component 3: Same number of images as original (10) (0.20)
  Component 4: File size reduced by at least 50% (0.25)
  Component 5: All image dimensions are reduced from originals (0.25)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_036'

ORIGINAL_PATH = os.path.join(WORKDIR, 'Documents', 'photo_report.pdf')
COMPRESSED_PATH = os.path.join(WORKDIR, 'Documents', 'photo_report_compressed.pdf')

# Known original image dimensions (from initial_env exploration)
# Each page has 2 images: 2400x1800 and 1200x900
ORIGINAL_IMAGE_COUNT = 10
EXPECTED_PAGES = 5


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: original file must exist (gate, not scored)
    if not os.path.exists(ORIGINAL_PATH):
        print(f"CRITICAL: Original file not found: {ORIGINAL_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Compressed file exists and is a valid PDF (0.15 points)
    try:
        import fitz
        if not os.path.exists(COMPRESSED_PATH):
            print(f"FAIL: Component 1 — Compressed file does not exist: {COMPRESSED_PATH}")
            print("REWARD: 0.0")
            return 0.0

        doc_compressed = fitz.open(COMPRESSED_PATH)
        page_count = len(doc_compressed)
        if page_count > 0:
            print(f"PASS: Component 1 — Compressed PDF is valid with {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Compressed PDF has 0 pages")
            doc_compressed.close()
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot open compressed PDF: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Compressed file has exactly 5 pages (0.15 points)
    try:
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 2 — Page count is {page_count} as expected (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Same number of images as original (0.20 points)
    try:
        total_images = 0
        for page in doc_compressed:
            imgs = page.get_images(full=True)
            total_images += len(imgs)

        if total_images == ORIGINAL_IMAGE_COUNT:
            print(f"PASS: Component 3 — Image count is {total_images} matching original (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Expected {ORIGINAL_IMAGE_COUNT} images, found {total_images}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: File size reduced by at least 50% (0.25 points)
    try:
        original_size = os.path.getsize(ORIGINAL_PATH)
        compressed_size = os.path.getsize(COMPRESSED_PATH)
        ratio = compressed_size / original_size
        reduction_pct = (1 - ratio) * 100

        if compressed_size < original_size * 0.5:
            print(f"PASS: Component 4 — File size reduced by {reduction_pct:.1f}% "
                  f"(original: {original_size} bytes, compressed: {compressed_size} bytes) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — File size only reduced by {reduction_pct:.1f}% "
                  f"(need at least 50% reduction). "
                  f"Original: {original_size}, Compressed: {compressed_size}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: All image dimensions are reduced from originals (0.25 points)
    # The original images are 2400x1800 and 1200x900.
    # At 96 DPI, they should be significantly smaller.
    # We check that every image in the compressed PDF is smaller than the
    # smallest original dimension (1200 width).
    try:
        all_reduced = True
        image_details = []
        for i, page in enumerate(doc_compressed):
            imgs = page.get_images(full=True)
            for img in imgs:
                xref = img[0]
                pix = fitz.Pixmap(doc_compressed, xref)
                w, h = pix.width, pix.height
                image_details.append((i, xref, w, h))
                # Original smallest image is 1200x900; compressed should be well below
                if w >= 1200 or h >= 900:
                    all_reduced = False
                pix = None

        if all_reduced and len(image_details) > 0:
            print(f"PASS: Component 5 — All {len(image_details)} images have reduced dimensions (0.25 pts)")
            for pg, xref, w, h in image_details:
                print(f"  Page {pg} xref={xref}: {w}x{h}")
            total_score += 0.25
        else:
            print(f"FAIL: Component 5 — Not all images have reduced dimensions")
            for pg, xref, w, h in image_details:
                status = "OK" if (w < 1200 and h < 900) else "TOO LARGE"
                print(f"  Page {pg} xref={xref}: {w}x{h} [{status}]")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc_compressed.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
