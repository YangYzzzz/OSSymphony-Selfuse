"""
Reward Script: Create nested bookmarks for corporate bylaws PDF
Task ID: pdf_legal_055
Domain: pdf
Scoring:
  Component 1 (0.2): Output file exists and is valid 12-page PDF
  Component 2 (0.3): Correct TOC structure (9 entries, 4 top-level)
  Component 3 (0.3): All TOC entry titles match expected values
  Component 4 (0.2): All TOC entries have correct page numbers and levels
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_055'

# Expected TOC: [level, title, page_number]
EXPECTED_TOC = [
    [1, 'Article I - Name', 1],
    [1, 'Article II - Purpose', 2],
    [1, 'Article III - Members', 3],
    [2, 'Section 3.1 - Eligibility', 3],
    [2, 'Section 3.2 - Voting', 4],
    [1, 'Article IV - Directors', 5],
    [2, 'Section 4.1 - Number', 5],
    [2, 'Section 4.2 - Election', 6],
    [2, 'Section 4.3 - Removal', 7],
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid PDF with 12 pages (0.2 points)
    # This checks that the output file is a proper PDF preserving original content.
    # The initial_env does NOT have bylaws_bookmarked.pdf, so this only passes on golden.
    try:
        page_count = len(doc)
        if page_count == 12:
            print(f"PASS: Component 1 -- Valid PDF with {page_count} pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- Expected 12 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Correct TOC structure -- 9 entries total, 4 at level 1 (0.3 points)
    try:
        toc = doc.get_toc()
        num_entries = len(toc)
        num_top_level = sum(1 for entry in toc if entry[0] == 1)

        if num_entries == 9 and num_top_level == 4:
            print(f"PASS: Component 2 -- TOC has {num_entries} entries, {num_top_level} top-level (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- Expected 9 entries (4 top-level), found {num_entries} entries ({num_top_level} top-level)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All TOC entry titles match expected values (0.3 points)
    try:
        toc = doc.get_toc()
        if len(toc) != len(EXPECTED_TOC):
            print(f"FAIL: Component 3 -- TOC entry count mismatch ({len(toc)} vs {len(EXPECTED_TOC)}), cannot check titles")
        else:
            titles_correct = 0
            for actual, expected in zip(toc, EXPECTED_TOC):
                if actual[1].strip() == expected[1].strip():
                    titles_correct += 1
                else:
                    print(f"  MISMATCH: Expected title '{expected[1]}', found '{actual[1]}'")

            if titles_correct == len(EXPECTED_TOC):
                print(f"PASS: Component 3 -- All {titles_correct} TOC titles match (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 -- {titles_correct}/{len(EXPECTED_TOC)} titles match")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: All TOC entries have correct page numbers and levels (0.2 points)
    try:
        toc = doc.get_toc()
        if len(toc) != len(EXPECTED_TOC):
            print(f"FAIL: Component 4 -- TOC entry count mismatch, cannot check pages/levels")
        else:
            pages_levels_correct = 0
            for actual, expected in zip(toc, EXPECTED_TOC):
                if actual[0] == expected[0] and actual[2] == expected[2]:
                    pages_levels_correct += 1
                else:
                    print(f"  MISMATCH: Expected level={expected[0]}, page={expected[2]}; found level={actual[0]}, page={actual[2]} for '{expected[1]}'")

            if pages_levels_correct == len(EXPECTED_TOC):
                print(f"PASS: Component 4 -- All {pages_levels_correct} TOC entries have correct levels and pages (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 -- {pages_levels_correct}/{len(EXPECTED_TOC)} entries have correct levels/pages")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
file_path = f'{WORKDIR}/legal/corp/bylaws_bookmarked.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
