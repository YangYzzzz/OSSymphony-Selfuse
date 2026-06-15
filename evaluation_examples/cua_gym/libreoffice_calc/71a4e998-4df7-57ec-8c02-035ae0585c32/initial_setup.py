"""
Initial Setup: DBLP Scholar Research Task - Google Brain/DeepMind NLP Researchers
Task ID: osworld_multi_apps_scholar_to_calc_015
Domain: libreoffice_calc (multi-app: Chrome + LibreOffice Calc)

Creates google_researchers.ods with headers only (no data rows).
Agent must browse DBLP to fill in 4 researcher records and create a bar chart.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_scholar_to_calc_015'
OUTPUT = f'{WORKDIR}/google_researchers.ods'


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
    # Create the ODS file using pyexcel-ods3
    import pyexcel_ods3

    # Sheet with headers only — agent will fill in data rows
    sheet_data = [
        ['Name', 'Affiliation', 'Publications', 'Largest-Team Paper'],
    ]

    book_data = {
        'Researchers': sheet_data
    }

    pyexcel_ods3.save_data(OUTPUT, book_data)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open Chrome at DBLP, then open the ODS in LibreOffice Calc
    # Launch Chrome first pointing to DBLP
    launch_gui('google-chrome --new-window "https://dblp.org"', delay_sec=2.0)

    # Launch LibreOffice Calc with the initial file
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=2.0)

    print('GUI_READY: launched Chrome (DBLP) and LibreOffice Calc with DISPLAY=:0')


create_initial()
