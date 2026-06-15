"""
Initial Setup: Civil Cover Sheet fillable PDF form
Task ID: pdf_legal_013
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
TASK_ID = 'pdf_legal_013'
FORM_DIR = f'{WORKDIR}/legal/forms'
OUTPUT = f'{FORM_DIR}/civil_cover_sheet.pdf'


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

    # --- Page 1: Civil Cover Sheet ---
    page = doc.new_page(width=612, height=792)  # US Letter

    # Header area - court seal / decorative line
    shape = page.new_shape()
    # Top border line
    shape.draw_line(pymupdf.Point(72, 60), pymupdf.Point(540, 60))
    shape.finish(color=(0, 0, 0), width=2)
    shape.draw_line(pymupdf.Point(72, 63), pymupdf.Point(540, 63))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()

    # Court header text
    page.insert_text(pymupdf.Point(170, 45), "CIVIL COVER SHEET",
                     fontsize=18, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(155, 80),
                     "JUDICIAL COUNCIL OF CALIFORNIA",
                     fontsize=10, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(190, 95),
                     "Form CM-010 (Rev. January 2024)",
                     fontsize=8, fontname="heit", color=(0.3, 0.3, 0.3))

    # Instructions block
    page.insert_text(pymupdf.Point(72, 125),
                     "INSTRUCTIONS: This cover sheet must be filed with the first paper",
                     fontsize=9, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 138),
                     "in every civil action or proceeding (except small claims cases and",
                     fontsize=9, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 151),
                     "unlawful detainer cases). Complete all applicable items below.",
                     fontsize=9, fontname="helv", color=(0, 0, 0))

    # Section 1: Case Information
    shape2 = page.new_shape()
    shape2.draw_rect(pymupdf.Rect(72, 170, 540, 185))
    shape2.finish(color=(0, 0, 0), fill=(0.85, 0.85, 0.85), width=1)
    shape2.commit()

    page.insert_text(pymupdf.Point(78, 182),
                     "SECTION 1: CASE INFORMATION",
                     fontsize=10, fontname="hebo", color=(0, 0, 0))

    # Field labels and form fields
    y_pos = 210

    # 1. Case Title
    page.insert_text(pymupdf.Point(72, y_pos), "1. Case Title:",
                     fontsize=10, fontname="hebo", color=(0, 0, 0))
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "CaseTitle"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(170, y_pos - 12, 540, y_pos + 5)
    widget.text_fontsize = 10
    widget.text_color = (0, 0, 0)
    widget.fill_color = (1, 1, 1)
    widget.border_color = (0, 0, 0)
    widget.border_width = 1
    page.add_widget(widget)

    y_pos += 35

    # 2. Case Number
    page.insert_text(pymupdf.Point(72, y_pos), "2. Case Number:",
                     fontsize=10, fontname="hebo", color=(0, 0, 0))
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "CaseNumber"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(185, y_pos - 12, 400, y_pos + 5)
    widget.text_fontsize = 10
    widget.text_color = (0, 0, 0)
    widget.fill_color = (1, 1, 1)
    widget.border_color = (0, 0, 0)
    widget.border_width = 1
    page.add_widget(widget)

    y_pos += 35

    # 3. Court
    page.insert_text(pymupdf.Point(72, y_pos), "3. Court:",
                     fontsize=10, fontname="hebo", color=(0, 0, 0))
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "Court"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(140, y_pos - 12, 540, y_pos + 5)
    widget.text_fontsize = 10
    widget.text_color = (0, 0, 0)
    widget.fill_color = (1, 1, 1)
    widget.border_color = (0, 0, 0)
    widget.border_width = 1
    page.add_widget(widget)

    y_pos += 35

    # 4. Filing Date
    page.insert_text(pymupdf.Point(72, y_pos), "4. Filing Date:",
                     fontsize=10, fontname="hebo", color=(0, 0, 0))
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "FilingDate"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(170, y_pos - 12, 350, y_pos + 5)
    widget.text_fontsize = 10
    widget.text_color = (0, 0, 0)
    widget.fill_color = (1, 1, 1)
    widget.border_color = (0, 0, 0)
    widget.border_width = 1
    page.add_widget(widget)

    # Section 2: Attorney Information
    y_pos += 50

    shape3 = page.new_shape()
    shape3.draw_rect(pymupdf.Rect(72, y_pos - 15, 540, y_pos))
    shape3.finish(color=(0, 0, 0), fill=(0.85, 0.85, 0.85), width=1)
    shape3.commit()

    page.insert_text(pymupdf.Point(78, y_pos - 3),
                     "SECTION 2: ATTORNEY INFORMATION",
                     fontsize=10, fontname="hebo", color=(0, 0, 0))

    y_pos += 25

    # 5. Attorney Name
    page.insert_text(pymupdf.Point(72, y_pos), "5. Attorney Name:",
                     fontsize=10, fontname="hebo", color=(0, 0, 0))
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "AttorneyName"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(195, y_pos - 12, 540, y_pos + 5)
    widget.text_fontsize = 10
    widget.text_color = (0, 0, 0)
    widget.fill_color = (1, 1, 1)
    widget.border_color = (0, 0, 0)
    widget.border_width = 1
    page.add_widget(widget)

    y_pos += 35

    # 6. Bar Number
    page.insert_text(pymupdf.Point(72, y_pos), "6. Bar Number:",
                     fontsize=10, fontname="hebo", color=(0, 0, 0))
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "BarNumber"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(175, y_pos - 12, 350, y_pos + 5)
    widget.text_fontsize = 10
    widget.text_color = (0, 0, 0)
    widget.fill_color = (1, 1, 1)
    widget.border_color = (0, 0, 0)
    widget.border_width = 1
    page.add_widget(widget)

    # Additional static content - case type checkboxes section
    y_pos += 60

    shape4 = page.new_shape()
    shape4.draw_rect(pymupdf.Rect(72, y_pos - 15, 540, y_pos))
    shape4.finish(color=(0, 0, 0), fill=(0.85, 0.85, 0.85), width=1)
    shape4.commit()

    page.insert_text(pymupdf.Point(78, y_pos - 3),
                     "SECTION 3: TYPE OF ACTION (Check one box)",
                     fontsize=10, fontname="hebo", color=(0, 0, 0))

    y_pos += 20
    case_types = [
        "Auto Tort - Personal Injury/Property Damage/Wrongful Death",
        "Non-Auto Tort - Premises Liability",
        "Non-Auto Tort - Medical Malpractice",
        "Contract - Breach of Contract/Warranty",
        "Real Property - Eminent Domain/Inverse Condemnation",
        "Employment - Wrongful Termination",
        "Other Civil Complaint (Non-Tort/Non-Complex)",
    ]

    for ct in case_types:
        page.insert_text(pymupdf.Point(90, y_pos), ct,
                         fontsize=8, fontname="helv", color=(0, 0, 0))
        # Draw checkbox square
        shape5 = page.new_shape()
        shape5.draw_rect(pymupdf.Rect(74, y_pos - 8, 85, y_pos + 3))
        shape5.finish(color=(0, 0, 0), fill=(1, 1, 1), width=0.5)
        shape5.commit()
        y_pos += 16

    # Footer
    shape6 = page.new_shape()
    shape6.draw_line(pymupdf.Point(72, 740), pymupdf.Point(540, 740))
    shape6.finish(color=(0, 0, 0), width=0.5)
    shape6.commit()

    page.insert_text(pymupdf.Point(72, 755),
                     "CM-010 [Rev. January 2024]",
                     fontsize=7, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(420, 755),
                     "Page 1 of 1",
                     fontsize=7, fontname="helv", color=(0.4, 0.4, 0.4))

    # Set document metadata
    doc.set_metadata({
        "title": "Civil Cover Sheet - CM-010",
        "author": "Judicial Council of California",
        "subject": "Civil Case Filing",
        "keywords": "civil, cover sheet, court filing, California",
        "creator": "Court Forms System",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the form in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
