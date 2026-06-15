"""
Initial Setup: Set up envelope printing for mail merge
Task ID: writer_mt_012
Domain: libreoffice_writer

Creates a blank document. The task requires the user to set up envelope
printing with mail merge, so the initial state is simply a blank document
open in LibreOffice Writer.
"""

import os
import shlex
import subprocess
import time
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_012'
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
    doc = Document()

    # A blank document - the user needs to create the envelope from scratch
    # Add a single empty paragraph (default in a new document)
    # The document is intentionally blank as the task is to create an envelope

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # Open in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
