"""
Reward Script: Build a complete bookmark hierarchy for dissertation.pdf
Task ID: pdf_mbc_048
Domain: pdf
Scoring:
  Component 1: Bookmark count (0.2) - PDF has 11 bookmarks total
  Component 2: Top-level bookmarks correct (0.3) - 5 level-1 entries with correct titles and pages
  Component 3: Level-2 subsections correct (0.25) - 4 level-2 entries nested correctly
  Component 4: Level-3 sub-subsections correct (0.25) - 2 level-3 entries nested under 2.2
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_048'

# Expected full TOC: [level, title, page_number (1-indexed)]
EXPECTED_TOC = [
    [1, 'Abstract', 1],
    [1, 'Chapter 1: Introduction', 5],
    [2, '1.1 Background', 5],
    [2, '1.2 Motivation', 8],
    [1, 'Chapter 2: Literature Review', 12],
    [2, '2.1 Historical Context', 12],
    [2, '2.2 Current Research', 18],
    [3, '2.2.1 Method A', 18],
    [3, '2.2.2 Method B', 22],
    [1, 'Chapter 3: Methodology', 26],
    [1, 'References', 40],
]

# Top-level (level 1) entries
EXPECTED_LEVEL1 = [e for e in EXPECTED_TOC if e[0] == 1]
# Level 2 entries
EXPECTED_LEVEL2 = [e for e in EXPECTED_TOC if e[0] == 2]
# Level 3 entries
EXPECTED_LEVEL3 = [e for e in EXPECTED_TOC if e[0] == 3]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
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

    # Component 1: Bookmark count is correct (0.2 points)
    # Initial has 0 bookmarks; golden should have 11
    try:
        num_bookmarks = len(toc)
        if num_bookmarks == len(EXPECTED_TOC):
            print(f"PASS: Component 1 -- Bookmark count is {num_bookmarks} (expected {len(EXPECTED_TOC)}) (0.2 pts)")
            total_score += 0.2
        elif num_bookmarks >= 8:
            # Partial credit for close count
            partial = 0.1
            print(f"PARTIAL: Component 1 -- Bookmark count is {num_bookmarks} (expected {len(EXPECTED_TOC)}) ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- Bookmark count is {num_bookmarks} (expected {len(EXPECTED_TOC)})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Top-level (level 1) bookmarks correct (0.3 points)
    # Check that all 5 level-1 entries exist with correct titles and page numbers
    try:
        actual_level1 = [e for e in toc if e[0] == 1]
        matched = 0
        for expected in EXPECTED_LEVEL1:
            for actual in actual_level1:
                if (actual[1].strip() == expected[1].strip() and
                        actual[2] == expected[2]):
                    matched += 1
                    break
        if matched == len(EXPECTED_LEVEL1):
            print(f"PASS: Component 2 -- All {len(EXPECTED_LEVEL1)} level-1 bookmarks correct (0.3 pts)")
            total_score += 0.3
        elif matched > 0:
            partial = round(0.3 * matched / len(EXPECTED_LEVEL1), 2)
            print(f"PARTIAL: Component 2 -- {matched}/{len(EXPECTED_LEVEL1)} level-1 bookmarks correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No level-1 bookmarks matched. Found: {actual_level1}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Level-2 subsections correct (0.25 points)
    # Check that all 4 level-2 entries exist with correct titles, pages, and nesting
    try:
        actual_level2 = [e for e in toc if e[0] == 2]
        matched = 0
        for expected in EXPECTED_LEVEL2:
            for actual in actual_level2:
                if (actual[1].strip() == expected[1].strip() and
                        actual[2] == expected[2]):
                    matched += 1
                    break
        if matched == len(EXPECTED_LEVEL2):
            print(f"PASS: Component 3 -- All {len(EXPECTED_LEVEL2)} level-2 bookmarks correct (0.25 pts)")
            total_score += 0.25
        elif matched > 0:
            partial = round(0.25 * matched / len(EXPECTED_LEVEL2), 2)
            print(f"PARTIAL: Component 3 -- {matched}/{len(EXPECTED_LEVEL2)} level-2 bookmarks correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No level-2 bookmarks matched. Found: {actual_level2}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Level-3 sub-subsections correct (0.25 points)
    # Check that 2.2.1 and 2.2.2 are level-3 children of 2.2 Current Research
    try:
        actual_level3 = [e for e in toc if e[0] == 3]
        matched = 0
        for expected in EXPECTED_LEVEL3:
            for actual in actual_level3:
                if (actual[1].strip() == expected[1].strip() and
                        actual[2] == expected[2]):
                    matched += 1
                    break

        # Also verify hierarchical nesting: level-3 entries must appear after '2.2 Current Research' (level 2)
        # and before the next level-1 or level-2 entry that isn't part of section 2.2
        hierarchy_ok = False
        if matched == len(EXPECTED_LEVEL3):
            # Find index of '2.2 Current Research' in the TOC
            parent_idx = None
            for i, entry in enumerate(toc):
                if entry[0] == 2 and '2.2' in entry[1] and 'Current Research' in entry[1]:
                    parent_idx = i
                    break
            if parent_idx is not None:
                # Check that the two level-3 entries follow immediately after parent
                children_found = 0
                for i in range(parent_idx + 1, len(toc)):
                    if toc[i][0] == 3:
                        children_found += 1
                    else:
                        break
                if children_found == 2:
                    hierarchy_ok = True

        if matched == len(EXPECTED_LEVEL3) and hierarchy_ok:
            print(f"PASS: Component 4 -- All {len(EXPECTED_LEVEL3)} level-3 bookmarks correct and nested under 2.2 (0.25 pts)")
            total_score += 0.25
        elif matched > 0:
            partial = round(0.25 * matched / len(EXPECTED_LEVEL3), 2)
            print(f"PARTIAL: Component 4 -- {matched}/{len(EXPECTED_LEVEL3)} level-3 bookmarks found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- No level-3 bookmarks matched. Found: {actual_level3}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/Documents/dissertation.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
