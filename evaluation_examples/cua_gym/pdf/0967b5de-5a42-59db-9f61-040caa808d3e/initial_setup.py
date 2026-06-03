"""
Initial Setup: Budget variance report PDF creation task
Task ID: pdf_fin_071
Domain: pdf

Creates the /home/user/finance/ directory and opens a file manager
so the agent can create the variance report PDF.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_071'
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
    # Create the finance directory if it doesn't exist
    os.makedirs(FINANCE_DIR, exist_ok=True)
    print(f'Directory created: {FINANCE_DIR}')

    # Create a placeholder README in the finance directory to make it look realistic
    readme_path = os.path.join(FINANCE_DIR, 'README.txt')
    with open(readme_path, 'w') as f:
        f.write("Finance Department Reports\n")
        f.write("==========================\n\n")
        f.write("This directory contains monthly financial reports.\n")
        f.write("Please use the standard naming convention:\n")
        f.write("  variance_report_<month>.pdf\n")
        f.write("  budget_summary_<quarter>.pdf\n")
        f.write("  expense_detail_<month>.xlsx\n")
    print(f'README created: {readme_path}')

    # Open file manager showing the finance directory
    launch_gui(f'nautilus "{FINANCE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched file manager with DISPLAY=:0')

create_initial()
