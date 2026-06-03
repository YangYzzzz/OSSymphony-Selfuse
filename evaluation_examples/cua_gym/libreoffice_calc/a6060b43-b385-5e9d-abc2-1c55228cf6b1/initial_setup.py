"""
Initial Setup: Create NLP faculty spreadsheet task
Task ID: osworld_multi_apps_web_scholar_003
Domain: libreoffice_calc

Initial state: Desktop is empty. LibreOffice Calc is installed.
The agent must create nlp_faculty.ods on the Desktop with 5 NLP researchers.
This script ensures the Desktop exists and is empty of any nlp_faculty.ods,
then opens LibreOffice Calc so the agent can start working.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_scholar_003'
TARGET_FILE = f'{DESKTOP}/nlp_faculty.ods'


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

    # Remove any existing nlp_faculty.ods to ensure clean initial state
    if os.path.exists(TARGET_FILE):
        os.remove(TARGET_FILE)
        print(f'Removed existing file: {TARGET_FILE}')

    print(f'Initial state: Desktop is clean, no nlp_faculty.ods present')
    print(f'Desktop path: {DESKTOP}')

    # Open LibreOffice Calc with a new blank spreadsheet
    # The agent will create nlp_faculty.ods from scratch
    launch_gui('libreoffice --calc', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Calc with DISPLAY=:0')


create_initial()
