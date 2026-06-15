"""
Initial Setup: Schengen Visa Research Task - Multi-App (Chrome + LibreOffice Writer)
Task ID: osworld_multi_apps_travel_permit_research_009
Domain: libreoffice_calc (multi-app: Chrome browser + LibreOffice Writer)

Sets up the initial environment:
- Ensures Desktop directory exists and is clean (no prior ODT guide)
- Opens Chrome browser so agent can research Schengen visa requirements
- No Writer document pre-exists (agent must create it)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_travel_permit_research_009'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT_ODT = f'{DESKTOP}/schengen_visa_china_applicant_guide.odt'


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

    # Remove any pre-existing ODT guide to ensure clean initial state
    if os.path.exists(OUTPUT_ODT):
        os.remove(OUTPUT_ODT)
        print(f'Removed pre-existing file: {OUTPUT_ODT}')

    print(f'Initial state ready: Desktop exists at {DESKTOP}')
    print(f'No Writer document at {OUTPUT_ODT} - agent must research and create it')

    # Open Chrome browser so agent can start researching immediately
    # Try google-chrome first, fall back to chromium-browser
    chrome_url = 'https://www.google.com'
    try:
        launch_gui(f'google-chrome --new-window "{chrome_url}"', delay_sec=2.0)
        print('GUI_READY: launched Google Chrome with DISPLAY=:0')
    except Exception:
        try:
            launch_gui(f'chromium-browser --new-window "{chrome_url}"', delay_sec=2.0)
            print('GUI_READY: launched Chromium with DISPLAY=:0')
        except Exception:
            # Fall back to just opening the browser without specific URL
            launch_gui('x-www-browser', delay_sec=2.0)
            print('GUI_READY: launched default browser with DISPLAY=:0')


create_initial()
