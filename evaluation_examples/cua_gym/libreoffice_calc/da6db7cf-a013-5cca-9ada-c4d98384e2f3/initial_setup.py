"""
Initial Setup: Open Chrome to Flask GitHub README, LibreOffice Writer for note-taking
Task ID: osworld_multi_apps_multi_simple_004
Domain: multi-app (Chrome + LibreOffice Writer)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_multi_simple_004'
NOTES_DIR = f'{WORKDIR}/notes'


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
    # 1. Ensure /home/user/notes/ directory exists
    os.makedirs(NOTES_DIR, exist_ok=True)
    print(f'Created notes directory: {NOTES_DIR}')

    # 2. Verify no flask_install.odt exists yet (task requires creating it)
    odt_path = f'{NOTES_DIR}/flask_install.odt'
    if os.path.exists(odt_path):
        os.remove(odt_path)
        print(f'Removed pre-existing {odt_path} to ensure clean initial state')

    print('Initial state ready: notes/ directory exists, flask_install.odt does not exist')

    # 3. GUI startup: Open Chrome navigated to Flask GitHub page
    launch_gui(
        'google-chrome --new-window "https://github.com/pallets/flask"',
        delay_sec=3.0
    )
    print('Launched Chrome with Flask GitHub page')

    # 4. Also open LibreOffice Writer (blank, for the user to create the document)
    launch_gui(
        'libreoffice --writer',
        delay_sec=2.0
    )
    print('Launched LibreOffice Writer')

    print('GUI_READY: Chrome and LibreOffice Writer launched with DISPLAY=:0')


create_initial()
