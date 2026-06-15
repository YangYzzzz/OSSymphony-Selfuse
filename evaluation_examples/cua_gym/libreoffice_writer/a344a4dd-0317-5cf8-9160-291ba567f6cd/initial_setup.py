"""
Initial Setup: Wedding Guest List - Table 5
Task ID: writer_tbl_053
Domain: libreoffice_writer

Creates initial state: a .docx file with just the heading 'Wedding Guest List - Table 5'
and NO table. The agent must create the table.
"""

import os
import shlex
import subprocess
import time
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_tbl_053'
OUTPUT = f'{WORKDIR}/Desktop/guest_list.docx'


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
    # Ensure Desktop directory exists
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    doc = Document()

    # Add heading: "Wedding Guest List - Table 5"
    heading = doc.add_heading('Wedding Guest List - Table 5', level=1)

    # NO table — the agent must create it
    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready: open in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
