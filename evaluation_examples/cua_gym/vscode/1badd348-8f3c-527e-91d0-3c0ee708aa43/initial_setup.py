"""
Initial Setup: Open VSCode with ~/projects/python-orm-framework containing only src/__init__.py and tests/__init__.py
Task ID: vscode_gf4_046
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_046'
PROJECT_DIR = f'{WORKDIR}/projects/python-orm-framework'

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

    # Create minimal __init__.py files
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('# Python ORM Framework - Source Package\n')

    with open(f'{PROJECT_DIR}/tests/__init__.py', 'w') as f:
        f.write('# Python ORM Framework - Tests Package\n')

    print(f'Project structure created at: {PROJECT_DIR}')
    print(f'  src/__init__.py')
    print(f'  tests/__init__.py')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
