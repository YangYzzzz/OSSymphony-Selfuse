"""
Reward Script: Rename Korean bookmarks to English in a PDF
Task ID: pdf_mbc_058
Domain: pdf
Scoring:
  Component 1 (0.10): Correct number of bookmarks (4)
  Component 2 (0.60): All 4 bookmark titles match expected English names
  Component 3 (0.30): All 4 bookmark page destinations preserved correctly
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_058'

# Expected golden state: English bookmarks with same page destinations
EXPECTED_TOC = [
    [1, 'Introduction', 1],
    [1, 'Methodology', 5],
    [1, 'Results', 12],
    [1, 'Conclusion', 18],
]

# Korean titles that should NOT be present (initial state)
KOREAN_TITLES = {'소개', '방법론', '결과', '결론'}


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

    toc = doc.get_toc()
    doc.close()

    print(f"INFO: Found {len(toc)} bookmarks")
    for entry in toc:
        print(f"  Level={entry[0]}, Title={repr(entry[1])}, Page={entry[2]}")

    # Component 1: Correct number of bookmarks (0.10 points)
    # This checks that exactly 4 bookmarks exist AND none of them are Korean.
    # The Korean check ensures this component fails on the initial_env.
    try:
        has_correct_count = len(toc) == 4
        has_no_korean = all(entry[1].strip() not in KOREAN_TITLES for entry in toc)
        if has_correct_count and has_no_korean:
            print(f"PASS: Component 1 — 4 bookmarks found, none Korean (0.10 pts)")
            total_score += 0.10
        elif not has_correct_count:
            print(f"FAIL: Component 1 — expected 4 bookmarks, found {len(toc)}")
        else:
            print(f"FAIL: Component 1 — Korean titles still present")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 bookmark titles match expected English names (0.60 points)
    # Award 0.15 per correctly titled bookmark
    try:
        title_score = 0.0
        for i, expected in enumerate(EXPECTED_TOC):
            expected_title = expected[1]
            if i < len(toc):
                actual_title = toc[i][1].strip()
                if actual_title == expected_title:
                    print(f"PASS: Component 2.{i+1} — Bookmark {i+1} title is '{actual_title}' (0.15 pts)")
                    title_score += 0.15
                else:
                    print(f"FAIL: Component 2.{i+1} — Bookmark {i+1} title expected '{expected_title}', found '{actual_title}'")
            else:
                print(f"FAIL: Component 2.{i+1} — Bookmark {i+1} missing")
        if title_score > 0:
            total_score += title_score
        print(f"INFO: Component 2 subtotal: {title_score}/0.60")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 4 bookmark page destinations preserved (0.30 points)
    # Award 0.075 per correct page destination, but ONLY if the title is also English
    # (so this fails on initial_env where titles are Korean)
    try:
        page_score = 0.0
        for i, expected in enumerate(EXPECTED_TOC):
            expected_title = expected[1]
            expected_page = expected[2]
            if i < len(toc):
                actual_title = toc[i][1].strip()
                actual_page = toc[i][2]
                if actual_title == expected_title and actual_page == expected_page:
                    print(f"PASS: Component 3.{i+1} — Bookmark '{actual_title}' points to page {actual_page} (0.075 pts)")
                    page_score += 0.075
                elif actual_title != expected_title:
                    print(f"FAIL: Component 3.{i+1} — Title mismatch '{actual_title}' != '{expected_title}', page check skipped")
                else:
                    print(f"FAIL: Component 3.{i+1} — Bookmark '{actual_title}' points to page {actual_page}, expected {expected_page}")
            else:
                print(f"FAIL: Component 3.{i+1} — Bookmark {i+1} missing")
        if page_score > 0:
            total_score += page_score
        print(f"INFO: Component 3 subtotal: {page_score}/0.30")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/{TASK_ID}.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
