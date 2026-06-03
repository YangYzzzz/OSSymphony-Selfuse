"""
Initial Setup: Create finance directory for credit memo task
Task ID: pdf_fin_087
Domain: pdf

The task asks the agent to CREATE a credit memo PDF.
Initial state: only the /home/user/finance/ directory exists (empty).
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_087'
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
    print(f'Finance directory created: {FINANCE_DIR}')

    # Open a terminal in the finance directory so the agent can work
    launch_gui(f'nautilus "{FINANCE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')

create_initial()
