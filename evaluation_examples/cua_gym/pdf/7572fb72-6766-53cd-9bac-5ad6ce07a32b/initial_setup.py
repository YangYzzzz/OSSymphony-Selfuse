"""
Initial Setup: Create a static PDF with labels for a project request form.
Task ID: pdf_pw_018
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_018'
FORMS_DIR = f'{WORKDIR}/forms'
OUTPUT = f'{FORMS_DIR}/project_request.pdf'

# Letter size
PAGE_W = 612
PAGE_H = 792


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
    os.makedirs(FORMS_DIR, exist_ok=True)

    doc = pymupdf.open()
    page = doc.new_page(width=PAGE_W, height=PAGE_H)

    # Title
    page.insert_text(
        pymupdf.Point(72, 60),
        "Project Request Form",
        fontsize=22,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    # Horizontal rule under title
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 75), pymupdf.Point(540, 75))
    shape.finish(color=(0.3, 0.3, 0.3), width=1.0)
    shape.commit()

    # Labels positioned vertically with 50-point spacing starting at y=120
    labels = [
        (120, "Project Name:"),
        (170, "Requester:"),
        (220, "Budget Estimate:"),
        (270, "Priority:"),
        (320, "Description:"),
        (420, "Approved:"),  # description area is tall, so approved is further down
    ]

    for y, label in labels:
        page.insert_text(
            pymupdf.Point(72, y),
            label,
            fontsize=12,
            fontname="hebo",
            color=(0, 0, 0),
        )

    # No form fields -- this is the initial state (static labels only)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
