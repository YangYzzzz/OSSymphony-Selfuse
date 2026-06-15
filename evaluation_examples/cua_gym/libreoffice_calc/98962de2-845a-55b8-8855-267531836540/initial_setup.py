"""
Initial Setup: ML Conference Gender Diversity Analysis
Task ID: osworld_multi_apps_web_conference_010
Domain: libreoffice_calc (multi-app: Chrome + LibreOffice Calc)

This script sets up the initial state for the task where the agent must:
1. Visit NeurIPS 2023 and ICML 2023 program committee pages
2. Collect area chair names and assess gender
3. Create a spreadsheet with results at ~/Desktop/conference_diversity.ods
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_conference_010'
DESKTOP = f'{WORKDIR}/Desktop'

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

    # No pre-existing conference_diversity.ods file should exist
    # The agent must create it from scratch by visiting the web pages
    target_file = f'{DESKTOP}/conference_diversity.ods'
    if os.path.exists(target_file):
        os.remove(target_file)
        print(f'Removed existing file: {target_file}')

    print(f'Initial state: Desktop ready at {DESKTOP}')
    print(f'Target file does NOT exist (agent must create it): {target_file}')

    # GUI-ready startup: Open Chrome to NeurIPS 2023 program committee page
    # The agent should start by visiting the committee pages
    launch_gui(
        'google-chrome --new-window "https://neurips.cc/Conferences/2023/ProgramCommittee"',
        delay_sec=3.0
    )
    print('GUI_READY: Launched Chrome with NeurIPS 2023 Program Committee page')

    # Also open a blank LibreOffice Calc for the agent to enter data
    launch_gui('libreoffice --calc', delay_sec=2.0)
    print('GUI_READY: Launched LibreOffice Calc (blank)')

create_initial()
