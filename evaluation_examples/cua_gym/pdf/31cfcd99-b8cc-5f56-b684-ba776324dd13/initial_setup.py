"""
Initial Setup: Empty Desktop for NDA PDF creation task
Task ID: pdf_cr_023
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_023'
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

    # Remove legal_doc.pdf if it exists (ensure clean initial state)
    target = os.path.join(DESKTOP, 'legal_doc.pdf')
    if os.path.exists(target):
        os.remove(target)

    print(f'Initial state: Desktop is empty at {DESKTOP}')

    # Open file manager showing the Desktop so the agent can see the empty state
    launch_gui(f'nautilus "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus with DISPLAY=:0')

create_initial()
