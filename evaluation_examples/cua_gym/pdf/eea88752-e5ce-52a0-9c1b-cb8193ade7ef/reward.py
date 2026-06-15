"""
Reward Script: Merge medical records PDFs, add Bates numbers and bookmarks
Task ID: pdf_legal_091
Domain: pdf
Scoring:
  Component 1 (0.25): Output file exists with 90 pages
  Component 2 (0.35): Bates numbers MED-0001 through MED-0090 present on pages
  Component 3 (0.25): 4 bookmarks at correct page positions
  Component 4 (0.15): Correct merge order verified by source content at boundary pages
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_091'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'medical', 'complete_medical_records.pdf')

# Expected bookmarks: [level, title, page_number (1-indexed)]
EXPECTED_BOOKMARKS = [
    [1, 'Hospital Records', 1],
    [1, 'Primary Care', 46],
    [1, 'Specialist Reports', 66],
    [1, 'Imaging Results', 81],
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Early exit: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {OUTPUT_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has exactly 90 pages (0.25 points)
    try:
        page_count = doc.page_count
        if page_count == 90:
            print(f"PASS: Component 1 — Page count is 90 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 90 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Bates numbers MED-0001 through MED-0090 (0.35 points)
    # Check a representative sample of pages for correct Bates stamps
    try:
        bates_pattern = re.compile(r'MED-(\d{4})')
        # Check all pages for Bates numbers
        correct_bates = 0
        total_pages_to_check = min(doc.page_count, 90)
        sample_pages = list(range(total_pages_to_check))  # check all 90 pages

        for pg_idx in sample_pages:
            expected_num = pg_idx + 1
            expected_bates = f"MED-{expected_num:04d}"
            page_text = doc[pg_idx].get_text("text")
            matches = bates_pattern.findall(page_text)
            if any(int(m) == expected_num for m in matches):
                correct_bates += 1

        bates_ratio = correct_bates / total_pages_to_check if total_pages_to_check > 0 else 0
        bates_score = 0.35 * bates_ratio
        if bates_ratio >= 1.0:
            print(f"PASS: Component 2 — All {correct_bates}/{total_pages_to_check} pages have correct Bates numbers (0.35 pts)")
            total_score += 0.35
        elif bates_ratio > 0:
            print(f"PARTIAL: Component 2 — {correct_bates}/{total_pages_to_check} pages have correct Bates numbers ({bates_score:.3f} pts)")
            total_score += bates_score
        else:
            print(f"FAIL: Component 2 — No pages have correct Bates numbers")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 4 bookmarks with correct titles and page numbers (0.25 points)
    try:
        toc = doc.get_toc()
        if len(toc) >= 4:
            bookmark_score = 0.0
            per_bookmark = 0.25 / 4.0  # ~0.0625 per bookmark

            for expected in EXPECTED_BOOKMARKS:
                exp_level, exp_title, exp_page = expected
                # Find a matching bookmark (flexible on exact title match)
                found_match = any(
                    (exp_title.lower() in entry[1].lower() or
                     entry[1].lower() in exp_title.lower()) and entry[2] == exp_page
                    for entry in toc
                )
                if found_match:
                    bookmark_score += per_bookmark
                    print(f"  PASS: Bookmark '{exp_title}' at page {exp_page}")
                else:
                    print(f"  FAIL: Bookmark '{exp_title}' at page {exp_page} not found in TOC: {toc}")

            if bookmark_score >= 0.24:  # all 4 found (accounting for float)
                print(f"PASS: Component 3 — All 4 bookmarks correct (0.25 pts)")
                total_score += 0.25
            elif bookmark_score > 0:
                print(f"PARTIAL: Component 3 — Some bookmarks correct ({bookmark_score:.3f} pts)")
                total_score += bookmark_score
            else:
                print(f"FAIL: Component 3 — No correct bookmarks found")
        else:
            print(f"FAIL: Component 3 — Expected >= 4 bookmarks, found {len(toc)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Correct merge order (0.15 points)
    # Verify that content from source PDFs appears at expected page positions
    # Hospital records should be pages 1-45, primary care 46-65, specialist 66-80, imaging 81-90
    try:
        source_files = {
            'hospital_records.pdf': (0, 44),    # pages 1-45 (0-indexed: 0-44)
            'primary_care.pdf': (45, 64),       # pages 46-65 (0-indexed: 45-64)
            'specialist_reports.pdf': (65, 79),  # pages 66-80 (0-indexed: 65-79)
            'imaging_results.pdf': (80, 89),     # pages 81-90 (0-indexed: 80-89)
        }

        order_checks_passed = 0
        total_order_checks = 4

        for src_name, (start_idx, end_idx) in source_files.items():
            src_path = os.path.join(WORKDIR, 'legal', 'medical', src_name)
            if not os.path.exists(src_path):
                print(f"  WARN: Source file {src_name} not found, skipping order check")
                continue
            try:
                src_doc = fitz.open(src_path)
                # Compare first page text of each source with expected position in merged doc
                src_first_text = src_doc[0].get_text("text").strip()[:200]
                merged_text = doc[start_idx].get_text("text").strip()[:200]
                src_doc.close()

                # Remove Bates numbers from merged text for comparison
                merged_clean = bates_pattern.sub('', merged_text).strip()[:200]
                src_clean = src_first_text[:200]

                # Check if at least partial overlap (source content appears in merged)
                # Use first 100 chars of source text as a fingerprint
                if len(src_clean) > 20 and src_clean[:100] in merged_clean or merged_clean[:100] in src_clean:
                    order_checks_passed += 1
                    print(f"  PASS: {src_name} content found at page {start_idx + 1}")
                elif len(src_clean) <= 20:
                    # Very short text, hard to compare; give benefit of doubt if page count matches
                    order_checks_passed += 1
                    print(f"  PASS: {src_name} at page {start_idx + 1} (short text, page count consistent)")
                else:
                    print(f"  FAIL: {src_name} content not found at expected page {start_idx + 1}")
                    print(f"    Source first 80 chars: {src_clean[:80]!r}")
                    print(f"    Merged first 80 chars: {merged_clean[:80]!r}")
            except Exception as e:
                print(f"  ERROR: Checking {src_name}: {e}")

        if order_checks_passed == total_order_checks:
            print(f"PASS: Component 4 — Correct merge order verified (0.15 pts)")
            total_score += 0.15
        elif order_checks_passed > 0:
            partial = 0.15 * (order_checks_passed / total_order_checks)
            print(f"PARTIAL: Component 4 — {order_checks_passed}/{total_order_checks} order checks passed ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Merge order could not be verified")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
