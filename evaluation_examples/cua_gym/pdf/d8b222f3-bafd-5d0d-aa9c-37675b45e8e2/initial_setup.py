"""
Initial Setup: Empty Desktop for PDF checklist creation task
Task ID: pdf_cr_037
Domain: pdf

The agent must create checklist.pdf from scratch on the Desktop.
Initial state: Empty Desktop with no checklist file present.
"""

import os
import glob
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
TASK_ID = 'pdf_cr_037'


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

    # Remove any existing checklist.pdf to ensure clean state
    target = os.path.join(DESKTOP, 'checklist.pdf')
    if os.path.exists(target):
        os.remove(target)

    print(f'Initial state prepared: Desktop is clean, no checklist.pdf')

    # Open file manager to show the empty Desktop
    launch_gui('nautilus "/home/user/Desktop"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')


create_initial()
