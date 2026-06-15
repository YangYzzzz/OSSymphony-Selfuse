"""
Reward Script: Update PDF bookmarks using pdftk
Task ID: pdf_mbc_060
Domain: pdf
Scoring:
  Component 1 (0.3): Bookmark count is exactly 8
  Component 2 (0.4): Bookmark titles match expected 8 entries
  Component 3 (0.3): Bookmark page numbers match expected values
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_060'

# Expected bookmarks from new_bookmarks.info (ground truth)
EXPECTED_BOOKMARKS = [
    [1, 'Introduction to Cloud Computing', 1],
    [1, 'Infrastructure as a Service (IaaS)', 6],
    [1, 'Platform as a Service (PaaS)', 11],
    [1, 'Software as a Service (SaaS)', 16],
    [1, 'Security and Compliance', 21],
    [1, 'Cost Optimization', 26],
    [1, 'Migration Strategies', 31],
    [1, 'Monitoring and Observability', 36],
]


def verify_task(file_path):
    """
    Verify that guide.pdf bookmarks have been updated from the old 3 entries
    to the new 8 entries specified in new_bookmarks.info.
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
        toc = doc.get_toc()  # returns [[level, title, page_num], ...]
    except Exception as e:
        print(f"CRITICAL: Cannot read TOC: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(toc)} bookmark entries")
    for entry in toc:
        print(f"  Bookmark: level={entry[0]}, title='{entry[1]}', page={entry[2]}")

    # Component 1: Bookmark count is exactly 8 (0.3 points)
    # Initial has 3 bookmarks, golden should have 8
    try:
        if len(toc) == 8:
            print(f"PASS: Component 1 -- Bookmark count is 8 (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- Expected 8 bookmarks, found {len(toc)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Bookmark titles match expected 8 entries (0.4 points)
    # Award partial credit per title match (0.05 per title)
    try:
        expected_titles = [b[1] for b in EXPECTED_BOOKMARKS]
        actual_titles = [entry[1] for entry in toc]
        matched_titles = 0
        for exp_title in expected_titles:
            if exp_title in actual_titles:
                matched_titles += 1
            else:
                print(f"FAIL: Component 2 -- Missing title: '{exp_title}'")

        if matched_titles == len(expected_titles):
            print(f"PASS: Component 2 -- All 8 bookmark titles match (0.4 pts)")
            total_score += 0.4
        elif matched_titles > 0:
            partial = round(0.4 * (matched_titles / len(expected_titles)), 2)
            print(f"PARTIAL: Component 2 -- {matched_titles}/{len(expected_titles)} titles match ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No expected bookmark titles found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Bookmark page numbers match expected values (0.3 points)
    # Award partial credit per correct page number (0.0375 per entry)
    try:
        matched_pages = 0
        for exp_bm in EXPECTED_BOOKMARKS:
            exp_level, exp_title, exp_page = exp_bm
            match_exists = any(
                entry[1] == exp_title and entry[2] == exp_page and entry[0] == exp_level
                for entry in toc
            )
            if match_exists:
                matched_pages += 1
            else:
                print(f"FAIL: Component 3 -- Bookmark '{exp_title}' not at expected page {exp_page} level {exp_level}")

        if matched_pages == len(EXPECTED_BOOKMARKS):
            print(f"PASS: Component 3 -- All 8 bookmark page numbers and levels correct (0.3 pts)")
            total_score += 0.3
        elif matched_pages > 0:
            partial = round(0.3 * (matched_pages / len(EXPECTED_BOOKMARKS)), 2)
            print(f"PARTIAL: Component 3 -- {matched_pages}/{len(EXPECTED_BOOKMARKS)} entries fully match ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No bookmark entries fully match expected values")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/Documents/guide.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
