"""
Reward Script: Reorder bookmarks in proceedings.pdf
Task ID: pdf_mbc_041
Domain: pdf
Scoring:
  Component 1 (0.3): Correct number of bookmarks (5) with correct titles
  Component 2 (0.3): Correct order of bookmarks
  Component 3 (0.4): Correct page destinations for each bookmark
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_041'

# Expected bookmark order and page destinations (from task context)
EXPECTED_TOC = [
    [1, 'Keynote Address', 1],
    [1, 'Session A', 8],
    [1, 'Session B', 15],
    [1, 'Session C', 30],
    [1, 'Closing Remarks', 50],
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        toc = doc.get_toc()
    except Exception as e:
        print(f"CRITICAL: Cannot read TOC: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    doc.close()

    # Component 1: Correct number of bookmarks with correct titles (0.3 points)
    # Initial has 5 bookmarks with the same titles but in wrong order,
    # so we check that the ORDER of titles matches expected (not just presence).
    # This component checks the first bookmark is 'Keynote Address' — which is
    # NOT true in initial (initial has 'Session B' first).
    try:
        if len(toc) != 5:
            print(f"FAIL: Component 1 — Expected 5 bookmarks, found {len(toc)}")
        else:
            actual_titles = [entry[1] for entry in toc]
            expected_titles = [entry[1] for entry in EXPECTED_TOC]
            # Check that the first bookmark is 'Keynote Address' (fails on initial)
            if actual_titles[0] == 'Keynote Address' and set(actual_titles) == set(expected_titles):
                print(f"PASS: Component 1 — 5 bookmarks present, first is 'Keynote Address' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — First bookmark is '{actual_titles[0]}', expected 'Keynote Address'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct full ordering of bookmarks (0.3 points)
    # The exact sequence must match: Keynote, Session A, Session B, Session C, Closing
    # Initial has: Session B, Closing, Session A, Keynote, Session C — fails this check
    try:
        actual_titles = [entry[1] for entry in toc]
        expected_titles = [entry[1] for entry in EXPECTED_TOC]
        if actual_titles == expected_titles:
            print(f"PASS: Component 2 — Bookmark order is correct: {actual_titles} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected order {expected_titles}, found {actual_titles}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct page destinations for each bookmark (0.4 points)
    # Each bookmark must point to the correct page. Award partial credit per bookmark.
    # Initial has same page numbers but in wrong order, so matching (title, page) pairs
    # in the correct positions will fail on initial.
    try:
        points_per_bm = 0.4 / len(EXPECTED_TOC)
        comp3_score = 0.0
        for i, expected in enumerate(EXPECTED_TOC):
            if i < len(toc):
                actual = toc[i]
                if actual[1] == expected[1] and actual[2] == expected[2]:
                    comp3_score += points_per_bm
                    print(f"  PASS: Bookmark {i+1} '{expected[1]}' -> page {expected[2]} matches")
                else:
                    print(f"  FAIL: Bookmark {i+1} expected '{expected[1]}' p{expected[2]}, "
                          f"found '{actual[1]}' p{actual[2]}")
            else:
                print(f"  FAIL: Bookmark {i+1} missing")

        # Round to avoid floating point issues
        comp3_score = round(comp3_score, 2)
        if comp3_score > 0:
            print(f"PASS: Component 3 — Bookmark destinations ({comp3_score} pts)")
            total_score += comp3_score
        else:
            print(f"FAIL: Component 3 — No bookmark positions matched correctly")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/proceedings.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
