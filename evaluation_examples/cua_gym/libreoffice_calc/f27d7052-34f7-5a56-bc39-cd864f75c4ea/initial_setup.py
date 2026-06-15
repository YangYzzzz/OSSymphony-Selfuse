"""
Initial Setup: MIT CSAIL Learning and Intelligent Systems Researchers Task
Task ID: osworld_multi_apps_web_faculty_007
Domain: libreoffice_calc (multi-app: Chrome + LibreOffice Calc)

Creates a blank initial state:
- Desktop exists (default)
- Chrome is open with MIT CSAIL people page
- LibreOffice Calc is open with an empty spreadsheet
  (agent will create mit_lis_researchers.ods on Desktop)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_faculty_007'
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

    # Remove any stale output file from prior runs (idempotency)
    stale_path = os.path.join(DESKTOP, 'mit_lis_researchers.ods')
    if os.path.exists(stale_path):
        os.remove(stale_path)

    print(f'Desktop directory ready: {DESKTOP}')
    print('Initial state: no mit_lis_researchers.ods file (agent must create it)')

    # GUI-ready startup: open Chrome with the MIT CSAIL people page
    launch_gui(
        'google-chrome "https://www.csail.mit.edu/people"',
        delay_sec=3.0
    )
    print('GUI_READY: launched Chrome with MIT CSAIL people page (DISPLAY=:0)')

    # Also open LibreOffice Calc (blank) so agent has it ready
    launch_gui(
        'libreoffice --calc',
        delay_sec=2.0
    )
    print('GUI_READY: launched LibreOffice Calc blank (DISPLAY=:0)')

create_initial()
