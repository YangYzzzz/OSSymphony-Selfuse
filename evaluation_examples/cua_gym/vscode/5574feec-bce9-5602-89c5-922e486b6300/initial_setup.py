"""
Initial Setup: Create a Python project workspace for VSCode tasks.json task
Task ID: vscode_stu_058
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_058'
PROJECT_DIR = f'{WORKDIR}/cs301/project'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
TESTS_DIR = f'{PROJECT_DIR}/tests'
SRC_DIR = f'{PROJECT_DIR}/src'


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
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(TESTS_DIR, exist_ok=True)

    # Make sure NO .vscode/tasks.json exists
    tasks_json_path = os.path.join(VSCODE_DIR, 'tasks.json')
    if os.path.exists(tasks_json_path):
        os.remove(tasks_json_path)

    # Create realistic Python project files

    # src/calculator.py - main module
    with open(os.path.join(SRC_DIR, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(SRC_DIR, 'calculator.py'), 'w') as f:
        f.write('''"""Simple calculator module for CS301 project."""


class Calculator:
    """A basic calculator with memory functionality."""

    def __init__(self):
        self.memory = 0.0
        self.history = []

    def add(self, a: float, b: float) -> float:
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a: float, b: float) -> float:
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def multiply(self, a: float, b: float) -> float:
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result

    def store_in_memory(self, value: float):
        self.memory = value

    def recall_memory(self) -> float:
        return self.memory

    def clear_history(self):
        self.history.clear()
''')

    # src/statistics_utils.py
    with open(os.path.join(SRC_DIR, 'statistics_utils.py'), 'w') as f:
        f.write('''"""Statistical utility functions for CS301 data analysis."""

import math
from typing import List


def mean(data: List[float]) -> float:
    if not data:
        raise ValueError("Cannot compute mean of empty dataset")
    return sum(data) / len(data)


def median(data: List[float]) -> float:
    if not data:
        raise ValueError("Cannot compute median of empty dataset")
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]


def standard_deviation(data: List[float]) -> float:
    if len(data) < 2:
        raise ValueError("Need at least 2 data points")
    avg = mean(data)
    variance = sum((x - avg) ** 2 for x in data) / (len(data) - 1)
    return math.sqrt(variance)


def z_score(value: float, data: List[float]) -> float:
    avg = mean(data)
    std = standard_deviation(data)
    if std == 0:
        raise ValueError("Standard deviation is zero")
    return (value - avg) / std
''')

    # tests/__init__.py
    with open(os.path.join(TESTS_DIR, '__init__.py'), 'w') as f:
        f.write('')

    # tests/test_calculator.py
    with open(os.path.join(TESTS_DIR, 'test_calculator.py'), 'w') as f:
        f.write('''"""Tests for the Calculator class."""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from calculator import Calculator


class TestCalculator:
    def setup_method(self):
        self.calc = Calculator()

    def test_add(self):
        assert self.calc.add(3, 5) == 8
        assert self.calc.add(-1, 1) == 0

    def test_subtract(self):
        assert self.calc.subtract(10, 4) == 6

    def test_multiply(self):
        assert self.calc.multiply(3, 7) == 21

    def test_divide(self):
        assert self.calc.divide(10, 2) == 5.0

    def test_divide_by_zero(self):
        with pytest.raises(ValueError):
            self.calc.divide(5, 0)

    def test_memory(self):
        self.calc.store_in_memory(42.0)
        assert self.calc.recall_memory() == 42.0

    def test_history(self):
        self.calc.add(1, 2)
        self.calc.subtract(5, 3)
        assert len(self.calc.history) == 2
        self.calc.clear_history()
        assert len(self.calc.history) == 0
''')

    # tests/test_statistics.py
    with open(os.path.join(TESTS_DIR, 'test_statistics.py'), 'w') as f:
        f.write('''"""Tests for statistical utility functions."""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from statistics_utils import mean, median, standard_deviation, z_score


class TestStatistics:
    def test_mean(self):
        assert mean([1, 2, 3, 4, 5]) == 3.0

    def test_mean_empty(self):
        with pytest.raises(ValueError):
            mean([])

    def test_median_odd(self):
        assert median([1, 3, 5]) == 3

    def test_median_even(self):
        assert median([1, 2, 3, 4]) == 2.5

    def test_standard_deviation(self):
        result = standard_deviation([2, 4, 4, 4, 5, 5, 7, 9])
        assert abs(result - 2.0) < 0.1

    def test_z_score(self):
        data = [10, 20, 30, 40, 50]
        z = z_score(30, data)
        assert abs(z) < 0.001  # mean value should have z-score ~0
''')

    # requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('''pytest>=7.0.0
pytest-cov>=4.0.0
''')

    # README.md
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('''# CS301 Project - Calculator & Statistics Library

A Python library implementing basic calculator operations and statistical
analysis functions for the CS301 Data Structures course.

## Setup

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
python3 -m pytest tests/
```

## Project Structure

- `src/calculator.py` - Calculator class with memory
- `src/statistics_utils.py` - Statistical functions
- `tests/` - Unit tests
''')

    print(f'Initial project created at: {PROJECT_DIR}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
