"""
Reward Script: Outdent lines 12-18 by one level in nested.py
Task ID: vscode_edit_021
Domain: vs_code
Scoring:
  - Component 1 (0.4): Lines 12-14 each have exactly 4 spaces indentation (down from 8)
  - Component 2 (0.6): Lines 15-18 each have exactly 4 spaces indentation (down from 8)
Total: 1.0

Initial state: Lines 12-18 all have 8 spaces (over-indented)
Golden state:  Lines 12-18 all have 4 spaces (correctly indented)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_021'
FILE_PATH = '/home/user/Desktop/nested.py'


def count_lines_at_indent(lines, line_range, expected_indent):
    """Count how many lines in line_range (1-indexed) have the expected indentation."""
    correct = 0
    wrong = []
    for lineno in line_range:
        line = lines[lineno - 1]  # Convert to 0-indexed
        stripped = line.rstrip('\n').rstrip('\r')
        actual_indent = len(stripped) - len(stripped.lstrip(' '))
        if actual_indent == expected_indent:
            correct += 1
        else:
            wrong.append((lineno, actual_indent, stripped[:50]))
    return correct, wrong


def verify_task(file_path):
    """
    Verify that lines 12-18 have been outdented by exactly one level (4 spaces removed).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the file
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must have exactly 40 lines
    if len(lines) != 40:
        print(f"CRITICAL: Expected 40 lines, found {len(lines)}. File structure corrupted.")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Lines 12-14 have exactly 4 spaces of indentation (0.4 points)
    # These lines were at 8 spaces in initial_env; task requires reducing to 4 spaces.
    try:
        correct_1, wrong_1 = count_lines_at_indent(lines, range(12, 15), 4)
        if correct_1 == 3:
            print(f"PASS: Component 1 — Lines 12-14 all have exactly 4 spaces indentation (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — {correct_1}/3 lines at correct indentation; wrong: {wrong_1}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Lines 15-18 have exactly 4 spaces of indentation (0.6 points)
    # These lines were at 8 spaces in initial_env; task requires reducing to 4 spaces.
    try:
        correct_2, wrong_2 = count_lines_at_indent(lines, range(15, 19), 4)
        if correct_2 == 4:
            print(f"PASS: Component 2 — Lines 15-18 all have exactly 4 spaces indentation (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 2 — {correct_2}/4 lines at correct indentation; wrong: {wrong_2}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
