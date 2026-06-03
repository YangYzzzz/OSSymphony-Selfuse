"""
Initial Setup: Create the /home/user/finance/ directory for cash flow statement task.
Task ID: pdf_fin_029
Domain: pdf

The agent must create a cash flow statement PDF from scratch.
Initial state: empty finance directory, file manager open.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_029'
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
    # Ensure the finance directory exists
    os.makedirs(FINANCE_DIR, exist_ok=True)
    print(f'Directory created: {FINANCE_DIR}')

    # No PDF file should exist -- the agent's task is to create it
    # Verify it doesn't exist
    target = os.path.join(FINANCE_DIR, 'cashflow_q4_2024.pdf')
    if os.path.exists(target):
        os.remove(target)
        print(f'Removed pre-existing file: {target}')

    # Open file manager to the finance directory so agent sees the workspace
    launch_gui(f'nautilus "{FINANCE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
