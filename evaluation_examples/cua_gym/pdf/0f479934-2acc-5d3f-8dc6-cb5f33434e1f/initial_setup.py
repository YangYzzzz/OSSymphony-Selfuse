"""
Initial Setup: Create the /home/user/legal/ directory for the privilege log task.
Task ID: pdf_legal_093
Domain: pdf

The task asks the agent to CREATE a privilege log PDF from scratch.
Initial state: directory exists, no PDF file present.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
LEGAL_DIR = f'{WORKDIR}/legal'

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
    # Ensure the legal directory exists
    os.makedirs(LEGAL_DIR, exist_ok=True)
    print(f'Directory created: {LEGAL_DIR}')

    # Verify no privilege_log.pdf exists (clean state)
    target_pdf = os.path.join(LEGAL_DIR, 'privilege_log.pdf')
    if os.path.exists(target_pdf):
        os.remove(target_pdf)
        print(f'Removed pre-existing file: {target_pdf}')

    # Open a terminal in the legal directory so the agent has context
    launch_gui('nautilus /home/user/legal', delay_sec=2.0)
    print('GUI_READY: launched nautilus file manager with DISPLAY=:0')

create_initial()
