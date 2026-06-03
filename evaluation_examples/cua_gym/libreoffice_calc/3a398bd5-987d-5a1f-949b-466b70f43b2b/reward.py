"""
Reward Script: Set PDF metadata for report.pdf and save as report_metadata.pdf
Task ID: pdf_ro_025
Domain: pdf (libreoffice_calc label but actually PDF task)
Scoring:
  - Component 1: Output file exists and is a valid PDF (0.1 pts)
  - Component 2: Title metadata correct (0.2 pts)
  - Component 3: Author metadata correct (0.2 pts)
  - Component 4: Subject metadata correct (0.15 pts)
  - Component 5: Keywords metadata correct (0.15 pts)
  - Component 6: Creator metadata correct (0.1 pts)
  - Component 7: Page count preserved (15 pages) (0.1 pts)
"""

import os
import pymupdf  # PyMuPDF / fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_025'

# The task requires saving to this specific path
OUTPUT_PATH = os.path.join(WORKDIR, 'Documents', 'report_metadata.pdf')

# Expected metadata values from task instruction
EXPECTED_METADATA = {
    'title': 'Q4 Financial Report',
    'author': 'Finance Team',
    'subject': 'Quarterly Financial Summary',
    'keywords': 'finance, quarterly, report, 2025, Q4',
    'creator': 'CUA-Gym PDF Generator',
}

EXPECTED_PAGE_COUNT = 15


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must be a valid PDF
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    meta = doc.metadata
    page_count = len(doc)
    doc.close()

    # Component 1: Output file is a valid PDF with content (0.1 points)
    # This checks that the file was actually created as a proper PDF
    # (Fails on initial_env because report_metadata.pdf doesn't exist there)
    try:
        if page_count > 0:
            print(f"PASS: Component 1 — Valid PDF with {page_count} pages (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — PDF has 0 pages")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Title metadata (0.2 points)
    try:
        actual_title = (meta.get('title', '') or '').strip()
        expected_title = EXPECTED_METADATA['title']
        if actual_title == expected_title:
            print(f"PASS: Component 2 — Title = '{actual_title}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Title: expected '{expected_title}', found '{actual_title}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Author metadata (0.2 points)
    try:
        actual_author = (meta.get('author', '') or '').strip()
        expected_author = EXPECTED_METADATA['author']
        if actual_author == expected_author:
            print(f"PASS: Component 3 — Author = '{actual_author}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Author: expected '{expected_author}', found '{actual_author}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Subject metadata (0.15 points)
    try:
        actual_subject = (meta.get('subject', '') or '').strip()
        expected_subject = EXPECTED_METADATA['subject']
        if actual_subject == expected_subject:
            print(f"PASS: Component 4 — Subject = '{actual_subject}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Subject: expected '{expected_subject}', found '{actual_subject}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Keywords metadata (0.15 points)
    try:
        actual_keywords = (meta.get('keywords', '') or '').strip()
        expected_keywords = EXPECTED_METADATA['keywords']
        if actual_keywords == expected_keywords:
            print(f"PASS: Component 5 — Keywords = '{actual_keywords}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Keywords: expected '{expected_keywords}', found '{actual_keywords}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Creator metadata (0.1 points)
    try:
        actual_creator = (meta.get('creator', '') or '').strip()
        expected_creator = EXPECTED_METADATA['creator']
        if actual_creator == expected_creator:
            print(f"PASS: Component 6 — Creator = '{actual_creator}' (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 6 — Creator: expected '{expected_creator}', found '{actual_creator}'")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Page count preserved at 15 pages (0.1 points)
    # Ensures the content wasn't lost during metadata setting
    try:
        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 7 — Page count = {page_count} (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 7 — Page count: expected {EXPECTED_PAGE_COUNT}, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
