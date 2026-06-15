"""
Initial Setup: Git bisect debug repository for VSCode
Task ID: vscode_gf6_016
Domain: vscode

Creates a git repository with 30 commits where a bug is introduced at commit #18.
The bug changes calculate_tax() to return incorrect results for amounts over 10000.
Tag v1.0 is placed at commit #5.
"""

import os
import shlex
import subprocess
import stat
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_016'
PROJECT_DIR = f'{WORKDIR}/projects/git-bisect-debug'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def run_cmd(cmd, cwd=None):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True,
        env={**os.environ, 'GIT_AUTHOR_NAME': 'Alex Rivera',
             'GIT_AUTHOR_EMAIL': 'alex.rivera@techcorp.dev',
             'GIT_COMMITTER_NAME': 'Alex Rivera',
             'GIT_COMMITTER_EMAIL': 'alex.rivera@techcorp.dev'}
    )
    if result.returncode != 0 and 'fatal' in result.stderr.lower():
        print(f"CMD ERROR: {cmd}\n{result.stderr}")
    return result.stdout.strip()


# ── Correct tax function (used for commits 1-17 and after any correct versions) ──
CORRECT_TAX_PY = '''\
"""Tax calculation module for TechCorp payroll system."""


def calculate_tax(amount, rate):
    """
    Calculate tax based on progressive brackets.

    Args:
        amount: The taxable income amount
        rate: The base tax rate (0.0 to 1.0)

    Returns:
        The calculated tax as a float
    """
    if amount <= 0:
        return 0.0

    # Progressive bracket calculation
    if amount <= 5000:
        tax = amount * rate * 0.5
    elif amount <= 10000:
        tax = 5000 * rate * 0.5 + (amount - 5000) * rate * 0.75
    else:
        # For amounts over 10000, apply full rate on the excess
        tax = (5000 * rate * 0.5
               + 5000 * rate * 0.75
               + (amount - 10000) * rate)

    return round(tax, 2)


def calculate_total_tax(incomes, rate):
    """Calculate total tax across multiple income sources."""
    return sum(calculate_tax(inc, rate) for inc in incomes)


def format_tax_report(amount, rate):
    """Generate a formatted tax report string."""
    tax = calculate_tax(amount, rate)
    effective_rate = (tax / amount * 100) if amount > 0 else 0
    return (f"Income: ${amount:,.2f}\\n"
            f"Tax Rate: {rate:.1%}\\n"
            f"Tax Owed: ${tax:,.2f}\\n"
            f"Effective Rate: {effective_rate:.1f}%")
'''

# ── Buggy tax function (introduced at commit #18) ──
BUGGY_TAX_PY = '''\
"""Tax calculation module for TechCorp payroll system."""


def calculate_tax(amount, rate):
    """
    Calculate tax based on progressive brackets.

    Args:
        amount: The taxable income amount
        rate: The base tax rate (0.0 to 1.0)

    Returns:
        The calculated tax as a float
    """
    if amount <= 0:
        return 0.0

    # Progressive bracket calculation
    if amount <= 5000:
        tax = amount * rate * 0.5
    elif amount <= 10000:
        tax = 5000 * rate * 0.5 + (amount - 5000) * rate * 0.75
    else:
        # Refactored bracket logic for clarity
        tax = (5000 * rate * 0.5
               + 5000 * rate * 0.75
               + (amount - 10000) * rate * 0.5)

    return round(tax, 2)


def calculate_total_tax(incomes, rate):
    """Calculate total tax across multiple income sources."""
    return sum(calculate_tax(inc, rate) for inc in incomes)


def format_tax_report(amount, rate):
    """Generate a formatted tax report string."""
    tax = calculate_tax(amount, rate)
    effective_rate = (tax / amount * 100) if amount > 0 else 0
    return (f"Income: ${amount:,.2f}\\n"
            f"Tax Rate: {rate:.1%}\\n"
            f"Tax Owed: ${tax:,.2f}\\n"
            f"Effective Rate: {effective_rate:.1f}%")
'''

# ── Test file ──
TEST_TAX_PY = '''\
"""Tests for the tax calculation module."""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tax import calculate_tax


def test_zero_amount():
    assert calculate_tax(0, 0.2) == 0.0


def test_negative_amount():
    assert calculate_tax(-100, 0.2) == 0.0


def test_low_bracket():
    """Test amounts in the first bracket (0-5000)."""
    result = calculate_tax(3000, 0.2)
    expected = 3000 * 0.2 * 0.5  # 300.0
    assert result == expected, f"Expected {expected}, got {result}"


def test_mid_bracket():
    """Test amounts in the second bracket (5001-10000)."""
    result = calculate_tax(8000, 0.2)
    expected = 5000 * 0.2 * 0.5 + 3000 * 0.2 * 0.75  # 500 + 450 = 950
    assert result == expected, f"Expected {expected}, got {result}"


def test_high_bracket():
    """Test amounts in the third bracket (over 10000)."""
    result = calculate_tax(15000, 0.2)
    # 5000*0.2*0.5 + 5000*0.2*0.75 + 5000*0.2
    expected = 500.0 + 750.0 + 1000.0  # 2250.0
    assert result == expected, f"Expected {expected}, got {result}"


def test_high_bracket_large_amount():
    """Test with a large amount well over 10000."""
    result = calculate_tax(50000, 0.3)
    # 5000*0.3*0.5 + 5000*0.3*0.75 + 40000*0.3
    expected = 750.0 + 1125.0 + 12000.0  # 13875.0
    assert result == expected, f"Expected {expected}, got {result}"


def test_boundary_10000():
    """Test at the exact boundary of 10000."""
    result = calculate_tax(10000, 0.2)
    expected = 5000 * 0.2 * 0.5 + 5000 * 0.2 * 0.75  # 500 + 750 = 1250
    assert result == expected, f"Expected {expected}, got {result}"


def test_just_over_10000():
    """Test just over the 10000 boundary."""
    result = calculate_tax(10001, 0.2)
    expected = 5000 * 0.2 * 0.5 + 5000 * 0.2 * 0.75 + 1 * 0.2
    assert round(result, 2) == round(expected, 2), f"Expected {expected}, got {result}"
'''

# ── run_test.sh ──
RUN_TEST_SH = '''\
#!/bin/bash
cd "$(dirname "$0")"
python3 -m pytest tests/test_tax.py -q
'''

# ── README ──
README_MD = '''\
# TechCorp Tax Calculator

Internal payroll tax calculation module for TechCorp.

## Structure

- `src/tax.py` - Core tax calculation functions
- `tests/test_tax.py` - Test suite
- `run_test.sh` - Test runner script

## Usage

```python
from src.tax import calculate_tax

tax = calculate_tax(amount=45000, rate=0.25)
```

## Running Tests

```bash
./run_test.sh
```
'''

# ── Various file contents for non-tax commits ──

UTILS_PY = '''\
"""Utility functions for the tax system."""

import logging

logger = logging.getLogger(__name__)


def validate_amount(amount):
    """Validate that amount is a valid number."""
    if not isinstance(amount, (int, float)):
        raise TypeError(f"Amount must be numeric, got {type(amount).__name__}")
    return float(amount)


def validate_rate(rate):
    """Validate that rate is between 0 and 1."""
    if not 0 <= rate <= 1:
        raise ValueError(f"Rate must be between 0 and 1, got {rate}")
    return float(rate)
'''

CONFIG_PY = '''\
"""Configuration settings for the tax calculator."""

# Tax bracket thresholds
BRACKET_1_MAX = 5000
BRACKET_2_MAX = 10000

# Bracket multipliers
BRACKET_1_MULTIPLIER = 0.5
BRACKET_2_MULTIPLIER = 0.75
BRACKET_3_MULTIPLIER = 1.0

# Formatting
CURRENCY_SYMBOL = "$"
DECIMAL_PLACES = 2
'''

CONFTEST_PY = '''\
"""Pytest configuration and shared fixtures."""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def sample_amounts():
    """Provide sample test amounts."""
    return [1000, 5000, 8000, 10000, 15000, 25000, 50000]


@pytest.fixture
def standard_rate():
    """Provide a standard tax rate for testing."""
    return 0.2
'''

SETUP_CFG = '''\
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
'''


def create_initial():
    # Install pytest on the VM
    subprocess.run('pip3 install pytest 2>/dev/null', shell=True)

    # Clean up any existing project directory
    if os.path.exists(PROJECT_DIR):
        subprocess.run(f'rm -rf {PROJECT_DIR}', shell=True)

    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # Initialize git repo with 'main' as default branch
    run_cmd('git init -b main', cwd=PROJECT_DIR)
    run_cmd('git config user.name "Alex Rivera"', cwd=PROJECT_DIR)
    run_cmd('git config user.email "alex.rivera@techcorp.dev"', cwd=PROJECT_DIR)

    # Commit messages for 30 commits - realistic project history
    # Commits 1-17: correct code, building up the project
    # Commit 18: introduces the bug (changes rate*1.0 to rate*0.5 for bracket 3)
    # Commits 19-30: continue development with the bug still present

    commits = [
        # 1
        ("Initial project structure",
         {"README.md": "# TechCorp Tax Calculator\n\nInitial project setup.\n",
          "src/__init__.py": "",
          "tests/__init__.py": ""}),
        # 2
        ("Add basic calculate_tax function",
         {"src/tax.py": CORRECT_TAX_PY}),
        # 3
        ("Add test suite for tax calculations",
         {"tests/test_tax.py": TEST_TAX_PY}),
        # 4
        ("Add test runner script",
         {"run_test.sh": RUN_TEST_SH}),
        # 5 - this gets tag v1.0
        ("Release v1.0 - stable tax calculation module",
         {"README.md": README_MD}),
        # 6
        ("Add input validation utilities",
         {"src/utils.py": UTILS_PY}),
        # 7
        ("Add configuration constants",
         {"src/config.py": CONFIG_PY}),
        # 8
        ("Add pytest configuration",
         {"setup.cfg": SETUP_CFG}),
        # 9
        ("Add conftest with shared fixtures",
         {"tests/conftest.py": CONFTEST_PY}),
        # 10
        ("Update README with project structure details",
         {"README.md": README_MD.replace("## Structure", "## Project Structure")}),
        # 11
        ("Add docstring improvements to tax module",
         {None: None}),  # no-op, we'll handle specially
        # 12
        ("Add type hints to utility functions",
         {None: None}),
        # 13
        ("Update test descriptions for clarity",
         {None: None}),
        # 14
        ("Add .gitignore for Python artifacts",
         {".gitignore": "__pycache__/\n*.pyc\n*.pyo\n.pytest_cache/\n*.egg-info/\ndist/\nbuild/\n.env\n"}),
        # 15
        ("Add CHANGELOG.md",
         {"CHANGELOG.md": "# Changelog\n\n## v1.0 (2025-01-15)\n- Initial release\n- Progressive tax bracket calculation\n- Test suite with full coverage\n"}),
        # 16
        ("Update logging configuration in utils",
         {None: None}),
        # 17
        ("Minor code style cleanup",
         {None: None}),
        # 18 - THE BUG COMMIT
        ("Refactor tax bracket calculation for readability",
         {"src/tax.py": BUGGY_TAX_PY}),
        # 19
        ("Add performance benchmarks placeholder",
         {"benchmarks/__init__.py": "",
          "benchmarks/bench_tax.py": '"""Performance benchmarks for tax calculations."""\n\nimport time\nfrom src.tax import calculate_tax\n\n\ndef benchmark_calculate_tax(iterations=10000):\n    start = time.time()\n    for _ in range(iterations):\n        calculate_tax(50000, 0.25)\n    elapsed = time.time() - start\n    print(f"{iterations} iterations in {elapsed:.3f}s")\n\n\nif __name__ == "__main__":\n    benchmark_calculate_tax()\n'}),
        # 20
        ("Add CI configuration stub",
         {".github/workflows/test.yml": "name: Tests\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - uses: actions/setup-python@v4\n        with:\n          python-version: '3.11'\n      - run: pip install pytest\n      - run: python -m pytest\n"}),
        # 21
        ("Add contribution guidelines",
         {"CONTRIBUTING.md": "# Contributing\n\n1. Fork the repository\n2. Create a feature branch\n3. Make your changes\n4. Run tests with ./run_test.sh\n5. Submit a pull request\n"}),
        # 22
        ("Update CHANGELOG for upcoming v1.1",
         {"CHANGELOG.md": "# Changelog\n\n## v1.1 (Unreleased)\n- Refactored bracket logic\n- Added benchmarks\n- Added CI pipeline\n\n## v1.0 (2025-01-15)\n- Initial release\n- Progressive tax bracket calculation\n- Test suite with full coverage\n"}),
        # 23
        ("Add requirements.txt",
         {"requirements.txt": "pytest>=7.0\npytest-cov>=4.0\n"}),
        # 24
        ("Add coverage configuration",
         {".coveragerc": "[run]\nsource = src\nomit = tests/*\n\n[report]\nshow_missing = true\nprecision = 2\n"}),
        # 25
        ("Add LICENSE file",
         {"LICENSE": "MIT License\n\nCopyright (c) 2025 TechCorp\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files.\n"}),
        # 26
        ("Add format_tax_report edge case handling",
         {None: None}),
        # 27
        ("Update test fixture data",
         {None: None}),
        # 28
        ("Add Makefile for common tasks",
         {"Makefile": "test:\n\t./run_test.sh\n\nbenchmark:\n\tpython -m benchmarks.bench_tax\n\nclean:\n\tfind . -name __pycache__ -exec rm -rf {} +\n\tfind . -name '*.pyc' -delete\n"}),
        # 29
        ("Improve error messages in validation",
         {None: None}),
        # 30
        ("Update README with badge and setup instructions",
         {"README.md": README_MD.replace("# TechCorp Tax Calculator",
                                          "# TechCorp Tax Calculator\n\n![Tests](https://github.com/techcorp/tax-calc/actions/workflows/test.yml/badge.svg)")}),
    ]

    for i, (message, files) in enumerate(commits, 1):
        if files and list(files.keys())[0] is not None:
            for filepath, content in files.items():
                full_path = os.path.join(PROJECT_DIR, filepath)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w') as f:
                    f.write(content)
                run_cmd(f'git add "{filepath}"', cwd=PROJECT_DIR)
        else:
            # For no-op commits, make a trivial whitespace change to an existing file
            # to keep commit history realistic
            trivial_file = os.path.join(PROJECT_DIR, 'src', 'tax.py')
            with open(trivial_file, 'r') as f:
                content = f.read()
            # Add/remove a trailing newline to create a diff
            if content.endswith('\n\n'):
                content = content.rstrip('\n') + '\n'
            else:
                content = content.rstrip('\n') + '\n\n'
            with open(trivial_file, 'w') as f:
                f.write(content)
            run_cmd('git add src/tax.py', cwd=PROJECT_DIR)

        run_cmd(f'git commit -m "{message}"', cwd=PROJECT_DIR)

        # Tag v1.0 at commit #5
        if i == 5:
            run_cmd('git tag v1.0', cwd=PROJECT_DIR)

    # Make run_test.sh executable
    run_test_path = os.path.join(PROJECT_DIR, 'run_test.sh')
    os.chmod(run_test_path, os.stat(run_test_path).st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    # Verify: check commit count and tag
    log_output = run_cmd('git log --oneline', cwd=PROJECT_DIR)
    commit_count = len(log_output.strip().split('\n'))
    print(f"Repository created with {commit_count} commits")

    tag_output = run_cmd('git tag -l', cwd=PROJECT_DIR)
    print(f"Tags: {tag_output}")

    # Verify tests fail on HEAD (bug is present)
    test_result = subprocess.run(
        'python3 -m pytest tests/test_tax.py -q',
        shell=True, cwd=PROJECT_DIR,
        capture_output=True, text=True
    )
    print(f"Tests on HEAD (should fail): exit code {test_result.returncode}")
    print(test_result.stdout[-200:] if len(test_result.stdout) > 200 else test_result.stdout)

    # Verify tests pass at v1.0
    run_cmd('git stash', cwd=PROJECT_DIR)
    run_cmd('git checkout v1.0', cwd=PROJECT_DIR)
    test_v1 = subprocess.run(
        'python3 -m pytest tests/test_tax.py -q',
        shell=True, cwd=PROJECT_DIR,
        capture_output=True, text=True
    )
    print(f"Tests on v1.0 (should pass): exit code {test_v1.returncode}")
    run_cmd('git checkout main', cwd=PROJECT_DIR)

    print(f'Initial setup complete: {PROJECT_DIR}')

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
