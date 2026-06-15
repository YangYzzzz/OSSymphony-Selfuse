"""
Initial Setup: Create insurance claim form PDF with empty fields
Task ID: pdf_fm_031
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_031'
FORMS_DIR = f'{WORKDIR}/Documents/forms'
OUTPUT = f'{FORMS_DIR}/claim_form.pdf'

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

    # ===== PAGE 1: Claimant & Loss Information =====
    page1 = doc.new_page(width=612, height=792)  # Letter size

    # Title
    page1.insert_text(
        pymupdf.Point(72, 60),
        "INSURANCE CLAIM FORM",
        fontsize=20,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    # Horizontal rule
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 70), pymupdf.Point(540, 70))
    shape.finish(color=(0.1, 0.2, 0.5), width=2)
    shape.commit()

    # Section header
    page1.insert_text(
        pymupdf.Point(72, 105),
        "Section A: Policy & Claimant Information",
        fontsize=14,
        fontname="hebo",
        color=(0.2, 0.2, 0.2),
    )

    # --- Policy Number ---
    page1.insert_text(pymupdf.Point(72, 145), "Policy Number:", fontsize=11, fontname="hebo")
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "policy_number"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(200, 130, 450, 150)
    widget.text_fontsize = 11
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.97, 0.97, 0.97)
    widget.border_color = (0.4, 0.4, 0.4)
    widget.border_width = 1
    page1.add_widget(widget)

    # --- Claimant Name ---
    page1.insert_text(pymupdf.Point(72, 190), "Claimant Name:", fontsize=11, fontname="hebo")
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "claimant_name"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(200, 175, 450, 195)
    widget.text_fontsize = 11
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.97, 0.97, 0.97)
    widget.border_color = (0.4, 0.4, 0.4)
    widget.border_width = 1
    page1.add_widget(widget)

    # --- Date of Loss ---
    page1.insert_text(pymupdf.Point(72, 235), "Date of Loss:", fontsize=11, fontname="hebo")
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "date_of_loss"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(200, 220, 350, 240)
    widget.text_fontsize = 11
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.97, 0.97, 0.97)
    widget.border_color = (0.4, 0.4, 0.4)
    widget.border_width = 1
    page1.add_widget(widget)
    page1.insert_text(pymupdf.Point(355, 235), "(MM/DD/YYYY)", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Loss Type (Dropdown) ---
    page1.insert_text(pymupdf.Point(72, 280), "Loss Type:", fontsize=11, fontname="hebo")
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_COMBOBOX
    widget.field_name = "loss_type"
    widget.choice_values = [
        "Select Loss Type...",
        "Property Damage",
        "Bodily Injury",
        "Vehicle Collision",
        "Theft/Burglary",
        "Fire Damage",
        "Natural Disaster",
        "Water Damage",
        "Other",
    ]
    widget.field_value = ""
    widget.rect = pymupdf.Rect(200, 265, 450, 285)
    widget.text_fontsize = 11
    widget.fill_color = (0.97, 0.97, 0.97)
    widget.border_color = (0.4, 0.4, 0.4)
    widget.border_width = 1
    page1.add_widget(widget)

    # --- Estimated Amount ---
    page1.insert_text(pymupdf.Point(72, 325), "Estimated Amount:", fontsize=11, fontname="hebo")
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "estimated_amount"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(220, 310, 400, 330)
    widget.text_fontsize = 11
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.97, 0.97, 0.97)
    widget.border_color = (0.4, 0.4, 0.4)
    widget.border_width = 1
    page1.add_widget(widget)

    # Footer note on page 1
    page1.insert_text(
        pymupdf.Point(72, 750),
        "Page 1 of 2  |  Acme Insurance Co.  |  Claims Department",
        fontsize=8,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    # ===== PAGE 2: Description & Declarations =====
    page2 = doc.new_page(width=612, height=792)

    # Section header
    page2.insert_text(
        pymupdf.Point(72, 60),
        "Section B: Loss Description & Declarations",
        fontsize=14,
        fontname="hebo",
        color=(0.2, 0.2, 0.2),
    )

    # Horizontal rule
    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 70), pymupdf.Point(540, 70))
    shape2.finish(color=(0.1, 0.2, 0.5), width=2)
    shape2.commit()

    # --- Description (Multiline) ---
    page2.insert_text(pymupdf.Point(72, 105), "Description of Loss:", fontsize=11, fontname="hebo")
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "description"
    widget.field_value = ""
    widget.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
    widget.rect = pymupdf.Rect(72, 115, 540, 280)
    widget.text_fontsize = 11
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.97, 0.97, 0.97)
    widget.border_color = (0.4, 0.4, 0.4)
    widget.border_width = 1
    page2.add_widget(widget)

    page2.insert_text(
        pymupdf.Point(72, 295),
        "Please provide a detailed description of the loss or damage.",
        fontsize=9,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    # Section: Declarations
    page2.insert_text(
        pymupdf.Point(72, 340),
        "Section C: Declarations",
        fontsize=14,
        fontname="hebo",
        color=(0.2, 0.2, 0.2),
    )

    # --- Police Report Filed (Checkbox) ---
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    widget.field_name = "police_report_filed"
    widget.field_value = "Off"  # unchecked
    widget.rect = pymupdf.Rect(72, 365, 92, 385)
    widget.border_color = (0.3, 0.3, 0.3)
    widget.border_width = 1
    page2.add_widget(widget)
    page2.insert_text(pymupdf.Point(100, 380), "Police report has been filed", fontsize=11, fontname="helv")

    # --- Photos Attached (Checkbox) ---
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    widget.field_name = "photos_attached"
    widget.field_value = "Off"  # unchecked
    widget.rect = pymupdf.Rect(72, 400, 92, 420)
    widget.border_color = (0.3, 0.3, 0.3)
    widget.border_width = 1
    page2.add_widget(widget)
    page2.insert_text(pymupdf.Point(100, 415), "Photos/documentation attached", fontsize=11, fontname="helv")

    # Disclaimer text
    page2.insert_textbox(
        pymupdf.Rect(72, 480, 540, 580),
        "By submitting this claim, I certify that the information provided is true and accurate "
        "to the best of my knowledge. I understand that any false or misleading statements may "
        "result in denial of the claim and possible legal action. I authorize Acme Insurance Co. "
        "to investigate this claim and obtain any necessary records.",
        fontsize=9,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Signature line
    shape3 = page2.new_shape()
    shape3.draw_line(pymupdf.Point(72, 620), pymupdf.Point(300, 620))
    shape3.finish(color=(0, 0, 0), width=0.5)
    shape3.draw_line(pymupdf.Point(350, 620), pymupdf.Point(540, 620))
    shape3.finish(color=(0, 0, 0), width=0.5)
    shape3.commit()
    page2.insert_text(pymupdf.Point(72, 635), "Claimant Signature", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))
    page2.insert_text(pymupdf.Point(350, 635), "Date", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Footer note on page 2
    page2.insert_text(
        pymupdf.Point(72, 750),
        "Page 2 of 2  |  Acme Insurance Co.  |  Claims Department",
        fontsize=8,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
