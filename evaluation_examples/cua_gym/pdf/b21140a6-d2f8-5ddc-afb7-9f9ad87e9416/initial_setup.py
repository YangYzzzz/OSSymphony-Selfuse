"""
Initial Setup: Empty Desktop for PDF creation task
Task ID: pdf_cr_026
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/annotated.pdf'


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
    # Ensure Desktop exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove annotated.pdf if it exists (clean slate)
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)
        print(f'Removed existing {OUTPUT}')

    print(f'Desktop is ready and empty: {DESKTOP}')

    # Open file manager for GUI readiness
    launch_gui(f'nautilus "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
