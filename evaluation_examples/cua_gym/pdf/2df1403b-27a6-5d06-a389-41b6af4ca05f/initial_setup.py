"""
Initial Setup: Fillable PDF claim form for Evince form-filling task.
Task ID: pdf_basic_128
Domain: pdf

Creates a fillable PDF claim form at ~/Desktop/claim_form.pdf with:
  - Text field: 'Claim Number'
  - Text field: 'Date of Incident'
  - Text field: 'Description'
  - Combo box (dropdown): 'Claim Type' with options including 'Property Damage'

All fields are left empty (initial state).
Launches Evince to display the form.
"""

import os
import shlex
import subprocess
import time

import pymupdf

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/claim_form.pdf'


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
    os.makedirs(DESKTOP, exist_ok=True)

    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)  # Letter size

    # -----------------------------------------------------------------------
    # Background and title
    # -----------------------------------------------------------------------
    shape = page.new_shape()

    # Header bar background
    shape.draw_rect(pymupdf.Rect(0, 0, 612, 80))
    shape.finish(color=None, fill=(0.1, 0.3, 0.6))

    # Form border
    shape.draw_rect(pymupdf.Rect(40, 90, 572, 750))
    shape.finish(color=(0.7, 0.7, 0.7), fill=None, width=1)

    # Section divider line under Claimant Info
    shape.draw_line(pymupdf.Point(40, 290), pymupdf.Point(572, 290))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)

    # Section divider line under Incident Details
    shape.draw_line(pymupdf.Point(40, 490), pymupdf.Point(572, 490))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)

    shape.commit()

    # -----------------------------------------------------------------------
    # Title text
    # -----------------------------------------------------------------------
    page.insert_text(
        pymupdf.Point(306, 30),
        "INSURANCE CLAIM FORM",
        fontsize=20,
        fontname="hebo",
        color=(1, 1, 1),
    )
    page.insert_text(
        pymupdf.Point(306, 58),
        "Meridian Insurance Group — Claim Services Division",
        fontsize=9,
        fontname="helv",
        color=(0.9, 0.9, 0.9),
    )

    # Section headers
    page.insert_text(
        pymupdf.Point(55, 120),
        "CLAIM INFORMATION",
        fontsize=10,
        fontname="hebo",
        color=(0.1, 0.3, 0.6),
    )

    page.insert_text(
        pymupdf.Point(55, 310),
        "CLAIMANT INFORMATION",
        fontsize=10,
        fontname="hebo",
        color=(0.1, 0.3, 0.6),
    )

    page.insert_text(
        pymupdf.Point(55, 510),
        "INCIDENT DESCRIPTION",
        fontsize=10,
        fontname="hebo",
        color=(0.1, 0.3, 0.6),
    )

    # -----------------------------------------------------------------------
    # Field labels
    # -----------------------------------------------------------------------
    labels = [
        (55, 155, "Claim Number:"),
        (55, 205, "Date of Incident:"),
        (55, 255, "Claim Type:"),
        (55, 335, "Claimant Name:"),
        (55, 375, "Policy Number:"),
        (55, 415, "Contact Phone:"),
        (55, 455, "Email Address:"),
        (55, 535, "Description of Incident:"),
        (55, 680, "Estimated Damage Amount:"),
        (55, 720, "Supporting Documents:"),
    ]
    for x, y, text in labels:
        page.insert_text(pymupdf.Point(x, y), text, fontsize=10, fontname="hebo", color=(0.2, 0.2, 0.2))

    # -----------------------------------------------------------------------
    # Instructional footer text
    # -----------------------------------------------------------------------
    page.insert_text(
        pymupdf.Point(55, 765),
        "Please complete all required fields and save the form. Attach supporting documents when submitting.",
        fontsize=7.5,
        fontname="tiit",
        color=(0.5, 0.5, 0.5),
    )

    # -----------------------------------------------------------------------
    # Form fields (widgets)
    # -----------------------------------------------------------------------

    # --- Claim Number (text field) ---
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "Claim Number"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, 138, 550, 162)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 1.0)
    w.border_color = (0.4, 0.4, 0.7)
    w.border_width = 1
    page.add_widget(w)

    # --- Date of Incident (text field) ---
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "Date of Incident"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, 188, 400, 212)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 1.0)
    w.border_color = (0.4, 0.4, 0.7)
    w.border_width = 1
    page.add_widget(w)

    # --- Claim Type (combobox/dropdown) ---
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_COMBOBOX
    w.field_name = "Claim Type"
    w.choice_values = [
        "-- Select Claim Type --",
        "Auto Damage",
        "Bodily Injury",
        "Liability",
        "Medical Expense",
        "Property Damage",
        "Theft",
        "Weather Damage",
        "Other",
    ]
    w.field_value = "-- Select Claim Type --"
    w.rect = pymupdf.Rect(200, 238, 450, 262)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 1.0)
    w.border_color = (0.4, 0.4, 0.7)
    w.border_width = 1
    page.add_widget(w)

    # --- Claimant Name ---
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "Claimant Name"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, 318, 550, 342)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 1.0)
    w.border_color = (0.4, 0.4, 0.7)
    w.border_width = 1
    page.add_widget(w)

    # --- Policy Number ---
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "Policy Number"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, 358, 400, 382)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 1.0)
    w.border_color = (0.4, 0.4, 0.7)
    w.border_width = 1
    page.add_widget(w)

    # --- Contact Phone ---
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "Contact Phone"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, 398, 380, 422)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 1.0)
    w.border_color = (0.4, 0.4, 0.7)
    w.border_width = 1
    page.add_widget(w)

    # --- Email Address ---
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "Email Address"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, 438, 480, 462)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 1.0)
    w.border_color = (0.4, 0.4, 0.7)
    w.border_width = 1
    page.add_widget(w)

    # --- Description (multi-line text field) ---
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "Description"
    w.field_value = ""
    w.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
    w.rect = pymupdf.Rect(55, 548, 550, 655)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 1.0)
    w.border_color = (0.4, 0.4, 0.7)
    w.border_width = 1
    page.add_widget(w)

    # --- Estimated Damage Amount ---
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "Estimated Damage Amount"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, 663, 380, 687)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 1.0)
    w.border_color = (0.4, 0.4, 0.7)
    w.border_width = 1
    page.add_widget(w)

    # --- Supporting Documents (checkbox) ---
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "Supporting Documents"
    w.field_value = "Off"
    w.rect = pymupdf.Rect(200, 706, 222, 728)
    w.border_color = (0.3, 0.3, 0.3)
    w.border_width = 1
    page.add_widget(w)

    page.insert_text(
        pymupdf.Point(228, 722),
        "Attached",
        fontsize=10,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial form created: {OUTPUT}')

    # GUI-ready: open claim_form.pdf in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: Evince launched with claim_form.pdf')


create_initial()
