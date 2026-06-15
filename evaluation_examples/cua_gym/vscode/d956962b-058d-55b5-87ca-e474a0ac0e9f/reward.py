"""
Reward Script: Fix JSON syntax error in .vscode/extensions.json
Task ID: vscode_fix_082
Domain: vscode
Scoring:
  Component 1 (0.4): File is valid JSON (parseable)
  Component 2 (0.3): recommendations array contains all 4 expected extensions
  Component 3 (0.3): No trailing comma before closing bracket in raw content
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_082'
FILE_PATH = os.path.join(WORKDIR, 'team-project', '.vscode', 'extensions.json')

EXPECTED_EXTENSIONS = [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-python.python",
    "eamodio.gitlens",
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Read raw content for pattern checks
    try:
        with open(file_path, 'r') as f:
            raw_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File is valid JSON (0.4 points)
    # This is the core task requirement — fixing the syntax error
    parsed_data = None
    try:
        parsed_data = json.loads(raw_content)
        print(f"PASS: Component 1 — File is valid JSON (0.4 pts)")
        total_score += 0.4
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 — File is not valid JSON: {e}")

    # Component 2: recommendations array contains all 4 expected extensions (0.3 points)
    # Only score if JSON is valid; verifies data integrity was preserved during fix
    try:
        if parsed_data is not None:
            recs = parsed_data.get("recommendations", [])
            if isinstance(recs, list) and set(recs) == set(EXPECTED_EXTENSIONS) and len(recs) == len(EXPECTED_EXTENSIONS):
                print(f"PASS: Component 2 — All 4 expected extensions present in recommendations (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Expected {EXPECTED_EXTENSIONS}, found {recs}")
        else:
            print(f"FAIL: Component 2 — Cannot check recommendations (JSON invalid)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No trailing comma before closing bracket (0.3 points)
    # Checks that the specific syntax error (trailing comma) was removed
    try:
        # Look for pattern: comma followed by optional whitespace then ]
        trailing_comma_pattern = re.search(r',\s*\]', raw_content)
        if trailing_comma_pattern is None:
            print(f"PASS: Component 3 — No trailing comma before ] in file (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Trailing comma found before ]: '{trailing_comma_pattern.group()}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
