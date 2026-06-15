"""
Reward Script: Add a bookmark named 'Appendix A - Data Tables' pointing to page 45
Task ID: pdf_mbc_037
Domain: pdf
Scoring:
  Component 1 (0.5): Bookmark 'Appendix A - Data Tables' exists in TOC
  Component 2 (0.2): That bookmark points to page 45
  Component 3 (0.3): Appendix added AND all original bookmarks preserved
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_037'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'research_paper.pdf')

# Expected original bookmarks (must be preserved)
ORIGINAL_BOOKMARKS = [
    [1, 'Chapter 1: Introduction', 2],
    [1, 'Chapter 2: Literature Review', 9],
    [1, 'Chapter 3: Methodology', 19],
    [1, 'Chapter 4: Results and Analysis', 29],
    [1, 'Chapter 5: Discussion and Future Directions', 39],
]

TARGET_TITLE = 'Appendix A - Data Tables'
TARGET_PAGE = 45


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

    print(f"INFO: Found {len(toc)} TOC entries")
    for entry in toc:
        print(f"  Level={entry[0]}, Title={repr(entry[1])}, Page={entry[2]}")

    # Find the appendix bookmark entry
    appendix_entries = [e for e in toc if e[1].strip() == TARGET_TITLE]
    appendix_found = len(appendix_entries) > 0

    # Component 1: Bookmark 'Appendix A - Data Tables' exists in TOC (0.5 points)
    try:
        if appendix_found:
            print(f"PASS: Component 1 -- Bookmark '{TARGET_TITLE}' found in TOC (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- Bookmark '{TARGET_TITLE}' not found in TOC")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: The appendix bookmark points to page 45 (0.2 points)
    # Only scores if appendix bookmark exists (anchored to task change)
    try:
        if appendix_found:
            actual_page = appendix_entries[0][2]
            if actual_page == TARGET_PAGE:
                print(f"PASS: Component 2 -- Bookmark points to page {TARGET_PAGE} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 -- Bookmark points to page {actual_page}, expected {TARGET_PAGE}")
        else:
            print(f"FAIL: Component 2 -- Cannot check page: bookmark not found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Appendix bookmark added AND all original bookmarks preserved (0.3 points)
    # Anchored to the task change: only awards points if the appendix bookmark exists
    try:
        if appendix_found:
            preserved_count = 0
            for expected in ORIGINAL_BOOKMARKS:
                exp_level, exp_title, exp_page = expected
                matching = [e for e in toc if e[1].strip() == exp_title.strip()
                            and e[0] == exp_level and e[2] == exp_page]
                if matching:
                    preserved_count += 1
                else:
                    print(f"FAIL: Component 3 -- Missing original bookmark: '{exp_title}' at page {exp_page}")

            if preserved_count == len(ORIGINAL_BOOKMARKS):
                print(f"PASS: Component 3 -- Appendix added AND all {preserved_count} original bookmarks preserved (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 -- Only {preserved_count}/{len(ORIGINAL_BOOKMARKS)} original bookmarks preserved")
        else:
            print(f"FAIL: Component 3 -- Cannot check preservation: appendix bookmark not found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
