"""
Initial Setup: VSCode gRPC Protocol Buffer project skeleton
Task ID: vscode_gf4_059
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_059'
PROJECT_DIR = f'{WORKDIR}/projects/python-protocol-buffer'

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
    os.makedirs(f'{PROJECT_DIR}/protos', exist_ok=True)

    # Create src/__init__.py (empty)
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('')

    print(f'Initial project structure created at: {PROJECT_DIR}')
    print(f'  src/__init__.py (empty)')
    print(f'  protos/ (empty directory)')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
