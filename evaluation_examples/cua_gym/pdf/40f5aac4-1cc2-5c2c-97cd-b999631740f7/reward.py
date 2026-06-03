"""
Reward Script: Compress PDF by converting images to JPEG with 75% quality
Task ID: pdf_mbc_082
Domain: pdf
Scoring:
  Component 1: Output file exists (0.15)
  Component 2: Page count preserved at 30 (0.20)
  Component 3: File size under 30MB (0.25)
  Component 4: All images are JPEG format (0.25)
  Component 5: Image dimensions preserved (0.15)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_082'

# Paths
OUTPUT_PATH = os.path.join(WORKDIR, 'Documents', 'photo_album_small.pdf')

# Expected values from task context
EXPECTED_PAGE_COUNT = 30
MAX_FILE_SIZE_BYTES = 30 * 1024 * 1024  # 30 MB
EXPECTED_IMAGE_WIDTH = 1200
EXPECTED_IMAGE_HEIGHT = 1600


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must be a valid PDF
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file exists and is a valid PDF (0.15 points)
    # This is task-introduced: photo_album_small.pdf does not exist in initial_env
    try:
        if doc.page_count > 0:
            print(f"PASS: Component 1 - Output file exists and is valid PDF ({doc.page_count} pages) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - PDF has 0 pages")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Page count preserved at 30 (0.20 points)
    try:
        actual_pages = doc.page_count
        if actual_pages == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 2 - Page count is {actual_pages} (expected {EXPECTED_PAGE_COUNT}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 - Page count is {actual_pages}, expected {EXPECTED_PAGE_COUNT}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: File size under 30MB (0.25 points)
    try:
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        if file_size < MAX_FILE_SIZE_BYTES:
            print(f"PASS: Component 3 - File size is {file_size_mb:.2f} MB (under 30 MB) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - File size is {file_size_mb:.2f} MB, expected under 30 MB")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: All images converted to JPEG format (0.25 points)
    try:
        jpeg_count = 0
        non_jpeg_count = 0
        non_jpeg_details = []
        for page_idx in range(doc.page_count):
            images = doc[page_idx].get_images()
            for img in images:
                xref = img[0]
                img_data = doc.extract_image(xref)
                if img_data['ext'] == 'jpeg':
                    jpeg_count += 1
                else:
                    non_jpeg_count += 1
                    non_jpeg_details.append(f"page {page_idx}: {img_data['ext']}")

        if non_jpeg_count == 0 and jpeg_count > 0:
            print(f"PASS: Component 4 - All {jpeg_count} images are JPEG format (0.25 pts)")
            total_score += 0.25
        elif jpeg_count > 0 and non_jpeg_count > 0:
            # Partial credit: proportion of images converted
            ratio = jpeg_count / (jpeg_count + non_jpeg_count)
            partial = round(0.25 * ratio, 2)
            print(f"  Non-JPEG images: {non_jpeg_details[:5]}")
            if partial > 0:
                print(f"PARTIAL: Component 4 - {jpeg_count}/{jpeg_count + non_jpeg_count} images are JPEG ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 4 - No JPEG images found. JPEG: {jpeg_count}, Other: {non_jpeg_count}")
            if non_jpeg_details:
                print(f"  Non-JPEG images: {non_jpeg_details[:5]}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Image dimensions preserved (layout unchanged) (0.15 points)
    try:
        correct_dim_count = 0
        total_images = 0
        for page_idx in range(doc.page_count):
            images = doc[page_idx].get_images()
            for img in images:
                total_images += 1
                xref = img[0]
                img_data = doc.extract_image(xref)
                w = img_data['width']
                h = img_data['height']
                if w == EXPECTED_IMAGE_WIDTH and h == EXPECTED_IMAGE_HEIGHT:
                    correct_dim_count += 1

        if total_images > 0 and correct_dim_count == total_images:
            print(f"PASS: Component 5 - All {total_images} images have preserved dimensions ({EXPECTED_IMAGE_WIDTH}x{EXPECTED_IMAGE_HEIGHT}) (0.15 pts)")
            total_score += 0.15
        elif total_images > 0:
            ratio = correct_dim_count / total_images
            partial = round(0.15 * ratio, 2)
            if partial > 0:
                print(f"PARTIAL: Component 5 - {correct_dim_count}/{total_images} images have correct dimensions ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 5 - No images found in PDF")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
