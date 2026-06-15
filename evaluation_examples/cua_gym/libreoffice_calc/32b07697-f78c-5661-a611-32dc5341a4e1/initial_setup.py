"""
Initial Setup: Create finance directory for general ledger summary PDF task
Task ID: pdf_fin_061
Domain: pdf (reportlab)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_061'
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

    # Open file manager to show the finance directory
    launch_gui(f'nautilus "{FINANCE_DIR}"', delay_sec=2.0)

    print('GUI_READY: launched file manager with DISPLAY=:0')

create_initial()
