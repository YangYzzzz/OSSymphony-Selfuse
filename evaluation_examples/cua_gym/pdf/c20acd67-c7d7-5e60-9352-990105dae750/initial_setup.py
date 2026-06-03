"""
Initial Setup: Create a multi-page grant application PDF form with empty fields
Task ID: pdf_fm_024
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_024'
FORMS_DIR = f'{WORKDIR}/Documents/forms'
OUTPUT = f'{FORMS_DIR}/grant_application.pdf'


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

    # --- Page 1: Principal Investigator Information ---
    page1 = doc.new_page(width=612, height=792)  # Letter size

    # Title bar
    shape = page1.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, 612, 60))
    shape.finish(fill=(0.16, 0.31, 0.52), color=(0.16, 0.31, 0.52))
    shape.commit()

    page1.insert_text(pymupdf.Point(72, 40), "NATIONAL SCIENCE FOUNDATION",
                      fontsize=20, fontname="hebo", color=(1, 1, 1))

    page1.insert_text(pymupdf.Point(72, 90), "Grant Application Form",
                      fontsize=16, fontname="hebo", color=(0.16, 0.31, 0.52))
    page1.insert_text(pymupdf.Point(72, 110), "Section 1: Principal Investigator Information",
                      fontsize=13, fontname="hebo", color=(0.2, 0.2, 0.2))

    # Horizontal rule
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 120), pymupdf.Point(540, 120))
    shape.finish(color=(0.7, 0.7, 0.7), width=1)
    shape.commit()

    # Labels for form fields
    page1.insert_text(pymupdf.Point(72, 165), "Principal Investigator Name:",
                      fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
    page1.insert_text(pymupdf.Point(72, 245), "Institution / University:",
                      fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
    page1.insert_text(pymupdf.Point(72, 325), "Grant Title:",
                      fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))

    # Form field: pi_name
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "pi_name"
    w.field_value = ""
    w.rect = pymupdf.Rect(72, 175, 450, 200)
    w.text_fontsize = 12
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 1
    page1.add_widget(w)

    # Form field: institution
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "institution"
    w.field_value = ""
    w.rect = pymupdf.Rect(72, 255, 450, 280)
    w.text_fontsize = 12
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 1
    page1.add_widget(w)

    # Form field: grant_title
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "grant_title"
    w.field_value = ""
    w.rect = pymupdf.Rect(72, 335, 540, 360)
    w.text_fontsize = 12
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 1
    page1.add_widget(w)

    # Instructions text
    page1.insert_text(pymupdf.Point(72, 420), "Instructions:",
                      fontsize=11, fontname="hebo", color=(0.3, 0.3, 0.3))
    instructions = (
        "Please complete all sections of this application form. Fields marked with an "
        "asterisk (*) are required. Ensure all information is accurate and up-to-date "
        "before submission. Applications with incomplete fields will not be processed."
    )
    page1.insert_textbox(pymupdf.Rect(72, 430, 540, 530), instructions,
                         fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))

    page1.insert_text(pymupdf.Point(72, 740), "Page 1 of 5",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 2: Budget & Timeline ---
    page2 = doc.new_page(width=612, height=792)

    shape = page2.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, 612, 60))
    shape.finish(fill=(0.16, 0.31, 0.52), color=(0.16, 0.31, 0.52))
    shape.commit()

    page2.insert_text(pymupdf.Point(72, 40), "NATIONAL SCIENCE FOUNDATION",
                      fontsize=20, fontname="hebo", color=(1, 1, 1))

    page2.insert_text(pymupdf.Point(72, 90), "Section 2: Budget & Timeline",
                      fontsize=13, fontname="hebo", color=(0.2, 0.2, 0.2))

    shape = page2.new_shape()
    shape.draw_line(pymupdf.Point(72, 100), pymupdf.Point(540, 100))
    shape.finish(color=(0.7, 0.7, 0.7), width=1)
    shape.commit()

    page2.insert_text(pymupdf.Point(72, 145), "Total Budget Requested:",
                      fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
    page2.insert_text(pymupdf.Point(72, 225), "Project Duration:",
                      fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
    page2.insert_text(pymupdf.Point(72, 305), "Proposed Start Date:",
                      fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))

    # Form field: budget_total
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "budget_total"
    w.field_value = ""
    w.rect = pymupdf.Rect(72, 155, 300, 180)
    w.text_fontsize = 12
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 1
    page2.add_widget(w)

    # Form field: duration
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "duration"
    w.field_value = ""
    w.rect = pymupdf.Rect(72, 235, 300, 260)
    w.text_fontsize = 12
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 1
    page2.add_widget(w)

    # Form field: start_date
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "start_date"
    w.field_value = ""
    w.rect = pymupdf.Rect(72, 315, 300, 340)
    w.text_fontsize = 12
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 1
    page2.add_widget(w)

    # Budget breakdown info
    page2.insert_text(pymupdf.Point(72, 400), "Budget Breakdown Guidelines:",
                      fontsize=11, fontname="hebo", color=(0.3, 0.3, 0.3))
    breakdown_text = (
        "The total budget should include personnel costs, equipment, travel, "
        "materials and supplies, publication costs, and indirect costs. A detailed "
        "budget justification must be provided in Section 4. All costs should be "
        "calculated for the full duration of the project."
    )
    page2.insert_textbox(pymupdf.Rect(72, 410, 540, 520), breakdown_text,
                         fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))

    page2.insert_text(pymupdf.Point(72, 740), "Page 2 of 5",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 3: Compliance & Certifications ---
    page3 = doc.new_page(width=612, height=792)

    shape = page3.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, 612, 60))
    shape.finish(fill=(0.16, 0.31, 0.52), color=(0.16, 0.31, 0.52))
    shape.commit()

    page3.insert_text(pymupdf.Point(72, 40), "NATIONAL SCIENCE FOUNDATION",
                      fontsize=20, fontname="hebo", color=(1, 1, 1))

    page3.insert_text(pymupdf.Point(72, 90), "Section 3: Compliance & Certifications",
                      fontsize=13, fontname="hebo", color=(0.2, 0.2, 0.2))

    shape = page3.new_shape()
    shape.draw_line(pymupdf.Point(72, 100), pymupdf.Point(540, 100))
    shape.finish(color=(0.7, 0.7, 0.7), width=1)
    shape.commit()

    page3.insert_text(pymupdf.Point(72, 140),
                      "Please certify the following by checking the appropriate boxes:",
                      fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))

    # Checkbox: irb_approved
    page3.insert_text(pymupdf.Point(100, 195),
                      "This research has received Institutional Review Board (IRB) approval,",
                      fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page3.insert_text(pymupdf.Point(100, 208),
                      "or IRB approval is not applicable to this research.",
                      fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))

    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "irb_approved"
    w.field_value = "Off"
    w.rect = pymupdf.Rect(72, 180, 92, 200)
    w.border_color = (0.3, 0.3, 0.3)
    w.border_width = 1
    page3.add_widget(w)

    # Checkbox: conflict_none
    page3.insert_text(pymupdf.Point(100, 265),
                      "The Principal Investigator and all co-investigators have no financial",
                      fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page3.insert_text(pymupdf.Point(100, 278),
                      "conflicts of interest related to this research project.",
                      fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))

    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "conflict_none"
    w.field_value = "Off"
    w.rect = pymupdf.Rect(72, 250, 92, 270)
    w.border_color = (0.3, 0.3, 0.3)
    w.border_width = 1
    page3.add_widget(w)

    # Checkbox: terms_accepted
    page3.insert_text(pymupdf.Point(100, 335),
                      "I have read and agree to the NSF Grant General Conditions, including",
                      fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page3.insert_text(pymupdf.Point(100, 348),
                      "data management, reporting requirements, and intellectual property terms.",
                      fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))

    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "terms_accepted"
    w.field_value = "Off"
    w.rect = pymupdf.Rect(72, 320, 92, 340)
    w.border_color = (0.3, 0.3, 0.3)
    w.border_width = 1
    page3.add_widget(w)

    # Additional compliance text
    page3.insert_text(pymupdf.Point(72, 420), "Important Notice:",
                      fontsize=11, fontname="hebo", color=(0.7, 0.1, 0.1))
    notice_text = (
        "By checking the boxes above, you certify that all statements made in this "
        "application are true and complete to the best of your knowledge. Any false "
        "statements or omissions may result in the denial or termination of the grant "
        "and may subject the applicant to legal penalties under federal law."
    )
    page3.insert_textbox(pymupdf.Rect(72, 435, 540, 550), notice_text,
                         fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    page3.insert_text(pymupdf.Point(72, 740), "Page 3 of 5",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 4: Project Abstract ---
    page4 = doc.new_page(width=612, height=792)

    shape = page4.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, 612, 60))
    shape.finish(fill=(0.16, 0.31, 0.52), color=(0.16, 0.31, 0.52))
    shape.commit()

    page4.insert_text(pymupdf.Point(72, 40), "NATIONAL SCIENCE FOUNDATION",
                      fontsize=20, fontname="hebo", color=(1, 1, 1))

    page4.insert_text(pymupdf.Point(72, 90), "Section 4: Project Abstract",
                      fontsize=13, fontname="hebo", color=(0.2, 0.2, 0.2))

    shape = page4.new_shape()
    shape.draw_line(pymupdf.Point(72, 100), pymupdf.Point(540, 100))
    shape.finish(color=(0.7, 0.7, 0.7), width=1)
    shape.commit()

    page4.insert_text(pymupdf.Point(72, 130),
                      "Provide a concise summary of the proposed research (max 300 words):",
                      fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))

    # Multi-line text area for abstract
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "abstract"
    w.field_value = ""
    w.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
    w.rect = pymupdf.Rect(72, 145, 540, 400)
    w.text_fontsize = 10
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 1
    page4.add_widget(w)

    page4.insert_text(pymupdf.Point(72, 430), "Keywords (comma-separated):",
                      fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))

    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "keywords"
    w.field_value = ""
    w.rect = pymupdf.Rect(72, 440, 540, 465)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 1
    page4.add_widget(w)

    page4.insert_text(pymupdf.Point(72, 740), "Page 4 of 5",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 5: References & Submission ---
    page5 = doc.new_page(width=612, height=792)

    shape = page5.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, 612, 60))
    shape.finish(fill=(0.16, 0.31, 0.52), color=(0.16, 0.31, 0.52))
    shape.commit()

    page5.insert_text(pymupdf.Point(72, 40), "NATIONAL SCIENCE FOUNDATION",
                      fontsize=20, fontname="hebo", color=(1, 1, 1))

    page5.insert_text(pymupdf.Point(72, 90), "Section 5: References & Submission",
                      fontsize=13, fontname="hebo", color=(0.2, 0.2, 0.2))

    shape = page5.new_shape()
    shape.draw_line(pymupdf.Point(72, 100), pymupdf.Point(540, 100))
    shape.finish(color=(0.7, 0.7, 0.7), width=1)
    shape.commit()

    page5.insert_text(pymupdf.Point(72, 130),
                      "List up to 5 professional references who can attest to your qualifications:",
                      fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))

    # Reference fields
    for i in range(1, 4):
        y_base = 140 + (i - 1) * 80
        page5.insert_text(pymupdf.Point(72, y_base + 20),
                          f"Reference {i}:",
                          fontsize=10, fontname="hebo", color=(0.3, 0.3, 0.3))

        w = pymupdf.Widget()
        w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
        w.field_name = f"reference_{i}_name"
        w.field_value = ""
        w.rect = pymupdf.Rect(72, y_base + 25, 350, y_base + 48)
        w.text_fontsize = 10
        w.fill_color = (0.97, 0.97, 0.97)
        w.border_color = (0.5, 0.5, 0.5)
        w.border_width = 1
        page5.add_widget(w)

        w = pymupdf.Widget()
        w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
        w.field_name = f"reference_{i}_email"
        w.field_value = ""
        w.rect = pymupdf.Rect(360, y_base + 25, 540, y_base + 48)
        w.text_fontsize = 10
        w.fill_color = (0.97, 0.97, 0.97)
        w.border_color = (0.5, 0.5, 0.5)
        w.border_width = 1
        page5.add_widget(w)

    # Submission info
    page5.insert_text(pymupdf.Point(72, 430), "Submission Deadline:",
                      fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
    page5.insert_text(pymupdf.Point(72, 448),
                      "March 31, 2026 at 5:00 PM Eastern Time",
                      fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))

    page5.insert_text(pymupdf.Point(72, 490), "Submit completed forms to:",
                      fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
    page5.insert_text(pymupdf.Point(72, 508),
                      "grants@nsf.gov  |  National Science Foundation",
                      fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page5.insert_text(pymupdf.Point(72, 523),
                      "2415 Eisenhower Avenue, Alexandria, Virginia 22314",
                      fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))

    page5.insert_text(pymupdf.Point(72, 740), "Page 5 of 5",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the form in evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
