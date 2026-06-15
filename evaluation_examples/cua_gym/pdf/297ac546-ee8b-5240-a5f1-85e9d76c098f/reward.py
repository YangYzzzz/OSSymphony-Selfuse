"""
Reward Script: Add hierarchical bookmark structure to a PDF textbook chapter.
Task ID: pdf_gf2_010
Domain: pdf
Scoring:
  - Component 1 (0.2): TOC has exactly 6 entries
  - Component 2 (0.2): Level 1 root bookmark correct
  - Component 3 (0.3): Level 2 bookmarks correct (3 entries)
  - Component 4 (0.3): Level 3 bookmarks correct (2 entries)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_010'

# Expected TOC structure: [level, title, page]
EXPECTED_TOC = [
    [1, "Chapter 3: Data Structures", 1],
    [2, "Arrays and Lists", 1],
    [2, "Trees and Graphs", 8],
    [3, "Binary Trees", 8],
    [3, "Graph Algorithms", 12],
    [2, "Hash Tables", 15],
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

    # Precondition gate: must be a valid PDF with 20 pages
    if doc.page_count != 20:
        print(f"PRECONDITION FAIL: Expected 20 pages, found {doc.page_count}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    toc = doc.get_toc()
    doc.close()

    # Component 1: TOC has exactly 6 entries (0.2 points)
    try:
        if len(toc) == 6:
            print(f"PASS: Component 1 -- TOC has 6 entries (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- Expected 6 TOC entries, found {len(toc)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Level 1 root bookmark is correct (0.2 points)
    # Expected: [1, "Chapter 3: Data Structures", 1]
    try:
        if len(toc) >= 1:
            entry = toc[0]
            level_ok = entry[0] == 1
            title_ok = entry[1].strip() == "Chapter 3: Data Structures"
            page_ok = entry[2] == 1
            if level_ok and title_ok and page_ok:
                print(f"PASS: Component 2 -- Root bookmark 'Chapter 3: Data Structures' at level 1, page 1 (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 -- Root bookmark mismatch: level={entry[0]}, title='{entry[1]}', page={entry[2]}")
        else:
            print(f"FAIL: Component 2 -- No TOC entries found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Level 2 bookmarks correct (0.3 points)
    # Expected level-2 entries: "Arrays and Lists" (p1), "Trees and Graphs" (p8), "Hash Tables" (p15)
    try:
        level2_expected = [
            ("Arrays and Lists", 1),
            ("Trees and Graphs", 8),
            ("Hash Tables", 15),
        ]
        level2_actual = [(e[1].strip(), e[2]) for e in toc if e[0] == 2]

        matched = 0
        for title, page in level2_expected:
            if (title, page) in level2_actual:
                matched += 1
            else:
                print(f"FAIL: Component 3 -- Missing level-2 bookmark: '{title}' -> page {page}")

        if matched == 3 and len(level2_actual) == 3:
            print(f"PASS: Component 3 -- All 3 level-2 bookmarks correct (0.3 pts)")
            total_score += 0.3
        elif matched > 0:
            partial = round(0.3 * matched / 3, 2)
            print(f"PARTIAL: Component 3 -- {matched}/3 level-2 bookmarks correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No level-2 bookmarks matched. Found: {level2_actual}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Level 3 bookmarks correct (0.3 points)
    # Expected level-3 entries: "Binary Trees" (p8), "Graph Algorithms" (p12)
    try:
        level3_expected = [
            ("Binary Trees", 8),
            ("Graph Algorithms", 12),
        ]
        level3_actual = [(e[1].strip(), e[2]) for e in toc if e[0] == 3]

        matched = 0
        for title, page in level3_expected:
            if (title, page) in level3_actual:
                matched += 1
            else:
                print(f"FAIL: Component 4 -- Missing level-3 bookmark: '{title}' -> page {page}")

        if matched == 2 and len(level3_actual) == 2:
            print(f"PASS: Component 4 -- All 2 level-3 bookmarks correct (0.3 pts)")
            total_score += 0.3
        elif matched > 0:
            partial = round(0.3 * matched / 2, 2)
            print(f"PARTIAL: Component 4 -- {matched}/2 level-3 bookmarks correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- No level-3 bookmarks matched. Found: {level3_actual}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Try primary path first, then fallback to canonical path
primary_path = f'{WORKDIR}/Documents/textbook_ch3_bookmarked.pdf'
fallback_path = f'{WORKDIR}/{TASK_ID}.pdf'

if os.path.exists(primary_path):
    verify_task(primary_path)
elif os.path.exists(fallback_path):
    print(f"Primary path not found, using fallback: {fallback_path}")
    verify_task(fallback_path)
else:
    print(f"File not found at {primary_path} or {fallback_path}")
    print("REWARD: 0.0")
