"""
Initial Setup: Create a static PDF with label text for an employee onboarding form.
Task ID: pdf_pw_003
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_003'
FORMS_DIR = f'{WORKDIR}/forms'
OUTPUT = f'{FORMS_DIR}/employee_onboarding.pdf'

# Letter size in points
LETTER_WIDTH = 612
LETTER_HEIGHT = 792


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
    page = doc.new_page(width=LETTER_WIDTH, height=LETTER_HEIGHT)

    # Title
    page.insert_text(
        pymupdf.Point(72, 60),
        "Employee Onboarding Form",
        fontsize=20,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Horizontal line under title
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 70), pymupdf.Point(540, 70))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    # Labels at the vertical positions matching the task specification
    labels = [
        ("Full Name:", 72, 115),
        ("Employee ID:", 72, 165),
        ("Start Date:", 72, 215),
        ("Department:", 72, 265),
        ("NDA Signed:", 72, 315),
    ]

    for text, x, y in labels:
        page.insert_text(
            pymupdf.Point(x, y),
            text,
            fontsize=12,
            fontname="hebo",
            color=(0, 0, 0),
        )

    # Instructions at the bottom
    page.insert_text(
        pymupdf.Point(72, 400),
        "Please complete all fields above. Return this form to HR within 3 business days.",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    page.insert_text(
        pymupdf.Point(72, 420),
        "For questions, contact hr@acmecorp.com or extension 4200.",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
