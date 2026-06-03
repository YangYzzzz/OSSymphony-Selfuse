"""
Reward Script: Verify page order of manual.pdf and write report to page_order.txt
Task ID: pdf_cr_064
Domain: pdf
Scoring:
  Component 1 (0.25): page_order.txt exists and has per-page lines for all 8 pages
  Component 2 (0.35): Each per-page line correctly identifies printed page number and MATCH/MISMATCH
  Component 3 (0.20): Summary line with correct count of correctly ordered pages
  Component 4 (0.20): Mismatch detail section lists all mismatched pages correctly
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_064'

# Ground truth: the PDF has 8 pages. Chapters on each physical page:
# Phys 1 -> Ch 1 (MATCH), Phys 2 -> Ch 3 (MISMATCH), Phys 3 -> Ch 2 (MISMATCH),
# Phys 4 -> Ch 4 (MATCH), Phys 5 -> Ch 6 (MISMATCH), Phys 6 -> Ch 5 (MISMATCH),
# Phys 7 -> Ch 7 (MATCH), Phys 8 -> Ch 8 (MATCH)
EXPECTED_MAPPING = {
    1: 1,  # MATCH
    2: 3,  # MISMATCH
    3: 2,  # MISMATCH
    4: 4,  # MATCH
    5: 6,  # MISMATCH
    6: 5,  # MISMATCH
    7: 7,  # MATCH
    8: 8,  # MATCH
}
TOTAL_PAGES = 8
CORRECT_COUNT = 4  # pages where physical == printed
MISMATCH_PAGES = {2, 3, 5, 6}  # physical pages that are mismatched


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    report_path = os.path.join(WORKDIR, 'Desktop', 'page_order.txt')

    # Gate: file must exist (task asks agent to create it)
    if not os.path.exists(report_path):
        print(f"CRITICAL: Report file not found: {report_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = open(report_path, 'r').read()
    except Exception as e:
        print(f"CRITICAL: Cannot read report file: {e}")
        print("REWARD: 0.0")
        return 0.0

    lines = content.strip().split('\n')
    content_lower = content.lower()

    # Component 1: Per-page lines exist for all 8 pages (0.25 points)
    # Look for lines mentioning each physical page (1-8)
    try:
        page_lines_found = 0
        for phys_page in range(1, TOTAL_PAGES + 1):
            # Match patterns like "Physical page X" or "Page X:" at start
            pattern = re.compile(
                rf'(?:physical\s+)?page\s+{phys_page}\b', re.IGNORECASE
            )
            if pattern.search(content):
                page_lines_found += 1

        if page_lines_found >= TOTAL_PAGES:
            print(f"PASS: Component 1 -- All {TOTAL_PAGES} pages referenced in report ({page_lines_found} found) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- Only {page_lines_found}/{TOTAL_PAGES} pages referenced in report")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Per-page lines correctly identify printed page number and MATCH/MISMATCH (0.35 points)
    # Each correct line earns 0.35/8 points
    try:
        correct_lines = 0
        per_line_score = 0.35 / TOTAL_PAGES

        for phys_page in range(1, TOTAL_PAGES + 1):
            expected_printed = EXPECTED_MAPPING[phys_page]
            is_match = (phys_page == expected_printed)
            expected_label = "MATCH" if is_match else "MISMATCH"

            # Look for a line that mentions the physical page and the printed page number
            # Pattern: physical page X ... Page Y ... MATCH/MISMATCH
            matching_lines = [
                line.strip() for line in lines
                if re.search(rf'(?:physical\s+)?page\s+{phys_page}\b', line.strip(), re.IGNORECASE)
                and re.search(rf'page\s+{expected_printed}\b', line.strip(), re.IGNORECASE)
                and (
                    (expected_label == "MATCH" and "MATCH" in line.strip().upper())
                    or (expected_label == "MISMATCH" and "MISMATCH" in line.strip().upper())
                )
            ]

            if len(matching_lines) > 0:
                correct_lines += 1

        awarded = correct_lines * per_line_score
        if correct_lines > 0:
            print(f"PASS: Component 2 -- {correct_lines}/{TOTAL_PAGES} per-page lines correct ({awarded:.3f} pts)")
            total_score += awarded
        else:
            print(f"FAIL: Component 2 -- No per-page lines correctly identify printed page and match status")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Summary line with correct count (0.20 points)
    # Expected: "Correctly ordered: 4 of 8 pages" or similar
    try:
        # Look for a summary indicating 4 of 8 (or 4/8, or 50%)
        summary_pattern = re.search(
            rf'(\d+)\s*(?:of|out\s+of|/)\s*{TOTAL_PAGES}\s*(?:pages?)?',
            content, re.IGNORECASE
        )
        if summary_pattern:
            reported_count = int(summary_pattern.group(1))
            if reported_count == CORRECT_COUNT:
                print(f"PASS: Component 3 -- Summary correctly reports {CORRECT_COUNT} of {TOTAL_PAGES} pages ordered (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 -- Summary reports {reported_count} of {TOTAL_PAGES}, expected {CORRECT_COUNT}")
        else:
            print(f"FAIL: Component 3 -- No summary line found with 'X of {TOTAL_PAGES}' pattern")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Mismatch details list (0.20 points)
    # Expected: identifies all 4 mismatched pages with their printed page numbers
    try:
        mismatches_found = 0
        for phys_page in sorted(MISMATCH_PAGES):
            expected_printed = EXPECTED_MAPPING[phys_page]
            # Look for mention of physical page N containing/having Page M
            # Pattern: "page 2 contains Page 3" or "Physical page 2 ... Page 3"
            pattern = re.compile(
                rf'(?:physical\s+)?page\s+{phys_page}\b.*?page\s+{expected_printed}\b',
                re.IGNORECASE
            )
            if pattern.search(content):
                mismatches_found += 1

        per_mismatch_score = 0.20 / len(MISMATCH_PAGES)
        awarded = mismatches_found * per_mismatch_score
        if mismatches_found > 0:
            print(f"PASS: Component 4 -- {mismatches_found}/{len(MISMATCH_PAGES)} mismatched pages detailed ({awarded:.3f} pts)")
            total_score += awarded
        else:
            print(f"FAIL: Component 4 -- No mismatch details found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
