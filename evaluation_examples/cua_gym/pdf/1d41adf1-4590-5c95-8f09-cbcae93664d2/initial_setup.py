"""
Initial Setup: Patient intake form (empty)
Task ID: pdf_fm_046
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_046'
FORM_DIR = f'{WORKDIR}/Documents/forms'
OUTPUT = f'{FORM_DIR}/patient_intake.pdf'


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
    os.makedirs(FORM_DIR, exist_ok=True)

    doc = pymupdf.open()

    # ======= PAGE 1: Patient Information =======
    page1 = doc.new_page(width=612, height=792)  # Letter size

    # Title
    page1.insert_text(
        pymupdf.Point(72, 50),
        "Greenfield Medical Center",
        fontsize=20,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )
    page1.insert_text(
        pymupdf.Point(72, 75),
        "Patient Intake Form",
        fontsize=16,
        fontname="hebo",
        color=(0.2, 0.2, 0.2),
    )

    # Horizontal rule
    shape1 = page1.new_shape()
    shape1.draw_line(pymupdf.Point(72, 85), pymupdf.Point(540, 85))
    shape1.finish(color=(0.5, 0.5, 0.5), width=1)
    shape1.commit()

    # Section: Personal Information
    page1.insert_text(pymupdf.Point(72, 115), "Section 1: Personal Information",
                      fontsize=13, fontname="hebo", color=(0.15, 0.15, 0.4))

    # Patient Name label + field
    page1.insert_text(pymupdf.Point(72, 150), "Patient Full Name:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "patient_name"
    w.field_value = ""
    w.rect = pymupdf.Rect(220, 137, 520, 157)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    # Date of Birth label + field
    page1.insert_text(pymupdf.Point(72, 190), "Date of Birth (MM/DD/YYYY):",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "dob"
    w.field_value = ""
    w.rect = pymupdf.Rect(280, 177, 430, 197)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    # Gender section (using checkboxes for reliable PyMuPDF handling)
    page1.insert_text(pymupdf.Point(72, 235), "Gender:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))

    # Male checkbox
    page1.insert_text(pymupdf.Point(175, 235), "Male",
                      fontsize=11, fontname="helv", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "male"
    w.field_value = "Off"
    w.rect = pymupdf.Rect(155, 222, 172, 239)
    w.border_color = (0.3, 0.3, 0.3)
    w.border_width = 1
    page1.add_widget(w)

    # Female checkbox
    page1.insert_text(pymupdf.Point(275, 235), "Female",
                      fontsize=11, fontname="helv", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "female"
    w.field_value = "Off"
    w.rect = pymupdf.Rect(255, 222, 272, 239)
    w.border_color = (0.3, 0.3, 0.3)
    w.border_width = 1
    page1.add_widget(w)

    # Additional patient info fields (phone, email, address) for realism
    page1.insert_text(pymupdf.Point(72, 280), "Phone Number:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "phone"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, 267, 400, 287)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    page1.insert_text(pymupdf.Point(72, 320), "Email Address:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "email"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, 307, 520, 327)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    page1.insert_text(pymupdf.Point(72, 360), "Street Address:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "address"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, 347, 520, 367)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    page1.insert_text(pymupdf.Point(72, 400), "City:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "city"
    w.field_value = ""
    w.rect = pymupdf.Rect(130, 387, 300, 407)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    page1.insert_text(pymupdf.Point(320, 400), "State:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "state"
    w.field_value = ""
    w.rect = pymupdf.Rect(370, 387, 430, 407)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    page1.insert_text(pymupdf.Point(450, 400), "ZIP:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "zip"
    w.field_value = ""
    w.rect = pymupdf.Rect(485, 387, 540, 407)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    # Emergency contact
    page1.insert_text(pymupdf.Point(72, 450), "Section 2: Emergency Contact",
                      fontsize=13, fontname="hebo", color=(0.15, 0.15, 0.4))

    page1.insert_text(pymupdf.Point(72, 485), "Emergency Contact Name:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "emergency_name"
    w.field_value = ""
    w.rect = pymupdf.Rect(270, 472, 520, 492)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    page1.insert_text(pymupdf.Point(72, 525), "Relationship:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "emergency_relationship"
    w.field_value = ""
    w.rect = pymupdf.Rect(195, 512, 370, 532)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    page1.insert_text(pymupdf.Point(390, 525), "Phone:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "emergency_phone"
    w.field_value = ""
    w.rect = pymupdf.Rect(440, 512, 540, 532)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    # Footer
    page1.insert_text(pymupdf.Point(250, 750), "Page 1 of 3",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # ======= PAGE 2: Medical History =======
    page2 = doc.new_page(width=612, height=792)

    page2.insert_text(
        pymupdf.Point(72, 50),
        "Greenfield Medical Center",
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )
    page2.insert_text(
        pymupdf.Point(72, 72),
        "Medical History",
        fontsize=14,
        fontname="hebo",
        color=(0.2, 0.2, 0.2),
    )

    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape2.finish(color=(0.5, 0.5, 0.5), width=1)
    shape2.commit()

    # Allergies
    page2.insert_text(pymupdf.Point(72, 115), "Section 3: Allergies & Medications",
                      fontsize=13, fontname="hebo", color=(0.15, 0.15, 0.4))

    page2.insert_text(pymupdf.Point(72, 150), "Known Allergies:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "allergies"
    w.field_value = ""
    w.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
    w.rect = pymupdf.Rect(72, 160, 540, 230)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page2.add_widget(w)

    # Current Medications
    page2.insert_text(pymupdf.Point(72, 260), "Current Medications (include dosage):",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "current_medications"
    w.field_value = ""
    w.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
    w.rect = pymupdf.Rect(72, 270, 540, 370)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page2.add_widget(w)

    # Previous surgeries
    page2.insert_text(pymupdf.Point(72, 400), "Section 4: Medical History",
                      fontsize=13, fontname="hebo", color=(0.15, 0.15, 0.4))

    page2.insert_text(pymupdf.Point(72, 435), "Previous Surgeries/Procedures:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "surgeries"
    w.field_value = ""
    w.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
    w.rect = pymupdf.Rect(72, 445, 540, 530)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page2.add_widget(w)

    page2.insert_text(pymupdf.Point(72, 560), "Chronic Conditions:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "chronic_conditions"
    w.field_value = ""
    w.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
    w.rect = pymupdf.Rect(72, 570, 540, 650)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page2.add_widget(w)

    page2.insert_text(pymupdf.Point(250, 750), "Page 2 of 3",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # ======= PAGE 3: Insurance Information =======
    page3 = doc.new_page(width=612, height=792)

    page3.insert_text(
        pymupdf.Point(72, 50),
        "Greenfield Medical Center",
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )
    page3.insert_text(
        pymupdf.Point(72, 72),
        "Insurance & Consent",
        fontsize=14,
        fontname="hebo",
        color=(0.2, 0.2, 0.2),
    )

    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape3.finish(color=(0.5, 0.5, 0.5), width=1)
    shape3.commit()

    # Insurance section
    page3.insert_text(pymupdf.Point(72, 115), "Section 5: Insurance Information",
                      fontsize=13, fontname="hebo", color=(0.15, 0.15, 0.4))

    page3.insert_text(pymupdf.Point(72, 150), "Do you have health insurance?",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))

    # Insurance Yes checkbox
    page3.insert_text(pymupdf.Point(100, 180), "Yes",
                      fontsize=11, fontname="helv", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "insurance_yes"
    w.field_value = "Off"
    w.rect = pymupdf.Rect(78, 168, 95, 185)
    w.border_color = (0.3, 0.3, 0.3)
    w.border_width = 1
    page3.add_widget(w)

    # Insurance No checkbox
    page3.insert_text(pymupdf.Point(180, 180), "No",
                      fontsize=11, fontname="helv", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "insurance_no"
    w.field_value = "Off"
    w.rect = pymupdf.Rect(158, 168, 175, 185)
    w.border_color = (0.3, 0.3, 0.3)
    w.border_width = 1
    page3.add_widget(w)

    # Insurance provider details
    page3.insert_text(pymupdf.Point(72, 220), "Insurance Provider:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "insurance_provider"
    w.field_value = ""
    w.rect = pymupdf.Rect(230, 207, 520, 227)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page3.add_widget(w)

    page3.insert_text(pymupdf.Point(72, 260), "Policy Number:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "policy_number"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, 247, 400, 267)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page3.add_widget(w)

    page3.insert_text(pymupdf.Point(72, 300), "Group Number:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "group_number"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, 287, 400, 307)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page3.add_widget(w)

    # Consent section
    page3.insert_text(pymupdf.Point(72, 360), "Section 6: Consent",
                      fontsize=13, fontname="hebo", color=(0.15, 0.15, 0.4))

    consent_text = (
        "I hereby consent to treatment and authorize Greenfield Medical Center "
        "to provide medical care as deemed necessary. I certify that the information "
        "provided in this form is accurate and complete to the best of my knowledge. "
        "I understand that providing false information may result in denial of service."
    )
    rect = pymupdf.Rect(72, 380, 540, 480)
    page3.insert_textbox(rect, consent_text, fontsize=10, fontname="helv",
                         color=(0.2, 0.2, 0.2), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page3.insert_text(pymupdf.Point(72, 510), "Patient Signature:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    # Signature line
    shape3b = page3.new_shape()
    shape3b.draw_line(pymupdf.Point(210, 515), pymupdf.Point(420, 515))
    shape3b.finish(color=(0, 0, 0), width=0.5)
    shape3b.commit()

    page3.insert_text(pymupdf.Point(440, 510), "Date:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "signature_date"
    w.field_value = ""
    w.rect = pymupdf.Rect(480, 500, 540, 520)
    w.text_fontsize = 10
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page3.add_widget(w)

    page3.insert_text(pymupdf.Point(250, 750), "Page 3 of 3",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Set metadata
    doc.set_metadata({
        "title": "Patient Intake Form",
        "author": "Greenfield Medical Center",
        "subject": "New Patient Registration",
        "creator": "Greenfield Medical Center Admin",
    })

    # Set TOC
    doc.set_toc([
        [1, "Personal Information", 1],
        [1, "Medical History", 2],
        [1, "Insurance & Consent", 3],
    ])

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
