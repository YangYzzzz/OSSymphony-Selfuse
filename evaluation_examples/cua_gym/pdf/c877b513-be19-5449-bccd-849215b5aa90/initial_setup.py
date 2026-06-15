"""
Initial Setup: Empty Desktop for two-column PDF creation task
Task ID: pdf_cr_014
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_014'
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

    # Remove any pre-existing two_column.pdf to ensure clean state
    target = os.path.join(DESKTOP, 'two_column.pdf')
    if os.path.exists(target):
        os.remove(target)

    print(f'Initial state: Desktop is clean, no two_column.pdf exists')

    # Open file manager showing Desktop so the agent can see the empty state
    launch_gui(f'nautilus "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')

create_initial()
