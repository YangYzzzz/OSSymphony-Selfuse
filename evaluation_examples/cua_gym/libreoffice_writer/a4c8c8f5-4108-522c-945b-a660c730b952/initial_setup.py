"""
Initial Setup: Create task_list.docx with 10 task lines, some ending in periods and some not.
Task ID: writer_edit_028
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_edit_028'
# Task says file is at ~/Desktop/task_list.docx
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/task_list.docx'


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
    os.makedirs(DESKTOP, exist_ok=True)

    doc = Document()

    # 10 task lines as specified in context:
    # Some already end with periods (lines 1, 3, 6, 8)
    # Some do NOT end with periods (lines 2, 4, 5, 7, 9, 10)
    tasks = [
        'Complete the budget review.',      # already has period
        'Submit expense reports',           # no period
        'Schedule team meeting.',           # already has period
        'Update project timeline',          # no period
        'Review vendor contracts',          # no period
        'Prepare presentation slides.',     # already has period
        'Order office supplies',            # no period
        'File quarterly taxes.',            # already has period
        'Organize training session',        # no period
        'Send client invoices',             # no period
    ]

    for task in tasks:
        doc.add_paragraph(task)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
