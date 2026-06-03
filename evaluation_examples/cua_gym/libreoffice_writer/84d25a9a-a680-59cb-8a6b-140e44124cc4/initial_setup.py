"""
Initial Setup: Tic-Tac-Toe Game Board Document
Task ID: writer_tbl_015
Domain: libreoffice_writer

Creates a document with a heading "Tic-Tac-Toe Game" on ~/Desktop/.
The document contains ONLY the heading — no table yet (agent must add it).
"""

import os
import shlex
import subprocess
import time

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user/Desktop'
TASK_ID = 'game_board'
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

    # Add heading "Tic-Tac-Toe Game" at Heading 1 level
    heading = doc.add_heading("Tic-Tac-Toe Game", level=1)
    heading.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

    # Save document — NO table (agent must create it)
    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
