"""
Initial Setup: Create a formatted A/B pricing experiment tracker
Task ID: calc_gpm_089
Domain: libreoffice_calc

Initial state: A blank spreadsheet with just a sheet named 'PriceTest'.
The agent's task is to build the full tracker from scratch.
"""

import os
import shlex
import subprocess
import time
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gpm_089'
OUTPUT = f'{WORKDIR}/{TASK_ID}.xlsx'


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
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'PriceTest'

    # Leave sheet blank - agent must build the entire tracker
    wb.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # Open LibreOffice Calc with the blank file
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Calc with DISPLAY=:0')


create_initial()
