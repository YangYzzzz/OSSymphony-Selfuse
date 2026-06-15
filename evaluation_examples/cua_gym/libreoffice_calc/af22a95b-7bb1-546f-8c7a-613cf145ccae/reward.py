"""
Reward Script: PDF Accessibility Audit
Task ID: pdf_cr_060
Domain: pdf (libreoffice_calc listed but actual domain is pdf)
Scoring:
  Component 1 (0.20): accessibility.txt file exists
  Component 2 (0.20): Report contains title metadata check with PASS and correct title
  Component 3 (0.20): Report contains extractable text check with PASS
  Component 4 (0.20): Report contains TOC check with PASS
  Component 5 (0.20): Report contains language metadata check with PASS and overall score line
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_060'

PDF_PATH = os.path.join(WORKDIR, 'Desktop', 'accessible.pdf')
REPORT_PATH = os.path.join(WORKDIR, 'Desktop', 'accessibility.txt')

# Ground truth values from the PDF (verified via VM exploration)
EXPECTED_TITLE = "Greenfield Sustainability Initiative - Annual Progress Report FY2025"
EXPECTED_PAGE_COUNT = 5
EXPECTED_TOC_ENTRIES = 6
EXPECTED_LANGUAGE = "en-US"


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: PDF must exist (not scored — it exists in both envs)
    if not os.path.exists(PDF_PATH):
        print(f"CRITICAL: PDF not found at {PDF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: accessibility.txt must exist to score anything
    # This is the primary task output — if it doesn't exist, score is 0.0
    if not os.path.exists(REPORT_PATH):
        print(f"FAIL: accessibility.txt not found at {REPORT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(REPORT_PATH, 'r') as f:
            report_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {REPORT_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    report_lower = report_content.lower()

    # Component 1: Report file exists and is non-empty with meaningful content (0.20 points)
    # This checks that the file is a real accessibility report, not just an empty file
    try:
        if len(report_content.strip()) > 50 and ('accessibility' in report_lower or 'audit' in report_lower or 'check' in report_lower or 'pass' in report_lower or 'fail' in report_lower):
            print(f"PASS: Component 1 — accessibility.txt exists with meaningful content ({len(report_content)} chars) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — accessibility.txt exists but has insufficient content ({len(report_content.strip())} chars)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Title metadata check present with PASS and correct title (0.20 points)
    # The report should indicate the document title was found in metadata
    try:
        # Look for a line mentioning title + PASS
        title_pass = False
        for line in report_content.split('\n'):
            line_lower = line.lower()
            if 'title' in line_lower and ('pass' in line_lower or 'yes' in line_lower or 'found' in line_lower):
                # Also verify the actual title string appears somewhere in the report
                if 'greenfield' in report_content.lower() or EXPECTED_TITLE.lower() in report_content.lower():
                    title_pass = True
                    break
        if title_pass:
            print(f"PASS: Component 2 — Title metadata check PASS with correct title mentioned (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Title metadata check not found or not PASS with correct title")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Extractable text check present with PASS (0.20 points)
    # The report should confirm all pages have extractable text
    try:
        text_pass = False
        for line in report_content.split('\n'):
            line_lower = line.lower()
            if ('text' in line_lower or 'extractable' in line_lower) and ('pass' in line_lower or 'yes' in line_lower):
                text_pass = True
                break
        if text_pass:
            print(f"PASS: Component 3 — Extractable text check PASS (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Extractable text check not found or not PASS")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Table of contents check present with PASS (0.20 points)
    # The report should confirm TOC/bookmarks exist
    try:
        toc_pass = False
        for line in report_content.split('\n'):
            line_lower = line.lower()
            if ('table of contents' in line_lower or 'toc' in line_lower or 'contents' in line_lower or 'bookmark' in line_lower) and ('pass' in line_lower or 'yes' in line_lower or 'present' in line_lower):
                toc_pass = True
                break
        if toc_pass:
            print(f"PASS: Component 4 — TOC check PASS (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — TOC check not found or not PASS")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Language metadata check and overall score (0.20 points)
    # The report should mention language check and provide an overall accessibility score
    try:
        lang_pass = False
        score_line = False
        for line in report_content.split('\n'):
            line_lower = line.lower()
            if 'language' in line_lower and ('pass' in line_lower or 'yes' in line_lower or 'en' in line_lower):
                lang_pass = True
            if 'score' in line_lower or 'overall' in line_lower or '/4' in line or 'checks passed' in line_lower:
                score_line = True

        if lang_pass and score_line:
            print(f"PASS: Component 5 — Language check PASS and overall score present (0.20 pts)")
            total_score += 0.20
        elif lang_pass:
            print(f"PARTIAL: Component 5 — Language check PASS but no overall score line (0.10 pts)")
            total_score += 0.10
        elif score_line:
            print(f"PARTIAL: Component 5 — Overall score present but language check missing (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Neither language check nor overall score found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(REPORT_PATH):
    print(f"File not found: {REPORT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
