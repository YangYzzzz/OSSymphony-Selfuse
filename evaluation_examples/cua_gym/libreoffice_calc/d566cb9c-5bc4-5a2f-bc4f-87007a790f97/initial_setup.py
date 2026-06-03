"""
Initial Setup: Save MDN CSS Flexbox content as flexbox_notes.docx on Desktop
Task ID: osworld_multi_apps_web_to_doc_001
Domain: multi_apps (Chrome + LibreOffice Writer)

Initial state:
- Desktop is empty (no flexbox_notes.docx)
- Chrome is open on a blank/default tab
- LibreOffice Writer is NOT open
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_to_doc_001'
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

    # Remove any pre-existing flexbox_notes.docx from the Desktop (idempotent)
    target_file = os.path.join(DESKTOP, 'flexbox_notes.docx')
    if os.path.exists(target_file):
        os.remove(target_file)
        print(f'Removed pre-existing file: {target_file}')

    print(f'Desktop is clean. Target file does not exist: {target_file}')

    # Kill any existing LibreOffice Writer instances so it is not open
    subprocess.run(['pkill', '-f', 'soffice'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)

    # Open Chrome on the MDN Flexbox page so the agent can see it
    # The agent's task is to save this page content into a .docx file
    mdn_url = 'https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox'
    launch_gui(f'google-chrome "{mdn_url}"', delay_sec=3.0)

    print('GUI_READY: Chrome launched with MDN Flexbox page, Desktop is empty, LibreOffice Writer is not open.')


setup_initial()
