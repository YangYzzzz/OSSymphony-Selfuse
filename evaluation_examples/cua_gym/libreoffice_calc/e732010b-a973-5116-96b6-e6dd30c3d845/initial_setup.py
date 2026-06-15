"""
Initial Setup: Development workspace setup task
Task ID: osworld_multi_apps_sys_config_008
Domain: os

Creates the initial state: /home/user/workspace/ exists but is empty.
The agent is expected to build the full project directory structure,
initialize git, create a venv, install packages, write scripts, etc.
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
WORKSPACE = '/home/user/workspace'


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
    # Ensure /home/user/workspace exists and is empty
    # If myproject already exists from a previous run, remove it to reset state
    myproject = os.path.join(WORKSPACE, 'myproject')
    if os.path.exists(myproject):
        import shutil
        shutil.rmtree(myproject)
        print(f'Removed existing myproject directory to reset state.')

    # Create workspace directory (should already exist per task context)
    os.makedirs(WORKSPACE, exist_ok=True)
    print(f'Workspace directory ensured: {WORKSPACE}')
    print(f'Initial state: {WORKSPACE} exists and is empty (no myproject subdir).')

    # Verify workspace is now empty of myproject
    contents = os.listdir(WORKSPACE)
    print(f'Workspace contents: {contents}')

    # Open a file manager showing the workspace so agent can see it
    launch_gui(f'nautilus "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager at /home/user/workspace with DISPLAY=:0')


create_initial()
