"""
Initial Setup: ACL Awards by Topic - awards_by_topic.ods
Task ID: osworld_multi_apps_acl_awards_calc_015
Domain: libreoffice_calc (multi-app: Chrome + LibreOffice Calc)
"""

import os
import shlex
import subprocess
import time
import ezodf

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_acl_awards_calc_015'
OUTPUT = f'{WORKDIR}/awards_by_topic.ods'


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
    # Create ODS spreadsheet with two sheets: Sheet1 and Topics
    # Sheet1: headers only - Year, Conference, Title, Authors, Topic Area (no data)
    # Topics: headers only - Topic Area, Count (no data)

    doc = ezodf.newdoc(doctype='ods', filename=OUTPUT)

    # Sheet1 - main data sheet with headers only
    sheet1 = ezodf.Sheet('Sheet1', size=(30, 5))
    doc.sheets += sheet1

    # Write headers to Sheet1
    headers = ['Year', 'Conference', 'Title', 'Authors', 'Topic Area']
    for col_idx, header in enumerate(headers):
        doc.sheets['Sheet1'][0, col_idx].set_value(header)

    # Topics sheet - with headers only
    topics_sheet = ezodf.Sheet('Topics', size=(20, 2))
    doc.sheets += topics_sheet

    # Write headers to Topics sheet
    doc.sheets['Topics'][0, 0].set_value('Topic Area')
    doc.sheets['Topics'][0, 1].set_value('Count')

    # Save the file
    doc.save()
    print(f'Initial file created: {OUTPUT}')
    print(f'Sheets: {[s.name for s in doc.sheets]}')
    print('Sheet1 has headers only (no award data) - ready for agent to fill')
    print('Topics sheet has headers only - ready for agent to fill')

    # GUI-ready startup: Open Chrome and LibreOffice Calc
    # Kill existing processes to avoid conflicts
    subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
    time.sleep(1.5)

    # Launch Chrome with the ACL wiki best paper awards page
    launch_gui(
        'google-chrome --new-window https://aclweb.org/aclwiki/Best_paper_awards',
        delay_sec=3.0
    )

    # Launch LibreOffice Calc with the initial file
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=3.0)

    print('GUI_READY: launched Chrome and LibreOffice Calc with DISPLAY=:0')


create_initial()
