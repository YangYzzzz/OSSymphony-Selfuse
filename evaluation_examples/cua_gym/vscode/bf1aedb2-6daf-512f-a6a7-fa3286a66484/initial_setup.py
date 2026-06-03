"""
Initial Setup: VSCode with empty python-plugin-system project
Task ID: vscode_gf4_043
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_043'
PROJECT_DIR = f'{WORKDIR}/projects/python-plugin-system'


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
    os.makedirs(f'{PROJECT_DIR}/src/core', exist_ok=True)

    # Create src/__init__.py
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('"""Python Plugin System package."""\n')

    # Create src/core/__init__.py
    with open(f'{PROJECT_DIR}/src/core/__init__.py', 'w') as f:
        f.write('"""Core module for the plugin system."""\n')

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files: src/__init__.py, src/core/__init__.py')

    # Open VSCode with project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
