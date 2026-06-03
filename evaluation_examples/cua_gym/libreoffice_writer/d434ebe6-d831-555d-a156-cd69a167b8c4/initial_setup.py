"""
Initial Setup: Apply bullet/numbered list formatting to document paragraphs
Task ID: writer_list_032
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
from docx import Document

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'writer_list_032'
OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'
DESKTOP_PATH = f'{WORKDIR}/Desktop/project_notes.docx'


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

    # Ten plain text paragraphs — NO list formatting applied
    paragraphs_text = [
        "Important considerations for the project",
        "Budget constraints must be addressed early",
        "Stakeholder communication is critical",
        "Risk assessment should be ongoing",
        "Quality assurance cannot be compromised",
        "Gather requirements from all departments",
        "Create detailed design specifications",
        "Implement core features first",
        "Conduct thorough testing",
        "Deploy to production environment",
    ]

    for text in paragraphs_text:
        # Add as plain 'Normal' paragraph — no list style
        doc.add_paragraph(text, style='Normal')

    # Save canonical artifact
    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # Also save to the Desktop path referenced in the task instruction
    import shutil
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)
    shutil.copy(OUTPUT, DESKTOP_PATH)
    print(f'Copied to Desktop: {DESKTOP_PATH}')

    # GUI-ready startup: open the Desktop file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{DESKTOP_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
