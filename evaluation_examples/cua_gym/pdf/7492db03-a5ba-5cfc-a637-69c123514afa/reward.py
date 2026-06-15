"""
Reward Script: Verify hierarchical bookmark structure in textbook.pdf
Task ID: pdf_fm_035
Domain: pdf
Scoring:
  Component 1 (0.2): TOC has exactly 6 entries
  Component 2 (0.3): Two top-level entries with correct titles and page numbers
  Component 3 (0.25): Part I children (Chapter 1 pg3, Chapter 2 pg25)
  Component 4 (0.25): Part II children (Chapter 3 pg52, Chapter 4 pg78)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_035'

# Expected TOC structure: [[level, title, page], ...]
EXPECTED_TOC = [
    [1, 'Part I: Foundations', 1],
    [2, 'Chapter 1', 3],
    [2, 'Chapter 2', 25],
    [1, 'Part II: Advanced Topics', 50],
    [2, 'Chapter 3', 52],
    [2, 'Chapter 4', 78],
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    toc = doc.get_toc()
    doc.close()

    print(f"INFO: Found {len(toc)} TOC entries: {toc}")

    # Component 1: TOC has exactly 6 entries (0.2 points)
    try:
        if len(toc) == 6:
            print(f"PASS: Component 1 — TOC has exactly 6 entries (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected 6 TOC entries, found {len(toc)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Two top-level entries with correct titles and page numbers (0.3 points)
    try:
        top_level = [entry for entry in toc if entry[0] == 1]
        part1_count = sum(1 for e in top_level if e[1].strip() == 'Part I: Foundations' and e[2] == 1)
        part2_count = sum(1 for e in top_level if e[1].strip() == 'Part II: Advanced Topics' and e[2] == 50)

        if part1_count == 1 and part2_count == 1 and len(top_level) == 2:
            print(f"PASS: Component 2 — Both top-level entries correct (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Top-level entries: {top_level}, part1_found={part1_count}, part2_found={part2_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Part I children — Chapter 1 (pg 3) and Chapter 2 (pg 25) (0.25 points)
    try:
        ch1_count = sum(1 for e in toc if e[0] == 2 and e[1].strip() == 'Chapter 1' and e[2] == 3)
        ch2_count = sum(1 for e in toc if e[0] == 2 and e[1].strip() == 'Chapter 2' and e[2] == 25)

        if ch1_count == 1 and ch2_count == 1:
            print(f"PASS: Component 3 — Part I children correct: Ch1 pg3, Ch2 pg25 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — ch1_found={ch1_count}, ch2_found={ch2_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Part II children — Chapter 3 (pg 52) and Chapter 4 (pg 78) (0.25 points)
    try:
        ch3_count = sum(1 for e in toc if e[0] == 2 and e[1].strip() == 'Chapter 3' and e[2] == 52)
        ch4_count = sum(1 for e in toc if e[0] == 2 and e[1].strip() == 'Chapter 4' and e[2] == 78)

        if ch3_count == 1 and ch4_count == 1:
            print(f"PASS: Component 4 — Part II children correct: Ch3 pg52, Ch4 pg78 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — ch3_found={ch3_count}, ch4_found={ch4_count}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/textbook.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
