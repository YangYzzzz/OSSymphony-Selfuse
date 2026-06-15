"""
Reward Script: Split proceedings_bundle.pdf into 5 individual papers
Task ID: pdf_res_066
Domain: pdf
Scoring:
  - Component 1 (0.10): individual/ directory exists with exactly 5 paper PDFs
  - Component 2 (0.18): paper_1.pdf has 8 pages
  - Component 3 (0.18): paper_2.pdf has 7 pages
  - Component 4 (0.18): paper_3.pdf has 7 pages
  - Component 5 (0.18): paper_4.pdf has 8 pages
  - Component 6 (0.18): paper_5.pdf has 10 pages
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_066'
INDIVIDUAL_DIR = os.path.join(WORKDIR, 'papers', 'individual')

EXPECTED_PAPERS = {
    'paper_1.pdf': 8,
    'paper_2.pdf': 7,
    'paper_3.pdf': 7,
    'paper_4.pdf': 8,
    'paper_5.pdf': 10,
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: individual/ directory exists and contains exactly 5 paper_N.pdf files (0.10 pts)
    try:
        if not os.path.isdir(INDIVIDUAL_DIR):
            print(f"FAIL: Component 1 -- directory {INDIVIDUAL_DIR} does not exist")
            # No point checking further if directory doesn't exist
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        pdf_files = [f for f in os.listdir(INDIVIDUAL_DIR) if f.startswith('paper_') and f.endswith('.pdf')]
        if len(pdf_files) == 5:
            print(f"PASS: Component 1 -- individual/ contains exactly 5 paper PDFs: {sorted(pdf_files)} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 -- expected 5 paper PDFs, found {len(pdf_files)}: {sorted(pdf_files)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Components 2-6: Each paper has the correct page count (0.18 pts each)
    component_num = 2
    for filename, expected_pages in EXPECTED_PAPERS.items():
        filepath = os.path.join(INDIVIDUAL_DIR, filename)
        try:
            if not os.path.isfile(filepath):
                print(f"FAIL: Component {component_num} -- {filename} does not exist")
                component_num += 1
                continue

            doc = fitz.open(filepath)
            actual_pages = len(doc)
            doc.close()

            if actual_pages == expected_pages:
                print(f"PASS: Component {component_num} -- {filename} has {actual_pages} pages (0.18 pts)")
                total_score += 0.18
            else:
                print(f"FAIL: Component {component_num} -- {filename} expected {expected_pages} pages, found {actual_pages}")
        except Exception as e:
            print(f"ERROR: Component {component_num} -- {filename}: {e}")
        component_num += 1

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
