"""
Reward Script: Compare PDF metadata and write differences to a text file
Task ID: pdf_mbc_017
Domain: pdf
Scoring:
  Component 1 (0.30): Title change correctly reported (Draft Report -> Final Report)
  Component 2 (0.30): Author change correctly reported (John -> John Smith)
  Component 3 (0.20): ModDate change reported
  Component 4 (0.20): No false positives (Subject/Keywords not reported as changed)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_017'
DIFF_FILE = os.path.join(WORKDIR, 'Documents', 'metadata_diff.txt')


def verify_task():
    """
    Verify that metadata_diff.txt correctly reports metadata differences
    between report_v1.pdf and report_v2.pdf.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: diff file must exist and be non-empty
    if not os.path.exists(DIFF_FILE):
        print(f"CRITICAL: Diff file not found: {DIFF_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(DIFF_FILE, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read diff file: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not content.strip():
        print("CRITICAL: Diff file is empty")
        print("REWARD: 0.0")
        return 0.0

    content_lower = content.lower()

    # Component 1: Title change correctly reported (0.30 points)
    # The file should mention Title changed from 'Draft Report' to 'Final Report'
    try:
        has_title_field = 'title' in content_lower
        has_draft_report = 'draft report' in content_lower
        has_final_report = 'final report' in content_lower
        if has_title_field and has_draft_report and has_final_report:
            print(f"PASS: Component 1 — Title change correctly reported: Draft Report -> Final Report (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Title change not fully reported. "
                  f"Has 'title': {has_title_field}, 'draft report': {has_draft_report}, 'final report': {has_final_report}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Author change correctly reported (0.30 points)
    # The file should mention Author changed from 'John' to 'John Smith'
    try:
        has_author_field = 'author' in content_lower
        # Need to check that both 'John' (old value) and 'John Smith' (new value) appear
        # 'John Smith' contains 'John', so we just check for 'john smith' specifically
        has_john_smith = 'john smith' in content_lower
        if has_author_field and has_john_smith:
            print(f"PASS: Component 2 — Author change correctly reported: John -> John Smith (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Author change not fully reported. "
                  f"Has 'author': {has_author_field}, 'john smith': {has_john_smith}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: ModDate change reported (0.20 points)
    # The file should mention ModDate changed (with old/new dates)
    try:
        has_moddate = 'moddate' in content_lower or 'mod date' in content_lower or 'modification date' in content_lower
        has_date_values = ('20240601' in content or '2024-06-01' in content or '2024/06/01' in content) and \
                          ('20240815' in content or '2024-08-15' in content or '2024/08/15' in content)
        # Also accept if moddate is mentioned even without exact date strings
        # (the task says "ModDate changed" is sufficient)
        if has_moddate and has_date_values:
            print(f"PASS: Component 3 — ModDate change correctly reported with date values (0.20 pts)")
            total_score += 0.20
        elif has_moddate:
            # Partial: ModDate field mentioned but dates not fully spelled out
            print(f"PARTIAL: Component 3 — ModDate mentioned but date values not fully matched (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — ModDate change not reported")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: No false positives (0.20 points)
    # Subject and Keywords should NOT be reported as changed
    # They should either not be mentioned, or explicitly listed as unchanged
    try:
        # Check if the file falsely reports Subject or Keywords as changed
        # Look for patterns like "Subject: ... -> ..." or "Subject changed"
        import re

        # Split content into "changed" and "unchanged" sections if they exist
        # Common patterns: a "Changed fields:" section and "Unchanged fields:" section
        changed_section = ''
        unchanged_section = ''

        # Try to split by common section headers
        changed_match = re.search(r'(?i)(changed\s+fields?|differences?|changed):?\s*\n(.*?)(?=\n\s*(unchanged|$))',
                                  content, re.DOTALL)
        if changed_match:
            changed_section = changed_match.group(2).lower()
        else:
            # No explicit sections, treat entire content as the changed report
            changed_section = content_lower

        # Check if Subject or Keywords appear in the changed section as changed items
        # A false positive is mentioning them as changed (not as unchanged)
        subject_false_positive = False
        keywords_false_positive = False

        # If there are explicit unchanged/changed sections, check only the changed section
        if 'unchanged' in content_lower:
            # File has both sections - check the changed section only
            parts = re.split(r'(?i)unchanged\s+fields?:?', content)
            changed_part = parts[0].lower() if parts else content_lower

            # Subject should NOT appear in the changed section as a diff item
            # Look for "Subject" as a line item in the changed part
            subject_in_changed = bool(re.search(r'(?i)[-*]\s*subject\s*:', changed_part))
            keywords_in_changed = bool(re.search(r'(?i)[-*]\s*keywords?\s*:', changed_part))

            subject_false_positive = subject_in_changed
            keywords_false_positive = keywords_in_changed
        else:
            # No sections - if Subject or Keywords appear at all as changed items, it's a false positive
            # But they might appear just as context. Look for diff-style patterns:
            subject_false_positive = bool(re.search(r'(?i)subject\s*:.*->|subject\s+changed', content))
            keywords_false_positive = bool(re.search(r'(?i)keywords?\s*:.*->|keywords?\s+changed', content))

        if not subject_false_positive and not keywords_false_positive:
            print(f"PASS: Component 4 — No false positives for Subject/Keywords (0.20 pts)")
            total_score += 0.20
        else:
            details = []
            if subject_false_positive:
                details.append('Subject falsely reported as changed')
            if keywords_false_positive:
                details.append('Keywords falsely reported as changed')
            print(f"FAIL: Component 4 — False positives detected: {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
