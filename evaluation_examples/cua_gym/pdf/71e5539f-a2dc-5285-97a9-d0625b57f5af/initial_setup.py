"""
Initial Setup: Create empty receipts directory for payment receipt PDF task
Task ID: pdf_fin_032
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_032'
RECEIPTS_DIR = f'{WORKDIR}/finance/receipts'


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
    # Create the directory structure
    os.makedirs(RECEIPTS_DIR, exist_ok=True)

    # Ensure directory is empty (remove any stale files)
    for f in os.listdir(RECEIPTS_DIR):
        fp = os.path.join(RECEIPTS_DIR, f)
        if os.path.isfile(fp):
            os.remove(fp)

    print(f'Initial directory created: {RECEIPTS_DIR}')
    print(f'Directory contents: {os.listdir(RECEIPTS_DIR)}')

    # Open file manager showing the receipts directory
    launch_gui(f'nautilus "{RECEIPTS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
