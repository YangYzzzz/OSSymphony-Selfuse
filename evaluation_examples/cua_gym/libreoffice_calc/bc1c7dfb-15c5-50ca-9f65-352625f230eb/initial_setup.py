"""
Initial Setup: CV Conference History Spreadsheet Task
Task ID: osworld_multi_apps_web_conference_008
Domain: libreoffice_calc (multi-app: Chrome + LibreOffice Calc)

Initial state:
- No cv_conferences_history.ods exists on Desktop (agent must create it)
- Chrome is open with Wikipedia pages for CVPR, ICCV, ECCV preloaded
- LibreOffice Calc is open with an empty spreadsheet
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_conference_008'
# The output file must NOT exist at initial state; agent creates it
OUTPUT = f'{DESKTOP}/cv_conferences_history.ods'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
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

    # Remove any pre-existing output file to ensure clean initial state
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)
        print(f'Removed pre-existing file: {OUTPUT}')

    print(f'Initial state: {OUTPUT} does not exist (agent must create it from Wikipedia data)')

    # GUI-ready startup:
    # 1. Kill any existing LibreOffice/Chrome instances for clean start
    subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
    time.sleep(1)

    # 2. Open Chrome with the three Wikipedia pages (CVPR, ICCV, ECCV)
    # Open first tab
    launch_gui(
        'google-chrome '
        '"https://en.wikipedia.org/wiki/Conference_on_Computer_Vision_and_Pattern_Recognition" '
        '"https://en.wikipedia.org/wiki/International_Conference_on_Computer_Vision" '
        '"https://en.wikipedia.org/wiki/European_Conference_on_Computer_Vision"',
        delay_sec=3.0
    )

    # 3. Open LibreOffice Calc with an empty/blank spreadsheet for the agent to use
    launch_gui('libreoffice --calc', delay_sec=2.0)

    print('GUI_READY: Chrome (Wikipedia pages) and LibreOffice Calc launched with DISPLAY=:0')


create_initial()
