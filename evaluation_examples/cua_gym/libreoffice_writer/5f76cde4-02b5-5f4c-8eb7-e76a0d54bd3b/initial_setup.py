"""
Initial Setup: Demote items 2, 4, and 6 in numbered list to level 2 sub-items
Task ID: writer_list_027
Domain: libreoffice_writer

Creates a .docx file with 6 paragraphs all at level 1 in a numbered list.
The agent must demote items 2, 4, and 6 to level 2.
"""

import os
import shlex
import subprocess
import time
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user/Desktop'
TASK_ID = 'task_breakdown'
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

    # Add 6 items all at List Number level 1 (no sub-items yet)
    items = [
        "Plan the marketing campaign",
        "Design promotional materials",
        "Execute social media strategy",
        "Monitor engagement metrics",
        "Analyze campaign results",
        "Prepare summary report",
    ]

    for item in items:
        # All items at level 1 using "List Number" style
        para = doc.add_paragraph(item, style='List Number')

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
