"""
Initial Setup: Create a blank document for Avery 5160 label task
Task ID: writer_lec_041
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_041'
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
    # Create a blank document - the agent needs to create labels from scratch
    doc = Document()

    # Set page to US Letter
    section = doc.sections[0]
    from docx.shared import Inches
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(0.1875)   # Avery 5160 side margin ~0.1875"
    section.right_margin = Inches(0.1875)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)

    # Add a single empty paragraph so the document isn't completely empty
    doc.add_paragraph("")

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # Launch LibreOffice Writer with the blank document
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
