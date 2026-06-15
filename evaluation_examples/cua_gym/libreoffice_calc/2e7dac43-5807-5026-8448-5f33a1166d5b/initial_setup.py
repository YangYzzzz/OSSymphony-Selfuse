"""
Initial Setup: Citation analysis of Turing Award ML/AI winners (2018-2023)
Task ID: osworld_multi_apps_web_scholar_012
Domain: libreoffice_calc

This script prepares the initial GUI state for the agent:
- Opens Chrome browser at ACM Turing Award page for reference
- Opens a blank LibreOffice Calc for the agent to build the table
- No pre-existing turing_award_ml file (agent must create it from scratch)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_scholar_012'
DESKTOP = '/home/user/Desktop'


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

    # Remove any pre-existing turing_award_ml file to ensure clean state
    for ext in ['.ods', '.xlsx', '.csv']:
        target = os.path.join(DESKTOP, f'turing_award_ml{ext}')
        if os.path.exists(target):
            os.remove(target)
            print(f'Removed pre-existing file: {target}')

    # Open Chrome at ACM Turing Award page for agent to use as reference
    launch_gui('google-chrome --new-window "https://amturing.acm.org/"', delay_sec=3.0)

    # Open a blank LibreOffice Calc for the agent to build the table
    launch_gui('libreoffice --calc', delay_sec=2.0)

    print(f'Initial GUI state ready:')
    print(f'  - Chrome opened at https://amturing.acm.org/')
    print(f'  - LibreOffice Calc opened (blank)')
    print(f'  - No pre-existing turing_award_ml file on Desktop')
    print('GUI_READY: launched required app(s) with DISPLAY=:0')


create_initial()
