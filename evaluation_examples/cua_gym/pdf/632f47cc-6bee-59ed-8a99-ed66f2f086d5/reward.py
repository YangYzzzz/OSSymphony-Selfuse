"""
Reward Script: Merge closing documents and add bookmarks
Task ID: pdf_legal_034
Domain: pdf
Scoring:
  Component 1 (0.3): Merged PDF has correct total page count (35 pages)
  Component 2 (0.3): TOC has exactly 5 bookmark entries
  Component 3 (0.4): TOC entries have correct titles and page numbers
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_034'

# Expected TOC: [[level, title, page_number], ...]
EXPECTED_TOC = [
    [1, 'Deed', 1],
    [1, 'Mortgage', 5],
    [1, 'Title Insurance', 20],
    [1, 'Survey', 28],
    [1, 'Disclosure', 30],
]

EXPECTED_PAGE_COUNT = 35


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

    # Component 1: Merged PDF has correct total page count (0.3 points)
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 1 — Page count is {page_count} (expected {EXPECTED_PAGE_COUNT}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Page count is {page_count}, expected {EXPECTED_PAGE_COUNT}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: TOC has exactly 5 bookmark entries (0.3 points)
    try:
        toc = doc.get_toc()
        if len(toc) == len(EXPECTED_TOC):
            print(f"PASS: Component 2 — TOC has {len(toc)} entries (expected {len(EXPECTED_TOC)}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — TOC has {len(toc)} entries, expected {len(EXPECTED_TOC)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: TOC entries have correct titles and page numbers (0.4 points)
    # Award partial credit per correct entry (0.08 pts each = 0.4 total)
    try:
        toc = doc.get_toc()
        correct_entries = 0
        points_per_entry = 0.4 / len(EXPECTED_TOC)  # 0.08 per entry

        for i, expected in enumerate(EXPECTED_TOC):
            exp_level, exp_title, exp_page = expected
            if i < len(toc):
                act_level, act_title, act_page = toc[i][0], toc[i][1], toc[i][2]
                level_ok = (act_level == exp_level)
                title_ok = (act_title.strip().lower() == exp_title.strip().lower())
                page_ok = (act_page == exp_page)

                if level_ok and title_ok and page_ok:
                    print(f"PASS: Component 3.{i+1} — Bookmark '{act_title}' at page {act_page}, level {act_level} ({points_per_entry:.2f} pts)")
                    correct_entries += 1
                    total_score += points_per_entry
                else:
                    details = []
                    if not level_ok:
                        details.append(f"level {act_level} != {exp_level}")
                    if not title_ok:
                        details.append(f"title '{act_title}' != '{exp_title}'")
                    if not page_ok:
                        details.append(f"page {act_page} != {exp_page}")
                    print(f"FAIL: Component 3.{i+1} — Bookmark mismatch: {', '.join(details)}")
            else:
                print(f"FAIL: Component 3.{i+1} — Missing bookmark entry for '{exp_title}'")

        print(f"INFO: Component 3 — {correct_entries}/{len(EXPECTED_TOC)} bookmarks correct")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/legal/closing/closing_package.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
