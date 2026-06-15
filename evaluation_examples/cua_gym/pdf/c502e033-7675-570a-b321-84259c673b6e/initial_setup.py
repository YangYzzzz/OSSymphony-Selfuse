"""
Initial Setup: Create empty /home/user/finance/ directory for receipt creation task.
Task ID: pdf_fin_010
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_010'
FINANCE_DIR = f'{WORKDIR}/finance'

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
    # Create the finance directory
    os.makedirs(FINANCE_DIR, exist_ok=True)
    print(f'Directory created: {FINANCE_DIR}')

    # Ensure reportlab is available for the agent
    subprocess.run(
        ['pip3', 'install', 'reportlab'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print('reportlab installed')

    # Open a terminal in the finance directory so the agent can start working
    launch_gui('bash -c "cd /home/user/finance && xterm"', delay_sec=1.0)
    # Also open the file manager to show the finance directory
    launch_gui(f'nautilus "{FINANCE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched file manager and terminal with DISPLAY=:0')

create_initial()
