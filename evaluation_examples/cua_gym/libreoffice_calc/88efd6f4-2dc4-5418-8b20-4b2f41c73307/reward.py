"""
Reward Script: PDF integrity verification report
Task ID: pdf_gf1_038
Domain: pdf (libreoffice_calc listed but actually pdf task)
Scoring:
  Component 1 (0.25): archive_check.txt exists and is non-empty
  Component 2 (0.25): Report contains page count (15 pages)
  Component 3 (0.25): Report mentions validity / cross-reference check results
  Component 4 (0.25): Report contains a final Status line (PASS or FAIL)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_038'

REPORT_PATH = os.path.join(WORKDIR, 'Documents', 'archive_check.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: report file must exist
    if not os.path.exists(REPORT_PATH):
        print(f"CRITICAL: Report file not found: {REPORT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(REPORT_PATH, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read report file: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not content.strip():
        print("CRITICAL: Report file is empty")
        print("REWARD: 0.0")
        return 0.0

    content_lower = content.lower()

    # Component 1: Report file exists and is non-empty with meaningful content (0.25 points)
    # The file must reference the PDF being verified (archive.pdf or the path)
    try:
        has_pdf_reference = ('archive.pdf' in content_lower or
                             'archive' in content_lower or
                             'pdf' in content_lower)
        if has_pdf_reference and len(content.strip()) > 20:
            print(f"PASS: Component 1 — Report exists with meaningful content ({len(content)} chars) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Report lacks meaningful PDF-related content")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Report contains page count information showing 15 pages (0.25 points)
    try:
        # Accept various formats: "Pages: 15", "15 pages", "page count: 15", "Page count: 15", etc.
        page_count_match = (
            re.search(r'pages?\s*:\s*15\b', content_lower) or
            re.search(r'\b15\s+pages?\b', content_lower) or
            re.search(r'page\s*count\s*:\s*15\b', content_lower) or
            re.search(r'total\s+pages?\s*:\s*15\b', content_lower) or
            re.search(r'number\s+of\s+pages?\s*:\s*15\b', content_lower)
        )
        if page_count_match:
            print(f"PASS: Component 2 — Page count '15' found in report (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Page count '15' not found. Content snippet: {content[:200]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Report mentions PDF validity and cross-reference check (0.25 points)
    try:
        # Check for validity mention
        has_validity = (
            'valid' in content_lower or
            'no errors' in content_lower or
            'no error' in content_lower or
            'integrity' in content_lower or
            'verified' in content_lower
        )
        # Check for cross-reference mention
        has_xref = (
            'cross-reference' in content_lower or
            'cross reference' in content_lower or
            'xref' in content_lower or
            'cross_reference' in content_lower or
            'no errors detected' in content_lower
        )
        if has_validity and has_xref:
            print(f"PASS: Component 3 — Validity and cross-reference checks present (0.25 pts)")
            total_score += 0.25
        elif has_validity:
            # Partial: validity found but no xref mention — give half credit
            print(f"PARTIAL: Component 3 — Validity check found but no cross-reference mention (0.125 pts)")
            total_score += 0.125
        else:
            print(f"FAIL: Component 3 — No validity or cross-reference check found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Report contains a final status line (Status: PASS or Status: FAIL) (0.25 points)
    try:
        status_match = re.search(r'status\s*:\s*(pass|fail)', content_lower)
        if status_match:
            status_value = status_match.group(1).upper()
            print(f"PASS: Component 4 — Status line found: 'Status: {status_value}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — No 'Status: PASS' or 'Status: FAIL' line found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
