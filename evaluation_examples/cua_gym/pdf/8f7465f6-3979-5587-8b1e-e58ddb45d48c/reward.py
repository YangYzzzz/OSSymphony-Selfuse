"""
Reward Script: Merge four exhibit PDFs into one with bookmarks
Task ID: pdf_legal_004
Domain: pdf
Scoring:
  Component 1 (0.3): Combined PDF exists with correct page count (18)
  Component 2 (0.4): Four bookmarks with correct labels
  Component 3 (0.3): Bookmarks point to correct pages (1, 6, 9, 17)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_004'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'combined_exhibits.pdf')

# Expected bookmarks: (level, title, page_number)
EXPECTED_TOC = [
    [1, 'Exhibit A', 1],
    [1, 'Exhibit B', 6],
    [1, 'Exhibit C', 9],
    [1, 'Exhibit D', 17],
]

EXPECTED_PAGE_COUNT = 18


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
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

    # Component 1: Correct page count (0.3 points)
    # Initial env has no combined file, so this only passes on golden
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 1 — Page count is {page_count} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGE_COUNT} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Four bookmarks with correct labels (0.4 points)
    # Awards partial credit: 0.1 per correctly labeled bookmark
    try:
        toc = doc.get_toc()
        print(f"INFO: Found {len(toc)} TOC entries: {toc}")

        if len(toc) >= len(EXPECTED_TOC):
            matched_labels = 0
            for expected in EXPECTED_TOC:
                exp_title = expected[1].strip()
                # Check if any TOC entry has this title
                for actual in toc:
                    if actual[1].strip() == exp_title:
                        matched_labels += 1
                        break

            if matched_labels == len(EXPECTED_TOC):
                print(f"PASS: Component 2 — All {matched_labels} bookmark labels correct (0.4 pts)")
                total_score += 0.4
            elif matched_labels > 0:
                partial = round(0.1 * matched_labels, 2)
                print(f"PARTIAL: Component 2 — {matched_labels}/{len(EXPECTED_TOC)} labels correct ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — No matching bookmark labels found")
        else:
            print(f"FAIL: Component 2 — Expected at least {len(EXPECTED_TOC)} bookmarks, found {len(toc)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Bookmarks point to correct pages (0.3 points)
    # Awards partial credit: 0.075 per correct page target
    try:
        toc = doc.get_toc()
        matched_pages = 0
        for expected in EXPECTED_TOC:
            exp_title = expected[1].strip()
            exp_page = expected[2]
            for actual in toc:
                if actual[1].strip() == exp_title and actual[2] == exp_page:
                    matched_pages += 1
                    break

        if matched_pages == len(EXPECTED_TOC):
            print(f"PASS: Component 3 — All {matched_pages} bookmark page targets correct (0.3 pts)")
            total_score += 0.3
        elif matched_pages > 0:
            partial = round(0.075 * matched_pages, 3)
            print(f"PARTIAL: Component 3 — {matched_pages}/{len(EXPECTED_TOC)} page targets correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No bookmark page targets match expected values")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
