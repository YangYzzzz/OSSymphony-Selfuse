"""
Reward Script: Batch update PDF author metadata to 'Redacted'
Task ID: pdf_mbc_012
Domain: pdf
Scoring: 5 PDF files x 0.2 pts each = 1.0. Per file: 0.12 for author=='Redacted', 0.08 for author=='Redacted' AND title preserved.
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_012'
BATCH_DIR = os.path.join(WORKDIR, 'Documents', 'batch_pdfs')

# Expected titles per file (ground truth from initial state)
EXPECTED_TITLES = {
    'file1.pdf': 'Q1 2025 Marketing Strategy',
    'file2.pdf': 'Employee Onboarding Handbook',
    'file3.pdf': 'Project Phoenix - Technical Specification',
    'file4.pdf': 'Annual Financial Review 2024',
    'file5.pdf': 'Sustainability Report - Environmental Impact',
}

EXPECTED_FILES = ['file1.pdf', 'file2.pdf', 'file3.pdf', 'file4.pdf', 'file5.pdf']


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: batch_pdfs directory exists
    if not os.path.isdir(BATCH_DIR):
        print(f"CRITICAL: Directory not found: {BATCH_DIR}")
        print("REWARD: 0.0")
        return 0.0

    for fname in EXPECTED_FILES:
        fpath = os.path.join(BATCH_DIR, fname)

        # Component A: Author field == 'Redacted' (0.12 pts per file)
        try:
            doc = pymupdf.open(fpath)
            meta = doc.metadata
            author = meta.get('author', '') or ''
            title = meta.get('title', '') or ''
            doc.close()

            if author.strip() == 'Redacted':
                print(f"PASS: {fname} author is 'Redacted' (+0.12)")
                total_score += 0.12

                # Component B: Title preserved AND author is Redacted (0.08 pts per file)
                expected_title = EXPECTED_TITLES.get(fname, '')
                if title.strip() == expected_title.strip():
                    print(f"PASS: {fname} title preserved: '{title}' (+0.08)")
                    total_score += 0.08
                else:
                    print(f"FAIL: {fname} title changed: expected '{expected_title}', found '{title}'")
            else:
                print(f"FAIL: {fname} author is '{author}', expected 'Redacted'")
        except Exception as e:
            print(f"ERROR: {fname} - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
