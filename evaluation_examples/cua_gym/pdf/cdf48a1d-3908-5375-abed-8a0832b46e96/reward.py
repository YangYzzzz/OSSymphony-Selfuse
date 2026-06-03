"""
Reward Script: Reduce PDF file size by downsampling images to 150 DPI and compressing them.
Task ID: pdf_mbc_069
Domain: pdf
Scoring:
  Component 1: Compressed file exists at correct path        (0.15)
  Component 2: File size significantly reduced (< 20MB)      (0.25)
  Component 3: Page count preserved (8 pages)                (0.15)
  Component 4: Images downsampled (smaller dimensions)       (0.20)
  Component 5: Text remains selectable                       (0.15)
  Component 6: Images use lossy compression (JPEG) or much smaller (0.10)
"""

import os
import pymupdf  # PyMuPDF (fitz)

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_069'

COMPRESSED_PATH = os.path.join(WORKDIR, 'Documents', 'brochure_compressed.pdf')
ORIGINAL_PATH = os.path.join(WORKDIR, 'Documents', 'high_res_brochure.pdf')

# Thresholds derived from task context
MAX_COMPRESSED_SIZE_BYTES = 20 * 1024 * 1024  # 20MB target
EXPECTED_PAGE_COUNT = 8
# Original images are 3500x2800 px; downsampled to ~150 DPI should be much smaller
MAX_IMAGE_DIMENSION = 2000  # Any image dimension above this is NOT sufficiently downsampled


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================================
    # Component 1: Compressed file exists at ~/Documents/brochure_compressed.pdf
    # (0.15 points)
    # This FAILS on initial_env (file does not exist) and PASSES on golden_env
    # =========================================================================
    try:
        if os.path.isfile(COMPRESSED_PATH):
            print(f"PASS: Component 1 -- Compressed file exists at {COMPRESSED_PATH} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Compressed file not found at {COMPRESSED_PATH}")
            # No file means nothing else can be checked
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load the compressed PDF for subsequent checks
    try:
        doc = pymupdf.open(COMPRESSED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot load compressed PDF: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # =========================================================================
    # Component 2: File size significantly reduced (< 20MB)
    # (0.25 points)
    # Original is ~270MB; task requires significant compression
    # =========================================================================
    try:
        file_size = os.path.getsize(COMPRESSED_PATH)
        if file_size < MAX_COMPRESSED_SIZE_BYTES:
            print(f"PASS: Component 2 -- File size {file_size / (1024*1024):.2f}MB < 20MB (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- File size {file_size / (1024*1024):.2f}MB >= 20MB limit")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # =========================================================================
    # Component 3: Page count preserved (8 pages)
    # (0.15 points)
    # The compression should not remove pages
    # =========================================================================
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 3 -- Page count is {page_count} as expected (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- Expected {EXPECTED_PAGE_COUNT} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # =========================================================================
    # Component 4: Images downsampled (smaller dimensions than original)
    # (0.20 points)
    # Original images: 3500x2800 and 2400x1200
    # Downsampled to ~150 DPI should produce dimensions under ~2000px
    # =========================================================================
    try:
        oversized_count = 0
        total_images = 0
        for page_idx in range(doc.page_count):
            page = doc[page_idx]
            images = page.get_images()
            for img_info in images:
                xref = img_info[0]
                img_data = doc.extract_image(xref)
                w = img_data["width"]
                h = img_data["height"]
                total_images += 1
                if w > MAX_IMAGE_DIMENSION or h > MAX_IMAGE_DIMENSION:
                    oversized_count += 1
                    print(f"  Image on page {page_idx}: {w}x{h} exceeds max dimension {MAX_IMAGE_DIMENSION}")

        if total_images > 0 and oversized_count == 0:
            print(f"PASS: Component 4 -- All {total_images} images downsampled (max dim < {MAX_IMAGE_DIMENSION}) (0.20 pts)")
            total_score += 0.20
        elif total_images == 0:
            # No images at all -- task says downsample, not remove
            print(f"FAIL: Component 4 -- No images found in compressed PDF")
        else:
            print(f"FAIL: Component 4 -- Some images still exceed {MAX_IMAGE_DIMENSION}px dimension")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # =========================================================================
    # Component 5: Text remains selectable (extractable)
    # (0.15 points)
    # After compression, text should still be real text, not rasterized
    # =========================================================================
    try:
        total_text_len = 0
        for page_idx in range(doc.page_count):
            page = doc[page_idx]
            text = page.get_text()
            total_text_len += len(text.strip())

        # Original has substantial text on every page; expect at least 500 chars total
        if total_text_len >= 500:
            print(f"PASS: Component 5 -- Text is selectable, total {total_text_len} chars across all pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 -- Insufficient selectable text ({total_text_len} chars); text may be rasterized")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # =========================================================================
    # Component 6: Images use lossy compression (JPEG) or significantly smaller
    # (0.10 points)
    # Original images are PNG; compressed should use JPEG or equivalent
    # =========================================================================
    try:
        compressed_formats = []
        total_img_bytes = 0
        for page_idx in range(doc.page_count):
            page = doc[page_idx]
            images = page.get_images()
            for img_info in images:
                xref = img_info[0]
                img_data = doc.extract_image(xref)
                ext = img_data["ext"]
                img_bytes = len(img_data["image"])
                compressed_formats.append(ext)
                total_img_bytes += img_bytes

        if len(compressed_formats) > 0:
            # Check: either most are JPEG, or total image data is much smaller than original
            jpeg_count = sum(1 for f in compressed_formats if f.lower() in ("jpeg", "jpg"))
            jpeg_ratio = jpeg_count / len(compressed_formats)
            # Original total image data was ~12MB+; compressed should be much smaller
            avg_img_size = total_img_bytes / len(compressed_formats)

            if jpeg_ratio >= 0.5 or avg_img_size < 100000:
                print(f"PASS: Component 6 -- Images compressed: {jpeg_count}/{len(compressed_formats)} JPEG, avg size {avg_img_size:.0f} bytes (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 -- Images not sufficiently compressed: {jpeg_count}/{len(compressed_formats)} JPEG, avg {avg_img_size:.0f} bytes")
        else:
            print(f"FAIL: Component 6 -- No images found to verify compression format")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(COMPRESSED_PATH):
    print(f"File not found: {COMPRESSED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
