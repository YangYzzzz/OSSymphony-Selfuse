"""
Initial Setup: Apply 'List Bullet' style to document paragraphs
Task ID: writer_list_056
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
from docx import Document

WORKDIR = '/home/user/Desktop'  # VM path — file is on Desktop per task context
TASK_ID = 'daily_checklist'
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

    # Add five plain text paragraphs in Default Paragraph Style (no bullet style)
    # These are the exact paragraphs specified in the task context
    paragraphs = [
        "Check server health dashboard",
        "Review overnight error logs",
        "Verify backup completion status",
        "Monitor disk space utilization",
        "Confirm scheduled jobs executed successfully",
    ]

    for text in paragraphs:
        # Use default style (Normal) — no bullet, no list style
        para = doc.add_paragraph(text)
        # Explicitly set to Normal style to ensure no bullet formatting
        para.style = doc.styles['Normal']

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
