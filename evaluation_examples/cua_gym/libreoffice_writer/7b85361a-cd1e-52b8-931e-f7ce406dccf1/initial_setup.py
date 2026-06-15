"""
Initial Setup: Create a blank Letterhead_Template.docx with Letter page size and 2.54cm margins.
Task ID: writer_pd_042
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
from docx import Document
from docx.shared import Cm

WORKDIR = '/home/user'
TASK_ID = 'writer_pd_042'
OUTPUT = f'{WORKDIR}/Letterhead_Template.docx'


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

    # Set page size to Letter (8.5" x 11") and 2.54cm margins
    section = doc.sections[0]
    section.page_width = Cm(21.59)   # 8.5 inches
    section.page_height = Cm(27.94)  # 11 inches
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)

    # Ensure no header/footer (default Document has none, but be explicit)
    section.header.is_linked_to_previous = True
    section.footer.is_linked_to_previous = True

    # No content - blank document
    # Remove the default empty paragraph if there is one
    # (Document() creates one empty paragraph by default, which is fine for a blank doc)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # Open in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
