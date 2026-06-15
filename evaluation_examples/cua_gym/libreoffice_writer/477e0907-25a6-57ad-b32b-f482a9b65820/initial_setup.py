"""
Initial Setup: Create a class roster document with 25 names in 'FirstName LastName' format.
Task ID: writer_frd_021
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_021'
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

NAMES = [
    "Alice Johnson",
    "Bob Smith",
    "Catherine Rivera",
    "David Nakamura",
    "Elena Petrov",
    "Frank Donovan",
    "Grace Kim",
    "Henry Chang",
    "Isabella Martinez",
    "James Okonkwo",
    "Karen Walsh",
    "Leo Fernandez",
    "Maria Johansson",
    "Nathan Brooks",
    "Olivia Sato",
    "Patrick Novak",
    "Quinn Harper",
    "Rachel Stein",
    "Samuel Okafor",
    "Tanya Volkov",
    "Ulrich Weber",
    "Victoria Reyes",
    "William Tan",
    "Xena Morales",
    "Yusuf Abdi",
]

def create_initial():
    doc = Document()

    # Add each name as a separate paragraph (no heading, roster-only document)
    for name in NAMES:
        para = doc.add_paragraph(name)
        for run in para.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(12)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # Open in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')

create_initial()
