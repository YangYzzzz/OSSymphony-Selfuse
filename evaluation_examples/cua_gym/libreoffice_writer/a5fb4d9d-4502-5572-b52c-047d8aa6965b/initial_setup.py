"""
Initial Setup: Process notebooks and create combined Writer report
Task ID: osworld_multi_apps_code_to_writer_file_012
Domain: libreoffice_writer

Sets up the initial GUI state:
- Opens Chrome browser (for downloading notebooks from URLs)
- Opens LibreOffice Writer (blank document for the combined report)
No pre-existing data files are required; the agent fetches and processes
everything from the internet.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_to_writer_file_012'
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


def create_initial():
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Open Chrome browser so the agent can navigate to the notebook URLs
    launch_gui('google-chrome --new-window', delay_sec=2.5)

    # Open LibreOffice Writer with a blank document
    launch_gui('libreoffice --writer', delay_sec=2.0)

    print(f'Initial state prepared.')
    print(f'  Desktop path: {DESKTOP}')
    print('GUI_READY: launched Chrome and LibreOffice Writer with DISPLAY=:0')


create_initial()
