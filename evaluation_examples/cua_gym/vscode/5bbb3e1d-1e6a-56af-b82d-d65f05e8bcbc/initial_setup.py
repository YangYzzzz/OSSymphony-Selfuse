"""
Initial Setup: Set up a Python project with pytest installed, no launch.json
Task ID: vscode_py_051
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_051'
PROJECT_DIR = f'{WORKDIR}/workspace'

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

def create_initial():
    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # Create src/__init__.py
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('')

    # Create src/calculator.py - a realistic Python module
    with open(f'{PROJECT_DIR}/src/calculator.py', 'w') as f:
        f.write('''"""Calculator module with basic arithmetic operations."""


class Calculator:
    """A simple calculator class supporting basic math operations."""

    def __init__(self):
        self.history = []

    def add(self, a: float, b: float) -> float:
        """Return the sum of two numbers."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a: float, b: float) -> float:
        """Return the difference of two numbers."""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def multiply(self, a: float, b: float) -> float:
        """Return the product of two numbers."""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

    def divide(self, a: float, b: float) -> float:
        """Return the quotient of two numbers. Raises ValueError on zero division."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result

    def get_history(self) -> list:
        """Return the calculation history."""
        return list(self.history)

    def clear_history(self):
        """Clear the calculation history."""
        self.history.clear()
''')

    # Create src/stats.py - another module for coverage testing
    with open(f'{PROJECT_DIR}/src/stats.py', 'w') as f:
        f.write('''"""Statistics module for data analysis operations."""

from typing import List
import math


def mean(values: List[float]) -> float:
    """Calculate the arithmetic mean of a list of numbers."""
    if not values:
        raise ValueError("Cannot compute mean of empty list")
    return sum(values) / len(values)


def median(values: List[float]) -> float:
    """Calculate the median of a list of numbers."""
    if not values:
        raise ValueError("Cannot compute median of empty list")
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
    return sorted_vals[mid]


def standard_deviation(values: List[float]) -> float:
    """Calculate the population standard deviation."""
    if len(values) < 2:
        raise ValueError("Need at least two values for standard deviation")
    avg = mean(values)
    variance = sum((x - avg) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


def percentile(values: List[float], p: float) -> float:
    """Calculate the p-th percentile of a list of numbers (0-100)."""
    if not values:
        raise ValueError("Cannot compute percentile of empty list")
    if not 0 <= p <= 100:
        raise ValueError("Percentile must be between 0 and 100")
    sorted_vals = sorted(values)
    k = (len(sorted_vals) - 1) * (p / 100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[f] * (c - k) + sorted_vals[c] * (k - f)
''')

    # Create tests/__init__.py
    with open(f'{PROJECT_DIR}/tests/__init__.py', 'w') as f:
        f.write('')

    # Create tests/test_calculator.py
    with open(f'{PROJECT_DIR}/tests/test_calculator.py', 'w') as f:
        f.write('''"""Tests for the Calculator class."""

import pytest
from src.calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


class TestCalculatorBasic:
    def test_add(self, calc):
        assert calc.add(2, 3) == 5
        assert calc.add(-1, 1) == 0
        assert calc.add(0.1, 0.2) == pytest.approx(0.3)

    def test_subtract(self, calc):
        assert calc.subtract(10, 4) == 6
        assert calc.subtract(0, 5) == -5

    def test_multiply(self, calc):
        assert calc.multiply(3, 4) == 12
        assert calc.multiply(-2, 5) == -10
        assert calc.multiply(0, 100) == 0

    def test_divide(self, calc):
        assert calc.divide(10, 2) == 5
        assert calc.divide(7, 3) == pytest.approx(2.333333)

    def test_divide_by_zero(self, calc):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.divide(10, 0)


class TestCalculatorHistory:
    def test_history_records_operations(self, calc):
        calc.add(1, 2)
        calc.multiply(3, 4)
        history = calc.get_history()
        assert len(history) == 2
        assert "1 + 2 = 3" in history[0]

    def test_clear_history(self, calc):
        calc.add(1, 2)
        calc.clear_history()
        assert len(calc.get_history()) == 0
''')

    # Create tests/test_stats.py
    with open(f'{PROJECT_DIR}/tests/test_stats.py', 'w') as f:
        f.write('''"""Tests for the statistics module."""

import pytest
from src.stats import mean, median, standard_deviation, percentile


class TestMean:
    def test_basic_mean(self):
        assert mean([1, 2, 3, 4, 5]) == 3.0

    def test_single_value(self):
        assert mean([42]) == 42.0

    def test_empty_list(self):
        with pytest.raises(ValueError):
            mean([])


class TestMedian:
    def test_odd_count(self):
        assert median([1, 3, 5]) == 3

    def test_even_count(self):
        assert median([1, 2, 3, 4]) == 2.5

    def test_empty_list(self):
        with pytest.raises(ValueError):
            median([])


class TestStandardDeviation:
    def test_basic(self):
        result = standard_deviation([2, 4, 4, 4, 5, 5, 7, 9])
        assert abs(result - 2.0) < 0.01

    def test_too_few_values(self):
        with pytest.raises(ValueError):
            standard_deviation([1])


class TestPercentile:
    def test_50th(self):
        assert percentile([1, 2, 3, 4, 5], 50) == 3.0

    def test_boundaries(self):
        with pytest.raises(ValueError):
            percentile([1, 2, 3], 101)
''')

    # Create a main.py at project root
    with open(f'{PROJECT_DIR}/main.py', 'w') as f:
        f.write('''"""Main entry point for the workspace project."""

from src.calculator import Calculator
from src.stats import mean, median, standard_deviation


def main():
    calc = Calculator()

    # Basic operations
    print("Calculator Demo")
    print(f"  2 + 3 = {calc.add(2, 3)}")
    print(f"  10 - 4 = {calc.subtract(10, 4)}")
    print(f"  6 * 7 = {calc.multiply(6, 7)}")
    print(f"  15 / 4 = {calc.divide(15, 4)}")

    # Statistics
    data = [23.5, 45.1, 12.8, 67.3, 34.9, 51.2, 28.7, 39.4]
    print(f"\\nStatistics for {data}:")
    print(f"  Mean: {mean(data):.2f}")
    print(f"  Median: {median(data):.2f}")
    print(f"  Std Dev: {standard_deviation(data):.2f}")

    print(f"\\nHistory: {calc.get_history()}")


if __name__ == "__main__":
    main()
''')

    # Create a pyproject.toml for the project
    with open(f'{PROJECT_DIR}/pyproject.toml', 'w') as f:
        f.write('''[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "workspace"
version = "0.1.0"
description = "A sample Python project with calculator and statistics modules"
requires-python = ">=3.8"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.coverage.run]
source = ["src"]
''')

    # Ensure NO .vscode/launch.json exists (this is what the agent must create)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    launch_json_path = f'{vscode_dir}/launch.json'
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)

    # Install pytest and pytest-cov
    subprocess.run(['pip3', 'install', 'pytest', 'pytest-cov'], capture_output=True, text=True)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'  src/calculator.py, src/stats.py')
    print(f'  tests/test_calculator.py, tests/test_stats.py')
    print(f'  main.py, pyproject.toml')
    print(f'  .vscode/launch.json: DOES NOT EXIST (task requires creating it)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
