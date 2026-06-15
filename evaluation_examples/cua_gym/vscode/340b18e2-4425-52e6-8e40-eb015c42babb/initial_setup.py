"""
Initial Setup: TypeScript monorepo workspace setup
Task ID: vscode_gf3_092
Domain: vscode

Creates the /home/user/projects/ directory (empty) and opens VSCode on it.
The agent must create the entire ts-monorepo structure from scratch.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECTS_DIR = f'{WORKDIR}/projects'

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
    # Create the projects directory (empty - agent must create ts-monorepo)
    os.makedirs(PROJECTS_DIR, exist_ok=True)
    print(f'Created directory: {PROJECTS_DIR}')

    # Open VSCode with the projects folder
    launch_gui(f'code "{PROJECTS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
