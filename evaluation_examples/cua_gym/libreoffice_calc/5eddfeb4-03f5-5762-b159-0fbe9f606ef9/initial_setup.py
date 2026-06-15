"""
Initial Setup: CMU ML Faculty Data Collection Task
Task ID: osworld_multi_apps_web_faculty_006
Domain: multi_apps (Chrome + LibreOffice Calc)

The agent's job:
  1. Visit https://www.ml.cmu.edu/people/faculty.html
  2. Collect Name, Title, Research_Interests, Profile_URL for each faculty
  3. Enter data into LibreOffice Calc
  4. Highlight rows mentioning 'reinforcement learning' or 'robotics' in yellow
  5. Save as ~/Desktop/cmu_ml_faculty.ods
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_faculty_006'
DESKTOP = f'{WORKDIR}/Desktop'


def launch_gui(command: str, delay_sec: float = 1.5):
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

    # Remove any leftover target file so agent starts clean
    target_file = os.path.join(DESKTOP, 'cmu_ml_faculty.ods')
    if os.path.exists(target_file):
        os.remove(target_file)
        print(f'Removed leftover file: {target_file}')

    # Also remove any .xlsx or .csv variants
    for ext in ['.xlsx', '.csv', '.xls']:
        alt = os.path.join(DESKTOP, f'cmu_ml_faculty{ext}')
        if os.path.exists(alt):
            os.remove(alt)

    print('Initial state: Desktop is clean, no pre-existing faculty file.')

    # Launch Chrome pointing to CMU ML faculty page
    cmu_url = 'https://www.ml.cmu.edu/people/faculty.html'
    launch_gui(f'google-chrome "{cmu_url}"', delay_sec=3.0)
    print(f'Launched Chrome with URL: {cmu_url}')

    # Launch LibreOffice Calc (blank) for the agent to start entering data
    launch_gui('libreoffice --calc', delay_sec=2.5)
    print('Launched LibreOffice Calc (blank).')

    print('GUI_READY: Chrome and LibreOffice Calc opened with DISPLAY=:0')


setup_initial()
