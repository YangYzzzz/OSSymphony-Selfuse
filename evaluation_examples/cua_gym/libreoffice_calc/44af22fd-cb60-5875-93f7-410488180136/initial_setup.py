"""
Initial Setup: UK Skilled Worker Visa Research Task
Task ID: osworld_multi_apps_travel_permit_research_008
Domain: libreoffice_calc (writer/multi-app)

Initial state: Browser open, no prior Writer document.
The agent will research online and create uk_skilled_worker_visa_guide.odt on the Desktop.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_FILE = f'{DESKTOP}/uk_skilled_worker_visa_guide.odt'


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


def create_initial():
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any pre-existing target file to ensure clean initial state
    if os.path.exists(TASK_FILE):
        os.remove(TASK_FILE)
        print(f'Removed pre-existing file: {TASK_FILE}')

    print(f'Desktop directory confirmed: {DESKTOP}')

    # Open Chrome browser pointing to the UK gov Skilled Worker visa page
    # This gives the agent a starting point for research
    launch_gui(
        'google-chrome --new-window "https://www.gov.uk/skilled-worker-visa"',
        delay_sec=3.0,
    )
    print('Launched Chrome browser to gov.uk Skilled Worker visa page')

    # Also open a blank LibreOffice Writer window so agent can start writing
    launch_gui('libreoffice --writer', delay_sec=2.0)
    print('Launched LibreOffice Writer (blank document)')

    print('GUI_READY: browser and Writer launched with DISPLAY=:0')
    print(f'Target output: {TASK_FILE}')
    print('Initial state: No uk_skilled_worker_visa_guide.odt on Desktop')


create_initial()
