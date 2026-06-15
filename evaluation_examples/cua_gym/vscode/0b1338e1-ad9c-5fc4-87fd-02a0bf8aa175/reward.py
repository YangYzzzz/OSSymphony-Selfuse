"""
Reward Script: Copy function from lines 3-8 and paste at line 20
Task ID: vscode_stu_011
Domain: vscode
Scoring:
  Component 1 (0.5): Function from lines 3-8 is duplicated near line 20
  Component 2 (0.3): File length increased by ~6 lines (confirming copy, not move)
  Component 3 (0.2): Original lines 3-8 intact AND duplicated function present
                      (compound check: both conditions must hold)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_011'

# The function that should be on lines 3-8 in the initial file
EXPECTED_FUNC_LINES = [
    'def calculate_tax(income, rate=0.25):',
    '    """Calculate tax amount based on income and rate."""',
    '    if income < 0:',
    '        raise ValueError("Income cannot be negative")',
    '    tax = income * rate',
    '    return round(tax, 2)',
]


def normalize(s):
    """Strip trailing whitespace for comparison."""
    return s.rstrip()


def find_func_after_line(stripped_lines, start_line_1indexed):
    """Find the expected function block starting at or after the given 1-indexed line.
    Returns the 1-indexed line number where found, or None."""
    start_idx = start_line_1indexed - 1  # convert to 0-indexed
    for idx in range(start_idx, len(stripped_lines)):
        if idx + len(EXPECTED_FUNC_LINES) > len(stripped_lines):
            break
        match = all(
            normalize(stripped_lines[idx + j]) == normalize(EXPECTED_FUNC_LINES[j])
            for j in range(len(EXPECTED_FUNC_LINES))
        )
        if match:
            return idx + 1  # return 1-indexed
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        stripped_lines = [line.rstrip('\n') for line in lines]
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check if original function is at lines 3-8 (precondition gate)
    original_intact = False
    if len(stripped_lines) >= 8:
        original_intact = all(
            normalize(stripped_lines[2 + j]) == normalize(EXPECTED_FUNC_LINES[j])
            for j in range(len(EXPECTED_FUNC_LINES))
        )

    # Find if the function appears a SECOND time (after line 9)
    # This is the key task-introduced change
    second_occurrence = find_func_after_line(stripped_lines, 9)

    # Component 1: Function is duplicated somewhere after line 9 (0.5 points)
    # This FAILS on initial (no duplication) and PASSES on golden
    try:
        if second_occurrence is not None:
            print(f"PASS: Component 1 — Function duplicated at line {second_occurrence} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — No second occurrence of function found after line 9")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: File length increased (0.3 points)
    # Initial file has 48 lines. After duplication should have ~54.
    # This FAILS on initial (48 lines) and PASSES on golden
    try:
        initial_line_count = 48
        expected_min = initial_line_count + 4
        actual_count = len(stripped_lines)
        if actual_count >= expected_min:
            print(f"PASS: Component 2 — File has {actual_count} lines (>= {expected_min}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — File has {actual_count} lines, expected >= {expected_min}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Original preserved AND duplicate exists (compound check) (0.2 points)
    # Both conditions must be true together. On initial, duplicate doesn't exist, so this fails.
    try:
        if original_intact and second_occurrence is not None:
            print(f"PASS: Component 3 — Original at lines 3-8 intact AND duplicate present (0.2 pts)")
            total_score += 0.2
        else:
            if not original_intact:
                print(f"FAIL: Component 3 — Original function at lines 3-8 is not intact")
            if second_occurrence is None:
                print(f"FAIL: Component 3 — No duplicate found (compound condition fails)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.py'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
