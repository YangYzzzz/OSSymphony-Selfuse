"""
Initial Setup: Prepare environment for PDF cover page creation task.
Task ID: pdf_ro_023
Domain: pdf

The agent's task is to CREATE /home/user/Documents/cover_page.pdf from scratch.
Initial state: /home/user/Documents/ exists, no cover_page.pdf yet.
We open a terminal so the agent can use it to run commands or open tools.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DOCS_DIR = f'{WORKDIR}/Documents'

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
    # Ensure Documents directory exists
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Make sure no cover_page.pdf exists (clean state)
    target = os.path.join(DOCS_DIR, 'cover_page.pdf')
    if os.path.exists(target):
        os.remove(target)

    print(f'Initial state prepared: {DOCS_DIR} exists, no cover_page.pdf')

    # Open file manager showing Documents directory so agent has a visual context
    launch_gui(f'nautilus "{DOCS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')

create_initial()
