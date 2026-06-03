"""
Reward Script: Verify hierarchical bookmark structure in manual.pdf
Task ID: pdf_mbc_038
Domain: pdf
Scoring:
  Component 1 (0.2): TOC has exactly 6 entries
  Component 2 (0.3): Top-level bookmarks correct (titles + pages)
  Component 3 (0.3): Child bookmarks correct (titles + pages)
  Component 4 (0.2): Hierarchical nesting structure correct
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_038'

# Expected TOC: [level, title, page_number (1-indexed)]
EXPECTED_TOC = [
    [1, 'Part I: Basics', 1],
    [2, 'Chapter 1: Overview', 1],
    [2, 'Chapter 2: Setup', 8],
    [1, 'Part II: Advanced', 15],
    [2, 'Chapter 3: Customization', 15],
    [2, 'Chapter 4: Troubleshooting', 22],
]

# Top-level entries (level 1)
EXPECTED_TOP_LEVEL = [
    [1, 'Part I: Basics', 1],
    [1, 'Part II: Advanced', 15],
]

# Child entries (level 2)
EXPECTED_CHILDREN = [
    [2, 'Chapter 1: Overview', 1],
    [2, 'Chapter 2: Setup', 8],
    [2, 'Chapter 3: Customization', 15],
    [2, 'Chapter 4: Troubleshooting', 22],
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

    print(f"Found TOC with {len(toc)} entries: {toc}")

    # Component 1: TOC has exactly 6 entries (0.2 points)
    try:
        if len(toc) == 6:
            print(f"PASS: Component 1 -- TOC has exactly 6 entries (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- Expected 6 TOC entries, found {len(toc)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Top-level bookmarks correct (0.3 points)
    # Check that the level-1 entries have correct titles and page numbers
    try:
        actual_top = [entry for entry in toc if entry[0] == 1]
        if len(actual_top) == len(EXPECTED_TOP_LEVEL):
            all_match = True
            for actual, expected in zip(actual_top, EXPECTED_TOP_LEVEL):
                if actual[1].strip() != expected[1] or actual[2] != expected[2]:
                    print(f"FAIL: Component 2 -- Top-level mismatch: got ({actual[1]!r}, p{actual[2]}), expected ({expected[1]!r}, p{expected[2]})")
                    all_match = False
                    break
            if all_match:
                print(f"PASS: Component 2 -- Top-level bookmarks correct: {[e[1] for e in actual_top]} (0.3 pts)")
                total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- Expected {len(EXPECTED_TOP_LEVEL)} top-level entries, found {len(actual_top)}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Child bookmarks correct (0.3 points)
    # Check that level-2 entries have correct titles and page numbers
    try:
        actual_children = [entry for entry in toc if entry[0] == 2]
        if len(actual_children) == len(EXPECTED_CHILDREN):
            all_match = True
            for actual, expected in zip(actual_children, EXPECTED_CHILDREN):
                if actual[1].strip() != expected[1] or actual[2] != expected[2]:
                    print(f"FAIL: Component 3 -- Child mismatch: got ({actual[1]!r}, p{actual[2]}), expected ({expected[1]!r}, p{expected[2]})")
                    all_match = False
                    break
            if all_match:
                print(f"PASS: Component 3 -- Child bookmarks correct: {[e[1] for e in actual_children]} (0.3 pts)")
                total_score += 0.3
        else:
            print(f"FAIL: Component 3 -- Expected {len(EXPECTED_CHILDREN)} child entries, found {len(actual_children)}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Hierarchical nesting structure correct (0.2 points)
    # Verify that the level sequence matches: 1,2,2,1,2,2
    try:
        expected_levels = [e[0] for e in EXPECTED_TOC]
        actual_levels = [e[0] for e in toc]
        if actual_levels == expected_levels:
            print(f"PASS: Component 4 -- Nesting structure correct: {actual_levels} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 -- Expected level sequence {expected_levels}, found {actual_levels}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/Documents/manual.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
