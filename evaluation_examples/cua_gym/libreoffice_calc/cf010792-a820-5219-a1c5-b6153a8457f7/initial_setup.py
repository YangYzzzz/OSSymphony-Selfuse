"""
Initial Setup: Organize SF restaurant data into a LibreOffice Calc table
Task ID: osworld_multi_apps_web_location_001
Domain: libreoffice_calc

Initial state: Desktop is empty. LibreOffice Calc is installed.
The agent will create the file sf_restaurants.ods on the Desktop.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'osworld_multi_apps_web_location_001'
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

    # Remove any pre-existing sf_restaurants file to ensure clean state
    for ext in ['.ods', '.xlsx', '.csv']:
        target = os.path.join(DESKTOP, f'sf_restaurants{ext}')
        if os.path.exists(target):
            os.remove(target)
            print(f'Removed existing file: {target}')

    print('Initial state: Desktop is empty (no sf_restaurants file exists).')
    print(f'Desktop path: {DESKTOP}')

    # GUI-ready startup: open a blank LibreOffice Calc so agent can start working
    launch_gui('libreoffice --calc', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Calc (blank) with DISPLAY=:0')


create_initial()
