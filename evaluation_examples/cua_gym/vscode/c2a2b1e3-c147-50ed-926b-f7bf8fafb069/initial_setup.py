"""
Initial Setup: VSCode with python-ddd project - bare skeleton
Task ID: vscode_gf6_078
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_078'
PROJECT_DIR = f'{WORKDIR}/projects/python-ddd'

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

    # Create src/__init__.py
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('# Python DDD Project\n')

    # Create a basic pyproject.toml for the project
    with open(f'{PROJECT_DIR}/pyproject.toml', 'w') as f:
        f.write("""[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "python-ddd"
version = "0.1.0"
description = "Domain-Driven Design project for e-commerce"
requires-python = ">=3.10"
dependencies = [
    "sqlalchemy>=2.0",
    "pytest>=7.0",
]
""")

    # Ensure virtualenv is available
    subprocess.run(
        ['pip3', 'install', 'virtualenv'],
        capture_output=True,
    )

    # Create venv with sqlalchemy and pytest
    print("Creating virtual environment...")
    subprocess.run(
        [os.path.expanduser('~/.local/bin/virtualenv'), f'{PROJECT_DIR}/venv'],
        check=True,
        capture_output=True,
    )

    # Install packages in venv
    pip_path = f'{PROJECT_DIR}/venv/bin/pip'
    subprocess.run(
        [pip_path, 'install', 'sqlalchemy', 'pytest', '-q'],
        check=True,
        capture_output=True,
    )
    print("Installed sqlalchemy and pytest in venv")

    # Create .vscode directory (empty, for the agent to populate)
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)

    print(f'Initial project created: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
