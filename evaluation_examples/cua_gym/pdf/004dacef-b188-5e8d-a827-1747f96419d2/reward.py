"""
Reward Script: Merge PDFs with bookmark offset
Task ID: pdf_mbc_055
Domain: pdf
Scoring:
  - Component 1: combined.pdf exists and has 45 pages (0.25 pts)
  - Component 2: TOC has exactly 4 bookmark entries with correct titles (0.35 pts)
  - Component 3: Bookmark page numbers are correctly offset (0.40 pts)
"""

import os
import pymupdf  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_055'
COMBINED_PATH = os.path.join(WORKDIR, 'Documents', 'combined.pdf')

# Expected bookmark structure after merge with page offset
# Part1 (25 pages): Intro->1, Body->5
# Part2 (20 pages): Methods->1+25=26, Results->10+25=35
EXPECTED_TOC = [
    [1, 'Intro', 1],
    [1, 'Body', 5],
    [1, 'Methods', 26],
    [1, 'Results', 35],
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: combined.pdf must exist
    if not os.path.exists(COMBINED_PATH):
        print(f"CRITICAL: combined.pdf not found at {COMBINED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(COMBINED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open combined.pdf: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page count is 45 (0.25 points)
    try:
        page_count = doc.page_count
        if page_count == 45:
            print(f"PASS: Component 1 — combined.pdf has {page_count} pages (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected 45 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: TOC has 4 entries with correct titles (0.35 points)
    try:
        toc = doc.get_toc()
        expected_titles = [entry[1] for entry in EXPECTED_TOC]

        if len(toc) == len(EXPECTED_TOC):
            actual_titles = [entry[1].strip() for entry in toc]
            if actual_titles == expected_titles:
                print(f"PASS: Component 2 — TOC has 4 entries with correct titles: {actual_titles} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — TOC titles mismatch. Expected {expected_titles}, found {actual_titles}")
        else:
            print(f"FAIL: Component 2 — expected {len(EXPECTED_TOC)} TOC entries, found {len(toc)}")
            if toc:
                print(f"  Actual TOC: {toc}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Bookmark page numbers correctly offset (0.40 points)
    # Part2 bookmarks should be offset by 25 (page count of part1)
    try:
        toc = doc.get_toc()
        expected_pages = [entry[2] for entry in EXPECTED_TOC]

        if len(toc) >= len(EXPECTED_TOC):
            actual_pages = [entry[2] for entry in toc[:len(EXPECTED_TOC)]]
            matching = sum(1 for a, e in zip(actual_pages, expected_pages) if a == e)
            if matching == len(EXPECTED_TOC):
                print(f"PASS: Component 3 — All bookmark page numbers correct: {actual_pages} (0.40 pts)")
                total_score += 0.40
            elif matching > 0:
                # Partial credit: proportional to correct page numbers
                partial = 0.40 * (matching / len(EXPECTED_TOC))
                print(f"PARTIAL: Component 3 — {matching}/{len(EXPECTED_TOC)} page numbers correct. Expected {expected_pages}, found {actual_pages} ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — No page numbers match. Expected {expected_pages}, found {actual_pages}")
        else:
            print(f"FAIL: Component 3 — Not enough TOC entries to check page numbers")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
