"""
Initial Setup: Full-stack Todo project with empty client/ and server/ directories
Task ID: vscode_gf4_028
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_028'
PROJECT_DIR = f'{WORKDIR}/projects/full-stack-todo'

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
    # Create the project directory with empty client/ and server/ subdirectories
    os.makedirs(f'{PROJECT_DIR}/client', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/server', exist_ok=True)

    print(f'Initial project structure created at: {PROJECT_DIR}')
    print(f'  - client/ (empty)')
    print(f'  - server/ (empty)')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
