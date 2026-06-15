"""
Initial Setup: Create empty Desktop state for conference agenda PDF task
Task ID: pdf_cr_036
Domain: pdf

The agent's task is to CREATE agenda.pdf from scratch on the Desktop.
Initial state: Empty Desktop, no agenda.pdf present.
"""

import os
import shlex
import subprocess
import time


WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_036'
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

    # Remove any pre-existing agenda.pdf to guarantee clean state
    agenda_path = os.path.join(DESKTOP, 'agenda.pdf')
    if os.path.exists(agenda_path):
        os.remove(agenda_path)

    print(f'Initial state prepared: empty Desktop at {DESKTOP}')
    print(f'Verified agenda.pdf does NOT exist: {not os.path.exists(agenda_path)}')

    # Open file manager showing the Desktop so the agent sees the empty state
    launch_gui(f'nautilus "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')


create_initial()
