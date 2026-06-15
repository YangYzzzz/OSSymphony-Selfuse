"""
Initial Setup: Create environment for PDF creation task
Task ID: pdf_gf2_040
Domain: pdf

The task asks the agent to create a PDF from scratch at /home/user/Documents/summary_sheet.pdf.
Initial state: No PDF exists. We ensure the Documents directory exists and open a terminal
so the agent can write and run a Python script using reportlab.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_040'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'

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
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    print(f'Documents directory ensured: {DOCUMENTS_DIR}')

    # Verify the target file does NOT exist (clean state)
    target = f'{DOCUMENTS_DIR}/summary_sheet.pdf'
    if os.path.exists(target):
        os.remove(target)
        print(f'Removed pre-existing file: {target}')

    # Open a terminal for the agent to write and run scripts
    launch_gui('bash -c "DISPLAY=:0 gnome-terminal"', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')

create_initial()
