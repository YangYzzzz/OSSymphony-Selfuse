"""
Initial Setup: Create a filled PDF form with 8 AcroForm fields (text + checkboxes) across 3 pages.
Task ID: pdf_gf1_022
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCDIR = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_gf1_022'
OUTPUT = f'{DOCDIR}/filled_form.pdf'


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
    os.makedirs(DOCDIR, exist_ok=True)

    # Remove filled_form_flat.pdf if it exists (must NOT exist in initial state)
    flat_path = f'{DOCDIR}/filled_form_flat.pdf'
    if os.path.exists(flat_path):
        os.remove(flat_path)

    doc = pymupdf.open()

    # ── Page 1: Personal Information ──
    page1 = doc.new_page(width=612, height=792)  # Letter size

    # Title
    page1.insert_text(pymupdf.Point(72, 50), "Employee Onboarding Form",
                      fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    page1.insert_text(pymupdf.Point(72, 75), "Meridian Technologies Inc.",
                      fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))

    # Horizontal rule
    shape1 = page1.new_shape()
    shape1.draw_line(pymupdf.Point(72, 85), pymupdf.Point(540, 85))
    shape1.finish(color=(0.6, 0.6, 0.6), width=1)
    shape1.commit()

    # Section header
    page1.insert_text(pymupdf.Point(72, 115), "Section 1: Personal Information",
                      fontsize=14, fontname="hebo", color=(0.15, 0.15, 0.45))

    # Field 1: Full Name (text)
    page1.insert_text(pymupdf.Point(72, 155), "Full Name:", fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "full_name"
    w.field_value = "Alexandra Petrova"
    w.rect = pymupdf.Rect(200, 140, 450, 162)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.96, 0.96, 0.96)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    # Field 2: Email Address (text)
    page1.insert_text(pymupdf.Point(72, 205), "Email Address:", fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "email"
    w.field_value = "a.petrova@meridiantech.com"
    w.rect = pymupdf.Rect(200, 190, 450, 212)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.96, 0.96, 0.96)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    # Field 3: Department (text)
    page1.insert_text(pymupdf.Point(72, 255), "Department:", fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "department"
    w.field_value = "Cloud Infrastructure Engineering"
    w.rect = pymupdf.Rect(200, 240, 450, 262)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.96, 0.96, 0.96)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    # Additional static content
    page1.insert_text(pymupdf.Point(72, 310), "Instructions:",
                      fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
    page1.insert_textbox(
        pymupdf.Rect(72, 320, 540, 420),
        "Please complete all sections of this form accurately. Your information "
        "will be used to set up your employee accounts, benefits enrollment, and "
        "office access credentials. All fields marked with an asterisk (*) are "
        "mandatory. If you have questions, contact HR at hr@meridiantech.com or "
        "extension 4500.",
        fontsize=10, fontname="helv", color=(0.25, 0.25, 0.25),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # Footer
    page1.insert_text(pymupdf.Point(72, 750), "Page 1 of 3",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))
    page1.insert_text(pymupdf.Point(350, 750), "Form ID: MER-ONB-2025-0147",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # ── Page 2: Employment Details ──
    page2 = doc.new_page(width=612, height=792)

    page2.insert_text(pymupdf.Point(72, 50), "Section 2: Employment Details",
                      fontsize=14, fontname="hebo", color=(0.15, 0.15, 0.45))

    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 60), pymupdf.Point(540, 60))
    shape2.finish(color=(0.6, 0.6, 0.6), width=1)
    shape2.commit()

    # Field 4: Start Date (text)
    page2.insert_text(pymupdf.Point(72, 105), "Start Date:", fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "start_date"
    w.field_value = "2025-04-14"
    w.rect = pymupdf.Rect(200, 90, 350, 112)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.96, 0.96, 0.96)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page2.add_widget(w)

    # Field 5: Employee ID (text)
    page2.insert_text(pymupdf.Point(72, 155), "Employee ID:", fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "employee_id"
    w.field_value = "MER-78234"
    w.rect = pymupdf.Rect(200, 140, 350, 162)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.96, 0.96, 0.96)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page2.add_widget(w)

    # Static table for reference
    page2.insert_text(pymupdf.Point(72, 210), "Benefits Package Summary:",
                      fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))

    table_data = [
        ["Benefit", "Coverage", "Monthly Cost"],
        ["Health Insurance (PPO)", "Employee + Family", "$385.00"],
        ["Dental Plan", "Employee + Family", "$62.50"],
        ["Vision Plan", "Employee Only", "$18.75"],
        ["Life Insurance", "2x Annual Salary", "$0.00"],
        ["401(k) Match", "Up to 6%", "Employer Paid"],
    ]
    y_start = 225
    col_x = [72, 250, 410]
    for row_idx, row in enumerate(table_data):
        y = y_start + row_idx * 22
        fontname = "hebo" if row_idx == 0 else "helv"
        for col_idx, cell in enumerate(row):
            page2.insert_text(pymupdf.Point(col_x[col_idx], y + 15),
                              cell, fontsize=10, fontname=fontname,
                              color=(0.1, 0.1, 0.1))
        # Draw row separator
        shape2b = page2.new_shape()
        shape2b.draw_line(pymupdf.Point(72, y + 20), pymupdf.Point(540, y + 20))
        shape2b.finish(color=(0.85, 0.85, 0.85), width=0.5)
        shape2b.commit()

    page2.insert_text(pymupdf.Point(72, 750), "Page 2 of 3",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))
    page2.insert_text(pymupdf.Point(350, 750), "Form ID: MER-ONB-2025-0147",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # ── Page 3: Agreements & Signatures ──
    page3 = doc.new_page(width=612, height=792)

    page3.insert_text(pymupdf.Point(72, 50), "Section 3: Agreements",
                      fontsize=14, fontname="hebo", color=(0.15, 0.15, 0.45))

    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, 60), pymupdf.Point(540, 60))
    shape3.finish(color=(0.6, 0.6, 0.6), width=1)
    shape3.commit()

    # Agreement text
    page3.insert_textbox(
        pymupdf.Rect(72, 75, 540, 200),
        "By checking the boxes below, I confirm that all information provided in "
        "this form is accurate and complete to the best of my knowledge. I acknowledge "
        "that I have read and understood the Employee Handbook, the Code of Conduct, "
        "and the Information Security Policy. I agree to abide by all company policies "
        "and understand that any false statements may result in disciplinary action, "
        "up to and including termination of employment.",
        fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Field 6: Checkbox - NDA Agreement
    page3.insert_text(pymupdf.Point(95, 225),
                      "I agree to the Non-Disclosure Agreement (NDA)",
                      fontsize=10, fontname="helv")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "nda_agree"
    w.field_value = "Yes"
    w.rect = pymupdf.Rect(72, 213, 90, 231)
    w.border_color = (0.3, 0.3, 0.3)
    w.border_width = 1
    page3.add_widget(w)

    # Field 7: Checkbox - Code of Conduct
    page3.insert_text(pymupdf.Point(95, 255),
                      "I have read and accept the Code of Conduct",
                      fontsize=10, fontname="helv")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "code_of_conduct"
    w.field_value = "Yes"
    w.rect = pymupdf.Rect(72, 243, 90, 261)
    w.border_color = (0.3, 0.3, 0.3)
    w.border_width = 1
    page3.add_widget(w)

    # Field 8: Checkbox - IT Security Policy
    page3.insert_text(pymupdf.Point(95, 285),
                      "I acknowledge the IT Security Policy",
                      fontsize=10, fontname="helv")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "it_security"
    w.field_value = "Yes"
    w.rect = pymupdf.Rect(72, 273, 90, 291)
    w.border_color = (0.3, 0.3, 0.3)
    w.border_width = 1
    page3.add_widget(w)

    # Signature line
    page3.insert_text(pymupdf.Point(72, 370), "Employee Signature:",
                      fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
    shape3b = page3.new_shape()
    shape3b.draw_line(pymupdf.Point(200, 375), pymupdf.Point(450, 375))
    shape3b.finish(color=(0, 0, 0), width=1)
    shape3b.commit()

    page3.insert_text(pymupdf.Point(72, 410), "Date: April 2, 2025",
                      fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))

    # Confidentiality notice
    page3.insert_textbox(
        pymupdf.Rect(72, 680, 540, 730),
        "CONFIDENTIAL: This document contains personal employee information protected "
        "under company policy MER-HR-004. Unauthorized distribution is prohibited. "
        "For questions, contact the HR department at hr@meridiantech.com.",
        fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    page3.insert_text(pymupdf.Point(72, 750), "Page 3 of 3",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))
    page3.insert_text(pymupdf.Point(350, 750), "Form ID: MER-ONB-2025-0147",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Set metadata
    doc.set_metadata({
        "title": "Employee Onboarding Form - Alexandra Petrova",
        "author": "Meridian Technologies HR",
        "subject": "Employee Onboarding",
        "keywords": "onboarding, employee, form, HR",
        "creator": "Meridian HR Portal",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify field count
    verify_doc = pymupdf.open(OUTPUT)
    field_count = 0
    for page in verify_doc:
        field_count += len(list(page.widgets()))
    verify_doc.close()
    print(f'Verified: {field_count} form fields across 3 pages')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
