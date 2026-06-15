"""
Reward Script: Reorder pages of scrambled_thesis.pdf to correct sequential order
Task ID: pdf_res_054
Domain: pdf
Scoring:
  - Component 1 (0.2): Output file exists with correct page count (10 pages)
  - Component 2 (0.4): Pages 0-4 contain Chapters 1-5 in order
  - Component 3 (0.4): Pages 5-9 contain Chapters 6-10 in order
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_054'
OUTPUT_FILE = os.path.join(WORKDIR, 'thesis', 'scrambled_thesis_fixed.pdf')

# Expected chapter titles for each page position (0-indexed)
EXPECTED_CHAPTERS = [
    "Chapter 1:",
    "Chapter 2:",
    "Chapter 3:",
    "Chapter 4:",
    "Chapter 5:",
    "Chapter 6:",
    "Chapter 7:",
    "Chapter 8:",
    "Chapter 9:",
    "Chapter 10:",
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists and has 10 pages (0.2 points)
    # This is a task-introduced change: the output file does not exist in initial_env
    try:
        doc = pymupdf.open(file_path)
        page_count = doc.page_count
        if page_count == 10:
            print(f"PASS: Component 1 — Output file exists with {page_count} pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected 10 pages, found {page_count}")
            doc.close()
            final_score = min(total_score, 1.0)
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {final_score}")
            return final_score
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Pages 0-4 contain Chapters 1-5 in correct order (0.4 points)
    # Each correct page earns 0.08 points (5 pages x 0.08 = 0.4)
    try:
        comp2_score = 0.0
        for i in range(5):
            page = doc[i]
            text = page.get_text().strip()
            expected = EXPECTED_CHAPTERS[i]
            if text.startswith(expected):
                comp2_score += 0.08
                print(f"  PASS: Page {i} starts with '{expected}' as expected")
            else:
                # Extract the first line for debug output
                first_line = text.split('\n')[0] if text else "(empty)"
                print(f"  FAIL: Page {i} expected '{expected}', found '{first_line}'")
        if comp2_score > 0:
            print(f"PASS: Component 2 — Pages 0-4 chapter order ({comp2_score:.2f} pts)")
            total_score += comp2_score
        else:
            print(f"FAIL: Component 2 — No pages in 0-4 have correct chapter order")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Pages 5-9 contain Chapters 6-10 in correct order (0.4 points)
    # Each correct page earns 0.08 points (5 pages x 0.08 = 0.4)
    try:
        comp3_score = 0.0
        for i in range(5, 10):
            page = doc[i]
            text = page.get_text().strip()
            expected = EXPECTED_CHAPTERS[i]
            if text.startswith(expected):
                comp3_score += 0.08
                print(f"  PASS: Page {i} starts with '{expected}' as expected")
            else:
                first_line = text.split('\n')[0] if text else "(empty)"
                print(f"  FAIL: Page {i} expected '{expected}', found '{first_line}'")
        if comp3_score > 0:
            print(f"PASS: Component 3 — Pages 5-9 chapter order ({comp3_score:.2f} pts)")
            total_score += comp3_score
        else:
            print(f"FAIL: Component 3 — No pages in 5-9 have correct chapter order")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)
