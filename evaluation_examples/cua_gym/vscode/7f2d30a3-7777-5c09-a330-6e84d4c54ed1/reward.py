"""
Reward Script: Add 'self.' before each parameter in __init__ method
Task ID: vscode_stu_034
Domain: vscode
Scoring: 5 components (0.2 each) — one per parameter line (5-9) that must have 'self.<param> = <param>'
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_034'

# The 5 parameters and their expected line content (stripped)
EXPECTED_LINES = {
    5: ('self.name = name', 'name'),
    6: ('self.age = age', 'age'),
    7: ('self.grade = grade', 'grade'),
    8: ('self.major = major', 'major'),
    9: ('self.gpa = gpa', 'gpa'),
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must have at least 9 lines
    if len(lines) < 9:
        print(f"FAIL: File has only {len(lines)} lines, expected at least 9")
        print("REWARD: 0.0")
        return 0.0

    for line_num, (expected_stripped, param_name) in EXPECTED_LINES.items():
        # Component N: self.<param> = <param> on line <line_num> (0.2 points)
        try:
            actual_line = lines[line_num - 1]  # 0-indexed
            actual_stripped = actual_line.strip()

            # Check that the line contains the self.<param> = <param> pattern
            # Allow flexible whitespace: "self.<param> = <param>" or "self.<param>=<param>"
            pattern = rf'^self\.{re.escape(param_name)}\s*=\s*{re.escape(param_name)}$'
            if re.match(pattern, actual_stripped):
                print(f"PASS: Line {line_num} — '{actual_stripped}' matches expected 'self.{param_name} = {param_name}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Line {line_num} — expected 'self.{param_name} = {param_name}', found '{actual_stripped}'")
        except Exception as e:
            print(f"ERROR: Line {line_num} check — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.py'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
