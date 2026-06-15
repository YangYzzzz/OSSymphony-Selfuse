"""
Initial Setup: Create /home/user/finance/ directory for depreciation schedule task.
Task ID: pdf_fin_048
Domain: pdf

The agent's task is to CREATE the depreciation schedule PDF from scratch.
Initial state: only the empty directory exists, no PDF yet.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_048'
FINANCE_DIR = f'{WORKDIR}/finance'

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
    # Create the finance directory
    os.makedirs(FINANCE_DIR, exist_ok=True)
    print(f'Directory created: {FINANCE_DIR}')

    # Open file manager showing the finance directory so the agent can see
    # the working directory where the PDF should be created
    launch_gui(f'nautilus "{FINANCE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')

create_initial()
