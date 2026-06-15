"""
Initial Setup: Python CLI Framework project scaffold
Task ID: vscode_gf4_065
Domain: vscode

Creates ~/projects/python-cli-framework with:
- src/__init__.py
- commands/example.yml (showing expected YAML format)
No virtual environment, no framework code.
Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_065'
PROJECT_DIR = f'{WORKDIR}/projects/python-cli-framework'

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
    os.makedirs(f'{PROJECT_DIR}/commands', exist_ok=True)

    # Create src/__init__.py (empty package init)
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('"""Python CLI Framework - Source Package."""\n')

    # Create commands/example.yml showing the expected YAML format
    example_yml = """# Example CLI Command Definition
# This file demonstrates the expected YAML format for command definitions.
# Create your own command YAML files in this directory.

name: greet
description: "Greet a user by name"
parameters:
  - name: username
    type: string
    required: true
    default: null
    help: "The name of the person to greet"
  - name: greeting
    type: string
    required: false
    default: "Hello"
    help: "The greeting phrase to use"
  - name: loud
    type: bool
    required: false
    default: false
    help: "Whether to shout the greeting in uppercase"
"""
    with open(f'{PROJECT_DIR}/commands/example.yml', 'w') as f:
        f.write(example_yml)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  - src/__init__.py')
    print(f'  - commands/example.yml')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
