"""
Initial Setup: Computer Vision Professors Database
Task ID: osworld_multi_apps_web_faculty_009
Domain: libreoffice_calc (multi-app: Chrome + LibreOffice Calc)

Sets up the initial environment for the agent:
- Ensures no existing cv_professors.ods file on Desktop
- Opens Chrome with Stanford Vision Lab faculty page
- Opens LibreOffice Calc (empty spreadsheet ready for data entry)
"""

import os
import shlex
import subprocess
import time

TASK_ID = 'osworld_multi_apps_web_faculty_009'
DESKTOP = '/home/user/Desktop'
OUTPUT_FILE = os.path.join(DESKTOP, 'cv_professors.ods')

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
    # 1. Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # 2. Remove any pre-existing cv_professors.ods from Desktop (idempotent)
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print(f'Removed existing file: {OUTPUT_FILE}')

    print(f'Desktop ready. No cv_professors.ods present.')

    # 3. Launch Chrome with Stanford Vision Lab faculty page
    #    (first source the agent needs to browse)
    launch_gui(
        'google-chrome "http://vision.stanford.edu/people.html"',
        delay_sec=3.0
    )
    print('Launched Chrome → Stanford Vision Lab faculty page')

    # 4. Launch LibreOffice Calc (empty spreadsheet for agent to fill in)
    launch_gui(
        'libreoffice --calc',
        delay_sec=2.0
    )
    print('Launched LibreOffice Calc (empty spreadsheet)')

    print('GUI_READY: Chrome and LibreOffice Calc launched with DISPLAY=:0')


setup_initial()
