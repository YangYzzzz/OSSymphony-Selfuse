"""
Reward Script: Configure pytest in VSCode and create test files
Task ID: vscode_gf4_010
Domain: vscode
Scoring:
  Component 1 (0.4): .vscode/settings.json has correct pytest configuration
  Component 2 (0.3): tests/test_sample.py exists with at least 2 test functions
  Component 3 (0.3): pytest runs and all tests pass
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_010'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'python-tests')


def _is_subset(expected, actual):
    """Check that expected is a subset of actual (recursive for dicts/lists)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return False
        return expected == actual
    return expected == actual


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .vscode/settings.json has correct pytest configuration (0.4 points)
    settings_path = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
    try:
        if not os.path.exists(settings_path):
            print(f"FAIL: Component 1 — .vscode/settings.json does not exist")
        else:
            with open(settings_path, 'r') as f:
                content = f.read()
            # Strip potential JSONC comments
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            settings = json.loads(content_clean)

            expected = {
                "python.testing.pytestEnabled": True,
                "python.testing.pytestArgs": ["tests/", "-v", "--tb=short"],
                "python.testing.autoTestDiscoverOnSaveEnabled": True
            }

            if _is_subset(expected, settings):
                print(f"PASS: Component 1 — .vscode/settings.json has all required pytest settings (0.4 pts)")
                total_score += 0.4
            else:
                # Check individual settings for partial info
                missing = []
                for key, val in expected.items():
                    if key not in settings:
                        missing.append(f"  missing key: {key}")
                    elif settings[key] != val:
                        missing.append(f"  wrong value for {key}: expected {val}, got {settings[key]}")
                print(f"FAIL: Component 1 — settings.json missing/wrong entries:")
                for m in missing:
                    print(m)
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: tests/test_sample.py exists with at least 2 test functions (0.3 points)
    test_file_path = os.path.join(PROJECT_DIR, 'tests', 'test_sample.py')
    try:
        if not os.path.exists(test_file_path):
            print(f"FAIL: Component 2 — tests/test_sample.py does not exist")
        else:
            with open(test_file_path, 'r') as f:
                test_content = f.read()

            # Count test functions (def test_...)
            test_funcs = re.findall(r'^def\s+(test_\w+)\s*\(', test_content, re.MULTILINE)
            if len(test_funcs) >= 2:
                print(f"PASS: Component 2 — test_sample.py has {len(test_funcs)} test functions: {test_funcs} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — test_sample.py has only {len(test_funcs)} test function(s), need >= 2. Found: {test_funcs}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: pytest runs and all tests pass (0.3 points)
    # Use pytest.main() programmatically to avoid subprocess
    try:
        if not os.path.exists(test_file_path):
            print(f"FAIL: Component 3 — cannot run pytest, test file missing")
        else:
            import sys
            original_cwd = os.getcwd()
            original_argv = sys.argv[:]
            try:
                os.chdir(PROJECT_DIR)
                import pytest
                # pytest.main returns 0 on success, non-zero on failure
                exit_code = pytest.main(['tests/', '-v', '--tb=short', '-q'])
                if exit_code == 0:
                    print(f"PASS: Component 3 — pytest passed all tests (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — pytest returned exit code {exit_code}")
            finally:
                os.chdir(original_cwd)
                sys.argv = original_argv
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
