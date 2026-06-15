"""
Reward Script: Create hierarchical bookmarks for trial binder PDF
Task ID: pdf_legal_026
Domain: pdf
Scoring:
  Component 1 (0.2): Correct total TOC entry count (9)
  Component 2 (0.2): Top-level bookmarks correct (3 entries with correct titles)
  Component 3 (0.3): Child bookmarks correct (6 entries with correct titles and levels)
  Component 4 (0.3): All bookmark page numbers correct
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_026'

# Expected TOC: [level, title, page_number]
EXPECTED_TOC = [
    [1, 'Pleadings', 1],
    [2, 'Complaint', 1],
    [2, 'Answer', 15],
    [1, 'Discovery', 30],
    [2, 'Interrogatories', 30],
    [2, 'Depositions', 45],
    [1, 'Motions', 80],
    [2, 'Motion in Limine', 80],
    [2, 'Summary Judgment', 95],
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist and be loadable
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

    print(f"INFO: Found {len(toc)} TOC entries")
    for entry in toc:
        print(f"  Level {entry[0]}: '{entry[1]}' -> page {entry[2]}")

    # Component 1: Correct total TOC entry count (0.2 points)
    # Expected: 9 entries (3 top-level + 6 children)
    try:
        if len(toc) == 9:
            print(f"PASS: Component 1 -- TOC has exactly 9 entries (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- Expected 9 TOC entries, found {len(toc)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Top-level bookmarks correct (0.2 points)
    # Expected: 3 level-1 entries with titles 'Pleadings', 'Discovery', 'Motions'
    try:
        top_level = [entry for entry in toc if entry[0] == 1]
        expected_top = ['Pleadings', 'Discovery', 'Motions']
        actual_top = [entry[1].strip() for entry in top_level]

        if len(top_level) == 3 and actual_top == expected_top:
            print(f"PASS: Component 2 -- 3 top-level bookmarks correct: {actual_top} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- Expected top-level {expected_top}, found {actual_top}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Child bookmarks correct (0.3 points)
    # Expected: 6 level-2 entries with correct titles in correct order
    try:
        children = [entry for entry in toc if entry[0] == 2]
        expected_children = ['Complaint', 'Answer', 'Interrogatories', 'Depositions',
                             'Motion in Limine', 'Summary Judgment']
        actual_children = [entry[1].strip() for entry in children]

        if len(children) == 6 and actual_children == expected_children:
            print(f"PASS: Component 3 -- 6 child bookmarks correct: {actual_children} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 -- Expected children {expected_children}, found {actual_children}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: All bookmark page numbers correct (0.3 points)
    # Verify each entry points to the correct page
    try:
        if len(toc) == len(EXPECTED_TOC):
            mismatches = []
            for actual, expected in zip(toc, EXPECTED_TOC):
                if actual[2] != expected[2]:
                    mismatches.append(
                        f"'{expected[1]}': expected page {expected[2]}, got page {actual[2]}"
                    )

            if len(mismatches) == 0:
                print(f"PASS: Component 4 -- All 9 bookmark page numbers correct (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 4 -- Page number mismatches: {'; '.join(mismatches)}")
        else:
            print(f"FAIL: Component 4 -- Cannot check pages, TOC entry count mismatch ({len(toc)} vs {len(EXPECTED_TOC)})")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/legal/trial_binder_indexed.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
