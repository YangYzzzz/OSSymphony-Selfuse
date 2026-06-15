"""
Initial Setup: Create empty environment for PDF creation task
Task ID: pdf_res_007
Domain: pdf

The agent's task is to CREATE the PDF from scratch, so the initial state
has no PDF file - only the target directory and an open file manager.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_007'
OUTPUT_DIR = f'{WORKDIR}/papers'


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
    # Create the target directory so the agent knows where to save
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Ensure no PDF exists at the target path (clean state)
    target = f'{OUTPUT_DIR}/draft_paper.pdf'
    if os.path.exists(target):
        os.remove(target)

    print(f'Initial environment prepared: directory {OUTPUT_DIR} created')
    print(f'No PDF at {target} (agent must create it)')

    # Open file manager at the papers directory so agent sees the workspace
    launch_gui(f'nautilus "{OUTPUT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
