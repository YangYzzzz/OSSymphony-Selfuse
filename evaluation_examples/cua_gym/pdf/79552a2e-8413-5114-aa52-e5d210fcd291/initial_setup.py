"""
Initial Setup: Create blank environment for PDF note-taking page generation task.
Task ID: pdf_res_042
Domain: pdf

Initial state: No PDF file exists. The /home/user/papers/ directory is created
so the agent has a target location. Evince or file manager is not opened since
there is no file to open yet.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_042'
PAPERS_DIR = f'{WORKDIR}/papers'


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
    # Ensure the papers directory exists so the agent can save there
    os.makedirs(PAPERS_DIR, exist_ok=True)
    print(f'Created directory: {PAPERS_DIR}')

    # Verify no PDF exists at the target path
    target = f'{PAPERS_DIR}/seminar_notes.pdf'
    if os.path.exists(target):
        os.remove(target)
        print(f'Removed existing file: {target}')

    print('Initial state ready: no PDF at target path, papers/ directory exists.')

    # Open file manager showing the papers directory so the agent sees the workspace
    launch_gui(f'nautilus "{PAPERS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')


create_initial()
