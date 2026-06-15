"""
Initial Setup: Blank Writer document template for meeting minutes
Task ID: writer_rd_045
Domain: libreoffice_writer

Creates a blank .ott template file with A4 dimensions and no content,
fields, or special formatting. Opens it in LibreOffice Writer.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_045'
OUTPUT_DOCX = f'{WORKDIR}/{TASK_ID}.docx'
OUTPUT_OTT = f'{WORKDIR}/{TASK_ID}.ott'


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
    from docx import Document
    from docx.shared import Cm

    # Create a blank document with A4 page size
    doc = Document()

    # Set A4 page dimensions
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)

    # Save as .docx first
    doc.save(OUTPUT_DOCX)
    print(f'Blank docx created: {OUTPUT_DOCX}')

    # Convert to .ott using LibreOffice headless
    result = subprocess.run(
        ['libreoffice', '--headless', '--convert-to', 'ott', OUTPUT_DOCX, '--outdir', WORKDIR],
        capture_output=True, text=True, timeout=30,
        env={**os.environ, 'HOME': '/home/user'}
    )
    print(f'Conversion stdout: {result.stdout}')
    print(f'Conversion stderr: {result.stderr}')

    # Verify .ott exists
    if os.path.exists(OUTPUT_OTT):
        print(f'Initial .ott template created: {OUTPUT_OTT}')
        # Remove intermediate .docx
        os.remove(OUTPUT_DOCX)
    else:
        print(f'WARNING: .ott conversion may have failed, keeping .docx')

    # Open the .ott file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT_OTT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
