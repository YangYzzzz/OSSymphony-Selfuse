"""
Initial Setup: Create workspace for Jupyter notebook visualization task
Task ID: vscode_prod_026
Domain: vscode (Jupyter notebook)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_026'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'visualization')


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
    # Create the workspace directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created workspace directory: {PROJECT_DIR}')

    # Verify no notebook exists
    nb_path = os.path.join(WORKDIR, f'{TASK_ID}.ipynb')
    if os.path.exists(nb_path):
        os.remove(nb_path)
        print(f'Removed existing notebook: {nb_path}')

    # Open VSCode with the workspace folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
