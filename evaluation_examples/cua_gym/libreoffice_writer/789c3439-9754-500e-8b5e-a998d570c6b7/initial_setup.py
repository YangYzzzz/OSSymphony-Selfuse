"""
Initial Setup: Create a blank document for label creation task.
Task ID: writer_lec_061
Domain: libreoffice_writer

The initial state is a blank document open in LibreOffice Writer.
"""

import os
import shlex
import subprocess
import time
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_061'
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
    # Create a blank document — the task starts from a blank state
    doc = Document()

    # Set standard US Letter page (Avery 5160 is designed for Letter)
    section = doc.sections[0]
    from docx.shared import Inches
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(0.19)
    section.right_margin = Inches(0.19)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # Open in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
