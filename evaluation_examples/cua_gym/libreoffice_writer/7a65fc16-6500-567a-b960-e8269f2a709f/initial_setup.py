"""
Initial Setup: Bullet list with black 11pt bullets and 11pt text
Task ID: writer_list_021
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time

from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_list_021'
OUTPUT = f'{WORKDIR}/Desktop/highlights.docx'


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
    import os as _os
    _os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    doc = Document()

    bullet_items = [
        "Record-breaking Q3 revenue of $12.5M",
        "Customer satisfaction score increased to 94%",
        "Successfully launched mobile application",
        "Opened three new regional offices",
        "Employee retention rate above 92%",
    ]

    for item in bullet_items:
        para = doc.add_paragraph(item, style='List Bullet')
        # Ensure paragraph-level rPr has no special color/size for bullet char
        # (default: no pPr/rPr, so bullet inherits normal black 11pt)
        pPr = para._p.get_or_add_pPr()
        # Remove any existing rPr in pPr to ensure clean initial state
        for existing_rpr in pPr.findall(qn('w:rPr')):
            pPr.remove(existing_rpr)
        # Also ensure each text run is 11pt black (not red)
        for run in para.runs:
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(0, 0, 0)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
