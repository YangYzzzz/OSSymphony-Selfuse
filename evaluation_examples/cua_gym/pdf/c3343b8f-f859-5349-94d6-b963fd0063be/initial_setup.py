"""
Initial Setup: Create empty forms directory for employee survey PDF creation task.
Task ID: pdf_gf3_011
Domain: pdf

The agent must create /home/user/forms/employee_survey.pdf from scratch.
Initial state: the directory exists but the PDF does NOT exist.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_011'
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
    # Create the forms directory (the PDF does NOT exist yet - the agent must create it)
    os.makedirs(FORMS_DIR, exist_ok=True)
    print(f'Created directory: {FORMS_DIR}')

    # Verify the PDF does NOT exist
    pdf_path = f'{FORMS_DIR}/employee_survey.pdf'
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        print(f'Removed pre-existing PDF: {pdf_path}')

    # Open a file manager showing the forms directory so the agent can see the workspace
    launch_gui(f'nautilus "{FORMS_DIR}"', delay_sec=1.5)

    # Also open a terminal in the forms directory for the agent to use
    launch_gui(f'bash -c "cd {FORMS_DIR} && gnome-terminal --working-directory={FORMS_DIR}"', delay_sec=1.5)

    print('GUI_READY: launched file manager and terminal with DISPLAY=:0')
    print(f'Initial state: {FORMS_DIR}/ exists, employee_survey.pdf does NOT exist')

create_initial()
