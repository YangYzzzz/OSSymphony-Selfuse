"""
Reward Script: Optimize photo_book.pdf images, set metadata, save as photo_book_optimized.pdf
Task ID: pdf_pw_007
Domain: pdf
Scoring:
  Component 1: Output file exists and has 20 pages (0.15 pts)
  Component 2: File size is reduced (< 25 MB) (0.15 pts)
  Component 3: Images are downsampled (resolution reduced from ~1800x1200) (0.20 pts)
  Component 4: Metadata title = 'Summer Memories 2025' (0.25 pts)
  Component 5: Metadata author = 'Elena Rodriguez' (0.25 pts)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_007'
OUTPUT_FILE = os.path.join(WORKDIR, 'publishing', 'photo_book_optimized.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Try to open the PDF
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has 20 pages (content preserved) (0.15 pts)
    # This verifies the output was created AND content is intact.
    # Initial env has no photo_book_optimized.pdf, so this fails there.
    try:
        page_count = doc.page_count
        if page_count == 20:
            print(f"PASS: Component 1 -- Output PDF has 20 pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected 20 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: File size is reduced (< 25 MB target from task context) (0.15 pts)
    # Initial file is ~123 MB, golden should be significantly smaller.
    try:
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)
        if file_size_mb < 25.0:
            print(f"PASS: Component 2 -- File size {file_size_mb:.2f} MB < 25 MB target (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- File size {file_size_mb:.2f} MB >= 25 MB target")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Images are downsampled (0.20 pts)
    # Initial images are 1800x1200. Golden should have significantly smaller images.
    # At 150 DPI target, images should be roughly 750x500 for typical page sizes.
    # We check that the max image dimension across all pages is <= 1000 (well below 1800).
    try:
        max_dim = 0
        image_count = 0
        for i in range(doc.page_count):
            images = doc[i].get_images()
            for img in images:
                w, h = img[2], img[3]
                max_dim = max(max_dim, w, h)
                image_count += 1

        if image_count > 0 and max_dim <= 1000:
            print(f"PASS: Component 3 -- Images downsampled, max dimension={max_dim}, count={image_count} (0.20 pts)")
            total_score += 0.20
        elif image_count == 0:
            print(f"FAIL: Component 3 -- No images found in PDF")
        else:
            print(f"FAIL: Component 3 -- Max image dimension={max_dim} > 1000 (not sufficiently downsampled)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Metadata title = 'Summer Memories 2025' (0.25 pts)
    # Initial metadata title is empty. This is a task-introduced change.
    try:
        meta = doc.metadata
        title = (meta.get('title') or '').strip()
        if title == 'Summer Memories 2025':
            print(f"PASS: Component 4 -- Metadata title = '{title}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 -- Expected title 'Summer Memories 2025', found '{title}'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Metadata author = 'Elena Rodriguez' (0.25 pts)
    # Initial metadata author is empty. This is a task-introduced change.
    try:
        meta = doc.metadata
        author = (meta.get('author') or '').strip()
        if author == 'Elena Rodriguez':
            print(f"PASS: Component 5 -- Metadata author = '{author}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 5 -- Expected author 'Elena Rodriguez', found '{author}'")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)
