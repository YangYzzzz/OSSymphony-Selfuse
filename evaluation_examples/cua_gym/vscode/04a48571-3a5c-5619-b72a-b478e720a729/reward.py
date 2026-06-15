"""
Reward Script: Python testing setup in ~/project
Task ID: vscode_wf_017
Domain: vscode
Scoring:
  Component 1 (0.2): pytest is installed
  Component 2 (0.2): tests/test_calculator.py exists with proper structure
  Component 3 (0.3): test_calculator.py contains test functions for add and subtract
  Component 4 (0.3): VSCode settings.json has pytest configuration
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_017'

PROJECT_DIR = os.path.join(WORKDIR, 'project')
TEST_FILE = os.path.join(PROJECT_DIR, 'tests', 'test_calculator.py')
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: pytest is installed (0.2 points)
    # In initial_env, pytest is NOT installed. In golden_env, it is.
    try:
        import importlib
        import importlib.util
        spec = importlib.util.find_spec('pytest')
        if spec is not None:
            print(f"PASS: Component 1 — pytest is installed (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — pytest is not installed")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: tests/test_calculator.py exists (0.2 points)
    # In initial_env, no tests/ directory exists. In golden_env, it does.
    try:
        if os.path.isfile(TEST_FILE):
            print(f"PASS: Component 2 — {TEST_FILE} exists (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — {TEST_FILE} does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: test_calculator.py contains test functions for both add and subtract (0.3 points)
    # In initial_env, the file doesn't exist so this fails. In golden_env, it has test functions.
    try:
        if os.path.isfile(TEST_FILE):
            with open(TEST_FILE, 'r') as f:
                content = f.read()

            # Check for test functions/methods for add and subtract
            has_add_test = bool(re.search(r'def\s+test_\w*add\w*\s*\(', content))
            has_subtract_test = bool(re.search(r'def\s+test_\w*subtract\w*\s*\(', content))

            # Also check that the tests actually import and use the functions
            imports_functions = ('from calculator import' in content or
                                'import calculator' in content)

            if has_add_test and has_subtract_test and imports_functions:
                print(f"PASS: Component 3 — test_calculator.py has tests for add and subtract with proper imports (0.3 pts)")
                total_score += 0.3
            elif has_add_test and has_subtract_test:
                # Has test functions but no import — partial credit
                print(f"PARTIAL: Component 3 — test functions found but no calculator import (0.15 pts)")
                total_score += 0.15
            else:
                missing = []
                if not has_add_test:
                    missing.append('add')
                if not has_subtract_test:
                    missing.append('subtract')
                print(f"FAIL: Component 3 — missing test functions for: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 3 — test file does not exist, cannot check test functions")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: VSCode settings.json has pytest configuration (0.3 points)
    # In initial_env, settings.json does NOT have pytest keys. In golden_env, it does.
    try:
        if os.path.isfile(SETTINGS_PATH):
            with open(SETTINGS_PATH, 'r') as f:
                raw = f.read()
            # Handle JSONC (strip comments)
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            settings = json.loads(cleaned)

            pytest_enabled = settings.get('python.testing.pytestEnabled')
            pytest_args = settings.get('python.testing.pytestArgs')

            sub_score = 0.0

            if pytest_enabled is True:
                sub_score += 0.15
                print(f"  PASS: pytestEnabled is true")
            else:
                print(f"  FAIL: pytestEnabled expected true, found: {pytest_enabled}")

            if isinstance(pytest_args, list) and 'tests' in pytest_args:
                sub_score += 0.15
                print(f"  PASS: pytestArgs contains 'tests'")
            else:
                print(f"  FAIL: pytestArgs expected ['tests'], found: {pytest_args}")

            if sub_score > 0:
                print(f"PASS: Component 4 — VSCode pytest settings ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 4 — no pytest settings found")
        else:
            print(f"FAIL: Component 4 — settings.json not found at {SETTINGS_PATH}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
