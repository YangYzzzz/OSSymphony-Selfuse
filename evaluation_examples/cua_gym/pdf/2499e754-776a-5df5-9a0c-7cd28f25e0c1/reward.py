"""
Reward Script: Split combined pleadings PDF into individual documents
Task ID: pdf_legal_070
Domain: pdf
Scoring:
  Component 1 (0.10 each, 0.40 total): Each of the 4 split files exists
  Component 2 (0.10 each, 0.40 total): Each split file has the correct page count
  Component 3 (0.05 each, 0.20 total): Content of first page of each split matches source pages
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_070'

# Expected split files: (filename, expected_page_count, source_start_page_0indexed)
EXPECTED_FILES = [
    ('complaint.pdf', 12, 0),    # pages 1-12
    ('answer.pdf', 8, 12),       # pages 13-20
    ('counterclaim.pdf', 5, 20), # pages 21-25
    ('reply.pdf', 7, 25),       # pages 26-32
]

SOURCE_PATH = os.path.join(WORKDIR, 'legal', 'pleadings_all.pdf')
SPLIT_DIR = os.path.join(WORKDIR, 'legal', 'pleadings')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: source file must exist (gate, not scored)
    if not os.path.exists(SOURCE_PATH):
        print(f"CRITICAL: Source file not found: {SOURCE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Load source document for content comparison
    try:
        import fitz
        source_doc = fitz.open(SOURCE_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot load source PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    for fname, expected_pages, src_start_idx in EXPECTED_FILES:
        fpath = os.path.join(SPLIT_DIR, fname)

        # Component A: File exists (0.10 points per file)
        try:
            if os.path.isfile(fpath):
                print(f"PASS: {fname} exists (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: {fname} does not exist at {fpath}")
                # Skip page count and content checks if file missing
                continue
        except Exception as e:
            print(f"ERROR: Checking existence of {fname}: {e}")
            continue

        # Component B: Correct page count (0.10 points per file)
        try:
            doc = fitz.open(fpath)
            actual_pages = len(doc)
            if actual_pages == expected_pages:
                print(f"PASS: {fname} has {actual_pages} pages (expected {expected_pages}) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: {fname} has {actual_pages} pages, expected {expected_pages}")
                doc.close()
                continue
        except Exception as e:
            print(f"ERROR: Reading {fname}: {e}")
            continue

        # Component C: Content matches source (0.05 points per file)
        try:
            split_first_text = doc[0].get_text()[:200].strip()
            source_first_text = source_doc[src_start_idx].get_text()[:200].strip()
            if split_first_text and split_first_text == source_first_text:
                print(f"PASS: {fname} first page content matches source page {src_start_idx + 1} (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: {fname} first page content does not match source page {src_start_idx + 1}")
            doc.close()
        except Exception as e:
            print(f"ERROR: Content comparison for {fname}: {e}")
            try:
                doc.close()
            except:
                pass

    source_doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
