"""
Reward Script: Update PDF metadata Subject and Keywords fields
Task ID: pdf_mbc_008
Domain: pdf
Scoring:
  Component 1 (0.4): Subject field matches expected value
  Component 2 (0.4): Keywords field matches expected value
  Component 3 (0.2): Both fields correct AND Author unchanged (integrity)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_008'

EXPECTED_SUBJECT = 'Quantum Computing Applications in Cryptography'
EXPECTED_KEYWORDS = 'quantum, cryptography, post-quantum, lattice-based'
EXPECTED_AUTHOR = 'Prof. Alan Rivera'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
        meta = doc.metadata
        doc.close()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    actual_subject = (meta.get('subject') or '').strip()
    actual_keywords = (meta.get('keywords') or '').strip()
    actual_author = (meta.get('author') or '').strip()

    # Component 1: Subject field is set to expected value (0.4 points)
    # Initial env has Subject='', golden should have the correct subject.
    try:
        if actual_subject.lower() == EXPECTED_SUBJECT.lower():
            print(f"PASS: Component 1 -- Subject matches: '{actual_subject}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- Expected subject '{EXPECTED_SUBJECT}', found '{actual_subject}'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Keywords field is set to expected value (0.4 points)
    # Initial env has Keywords='', golden should have the correct keywords.
    try:
        if actual_keywords.lower() == EXPECTED_KEYWORDS.lower():
            print(f"PASS: Component 2 -- Keywords match: '{actual_keywords}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 -- Expected keywords '{EXPECTED_KEYWORDS}', found '{actual_keywords}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Both Subject and Keywords correct AND Author unchanged (0.2 points)
    # This compound check awards points only when the task changes are present
    # AND the existing Author metadata was not accidentally modified.
    try:
        subject_ok = actual_subject.lower() == EXPECTED_SUBJECT.lower()
        keywords_ok = actual_keywords.lower() == EXPECTED_KEYWORDS.lower()
        author_ok = actual_author == EXPECTED_AUTHOR

        if subject_ok and keywords_ok and author_ok:
            print(f"PASS: Component 3 -- Both fields correct and Author unchanged: '{actual_author}' (0.2 pts)")
            total_score += 0.2
        else:
            reasons = []
            if not subject_ok:
                reasons.append("subject mismatch")
            if not keywords_ok:
                reasons.append("keywords mismatch")
            if not author_ok:
                reasons.append(f"author changed from '{EXPECTED_AUTHOR}' to '{actual_author}'")
            print(f"FAIL: Component 3 -- {', '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Research/paper_v2.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
