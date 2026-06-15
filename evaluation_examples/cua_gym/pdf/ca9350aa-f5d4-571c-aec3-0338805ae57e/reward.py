"""
Reward Script: Update PDF metadata
Task ID: pdf_res_015
Domain: pdf
Scoring:
  - Component 1: Output file exists at correct path (precondition gate)
  - Component 2: Title metadata matches (0.25 pts)
  - Component 3: Author metadata matches (0.25 pts)
  - Component 4: Subject metadata matches (0.25 pts)
  - Component 5: Keywords metadata matches (0.25 pts)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_015'

# Expected metadata values from task instruction
EXPECTED_TITLE = 'Deep Learning for Natural Language Processing: A Survey'
EXPECTED_AUTHOR = 'Alice Zhang, Bob Smith'
EXPECTED_SUBJECT = 'Computer Science, NLP'
EXPECTED_KEYWORDS = 'deep learning, NLP, transformers, attention'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(file_path):
        print(f"FAIL: Output file not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
        meta = doc.metadata
        doc.close()
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Title metadata matches (0.25 points)
    try:
        actual_title = (meta.get('title', '') or '').strip()
        if actual_title == EXPECTED_TITLE:
            print(f"PASS: Component 1 — title matches: '{actual_title}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected title '{EXPECTED_TITLE}', found '{actual_title}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Author metadata matches (0.25 points)
    try:
        actual_author = (meta.get('author', '') or '').strip()
        if actual_author == EXPECTED_AUTHOR:
            print(f"PASS: Component 2 — author matches: '{actual_author}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected author '{EXPECTED_AUTHOR}', found '{actual_author}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Subject metadata matches (0.25 points)
    try:
        actual_subject = (meta.get('subject', '') or '').strip()
        if actual_subject == EXPECTED_SUBJECT:
            print(f"PASS: Component 3 — subject matches: '{actual_subject}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — expected subject '{EXPECTED_SUBJECT}', found '{actual_subject}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Keywords metadata matches (0.25 points)
    try:
        actual_keywords = (meta.get('keywords', '') or '').strip()
        if actual_keywords == EXPECTED_KEYWORDS:
            print(f"PASS: Component 4 — keywords match: '{actual_keywords}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — expected keywords '{EXPECTED_KEYWORDS}', found '{actual_keywords}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point — check the output file at the canonical path
file_path = f'{WORKDIR}/papers/my_paper_metadata.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
