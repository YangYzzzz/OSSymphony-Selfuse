"""
Reward Script: Compare TOC (bookmarks) between two PDFs and write diff report
Task ID: pdf_cr_056
Domain: pdf
Scoring:
  - Component 1 (0.1): toc_diff.txt exists and is non-empty
  - Component 2 (0.3): Added entries correctly identified
  - Component 3 (0.2): Removed entries correctly identified
  - Component 4 (0.4): Modified entries correctly identified
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_056'

DIFF_FILE = os.path.join(WORKDIR, 'Desktop', 'toc_diff.txt')


def normalize(s):
    """Lowercase, collapse whitespace, strip punctuation for fuzzy matching."""
    s = s.lower().strip()
    s = re.sub(r'\s+', ' ', s)
    return s


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: toc_diff.txt must exist
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

    if not content.strip():
        print("CRITICAL: toc_diff.txt is empty")
        print("REWARD: 0.0")
        return 0.0

    content_norm = normalize(content)
    lines_norm = [normalize(line) for line in content.strip().splitlines() if line.strip()]

    # Component 1: File exists and is non-empty (0.1 points)
    # Already confirmed above; this is a task-introduced file (doesn't exist in initial_env)
    if len(content.strip()) > 0:
        print(f"PASS: Component 1 — toc_diff.txt exists and is non-empty (0.1 pts)")
        total_score += 0.1

    # Component 2: Added entries correctly identified (0.3 points)
    # Expected: Background (page 2) and Discussion (page 8)
    try:
        added_score = 0.0

        # Check for "added" section mentioning both entries
        has_added_section = 'added' in content_norm

        # Check for Background page 2
        has_background = bool(re.search(r'background.*(?:page\s*)?2', content_norm))

        # Check for Discussion page 8
        has_discussion = bool(re.search(r'discussion.*(?:page\s*)?8', content_norm))

        if has_added_section and has_background and has_discussion:
            added_score = 0.3
            print(f"PASS: Component 2 — Both added entries found: Background (page 2), Discussion (page 8) (0.3 pts)")
        elif has_background and has_discussion:
            added_score = 0.2
            print(f"PARTIAL: Component 2 — Both added entries found but 'Added' section label missing (0.2 pts)")
        elif has_added_section and (has_background or has_discussion):
            added_score = 0.15
            print(f"PARTIAL: Component 2 — Added section found but only one entry correct (0.15 pts)")
        else:
            print(f"FAIL: Component 2 — Added entries not correctly identified. has_added={has_added_section}, background={has_background}, discussion={has_discussion}")

        if added_score > 0:
            total_score += added_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Removed entries correctly identified (0.2 points)
    # Expected: None
    try:
        removed_score = 0.0

        has_removed_section = 'removed' in content_norm
        # Check that it says "none" for removed entries
        has_none = bool(re.search(r'removed.*none', content_norm))

        if has_removed_section and has_none:
            removed_score = 0.2
            print(f"PASS: Component 3 — Removed entries correctly reported as None (0.2 pts)")
        elif has_removed_section:
            # Has removed section but doesn't say None - partial
            removed_score = 0.05
            print(f"PARTIAL: Component 3 — Removed section found but 'None' not identified (0.05 pts)")
        else:
            print(f"FAIL: Component 3 — Removed entries section not found")

        if removed_score > 0:
            total_score += removed_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Modified entries correctly identified (0.4 points)
    # Expected: Methods (page 3 -> 4) and Results (page 5 -> 6)
    try:
        modified_score = 0.0

        has_modified_section = 'modified' in content_norm

        # Check for Methods page change 3 -> 4
        has_methods = bool(re.search(r'methods.*3.*4', content_norm))

        # Check for Results page change 5 -> 6
        has_results = bool(re.search(r'results.*5.*6', content_norm))

        if has_modified_section and has_methods and has_results:
            modified_score = 0.4
            print(f"PASS: Component 4 — Both modified entries found: Methods (3->4), Results (5->6) (0.4 pts)")
        elif has_methods and has_results:
            modified_score = 0.3
            print(f"PARTIAL: Component 4 — Both modified entries found but 'Modified' section label missing (0.3 pts)")
        elif has_modified_section and (has_methods or has_results):
            modified_score = 0.2
            print(f"PARTIAL: Component 4 — Modified section found but only one entry correct (0.2 pts)")
        else:
            print(f"FAIL: Component 4 — Modified entries not correctly identified. has_modified={has_modified_section}, methods={has_methods}, results={has_results}")

        if modified_score > 0:
            total_score += modified_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
