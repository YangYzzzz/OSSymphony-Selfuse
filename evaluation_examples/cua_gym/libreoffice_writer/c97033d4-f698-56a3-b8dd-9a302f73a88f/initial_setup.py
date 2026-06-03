"""
Initial Setup: Convert comma-separated names list to table
Task ID: osworld_writer_easy_016
Domain: libreoffice_writer

Creates team_roster.docx with a comma-separated list of names.
The agent task is to convert this text into a 1-row, 6-column table.
"""

import os
import shlex
import subprocess
import time
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_easy_016'
OUTPUT = f'{WORKDIR}/team_roster.docx'


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
    doc = Document()

    # Add the comma-separated names as a single paragraph
    doc.add_paragraph('Alice Johnson, Bob Smith, Carol Davis, David Lee, Emma Wilson, Frank Brown')

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
