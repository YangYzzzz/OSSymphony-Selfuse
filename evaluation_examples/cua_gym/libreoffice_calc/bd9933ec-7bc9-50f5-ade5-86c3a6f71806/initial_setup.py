"""
Initial Setup: Multi-app task — Chrome browser + terminal download + LibreOffice Calc filter
Task ID: osworld_multi_apps_sys_browser_os_005
Domain: libreoffice_calc (multi-app: chrome, os, libreoffice_calc)

Initial state:
  - /home/user/data/ directory exists but does NOT contain covid_data.csv
  - Chrome is open and navigated to the CSV URL for preview
  - Terminal is available for running wget/curl
  - LibreOffice Calc is installed and ready
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_sys_browser_os_005'
DATA_DIR = f'{WORKDIR}/data'
CSV_PATH = f'{DATA_DIR}/covid_data.csv'
CSV_URL = 'https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv'


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
    # 1. Create the /home/user/data/ directory (empty — no CSV yet)
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f'Created directory: {DATA_DIR}')

    # 2. Ensure covid_data.csv does NOT exist (remove if somehow present)
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)
        print(f'Removed pre-existing file: {CSV_PATH}')

    # 3. Verify wget and curl are available (just check, don't install)
    for tool in ['wget', 'curl']:
        result = subprocess.run(['which', tool], capture_output=True, text=True)
        if result.returncode == 0:
            print(f'Tool available: {tool} -> {result.stdout.strip()}')
        else:
            print(f'WARNING: {tool} not found in PATH')

    print(f'Initial state ready:')
    print(f'  - {DATA_DIR}/ exists and is empty (no covid_data.csv)')
    print(f'  - wget/curl available for download')

    # 4. GUI startup — open Chrome navigated to the CSV URL for preview
    launch_gui(
        f'google-chrome --no-sandbox "{CSV_URL}"',
        delay_sec=3.0,
    )
    print(f'GUI_READY: Chrome opened with CSV URL for preview')

    # 5. Also open a GNOME Terminal so the user can run wget/curl
    launch_gui(
        'gnome-terminal',
        delay_sec=1.5,
    )
    print('GUI_READY: Terminal opened for wget/curl commands')


create_initial()
