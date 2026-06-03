"""
Reward Script: Find and Replace className="btn" with className="btn btn-primary"
Task ID: vscode_web_014
Domain: vscode
Scoring:
  Component 1 (0.5): All className="btn" occurrences removed
  Component 2 (0.3): All 12 occurrences replaced with className="btn btn-primary"
  Component 3 (0.2): Changes span all 7 expected files
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_014'
PROJECT_SRC = os.path.join(WORKDIR, 'projects', 'react-app', 'src')

# The 7 files that should be affected
EXPECTED_FILES = [
    'layouts/Header.jsx',
    'pages/HomePage.jsx',
    'pages/AboutPage.jsx',
    'components/LoginForm.jsx',
    'components/common/Modal.jsx',
    'components/ProductCard.jsx',
    'App.jsx',
]

# Expected count of className="btn btn-primary" per file (total 12)
EXPECTED_COUNTS = {
    'layouts/Header.jsx': 2,
    'pages/HomePage.jsx': 1,
    'pages/AboutPage.jsx': 1,
    'components/LoginForm.jsx': 2,
    'components/common/Modal.jsx': 2,
    'components/ProductCard.jsx': 2,
    'App.jsx': 2,
}

OLD_PATTERN = 'className="btn"'
NEW_PATTERN = 'className="btn btn-primary"'


def count_occurrences_in_file(filepath, pattern):
    """Count exact occurrences of pattern in a file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return content.count(pattern)
    except Exception:
        return -1


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gather all jsx files in src/
    all_jsx_files = []
    for root, dirs, files in os.walk(PROJECT_SRC):
        for fname in files:
            if fname.endswith('.jsx'):
                all_jsx_files.append(os.path.join(root, fname))

    if not all_jsx_files:
        print("CRITICAL: No .jsx files found in project src/")
        print("REWARD: 0.0")
        return 0.0

    # Count old pattern across all files
    total_old = 0
    for fpath in all_jsx_files:
        count = count_occurrences_in_file(fpath, OLD_PATTERN)
        if count > 0:
            total_old += count

    # Count new pattern across all files
    total_new = 0
    files_with_new = []
    for fpath in all_jsx_files:
        count = count_occurrences_in_file(fpath, NEW_PATTERN)
        if count > 0:
            total_new += count
            rel = os.path.relpath(fpath, PROJECT_SRC)
            files_with_new.append(rel)

    # Component 1: All occurrences of className="btn" are removed (0.5 points)
    # This checks the OLD pattern is completely gone
    try:
        if total_old == 0:
            print(f"PASS: Component 1 — No remaining className=\"btn\" occurrences (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Found {total_old} remaining className=\"btn\" occurrences (expected 0)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 12 occurrences replaced with className="btn btn-primary" (0.3 points)
    # Progressive: partial credit for partial replacements
    try:
        if total_new >= 12:
            print(f"PASS: Component 2 — Found {total_new} className=\"btn btn-primary\" occurrences (expected 12) (0.3 pts)")
            total_score += 0.3
        elif total_new > 0:
            partial = round(0.3 * (total_new / 12), 2)
            print(f"PARTIAL: Component 2 — Found {total_new}/12 className=\"btn btn-primary\" occurrences ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Found 0 className=\"btn btn-primary\" occurrences (expected 12)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Changes span all 7 expected files (0.2 points)
    try:
        expected_set = set(EXPECTED_FILES)
        actual_set = set(files_with_new)
        matched = expected_set.intersection(actual_set)
        if len(matched) >= 7:
            print(f"PASS: Component 3 — All 7 expected files contain replacements (0.2 pts)")
            total_score += 0.2
        elif len(matched) > 0:
            partial = round(0.2 * (len(matched) / 7), 2)
            print(f"PARTIAL: Component 3 — {len(matched)}/7 expected files contain replacements ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No expected files contain className=\"btn btn-primary\"")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(PROJECT_SRC):
    print(f"Project src directory not found: {PROJECT_SRC}")
    print("REWARD: 0.0")
else:
    verify_task()
