"""
Initial Setup: Prepare empty Desktop for student report card creation task.
Task ID: pdf_cr_035
Domain: pdf

The agent is asked to CREATE a PDF named report_card.pdf on the Desktop.
Initial state: Empty Desktop, file manager open showing Desktop.
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
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any pre-existing report_card.pdf to ensure clean initial state
    target = os.path.join(DESKTOP, 'report_card.pdf')
    if os.path.exists(target):
        os.remove(target)

    print(f'Initial state prepared: empty Desktop at {DESKTOP}')

    # Open file manager showing the Desktop directory
    launch_gui(f'nautilus "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')

create_initial()
