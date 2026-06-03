"""
Reward Script: Configure Python test discovery with custom 'check_*.py' pattern
Task ID: vscode_py_055
Domain: vscode
Scoring:
  Component 1 (0.5): pyproject.toml contains python_files = "check_*.py" (or equivalent)
  Component 2 (0.2): pyproject.toml has testpaths configured to include "tests"
  Component 3 (0.3): VSCode workspace settings include python.testing.pytestArgs
"""

import os
import json
import re

WORKDIR = '/home/user'
WORKSPACE = os.path.join(WORKDIR, 'workspace')
TASK_ID = 'vscode_py_055'


def strip_jsonc_comments(text):
    """Remove // and /* */ comments from JSONC content."""
    # Remove single-line comments
    text = re.sub(r'//.*$', '', text, flags=re.MULTILINE)
    # Remove multi-line comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    return text


def load_json_file(path):
    """Load a JSON/JSONC file, stripping comments if needed."""
    with open(path, 'r') as f:
        content = f.read()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        cleaned = strip_jsonc_comments(content)
        return json.loads(cleaned)


def check_pytest_config_for_check_pattern():
    """
    Check if any pytest configuration file (pyproject.toml, pytest.ini, setup.cfg)
    contains python_files = check_*.py or equivalent pattern.
    Returns (found_pattern, found_testpaths, details)
    """
    found_pattern = False
    found_testpaths = False
    details_pattern = ""
    details_testpaths = ""

    # Check pyproject.toml
    pyproject_path = os.path.join(WORKSPACE, 'pyproject.toml')
    if os.path.exists(pyproject_path):
        with open(pyproject_path, 'r') as f:
            content = f.read()

        # Check for python_files with check_*.py pattern
        # Matches: python_files = "check_*.py" or python_files = ["check_*.py"] or check_*
        if re.search(r'python_files\s*=\s*.*check_\*', content):
            found_pattern = True
            details_pattern = f"pyproject.toml contains python_files with check_* pattern"

        # Check for testpaths containing "tests"
        if re.search(r'testpaths\s*=', content):
            if re.search(r'testpaths\s*=\s*\[.*"tests"', content) or re.search(r'testpaths\s*=\s*.*tests', content):
                found_testpaths = True
                details_testpaths = f"pyproject.toml has testpaths configured with 'tests'"

    # Check pytest.ini
    pytest_ini_path = os.path.join(WORKSPACE, 'pytest.ini')
    if os.path.exists(pytest_ini_path):
        with open(pytest_ini_path, 'r') as f:
            content = f.read()
        if re.search(r'python_files\s*=\s*.*check_\*', content):
            found_pattern = True
            details_pattern = f"pytest.ini contains python_files with check_* pattern"
        if re.search(r'testpaths\s*=', content):
            found_testpaths = True
            details_testpaths = f"pytest.ini has testpaths configured"

    # Check setup.cfg
    setup_cfg_path = os.path.join(WORKSPACE, 'setup.cfg')
    if os.path.exists(setup_cfg_path):
        with open(setup_cfg_path, 'r') as f:
            content = f.read()
        if re.search(r'python_files\s*=\s*.*check_\*', content):
            found_pattern = True
            details_pattern = f"setup.cfg contains python_files with check_* pattern"
        if re.search(r'testpaths\s*=', content):
            found_testpaths = True
            details_testpaths = f"setup.cfg has testpaths configured"

    # Check conftest.py for collect_ignore or similar
    # Also check if tox.ini has pytest section
    tox_ini_path = os.path.join(WORKSPACE, 'tox.ini')
    if os.path.exists(tox_ini_path):
        with open(tox_ini_path, 'r') as f:
            content = f.read()
        if re.search(r'python_files\s*=\s*.*check_\*', content):
            found_pattern = True
            details_pattern = f"tox.ini contains python_files with check_* pattern"

    return found_pattern, found_testpaths, details_pattern, details_testpaths


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: pytest config has python_files = check_*.py (0.5 points)
    # This is the CORE requirement - telling pytest to discover check_*.py files
    try:
        found_pattern, found_testpaths, details_pattern, details_testpaths = check_pytest_config_for_check_pattern()

        if found_pattern:
            print(f"PASS: Component 1 - {details_pattern} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - No pytest config found with python_files = check_*.py pattern")
            print(f"  Checked: pyproject.toml, pytest.ini, setup.cfg, tox.ini in {WORKSPACE}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: testpaths is configured (0.2 points)
    # This ensures pytest knows where to look for test files
    try:
        if found_testpaths:
            print(f"PASS: Component 2 - {details_testpaths} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 - No testpaths configuration found in pytest config files")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: VSCode workspace settings have pytestArgs (0.3 points)
    # This configures VSCode's test discovery integration
    try:
        # Check workspace-level .vscode/settings.json
        ws_settings_path = os.path.join(WORKSPACE, '.vscode', 'settings.json')
        settings = None

        if os.path.exists(ws_settings_path):
            settings = load_json_file(ws_settings_path)

        if settings is None:
            print(f"FAIL: Component 3 - No .vscode/settings.json found at {ws_settings_path}")
        else:
            pytest_args = settings.get("python.testing.pytestArgs")
            if pytest_args is not None and isinstance(pytest_args, list):
                print(f"PASS: Component 3 - python.testing.pytestArgs found: {pytest_args} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 - python.testing.pytestArgs not found or not a list in workspace settings")
                print(f"  Found keys: {list(settings.keys())}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
