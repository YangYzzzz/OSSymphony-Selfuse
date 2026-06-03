"""
Initial Setup: Multi-app task - Chrome + LibreOffice Calc URL checker
Task ID: osworld_multi_apps_multi_simple_009
Domain: libreoffice_calc (multi-app with Chrome)

Creates /home/user/links/websites.ods with 5 URLs to check.
Columns: Label (A), URL (B), Status (C), Title (D)
- Column C (Status): empty (to be filled by agent)
- Column D (Title): header only, data rows empty (to be filled by agent)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_multi_simple_009'
LINKS_DIR = f'{WORKDIR}/links'
OUTPUT = f'{LINKS_DIR}/websites.ods'


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
    import pandas as pd

    # Ensure the links directory exists
    os.makedirs(LINKS_DIR, exist_ok=True)

    # Define the 5 URLs with labels
    # Column C (Status) and D (Title data rows) are left empty
    data = {
        'Label': [
            'Wikipedia',
            'GitHub',
            'Stack Overflow',
            'Python Official',
            'Mozilla Developer',
        ],
        'URL': [
            'https://www.wikipedia.org',
            'https://www.github.com',
            'https://stackoverflow.com',
            'https://www.python.org',
            'https://developer.mozilla.org',
        ],
        'Status': ['', '', '', '', ''],
        'Title':  ['', '', '', '', ''],
    }

    df = pd.DataFrame(data)

    # Write to ODS using odf engine
    with pd.ExcelWriter(OUTPUT, engine='odf') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the ODS file in LibreOffice Calc
    # Task expects agent to open Chrome and check URLs, so launch both
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=2.0)
    launch_gui('google-chrome', delay_sec=2.0)

    print('GUI_READY: launched LibreOffice Calc and Chrome with DISPLAY=:0')


create_initial()
