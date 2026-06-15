"""
Initial Setup: Visit Yoshua Bengio's DBLP page and extract recent publications into a Calc file.
Task ID: osworld_multi_apps_web_scholar_005
Domain: libreoffice_calc (multi-app: Chrome + LibreOffice Calc)

Initial state:
- Desktop is empty (no bengio_recent.ods exists)
- Chrome is open with Yoshua Bengio's DBLP page loaded
- LibreOffice Calc is open with a new blank document
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_scholar_005'
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

    # Remove any pre-existing bengio_recent.ods on Desktop (idempotent cleanup)
    target_file = os.path.join(DESKTOP, 'bengio_recent.ods')
    if os.path.exists(target_file):
        os.remove(target_file)
        print(f'Removed pre-existing file: {target_file}')

    print('Desktop is clean — no bengio_recent.ods present.')
    print(f'Desktop path: {DESKTOP}')

    # Launch Chrome with Yoshua Bengio's DBLP page
    launch_gui(
        'google-chrome "https://dblp.org/pid/b/YoshuaBengio.html"',
        delay_sec=3.0
    )
    print('GUI_READY: launched Chrome with DBLP page at DISPLAY=:0')

    # Launch LibreOffice Calc with a blank new document
    launch_gui(
        'libreoffice --calc',
        delay_sec=2.0
    )
    print('GUI_READY: launched LibreOffice Calc at DISPLAY=:0')

create_initial()
