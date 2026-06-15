"""
Initial Setup: Create batch blank PDF forms for employee data filling
Task ID: pdf_fm_050
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
TASK_ID = 'pdf_fm_050'
FORMS_DIR = f'{WORKDIR}/Documents/forms/batch_forms'


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


def create_blank_form(output_path: str):
    """Create a single-page PDF form with employee_name and employee_id fields, all empty."""
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)  # A4

    # Title
    page.insert_text(
        pymupdf.Point(72, 60),
        "Employee Information Form",
        fontsize=20,
        fontname="hebo",
        color=(0, 0, 0.5),
    )

    # Decorative line under title
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 72), pymupdf.Point(523, 72))
    shape.finish(color=(0, 0, 0.5), width=2)
    shape.commit()

    # Company info
    page.insert_text(
        pymupdf.Point(72, 105),
        "Meridian Technologies Inc.",
        fontsize=12,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(72, 122),
        "Human Resources Department - New Hire Onboarding",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # Section header
    page.insert_text(
        pymupdf.Point(72, 170),
        "Section 1: Employee Details",
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Employee Name label
    page.insert_text(
        pymupdf.Point(72, 210),
        "Employee Full Name:",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Employee Name field (text widget)
    widget_name = pymupdf.Widget()
    widget_name.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget_name.field_name = "employee_name"
    widget_name.field_value = ""
    widget_name.rect = pymupdf.Rect(230, 195, 500, 218)
    widget_name.text_fontsize = 12
    widget_name.text_color = (0, 0, 0)
    widget_name.fill_color = (0.97, 0.97, 0.97)
    widget_name.border_color = (0.4, 0.4, 0.4)
    widget_name.border_width = 1
    page.add_widget(widget_name)

    # Employee ID label
    page.insert_text(
        pymupdf.Point(72, 260),
        "Employee ID:",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Employee ID field (text widget)
    widget_id = pymupdf.Widget()
    widget_id.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget_id.field_name = "employee_id"
    widget_id.field_value = ""
    widget_id.rect = pymupdf.Rect(230, 245, 500, 268)
    widget_id.text_fontsize = 12
    widget_id.text_color = (0, 0, 0)
    widget_id.fill_color = (0.97, 0.97, 0.97)
    widget_id.border_color = (0.4, 0.4, 0.4)
    widget_id.border_width = 1
    page.add_widget(widget_id)

    # Additional form decoration
    page.insert_text(
        pymupdf.Point(72, 320),
        "Section 2: Department Assignment",
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0),
    )

    page.insert_text(
        pymupdf.Point(72, 350),
        "Department assignment will be completed by HR after processing.",
        fontsize=10,
        fontname="heit",
        color=(0.4, 0.4, 0.4),
    )

    # Footer
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(72, 780), pymupdf.Point(523, 780))
    shape2.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape2.commit()

    page.insert_text(
        pymupdf.Point(72, 800),
        "Confidential - Meridian Technologies Inc. - HR Form v3.2",
        fontsize=8,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    doc.save(output_path)
    doc.close()


def create_initial():
    # Create directory structure
    os.makedirs(FORMS_DIR, exist_ok=True)

    # Create 5 identical blank forms
    for i in range(1, 6):
        form_path = os.path.join(FORMS_DIR, f'form_{i:02d}.pdf')
        create_blank_form(form_path)
        print(f'Created blank form: {form_path}')

    print(f'All 5 blank forms created in {FORMS_DIR}')

    # Open file manager to show the forms directory
    launch_gui(f'nautilus "{FORMS_DIR}"', delay_sec=2.0)
    # Open one form to show it's blank
    launch_gui(f'evince "{FORMS_DIR}/form_01.pdf"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus and Evince with DISPLAY=:0')


create_initial()
