"""
Reward Script: Batch Bates numbering of PDFs
Task ID: pdf_fin_053
Domain: pdf
Scoring:
  Component 1 (0.2): bates/ directory exists with all 6 expected files
  Component 2 (0.2): Page counts match original source files
  Component 3 (0.6): Correct sequential Bates numbers (DISC-000001..DISC-000023) on every page
"""

import os
import re
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_053'

# Expected files in alphabetical order with their page counts
EXPECTED_FILES = {
    'alpha.pdf': 3,
    'beta.pdf': 5,
    'delta.pdf': 4,
    'epsilon.pdf': 6,
    'gamma.pdf': 2,
    'zeta.pdf': 3,
}

BATES_DIR = os.path.join(WORKDIR, 'finance', 'discovery', 'bates')


def verify_task():
    """
    Verify Bates numbering task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: bates/ directory exists with all 6 expected files (0.2 points)
    try:
        if not os.path.isdir(BATES_DIR):
            print(f"FAIL: Component 1 — bates/ directory does not exist at {BATES_DIR}")
            print("REWARD: 0.0")
            return 0.0

        actual_files = sorted([f for f in os.listdir(BATES_DIR) if f.endswith('.pdf')])
        expected_names = sorted(EXPECTED_FILES.keys())

        if actual_files == expected_names:
            print(f"PASS: Component 1 — All 6 expected files present in bates/ (0.2 pts)")
            total_score += 0.2
        else:
            missing = set(expected_names) - set(actual_files)
            extra = set(actual_files) - set(expected_names)
            print(f"FAIL: Component 1 — Files mismatch. Missing: {missing}, Extra: {extra}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page counts match original source files (0.2 points)
    try:
        page_count_correct = 0
        total_files = len(EXPECTED_FILES)

        for fname, expected_pages in EXPECTED_FILES.items():
            fpath = os.path.join(BATES_DIR, fname)
            if not os.path.exists(fpath):
                print(f"FAIL: Component 2 — {fname} not found, cannot check page count")
                continue
            doc = fitz.open(fpath)
            actual_pages = len(doc)
            doc.close()
            if actual_pages == expected_pages:
                page_count_correct += 1
            else:
                print(f"FAIL: Component 2 — {fname}: expected {expected_pages} pages, got {actual_pages}")

        if page_count_correct == total_files:
            print(f"PASS: Component 2 — All 6 files have correct page counts (0.2 pts)")
            total_score += 0.2
        else:
            # Partial credit within this component
            partial = 0.2 * (page_count_correct / total_files)
            print(f"PARTIAL: Component 2 — {page_count_correct}/{total_files} files have correct page counts ({partial:.2f} pts)")
            total_score += partial
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct sequential Bates numbers on every page (0.6 points)
    # Files processed alphabetically: alpha, beta, delta, epsilon, gamma, zeta
    # Continuous numbering DISC-000001 through DISC-000023
    try:
        bates_counter = 1
        total_pages = 23  # sum of all page counts
        correct_pages = 0
        sorted_files = sorted(EXPECTED_FILES.keys())

        for fname in sorted_files:
            expected_pages = EXPECTED_FILES[fname]
            fpath = os.path.join(BATES_DIR, fname)
            if not os.path.exists(fpath):
                bates_counter += expected_pages
                continue

            doc = fitz.open(fpath)
            for page_idx in range(min(len(doc), expected_pages)):
                page = doc[page_idx]
                text = page.get_text()
                expected_bates = f"DISC-{bates_counter:06d}"

                # Check if the expected Bates number appears on this page
                if expected_bates in text:
                    correct_pages += 1
                else:
                    # Also search for it in case of minor formatting differences
                    found = re.findall(r'DISC-\d{6}', text)
                    if found and expected_bates in found:
                        correct_pages += 1
                    else:
                        print(f"FAIL: Component 3 — {fname} page {page_idx}: expected {expected_bates}, found {found}")

                bates_counter += 1
            doc.close()

        if correct_pages == total_pages:
            print(f"PASS: Component 3 — All 23 pages have correct sequential Bates numbers (0.6 pts)")
            total_score += 0.6
        elif correct_pages > 0:
            partial = 0.6 * (correct_pages / total_pages)
            print(f"PARTIAL: Component 3 — {correct_pages}/{total_pages} pages have correct Bates numbers ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages have correct Bates numbers")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
