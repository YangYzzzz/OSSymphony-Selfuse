"""
Initial Setup: Create a 2-page visa application PDF form with all fields empty/unchecked
Task ID: pdf_fm_036
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_036'
FORMS_DIR = f'{WORKDIR}/Documents/forms'
OUTPUT = f'{FORMS_DIR}/visa_application.pdf'

A4_WIDTH, A4_HEIGHT = 595, 842


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

    # ==================== PAGE 1 ====================
    page1 = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)

    # --- Header ---
    # Title background
    shape = page1.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, A4_WIDTH, 70))
    shape.finish(fill=(0.13, 0.22, 0.45))  # dark navy
    shape.commit()

    page1.insert_text(pymupdf.Point(72, 42), "VISA APPLICATION FORM",
                      fontsize=22, fontname="hebo", color=(1, 1, 1))
    page1.insert_text(pymupdf.Point(72, 60), "Ministry of Foreign Affairs",
                      fontsize=10, fontname="helv", color=(0.85, 0.85, 0.85))

    # Reference number (decorative)
    page1.insert_text(pymupdf.Point(400, 42), "Form VA-2025",
                      fontsize=9, fontname="helv", color=(0.85, 0.85, 0.85))
    page1.insert_text(pymupdf.Point(400, 56), "Rev. 03/2025",
                      fontsize=8, fontname="heit", color=(0.7, 0.7, 0.8))

    # Instructions box
    shape = page1.new_shape()
    shape.draw_rect(pymupdf.Rect(50, 80, 545, 130))
    shape.finish(fill=(0.95, 0.95, 1.0), color=(0.6, 0.6, 0.8), width=0.5)
    shape.commit()

    page1.insert_text(pymupdf.Point(60, 97), "INSTRUCTIONS:",
                      fontsize=9, fontname="hebo", color=(0.13, 0.22, 0.45))
    page1.insert_textbox(
        pymupdf.Rect(60, 100, 535, 125),
        "Please complete all fields in BLOCK CAPITALS or typed format. "
        "All fields marked with (*) are mandatory. Submit this form along with "
        "supporting documents to the nearest consular office.",
        fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3),
    )

    # --- Section 1: Personal Information ---
    y = 145
    page1.insert_text(pymupdf.Point(50, y), "SECTION 1: PERSONAL INFORMATION",
                      fontsize=11, fontname="hebo", color=(0.13, 0.22, 0.45))
    y += 5
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(50, y), pymupdf.Point(545, y))
    shape.finish(color=(0.13, 0.22, 0.45), width=1.5)
    shape.commit()

    # Field: Surname
    y += 18
    page1.insert_text(pymupdf.Point(55, y), "Surname / Family Name *",
                      fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "surname"
    w.field_value = ""
    w.rect = pymupdf.Rect(55, y + 5, 540, y + 25)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (1, 1, 1)
    w.border_color = (0.6, 0.6, 0.6)
    w.border_width = 0.75
    page1.add_widget(w)

    # Field: Given Names
    y += 45
    page1.insert_text(pymupdf.Point(55, y), "Given Names *",
                      fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "given_names"
    w.field_value = ""
    w.rect = pymupdf.Rect(55, y + 5, 540, y + 25)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (1, 1, 1)
    w.border_color = (0.6, 0.6, 0.6)
    w.border_width = 0.75
    page1.add_widget(w)

    # Field: Nationality
    y += 45
    page1.insert_text(pymupdf.Point(55, y), "Nationality *",
                      fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "nationality"
    w.field_value = ""
    w.rect = pymupdf.Rect(55, y + 5, 280, y + 25)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (1, 1, 1)
    w.border_color = (0.6, 0.6, 0.6)
    w.border_width = 0.75
    page1.add_widget(w)

    # Field: Passport Number (same row, right side)
    page1.insert_text(pymupdf.Point(300, y), "Passport Number *",
                      fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "passport_no"
    w.field_value = ""
    w.rect = pymupdf.Rect(300, y + 5, 540, y + 25)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (1, 1, 1)
    w.border_color = (0.6, 0.6, 0.6)
    w.border_width = 0.75
    page1.add_widget(w)

    # Field: Date of Birth
    y += 45
    page1.insert_text(pymupdf.Point(55, y), "Date of Birth (YYYY-MM-DD) *",
                      fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "dob"
    w.field_value = ""
    w.rect = pymupdf.Rect(55, y + 5, 220, y + 25)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (1, 1, 1)
    w.border_color = (0.6, 0.6, 0.6)
    w.border_width = 0.75
    page1.add_widget(w)

    # Field: Gender (radio buttons) - use separate checkboxes for Male/Female/Other
    page1.insert_text(pymupdf.Point(260, y), "Gender *",
                      fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))

    # We'll use a combobox for gender since radio buttons are complex in PyMuPDF
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_COMBOBOX
    w.field_name = "gender"
    w.choice_values = ["", "Male", "Female", "Other"]
    w.field_value = ""
    w.rect = pymupdf.Rect(260, y + 5, 420, y + 25)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (1, 1, 1)
    w.border_color = (0.6, 0.6, 0.6)
    w.border_width = 0.75
    page1.add_widget(w)

    # --- Section 2: Travel Details ---
    y += 55
    page1.insert_text(pymupdf.Point(50, y), "SECTION 2: TRAVEL DETAILS",
                      fontsize=11, fontname="hebo", color=(0.13, 0.22, 0.45))
    y += 5
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(50, y), pymupdf.Point(545, y))
    shape.finish(color=(0.13, 0.22, 0.45), width=1.5)
    shape.commit()

    # Field: Purpose of Visit (dropdown)
    y += 18
    page1.insert_text(pymupdf.Point(55, y), "Purpose of Visit *",
                      fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_COMBOBOX
    w.field_name = "purpose"
    w.choice_values = ["", "Tourism", "Business", "Education", "Medical", "Transit", "Employment", "Other"]
    w.field_value = ""
    w.rect = pymupdf.Rect(55, y + 5, 300, y + 25)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (1, 1, 1)
    w.border_color = (0.6, 0.6, 0.6)
    w.border_width = 0.75
    page1.add_widget(w)

    # Field: Arrival Date
    y += 45
    page1.insert_text(pymupdf.Point(55, y), "Date of Arrival (YYYY-MM-DD) *",
                      fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "arrival_date"
    w.field_value = ""
    w.rect = pymupdf.Rect(55, y + 5, 270, y + 25)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (1, 1, 1)
    w.border_color = (0.6, 0.6, 0.6)
    w.border_width = 0.75
    page1.add_widget(w)

    # Field: Departure Date (same row, right side)
    page1.insert_text(pymupdf.Point(300, y), "Date of Departure (YYYY-MM-DD) *",
                      fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "departure_date"
    w.field_value = ""
    w.rect = pymupdf.Rect(300, y + 5, 540, y + 25)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (1, 1, 1)
    w.border_color = (0.6, 0.6, 0.6)
    w.border_width = 0.75
    page1.add_widget(w)

    # Field: Accommodation
    y += 45
    page1.insert_text(pymupdf.Point(55, y), "Accommodation Address in Destination Country *",
                      fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "accommodation"
    w.field_value = ""
    w.rect = pymupdf.Rect(55, y + 5, 540, y + 25)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (1, 1, 1)
    w.border_color = (0.6, 0.6, 0.6)
    w.border_width = 0.75
    page1.add_widget(w)

    # --- Footer on page 1 ---
    page1.insert_text(pymupdf.Point(50, A4_HEIGHT - 30),
                      "Page 1 of 2  |  Visa Application Form VA-2025",
                      fontsize=7, fontname="heit", color=(0.5, 0.5, 0.5))

    # ==================== PAGE 2 ====================
    page2 = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)

    # Header bar
    shape = page2.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, A4_WIDTH, 50))
    shape.finish(fill=(0.13, 0.22, 0.45))
    shape.commit()

    page2.insert_text(pymupdf.Point(72, 35), "VISA APPLICATION FORM (continued)",
                      fontsize=16, fontname="hebo", color=(1, 1, 1))

    # --- Section 3: Supporting Information ---
    y2 = 70
    page2.insert_text(pymupdf.Point(50, y2), "SECTION 3: SUPPORTING INFORMATION",
                      fontsize=11, fontname="hebo", color=(0.13, 0.22, 0.45))
    y2 += 5
    shape = page2.new_shape()
    shape.draw_line(pymupdf.Point(50, y2), pymupdf.Point(545, y2))
    shape.finish(color=(0.13, 0.22, 0.45), width=1.5)
    shape.commit()

    y2 += 15
    page2.insert_textbox(
        pymupdf.Rect(55, y2, 540, y2 + 80),
        "Please provide details of your travel itinerary, including any connecting flights, "
        "stopovers, and local transportation arrangements. If traveling for business, "
        "include the name and address of the company or organization you will be visiting. "
        "For tourism, list the main attractions or regions you plan to visit. "
        "Attach additional pages if necessary.",
        fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3),
    )

    # Checklist section
    y2 += 100
    page2.insert_text(pymupdf.Point(50, y2), "SECTION 4: REQUIRED DOCUMENTS CHECKLIST",
                      fontsize=11, fontname="hebo", color=(0.13, 0.22, 0.45))
    y2 += 5
    shape = page2.new_shape()
    shape.draw_line(pymupdf.Point(50, y2), pymupdf.Point(545, y2))
    shape.finish(color=(0.13, 0.22, 0.45), width=1.5)
    shape.commit()

    y2 += 15
    checklist_items = [
        "Valid passport (minimum 6 months validity beyond travel dates)",
        "Two recent passport-sized photographs (35mm x 45mm)",
        "Proof of accommodation (hotel booking or invitation letter)",
        "Return/onward flight ticket confirmation",
        "Proof of sufficient funds (bank statements from last 3 months)",
        "Travel insurance certificate covering the entire stay",
        "Employment verification letter or business invitation",
    ]
    for item in checklist_items:
        # Draw checkbox square (decorative, not a form field)
        shape = page2.new_shape()
        shape.draw_rect(pymupdf.Rect(60, y2 - 8, 72, y2 + 4))
        shape.finish(color=(0.4, 0.4, 0.4), width=0.5)
        shape.commit()
        page2.insert_text(pymupdf.Point(80, y2), item,
                          fontsize=8.5, fontname="helv", color=(0.25, 0.25, 0.25))
        y2 += 20

    # --- Section 5: Declaration ---
    y2 += 20
    page2.insert_text(pymupdf.Point(50, y2), "SECTION 5: DECLARATION",
                      fontsize=11, fontname="hebo", color=(0.13, 0.22, 0.45))
    y2 += 5
    shape = page2.new_shape()
    shape.draw_line(pymupdf.Point(50, y2), pymupdf.Point(545, y2))
    shape.finish(color=(0.13, 0.22, 0.45), width=1.5)
    shape.commit()

    y2 += 15
    page2.insert_textbox(
        pymupdf.Rect(55, y2, 540, y2 + 50),
        "I hereby declare that the information provided in this application is true, "
        "complete, and correct to the best of my knowledge. I understand that any false "
        "or misleading information may result in the refusal or cancellation of my visa, "
        "and may lead to legal proceedings under applicable immigration laws.",
        fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2),
    )

    # Checkbox: declaration_agreed
    y2 += 60
    page2.insert_text(pymupdf.Point(80, y2 + 2),
                      "I agree to the declaration above *",
                      fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "declaration_agreed"
    w.field_value = "Off"
    w.rect = pymupdf.Rect(55, y2 - 7, 73, y2 + 11)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 0.75
    page2.add_widget(w)

    # Checkbox: info_correct
    y2 += 25
    page2.insert_text(pymupdf.Point(80, y2 + 2),
                      "I confirm all information provided is correct *",
                      fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "info_correct"
    w.field_value = "Off"
    w.rect = pymupdf.Rect(55, y2 - 7, 73, y2 + 11)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 0.75
    page2.add_widget(w)

    # Signature area
    y2 += 45
    page2.insert_text(pymupdf.Point(55, y2), "Applicant's Signature:",
                      fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))
    y2 += 5
    shape = page2.new_shape()
    shape.draw_line(pymupdf.Point(55, y2 + 30), pymupdf.Point(280, y2 + 30))
    shape.finish(color=(0.3, 0.3, 0.3), width=0.5, dashes="[2 2]")
    shape.commit()

    page2.insert_text(pymupdf.Point(320, y2), "Date:",
                      fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))
    shape = page2.new_shape()
    shape.draw_line(pymupdf.Point(320, y2 + 30), pymupdf.Point(540, y2 + 30))
    shape.finish(color=(0.3, 0.3, 0.3), width=0.5, dashes="[2 2]")
    shape.commit()

    # --- Official Use Box ---
    y2 += 55
    shape = page2.new_shape()
    shape.draw_rect(pymupdf.Rect(50, y2, 545, y2 + 80))
    shape.finish(fill=(0.96, 0.96, 0.96), color=(0.5, 0.5, 0.5), width=0.75)
    shape.commit()

    page2.insert_text(pymupdf.Point(60, y2 + 15), "FOR OFFICIAL USE ONLY",
                      fontsize=9, fontname="hebo", color=(0.5, 0.5, 0.5))
    page2.insert_text(pymupdf.Point(60, y2 + 32), "Application No.: ________________",
                      fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
    page2.insert_text(pymupdf.Point(300, y2 + 32), "Received by: ________________",
                      fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
    page2.insert_text(pymupdf.Point(60, y2 + 50), "Decision:  APPROVED  /  DENIED  /  PENDING",
                      fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
    page2.insert_text(pymupdf.Point(300, y2 + 50), "Date: ________________",
                      fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Footer on page 2
    page2.insert_text(pymupdf.Point(50, A4_HEIGHT - 30),
                      "Page 2 of 2  |  Visa Application Form VA-2025",
                      fontsize=7, fontname="heit", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open the form in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
