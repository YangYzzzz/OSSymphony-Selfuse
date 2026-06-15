"""
Initial Setup: Open LibreOffice Impress with a blank presentation.
Task ID: impress_wf_008
Domain: libreoffice_impress

The agent's task is to create an agenda slide deck from scratch,
so the initial state is simply a blank presentation open in Impress.
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
    os.makedirs("/home/user/Desktop", exist_ok=True)

    # Launch LibreOffice Impress with a blank presentation
    launch_gui("libreoffice --impress", delay_sec=3.0)
    print("GUI_READY: LibreOffice Impress launched with blank presentation on DISPLAY=:0")


create_initial()
