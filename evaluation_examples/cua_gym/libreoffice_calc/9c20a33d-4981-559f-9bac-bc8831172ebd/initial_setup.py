"""
Initial Setup: Web to document task - React Hooks documentation
Task ID: osworld_multi_apps_web_to_doc_007
Domain: multi_apps (Chrome + LibreOffice Writer)

Initial state:
  - Chrome is open (with a new tab or any URL)
  - Desktop is empty (no react_hooks.docx)
  - LibreOffice Writer is NOT running
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_to_doc_007'
DESKTOP = '/home/user/Desktop'


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

    # Remove any pre-existing react_hooks.docx from Desktop (idempotent)
    target_file = os.path.join(DESKTOP, 'react_hooks.docx')
    if os.path.exists(target_file):
        os.remove(target_file)
        print(f'Removed existing file: {target_file}')

    print(f'Desktop is clean (no react_hooks.docx): {DESKTOP}')

    # Kill any running LibreOffice processes to ensure it's not running
    subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
    time.sleep(1.0)

    # Launch Chrome with the React Hooks reference page
    launch_gui('google-chrome "https://react.dev/reference/react"', delay_sec=3.0)
    print('GUI_READY: launched Chrome with DISPLAY=:0')


setup_initial()
