"""
Initial Setup: Schengen Visa Application Checklist Task
Task ID: osworld_multi_apps_travel_permit_research_001
Domain: libreoffice_writer / os

Creates:
  - /home/user/Desktop/schengen_steps.txt with 5 plain-text Schengen visa steps
  - Opens the file in gedit so the agent can read and copy the steps

NO Writer document should exist at this point — the agent creates it.
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
STEPS_FILE = f'{DESKTOP}/schengen_steps.txt'


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

    # Remove any pre-existing Writer document (ensure clean state)
    checklist_file = f'{DESKTOP}/schengen_checklist.odt'
    if os.path.exists(checklist_file):
        os.remove(checklist_file)
        print(f'Removed pre-existing file: {checklist_file}')

    # Write the 5 plain-text steps to schengen_steps.txt
    steps_content = (
        "1. Gather required documents\n"
        "2. Complete the application form\n"
        "3. Schedule appointment at consulate\n"
        "4. Pay visa fee\n"
        "5. Attend appointment and submit documents\n"
    )
    Path(STEPS_FILE).write_text(steps_content, encoding='utf-8')
    print(f'Created: {STEPS_FILE}')

    # GUI-ready startup: open the steps file in gedit so the agent can see it
    launch_gui(f'gedit "{STEPS_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched gedit with schengen_steps.txt using DISPLAY=:0')


create_initial()
