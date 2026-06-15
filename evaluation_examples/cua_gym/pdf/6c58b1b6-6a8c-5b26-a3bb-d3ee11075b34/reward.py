"""
Reward Script: Import bookmarks from text file into PDF
Task ID: pdf_mbc_049
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists with at least 1 bookmark (task-created file)
  Component 2 (0.20): Correct number of bookmarks (7)
  Component 3 (0.30): All bookmark titles match expected values
  Component 4 (0.15): All bookmark hierarchy levels correct
  Component 5 (0.20): All bookmark page references correct
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_049'

# Expected TOC from bookmark_data.txt:
# Format in file: level|title|page (where 0=top-level, 1=child)
# PyMuPDF TOC format: [level, title, page] (where 1=top-level, 2=child)
EXPECTED_TOC = [
    [1, 'Executive Summary', 1],
    [1, 'Financial Overview', 5],
    [2, 'Revenue', 5],
    [2, 'Expenses', 10],
    [1, 'Projections', 15],
    [2, 'Q1 Forecast', 15],
    [2, 'Q2 Forecast', 20],
]


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

    try:
        toc = doc.get_toc()
    except Exception as e:
        print(f"CRITICAL: Cannot read TOC: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has at least 1 bookmark (0.15 points)
    # This distinguishes golden (has bookmarks) from initial (no bookmarks / no file)
    try:
        if len(toc) >= 1:
            print(f"PASS: Component 1 — File has {len(toc)} bookmark(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — File has no bookmarks")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct number of bookmarks — exactly 7 (0.20 points)
    try:
        if len(toc) == len(EXPECTED_TOC):
            print(f"PASS: Component 2 — Bookmark count is {len(toc)} as expected (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected {len(EXPECTED_TOC)} bookmarks, found {len(toc)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All bookmark titles match expected values (0.30 points)
    # Award partial credit: each correct title contributes proportionally
    try:
        if len(toc) == len(EXPECTED_TOC):
            correct_titles = 0
            for actual, expected in zip(toc, EXPECTED_TOC):
                if actual[1].strip() == expected[1].strip():
                    correct_titles += 1
                else:
                    print(f"  MISMATCH title: expected '{expected[1]}', found '{actual[1]}'")
            title_ratio = correct_titles / len(EXPECTED_TOC)
            title_score = 0.30 * title_ratio
            if title_ratio == 1.0:
                print(f"PASS: Component 3 — All {correct_titles}/{len(EXPECTED_TOC)} titles correct (0.30 pts)")
                total_score += title_score
            elif title_ratio > 0:
                print(f"PARTIAL: Component 3 — {correct_titles}/{len(EXPECTED_TOC)} titles correct ({title_score:.2f} pts)")
                total_score += title_score
        else:
            print(f"FAIL: Component 3 — Cannot check titles, bookmark count mismatch")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All bookmark hierarchy levels correct (0.15 points)
    # Level 0 in txt -> level 1 in TOC (top-level), level 1 in txt -> level 2 in TOC (child)
    try:
        if len(toc) == len(EXPECTED_TOC):
            correct_levels = 0
            for actual, expected in zip(toc, EXPECTED_TOC):
                if actual[0] == expected[0]:
                    correct_levels += 1
                else:
                    print(f"  MISMATCH level for '{expected[1]}': expected {expected[0]}, found {actual[0]}")
            level_ratio = correct_levels / len(EXPECTED_TOC)
            level_score = 0.15 * level_ratio
            if level_ratio == 1.0:
                print(f"PASS: Component 4 — All {correct_levels}/{len(EXPECTED_TOC)} levels correct (0.15 pts)")
                total_score += level_score
            elif level_ratio > 0:
                print(f"PARTIAL: Component 4 — {correct_levels}/{len(EXPECTED_TOC)} levels correct ({level_score:.2f} pts)")
                total_score += level_score
        else:
            print(f"FAIL: Component 4 — Cannot check levels, bookmark count mismatch")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: All bookmark page references correct (0.20 points)
    try:
        if len(toc) == len(EXPECTED_TOC):
            correct_pages = 0
            for actual, expected in zip(toc, EXPECTED_TOC):
                if actual[2] == expected[2]:
                    correct_pages += 1
                else:
                    print(f"  MISMATCH page for '{expected[1]}': expected {expected[2]}, found {actual[2]}")
            page_ratio = correct_pages / len(EXPECTED_TOC)
            page_score = 0.20 * page_ratio
            if page_ratio == 1.0:
                print(f"PASS: Component 5 — All {correct_pages}/{len(EXPECTED_TOC)} page refs correct (0.20 pts)")
                total_score += page_score
            elif page_ratio > 0:
                print(f"PARTIAL: Component 5 — {correct_pages}/{len(EXPECTED_TOC)} page refs correct ({page_score:.2f} pts)")
                total_score += page_score
        else:
            print(f"FAIL: Component 5 — Cannot check pages, bookmark count mismatch")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/report_with_bookmarks.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
