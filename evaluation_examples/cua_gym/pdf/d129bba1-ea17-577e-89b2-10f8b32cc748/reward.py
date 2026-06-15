"""
Reward Script: Batch process PDFs - set Author to 'Anonymous' and remove Title
Task ID: pdf_mbc_035
Domain: pdf
Scoring:
  Component 1 (0.3): submissions_anon/ directory exists with 8 correctly-named PDFs
  Component 2 (0.4): All 8 PDFs have Author == 'Anonymous'
  Component 3 (0.3): All 8 PDFs have Title removed (empty string or None)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_035'

EXPECTED_FILES = [f'paper{i}.pdf' for i in range(1, 9)]
ANON_DIR = os.path.join(WORKDIR, 'Documents', 'submissions_anon')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: submissions_anon/ directory exists with 8 correctly-named PDF files (0.3 points)
    try:
        if not os.path.isdir(ANON_DIR):
            print(f"FAIL: Component 1 — directory {ANON_DIR} does not exist")
        else:
            actual_files = sorted([f for f in os.listdir(ANON_DIR) if f.endswith('.pdf')])
            expected_sorted = sorted(EXPECTED_FILES)
            if actual_files == expected_sorted:
                print(f"PASS: Component 1 — {ANON_DIR} exists with all 8 expected PDFs (0.3 pts)")
                total_score += 0.3
            else:
                missing = set(expected_sorted) - set(actual_files)
                extra = set(actual_files) - set(expected_sorted)
                print(f"FAIL: Component 1 — file mismatch. Missing: {missing}, Extra: {extra}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If directory doesn't exist or is empty, no point checking metadata
    if total_score < 0.3:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: All 8 PDFs have Author set to 'Anonymous' (0.4 points)
    # Award partial credit: 0.05 per file
    try:
        author_pass_count = 0
        for fname in EXPECTED_FILES:
            fpath = os.path.join(ANON_DIR, fname)
            try:
                doc = pymupdf.open(fpath)
                meta = doc.metadata
                doc.close()
                author_val = meta.get('author', '')
                if author_val is None:
                    author_val = ''
                if author_val.strip() == 'Anonymous':
                    author_pass_count += 1
                else:
                    print(f"FAIL: Component 2 — {fname} has author={repr(author_val)}, expected 'Anonymous'")
            except Exception as e:
                print(f"ERROR: Component 2 — could not read {fname}: {e}")

        author_score = (author_pass_count / 8.0) * 0.4
        if author_pass_count == 8:
            print(f"PASS: Component 2 — all 8 PDFs have Author='Anonymous' (0.4 pts)")
        else:
            print(f"PARTIAL: Component 2 — {author_pass_count}/8 PDFs have correct Author ({author_score:.2f} pts)")
        total_score += author_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 8 PDFs have Title removed/empty (0.3 points)
    # Award partial credit: 0.0375 per file
    try:
        title_pass_count = 0
        for fname in EXPECTED_FILES:
            fpath = os.path.join(ANON_DIR, fname)
            try:
                doc = pymupdf.open(fpath)
                meta = doc.metadata
                doc.close()
                title_val = meta.get('title', '')
                if title_val is None:
                    title_val = ''
                if title_val.strip() == '':
                    title_pass_count += 1
                else:
                    print(f"FAIL: Component 3 — {fname} has title={repr(title_val)}, expected empty")
            except Exception as e:
                print(f"ERROR: Component 3 — could not read {fname}: {e}")

        title_score = (title_pass_count / 8.0) * 0.3
        if title_pass_count == 8:
            print(f"PASS: Component 3 — all 8 PDFs have Title removed (0.3 pts)")
        else:
            print(f"PARTIAL: Component 3 — {title_pass_count}/8 PDFs have Title removed ({title_score:.2f} pts)")
        total_score += title_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
