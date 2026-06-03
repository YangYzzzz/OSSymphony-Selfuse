"""
Initial Setup: Open LibreOffice Impress with a blank presentation.
Task ID: impress_wf_053
Domain: libreoffice_impress
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'impress_wf_053'


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
    # Task says initial state is "LibreOffice Impress is open with a blank presentation"
    # No file needs to be pre-created - just open Impress with a blank presentation
    # Ensure Desktop directory exists
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    # Launch LibreOffice Impress with a blank presentation
    launch_gui('libreoffice --impress', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Impress with blank presentation on DISPLAY=:0')


create_initial()
