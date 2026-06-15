"""
Initial Setup: Create directory structure for receipt template PDF task
Task ID: pdf_pw_033
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_033'
FORMS_DIR = f'{WORKDIR}/forms'

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
    # Create the forms directory
    os.makedirs(FORMS_DIR, exist_ok=True)
    print(f'Directory created: {FORMS_DIR}')

    # Verify no receipt_template.pdf exists
    target = os.path.join(FORMS_DIR, 'receipt_template.pdf')
    if os.path.exists(target):
        os.remove(target)
        print(f'Removed pre-existing file: {target}')

    # Open file manager to show the forms directory
    launch_gui(f'nautilus "{FORMS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched file manager with DISPLAY=:0')

create_initial()
