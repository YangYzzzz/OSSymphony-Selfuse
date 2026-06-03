"""
Reward Script: Add nested bookmarks to employee benefits handbook PDF
Task ID: pdf_fin_059
Domain: pdf
Scoring:
  Component 1 (0.1): Output file exists, is valid PDF with 30 pages
  Component 2 (0.2): Has exactly 11 TOC entries total
  Component 3 (0.3): 3 top-level bookmarks with correct names and page numbers
  Component 4 (0.4): 8 child bookmarks with correct names, levels, and page numbers
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_059'

# Expected TOC structure: [level, title, page_number (1-indexed)]
EXPECTED_TOC = [
    [1, 'Health Insurance', 1],
    [2, 'Medical', 1],
    [2, 'Dental', 5],
    [2, 'Vision', 8],
    [1, 'Retirement', 10],
    [2, '401(k) Plan', 10],
    [2, 'Pension', 15],
    [1, 'Leave Policies', 20],
    [2, 'PTO', 20],
    [2, 'FMLA', 24],
    [2, 'Parental Leave', 27],
]

EXPECTED_TOP_LEVEL = [e for e in EXPECTED_TOC if e[0] == 1]
EXPECTED_CHILDREN = [e for e in EXPECTED_TOC if e[0] == 2]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists, is valid PDF, has 30 pages (0.1 points)
    # This checks the OUTPUT file (benefits_handbook_nav.pdf) which does NOT exist in initial_env
    try:
        doc = pymupdf.open(file_path)
        page_count = len(doc)
        if page_count == 30:
            print(f"PASS: Component 1 — Output file is valid PDF with {page_count} pages (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — Expected 30 pages, found {page_count}")
            doc.close()
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get actual TOC
    toc = doc.get_toc()
    doc.close()

    # Component 2: Has exactly 11 TOC entries (0.2 points)
    try:
        if len(toc) == 11:
            print(f"PASS: Component 2 — TOC has exactly 11 entries (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Expected 11 TOC entries, found {len(toc)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 3 top-level bookmarks with correct names and pages (0.3 points)
    try:
        actual_top = [e for e in toc if e[0] == 1]
        top_matches = 0
        for expected in EXPECTED_TOP_LEVEL:
            found = any(
                a[0] == expected[0] and a[1].strip() == expected[1] and a[2] == expected[2]
                for a in actual_top
            )
            if found:
                top_matches += 1
                print(f"  TOP-LEVEL MATCH: '{expected[1]}' -> page {expected[2]}")
            else:
                print(f"  TOP-LEVEL MISS: '{expected[1]}' -> page {expected[2]} not found")

        if top_matches == 3:
            print(f"PASS: Component 3 — All 3 top-level bookmarks correct (0.3 pts)")
            total_score += 0.3
        elif top_matches > 0:
            partial = round(0.3 * top_matches / 3, 2)
            print(f"PARTIAL: Component 3 — {top_matches}/3 top-level bookmarks correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No top-level bookmarks match")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 8 child bookmarks with correct names, levels, and pages (0.4 points)
    try:
        actual_children = [e for e in toc if e[0] == 2]
        child_matches = 0
        for expected in EXPECTED_CHILDREN:
            found = any(
                a[0] == expected[0] and a[1].strip() == expected[1] and a[2] == expected[2]
                for a in actual_children
            )
            if found:
                child_matches += 1
                print(f"  CHILD MATCH: '{expected[1]}' (level {expected[0]}) -> page {expected[2]}")
            else:
                print(f"  CHILD MISS: '{expected[1]}' (level {expected[0]}) -> page {expected[2]} not found")

        if child_matches == 8:
            print(f"PASS: Component 4 — All 8 child bookmarks correct (0.4 pts)")
            total_score += 0.4
        elif child_matches > 0:
            partial = round(0.4 * child_matches / 8, 2)
            print(f"PARTIAL: Component 4 — {child_matches}/8 child bookmarks correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No child bookmarks match")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/finance/benefits_handbook_nav.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
