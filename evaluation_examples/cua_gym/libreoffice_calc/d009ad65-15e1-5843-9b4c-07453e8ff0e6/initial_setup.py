"""
Initial Setup: Docker networking study guide - web to doc task
Task ID: osworld_multi_apps_web_to_doc_008
Domain: multi_apps (Chrome + LibreOffice Writer)

Initial state:
  - Chrome is open (showing a neutral start page or the Docker networking URL)
  - Desktop is empty (no docker_networking.docx)
  - LibreOffice Writer is NOT running
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_to_doc_008'
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


def create_initial():
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any existing docker_networking.docx from Desktop (idempotent)
    target_file = os.path.join(DESKTOP, 'docker_networking.docx')
    if os.path.exists(target_file):
        os.remove(target_file)
        print(f'Removed existing file: {target_file}')

    # Kill any running LibreOffice Writer instances
    subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
    time.sleep(1)

    # Kill any existing Chrome instances to ensure clean state
    subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
    subprocess.run(['pkill', '-f', 'chromium'], capture_output=True)
    time.sleep(2)

    # Launch Chrome with the Docker networking documentation URL
    # The agent needs to fetch content from this URL
    launch_gui(
        'google-chrome --no-first-run --disable-default-apps '
        '"https://docs.docker.com/network/"',
        delay_sec=3.0
    )

    print(f'Desktop cleared: no docker_networking.docx present')
    print(f'Chrome launched with Docker networking docs URL')
    print('LibreOffice Writer is not running')
    print('GUI_READY: Chrome opened with DISPLAY=:0')


create_initial()
