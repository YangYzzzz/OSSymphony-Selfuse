"""
Initial Setup: Import a CSV file into LibreOffice Calc
Task ID: calc_gsi_013
Domain: libreoffice_calc

Creates a realistic inventory CSV file and opens LibreOffice Calc (empty)
so the agent can use File > Open to import the CSV.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_013'
CSV_FILE = f'{WORKDIR}/inventory_export.csv'
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
    # Create realistic inventory CSV data with comma delimiters
    csv_content = """Product Code,Description,Quantity,Unit Price
WH-1001,Industrial Bolt M10x50,2450,0.85
WH-1002,Hex Nut M10 Zinc Plated,5200,0.32
WH-1003,Flat Washer M10 Stainless,3800,0.18
WH-1004,Spring Washer M10,1900,0.25
WH-1005,Socket Head Cap Screw M8x30,1750,1.45
WH-1006,Carriage Bolt M12x60,820,2.10
WH-1007,Wing Nut M8 Brass,640,0.95
WH-1008,Threaded Rod M16x1000,185,8.75
WH-1009,Lock Washer M12,4100,0.22
WH-1010,Coupling Nut M10x30,960,1.15
WH-1011,Eye Bolt M12x100,350,3.80
WH-1012,U-Bolt M10x80,720,2.65
WH-1013,Anchor Bolt M16x200,290,5.40
WH-1014,Flange Nut M10,2800,0.48
WH-1015,Nylon Lock Nut M8,3400,0.38"""

    with open(CSV_FILE, 'w') as f:
        f.write(csv_content)

    print(f'CSV file created: {CSV_FILE}')

    # Open LibreOffice Calc empty so the agent can use File > Open
    launch_gui('libreoffice --calc', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Calc with DISPLAY=:0')


create_initial()
