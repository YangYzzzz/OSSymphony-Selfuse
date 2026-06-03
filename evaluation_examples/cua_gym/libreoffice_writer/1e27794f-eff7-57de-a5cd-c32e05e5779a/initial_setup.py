"""
Initial Setup: Blank document for thank-you letter
Task ID: writer_wf_044
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
from docx import Document
from docx.shared import Cm

WORKDIR = '/home/user'
TASK_ID = 'writer_wf_044'
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

    # Set 2.54cm margins (matching task requirement as starting point)
    # The task says to "set 2.54cm margins" so initial should have default margins
    # Default margins in python-docx are 1 inch = 2.54cm already, but let's
    # leave them as default so the agent still needs to verify/set them.
    section = doc.sections[0]
    # Default python-docx margins are 1 inch (2.54cm) - leave as is
    # The document is blank - no content at all

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # Open in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
