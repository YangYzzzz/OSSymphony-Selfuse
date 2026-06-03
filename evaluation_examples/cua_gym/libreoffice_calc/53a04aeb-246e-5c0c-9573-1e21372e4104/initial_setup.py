"""
Initial Setup: NSF ML Grant Research Task
Task ID: osworld_multi_apps_web_faculty_014
Domain: libreoffice_calc (multi-app: Chrome + LibreOffice Calc)

Initial state:
  - Chrome open at NSF Award Search page
  - LibreOffice Calc open (blank new spreadsheet)
  - Desktop exists at /home/user/Desktop/
  - No pre-existing nsf_ml_grants.ods file
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_faculty_014'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch a GUI app on the VM display without blocking script exit."""
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

    # Remove any pre-existing output file to ensure clean initial state
    output_file = os.path.join(DESKTOP, 'nsf_ml_grants.ods')
    if os.path.exists(output_file):
        os.remove(output_file)
    # Also remove xlsx variant if present
    output_xlsx = os.path.join(DESKTOP, 'nsf_ml_grants.xlsx')
    if os.path.exists(output_xlsx):
        os.remove(output_xlsx)

    print(f'Desktop directory ready: {DESKTOP}')
    print('Output file removed (if existed) for clean initial state.')

    # Launch Chrome with NSF Award Search as the starting page
    launch_gui(
        'google-chrome --new-window "https://www.nsf.gov/awardsearch/"',
        delay_sec=3.0
    )
    print('GUI_READY: Chrome launched with NSF Award Search page.')

    # Launch LibreOffice Calc with a blank spreadsheet
    launch_gui(
        'libreoffice --calc',
        delay_sec=2.0
    )
    print('GUI_READY: LibreOffice Calc launched (blank spreadsheet).')


setup_initial()
