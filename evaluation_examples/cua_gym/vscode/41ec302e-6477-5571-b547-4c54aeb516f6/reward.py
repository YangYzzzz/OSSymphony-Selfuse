"""
Reward Script: Configure Python test coverage visualization in VSCode
Task ID: vscode_py_070
Domain: vscode
Scoring:
  Component 1: pyproject.toml has pytest-cov addopts (0.3 pts)
  Component 2: VSCode settings have coverage-gutters config (0.3 pts)
  Component 3: VSCode settings have pytest + coverage args (0.2 pts)
  Component 4: lcov.info exists with valid LCOV content (0.2 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_070'
PROJECT_DIR = os.path.join(WORKDIR, TASK_ID)
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Cannot load settings.json: {e}")
        return {}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: pyproject.toml has pytest-cov addopts with --cov and --cov-report=lcov (0.3 pts)
    try:
        pyproject_path = os.path.join(PROJECT_DIR, 'pyproject.toml')
        if not os.path.exists(pyproject_path):
            print(f"FAIL: Component 1 — pyproject.toml not found at {pyproject_path}")
        else:
            with open(pyproject_path, 'r') as f:
                pyproject_content = f.read()

            # Check for addopts containing --cov and --cov-report=lcov
            # Look for addopts line in [tool.pytest.ini_options]
            addopts_match = re.search(r'addopts\s*=\s*["\'](.+?)["\']', pyproject_content)
            addopts_value = addopts_match.group(1) if addopts_match else ''
            # Check for --cov (but not just --cov-report which also contains --cov)
            has_cov = bool(re.search(r'--cov\b', addopts_value))
            # Check for --cov-report with lcov format
            has_lcov_report = bool(re.search(r'--cov-report\s*=\s*lcov', addopts_value))

            if has_cov and has_lcov_report:
                print(f"PASS: Component 1 — pyproject.toml has --cov and --cov-report=lcov in addopts (0.3 pts)")
                total_score += 0.3
            elif has_cov:
                print(f"PARTIAL: Component 1 — pyproject.toml has --cov but missing --cov-report=lcov (0.15 pts)")
                total_score += 0.15
            elif has_lcov_report:
                print(f"PARTIAL: Component 1 — pyproject.toml has --cov-report=lcov but missing --cov (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — pyproject.toml missing --cov and --cov-report=lcov in addopts. Found addopts: {addopts_match.group(0) if addopts_match else 'none'}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: VSCode settings have coverage-gutters configuration (0.3 pts)
    try:
        settings = load_settings()

        gutters_checks = 0
        gutters_total = 3

        # Check coverage-gutters.showGutterCoverage
        if settings.get('coverage-gutters.showGutterCoverage') is True:
            gutters_checks += 1
            print("  PASS: coverage-gutters.showGutterCoverage = true")
        else:
            print(f"  FAIL: coverage-gutters.showGutterCoverage expected true, found: {settings.get('coverage-gutters.showGutterCoverage', '<missing>')}")

        # Check coverage-gutters.showLineCoverage
        if settings.get('coverage-gutters.showLineCoverage') is True:
            gutters_checks += 1
            print("  PASS: coverage-gutters.showLineCoverage = true")
        else:
            print(f"  FAIL: coverage-gutters.showLineCoverage expected true, found: {settings.get('coverage-gutters.showLineCoverage', '<missing>')}")

        # Check coverage-gutters.coverageFileNames includes lcov.info
        cov_files = settings.get('coverage-gutters.coverageFileNames', [])
        if isinstance(cov_files, list) and 'lcov.info' in cov_files:
            gutters_checks += 1
            print("  PASS: coverage-gutters.coverageFileNames includes 'lcov.info'")
        else:
            print(f"  FAIL: coverage-gutters.coverageFileNames expected to include 'lcov.info', found: {cov_files}")

        if gutters_checks > 0:
            comp2_score = round(0.3 * gutters_checks / gutters_total, 2)
            print(f"PASS: Component 2 — {gutters_checks}/{gutters_total} coverage-gutters settings correct ({comp2_score} pts)")
            total_score += comp2_score
        else:
            print("FAIL: Component 2 — no coverage-gutters settings found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: VSCode settings have pytest enabled with coverage args (0.2 pts)
    try:
        settings = load_settings()

        pytest_checks = 0
        pytest_total = 2

        # Check python.testing.pytestEnabled
        if settings.get('python.testing.pytestEnabled') is True:
            pytest_checks += 1
            print("  PASS: python.testing.pytestEnabled = true")
        else:
            print(f"  FAIL: python.testing.pytestEnabled expected true, found: {settings.get('python.testing.pytestEnabled', '<missing>')}")

        # Check python.testing.pytestArgs contains coverage args
        pytest_args = settings.get('python.testing.pytestArgs', [])
        if isinstance(pytest_args, list):
            args_str = ' '.join(pytest_args)
            has_cov_arg = any('--cov' in arg and '--cov-report' not in arg for arg in pytest_args)
            has_lcov_arg = any('--cov-report' in arg and 'lcov' in arg for arg in pytest_args)
            if has_cov_arg and has_lcov_arg:
                pytest_checks += 1
                print(f"  PASS: python.testing.pytestArgs contains --cov and --cov-report=lcov")
            else:
                print(f"  FAIL: python.testing.pytestArgs missing coverage args, found: {pytest_args}")
        else:
            print(f"  FAIL: python.testing.pytestArgs not a list, found: {pytest_args}")

        if pytest_checks > 0:
            comp3_score = round(0.2 * pytest_checks / pytest_total, 2)
            print(f"PASS: Component 3 — {pytest_checks}/{pytest_total} pytest settings correct ({comp3_score} pts)")
            total_score += comp3_score
        else:
            print("FAIL: Component 3 — no pytest coverage settings found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: lcov.info exists with valid LCOV content (0.2 pts)
    try:
        lcov_path = os.path.join(PROJECT_DIR, 'lcov.info')
        if not os.path.exists(lcov_path):
            print(f"FAIL: Component 4 — lcov.info not found at {lcov_path}")
        else:
            with open(lcov_path, 'r') as f:
                lcov_content = f.read()

            lcov_checks = 0
            lcov_total = 2

            # Check lcov has SF: lines (source file references)
            sf_lines = re.findall(r'^SF:', lcov_content, re.MULTILINE)
            if len(sf_lines) > 0:
                lcov_checks += 1
                print(f"  PASS: lcov.info has {len(sf_lines)} source file entries")
            else:
                print("  FAIL: lcov.info has no SF: lines")

            # Check lcov has DA: lines (data/coverage lines)
            da_lines = re.findall(r'^DA:', lcov_content, re.MULTILINE)
            if len(da_lines) > 0:
                lcov_checks += 1
                print(f"  PASS: lcov.info has {len(da_lines)} coverage data lines")
            else:
                print("  FAIL: lcov.info has no DA: lines")

            if lcov_checks > 0:
                comp4_score = round(0.2 * lcov_checks / lcov_total, 2)
                print(f"PASS: Component 4 — lcov.info has valid content ({comp4_score} pts)")
                total_score += comp4_score
            else:
                print("FAIL: Component 4 — lcov.info has no valid LCOV content")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
