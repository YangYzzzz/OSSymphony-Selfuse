"""
Initial Setup: VSCode project scaffolding workflow
Task ID: vscode_wf_067
Domain: vscode

Creates an empty initial state: VSCode open, no ~/project directory.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'

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
    # Ensure ~/project does NOT exist (clean slate)
    project_dir = os.path.join(WORKDIR, 'project')
    if os.path.exists(project_dir):
        import shutil
        shutil.rmtree(project_dir)
        print(f'Removed existing {project_dir}')

    print('Initial state: ~/project does not exist (clean slate)')

    # Launch VSCode (just the editor, no specific folder)
    launch_gui('code', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
