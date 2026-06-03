"""
Initial Setup: Open browser and navigate to the GitHub raw notebook URL.
Task ID: osworld_multi_apps_code_to_writer_file_005
Domain: libreoffice_writer (multi-apps: browser + writer)

Initial state:
  - Browser open and navigated to the GitHub raw notebook URL
  - No numpy_code.py exists on the Desktop
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_to_writer_file_005'
DESKTOP = f'{WORKDIR}/Desktop'
NOTEBOOK_URL = 'https://raw.githubusercontent.com/jakevdp/PythonDataScienceHandbook/master/notebooks/02.02-The-Basics-Of-NumPy-Arrays.ipynb'


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

    # Remove any pre-existing numpy_code.py on Desktop
    target_file = os.path.join(DESKTOP, 'numpy_code.py')
    if os.path.exists(target_file):
        os.remove(target_file)
        print(f'Removed pre-existing file: {target_file}')

    print(f'Desktop confirmed clean: no numpy_code.py present')

    # Launch browser and navigate to the GitHub raw notebook URL
    # Use Google Chrome / Chromium
    launch_gui(f'google-chrome --new-window "{NOTEBOOK_URL}"', delay_sec=3.0)
    print(f'GUI_READY: launched browser with URL: {NOTEBOOK_URL}')


create_initial()
