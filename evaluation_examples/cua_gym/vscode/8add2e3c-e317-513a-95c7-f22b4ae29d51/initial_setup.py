"""
Initial Setup: Configure VSCode with pytest for python-tests project
Task ID: vscode_gf4_010
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_010'
PROJECT_DIR = f'{WORKDIR}/projects/python-tests'
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

    # Create src/utils.py with the add function
    utils_content = '''\
"""Utility functions for the python-tests project."""


def add(a, b):
    """Return the sum of two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        The sum of a and b.
    """
    return a + b


def multiply(a, b):
    """Return the product of two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        The product of a and b.
    """
    return a * b


def subtract(a, b):
    """Return the difference of two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        a minus b.
    """
    return a - b
'''
    with open(f'{SRC_DIR}/utils.py', 'w') as f:
        f.write(utils_content)

    # Create src/__init__.py to make it a package
    with open(f'{SRC_DIR}/__init__.py', 'w') as f:
        f.write('')

    # Create a basic README for the project
    readme_content = '''\
# Python Tests Project

A sample Python project for demonstrating pytest integration with VSCode.

## Project Structure

```
python-tests/
├── src/
│   ├── __init__.py
│   └── utils.py
└── README.md
```

## Getting Started

Install dependencies:

```bash
pip install pytest
```

## Usage

```python
from src.utils import add, multiply, subtract

result = add(3, 5)  # Returns 8
```
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme_content)

    # Ensure NO .vscode directory exists (task asks agent to create it)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    # Ensure NO tests directory exists (task asks agent to create it)
    tests_dir = f'{PROJECT_DIR}/tests'
    if os.path.exists(tests_dir):
        import shutil
        shutil.rmtree(tests_dir)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  src/utils.py: add(), multiply(), subtract()')
    print(f'  No .vscode/ directory')
    print(f'  No tests/ directory')

    # Install pytest (task says Python and pytest are installed)
    subprocess.run(['pip3', 'install', 'pytest', '-q'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('Installed pytest')

    # GUI-ready startup: Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
