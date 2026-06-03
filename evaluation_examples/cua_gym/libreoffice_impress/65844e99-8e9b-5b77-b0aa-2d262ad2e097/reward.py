"""
Reward Script: Export presentation as PDF with JPEG compression at 50% quality
Task ID: impstruct_047
Domain: libreoffice_impress
Scoring:
  Component 1 (0.30): compressed.pdf exists at correct path and is a valid PDF
  Component 2 (0.30): PDF has 15 pages matching the 15 slides
  Component 3 (0.25): PDF images use JPEG compression (DCTDecode)
  Component 4 (0.15): PDF contains image XObjects (images were included)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'impstruct_047'
PDF_PATH = os.path.join(WORKDIR, 'Desktop', 'compressed.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    if not os.path.isfile(PDF_PATH):
        print(f"CRITICAL: File not found: {PDF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(PDF_PATH, 'rb') as f:
            pdf_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {PDF_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid PDF file at correct location (0.30 points)
    # Checks that the file is a genuine PDF (not empty, not corrupt header)
    try:
        is_valid_pdf = pdf_content[:5] == b'%PDF-'
        file_size = len(pdf_content)
        if is_valid_pdf and file_size > 1000:
            print(f"PASS: Component 1 — Valid PDF at {PDF_PATH}, size={file_size} bytes (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Invalid PDF header or too small. Header={pdf_content[:5]!r}, size={file_size}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: PDF has 15 pages matching the 15 slides (0.30 points)
    # Count /Type /Page (but not /Type /Pages which is the page tree node)
    try:
        page_matches = re.findall(rb'/Type\s*/Page(?!s)', pdf_content)
        page_count = len(page_matches)
        if page_count == 15:
            print(f"PASS: Component 2 — PDF has 15 pages matching 15 slides (0.30 pts)")
            total_score += 0.30
        elif page_count > 0:
            # Partial credit: has pages but wrong count
            partial = round(0.30 * min(page_count, 15) / 15.0, 2)
            if partial > 0:
                print(f"PARTIAL: Component 2 — PDF has {page_count} pages, expected 15 ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 2 — Could not detect any pages in PDF")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Images use JPEG compression / DCTDecode (0.25 points)
    # When PDF export uses JPEG quality setting, images are stored with DCTDecode filter
    try:
        jpeg_stream_count = pdf_content.count(b'/DCTDecode')
        if jpeg_stream_count > 0:
            print(f"PASS: Component 3 — Found {jpeg_stream_count} JPEG-compressed image streams (0.25 pts)")
            total_score += 0.25
        else:
            # Check if there are any images at all (could be FlateDecode instead)
            flate_images = pdf_content.count(b'/FlateDecode')
            print(f"FAIL: Component 3 — No JPEG (DCTDecode) streams found. FlateDecode count: {flate_images}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: PDF contains image XObjects (0.15 points)
    # Verifies that images from the presentation were embedded in the PDF
    try:
        image_xobjects = re.findall(rb'/Subtype\s*/Image', pdf_content)
        image_count = len(image_xobjects)
        if image_count >= 10:
            # The presentation has many images across 15 slides; expect at least 10
            print(f"PASS: Component 4 — Found {image_count} image XObjects in PDF (0.15 pts)")
            total_score += 0.15
        elif image_count > 0:
            partial = round(0.15 * (image_count / 10.0), 2)
            if partial > 0:
                print(f"PARTIAL: Component 4 — Found {image_count} images, expected >=10 ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 4 — No image XObjects found in PDF")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
