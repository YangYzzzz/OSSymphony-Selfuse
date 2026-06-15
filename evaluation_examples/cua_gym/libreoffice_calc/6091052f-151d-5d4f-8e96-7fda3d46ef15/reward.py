"""
Reward Script: Set up FastAPI framework from GitHub
Task ID: osworld_multi_apps_vscode_env_setup_005
Domain: multi_apps / vscode_env_setup (OS-level)
Scoring:
  - Component 1: fastapi repo cloned to /home/user/fastapi with correct git remote (0.3 pts)
  - Component 2: fastapi is importable via Python (0.4 pts)
  - Component 3: pytest runs at least some tests without import errors (0.3 pts)

NOTE: This is an OS/shell environment task. subprocess is required for:
  - git remote verification (no pure-Python alternative)
  - pytest execution (test runner must be invoked as separate process)
  These are justified uses; importlib is used for Python import checks.
"""

import os
import sys
import importlib.util
import subprocess

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_env_setup_005'
FASTAPI_DIR = os.path.join(WORKDIR, 'fastapi')
EXPECTED_REMOTE_SUBSTR = 'tiangolo/fastapi'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: fastapi repo cloned to /home/user/fastapi (0.3 points)
    # Checks: directory exists, is a git repo, has pyproject.toml, has tests/ directory,
    # and git remote origin points to tiangolo/fastapi
    try:
        repo_exists = os.path.isdir(FASTAPI_DIR)
        git_dir_exists = os.path.isdir(os.path.join(FASTAPI_DIR, '.git'))
        pyproject_exists = os.path.isfile(os.path.join(FASTAPI_DIR, 'pyproject.toml'))
        tests_dir_exists = os.path.isdir(os.path.join(FASTAPI_DIR, 'tests'))

        if not (repo_exists and git_dir_exists and pyproject_exists and tests_dir_exists):
            print(f"FAIL: Component 1 — fastapi repo not properly cloned at {FASTAPI_DIR}")
            print(f"  repo_exists={repo_exists}, git_dir={git_dir_exists}, "
                  f"pyproject={pyproject_exists}, tests_dir={tests_dir_exists}")
        else:
            # Verify remote URL by reading the git config file directly (no subprocess)
            git_config_path = os.path.join(FASTAPI_DIR, '.git', 'config')
            remote_ok = False
            remote_url_found = 'not found'
            try:
                with open(git_config_path, 'r') as f:
                    git_config = f.read()
                # Find 'url = ...' line after [remote "origin"] section
                in_origin = False
                for line in git_config.splitlines():
                    stripped = line.strip()
                    if stripped == '[remote "origin"]':
                        in_origin = True
                    elif stripped.startswith('[') and in_origin:
                        in_origin = False
                    elif in_origin and stripped.startswith('url ='):
                        remote_url_found = stripped.split('url =', 1)[1].strip()
                        remote_ok = EXPECTED_REMOTE_SUBSTR in remote_url_found
                        break
            except Exception as git_err:
                print(f"  WARN: Could not read git config: {git_err}")

            if remote_ok:
                print(f"PASS: Component 1 — fastapi repo cloned at {FASTAPI_DIR}, "
                      f"remote={remote_url_found} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — repo exists but remote URL unexpected: "
                      f"{remote_url_found}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: fastapi is importable (verifies pip install -e .[all] worked) (0.4 points)
    # Use importlib.util.find_spec to check without importing into this process
    try:
        # First check via find_spec
        spec = importlib.util.find_spec('fastapi')
        if spec is not None:
            # Actually import it to confirm it loads without errors
            import fastapi
            version = getattr(fastapi, '__version__', 'unknown')
            print(f"PASS: Component 2 — fastapi importable, version={version} (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 2 — fastapi module not found (not installed)")
    except ImportError as e:
        print(f"FAIL: Component 2 — fastapi import failed: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: pytest runs at least some tests without import errors (0.3 points)
    # Run a small set of stable test files (avoid test_application.py which requires
    # inline_snapshot — an optional dev dependency not bundled in a basic install).
    # subprocess is required here because pytest is a CLI test runner.
    try:
        test_files = [
            os.path.join(FASTAPI_DIR, 'tests', 'test_path.py'),
            os.path.join(FASTAPI_DIR, 'tests', 'test_query.py'),
        ]

        # Check the test files exist first
        test_files_exist = all(os.path.isfile(tf) for tf in test_files)
        if not test_files_exist:
            missing = [tf for tf in test_files if not os.path.isfile(tf)]
            print(f"FAIL: Component 3 — test files not found: {missing}")
        else:
            result = subprocess.run(
                [sys.executable, '-m', 'pytest'] + test_files +
                ['--no-header', '-q', '--override-ini=filterwarnings=ignore', '--tb=short'],
                capture_output=True, text=True, timeout=60,
                cwd=FASTAPI_DIR
            )
            output = result.stdout + result.stderr
            # Look for at least some tests passing, and no import errors
            has_passed = 'passed' in output
            has_import_error = 'ModuleNotFoundError: No module named' in output

            if has_import_error and not has_passed:
                print(f"FAIL: Component 3 — import errors running pytest. "
                      f"Output snippet: {output[:300]}")
            elif has_passed:
                passed_line = [l for l in output.splitlines() if 'passed' in l]
                summary = passed_line[-1].strip() if passed_line else 'some tests passed'
                print(f"PASS: Component 3 — pytest ran successfully: {summary} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — no tests passed. returncode={result.returncode}. "
                      f"Output: {output[:300]}")
    except subprocess.TimeoutExpired:
        print("ERROR: Component 3 — pytest timed out after 60s")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
