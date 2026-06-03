"""
Initial Setup: Open VSCode with python-async-patterns project skeleton
Task ID: vscode_gf6_076
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_076'
PROJECT_DIR = f'{WORKDIR}/projects/python-async-patterns'

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
    os.makedirs(f'{PROJECT_DIR}/src/patterns', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)

    # Create src/patterns/__init__.py
    with open(f'{PROJECT_DIR}/src/patterns/__init__.py', 'w') as f:
        f.write('"""Async patterns library."""\n')

    # Create src/__init__.py
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('')

    # Create tests/__init__.py
    with open(f'{PROJECT_DIR}/tests/__init__.py', 'w') as f:
        f.write('')

    # Create a basic pyproject.toml
    with open(f'{PROJECT_DIR}/pyproject.toml', 'w') as f:
        f.write("""[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "python-async-patterns"
version = "0.1.0"
description = "Advanced async design patterns for Python"
requires-python = ">=3.11"

[project.optional-dependencies]
dev = ["pytest", "pytest-asyncio"]
""")

    # Create a README
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# Python Async Patterns

A collection of advanced asynchronous design patterns for Python 3.11+.

## Patterns

- **Throttle / Rate Limiter** - Control concurrency with token bucket algorithm
- **Retry with Backoff** - Exponential backoff retry decorator for async functions
- **Circuit Breaker** - Prevent cascading failures with state machine pattern

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install pytest pytest-asyncio
```

## Running Tests

```bash
pytest tests/ -v
```
""")

    # Create basic .vscode/settings.json (NO asyncio-mode config)
    vscode_settings = {
        "python.defaultInterpreterPath": f"{PROJECT_DIR}/venv/bin/python",
        "editor.formatOnSave": True,
        "python.analysis.typeCheckingMode": "basic"
    }
    with open(f'{PROJECT_DIR}/.vscode/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # Install pytest and pytest-asyncio system-wide
    subprocess.run(
        ['pip3', 'install', 'pytest', 'pytest-asyncio'],
        check=True, capture_output=True
    )

    # Create virtual environment with system site packages
    subprocess.run(
        ['python3', '-m', 'venv', '--without-pip', '--system-site-packages',
         f'{PROJECT_DIR}/venv'],
        check=True, capture_output=True
    )
    print(f'Virtual environment created with pytest and pytest-asyncio')

    print(f'Initial project created: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
