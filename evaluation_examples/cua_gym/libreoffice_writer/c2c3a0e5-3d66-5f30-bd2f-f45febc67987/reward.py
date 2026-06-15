"""
Reward Script: Set document properties (title, subject, author, keywords)
Task ID: writer_struct_061
Domain: libreoffice_writer
Scoring:
  Component 1: Title == 'Machine Learning Workflow Specification'  (0.25 pts)
  Component 2: Subject == 'Technical Specification v2.1'           (0.25 pts)
  Component 3: Author == 'AI Engineering Team'                     (0.25 pts)
  Component 4: Keywords == 'ML, pipeline, specification, v2.1'    (0.25 pts)
  Total: 1.0

All four properties are empty in initial_env and must be set in golden_env.
"""

import os

from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_struct_061'
FILE_NAME = 'ml_spec.docx'

# Expected property values (ground truth from task context)
EXPECTED_TITLE    = 'Machine Learning Workflow Specification'
EXPECTED_SUBJECT  = 'Technical Specification v2.1'
EXPECTED_AUTHOR   = 'AI Engineering Team'
EXPECTED_KEYWORDS = 'ML, pipeline, specification, v2.1'


def verify_task(file_path):
    """
    Verify that all four document properties were correctly set.
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

    # Component 1: Title property (0.25 points)
    # Must transition from empty string '' to 'Machine Learning Workflow Specification'
    try:
        actual_title = cp.title
        if actual_title == EXPECTED_TITLE:
            print(f"PASS: Component 1 — title == '{actual_title}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected title '{EXPECTED_TITLE}', found '{actual_title}'")
    except Exception as e:
        print(f"ERROR: Component 1 — could not read title: {e}")

    # Component 2: Subject property (0.25 points)
    # Must transition from empty string '' to 'Technical Specification v2.1'
    try:
        actual_subject = cp.subject
        if actual_subject == EXPECTED_SUBJECT:
            print(f"PASS: Component 2 — subject == '{actual_subject}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected subject '{EXPECTED_SUBJECT}', found '{actual_subject}'")
    except Exception as e:
        print(f"ERROR: Component 2 — could not read subject: {e}")

    # Component 3: Author (creator) property (0.25 points)
    # Must transition from empty string '' to 'AI Engineering Team'
    try:
        actual_author = cp.author
        if actual_author == EXPECTED_AUTHOR:
            print(f"PASS: Component 3 — author == '{actual_author}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — expected author '{EXPECTED_AUTHOR}', found '{actual_author}'")
    except Exception as e:
        print(f"ERROR: Component 3 — could not read author: {e}")

    # Component 4: Keywords property (0.25 points)
    # Must transition from empty string '' to 'ML, pipeline, specification, v2.1'
    try:
        actual_keywords = cp.keywords
        if actual_keywords == EXPECTED_KEYWORDS:
            print(f"PASS: Component 4 — keywords == '{actual_keywords}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — expected keywords '{EXPECTED_KEYWORDS}', found '{actual_keywords}'")
    except Exception as e:
        print(f"ERROR: Component 4 — could not read keywords: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = os.path.join(WORKDIR, FILE_NAME)
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
