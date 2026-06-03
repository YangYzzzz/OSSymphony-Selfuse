"""
Initial Setup: Configure Python test coverage visualization in VSCode
Task ID: vscode_py_070
Domain: vscode

Creates a Python project with source code and tests. pytest-cov is installed
but NOT configured. Coverage Gutters extension is installed but not configured.
No coverage data exists.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_070'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
SRC_DIR = f'{PROJECT_DIR}/src'
TESTS_DIR = f'{PROJECT_DIR}/tests'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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


def create_project():
    """Create a realistic Python project with source and tests."""
    # Create directory structure
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(TESTS_DIR, exist_ok=True)

    # src/__init__.py
    with open(f'{SRC_DIR}/__init__.py', 'w') as f:
        f.write('')

    # src/calculator.py - A realistic calculator module
    with open(f'{SRC_DIR}/calculator.py', 'w') as f:
        f.write('''"""Calculator module for financial computations."""


class Calculator:
    """A calculator with memory and history tracking."""

    def __init__(self):
        self.memory = 0.0
        self.history = []

    def add(self, a: float, b: float) -> float:
        """Add two numbers and store in history."""
        result = a + b
        self.history.append(('add', a, b, result))
        return result

    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a and store in history."""
        result = a - b
        self.history.append(('subtract', a, b, result))
        return result

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers and store in history."""
        result = a * b
        self.history.append(('multiply', a, b, result))
        return result

    def divide(self, a: float, b: float) -> float:
        """Divide a by b. Raises ValueError on division by zero."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(('divide', a, b, result))
        return result

    def store_memory(self, value: float):
        """Store a value in memory."""
        self.memory = value

    def recall_memory(self) -> float:
        """Recall the stored memory value."""
        return self.memory

    def clear_history(self):
        """Clear computation history."""
        self.history = []

    def get_history(self) -> list:
        """Return the computation history."""
        return list(self.history)


def compound_interest(principal: float, rate: float, years: int,
                      compounds_per_year: int = 12) -> float:
    """Calculate compound interest.

    Args:
        principal: Initial investment amount
        rate: Annual interest rate (e.g., 0.05 for 5%)
        years: Number of years
        compounds_per_year: Times interest compounds per year

    Returns:
        Final amount after compound interest
    """
    if principal < 0:
        raise ValueError("Principal must be non-negative")
    if rate < 0:
        raise ValueError("Rate must be non-negative")
    if years < 0:
        raise ValueError("Years must be non-negative")

    amount = principal * (1 + rate / compounds_per_year) ** (
        compounds_per_year * years
    )
    return round(amount, 2)


def loan_payment(principal: float, annual_rate: float,
                 months: int) -> float:
    """Calculate monthly loan payment.

    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (e.g., 0.06 for 6%)
        months: Total number of monthly payments

    Returns:
        Monthly payment amount
    """
    if months <= 0:
        raise ValueError("Months must be positive")
    if annual_rate == 0:
        return round(principal / months, 2)

    monthly_rate = annual_rate / 12
    payment = principal * (
        monthly_rate * (1 + monthly_rate) ** months
    ) / ((1 + monthly_rate) ** months - 1)
    return round(payment, 2)
''')

    # src/statistics_utils.py - Additional module for more coverage area
    with open(f'{SRC_DIR}/statistics_utils.py', 'w') as f:
        f.write('''"""Statistical utility functions."""

import math


def mean(values: list) -> float:
    """Calculate the arithmetic mean."""
    if not values:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(values) / len(values)


def median(values: list) -> float:
    """Calculate the median value."""
    if not values:
        raise ValueError("Cannot calculate median of empty list")
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
    return sorted_vals[mid]


def standard_deviation(values: list) -> float:
    """Calculate population standard deviation."""
    if len(values) < 2:
        raise ValueError("Need at least 2 values for standard deviation")
    avg = mean(values)
    variance = sum((x - avg) ** 2 for x in values) / len(values)
    return round(math.sqrt(variance), 6)


def percentile(values: list, p: float) -> float:
    """Calculate the p-th percentile (0-100)."""
    if not values:
        raise ValueError("Cannot calculate percentile of empty list")
    if not 0 <= p <= 100:
        raise ValueError("Percentile must be between 0 and 100")
    sorted_vals = sorted(values)
    k = (len(sorted_vals) - 1) * (p / 100)
    floor_k = int(math.floor(k))
    ceil_k = int(math.ceil(k))
    if floor_k == ceil_k:
        return sorted_vals[floor_k]
    d = k - floor_k
    return sorted_vals[floor_k] + d * (sorted_vals[ceil_k] - sorted_vals[floor_k])
''')

    # tests/__init__.py
    with open(f'{TESTS_DIR}/__init__.py', 'w') as f:
        f.write('')

    # tests/test_calculator.py - test file with decent coverage
    with open(f'{TESTS_DIR}/test_calculator.py', 'w') as f:
        f.write('''"""Tests for the calculator module."""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.calculator import Calculator, compound_interest, loan_payment


class TestCalculator:
    """Tests for the Calculator class."""

    def setup_method(self):
        self.calc = Calculator()

    def test_add(self):
        assert self.calc.add(3, 5) == 8
        assert self.calc.add(-1, 1) == 0
        assert self.calc.add(0.1, 0.2) == pytest.approx(0.3)

    def test_subtract(self):
        assert self.calc.subtract(10, 3) == 7
        assert self.calc.subtract(5, 5) == 0

    def test_multiply(self):
        assert self.calc.multiply(4, 5) == 20
        assert self.calc.multiply(-2, 3) == -6

    def test_divide(self):
        assert self.calc.divide(10, 2) == 5
        assert self.calc.divide(7, 3) == pytest.approx(2.3333, abs=0.001)

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)

    def test_memory(self):
        self.calc.store_memory(42.5)
        assert self.calc.recall_memory() == 42.5

    def test_history(self):
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        history = self.calc.get_history()
        assert len(history) == 2
        assert history[0] == ('add', 1, 2, 3)

    def test_clear_history(self):
        self.calc.add(1, 1)
        self.calc.clear_history()
        assert self.calc.get_history() == []


class TestCompoundInterest:
    """Tests for compound_interest function."""

    def test_basic_compound(self):
        result = compound_interest(1000, 0.05, 1)
        assert result == pytest.approx(1051.16, abs=0.01)

    def test_zero_rate(self):
        result = compound_interest(5000, 0.0, 5)
        assert result == 5000.0

    def test_negative_principal(self):
        with pytest.raises(ValueError):
            compound_interest(-100, 0.05, 1)

    def test_negative_rate(self):
        with pytest.raises(ValueError):
            compound_interest(1000, -0.05, 1)


class TestLoanPayment:
    """Tests for loan_payment function."""

    def test_basic_loan(self):
        payment = loan_payment(200000, 0.06, 360)
        assert payment == pytest.approx(1199.10, abs=0.01)

    def test_zero_rate_loan(self):
        payment = loan_payment(12000, 0.0, 12)
        assert payment == 1000.0

    def test_invalid_months(self):
        with pytest.raises(ValueError):
            loan_payment(1000, 0.05, 0)
''')

    # tests/test_statistics.py
    with open(f'{TESTS_DIR}/test_statistics.py', 'w') as f:
        f.write('''"""Tests for statistics utility functions."""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.statistics_utils import mean, median, standard_deviation, percentile


class TestMean:
    def test_basic(self):
        assert mean([1, 2, 3, 4, 5]) == 3.0

    def test_single_value(self):
        assert mean([42]) == 42.0

    def test_empty_list(self):
        with pytest.raises(ValueError):
            mean([])


class TestMedian:
    def test_odd_count(self):
        assert median([3, 1, 2]) == 2

    def test_even_count(self):
        assert median([1, 2, 3, 4]) == 2.5

    def test_empty_list(self):
        with pytest.raises(ValueError):
            median([])


class TestStandardDeviation:
    def test_basic(self):
        result = standard_deviation([2, 4, 4, 4, 5, 5, 7, 9])
        assert result == pytest.approx(2.0, abs=0.01)

    def test_too_few_values(self):
        with pytest.raises(ValueError):
            standard_deviation([1])


class TestPercentile:
    def test_50th(self):
        assert percentile([1, 2, 3, 4, 5], 50) == 3.0

    def test_boundary(self):
        with pytest.raises(ValueError):
            percentile([1, 2, 3], 101)

    def test_empty(self):
        with pytest.raises(ValueError):
            percentile([], 50)
''')

    # pyproject.toml - basic config WITHOUT pytest-cov settings
    with open(f'{PROJECT_DIR}/pyproject.toml', 'w') as f:
        f.write('''[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "financial-tools"
version = "1.0.0"
description = "Financial calculation utilities"
requires-python = ">=3.8"

[tool.pytest.ini_options]
testpaths = ["tests"]
''')

    # README.md for the project
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('''# Financial Tools

A Python library for financial calculations including compound interest,
loan payments, and statistical analysis.

## Running Tests

```bash
cd /home/user/vscode_py_070
pytest
```

## Project Structure

```
vscode_py_070/
  src/
    calculator.py       - Financial calculation functions
    statistics_utils.py - Statistical utility functions
  tests/
    test_calculator.py  - Calculator tests
    test_statistics.py  - Statistics tests
```
''')

    print(f'Project created at: {PROJECT_DIR}')


def install_dependencies():
    """Ensure pytest-cov is installed (as stated in task context)."""
    subprocess.run(['pip3', 'install', 'pytest', 'pytest-cov'],
                   capture_output=True, text=True)
    print('Dependencies installed: pytest, pytest-cov')


def install_coverage_gutters():
    """Install Coverage Gutters extension (installed but not configured per task)."""
    result = subprocess.run(
        ['code', '--install-extension', 'ryanluker.vscode-coverage-gutters', '--force'],
        capture_output=True, text=True
    )
    print(f'Coverage Gutters extension install: {result.stdout.strip()}')
    if result.returncode != 0:
        print(f'Extension install stderr: {result.stderr.strip()}')


def setup_gui():
    """Open VSCode with the project directory."""
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


if __name__ == '__main__':
    create_project()
    install_dependencies()
    install_coverage_gutters()
    setup_gui()
