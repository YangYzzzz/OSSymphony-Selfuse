"""
Initial Setup: Create numbered_list.docx with 8 numbered items (period + space format)
Task ID: writer_edit_061
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
from docx import Document

WORKDIR = '/home/user/Desktop'  # VM path — file is on the Desktop
TASK_ID = 'writer_edit_061'
OUTPUT = f'{WORKDIR}/numbered_list.docx'


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

    # 8 numbered items formatted as: "N. Text" (period + space + text)
    items = [
        "1. First item",
        "2. Second item",
        "3. Third item",
        "4. Fourth item",
        "5. Fifth item",
        "6. Sixth item",
        "7. Seventh item",
        "8. Eighth item",
    ]

    for item in items:
        doc.add_paragraph(item)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
