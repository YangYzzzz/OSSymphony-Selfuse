"""
Initial Setup: Bullet list with six items, all formatted as bullet list items
Task ID: writer_list_070
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time

from docx import Document
from docx.shared import Pt, Inches

WORKDIR = '/home/user'
TASK_ID = 'writer_list_070'
# Task specifies ~/Desktop/mixed_content.docx
OUTPUT = f'{WORKDIR}/Desktop/mixed_content.docx'


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
    desktop_dir = f'{WORKDIR}/Desktop'
    os.makedirs(desktop_dir, exist_ok=True)

    doc = Document()

    # Six paragraphs all formatted as bullet list items
    bullet_items = [
        'Primary objective: Launch new product line',
        'Secondary objective: Improve market share',
        'Note: Timeline subject to change based on supplier availability',
        'Note: Budget allocation pending board approval',
        'Action item: Finalize vendor selection by March 15',
        'Action item: Complete prototype testing by April 1',
    ]

    for item_text in bullet_items:
        para = doc.add_paragraph(item_text, style='List Bullet')

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
