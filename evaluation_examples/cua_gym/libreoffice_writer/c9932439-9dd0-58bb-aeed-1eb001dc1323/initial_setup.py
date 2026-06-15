"""
Initial Setup: Creative writing document with 8 paragraphs, all at 0cm left indent.
Task ID: wrpara_041
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'wrpara_041'
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
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

    # 8 short creative writing paragraphs - all at 0cm left indent (default)
    paragraphs = [
        "The morning fog clung to the harbor like a silver blanket, muffling the cries of gulls circling above the wooden docks.",
        "Elena adjusted the worn leather strap of her satchel and stepped onto the cobblestone path that wound toward the lighthouse.",
        "Inside the keeper's cottage, a fire crackled in the stone hearth, casting dancing shadows across shelves lined with nautical charts and faded logbooks.",
        "She traced her finger along the coastline drawn in sepia ink, pausing at the small island marked with a crimson X.",
        "The tide would turn at midnight, and with it would come the narrow window she had been waiting three months to exploit.",
        "Captain Aldric had warned her about the reef, but his charts were forty years old and the sea had reshaped the passage since then.",
        "She folded the map carefully, tucked it into her coat pocket, and stepped outside into the salt-tinged wind.",
        "Somewhere beyond the mist, the island waited with its secrets buried beneath centuries of sand and silence.",
    ]

    for text in paragraphs:
        para = doc.add_paragraph(text)
        # Ensure 0cm left indent explicitly (default, but be clear)
        para.paragraph_format.left_indent = Pt(0)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
