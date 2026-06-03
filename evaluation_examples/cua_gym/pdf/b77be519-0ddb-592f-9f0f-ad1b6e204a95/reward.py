"""
Reward Script: Add a bookmark 'Chapter 3: Methodology' pointing to page 15
Task ID: pdf_fm_018
Domain: pdf
Scoring:
  Component 1 (0.4): A new bookmark entry exists (TOC count increased)
  Component 2 (0.3): Bookmark with title 'Chapter 3: Methodology' is present
  Component 3 (0.3): That bookmark points to page 15 (1-indexed)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_018'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'thesis_final.pdf')

# Known initial TOC entries (precondition check)
INITIAL_TOC_TITLES = [
    'Chapter 1: Introduction',
    '1.1 Background and Motivation',
    '1.2 Research Questions',
    '1.3 Scope and Limitations',
    '1.4 Thesis Outline',
    'Chapter 2: Literature Review',
    '2.1 Theoretical Framework',
    '2.2 Previous Studies',
    '2.3 Gaps in the Literature',
    '2.4 Summary',
]

TARGET_TITLE = 'Chapter 3: Methodology'
TARGET_PAGE = 15  # 1-indexed as returned by get_toc()


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the PDF
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

    toc_titles = [entry[1].strip() for entry in toc]

    # Precondition gate: existing bookmarks must still be present
    for orig_title in INITIAL_TOC_TITLES:
        if orig_title not in toc_titles:
            print(f"PRECONDITION FAIL: Original bookmark '{orig_title}' is missing — file corrupted or overwritten")
            doc.close()
            print("REWARD: 0.0")
            return 0.0
    print("PRECONDITION: All original bookmarks preserved")

    # Component 1: A new bookmark entry exists beyond the original 10 (0.4 points)
    # Initial has 10 entries; golden should have >= 11
    try:
        new_entry_count = len(toc) - len(INITIAL_TOC_TITLES)
        if new_entry_count >= 1:
            print(f"PASS: Component 1 — TOC has {len(toc)} entries ({new_entry_count} new) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — TOC still has {len(toc)} entries, no new bookmark added")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Bookmark with exact title 'Chapter 3: Methodology' exists (0.3 points)
    try:
        target_entries = [entry for entry in toc if entry[1].strip() == TARGET_TITLE]
        if len(target_entries) >= 1:
            print(f"PASS: Component 2 — Found bookmark titled '{TARGET_TITLE}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No bookmark titled '{TARGET_TITLE}' found. Titles: {toc_titles}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: That bookmark points to page 15 (1-indexed) (0.3 points)
    try:
        target_entries = [entry for entry in toc if entry[1].strip() == TARGET_TITLE]
        if len(target_entries) >= 1:
            actual_page = target_entries[0][2]
            if actual_page == TARGET_PAGE:
                print(f"PASS: Component 3 — Bookmark '{TARGET_TITLE}' points to page {actual_page} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Bookmark '{TARGET_TITLE}' points to page {actual_page}, expected {TARGET_PAGE}")
        else:
            print(f"FAIL: Component 3 — Cannot check page; bookmark '{TARGET_TITLE}' not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
