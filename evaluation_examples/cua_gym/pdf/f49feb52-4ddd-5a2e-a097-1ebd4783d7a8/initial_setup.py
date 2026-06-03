"""
Initial Setup: Empty desktop for PDF cover page creation task
Task ID: pdf_cr_038
Domain: pdf

The agent must create /home/user/Desktop/cover_page.pdf from scratch.
Initial state: empty Desktop, no pre-existing PDF.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
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
    # Ensure Desktop directory exists and is clean of any cover_page.pdf
    os.makedirs(DESKTOP, exist_ok=True)
    target = os.path.join(DESKTOP, 'cover_page.pdf')
    if os.path.exists(target):
        os.remove(target)

    print(f'Initial state: Desktop is clean, no cover_page.pdf')

    # Open file manager so the agent can see the empty Desktop
    launch_gui('nautilus "/home/user/Desktop"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')

create_initial()
