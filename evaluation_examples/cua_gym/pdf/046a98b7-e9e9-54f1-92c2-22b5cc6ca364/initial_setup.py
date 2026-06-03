"""
Initial Setup: Empty Desktop for PDF form creation task
Task ID: pdf_cr_018
Domain: pdf

The agent must create a PDF form from scratch on an empty Desktop.
Initial state: Empty Desktop with a file manager open showing the Desktop folder.
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
    # Ensure Desktop directory exists and is clean of any prior application.pdf
    os.makedirs(DESKTOP, exist_ok=True)
    target = os.path.join(DESKTOP, 'application.pdf')
    if os.path.exists(target):
        os.remove(target)

    print(f'Desktop is ready (empty): {DESKTOP}')
    print(f'No application.pdf exists: {not os.path.exists(target)}')

    # Open file manager showing the Desktop for visual context
    launch_gui(f'nautilus "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
