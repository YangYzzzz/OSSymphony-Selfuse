"""
Initial Setup: Scaffold a Python package 'datatools' in ~/projects/python-scaffold
Task ID: vscode_gf6_001
Domain: vs_code

Initial state: Empty ~/projects/python-scaffold folder with VSCode open on it.
No project files exist yet - the agent will create them.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_001'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'python-scaffold')


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
    # Create the empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created empty project directory: {PROJECT_DIR}')

    # Verify no files exist (clean state)
    contents = os.listdir(PROJECT_DIR)
    if contents:
        print(f'WARNING: Project directory not empty: {contents}')
    else:
        print('Project directory is empty as expected.')

    # Launch VSCode with the project folder (GUI-ready state)
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0 on ~/projects/python-scaffold')


create_initial()
