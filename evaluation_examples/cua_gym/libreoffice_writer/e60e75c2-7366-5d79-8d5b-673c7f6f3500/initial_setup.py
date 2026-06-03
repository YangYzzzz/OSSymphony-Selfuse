"""
Initial Setup: Navigation instructions as plain text paragraphs
Task ID: writer_list_052
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user/Desktop'
TASK_ID = 'navigation'
OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'


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
    os.makedirs(WORKDIR, exist_ok=True)

    doc = Document()

    # Five plain text paragraphs — NO bullet formatting
    paragraphs = [
        "Click on Settings in the top menu bar",
        "Select Account Preferences from the dropdown",
        "Navigate to the Security section",
        "Enable two-factor authentication toggle",
        "Save changes and confirm with your password",
    ]

    for text in paragraphs:
        para = doc.add_paragraph(text)
        # Explicitly set to normal style (no list formatting)
        para.style = doc.styles['Normal']

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
