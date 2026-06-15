"""
Initial Setup: Group sheets Monday-Friday with Hours/AM/PM values
Task ID: calc_ps_084
Domain: libreoffice_calc

Creates a workbook with 5 blank day-of-week sheets (Monday through Friday).
All sheets are empty — no values in any cells.
"""

import os
import shlex
import subprocess
import time
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ps_084'
OUTPUT = f'{WORKDIR}/{TASK_ID}.xlsx'

DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']


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

    # Create Monday sheet (rename default sheet)
    ws = wb.active
    ws.title = DAY_NAMES[0]

    # Create Tuesday through Friday sheets
    for day in DAY_NAMES[1:]:
        wb.create_sheet(day)

    # All sheets remain completely blank — no data in any cells
    wb.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # Open in LibreOffice Calc for the GUI agent
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Calc with DISPLAY=:0')


create_initial()
