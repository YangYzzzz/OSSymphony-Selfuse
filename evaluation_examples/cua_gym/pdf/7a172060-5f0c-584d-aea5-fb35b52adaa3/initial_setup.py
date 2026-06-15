"""
Initial Setup: Create finance directory for PDF report creation task.
Task ID: pdf_fin_016
Domain: pdf

The agent needs to create a multi-page financial summary report PDF.
Initial state: /home/user/finance/ directory exists, no PDF yet.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_016'
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

    # Open file manager to the finance directory so agent can see the workspace
    launch_gui(f'nautilus "{FINANCE_DIR}"', delay_sec=2.0)

    print('GUI_READY: launched file manager with DISPLAY=:0')

create_initial()
