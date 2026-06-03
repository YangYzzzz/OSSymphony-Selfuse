"""
Reward Script: Convert console.log string concatenation to template literals
Task ID: vscode_edit_079
Domain: vs_code
Scoring:
  Component 1 (0.6): All 6 console.log statements use template literals (backtick syntax)
                      Partial credit: 0.1 per converted statement
  Component 2 (0.4): No console.log statements still use old string concatenation pattern
                      Full credit only when all 6 old patterns are gone
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user/Desktop'
TASK_ID = 'vscode_edit_079'
FILE_PATH = os.path.join(WORKDIR, 'debug.js')

# Expected template literal console.log patterns in the golden file
EXPECTED_TEMPLATE_LOGS = [
    r'console\.log\(`User login event: \$\{userId\} \(\$\{username\}\)`\)',
    r'console\.log\(`API request: \$\{method\} \$\{endpoint\}`\)',
    r'console\.log\(`DB query on table: \$\{table\}, returned \$\{rowCount\} rows`\)',
    r'console\.log\(`Cache hit for key: \$\{key\}, value: \$\{value\}`\)',
    r'console\.log\(`Error \$\{code\}: \$\{message\}`\)',
    r'console\.log\(`Session \$\{sessionId\} expires at \$\{expiresAt\}`\)',
]

# Old string concatenation patterns that should no longer appear in console.log lines
OLD_CONCAT_PATTERNS = [
    r'console\.log\("User login event: " \+',
    r'console\.log\("API request: " \+',
    r'console\.log\("DB query on table: " \+',
    r'console\.log\("Cache hit for key: " \+',
    r'console\.log\("Error " \+',
    r'console\.log\("Session " \+',
]

TOTAL_LOG_STATEMENTS = 6  # There are 6 console.log statements in the file


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
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

    print(f"File loaded: {file_path} ({len(content)} bytes)")

    # Component 1: console.log statements use template literals (0.6 points total)
    # Each of the 6 converted statements is worth 0.1 points (6 * 0.1 = 0.6)
    try:
        matched_logs = 0
        for pattern in EXPECTED_TEMPLATE_LOGS:
            if re.search(pattern, content):
                matched_logs += 1
            else:
                print(f"FAIL (C1): Template literal pattern not found: {pattern}")

        component1_score = round(matched_logs * 0.1, 4)
        if matched_logs == TOTAL_LOG_STATEMENTS:
            print(f"PASS: Component 1 — All {matched_logs}/6 console.log statements use template literals ({component1_score} pts)")
            total_score += component1_score
        elif matched_logs > 0:
            print(f"PARTIAL: Component 1 — {matched_logs}/6 console.log statements use template literals ({component1_score} pts)")
            total_score += component1_score
        else:
            print(f"FAIL: Component 1 — No console.log template literals found (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No console.log statements use old string concatenation (0.4 points)
    # Awards full 0.4 only when ALL 6 old patterns are eliminated
    # Partial credit: 0.4 * (removed / total)
    try:
        old_concat_found = 0
        for pattern in OLD_CONCAT_PATTERNS:
            if re.search(pattern, content):
                old_concat_found += 1
                print(f"FAIL (C2): Old string concatenation pattern still present: {pattern}")

        removed_count = TOTAL_LOG_STATEMENTS - old_concat_found
        component2_score = round(removed_count / TOTAL_LOG_STATEMENTS * 0.4, 4)
        if old_concat_found == 0:
            print(f"PASS: Component 2 — All old string concatenation patterns removed from console.log statements (0.4 pts)")
            total_score += component2_score
        elif removed_count > 0:
            print(f"PARTIAL: Component 2 — {removed_count}/{TOTAL_LOG_STATEMENTS} old patterns removed ({component2_score} pts)")
            total_score += component2_score
        else:
            print(f"FAIL: Component 2 — All {old_concat_found} old console.log concatenation patterns still present (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: verify the canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
