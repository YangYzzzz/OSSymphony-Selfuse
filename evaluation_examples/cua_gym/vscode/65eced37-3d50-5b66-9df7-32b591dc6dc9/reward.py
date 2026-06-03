"""
Reward Script: Create src/analyzer.py with Python code in data-project
Task ID: vscode_file_057
Domain: vs_code
Scoring:
  Component 1: File src/analyzer.py exists (0.5 pts)
  Component 2: File contains a Python function or class definition (0.3 pts)
  Component 3: File has meaningful content (non-trivial code body, >5 lines) (0.2 pts)
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_057'

# Target file path expected by the task
TARGET_FILE = os.path.join(WORKDIR, 'data-project', 'src', 'analyzer.py')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File src/analyzer.py exists (0.5 points)
    # This is the primary task requirement — the file must exist at the specified path.
    try:
        if os.path.isfile(file_path):
            print(f"PASS: Component 1 — analyzer.py exists at {file_path} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — analyzer.py not found at {file_path}")
            # If the file doesn't exist, remaining components cannot be verified
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — could not check file existence: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read the file content for subsequent checks
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: File contains a Python function or class definition (0.3 points)
    # Task requirement: "type Python code into it" — specifically requires "a function or class definition"
    try:
        # Check for def or class keywords at statement level (not indented inside strings)
        has_def = bool(re.search(r'^def\s+\w+', content, re.MULTILINE))
        has_class = bool(re.search(r'^class\s+\w+', content, re.MULTILINE))
        if has_def or has_class:
            what = 'class definition' if has_class else 'function definition'
            if has_def and has_class:
                what = 'function and class definition'
            print(f"PASS: Component 2 — file contains {what} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — no 'def' or 'class' found at module level in analyzer.py")
    except Exception as e:
        print(f"ERROR: Component 2 — could not parse content: {e}")

    # Component 3: File has meaningful content — at least 5 non-blank, non-comment lines (0.2 points)
    # Ensures the agent actually typed substantive code, not an empty or trivial file.
    try:
        lines = content.splitlines()
        substantive_lines = [
            line for line in lines
            if line.strip() and not line.strip().startswith('#') and line.strip() != '"""'
        ]
        if len(substantive_lines) >= 5:
            print(f"PASS: Component 3 — file has {len(substantive_lines)} substantive lines (0.2 pts)")
            total_score += 0.2
        else:
            print(
                f"FAIL: Component 3 — only {len(substantive_lines)} substantive lines found, "
                f"expected at least 5"
            )
    except Exception as e:
        print(f"ERROR: Component 3 — could not count lines: {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(os.path.join(WORKDIR, 'data-project', 'src')):
    print(f"CRITICAL: src directory not found under {WORKDIR}/data-project/")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)
