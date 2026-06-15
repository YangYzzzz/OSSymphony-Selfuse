"""
Initial Setup: Create a PDF with table of contents (bookmarks)
Task ID: pdf_cr_019
Domain: pdf
Initial state: Empty Desktop — no PDF exists yet.
The agent must create the PDF from scratch.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_019'
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

    # Remove any pre-existing toc_document.pdf to guarantee clean state
    target = os.path.join(DESKTOP, 'toc_document.pdf')
    if os.path.exists(target):
        os.remove(target)

    print(f'Initial state: empty Desktop at {DESKTOP}')
    print(f'No toc_document.pdf present — agent must create it.')

    # Open file manager on Desktop so the agent sees the empty Desktop
    launch_gui(f'nautilus "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus on Desktop with DISPLAY=:0')


create_initial()
