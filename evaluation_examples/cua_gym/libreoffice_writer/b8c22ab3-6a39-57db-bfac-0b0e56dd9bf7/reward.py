"""
Reward Script: Add subject and keywords to document properties
Task ID: writer_struct_016
Domain: libreoffice_writer
Scoring:
  Component 1: Subject set to 'Q4 Financial Review' (0.5 pts)
  Component 2: Keywords set to 'finance, review, quarterly, 2025' (0.4 pts)
  Component 3: Title and Author remain unchanged (0.1 pts)
  Total: 1.0
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_struct_016'

FILE_PATH = f'{WORKDIR}/Desktop/financial_review.docx'

EXPECTED_SUBJECT = 'Q4 Financial Review'
EXPECTED_KEYWORDS = 'finance, review, quarterly, 2025'
EXPECTED_TITLE = 'Financial Review'
EXPECTED_AUTHOR = 'CFO Office'


def verify_task(file_path):
    """
    Verify that the document properties have been correctly set.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document — precondition gate
    try:
        doc = Document(file_path)
        cp = doc.core_properties
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Subject is set to 'Q4 Financial Review' (0.5 points)
    # This should FAIL on initial (subject='') and PASS on golden (subject='Q4 Financial Review')
    try:
        actual_subject = cp.subject
        if actual_subject == EXPECTED_SUBJECT:
            print(f"PASS: Component 1 — Subject is '{actual_subject}' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected subject '{EXPECTED_SUBJECT}', found: {repr(actual_subject)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Keywords are set to 'finance, review, quarterly, 2025' (0.4 points)
    # This should FAIL on initial (keywords='') and PASS on golden
    try:
        actual_keywords = cp.keywords
        if actual_keywords == EXPECTED_KEYWORDS:
            print(f"PASS: Component 2 — Keywords is '{actual_keywords}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Expected keywords '{EXPECTED_KEYWORDS}', found: {repr(actual_keywords)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Title and Author remain unchanged (0.1 points)
    # This checks that the pre-existing metadata was NOT corrupted while making changes.
    # We only award this point if subject or keywords were successfully set (i.e., task was attempted).
    # Without this guard it could pass on initial (since title/author are always correct there).
    # We award it only when Component 1 OR Component 2 passed (task was performed).
    try:
        actual_title = cp.title
        actual_author = cp.author
        task_was_attempted = total_score > 0.0
        if task_was_attempted and actual_title == EXPECTED_TITLE and actual_author == EXPECTED_AUTHOR:
            print(f"PASS: Component 3 — Title='{actual_title}', Author='{actual_author}' unchanged (0.1 pts)")
            total_score += 0.1
        elif not task_was_attempted:
            print(f"SKIP: Component 3 — Skipped as task does not appear to have been performed")
        else:
            print(f"FAIL: Component 3 — Title or Author changed. Title: {repr(actual_title)}, Author: {repr(actual_author)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
