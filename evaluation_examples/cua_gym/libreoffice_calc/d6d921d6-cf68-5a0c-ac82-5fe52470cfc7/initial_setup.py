"""
Initial Setup: Download GNU Bash Shell Variables content and save as bash_vars.docx
Task ID: osworld_multi_apps_web_to_doc_004
Domain: multi_apps (Chrome + LibreOffice Writer)

Initial state:
- Chrome is open (may navigate to the GNU Bash manual page)
- Desktop is empty (no bash_vars.docx)
- LibreOffice Writer is not running
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_to_doc_004'
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

    # Remove bash_vars.docx if it somehow already exists (idempotent)
    target_file = os.path.join(DESKTOP, 'bash_vars.docx')
    if os.path.exists(target_file):
        os.remove(target_file)
        print(f'Removed pre-existing file: {target_file}')

    print(f'Desktop is clean: {DESKTOP}')

    # Kill any running LibreOffice instances to ensure Writer is not running
    subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
    time.sleep(1)

    # Open Chrome with the GNU Bash Shell Variables page
    # This is the starting point for the agent
    launch_gui(
        'google-chrome "https://www.gnu.org/software/bash/manual/html_node/Shell-Variables.html"',
        delay_sec=3.0
    )
    print('GUI_READY: Chrome launched with GNU Bash Shell Variables page at DISPLAY=:0')


setup_initial()
