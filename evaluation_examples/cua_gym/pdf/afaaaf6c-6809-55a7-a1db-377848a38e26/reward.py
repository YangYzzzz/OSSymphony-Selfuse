"""
Reward Script: Add hierarchical bookmarks to a PDF dissertation
Task ID: pdf_res_036
Domain: pdf
Scoring:
  Component 1 (0.20): Output file exists at correct path
  Component 2 (0.15): Output PDF has 100 pages (same as source)
  Component 3 (0.25): Exactly 6 TOC/bookmark entries
  Component 4 (0.20): Level-1 entries correct (Part I: Theory p1, Part II: Experiments p50)
  Component 5 (0.20): Level-2 entries correct (Chapters 1-4 at correct pages)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_036'

# Expected TOC structure: [level, title, page_number]
EXPECTED_TOC = [
    [1, 'Part I: Theory', 1],
    [2, 'Chapter 1', 1],
    [2, 'Chapter 2', 25],
    [1, 'Part II: Experiments', 50],
    [2, 'Chapter 3', 50],
    [2, 'Chapter 4', 75],
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    import pymupdf

    total_score = 0.0

    # Precondition: file must exist (gate, not scored as task-introduced change)
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

    # Component 1: Output file is a new file at the bookmarked path (0.20 points)
    # This discriminates initial vs golden because the output file only exists in golden.
    try:
        source_path = os.path.join(WORKDIR, 'thesis', 'dissertation_v2.pdf')
        # Verify it's a distinct file from the source (different size or both exist)
        if os.path.exists(source_path) and os.path.exists(file_path):
            # The output file should be different from the source
            # (bookmarks add data, so file size changes)
            src_size = os.path.getsize(source_path)
            out_size = os.path.getsize(file_path)
            if out_size != src_size:
                print(f"PASS: Component 1 — Output file exists and differs from source "
                      f"(src={src_size}, out={out_size}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — Output file is identical to source (no bookmarks added?)")
        else:
            print(f"FAIL: Component 1 — Source or output file missing")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Output PDF has 100 pages matching the source (0.15 points)
    # This is scored as a compound check: output exists AND has correct page count.
    # On initial_env, the output file doesn't exist so this won't be reached.
    try:
        page_count = doc.page_count
        if page_count == 100:
            print(f"PASS: Component 2 — PDF has 100 pages as expected (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected 100 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Exactly 6 TOC/bookmark entries (0.25 points)
    try:
        toc = doc.get_toc()
        if len(toc) == 6:
            print(f"PASS: Component 3 — TOC has exactly 6 entries (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Expected 6 TOC entries, found {len(toc)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Level-1 entries are correct (0.20 points)
    # Check: two level-1 entries with correct titles and page numbers
    try:
        toc = doc.get_toc()
        level1_entries = [e for e in toc if e[0] == 1]
        expected_l1 = [
            ('Part I: Theory', 1),
            ('Part II: Experiments', 50),
        ]
        level1_mismatches = []

        if len(level1_entries) != 2:
            level1_mismatches.append(
                f"Expected 2 level-1 entries, found {len(level1_entries)}")
        else:
            for actual, (exp_title, exp_page) in zip(level1_entries, expected_l1):
                if actual[1].strip() != exp_title:
                    level1_mismatches.append(
                        f"Title mismatch: expected '{exp_title}', found '{actual[1]}'")
                if actual[2] != exp_page:
                    level1_mismatches.append(
                        f"Page mismatch for '{exp_title}': expected {exp_page}, found {actual[2]}")

        if len(level1_mismatches) == 0:
            print(f"PASS: Component 4 — Level-1 entries correct: "
                  f"'Part I: Theory' (p1), 'Part II: Experiments' (p50) (0.20 pts)")
            total_score += 0.20
        else:
            for m in level1_mismatches:
                print(f"FAIL: Component 4 — {m}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Level-2 entries are correct (0.20 points)
    # Check: four level-2 children with correct titles and page numbers
    try:
        toc = doc.get_toc()
        level2_entries = [e for e in toc if e[0] == 2]
        expected_l2 = [
            ('Chapter 1', 1),
            ('Chapter 2', 25),
            ('Chapter 3', 50),
            ('Chapter 4', 75),
        ]
        level2_mismatches = []

        if len(level2_entries) != 4:
            level2_mismatches.append(
                f"Expected 4 level-2 entries, found {len(level2_entries)}")
        else:
            for actual, (exp_title, exp_page) in zip(level2_entries, expected_l2):
                if actual[1].strip() != exp_title:
                    level2_mismatches.append(
                        f"Title mismatch: expected '{exp_title}', found '{actual[1]}'")
                if actual[2] != exp_page:
                    level2_mismatches.append(
                        f"Page mismatch for '{exp_title}': expected {exp_page}, found {actual[2]}")

        if len(level2_mismatches) == 0:
            print(f"PASS: Component 5 — Level-2 entries correct: "
                  f"Ch1(p1), Ch2(p25), Ch3(p50), Ch4(p75) (0.20 pts)")
            total_score += 0.20
        else:
            for m in level2_mismatches:
                print(f"FAIL: Component 5 — {m}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical output path
file_path = os.path.join(WORKDIR, 'thesis', 'dissertation_v2_bookmarked.pdf')
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
