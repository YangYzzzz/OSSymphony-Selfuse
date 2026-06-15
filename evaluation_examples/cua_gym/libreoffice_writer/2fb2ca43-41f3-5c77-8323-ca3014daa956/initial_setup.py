"""
Initial Setup: Create contract_sections.docx with five plain text paragraphs
Task ID: writer_list_047
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time

from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_list_047'
OUTPUT = f'{WORKDIR}/contract_sections.docx'


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

    # Add the five plain text paragraphs as Normal style (no list formatting)
    sections = [
        "Definitions and Interpretations",
        "Rights and Obligations of Parties",
        "Payment Terms and Conditions",
        "Confidentiality and Non-Disclosure",
        "Termination and Dispute Resolution",
    ]

    for section_text in sections:
        para = doc.add_paragraph(section_text)
        para.style = doc.styles['Normal']

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
