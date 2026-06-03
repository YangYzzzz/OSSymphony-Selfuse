"""
Initial Setup: Install Python Test Explorer, create pytest config, and run tests with coverage
Task ID: vscode_stu_082
Domain: vs_code

Creates a Python project with src/calculator.py and tests/test_calculator.py.
VSCode is opened with the project. No test explorer extension, no pytest config,
no coverage config -- those are the task for the agent to set up.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_082'
PROJECT_DIR = f'{WORKDIR}/workspace'
SRC_DIR = f'{PROJECT_DIR}/src'
TESTS_DIR = f'{PROJECT_DIR}/tests'
VSCODE_USER = f'{WORKDIR}/.config/Code/User'
SETTINGS_PATH = f'{VSCODE_USER}/settings.json'


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

    # Create src/__init__.py
    with open(f'{SRC_DIR}/__init__.py', 'w') as f:
        f.write('')

    # Create tests/__init__.py
    with open(f'{TESTS_DIR}/__init__.py', 'w') as f:
        f.write('')

    # Create src/calculator.py - a realistic calculator module
    calculator_content = '''"""
Calculator module for basic and advanced arithmetic operations.
Used in CS201 Introduction to Software Testing course.
"""


class Calculator:
    """A calculator class supporting basic arithmetic and memory operations."""

    def __init__(self):
        self.memory = 0.0
        self.history = []

    def add(self, a, b):
        """Return the sum of two numbers."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a, b):
        """Return the difference of two numbers."""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def multiply(self, a, b):
        """Return the product of two numbers."""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

    def divide(self, a, b):
        """Return the quotient of two numbers. Raises ValueError on division by zero."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result

    def power(self, base, exponent):
        """Return base raised to the exponent."""
        result = base ** exponent
        self.history.append(f"{base} ^ {exponent} = {result}")
        return result

    def modulo(self, a, b):
        """Return the remainder of a divided by b."""
        if b == 0:
            raise ValueError("Cannot compute modulo with zero divisor")
        result = a % b
        self.history.append(f"{a} % {b} = {result}")
        return result

    def store_in_memory(self, value):
        """Store a value in calculator memory."""
        self.memory = value

    def recall_memory(self):
        """Recall the value stored in memory."""
        return self.memory

    def clear_memory(self):
        """Clear the calculator memory."""
        self.memory = 0.0

    def get_history(self):
        """Return the list of past calculations."""
        return list(self.history)

    def clear_history(self):
        """Clear the calculation history."""
        self.history = []
'''
    with open(f'{SRC_DIR}/calculator.py', 'w') as f:
        f.write(calculator_content)

    # Create tests/test_calculator.py - test file covering basic operations
    test_content = '''"""
Tests for the Calculator module.
CS201 - Introduction to Software Testing
"""

import sys
import os
import pytest

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from calculator import Calculator


@pytest.fixture
def calc():
    """Create a fresh Calculator instance for each test."""
    return Calculator()


class TestBasicArithmetic:
    """Test basic arithmetic operations."""

    def test_add_positive_numbers(self, calc):
        assert calc.add(3, 5) == 8

    def test_add_negative_numbers(self, calc):
        assert calc.add(-3, -5) == -8

    def test_add_mixed_numbers(self, calc):
        assert calc.add(-3, 5) == 2

    def test_subtract(self, calc):
        assert calc.subtract(10, 4) == 6

    def test_subtract_negative_result(self, calc):
        assert calc.subtract(4, 10) == -6

    def test_multiply(self, calc):
        assert calc.multiply(3, 7) == 21

    def test_multiply_by_zero(self, calc):
        assert calc.multiply(5, 0) == 0

    def test_divide(self, calc):
        assert calc.divide(10, 2) == 5.0

    def test_divide_by_zero(self, calc):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.divide(10, 0)


class TestAdvancedOperations:
    """Test advanced arithmetic operations."""

    def test_power(self, calc):
        assert calc.power(2, 3) == 8

    def test_power_of_zero(self, calc):
        assert calc.power(5, 0) == 1

    def test_modulo(self, calc):
        assert calc.modulo(10, 3) == 1

    def test_modulo_by_zero(self, calc):
        with pytest.raises(ValueError, match="Cannot compute modulo with zero divisor"):
            calc.modulo(10, 0)


class TestMemory:
    """Test memory operations."""

    def test_store_and_recall(self, calc):
        calc.store_in_memory(42.5)
        assert calc.recall_memory() == 42.5

    def test_clear_memory(self, calc):
        calc.store_in_memory(100)
        calc.clear_memory()
        assert calc.recall_memory() == 0.0

    def test_initial_memory_is_zero(self, calc):
        assert calc.recall_memory() == 0.0


class TestHistory:
    """Test calculation history tracking."""

    def test_history_tracks_operations(self, calc):
        calc.add(1, 2)
        calc.subtract(5, 3)
        history = calc.get_history()
        assert len(history) == 2
        assert "1 + 2 = 3" in history[0]

    def test_clear_history(self, calc):
        calc.add(1, 2)
        calc.clear_history()
        assert len(calc.get_history()) == 0
'''
    with open(f'{TESTS_DIR}/test_calculator.py', 'w') as f:
        f.write(test_content)

    # Install pytest and pytest-cov (needed for the task)
    subprocess.run(['pip3', 'install', 'pytest', 'pytest-cov'], capture_output=True)

    # Ensure basic VSCode settings exist (but NO test/coverage config)
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Only set basic Python settings - no test explorer or coverage config
    settings.update({
        "python.defaultInterpreterPath": "/usr/bin/python3",
    })
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'  src/calculator.py: Calculator module with 11 methods')
    print(f'  tests/test_calculator.py: 16 test cases')

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with workspace on DISPLAY=:0')


create_initial()
