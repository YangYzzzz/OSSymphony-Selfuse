"""
Reward Script: Extract images from PDF and save as PNGs
Task ID: pdf_gf3_006
Domain: pdf
Scoring:
  Component 1 (0.15): extracted_images directory exists
  Component 2 (0.25): Correct number of PNG files (18)
  Component 3 (0.20): All files follow naming convention image_pageX_imgY.png
  Component 4 (0.20): All files are valid PNGs (magic bytes check)
  Component 5 (0.20): Correct page-to-image count mapping
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_006'

# Expected page-to-image-count mapping (derived from PDF analysis)
# Pages 1-10, where page 6 and 9 have 0 images
EXPECTED_PAGE_IMAGE_COUNTS = {
    1: 3,
    2: 2,
    3: 2,
    4: 1,
    5: 3,
    # page 6: 0 images
    7: 2,
    8: 2,
    # page 9: 0 images
    10: 3,
}
EXPECTED_TOTAL_IMAGES = 18

IMG_DIR = os.path.join(WORKDIR, 'reports', 'extracted_images')
NAMING_PATTERN = re.compile(r'^image_page(\d+)_img(\d+)\.png$')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: extracted_images directory exists (0.15 points)
    # This directory does NOT exist in initial_env, so it scores the task-introduced change.
    try:
        if os.path.isdir(IMG_DIR):
            print(f"PASS: Component 1 — extracted_images directory exists (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — directory {IMG_DIR} does not exist")
            # No directory means nothing else can pass; return early
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"REWARD: 0.0")
        return 0.0

    # Get list of files in the directory
    try:
        all_files = os.listdir(IMG_DIR)
        png_files = [f for f in all_files if f.endswith('.png')]
    except Exception as e:
        print(f"ERROR: Cannot list directory {IMG_DIR}: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Correct number of PNG files — 18 (0.25 points)
    # Initial_env has no directory at all, so this fails on initial.
    try:
        if len(png_files) == EXPECTED_TOTAL_IMAGES:
            print(f"PASS: Component 2 — found {len(png_files)} PNG files as expected (0.25 pts)")
            total_score += 0.25
        elif len(png_files) > 0:
            # Partial credit: proportion of expected images found (up to 0.15)
            ratio = min(len(png_files), EXPECTED_TOTAL_IMAGES) / EXPECTED_TOTAL_IMAGES
            partial = round(0.15 * ratio, 3)
            print(f"PARTIAL: Component 2 — found {len(png_files)}/{EXPECTED_TOTAL_IMAGES} PNG files ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no PNG files found in {IMG_DIR}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All files follow naming convention image_pageX_imgY.png (0.20 points)
    try:
        matched_files = [f for f in png_files if NAMING_PATTERN.match(f)]
        if len(png_files) > 0 and len(matched_files) == len(png_files):
            print(f"PASS: Component 3 — all {len(matched_files)} files follow naming convention (0.20 pts)")
            total_score += 0.20
        elif len(matched_files) > 0:
            ratio = len(matched_files) / len(png_files) if len(png_files) > 0 else 0
            partial = round(0.10 * ratio, 3)
            bad_names = [f for f in png_files if f not in matched_files]
            print(f"PARTIAL: Component 3 — {len(matched_files)}/{len(png_files)} files match naming pattern ({partial} pts). Bad: {bad_names[:5]}")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — no files match naming pattern image_pageX_imgY.png")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All files are valid PNGs (magic bytes check) (0.20 points)
    try:
        valid_count = 0
        for f in png_files:
            fp = os.path.join(IMG_DIR, f)
            with open(fp, 'rb') as fh:
                header = fh.read(8)
            if header[:8] == b'\x89PNG\r\n\x1a\n':
                valid_count += 1
            else:
                print(f"  INFO: {f} does not have valid PNG header")

        if len(png_files) > 0 and valid_count == len(png_files):
            print(f"PASS: Component 4 — all {valid_count} files are valid PNGs (0.20 pts)")
            total_score += 0.20
        elif valid_count > 0:
            ratio = valid_count / len(png_files) if len(png_files) > 0 else 0
            partial = round(0.10 * ratio, 3)
            print(f"PARTIAL: Component 4 — {valid_count}/{len(png_files)} files are valid PNGs ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — no valid PNG files found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Correct page-to-image count mapping (0.20 points)
    # Parse filenames and build actual page-image count map, then compare to expected.
    try:
        actual_page_counts = {}
        for f in matched_files:
            m = NAMING_PATTERN.match(f)
            if m:
                page_num = int(m.group(1))
                actual_page_counts[page_num] = actual_page_counts.get(page_num, 0) + 1

        # Check how many pages have the correct image count
        correct_pages = 0
        total_expected_pages = len(EXPECTED_PAGE_IMAGE_COUNTS)
        for page, expected_count in EXPECTED_PAGE_IMAGE_COUNTS.items():
            actual_count = actual_page_counts.get(page, 0)
            if actual_count == expected_count:
                correct_pages += 1
            else:
                print(f"  INFO: Page {page}: expected {expected_count} images, found {actual_count}")

        # Also check that no unexpected pages have images
        unexpected_pages = set(actual_page_counts.keys()) - set(EXPECTED_PAGE_IMAGE_COUNTS.keys())
        has_unexpected = len(unexpected_pages) > 0
        if has_unexpected:
            for p in unexpected_pages:
                print(f"  INFO: Unexpected images on page {p}: {actual_page_counts[p]} files")

        if correct_pages == total_expected_pages and not has_unexpected:
            print(f"PASS: Component 5 — all {total_expected_pages} pages have correct image counts (0.20 pts)")
            total_score += 0.20
        elif correct_pages > 0:
            ratio = correct_pages / total_expected_pages
            partial = round(0.10 * ratio, 3)
            print(f"PARTIAL: Component 5 — {correct_pages}/{total_expected_pages} pages correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — no pages have correct image counts")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
