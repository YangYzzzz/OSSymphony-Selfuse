"""
Initial Setup: Create empty terraform-infra workspace and open VSCode
Task ID: vscode_ops_044
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_044'
WORKSPACE = f'{WORKDIR}/terraform-infra'


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
    # Create the empty workspace directory
    os.makedirs(WORKSPACE, exist_ok=True)
    print(f'Workspace directory created: {WORKSPACE}')

    # Verify it's empty (no .tf files should exist)
    existing = os.listdir(WORKSPACE)
    if existing:
        print(f'WARNING: Workspace not empty, contains: {existing}')
    else:
        print('Workspace is empty as expected.')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
