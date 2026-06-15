"""
Initial Setup: GraphQL API project with Strawberry - pre-task state
Task ID: vscode_gf6_088
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_088'
PROJECT_DIR = f'{WORKDIR}/projects/python-graphql'

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

    # Create empty __init__.py files
    open(f'{PROJECT_DIR}/src/__init__.py', 'w').close()
    open(f'{PROJECT_DIR}/tests/__init__.py', 'w').close()

    # Create requirements.txt (without strawberry - that's what the agent needs to add)
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write("fastapi==0.109.2\nuvicorn==0.27.1\n")

    # Create a basic pyproject.toml
    with open(f'{PROJECT_DIR}/pyproject.toml', 'w') as f:
        f.write("""[project]
name = "python-graphql"
version = "0.1.0"
description = "A GraphQL API built with Strawberry and FastAPI"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn>=0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
]
""")

    # Create a README
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# Python GraphQL API

A GraphQL API project using FastAPI.

## Setup

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
uvicorn src.main:app --reload
```
""")

    # Create .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""venv/
__pycache__/
*.pyc
.env
.pytest_cache/
*.egg-info/
dist/
build/
""")

    # Create virtualenv with fastapi and uvicorn installed (but NOT strawberry-graphql)
    print("Installing virtualenv package...")
    subprocess.run(
        ['pip3', 'install', 'virtualenv'],
        capture_output=True
    )
    print("Creating virtual environment...")
    subprocess.run(
        ['python3', '-m', 'virtualenv', f'{PROJECT_DIR}/venv'],
        check=True
    )
    print("Installing fastapi and uvicorn...")
    subprocess.run(
        [f'{PROJECT_DIR}/venv/bin/pip', 'install', 'fastapi==0.109.2', 'uvicorn==0.27.1'],
        check=True,
        capture_output=True
    )
    print("Verifying strawberry-graphql is NOT installed...")
    result = subprocess.run(
        [f'{PROJECT_DIR}/venv/bin/pip', 'list'],
        capture_output=True, text=True
    )
    assert 'strawberry' not in result.stdout.lower(), "strawberry should not be pre-installed"
    print("Initial environment ready.")

    print(f'Initial project created: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
