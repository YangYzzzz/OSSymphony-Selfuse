"""
Initial Setup: Ensure Desktop is clean for multi_font.pdf creation task
Task ID: pdf_cr_040
Domain: pdf

The agent must create the PDF from scratch - no pre-existing file should exist.
"""

import os
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
TARGET_FILE = f'{DESKTOP}/multi_font.pdf'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        command.split(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any pre-existing multi_font.pdf to ensure clean state
    if os.path.exists(TARGET_FILE):
        os.remove(TARGET_FILE)
        print(f'Removed pre-existing {TARGET_FILE}')

    print(f'Desktop is clean. No multi_font.pdf exists.')
    print(f'Desktop contents: {os.listdir(DESKTOP)}')

    # Open file manager so the agent can see the Desktop
    launch_gui('nautilus /home/user/Desktop', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')


create_initial()
