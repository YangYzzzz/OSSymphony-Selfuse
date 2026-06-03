"""
Reward Script: Add comma at column 15 on lines 15-20 in matrix.py
Task ID: vscode_edit_051
Domain: vs_code
Scoring:
  - Component 1 (0.60): Lines 15-18 each have comma inserted correctly (0.10 per line)
  - Component 2 (0.40): Lines 19-20 each have comma inserted correctly (0.20 per line)
  Total: 1.0 when all 6 target lines have commas correctly inserted

Context:
  The initial file has lines 15-20 missing a comma after the 3rd number in each inner list.
  e.g., '    [5, 10, 30 40, ...]' → '    [5, 10, 30, 40, ...]'
  The task requires inserting a comma at column 15 on each of these 6 lines.
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_051'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'matrix.py')

# Expected content for lines 15-20 (1-indexed) after the task is completed
# Each line should have a comma after the 3rd element in the inner list
EXPECTED_LINES = {
    15: '    [5, 10, 30, 40, 50, 60, 70, 80],',
    16: '    [5, 12, 25, 37, 48, 51, 63, 74],',
    17: '    [3, 11, 24, 36, 47, 58, 69, 72],',
    18: '    [7, 15, 29, 41, 53, 64, 76, 88],',
    19: '    [6, 14, 28, 45, 57, 68, 71, 83],',
    20: '    [4, 13, 27, 42, 56, 67, 78, 92],',
}

# Component weights per line (total = 1.0)
LINE_WEIGHTS = {
    15: 0.10,
    16: 0.10,
    17: 0.10,
    18: 0.10,
    19: 0.30,
    20: 0.30,
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that commas were inserted at column 15 on each of lines 15-20 in matrix.py.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be readable
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: file must have exactly 30 lines
    if len(lines) != 30:
        print(f"CRITICAL: Expected 30 lines, found {len(lines)}. File may be corrupted.")
        print("REWARD: 0.0")
        return 0.0

    # Component 1-6: Verify comma inserted on each of lines 15-20 (1-indexed)
    # Each line should match the expected content exactly (stripped of trailing newline)
    # Lines 15-18: 0.10 pts each (Group A — 4 lines, 0.40 pts total)
    # Lines 19-20: 0.30 pts each (Group B — 2 lines, 0.60 pts total)
    # Wait: 4*0.10 + 2*0.30 = 0.40 + 0.60 = 1.00 ✓

    for line_num in [15, 16, 17, 18, 19, 20]:
        line_idx = line_num - 1  # Convert to 0-indexed
        weight = LINE_WEIGHTS[line_num]
        expected = EXPECTED_LINES[line_num]

        try:
            actual = lines[line_idx].rstrip('\n').rstrip('\r')
            if actual == expected:
                print(f"PASS: Line {line_num} — comma correctly inserted: {repr(actual)} ({weight} pts)")
                total_score += weight
            else:
                # Check if comma is present somewhere (partial pattern check)
                has_no_missing = not bool(re.search(r'\d+ \d+', actual))
                if has_no_missing and actual.strip().startswith('['):
                    print(f"PARTIAL: Line {line_num} — comma present but content differs from expected.")
                    print(f"  Expected: {repr(expected)}")
                    print(f"  Actual:   {repr(actual)}")
                else:
                    print(f"FAIL: Line {line_num} — comma NOT inserted.")
                    print(f"  Expected: {repr(expected)}")
                    print(f"  Actual:   {repr(actual)}")
        except Exception as e:
            print(f"ERROR: Line {line_num} — could not check: {e}")

    final_score = round(min(total_score, 1.0), 6)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
