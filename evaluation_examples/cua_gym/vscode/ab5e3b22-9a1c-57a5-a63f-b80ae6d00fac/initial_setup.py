"""
Initial Setup: Terraform infrastructure development workflow in ~/project
Task ID: vscode_wf_087
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_087'
PROJECT_DIR = os.path.join(WORKDIR, 'project')


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
    print(f'Created project directory: {PROJECT_DIR}')

    # Ensure no terraform extension is installed (remove if present)
    subprocess.run(
        ["code", "--uninstall-extension", "hashicorp.terraform"],
        capture_output=True, text=True
    )
    print('Ensured hashicorp.terraform extension is not installed')

    # Launch VSCode with the empty project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0 on ~/project')


create_initial()
