"""
Initial Setup: Prepare environment for PDF checklist creation task
Task ID: pdf_adv_181
Domain: pdf

The task asks the agent to CREATE ~/Documents/checklist.pdf.
Initial state: the file does NOT exist. We only ensure ~/Documents exists
and open a file manager pointing there so the agent knows where to work.
"""

import os
import shlex
import subprocess
import time


WORKDIR = '/home/user'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'


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
    # Ensure ~/Documents directory exists
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    print(f'Documents directory ready: {DOCUMENTS_DIR}')

    # Do NOT create checklist.pdf -- the task is for the agent to create it
    # Verify it does not exist
    target = os.path.join(DOCUMENTS_DIR, 'checklist.pdf')
    if os.path.exists(target):
        os.remove(target)
        print(f'Removed pre-existing {target} to ensure clean initial state')

    # Open file manager at ~/Documents so the agent sees the workspace
    launch_gui(f'nautilus "{DOCUMENTS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')


create_initial()
