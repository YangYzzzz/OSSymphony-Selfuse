"""
Reward Script: Create table of contents bookmarks for handbook PDF
Task ID: pdf_ro_015
Domain: pdf
Scoring:
  Component 1: Output file exists and is a valid PDF with 40 pages (0.2)
  Component 2: TOC has exactly 5 entries, all at level 1 (0.2)
  Component 3: TOC titles match expected values (0.3)
  Component 4: TOC page numbers match expected values (0.3)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_015'
OUTPUT_PATH = os.path.join(WORKDIR, 'Documents', 'handbook_bookmarked.pdf')

# Expected TOC: [level, title, page_number]
EXPECTED_TOC = [
    [1, 'Introduction', 1],
    [1, 'Chapter 1: Policies', 5],
    [1, 'Chapter 2: Procedures', 15],
    [1, 'Chapter 3: Resources', 25],
    [1, 'Appendix', 35],
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must be a valid PDF
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = len(doc)
    toc = doc.get_toc()
    doc.close()

    # Component 1: Output file is a valid PDF with 40 pages preserved (0.2 points)
    # This checks that the output file exists as a proper PDF AND preserves all pages.
    # Initial env does NOT have handbook_bookmarked.pdf, so this fails on initial.
    try:
        if page_count == 40:
            print(f"PASS: Component 1 - Valid PDF with {page_count} pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 - Expected 40 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: TOC has exactly 5 entries, all at level 1 (0.2 points)
    # Initial env has no TOC (0 entries), so this fails on initial.
    try:
        if len(toc) == 5:
            all_level_1 = all(entry[0] == 1 for entry in toc)
            if all_level_1:
                print(f"PASS: Component 2 - TOC has 5 entries, all at level 1 (0.2 pts)")
                total_score += 0.2
            else:
                levels = [entry[0] for entry in toc]
                print(f"FAIL: Component 2 - TOC has 5 entries but not all level 1: {levels}")
        else:
            print(f"FAIL: Component 2 - Expected 5 TOC entries, found {len(toc)}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: TOC titles match expected values (0.3 points)
    # Each correct title earns 0.06 points (0.3 / 5).
    # Initial env has no TOC, so this fails on initial.
    try:
        if len(toc) >= 1:
            title_score = 0.0
            for i, expected in enumerate(EXPECTED_TOC):
                if i < len(toc):
                    actual_title = toc[i][1].strip()
                    expected_title = expected[1].strip()
                    if actual_title == expected_title:
                        print(f"PASS: Component 3.{i+1} - Title '{actual_title}' matches (0.06 pts)")
                        title_score += 0.06
                    else:
                        print(f"FAIL: Component 3.{i+1} - Expected title '{expected_title}', found '{actual_title}'")
                else:
                    print(f"FAIL: Component 3.{i+1} - Missing TOC entry {i+1}")
            if title_score > 0:
                total_score += title_score
        else:
            print(f"FAIL: Component 3 - No TOC entries to check titles")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: TOC page numbers match expected values (0.3 points)
    # Each correct page number earns 0.06 points (0.3 / 5).
    # Initial env has no TOC, so this fails on initial.
    try:
        if len(toc) >= 1:
            page_score = 0.0
            for i, expected in enumerate(EXPECTED_TOC):
                if i < len(toc):
                    actual_page = toc[i][2]
                    expected_page = expected[2]
                    if actual_page == expected_page:
                        print(f"PASS: Component 4.{i+1} - Page {actual_page} matches (0.06 pts)")
                        page_score += 0.06
                    else:
                        print(f"FAIL: Component 4.{i+1} - Expected page {expected_page}, found {actual_page}")
                else:
                    print(f"FAIL: Component 4.{i+1} - Missing TOC entry {i+1}")
            if page_score > 0:
                total_score += page_score
        else:
            print(f"FAIL: Component 4 - No TOC entries to check pages")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
