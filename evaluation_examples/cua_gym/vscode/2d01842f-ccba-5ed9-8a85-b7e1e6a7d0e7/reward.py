"""
Reward Script: Install Python Test Explorer, create pytest config, run tests with coverage
Task ID: vscode_stu_082
Domain: vs_code
Scoring:
  Component 1: Python extension installed (0.15 pts)
  Component 2: Coverage Gutters extension installed (0.15 pts)
  Component 3: pytest configuration present (pytest.ini or settings) (0.20 pts)
  Component 4: Coverage config (.coveragerc) present with correct settings (0.10 pts)
  Component 5: Tests have been run (.pytest_cache exists) (0.15 pts)
  Component 6: Coverage data generated (coverage.xml with valid content) (0.25 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
WORKSPACE = os.path.join(WORKDIR, 'workspace')
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
TASK_ID = 'vscode_stu_082'


def load_settings():
    """Load VSCode user settings, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_workspace_settings():
    """Load workspace .vscode/settings.json."""
    ws_settings_path = os.path.join(WORKSPACE, '.vscode', 'settings.json')
    try:
        with open(ws_settings_path, 'r') as f:
            content = f.read()
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def check_extension_installed(ext_id):
    """Check if a VSCode extension is installed by scanning the extensions directory."""
    extensions_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
    if not os.path.isdir(extensions_dir):
        return False
    for entry in os.listdir(extensions_dir):
        if entry.lower().startswith(ext_id.lower()):
            return True
    return False


def is_extension_present(ext_id):
    """Check extension presence via directory scan."""
    return check_extension_installed(ext_id)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Python extension installed (0.15 points)
    # The task requires "Python Test Explorer" which is part of ms-python.python
    try:
        python_ext = is_extension_present('ms-python.python')
        if python_ext:
            print(f"PASS: Component 1 — ms-python.python extension installed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — ms-python.python extension not installed")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Coverage Gutters extension installed (0.15 points)
    # Required to see coverage gutters in the editor
    try:
        coverage_ext = is_extension_present('ryanluker.vscode-coverage-gutters')
        if coverage_ext:
            print(f"PASS: Component 2 — vscode-coverage-gutters extension installed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — ryanluker.vscode-coverage-gutters extension not installed")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: pytest configuration present (0.20 points)
    # Either pytest.ini or VSCode settings must enable pytest
    try:
        pytest_configured = False
        details = []

        # Check pytest.ini
        pytest_ini_path = os.path.join(WORKSPACE, 'pytest.ini')
        if os.path.isfile(pytest_ini_path):
            with open(pytest_ini_path, 'r') as f:
                content = f.read()
            if '[pytest]' in content:
                pytest_configured = True
                details.append("pytest.ini with [pytest] section found")

        # Check setup.cfg for [tool:pytest]
        setup_cfg_path = os.path.join(WORKSPACE, 'setup.cfg')
        if os.path.isfile(setup_cfg_path):
            with open(setup_cfg_path, 'r') as f:
                content = f.read()
            if '[tool:pytest]' in content:
                pytest_configured = True
                details.append("setup.cfg with [tool:pytest] found")

        # Check pyproject.toml for [tool.pytest]
        pyproject_path = os.path.join(WORKSPACE, 'pyproject.toml')
        if os.path.isfile(pyproject_path):
            with open(pyproject_path, 'r') as f:
                content = f.read()
            if '[tool.pytest' in content:
                pytest_configured = True
                details.append("pyproject.toml with [tool.pytest] found")

        # Check VSCode settings for pytestEnabled
        user_settings = load_settings()
        ws_settings = load_workspace_settings()
        if user_settings.get('python.testing.pytestEnabled') is True:
            pytest_configured = True
            details.append("User settings: python.testing.pytestEnabled=true")
        if ws_settings.get('python.testing.pytestEnabled') is True:
            pytest_configured = True
            details.append("Workspace settings: python.testing.pytestEnabled=true")

        if pytest_configured:
            print(f"PASS: Component 3 — pytest configured: {'; '.join(details)} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — no pytest configuration found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Coverage config (.coveragerc) with correct settings (0.10 points)
    try:
        coveragerc_path = os.path.join(WORKSPACE, '.coveragerc')
        coverage_configured = False

        if os.path.isfile(coveragerc_path):
            with open(coveragerc_path, 'r') as f:
                content = f.read()
            if '[run]' in content and 'source' in content:
                coverage_configured = True

        # Also check if coverage args are in pytest.ini or settings
        if not coverage_configured:
            pytest_ini_path = os.path.join(WORKSPACE, 'pytest.ini')
            if os.path.isfile(pytest_ini_path):
                with open(pytest_ini_path, 'r') as f:
                    content = f.read()
                if '--cov' in content:
                    coverage_configured = True

        if not coverage_configured:
            # Check VSCode settings for coverage args
            user_settings = load_settings()
            ws_settings = load_workspace_settings()
            pytest_args = user_settings.get('python.testing.pytestArgs', [])
            pytest_args_ws = ws_settings.get('python.testing.pytestArgs', [])
            all_args = ' '.join(pytest_args + pytest_args_ws)
            if '--cov' in all_args:
                coverage_configured = True

        if coverage_configured:
            print(f"PASS: Component 4 — coverage configuration found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — no coverage configuration found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Tests have been run (.pytest_cache exists) (0.15 points)
    try:
        pytest_cache_dir = os.path.join(WORKSPACE, '.pytest_cache')
        tests_run = False

        if os.path.isdir(pytest_cache_dir):
            # Verify it has actual cache content (v/ directory or CACHEDIR.TAG)
            cache_contents = os.listdir(pytest_cache_dir)
            if len(cache_contents) > 0:
                tests_run = True

        if tests_run:
            print(f"PASS: Component 5 — .pytest_cache found with content, tests were run (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — .pytest_cache not found, tests have not been run")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Coverage data generated (coverage.xml with valid content) (0.25 points)
    try:
        coverage_xml_path = os.path.join(WORKSPACE, 'coverage.xml')
        coverage_valid = False

        if os.path.isfile(coverage_xml_path):
            with open(coverage_xml_path, 'r') as f:
                content = f.read()
            # Check it's a valid coverage XML with actual line data
            if '<coverage' in content and '<line ' in content and 'calculator' in content.lower():
                coverage_valid = True

        # Also accept .coverage sqlite db as alternative evidence
        if not coverage_valid:
            coverage_db_path = os.path.join(WORKSPACE, '.coverage')
            if os.path.isfile(coverage_db_path) and os.path.getsize(coverage_db_path) > 0:
                # It's a sqlite db, try to verify it has data
                try:
                    import sqlite3
                    conn = sqlite3.connect(coverage_db_path)
                    c = conn.cursor()
                    c.execute("SELECT COUNT(*) FROM file")
                    count = c.fetchone()[0]
                    conn.close()
                    if count > 0:
                        coverage_valid = True
                except Exception:
                    pass

        if coverage_valid:
            print(f"PASS: Component 6 — coverage data generated with calculator.py coverage (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 6 — no valid coverage data found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
