"""
Reward Script: Rotate specific pages in a PDF to correct orientation
Task ID: pdf_pw_024
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists with correct page count (12 pages)
  Component 2 (0.45): Pages 3,5,7 (0-indexed: 2,4,6) corrected to rotation=0 (0.15 each)
  Component 3 (0.20): Page 10 (0-indexed: 9) corrected to rotation=0
  Component 4 (0.20): All other pages retain rotation=0
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_024'
OUTPUT_FILE = os.path.join(WORKDIR, 'Documents', 'mixed_scans_corrected.pdf')


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

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has correct page count (0.15 points)
    # This is a task-introduced change because the corrected file doesn't exist in initial_env
    try:
        page_count = doc.page_count
        if page_count == 12:
            print(f"PASS: Component 1 -- Output file has {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected 12 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Pages 3, 5, 7 (0-indexed: 2, 4, 6) have rotation=0 (0.45 points total)
    # In initial_env these pages have rotation=270; after 90-degree CW rotation they should be 0
    landscape_pages = {2: "Page 3", 4: "Page 5", 6: "Page 7"}
    for page_idx, page_name in landscape_pages.items():
        try:
            if page_idx < doc.page_count:
                rotation = doc[page_idx].rotation
                if rotation == 0:
                    print(f"PASS: Component 2 -- {page_name} (idx {page_idx}) rotation={rotation} (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 2 -- {page_name} (idx {page_idx}) expected rotation=0, found {rotation}")
            else:
                print(f"FAIL: Component 2 -- {page_name} (idx {page_idx}) does not exist")
        except Exception as e:
            print(f"ERROR: Component 2 -- {page_name}: {e}")

    # Component 3: Page 10 (0-indexed: 9) has rotation=0 (0.20 points)
    # In initial_env this page has rotation=180; after 180-degree rotation it should be 0
    try:
        if doc.page_count > 9:
            rotation = doc[9].rotation
            if rotation == 0:
                print(f"PASS: Component 3 -- Page 10 (idx 9) rotation={rotation} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 -- Page 10 (idx 9) expected rotation=0, found {rotation}")
        else:
            print(f"FAIL: Component 3 -- Page 10 (idx 9) does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: All other pages retain rotation=0 (0.20 points)
    # Pages that should be unchanged: 0,1,3,5,7,8,10,11 (0-indexed)
    unchanged_pages = [0, 1, 3, 5, 7, 8, 10, 11]
    try:
        bad_pages = []
        for page_idx in unchanged_pages:
            if page_idx < doc.page_count:
                rotation = doc[page_idx].rotation
                if rotation != 0:
                    bad_pages.append((page_idx, rotation))
            else:
                bad_pages.append((page_idx, "missing"))
        if len(bad_pages) == 0:
            print(f"PASS: Component 4 -- All unchanged pages retain rotation=0 (0.20 pts)")
            total_score += 0.20
        else:
            for page_idx, rot in bad_pages:
                print(f"FAIL: Component 4 -- Page {page_idx+1} (idx {page_idx}) expected rotation=0, found {rot}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)
