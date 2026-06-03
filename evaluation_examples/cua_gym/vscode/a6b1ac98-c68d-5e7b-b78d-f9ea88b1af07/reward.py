"""
Reward Script: Add 'export ' before each function declaration on lines 5, 18, 31, 44
Task ID: vscode_edit_043
Domain: vs_code
Scoring:
  - Component 1: Line 5 begins with 'export function calculateTotal'    (0.25 pts)
  - Component 2: Line 18 begins with 'export function formatCurrency'   (0.25 pts)
  - Component 3: Line 31 begins with 'export function validateEmail'    (0.25 pts)
  - Component 4: Line 44 begins with 'export function generateReport'   (0.25 pts)
Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_043'
FILE_PATH = '/home/user/Desktop/modules.js'

# Expected export declarations keyed by 1-based line number
EXPECTED_EXPORTS = {
    5:  'export function calculateTotal',
    18: 'export function formatCurrency',
    31: 'export function validateEmail',
    44: 'export function generateReport',
}

# The original function declarations (without 'export ') — used to confirm
# initial state and to validate no other lines were unintentionally changed
ORIGINAL_PREFIXES = {
    5:  'function calculateTotal',
    18: 'function formatCurrency',
    31: 'function validateEmail',
    44: 'function generateReport',
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Each of the 4 function declarations must begin with 'export function'.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be readable
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: file should have at least 55 lines
    if len(lines) < 44:
        print(f"CRITICAL: File has only {len(lines)} lines, expected at least 55")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Line 5 begins with 'export function calculateTotal' (0.25 points)
    try:
        line5 = lines[4].rstrip('\n')  # 0-indexed: line 5 = index 4
        if line5.startswith('export function calculateTotal'):
            print(f"PASS: Component 1 — Line 5 starts with 'export function calculateTotal' (0.25 pts)")
            print(f"      Actual: {line5!r}")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Line 5 expected 'export function calculateTotal...', found: {line5!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Line 18 begins with 'export function formatCurrency' (0.25 points)
    try:
        line18 = lines[17].rstrip('\n')  # 0-indexed: line 18 = index 17
        if line18.startswith('export function formatCurrency'):
            print(f"PASS: Component 2 — Line 18 starts with 'export function formatCurrency' (0.25 pts)")
            print(f"      Actual: {line18!r}")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Line 18 expected 'export function formatCurrency...', found: {line18!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Line 31 begins with 'export function validateEmail' (0.25 points)
    try:
        line31 = lines[30].rstrip('\n')  # 0-indexed: line 31 = index 30
        if line31.startswith('export function validateEmail'):
            print(f"PASS: Component 3 — Line 31 starts with 'export function validateEmail' (0.25 pts)")
            print(f"      Actual: {line31!r}")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Line 31 expected 'export function validateEmail...', found: {line31!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Line 44 begins with 'export function generateReport' (0.25 points)
    try:
        line44 = lines[43].rstrip('\n')  # 0-indexed: line 44 = index 43
        if line44.startswith('export function generateReport'):
            print(f"PASS: Component 4 — Line 44 starts with 'export function generateReport' (0.25 pts)")
            print(f"      Actual: {line44!r}")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Line 44 expected 'export function generateReport...', found: {line44!r}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Integrity check (informational, not scored): verify no unexpected lines were changed
    # Check that non-target lines do not contain unexpected modifications
    try:
        non_export_lines_with_function = [
            (i + 1, lines[i].rstrip('\n'))
            for i in range(len(lines))
            if (i + 1) not in EXPECTED_EXPORTS
            and 'function ' in lines[i]
            and lines[i].lstrip().startswith('export function')
        ]
        if non_export_lines_with_function:
            print(f"INFO: Unexpected 'export function' found on non-target lines: {non_export_lines_with_function}")
        else:
            print("INFO: Integrity check passed — no unexpected 'export' modifications on non-target lines")
    except Exception as e:
        print(f"INFO: Integrity check error — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
