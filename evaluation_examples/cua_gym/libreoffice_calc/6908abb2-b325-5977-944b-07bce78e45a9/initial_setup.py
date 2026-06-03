"""
Initial Setup: Find Michelin-starred NYC restaurants and record in a Calc spreadsheet
Task ID: osworld_multi_apps_web_location_007
Domain: libreoffice_calc (multi-app: Chrome + LibreOffice Calc)

Initial state:
- Desktop is empty (no nyc_michelin.ods file)
- Chrome is opened with the Michelin Guide NYC restaurants URL
- LibreOffice Calc is opened as a new empty document
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_location_007'
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

def setup_initial():
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any pre-existing nyc_michelin.ods from Desktop (ensure clean state)
    target_file = os.path.join(DESKTOP, 'nyc_michelin.ods')
    if os.path.exists(target_file):
        os.remove(target_file)
        print(f'Removed pre-existing file: {target_file}')

    print(f'Desktop is clean - no nyc_michelin.ods exists.')

    # Launch Chrome with the Michelin Guide NYC restaurants page
    michelin_url = 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurants'
    launch_gui(f'google-chrome "{michelin_url}"', delay_sec=3.0)
    print(f'Chrome launched with Michelin Guide URL: {michelin_url}')

    # Launch LibreOffice Calc with a new empty document
    launch_gui('libreoffice --calc', delay_sec=2.0)
    print('LibreOffice Calc launched (new empty document)')

    print('GUI_READY: launched Chrome and LibreOffice Calc with DISPLAY=:0')

setup_initial()
