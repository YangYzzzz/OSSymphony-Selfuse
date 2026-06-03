"""
Initial Setup: Multi-destination travel permit research task
Task ID: osworld_multi_apps_travel_permit_research_012
Domain: libreoffice_calc (output is .odt - LibreOffice Writer)

Initial state: Browser with internet access showing official visa information.
No prior Writer document exists. The task is to research and create a comprehensive
multi-destination visa guide saved as 'multi_destination_visa_guide.odt' on Desktop.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_travel_permit_research_012'
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

    # Ensure there is NO pre-existing guide file on Desktop
    guide_path = os.path.join(DESKTOP, 'multi_destination_visa_guide.odt')
    if os.path.exists(guide_path):
        os.remove(guide_path)
        print(f'Removed pre-existing file: {guide_path}')

    print(f'Desktop directory ready: {DESKTOP}')
    print('No prior multi_destination_visa_guide.odt on Desktop — task state is clean.')

    # Open Chrome browser with official visa information pages
    # Use a simple URL that agents can use to start researching
    launch_gui(
        'google-chrome --new-window '
        '"https://www.schengenvisainfo.com/schengen-visa-requirements-application/"',
        delay_sec=3.0
    )

    # Open a second tab with UK visa info
    launch_gui(
        'google-chrome '
        '"https://www.gov.uk/standard-visitor/eligibility"',
        delay_sec=2.0
    )

    # Open a third tab with US visa info
    launch_gui(
        'google-chrome '
        '"https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html"',
        delay_sec=2.0
    )

    print('GUI_READY: launched Chrome browser with official visa info pages (DISPLAY=:0)')
    print(f'Task: Create multi_destination_visa_guide.odt on {DESKTOP}')


setup_initial()
