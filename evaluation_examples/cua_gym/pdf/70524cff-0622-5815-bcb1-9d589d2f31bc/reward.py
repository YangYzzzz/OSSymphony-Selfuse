"""
Reward Script: Add exhibit tabs to deposition exhibits bundle
Task ID: pdf_legal_044
Domain: pdf
Scoring:
  Component 1: Output file exists with correct page count (49) — 0.2 pts
  Component 2: EXHIBIT 1 tab page at correct position — 0.2 pts
  Component 3: EXHIBIT 2 tab page at correct position — 0.2 pts
  Component 4: EXHIBIT 3 tab page at correct position — 0.2 pts
  Component 5: EXHIBIT 4 tab page at correct position — 0.2 pts
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_044'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'depo_exhibits_tabbed.pdf')

# Expected tab pages: (page_index_in_output, expected_text)
# Task says: insert before original page 1,11,26,35 (1-indexed).
# After insertions cascade:
#   EXHIBIT 1 before original page 1 → new page 0
#   EXHIBIT 2 before original page 11 → after 10 orig pages + 1 tab = new page 11
#   EXHIBIT 3 before original page 26 → after 25 orig pages + 2 tabs = new page 27
#   EXHIBIT 4 before original page 35 → after 34 orig pages + 3 tabs = new page 37
EXPECTED_TABS = [
    (0, "EXHIBIT 1"),
    (11, "EXHIBIT 2"),
    (27, "EXHIBIT 3"),
    (37, "EXHIBIT 4"),
]
EXPECTED_PAGE_COUNT = 49  # 45 original + 4 tab pages


def verify_tab_page(doc, page_idx, expected_label):
    """
    Verify that a tab page exists at the given index with the expected label text.
    Returns True if the page text matches the expected exhibit label.
    """
    if page_idx >= doc.page_count:
        return False, f"Page index {page_idx} out of range (doc has {doc.page_count} pages)"
    page = doc[page_idx]
    text = page.get_text().strip()
    # The tab page should contain the exhibit label and be primarily just that text
    if expected_label in text and len(text) < 100:
        return True, f"Found '{expected_label}' at page {page_idx}"
    else:
        return False, f"Expected '{expected_label}' at page {page_idx}, found: {repr(text[:100])}"


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import pymupdf
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Correct page count (0.2 points)
    # Initial file has 45 pages; golden should have 49 (45 + 4 tabs)
    try:
        actual_count = doc.page_count
        if actual_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 1 — Page count is {actual_count} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGE_COUNT} pages, found {actual_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: EXHIBIT 1 tab page at position 0 (0.2 points)
    try:
        passed, detail = verify_tab_page(doc, 0, "EXHIBIT 1")
        if passed:
            print(f"PASS: Component 2 — {detail} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — {detail}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: EXHIBIT 2 tab page at position 11 (0.2 points)
    try:
        passed, detail = verify_tab_page(doc, 11, "EXHIBIT 2")
        if passed:
            print(f"PASS: Component 3 — {detail} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — {detail}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: EXHIBIT 3 tab page at position 27 (0.2 points)
    try:
        passed, detail = verify_tab_page(doc, 27, "EXHIBIT 3")
        if passed:
            print(f"PASS: Component 4 — {detail} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — {detail}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: EXHIBIT 4 tab page at position 37 (0.2 points)
    try:
        passed, detail = verify_tab_page(doc, 37, "EXHIBIT 4")
        if passed:
            print(f"PASS: Component 5 — {detail} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — {detail}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
