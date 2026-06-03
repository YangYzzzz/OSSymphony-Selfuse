"""
Reward Script: Split long_paper.pdf into chapter PDFs
Task ID: pdf_res_018
Domain: pdf
Scoring:
  Component 1 (0.2): chapters/ directory exists with exactly 4 expected files
  Component 2 (0.2): ch1.pdf has 8 pages
  Component 3 (0.2): ch2.pdf has 12 pages
  Component 4 (0.2): ch3.pdf has 15 pages
  Component 5 (0.2): ch4.pdf has 10 pages
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_018'
CHAPTERS_DIR = os.path.join(WORKDIR, 'papers', 'chapters')

# Expected chapter files and their page counts
EXPECTED_CHAPTERS = {
    'ch1.pdf': 8,
    'ch2.pdf': 12,
    'ch3.pdf': 15,
    'ch4.pdf': 10,
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: chapters/ directory exists and contains exactly the 4 expected files (0.2 points)
    try:
        if not os.path.isdir(CHAPTERS_DIR):
            print(f"FAIL: Component 1 -- chapters/ directory does not exist at {CHAPTERS_DIR}")
            # If no directory, nothing else can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        actual_files = set(os.listdir(CHAPTERS_DIR))
        expected_files = set(EXPECTED_CHAPTERS.keys())

        if expected_files.issubset(actual_files) and len(actual_files) == len(expected_files):
            print(f"PASS: Component 1 -- chapters/ contains exactly {sorted(actual_files)} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- expected {sorted(expected_files)}, found {sorted(actual_files)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Components 2-5: Verify page counts for each chapter PDF
    import fitz

    component_num = 2
    for filename, expected_pages in EXPECTED_CHAPTERS.items():
        filepath = os.path.join(CHAPTERS_DIR, filename)
        try:
            if not os.path.isfile(filepath):
                print(f"FAIL: Component {component_num} -- {filename} does not exist")
                component_num += 1
                continue

            doc = fitz.open(filepath)
            actual_pages = len(doc)
            doc.close()

            if actual_pages == expected_pages:
                print(f"PASS: Component {component_num} -- {filename} has {actual_pages} pages (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component {component_num} -- {filename} has {actual_pages} pages, expected {expected_pages}")
        except Exception as e:
            print(f"ERROR: Component {component_num} -- {filename}: {e}")
        component_num += 1

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
