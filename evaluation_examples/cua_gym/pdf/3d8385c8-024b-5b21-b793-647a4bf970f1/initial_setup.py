"""
Initial Setup: Prepare environment for PDF report creation task.
Task ID: pdf_mbc_090
Domain: pdf

The task asks the agent to CREATE a PDF report using Python reportlab.
Initial state: ~/Documents/ directory exists, no PDF file yet.
A terminal is opened so the agent can write and run a Python script.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_090'
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
    # Ensure ~/Documents/ directory exists
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    # Make sure no pre-existing system_report.pdf exists
    target_path = os.path.join(DOCUMENTS_DIR, 'system_report.pdf')
    if os.path.exists(target_path):
        os.remove(target_path)

    # Install reportlab so the agent can use it
    subprocess.run(
        ['pip3', 'install', 'reportlab'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print(f'Initial environment prepared: {DOCUMENTS_DIR} exists, no system_report.pdf')

    # Open a terminal for the agent to write and execute Python code
    launch_gui('bash -c "DISPLAY=:0 gnome-terminal"', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')

create_initial()
