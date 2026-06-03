"""
Reward Script: Count bookmarks in encyclopedia.pdf and write count to bookmark_count.txt
Task ID: pdf_mbc_051
Domain: pdf
Scoring:
  Component 1 (0.3): bookmark_count.txt exists and is readable
  Component 2 (0.4): File contains the correct count "44"
  Component 3 (0.3): Count in file matches actual PDF bookmark count (cross-validation)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_051'

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    txt_path = os.path.join(WORKDIR, 'Documents', 'bookmark_count.txt')
    pdf_path = os.path.join(WORKDIR, 'Documents', 'encyclopedia.pdf')

    # Component 1: bookmark_count.txt exists and is readable (0.3 points)
    # This file does NOT exist in initial_env, only in golden_env
    try:
        if os.path.isfile(txt_path):
            content = open(txt_path, 'r').read().strip()
            if len(content) > 0:
                print(f"PASS: Component 1 — bookmark_count.txt exists and is non-empty (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — bookmark_count.txt exists but is empty")
        else:
            print(f"FAIL: Component 1 — bookmark_count.txt does not exist at {txt_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: File contains the correct count "44" (0.4 points)
    # The ground truth from context specifies total bookmark count is 44
    try:
        if os.path.isfile(txt_path):
            content = open(txt_path, 'r').read().strip()
            # Try to parse as integer and check exact value
            try:
                count_value = int(content)
                if count_value == 44:
                    print(f"PASS: Component 2 — bookmark_count.txt contains correct value 44 (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 2 — expected 44, found {count_value}")
            except ValueError:
                # Maybe the file has extra text; try to extract a number
                import re
                numbers = re.findall(r'\b(\d+)\b', content)
                if numbers and int(numbers[0]) == 44:
                    print(f"PASS: Component 2 — bookmark_count.txt contains 44 (with extra text) (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 2 — could not find value 44 in content: '{content}'")
        else:
            print(f"FAIL: Component 2 — bookmark_count.txt does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Cross-validate count against actual PDF bookmarks (0.3 points)
    # Ensures the count matches the real PDF TOC, not just a hardcoded value
    try:
        if os.path.isfile(txt_path) and os.path.isfile(pdf_path):
            content = open(txt_path, 'r').read().strip()
            import re
            numbers = re.findall(r'\b(\d+)\b', content)
            if numbers:
                file_count = int(numbers[0])
                import pymupdf
                doc = pymupdf.open(pdf_path)
                toc = doc.get_toc()
                actual_count = len(toc)
                doc.close()
                if file_count == actual_count:
                    print(f"PASS: Component 3 — count in file ({file_count}) matches PDF bookmark count ({actual_count}) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — file says {file_count} but PDF has {actual_count} bookmarks")
            else:
                print(f"FAIL: Component 3 — no numeric value found in bookmark_count.txt")
        else:
            if not os.path.isfile(txt_path):
                print(f"FAIL: Component 3 — bookmark_count.txt does not exist")
            elif not os.path.isfile(pdf_path):
                print(f"FAIL: Component 3 — encyclopedia.pdf does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
