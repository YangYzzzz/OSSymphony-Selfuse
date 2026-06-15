"""
Initial Setup: Multi-app task - fetch Wikipedia ML article and save as docx
Task ID: osworld_multi_apps_web_to_doc_002
Domain: multi_apps (Chrome + LibreOffice Writer)

Initial state:
- Chrome is open (with default new tab page)
- Desktop is empty (no ml_overview.docx)
- LibreOffice Writer is NOT running
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_to_doc_002'
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


def setup_initial():
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any pre-existing ml_overview.docx from Desktop (keep initial clean)
    target_file = os.path.join(DESKTOP, 'ml_overview.docx')
    if os.path.exists(target_file):
        os.remove(target_file)
        print(f'Removed pre-existing: {target_file}')

    # Kill any existing LibreOffice Writer instances to ensure clean state
    subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
    time.sleep(1.0)

    # Kill any existing Chrome instances to ensure clean state
    subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
    subprocess.run(['pkill', '-f', 'chromium'], capture_output=True)
    time.sleep(1.5)

    print(f'Desktop is clean: no ml_overview.docx present')
    print(f'LibreOffice Writer: not running')

    # GUI-ready startup: Open Chrome with the Wikipedia Machine Learning page
    # This simulates the initial state where the user has Chrome open
    launch_gui('google-chrome --new-window "https://en.wikipedia.org/wiki/Machine_learning"', delay_sec=3.0)

    print('GUI_READY: launched Chrome with Wikipedia Machine Learning page, DISPLAY=:0')


setup_initial()
