"""
Initial Setup: PDF Form Fill Task
Task ID: pdf_cross_109
Domain: pdf

Creates:
  - ~/Documents/application_form.pdf  (2-page fillable PDF with empty fields)
  - ~/Documents/form_data.json        (JSON with field data to be used by agent)
  - ~/scripts/ directory              (exists, but no pdf_form_fill.py yet)

Opens application_form.pdf in Evince for the agent.
"""

import json
import os
import shlex
import subprocess
import time

import pymupdf

WORKDIR = '/home/user'
DOCS_DIR = f'{WORKDIR}/Documents'
SCRIPTS_DIR = f'{WORKDIR}/scripts'
FORM_PDF = f'{DOCS_DIR}/application_form.pdf'
FORM_JSON = f'{DOCS_DIR}/form_data.json'


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


def create_form_pdf():
    """Create a 2-page fillable PDF application form with empty form fields."""
    doc = pymupdf.open()

    # ---- PAGE 1: Personal Information ----
    page1 = doc.new_page(width=612, height=792)  # US Letter

    # Title
    page1.insert_text(
        pymupdf.Point(72, 60),
        "Personal Information Application Form",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )
    page1.insert_text(
        pymupdf.Point(72, 85),
        "Please complete all fields accurately.",
        fontsize=11,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )

    # Horizontal divider
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(540, 95))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    # Field labels
    label_x = 72
    field_x = 200
    field_w = 340
    fields_page1 = [
        ("Full Name:", "name", 140),
        ("Address:", "address", 200),
        ("Phone:", "phone", 260),
        ("Email:", "email", 320),
    ]

    for label, field_name, y in fields_page1:
        # Label
        page1.insert_text(
            pymupdf.Point(label_x, y),
            label,
            fontsize=11,
            fontname="hebo",
            color=(0.1, 0.1, 0.1),
        )
        # Empty form field widget
        widget = pymupdf.Widget()
        widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
        widget.field_name = field_name
        widget.field_value = ""
        widget.rect = pymupdf.Rect(field_x, y - 14, field_x + field_w, y + 4)
        widget.text_fontsize = 11
        widget.text_color = (0, 0, 0)
        widget.fill_color = (0.97, 0.97, 1.0)
        widget.border_color = (0.4, 0.4, 0.6)
        widget.border_width = 1
        page1.add_widget(widget)

    # Section heading
    page1.insert_text(
        pymupdf.Point(72, 380),
        "Instructions:",
        fontsize=12,
        fontname="hebo",
        color=(0.2, 0.3, 0.6),
    )
    page1.insert_textbox(
        pymupdf.Rect(72, 395, 540, 500),
        (
            "1. Enter your full legal name as it appears on your government-issued ID.\n"
            "2. Provide your current mailing address including city, state, and ZIP.\n"
            "3. Include area code with your phone number.\n"
            "4. Use a valid email address you check regularly.\n"
            "5. Date of birth should be in YYYY-MM-DD format.\n"
            "6. Signature field should contain your typed full name."
        ),
        fontsize=10,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
        align=0,
    )

    # Page number
    page1.insert_text(
        pymupdf.Point(270, 760),
        "Page 1 of 2",
        fontsize=9,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    # ---- PAGE 2: Additional Information & Signature ----
    page2 = doc.new_page(width=612, height=792)

    # Title
    page2.insert_text(
        pymupdf.Point(72, 60),
        "Additional Information & Declaration",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 75), pymupdf.Point(540, 75))
    shape2.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape2.commit()

    # DOB field
    page2.insert_text(
        pymupdf.Point(72, 120),
        "Date of Birth:",
        fontsize=11,
        fontname="hebo",
        color=(0.1, 0.1, 0.1),
    )
    dob_widget = pymupdf.Widget()
    dob_widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    dob_widget.field_name = "dob"
    dob_widget.field_value = ""
    dob_widget.rect = pymupdf.Rect(200, 106, 400, 124)
    dob_widget.text_fontsize = 11
    dob_widget.text_color = (0, 0, 0)
    dob_widget.fill_color = (0.97, 0.97, 1.0)
    dob_widget.border_color = (0.4, 0.4, 0.6)
    dob_widget.border_width = 1
    page2.add_widget(dob_widget)

    page2.insert_text(
        pymupdf.Point(410, 120),
        "(YYYY-MM-DD)",
        fontsize=9,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    # Declaration text
    page2.insert_text(
        pymupdf.Point(72, 200),
        "Declaration:",
        fontsize=12,
        fontname="hebo",
        color=(0.2, 0.3, 0.6),
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 215, 540, 320),
        (
            "I hereby declare that the information provided in this application is true, "
            "complete, and accurate to the best of my knowledge and belief. I understand "
            "that any misrepresentation or omission of facts may result in disqualification "
            "from the application process or termination of services. I consent to the "
            "verification of the information provided and agree to the terms and conditions "
            "of this application."
        ),
        fontsize=10,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Signature field label
    page2.insert_text(
        pymupdf.Point(72, 370),
        "Signature:",
        fontsize=11,
        fontname="hebo",
        color=(0.1, 0.1, 0.1),
    )
    sig_widget = pymupdf.Widget()
    sig_widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    sig_widget.field_name = "signature"
    sig_widget.field_value = ""
    sig_widget.rect = pymupdf.Rect(200, 355, 540, 375)
    sig_widget.text_fontsize = 12
    sig_widget.text_color = (0.0, 0.0, 0.6)
    sig_widget.fill_color = (0.97, 0.97, 1.0)
    sig_widget.border_color = (0.3, 0.3, 0.5)
    sig_widget.border_width = 1
    page2.add_widget(sig_widget)

    # Signature underline visual
    shape3 = page2.new_shape()
    shape3.draw_line(pymupdf.Point(200, 376), pymupdf.Point(540, 376))
    shape3.finish(color=(0.3, 0.3, 0.5), width=0.5)
    shape3.commit()

    page2.insert_text(
        pymupdf.Point(72, 420),
        "Date Submitted:",
        fontsize=11,
        fontname="hebo",
        color=(0.1, 0.1, 0.1),
    )
    page2.insert_text(
        pymupdf.Point(200, 420),
        "_______________________",
        fontsize=11,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    # Office use only box
    shape4 = page2.new_shape()
    shape4.draw_rect(pymupdf.Rect(72, 480, 540, 600))
    shape4.finish(color=(0.5, 0.5, 0.5), fill=(0.95, 0.95, 0.95), width=1)
    shape4.commit()

    page2.insert_text(
        pymupdf.Point(80, 498),
        "FOR OFFICE USE ONLY",
        fontsize=10,
        fontname="hebo",
        color=(0.4, 0.4, 0.4),
    )
    page2.insert_text(
        pymupdf.Point(80, 520),
        "Application ID: ___________",
        fontsize=10,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    page2.insert_text(
        pymupdf.Point(80, 540),
        "Received by: ___________",
        fontsize=10,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    page2.insert_text(
        pymupdf.Point(80, 560),
        "Date: ___________",
        fontsize=10,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    page2.insert_text(
        pymupdf.Point(80, 580),
        "Status: [ ] Approved   [ ] Pending   [ ] Rejected",
        fontsize=10,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )

    # Page number
    page2.insert_text(
        pymupdf.Point(270, 760),
        "Page 2 of 2",
        fontsize=9,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    # Save metadata
    doc.set_metadata({
        "title": "Personal Information Application Form",
        "author": "Application Services",
        "subject": "Fillable PDF Application Form",
        "keywords": "application, form, fillable",
        "creator": "CUA-Gym Setup",
    })

    doc.save(FORM_PDF)
    doc.close()
    print(f'Form PDF created: {FORM_PDF}')


def create_form_json():
    """Create the form data JSON file."""
    form_data = {
        "name": "Sarah Mitchell",
        "address": "789 Pine Street, Denver, CO 80202",
        "phone": "(303) 555-0198",
        "email": "sarah.m@email.com",
        "date_of_birth": "1990-07-22",
        "signature_text": "Sarah Mitchell"
    }
    with open(FORM_JSON, 'w') as f:
        json.dump(form_data, f, indent=2)
    print(f'Form JSON created: {FORM_JSON}')


def main():
    # Create directories
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    print(f'Directories ensured: {DOCS_DIR}, {SCRIPTS_DIR}')

    # Create initial files
    create_form_pdf()
    create_form_json()

    # Verify files exist
    assert os.path.exists(FORM_PDF), f'Missing: {FORM_PDF}'
    assert os.path.exists(FORM_JSON), f'Missing: {FORM_JSON}'

    # GUI-ready startup: open the form PDF in Evince
    launch_gui(f'evince "{FORM_PDF}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with application_form.pdf on DISPLAY=:0')


main()
