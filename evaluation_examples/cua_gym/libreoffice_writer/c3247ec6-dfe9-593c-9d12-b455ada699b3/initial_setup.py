"""
Initial Setup: Create plain-text project plan document for multi-level list task
Task ID: writer_list_005
Domain: libreoffice_writer

Creates ~/Desktop/project_plan.docx with nine plain paragraphs (no list formatting).
The agent's task is to convert these into a multi-level numbered list.
"""

import subprocess
subprocess.run(['pip3', 'install', 'python-docx'], check=True, capture_output=True)

import os
import shlex
import time
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_list_005'
OUTPUT = f'{WORKDIR}/Desktop/project_plan.docx'


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

    # Nine plain text paragraphs (no list formatting, no indentation)
    # These are intended to form a two-level outline but are currently plain text
    paragraphs = [
        'Research Phase',
        'Conduct market analysis',
        'Review competitor products',
        'Design Phase',
        'Create wireframes',
        'Design user interface mockups',
        'Write technical specifications',
        'Implementation Phase',
        'Set up development environment',
        'Develop core features',
    ]

    for text in paragraphs:
        # Add as plain "Normal" paragraphs — no list style applied
        para = doc.add_paragraph(text)
        # Explicitly keep Normal style (default); do NOT apply List Number or List Number 2

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
