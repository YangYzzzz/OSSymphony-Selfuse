"""
Reward Script: Fix Pong game score reset bug
Task ID: osworld_multi_apps_code_python_game_007
Domain: os (Python code file)
Scoring:
  Component 1 (0.5): score_left and score_right are both defined OUTSIDE the while running: loop
  Component 2 (0.3): Neither score_left = 0 nor score_right = 0 appears inside the while loop body
  Component 3 (0.2): The '# BUG:' comment is removed (clean fix without leftover bug marker)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_python_game_007'
GAME_FILE = '/home/user/projects/pong/game.py'


def verify_task(file_path):
    """
    Verify that the Pong game score reset bug has been fixed.
    The fix is: move score_left = 0 and score_right = 0 from INSIDE the
    while running: loop to OUTSIDE (before) it.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    lines = content.split('\n')

    # Parse the structure: find the while loop line index and what is inside it
    # We need to determine:
    #   1. Where "while running:" starts
    #   2. Where score_left/score_right assignments appear relative to the loop

    while_loop_line_idx = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('while running:') or stripped == 'while running:':
            while_loop_line_idx = i
            break

    if while_loop_line_idx is None:
        print("FAIL: Could not locate 'while running:' loop in file.")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: 'while running:' loop found at line {while_loop_line_idx + 1}")

    # Determine the indentation level of the loop body (lines after "while running:")
    # The loop body lines start after the while line and have deeper indentation
    # Lines before while_loop_line_idx are "outside the loop"
    # Lines after while_loop_line_idx (with indentation > while line's indent) are "inside the loop"

    # Get indentation of the while line itself
    while_line = lines[while_loop_line_idx]
    while_indent = len(while_line) - len(while_line.lstrip())
    # Body indent should be greater than while_indent (typically while_indent + 4)

    # Collect line indices of score_left and score_right assignments
    score_left_indices = []
    score_right_indices = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'score_left\s*=\s*0\s*$', stripped):
            score_left_indices.append(i)
        if re.match(r'score_right\s*=\s*0\s*$', stripped):
            score_right_indices.append(i)

    print(f"INFO: score_left = 0 found at lines: {[x+1 for x in score_left_indices]}")
    print(f"INFO: score_right = 0 found at lines: {[x+1 for x in score_right_indices]}")

    # Helper: determine if a line index is inside the while loop body
    def is_inside_while_loop(line_idx):
        """
        A line is inside the while loop if:
        - Its index > while_loop_line_idx
        - Its indentation is greater than while_indent (meaning it's inside the block)
        - We stop checking once indentation returns to <= while_indent (loop ends)
        """
        if line_idx <= while_loop_line_idx:
            return False
        line = lines[line_idx]
        if line.strip() == '':
            # blank line, look at surrounding context
            return True  # conservative: treat blank lines inside as inside
        line_indent = len(line) - len(line.lstrip())
        return line_indent > while_indent

    # -------------------------------------------------------------------------
    # Component 1: score_left and score_right are defined OUTSIDE the while loop
    # (0.5 points) — This is the core fix
    # -------------------------------------------------------------------------
    try:
        # Check that there is at least one score_left = 0 assignment BEFORE the while loop
        score_left_outside = any(idx < while_loop_line_idx for idx in score_left_indices)
        # Check that there is at least one score_right = 0 assignment BEFORE the while loop
        score_right_outside = any(idx < while_loop_line_idx for idx in score_right_indices)

        if score_left_outside and score_right_outside:
            print(f"PASS: Component 1 — score_left and score_right both initialized OUTSIDE while loop (0.5 pts)")
            total_score += 0.5
        else:
            missing = []
            if not score_left_outside:
                missing.append("score_left")
            if not score_right_outside:
                missing.append("score_right")
            print(f"FAIL: Component 1 — {', '.join(missing)} not initialized outside while loop")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Neither score_left nor score_right is re-initialized INSIDE the loop
    # (0.3 points) — Ensures the buggy code is actually removed, not just duplicated
    # -------------------------------------------------------------------------
    try:
        # Check that NO score_left = 0 assignment appears inside the while loop
        score_left_inside = any(is_inside_while_loop(idx) for idx in score_left_indices)
        # Check that NO score_right = 0 assignment appears inside the while loop
        score_right_inside = any(is_inside_while_loop(idx) for idx in score_right_indices)

        if not score_left_inside and not score_right_inside:
            print(f"PASS: Component 2 — No score variables re-initialized inside while loop (0.3 pts)")
            total_score += 0.3
        else:
            still_inside = []
            if score_left_inside:
                still_inside.append("score_left")
            if score_right_inside:
                still_inside.append("score_right")
            print(f"FAIL: Component 2 — {', '.join(still_inside)} still initialized inside while loop")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: The '# BUG:' comment marker is removed from the file
    # (0.2 points) — Confirms the buggy section was cleaned up
    # -------------------------------------------------------------------------
    try:
        bug_comment_present = '# BUG:' in content
        if not bug_comment_present:
            print(f"PASS: Component 3 — '# BUG:' comment removed; fix is clean (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — '# BUG:' comment still present; bug marker not cleaned up")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against the canonical game file path on the VM
if not os.path.exists(GAME_FILE):
    print(f"File not found: {GAME_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(GAME_FILE)
