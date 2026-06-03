"""
Initial Setup: Create empty Desktop state for budget PDF creation task
Task ID: pdf_cr_031
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_031'
DESKTOP = f'{WORKDIR}/Desktop'

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
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any pre-existing budget.pdf to ensure clean state
    budget_path = os.path.join(DESKTOP, 'budget.pdf')
    if os.path.exists(budget_path):
        os.remove(budget_path)

    print(f'Initial state prepared: empty Desktop at {DESKTOP}')

    # Open file manager showing Desktop so agent can see the empty state
    launch_gui(f'nautilus "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')

create_initial()
