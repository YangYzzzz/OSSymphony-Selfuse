"""
Initial Setup: Open LibreOffice Impress with a blank presentation.
Task ID: impress_wf_033
Domain: libreoffice_impress

The agent's task is to create a full 8-slide project management tool
comparison presentation from scratch. Initial state is just a blank
presentation open in Impress.
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
    # Launch LibreOffice Impress with a blank presentation
    launch_gui('libreoffice --impress', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Impress with blank presentation')


create_initial()
