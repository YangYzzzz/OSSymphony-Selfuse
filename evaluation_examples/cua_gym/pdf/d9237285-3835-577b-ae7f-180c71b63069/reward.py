"""
Reward Script: Create bookmarks for all section headings in policy_handbook.pdf
Task ID: pdf_pw_010
Domain: pdf
Scoring:
  Component 1 (0.3): Correct number of bookmarks (exactly 6)
  Component 2 (0.4): All bookmark titles match expected values
  Component 3 (0.3): All bookmark page numbers match expected values
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_010'

# Expected bookmarks: [level, title, page_number (1-indexed)]
EXPECTED_TOC = [
    [1, 'Introduction', 1],
    [1, 'Code of Conduct', 3],
    [1, 'Leave Policy', 8],
    [1, 'Benefits', 12],
    [1, 'Safety Guidelines', 18],
    [1, 'Appendix', 22],
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

    # Load PDF
    try:
        import fitz
        doc = fitz.open(file_path)
        toc = doc.get_toc()
        page_count = doc.page_count
        doc.close()
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: PDF has {page_count} pages and {len(toc)} TOC entries")
    for entry in toc:
        print(f"  TOC entry: level={entry[0]}, title='{entry[1]}', page={entry[2]}")

    # Component 1: Correct number of bookmarks (0.3 points)
    try:
        if len(toc) == len(EXPECTED_TOC):
            print(f"PASS: Component 1 — Found exactly {len(EXPECTED_TOC)} bookmarks (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected {len(EXPECTED_TOC)} bookmarks, found {len(toc)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All bookmark titles match (0.4 points)
    try:
        if len(toc) == 0:
            print("FAIL: Component 2 — No bookmarks to check titles")
        else:
            matching_titles = 0
            for i, expected in enumerate(EXPECTED_TOC):
                if i < len(toc):
                    actual_title = toc[i][1].strip()
                    expected_title = expected[1].strip()
                    if actual_title == expected_title:
                        matching_titles += 1
                    else:
                        print(f"  MISMATCH title at index {i}: expected '{expected_title}', got '{actual_title}'")

            if matching_titles == len(EXPECTED_TOC):
                print(f"PASS: Component 2 — All {len(EXPECTED_TOC)} bookmark titles match (0.4 pts)")
                total_score += 0.4
            elif matching_titles > 0:
                partial = 0.4 * (matching_titles / len(EXPECTED_TOC))
                total_score += partial
                print(f"PARTIAL: Component 2 — {matching_titles}/{len(EXPECTED_TOC)} titles match ({partial:.2f} pts)")
            else:
                print(f"FAIL: Component 2 — No bookmark titles match")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All bookmark page numbers match (0.3 points)
    try:
        if len(toc) == 0:
            print("FAIL: Component 3 — No bookmarks to check page numbers")
        else:
            matching_pages = 0
            for i, expected in enumerate(EXPECTED_TOC):
                if i < len(toc):
                    actual_page = toc[i][2]
                    expected_page = expected[2]
                    actual_level = toc[i][0]
                    expected_level = expected[0]
                    if actual_page == expected_page and actual_level == expected_level:
                        matching_pages += 1
                    else:
                        print(f"  MISMATCH at index {i}: expected level={expected_level}/page={expected_page}, got level={actual_level}/page={actual_page}")

            if matching_pages == len(EXPECTED_TOC):
                print(f"PASS: Component 3 — All {len(EXPECTED_TOC)} bookmark pages and levels match (0.3 pts)")
                total_score += 0.3
            elif matching_pages > 0:
                partial = 0.3 * (matching_pages / len(EXPECTED_TOC))
                total_score += partial
                print(f"PARTIAL: Component 3 — {matching_pages}/{len(EXPECTED_TOC)} pages/levels match ({partial:.2f} pts)")
            else:
                print(f"FAIL: Component 3 — No bookmark pages/levels match")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/policy_handbook_bookmarked.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
