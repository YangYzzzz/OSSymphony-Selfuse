"""
Initial Setup: Prepare environment for PDF report creation task
Task ID: pdf_gf1_040
Domain: pdf

Initial state: /home/user/Documents/ directory exists, no output file.
The agent must create the PDF from scratch.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_040'
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
    # Ensure the Documents directory exists
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    # Remove any pre-existing output file to guarantee clean state
    output_path = f'{DOCUMENTS_DIR}/generated_report.pdf'
    if os.path.exists(output_path):
        os.remove(output_path)

    print(f'Initial state prepared: {DOCUMENTS_DIR}/ exists, no generated_report.pdf')

    # Open a file manager so the agent has a GUI-ready starting point
    launch_gui(f'nautilus "{DOCUMENTS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')

create_initial()
