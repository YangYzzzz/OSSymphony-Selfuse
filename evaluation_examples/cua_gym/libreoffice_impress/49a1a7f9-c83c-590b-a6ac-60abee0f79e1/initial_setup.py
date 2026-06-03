"""
Initial Setup: Open LibreOffice Impress with a blank presentation.
Task ID: impress_wf_002
Domain: libreoffice_impress

The agent's task is to create a 4-slide team presentation from scratch,
so the initial state is simply a blank Impress window.
"""

import os
import shlex
import subprocess
import time


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
    desktop = "/home/user/Desktop"
    os.makedirs(desktop, exist_ok=True)

    # Launch LibreOffice Impress with a blank presentation
    launch_gui("libreoffice --impress", delay_sec=3.0)
    print("GUI_READY: LibreOffice Impress launched with blank presentation")


create_initial()
