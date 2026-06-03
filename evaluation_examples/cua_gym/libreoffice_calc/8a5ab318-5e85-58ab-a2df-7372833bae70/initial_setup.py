"""
Initial Setup: Create a blank spreadsheet for invoice building task
Task ID: calc_grs_001
Domain: libreoffice_calc

The task requires the agent to build an entire professional invoice from scratch.
The initial file is intentionally blank per the task context.
"""

import os
import shlex
import subprocess
import time
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_grs_001'
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
    # Create a blank workbook with a single sheet named "Sheet1"
    # The task says the file is "currently blank" - agent builds everything from scratch
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    wb.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open blank spreadsheet in LibreOffice Calc
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Calc with DISPLAY=:0')


create_initial()
