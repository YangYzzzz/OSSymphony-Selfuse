"""
Initial Setup: Create a fillable permit application PDF form
Task ID: pdf_basic_096
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

WORKDIR = '/home/user/Desktop'
TASK_ID = 'permit_application'
OUTPUT = f'{WORKDIR}/{TASK_ID}.pdf'


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
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)  # Letter size

    # --- Page header ---
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 36, 576, 90))
    shape.finish(color=(0.1, 0.2, 0.5), fill=(0.1, 0.2, 0.5), width=1)
    shape.commit()

    page.insert_text(
        pymupdf.Point(72, 72),
        "CITY OF AUSTIN — BUILDING PERMIT APPLICATION",
        fontsize=14,
        fontname="hebo",
        color=(1, 1, 1),
    )

    # --- Subtitle ---
    page.insert_text(
        pymupdf.Point(72, 108),
        "Please complete all fields below and submit to the Permit Office.",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # Draw a horizontal divider
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(36, 118), pymupdf.Point(576, 118))
    shape.finish(color=(0.6, 0.6, 0.6), width=1)
    shape.commit()

    # --- Section 1: Project Information ---
    page.insert_text(
        pymupdf.Point(36, 140),
        "SECTION 1: PROJECT INFORMATION",
        fontsize=11,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    # Label: Project Type
    page.insert_text(
        pymupdf.Point(36, 165),
        "Project Type:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Combo/dropdown widget for Project Type (initially empty/no selection)
    widget_project_type = pymupdf.Widget()
    widget_project_type.field_type = pymupdf.PDF_WIDGET_TYPE_COMBOBOX
    widget_project_type.field_name = "Project Type"
    widget_project_type.choice_values = [
        "Residential",
        "Commercial",
        "Industrial",
        "Mixed-Use",
        "Renovation",
        "Demolition",
    ]
    widget_project_type.field_value = ""
    widget_project_type.rect = pymupdf.Rect(160, 153, 400, 175)
    widget_project_type.text_fontsize = 10
    widget_project_type.fill_color = (1, 1, 1)
    widget_project_type.border_color = (0.4, 0.4, 0.4)
    widget_project_type.border_width = 1
    page.add_widget(widget_project_type)

    # Label: Property Address
    page.insert_text(
        pymupdf.Point(36, 200),
        "Property Address:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Text field: Property Address (empty)
    widget_address = pymupdf.Widget()
    widget_address.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget_address.field_name = "Property Address"
    widget_address.field_value = ""
    widget_address.rect = pymupdf.Rect(160, 188, 540, 210)
    widget_address.text_fontsize = 10
    widget_address.fill_color = (1, 1, 1)
    widget_address.border_color = (0.4, 0.4, 0.4)
    widget_address.border_width = 1
    page.add_widget(widget_address)

    # Label: Estimated Cost
    page.insert_text(
        pymupdf.Point(36, 235),
        "Estimated Cost:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Text field: Estimated Cost (empty)
    widget_cost = pymupdf.Widget()
    widget_cost.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget_cost.field_name = "Estimated Cost"
    widget_cost.field_value = ""
    widget_cost.rect = pymupdf.Rect(160, 223, 400, 245)
    widget_cost.text_fontsize = 10
    widget_cost.fill_color = (1, 1, 1)
    widget_cost.border_color = (0.4, 0.4, 0.4)
    widget_cost.border_width = 1
    page.add_widget(widget_cost)

    # Label: Start Date
    page.insert_text(
        pymupdf.Point(36, 270),
        "Start Date:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Text field: Start Date (empty)
    widget_date = pymupdf.Widget()
    widget_date.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget_date.field_name = "Start Date"
    widget_date.field_value = ""
    widget_date.rect = pymupdf.Rect(160, 258, 380, 280)
    widget_date.text_fontsize = 10
    widget_date.fill_color = (1, 1, 1)
    widget_date.border_color = (0.4, 0.4, 0.4)
    widget_date.border_width = 1
    page.add_widget(widget_date)

    # Hint text for date format
    page.insert_text(
        pymupdf.Point(385, 273),
        "(MM/DD/YYYY)",
        fontsize=8,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    # --- Section 2: Property Details ---
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(36, 298), pymupdf.Point(576, 298))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape.commit()

    page.insert_text(
        pymupdf.Point(36, 318),
        "SECTION 2: PROPERTY DETAILS",
        fontsize=11,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    # Label: Parcel Number
    page.insert_text(
        pymupdf.Point(36, 343),
        "Parcel Number:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )
    widget_parcel = pymupdf.Widget()
    widget_parcel.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget_parcel.field_name = "Parcel Number"
    widget_parcel.field_value = ""
    widget_parcel.rect = pymupdf.Rect(160, 331, 400, 353)
    widget_parcel.text_fontsize = 10
    widget_parcel.fill_color = (1, 1, 1)
    widget_parcel.border_color = (0.4, 0.4, 0.4)
    widget_parcel.border_width = 1
    page.add_widget(widget_parcel)

    # Label: Zoning District
    page.insert_text(
        pymupdf.Point(36, 378),
        "Zoning District:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )
    widget_zoning = pymupdf.Widget()
    widget_zoning.field_type = pymupdf.PDF_WIDGET_TYPE_COMBOBOX
    widget_zoning.field_name = "Zoning District"
    widget_zoning.choice_values = ["R1 - Single Family", "R2 - Multi-Family", "C1 - Commercial", "M1 - Industrial", "PUD - Planned"]
    widget_zoning.field_value = ""
    widget_zoning.rect = pymupdf.Rect(160, 366, 400, 388)
    widget_zoning.text_fontsize = 10
    widget_zoning.fill_color = (1, 1, 1)
    widget_zoning.border_color = (0.4, 0.4, 0.4)
    widget_zoning.border_width = 1
    page.add_widget(widget_zoning)

    # Label: Square Footage
    page.insert_text(
        pymupdf.Point(36, 413),
        "Square Footage:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )
    widget_sqft = pymupdf.Widget()
    widget_sqft.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget_sqft.field_name = "Square Footage"
    widget_sqft.field_value = ""
    widget_sqft.rect = pymupdf.Rect(160, 401, 400, 423)
    widget_sqft.text_fontsize = 10
    widget_sqft.fill_color = (1, 1, 1)
    widget_sqft.border_color = (0.4, 0.4, 0.4)
    widget_sqft.border_width = 1
    page.add_widget(widget_sqft)

    # --- Section 3: Applicant Information ---
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(36, 441), pymupdf.Point(576, 441))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape.commit()

    page.insert_text(
        pymupdf.Point(36, 461),
        "SECTION 3: APPLICANT INFORMATION",
        fontsize=11,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    # Label: Applicant Name
    page.insert_text(
        pymupdf.Point(36, 486),
        "Applicant Name:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )
    widget_name = pymupdf.Widget()
    widget_name.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget_name.field_name = "Applicant Name"
    widget_name.field_value = ""
    widget_name.rect = pymupdf.Rect(160, 474, 540, 496)
    widget_name.text_fontsize = 10
    widget_name.fill_color = (1, 1, 1)
    widget_name.border_color = (0.4, 0.4, 0.4)
    widget_name.border_width = 1
    page.add_widget(widget_name)

    # Label: Phone Number
    page.insert_text(
        pymupdf.Point(36, 521),
        "Phone Number:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )
    widget_phone = pymupdf.Widget()
    widget_phone.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget_phone.field_name = "Phone Number"
    widget_phone.field_value = ""
    widget_phone.rect = pymupdf.Rect(160, 509, 400, 531)
    widget_phone.text_fontsize = 10
    widget_phone.fill_color = (1, 1, 1)
    widget_phone.border_color = (0.4, 0.4, 0.4)
    widget_phone.border_width = 1
    page.add_widget(widget_phone)

    # Label: Email Address
    page.insert_text(
        pymupdf.Point(36, 556),
        "Email Address:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )
    widget_email = pymupdf.Widget()
    widget_email.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget_email.field_name = "Email Address"
    widget_email.field_value = ""
    widget_email.rect = pymupdf.Rect(160, 544, 540, 566)
    widget_email.text_fontsize = 10
    widget_email.fill_color = (1, 1, 1)
    widget_email.border_color = (0.4, 0.4, 0.4)
    widget_email.border_width = 1
    page.add_widget(widget_email)

    # --- Certification checkbox ---
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(36, 584), pymupdf.Point(576, 584))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape.commit()

    widget_cert = pymupdf.Widget()
    widget_cert.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    widget_cert.field_name = "Certification"
    widget_cert.field_value = "Off"
    widget_cert.rect = pymupdf.Rect(36, 595, 56, 615)
    widget_cert.border_color = (0, 0, 0)
    widget_cert.border_width = 1
    page.add_widget(widget_cert)

    page.insert_textbox(
        pymupdf.Rect(62, 590, 540, 625),
        "I certify that the information provided in this application is accurate and complete. "
        "I agree to comply with all applicable building codes, zoning regulations, and ordinances.",
        fontsize=9,
        fontname="helv",
        color=(0, 0, 0),
    )

    # --- Signature area ---
    page.insert_text(
        pymupdf.Point(36, 650),
        "Signature: _______________________________",
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(380, 650),
        "Date: ________________",
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
    )

    # --- Footer ---
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 700, 576, 756))
    shape.finish(color=(0.85, 0.85, 0.85), fill=(0.92, 0.92, 0.92), width=0.5)
    shape.commit()

    page.insert_textbox(
        pymupdf.Rect(42, 704, 570, 752),
        "City of Austin Development Services Department\n"
        "6310 Wilhelmina Delco Drive, Austin, TX 78752 | (512) 978-4000\n"
        "Office Hours: Monday–Friday 8:00 AM – 4:00 PM\n"
        "Form Version: 2025-01 | Permit Fee Schedule Available at austintexas.gov",
        fontsize=8,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    # Set metadata
    doc.set_metadata({
        "title": "Building Permit Application",
        "author": "City of Austin Development Services",
        "subject": "Permit Application Form",
        "keywords": "permit, building, construction, Austin, Texas",
        "creator": "CUA-Gym Setup",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the form in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
