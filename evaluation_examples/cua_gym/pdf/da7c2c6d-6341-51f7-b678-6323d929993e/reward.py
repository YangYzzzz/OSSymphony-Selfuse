"""
Reward Script: Add sub-bookmarks under 'Chapter 3' in programming_book.pdf
Task ID: pdf_mbc_044
Domain: pdf
Scoring:
  - Component 1 (0.15): Chapter 3 has exactly 4 child bookmarks
  - Component 2 (0.20): Sub-bookmark '3.1 Variables' exists at level 2 pointing to page 31
  - Component 3 (0.20): Sub-bookmark '3.2 Functions' exists at level 2 pointing to page 35
  - Component 4 (0.20): Sub-bookmark '3.3 Classes' exists at level 2 pointing to page 42
  - Component 5 (0.20): Sub-bookmark '3.4 Modules' exists at level 2 pointing to page 48
  - Component 6 (0.05): Original top-level bookmarks preserved (Chapters 1-5 still present)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_044'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'programming_book.pdf')

# Expected sub-bookmarks under Chapter 3 (level 2, title, 1-indexed page)
EXPECTED_CHILDREN = [
    (2, '3.1 Variables', 31),
    (2, '3.2 Functions', 35),
    (2, '3.3 Classes', 42),
    (2, '3.4 Modules', 48),
]

# Expected top-level bookmarks (level 1)
EXPECTED_CHAPTERS = [
    (1, 'Chapter 1', 1),
    (1, 'Chapter 2', 10),
    (1, 'Chapter 3', 28),
    (1, 'Chapter 4', 40),
    (1, 'Chapter 5', 49),
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
        toc = doc.get_toc()
        doc.close()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"TOC has {len(toc)} entries:")
    for entry in toc:
        print(f"  Level {entry[0]}: {repr(entry[1])} -> page {entry[2]}")

    # Find Chapter 3 position and extract its children
    ch3_idx = None
    for i, entry in enumerate(toc):
        if entry[0] == 1 and entry[1].strip() == 'Chapter 3':
            ch3_idx = i
            break

    if ch3_idx is None:
        print("FAIL: 'Chapter 3' top-level bookmark not found")
        print("REWARD: 0.0")
        return 0.0

    # Extract children of Chapter 3 (level 2 entries immediately after Chapter 3, before next level 1)
    ch3_children = []
    for i in range(ch3_idx + 1, len(toc)):
        if toc[i][0] <= 1:
            break
        if toc[i][0] == 2:
            ch3_children.append(toc[i])

    print(f"\nChapter 3 children found: {len(ch3_children)}")
    for c in ch3_children:
        print(f"  {repr(c[1])} -> page {c[2]}")

    # Component 1: Chapter 3 has exactly 4 child bookmarks (0.15 points)
    # This FAILS on initial (0 children) -> PASSES on golden (4 children)
    try:
        if len(ch3_children) == 4:
            print(f"\nPASS: Component 1 -- Chapter 3 has exactly 4 children (0.15 pts)")
            total_score += 0.15
        else:
            print(f"\nFAIL: Component 1 -- Expected 4 children under Chapter 3, found {len(ch3_children)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: '3.1 Variables' at page 31 (0.20 points)
    try:
        found = any(
            c[1].strip() == '3.1 Variables' and c[2] == 31
            for c in ch3_children
        )
        if found:
            print(f"PASS: Component 2 -- '3.1 Variables' -> page 31 (0.20 pts)")
            total_score += 0.20
        else:
            # Check partial: title exists but wrong page
            title_match = [c for c in ch3_children if c[1].strip() == '3.1 Variables']
            if title_match:
                print(f"FAIL: Component 2 -- '3.1 Variables' found but points to page {title_match[0][2]}, expected 31")
            else:
                print(f"FAIL: Component 2 -- '3.1 Variables' not found among Chapter 3 children")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: '3.2 Functions' at page 35 (0.20 points)
    try:
        found = any(
            c[1].strip() == '3.2 Functions' and c[2] == 35
            for c in ch3_children
        )
        if found:
            print(f"PASS: Component 3 -- '3.2 Functions' -> page 35 (0.20 pts)")
            total_score += 0.20
        else:
            title_match = [c for c in ch3_children if c[1].strip() == '3.2 Functions']
            if title_match:
                print(f"FAIL: Component 3 -- '3.2 Functions' found but points to page {title_match[0][2]}, expected 35")
            else:
                print(f"FAIL: Component 3 -- '3.2 Functions' not found among Chapter 3 children")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: '3.3 Classes' at page 42 (0.20 points)
    try:
        found = any(
            c[1].strip() == '3.3 Classes' and c[2] == 42
            for c in ch3_children
        )
        if found:
            print(f"PASS: Component 4 -- '3.3 Classes' -> page 42 (0.20 pts)")
            total_score += 0.20
        else:
            title_match = [c for c in ch3_children if c[1].strip() == '3.3 Classes']
            if title_match:
                print(f"FAIL: Component 4 -- '3.3 Classes' found but points to page {title_match[0][2]}, expected 42")
            else:
                print(f"FAIL: Component 4 -- '3.3 Classes' not found among Chapter 3 children")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: '3.4 Modules' at page 48 (0.20 points)
    try:
        found = any(
            c[1].strip() == '3.4 Modules' and c[2] == 48
            for c in ch3_children
        )
        if found:
            print(f"PASS: Component 5 -- '3.4 Modules' -> page 48 (0.20 pts)")
            total_score += 0.20
        else:
            title_match = [c for c in ch3_children if c[1].strip() == '3.4 Modules']
            if title_match:
                print(f"FAIL: Component 5 -- '3.4 Modules' found but points to page {title_match[0][2]}, expected 48")
            else:
                print(f"FAIL: Component 5 -- '3.4 Modules' not found among Chapter 3 children")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Original top-level bookmarks preserved (0.05 points)
    # This checks that the task-introduced changes didn't break existing bookmarks.
    # On initial_env this passes (precondition), so we make it a compound check:
    # top-level bookmarks preserved AND at least one child exists under Chapter 3.
    try:
        top_level = [e for e in toc if e[0] == 1]
        missing_chapters = [
            expected for expected in EXPECTED_CHAPTERS
            if not any(t[1].strip() == expected[1] and t[2] == expected[2] for t in top_level)
        ]

        if len(missing_chapters) == 0 and len(ch3_children) > 0:
            print(f"PASS: Component 6 -- All 5 original chapters preserved AND children added (0.05 pts)")
            total_score += 0.05
        elif len(missing_chapters) > 0:
            print(f"FAIL: Component 6 -- Missing top-level bookmark(s): {[m[1] for m in missing_chapters]}")
        else:
            print(f"FAIL: Component 6 -- Top-level bookmarks OK but no children under Chapter 3")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
