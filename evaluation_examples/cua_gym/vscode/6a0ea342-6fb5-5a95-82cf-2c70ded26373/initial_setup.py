"""
Initial Setup: Data science workspace in ~/project (empty state)
Task ID: vscode_wf_071
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')

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
    os.makedirs(PROJECT, exist_ok=True)
    print(f"Created empty project directory: {PROJECT}")

    # Launch VSCode with the empty project folder
    launch_gui(f'code "{PROJECT}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with ~/project on DISPLAY=:0")

create_initial()
