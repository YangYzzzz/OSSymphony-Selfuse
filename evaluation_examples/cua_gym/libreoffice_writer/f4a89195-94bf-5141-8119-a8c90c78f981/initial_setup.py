"""
Initial Setup: Class grades table in LibreOffice Writer (without Average row)
Task ID: writer_tbl_077
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'class_grades'
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

    # Create a 6-row x 4-column table (header + 5 student rows)
    table = doc.add_table(rows=6, cols=4)
    table.style = 'Table Grid'

    # Row 1: header
    header_cells = table.rows[0].cells
    header_cells[0].text = 'Student'
    header_cells[1].text = 'Homework'
    header_cells[2].text = 'Midterm'
    header_cells[3].text = 'Final'

    # Row 2: Amy
    row2 = table.rows[1].cells
    row2[0].text = 'Amy'
    row2[1].text = '85'
    row2[2].text = '78'
    row2[3].text = '90'

    # Row 3: Ben
    row3 = table.rows[2].cells
    row3[0].text = 'Ben'
    row3[1].text = '92'
    row3[2].text = '88'
    row3[3].text = '85'

    # Row 4: Carla
    row4 = table.rows[3].cells
    row4[0].text = 'Carla'
    row4[1].text = '78'
    row4[2].text = '82'
    row4[3].text = '88'

    # Row 5: Dan
    row5 = table.rows[4].cells
    row5[0].text = 'Dan'
    row5[1].text = '95'
    row5[2].text = '90'
    row5[3].text = '92'

    # Row 6: Eva
    row6 = table.rows[5].cells
    row6[0].text = 'Eva'
    row6[1].text = '80'
    row6[2].text = '72'
    row6[3].text = '78'

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
