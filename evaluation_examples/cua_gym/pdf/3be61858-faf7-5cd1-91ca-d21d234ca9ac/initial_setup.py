"""
Initial Setup: Create directory structure for PDF form creation task
Task ID: pdf_ro_029
Domain: pdf

Initial state: /home/user/forms/ directory exists. No survey.pdf exists yet.
The agent must create the PDF form from scratch.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
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
    # Ensure the forms directory exists
    os.makedirs(FORMS_DIR, exist_ok=True)
    print(f'Directory created: {FORMS_DIR}')

    # Verify no survey.pdf exists (clean state)
    survey_path = os.path.join(FORMS_DIR, 'survey.pdf')
    if os.path.exists(survey_path):
        os.remove(survey_path)
        print(f'Removed existing survey.pdf for clean initial state')

    # Open file manager to show the empty forms directory
    launch_gui(f'nautilus "{FORMS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')


create_initial()
