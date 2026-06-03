"""
Initial Setup: Canada TRV Guide Research Task
Task ID: osworld_multi_apps_travel_permit_research_006
Domain: multi_apps (Chrome + LibreOffice Writer)

Initial state:
- No canada_trv_guide.odt on Desktop (or anywhere)
- Chrome browser open with the Canada official visa page loaded
  so the agent can read info and create the Writer document
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_travel_permit_research_006'
DESKTOP = f'{WORKDIR}/Desktop'
TARGET_FILE = f'{DESKTOP}/canada_trv_guide.odt'

# Canada official Temporary Resident Visa eligibility page
CANADA_VISA_URL = 'https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada/eligibility.html'


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


def setup_initial():
    # 1. Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # 2. Remove any existing canada_trv_guide.odt to ensure clean initial state
    if os.path.exists(TARGET_FILE):
        os.remove(TARGET_FILE)
        print(f'Removed existing file: {TARGET_FILE}')

    # Also remove from /home/user directly in case it was placed there
    home_target = f'{WORKDIR}/canada_trv_guide.odt'
    if os.path.exists(home_target):
        os.remove(home_target)
        print(f'Removed existing file: {home_target}')

    print('Initial state: No canada_trv_guide.odt exists.')

    # 3. Open Chrome with the Canada official TRV eligibility page
    #    Try google-chrome first (x86), fallback to chromium (ARM)
    chrome_cmd = f'google-chrome --new-window "{CANADA_VISA_URL}"'
    launch_gui(chrome_cmd, delay_sec=3.0)

    print(f'GUI_READY: Chrome launched with URL {CANADA_VISA_URL}')
    print('Initial setup complete.')


setup_initial()
