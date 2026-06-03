"""
Reward Script: Extract and compare images between two PDF brochure versions
Task ID: pdf_cr_065
Domain: pdf
Scoring:
  Component 1 (0.20): File exists, references both PDFs, covers all pages
  Component 2 (0.25): Correct per-page image counts for v1 (2, 3, 1, 2)
  Component 3 (0.25): Correct per-page image counts for v2 (2, 2, 2, 1)
  Component 4 (0.30): Summary line with correct totals and change counts
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_065'
DIFF_FILE = os.path.join(WORKDIR, 'Desktop', 'image_diff.txt')

# Expected per-page image counts derived from the PDFs
V1_COUNTS = {1: 2, 2: 3, 3: 1, 4: 2}  # page -> image count in v1
V2_COUNTS = {1: 2, 2: 2, 3: 2, 4: 1}  # page -> image count in v2
V1_TOTAL = 8
V2_TOTAL = 7
EXPECTED_ADDED = 1
EXPECTED_REMOVED = 2
EXPECTED_CHANGED = 2


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist
    if not os.path.exists(DIFF_FILE):
        print(f"CRITICAL: File not found: {DIFF_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = open(DIFF_FILE, 'r').read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {DIFF_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(content.strip()) < 50:
        print(f"CRITICAL: File too short ({len(content.strip())} chars), likely empty or stub")
        print("REWARD: 0.0")
        return 0.0

    content_lower = content.lower()

    # Component 1: File references both PDFs and covers all 4 pages (0.20 points)
    try:
        has_v1_ref = 'v1' in content_lower or 'brochure_v1' in content_lower
        has_v2_ref = 'v2' in content_lower or 'brochure_v2' in content_lower
        # Check that multiple pages are referenced
        page_refs = re.findall(r'page\s*\d+', content_lower)
        num_page_refs = len(set(page_refs))

        if has_v1_ref and has_v2_ref and num_page_refs >= 3:
            print(f"PASS: Component 1 -- References both PDFs, {num_page_refs} distinct page refs (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- v1_ref={has_v1_ref}, v2_ref={has_v2_ref}, page_refs={num_page_refs}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Correct per-page image counts for v1 (0.25 points)
    # We look for patterns like "v1: N image" per page section
    try:
        v1_correct = 0
        v1_total_pages = len(V1_COUNTS)
        for page_num, expected_count in V1_COUNTS.items():
            # Look for page section, then v1 image count
            # Flexible: "v1: 2 image(s)" or "2 image(s)" near v1 context
            # Search within page section for v1 count
            page_pattern = re.compile(
                r'page\s*' + str(page_num) + r'.*?(?=page\s*\d+|summary|$)',
                re.DOTALL | re.IGNORECASE
            )
            page_match = page_pattern.search(content)
            if page_match:
                section = page_match.group(0)
                # Look for v1 image count in this section
                v1_count_match = re.search(
                    r'v1[:\s]+(\d+)\s+image', section, re.IGNORECASE
                )
                if v1_count_match and int(v1_count_match.group(1)) == expected_count:
                    v1_correct += 1

        points_per_page = 0.25 / v1_total_pages
        comp2_score = v1_correct * points_per_page
        if v1_correct == v1_total_pages:
            print(f"PASS: Component 2 -- All v1 per-page counts correct ({v1_correct}/{v1_total_pages}) (0.25 pts)")
        elif v1_correct > 0:
            print(f"PARTIAL: Component 2 -- v1 counts {v1_correct}/{v1_total_pages} correct ({comp2_score:.3f} pts)")
        else:
            print(f"FAIL: Component 2 -- No v1 per-page counts matched")
        total_score += comp2_score
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Correct per-page image counts for v2 (0.25 points)
    try:
        v2_correct = 0
        v2_total_pages = len(V2_COUNTS)
        for page_num, expected_count in V2_COUNTS.items():
            page_pattern = re.compile(
                r'page\s*' + str(page_num) + r'.*?(?=page\s*\d+|summary|$)',
                re.DOTALL | re.IGNORECASE
            )
            page_match = page_pattern.search(content)
            if page_match:
                section = page_match.group(0)
                v2_count_match = re.search(
                    r'v2[:\s]+(\d+)\s+image', section, re.IGNORECASE
                )
                if v2_count_match and int(v2_count_match.group(1)) == expected_count:
                    v2_correct += 1

        points_per_page = 0.25 / v2_total_pages
        comp3_score = v2_correct * points_per_page
        if v2_correct == v2_total_pages:
            print(f"PASS: Component 3 -- All v2 per-page counts correct ({v2_correct}/{v2_total_pages}) (0.25 pts)")
        elif v2_correct > 0:
            print(f"PARTIAL: Component 3 -- v2 counts {v2_correct}/{v2_total_pages} correct ({comp3_score:.3f} pts)")
        else:
            print(f"FAIL: Component 3 -- No v2 per-page counts matched")
        total_score += comp3_score
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Summary with correct totals and change counts (0.30 points)
    try:
        comp4_score = 0.0

        # Check v1 total
        v1_total_match = re.search(r'v1[:\s]+(\d+)\s+images?\s+total', content, re.IGNORECASE)
        if v1_total_match and int(v1_total_match.group(1)) == V1_TOTAL:
            comp4_score += 0.06
            print(f"  PASS: v1 total = {V1_TOTAL}")
        else:
            found = v1_total_match.group(1) if v1_total_match else 'not found'
            print(f"  FAIL: v1 total expected {V1_TOTAL}, found: {found}")

        # Check v2 total
        v2_total_match = re.search(r'v2[:\s]+(\d+)\s+images?\s+total', content, re.IGNORECASE)
        if v2_total_match and int(v2_total_match.group(1)) == V2_TOTAL:
            comp4_score += 0.06
            print(f"  PASS: v2 total = {V2_TOTAL}")
        else:
            found = v2_total_match.group(1) if v2_total_match else 'not found'
            print(f"  FAIL: v2 total expected {V2_TOTAL}, found: {found}")

        # Check Added count
        added_match = re.search(r'added[:\s]+(\d+)', content, re.IGNORECASE)
        if added_match and int(added_match.group(1)) == EXPECTED_ADDED:
            comp4_score += 0.06
            print(f"  PASS: Added = {EXPECTED_ADDED}")
        else:
            found = added_match.group(1) if added_match else 'not found'
            print(f"  FAIL: Added expected {EXPECTED_ADDED}, found: {found}")

        # Check Removed count
        removed_match = re.search(r'removed[:\s]+(\d+)', content, re.IGNORECASE)
        if removed_match and int(removed_match.group(1)) == EXPECTED_REMOVED:
            comp4_score += 0.06
            print(f"  PASS: Removed = {EXPECTED_REMOVED}")
        else:
            found = removed_match.group(1) if removed_match else 'not found'
            print(f"  FAIL: Removed expected {EXPECTED_REMOVED}, found: {found}")

        # Check Changed/Potentially changed count
        # Must be careful: "changed" appears in per-page lines like "potentially changed: 450x250 -> 450x200"
        # The summary line is like "Potentially changed: 2" (just a number, no 'x')
        changed_match = re.search(r'(?:potentially\s+)?changed[:\s]+(\d+)(?![x\d])', content, re.IGNORECASE)
        if changed_match and int(changed_match.group(1)) == EXPECTED_CHANGED:
            comp4_score += 0.06
            print(f"  PASS: Changed = {EXPECTED_CHANGED}")
        else:
            found = changed_match.group(1) if changed_match else 'not found'
            print(f"  FAIL: Changed expected {EXPECTED_CHANGED}, found: {found}")

        if comp4_score >= 0.29:
            print(f"PASS: Component 4 -- All summary values correct (0.30 pts)")
            total_score += 0.30
        elif comp4_score > 0:
            print(f"PARTIAL: Component 4 -- Some summary values correct ({comp4_score:.3f} pts)")
            total_score += comp4_score
        else:
            print(f"FAIL: Component 4 -- No summary values matched")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
