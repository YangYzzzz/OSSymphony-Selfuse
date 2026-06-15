"""
Initial Setup: Create empty project workspace for VSCode
Task ID: vscode_wf_003
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_003'
PROJECT_DIR = f'{WORKDIR}/project'


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
    # Create empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Project directory created: {PROJECT_DIR}')

    # Ensure no hello.py exists (clean state)
    hello_path = os.path.join(PROJECT_DIR, 'hello.py')
    if os.path.exists(hello_path):
        os.remove(hello_path)

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
