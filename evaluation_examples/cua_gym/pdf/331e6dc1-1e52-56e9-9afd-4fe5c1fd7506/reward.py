"""
Reward Script: Rotate PDF pages with specific rotations
Task ID: pdf_fm_089
Domain: pdf
Scoring:
  - Component 1 (0.15): Output file exists with correct page count (6 pages)
  - Component 2 (0.20): Page 1 rotated 90 degrees CW
  - Component 3 (0.20): Page 2 rotated 180 degrees
  - Component 4 (0.20): Page 3 rotated 270 degrees CW
  - Component 5 (0.25): Pages 4-6 unchanged (rotation 0)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_089'

# The task asks to save as ~/Documents/test_rotations_fixed.pdf
OUTPUT_PATH = os.path.join(WORKDIR, 'Documents', 'test_rotations_fixed.pdf')

# Expected rotations per page (0-indexed)
EXPECTED_ROTATIONS = {
    0: 90,   # Page 1: 90 CW (east)
    1: 180,  # Page 2: 180 (south)
    2: 270,  # Page 3: 270 CW (west)
    3: 0,    # Page 4: unchanged
    4: 0,    # Page 5: unchanged
    5: 0,    # Page 6: unchanged
}

EXPECTED_PAGE_COUNT = 6


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists and has 6 pages (0.15 points)
    try:
        if not os.path.exists(file_path):
            print(f"FAIL: Component 1 -- Output file not found: {file_path}")
            print("REWARD: 0.0")
            return 0.0

        doc = pymupdf.open(file_path)
        page_count = len(doc)

        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 1 -- Output file exists with {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected {EXPECTED_PAGE_COUNT} pages, found {page_count}")
            doc.close()
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 -- Cannot load file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Page 1 rotation == 90 (0.20 points)
    try:
        rotation = doc[0].rotation
        if rotation == 90:
            print(f"PASS: Component 2 -- Page 1 rotation is {rotation} (expected 90) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 -- Page 1 rotation is {rotation}, expected 90")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Page 2 rotation == 180 (0.20 points)
    try:
        rotation = doc[1].rotation
        if rotation == 180:
            print(f"PASS: Component 3 -- Page 2 rotation is {rotation} (expected 180) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- Page 2 rotation is {rotation}, expected 180")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Page 3 rotation == 270 (0.20 points)
    try:
        rotation = doc[2].rotation
        if rotation == 270:
            print(f"PASS: Component 4 -- Page 3 rotation is {rotation} (expected 270) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 -- Page 3 rotation is {rotation}, expected 270")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Pages 4-6 unchanged at rotation 0 (0.25 points)
    try:
        unchanged_count = 0
        for idx in [3, 4, 5]:
            rotation = doc[idx].rotation
            if rotation == 0:
                unchanged_count += 1
                print(f"  Page {idx+1} rotation is {rotation} (expected 0) -- OK")
            else:
                print(f"  Page {idx+1} rotation is {rotation} (expected 0) -- WRONG")

        if unchanged_count == 3:
            print(f"PASS: Component 5 -- Pages 4-6 all have rotation 0 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 5 -- Only {unchanged_count}/3 of pages 4-6 have rotation 0")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
