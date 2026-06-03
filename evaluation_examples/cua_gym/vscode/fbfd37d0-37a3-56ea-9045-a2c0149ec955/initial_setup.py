"""
Initial Setup: Set up background task processing with APScheduler in VSCode
Task ID: vscode_gf6_094
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_094'
PROJECT_DIR = f'{WORKDIR}/projects/python-background-tasks'

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

    # Create src/__init__.py (empty)
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('')

    # Create a basic pyproject.toml for the project
    with open(f'{PROJECT_DIR}/pyproject.toml', 'w') as f:
        f.write('''[project]
name = "python-background-tasks"
version = "0.1.0"
description = "Background task processing service"
requires-python = ">=3.11"
dependencies = [
    "structlog",
]

[project.optional-dependencies]
dev = [
    "pytest",
]
''')

    # Create a basic README
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('''# Python Background Tasks

A background task processing service using Python.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Project Structure

```
src/
    __init__.py
```
''')

    # Create requirements.txt with only structlog
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('structlog>=24.1.0\n')

    # Install virtualenv (python3-venv may not be available)
    subprocess.run(
        ['pip3', 'install', '--user', 'virtualenv'],
        capture_output=True,
    )

    # Create virtual environment using virtualenv and install structlog only
    subprocess.run(
        ['/home/user/.local/bin/virtualenv', f'{PROJECT_DIR}/venv'],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [f'{PROJECT_DIR}/venv/bin/pip', 'install', 'structlog'],
        check=True,
        capture_output=True,
    )

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Contents:')
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Skip venv internals for readability
        if 'venv' in root.split(os.sep):
            continue
        level = root.replace(PROJECT_DIR, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

    # GUI-ready startup: open VSCode with project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
