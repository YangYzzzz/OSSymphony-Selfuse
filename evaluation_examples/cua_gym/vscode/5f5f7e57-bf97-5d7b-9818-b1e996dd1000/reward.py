"""
Reward Script: Configure Python test explorer with pytest in VSCode
Task ID: vscode_we_073
Domain: vscode
Scoring:
  - Component 1: pytestEnabled is true (0.3 pts)
  - Component 2: unittestEnabled is false (0.2 pts)
  - Component 3: pytestArgs contains "tests/" (0.2 pts)
  - Component 4: pytestArgs contains "-v" (0.15 pts)
  - Component 5: pytestArgs contains "--cov=src" (0.15 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_073'
SETTINGS_PATH = os.path.join(WORKDIR, 'projects', 'api-service', '.vscode', 'settings.json')


def load_jsonc(path):
    """Load a JSON/JSONC file, stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line // comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: settings.json not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        settings = load_jsonc(SETTINGS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: python.testing.pytestEnabled is true (0.3 points)
    # This is the core requirement — enable pytest as the test framework
    try:
        pytest_enabled = settings.get("python.testing.pytestEnabled")
        if pytest_enabled is True:
            print(f"PASS: Component 1 — pytestEnabled is true (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — expected pytestEnabled=true, found: {pytest_enabled}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: python.testing.unittestEnabled is false (0.2 points)
    # Disabling unittest ensures pytest is the sole framework
    try:
        unittest_enabled = settings.get("python.testing.unittestEnabled")
        if unittest_enabled is False:
            print(f"PASS: Component 2 — unittestEnabled is false (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — expected unittestEnabled=false, found: {unittest_enabled}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Components 3-5: pytestArgs verification
    # The task requires: ["tests/", "-v", "--cov=src"]
    try:
        pytest_args = settings.get("python.testing.pytestArgs")
        if not isinstance(pytest_args, list):
            print(f"FAIL: Components 3-5 — pytestArgs is not a list, found: {type(pytest_args)}")
        else:
            # Component 3: pytestArgs contains "tests/" (0.2 points)
            # Sets the test directory
            if "tests/" in pytest_args:
                print(f"PASS: Component 3 — pytestArgs contains 'tests/' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — 'tests/' not in pytestArgs: {pytest_args}")

            # Component 4: pytestArgs contains "-v" for verbose output (0.15 points)
            if "-v" in pytest_args or "--verbose" in pytest_args:
                print(f"PASS: Component 4 — pytestArgs contains verbose flag (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — verbose flag not in pytestArgs: {pytest_args}")

            # Component 5: pytestArgs contains "--cov=src" for coverage (0.15 points)
            if "--cov=src" in pytest_args:
                print(f"PASS: Component 5 — pytestArgs contains '--cov=src' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — '--cov=src' not in pytestArgs: {pytest_args}")
    except Exception as e:
        print(f"ERROR: Components 3-5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
