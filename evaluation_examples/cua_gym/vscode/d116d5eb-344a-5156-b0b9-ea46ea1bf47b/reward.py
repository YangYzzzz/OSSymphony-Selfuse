"""
Reward Script: Convert %-style string formatting to f-string style in legacy_code.py
Task ID: vscode_py_093
Domain: vscode
Scoring:
  Component 1 (0.4): No %-style formatting patterns remain in the file
  Component 2 (0.3): f-strings are present (at least 10 f-string lines)
  Component 3 (0.3): All 15 original %-style lines have been converted (f-string count >= 15)
  Precondition gate: File must be valid Python (no syntax errors)
"""

import os
import re
import ast

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_093'
FILE_NAME = 'legacy_code.py'


def count_pct_style_lines(content):
    """Count lines that use %-style string formatting: '...' % (...)"""
    count = 0
    lines = content.split('\n')
    for line in lines:
        stripped = line.strip()
        # Match patterns like: "text %s text" % (val) or 'text %d' % val
        if re.search(r'["\'][^"\']*%[sdrfx][^"\']*["\']\s*%\s', stripped):
            count += 1
        elif re.search(r'%\d*\.?\d*[sdrfx][^"\']*["\']\s*%\s*\(', stripped):
            count += 1
    return count


def count_fstring_lines(content):
    """Count lines that contain f-string literals."""
    count = 0
    for line in content.split('\n'):
        stripped = line.strip()
        if re.search(r'\bf["\']', stripped):
            count += 1
    return count


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: File must still be valid Python
    # This is NOT scored because it passes on both initial and golden
    try:
        ast.parse(content)
        print("PRECONDITION: File compiles as valid Python — OK")
    except SyntaxError as se:
        print(f"PRECONDITION FAIL: Syntax error at line {se.lineno}: {se.msg}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: No %-style formatting patterns remain (0.4 points)
    # This is the core task requirement — all %-style must be gone
    try:
        pct_count = count_pct_style_lines(content)
        if pct_count == 0:
            print(f"PASS: Component 1 — No %-style formatting lines found (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Found {pct_count} %-style formatting lines (expected 0)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: f-strings are present — at least 10 f-string lines (0.3 points)
    # The golden file should have ~15 f-strings replacing the original %-style lines
    try:
        fstr_count = count_fstring_lines(content)
        if fstr_count >= 10:
            print(f"PASS: Component 2 — Found {fstr_count} f-string lines (>= 10) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Found {fstr_count} f-string lines (expected >= 10)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 15 original lines converted — f-string count >= 15 (0.3 points)
    # This checks for completeness of the conversion
    try:
        fstr_count = count_fstring_lines(content)
        if fstr_count >= 15:
            print(f"PASS: Component 3 — Found {fstr_count} f-string lines (>= 15, all converted) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Found {fstr_count} f-string lines (expected >= 15 for full conversion)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{FILE_NAME}'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
