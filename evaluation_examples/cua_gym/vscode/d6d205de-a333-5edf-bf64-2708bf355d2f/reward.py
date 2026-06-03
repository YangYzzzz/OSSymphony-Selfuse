"""
Reward Script: Create .prettierignore and .eslintignore files
Task ID: vscode_web_047
Domain: vscode
Scoring:
  Component 1 (0.5): .prettierignore exists with required exclusion entries
  Component 2 (0.5): .eslintignore exists with required exclusion entries
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_047'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'webapp')

# Required exclusion patterns that must appear in both ignore files
REQUIRED_PATTERNS = ['dist/', 'coverage/', 'src/generated/', 'node_modules/']


def check_ignore_file(file_path, file_label):
    """
    Check that an ignore file exists and contains all required exclusion patterns.
    Returns a score between 0.0 and 1.0 for this component.
    """
    if not os.path.exists(file_path):
        print(f"FAIL: {file_label} does not exist at {file_path}")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Could not read {file_label}: {e}")
        return 0.0

    # Parse non-empty, non-comment lines
    lines = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            lines.append(stripped)

    # Normalize lines for matching: strip leading / and trailing /
    normalized_lines = set(l.lstrip('/').rstrip('/') for l in lines)

    # Check each required pattern
    found_count = 0
    for pattern in REQUIRED_PATTERNS:
        # Accept with or without trailing slash, and with or without leading slash
        # e.g. "dist/", "dist", "/dist/", "/dist" all match "dist/"
        pattern_base = pattern.rstrip('/')
        if pattern_base in normalized_lines:
            found_count += 1
            print(f"  FOUND: '{pattern}' in {file_label}")
        else:
            print(f"  MISSING: '{pattern}' not found in {file_label}")

    if found_count == len(REQUIRED_PATTERNS):
        print(f"PASS: {file_label} contains all {len(REQUIRED_PATTERNS)} required patterns")
        return float(found_count) / float(len(REQUIRED_PATTERNS))
    elif found_count > 0:
        ratio = found_count / len(REQUIRED_PATTERNS)
        print(f"PARTIAL: {file_label} has {found_count}/{len(REQUIRED_PATTERNS)} patterns")
        return ratio
    else:
        print(f"FAIL: {file_label} has none of the required patterns")
        return 0.0


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .prettierignore exists with required entries (0.5 points)
    try:
        prettier_path = os.path.join(PROJECT_DIR, '.prettierignore')
        print("Component 1: Checking .prettierignore")
        comp1_score = check_ignore_file(prettier_path, '.prettierignore')
        points1 = 0.5 * comp1_score
        if comp1_score == 1.0:
            print(f"PASS: Component 1 -- .prettierignore complete ({points1} pts)")
            total_score += points1
        elif comp1_score > 0.0:
            print(f"PARTIAL: Component 1 -- .prettierignore ({points1} pts)")
            total_score += points1
        else:
            print(f"FAIL: Component 1 -- .prettierignore (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    print()

    # Component 2: .eslintignore exists with required entries (0.5 points)
    try:
        eslint_path = os.path.join(PROJECT_DIR, '.eslintignore')
        print("Component 2: Checking .eslintignore")
        comp2_score = check_ignore_file(eslint_path, '.eslintignore')
        points2 = 0.5 * comp2_score
        if comp2_score == 1.0:
            print(f"PASS: Component 2 -- .eslintignore complete ({points2} pts)")
            total_score += points2
        elif comp2_score > 0.0:
            print(f"PARTIAL: Component 2 -- .eslintignore ({points2} pts)")
            total_score += points2
        else:
            print(f"FAIL: Component 2 -- .eslintignore (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
