"""
Initial Setup: Create a PDF feedback survey form with empty fields.
Task ID: pdf_fm_043
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_043'
FORM_DIR = f'{WORKDIR}/Documents/forms'
OUTPUT = f'{FORM_DIR}/feedback_survey.pdf'


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
    # Ensure directory exists
    os.makedirs(FORM_DIR, exist_ok=True)

    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)  # A4

    # ---- Title ----
    page.insert_text(
        pymupdf.Point(150, 60),
        "Customer Feedback Survey",
        fontsize=22,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    # ---- Subtitle / instructions ----
    page.insert_text(
        pymupdf.Point(72, 100),
        "Thank you for taking the time to share your feedback. Please fill out all fields below.",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # Horizontal separator line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 115), pymupdf.Point(523, 115))
    shape.finish(color=(0.6, 0.6, 0.6), width=1)
    shape.commit()

    # ---- Section 1: Overall Satisfaction ----
    page.insert_text(
        pymupdf.Point(72, 155),
        "1. Overall Satisfaction",
        fontsize=14,
        fontname="hebo",
        color=(0.15, 0.15, 0.15),
    )
    page.insert_text(
        pymupdf.Point(72, 175),
        "How satisfied are you with our product/service?",
        fontsize=11,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )

    # Dropdown (ComboBox) for satisfaction
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_COMBOBOX
    widget.field_name = "satisfaction"
    widget.choice_values = ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied"]
    widget.field_value = ""  # Empty - no selection
    widget.rect = pymupdf.Rect(72, 190, 300, 215)
    widget.text_fontsize = 11
    widget.fill_color = (1, 1, 1)
    widget.border_color = (0.4, 0.4, 0.4)
    widget.border_width = 1
    page.add_widget(widget)

    # ---- Section 2: Recommendation ----
    page.insert_text(
        pymupdf.Point(72, 260),
        "2. Recommendation",
        fontsize=14,
        fontname="hebo",
        color=(0.15, 0.15, 0.15),
    )
    page.insert_text(
        pymupdf.Point(72, 280),
        "Would you recommend our product/service to others?",
        fontsize=11,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )

    # Checkbox for recommend
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    widget.field_name = "recommend"
    widget.field_value = "Off"  # Unchecked
    widget.rect = pymupdf.Rect(72, 295, 92, 315)
    widget.border_color = (0.4, 0.4, 0.4)
    widget.border_width = 1
    page.add_widget(widget)

    page.insert_text(
        pymupdf.Point(100, 310),
        "Yes, I would recommend this product/service",
        fontsize=11,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )

    # ---- Section 3: Comments ----
    page.insert_text(
        pymupdf.Point(72, 365),
        "3. Additional Comments",
        fontsize=14,
        fontname="hebo",
        color=(0.15, 0.15, 0.15),
    )
    page.insert_text(
        pymupdf.Point(72, 385),
        "Please share any additional feedback or suggestions:",
        fontsize=11,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )

    # Multiline text field for comments
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "comments"
    widget.field_value = ""  # Empty
    widget.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
    widget.rect = pymupdf.Rect(72, 400, 523, 520)
    widget.text_fontsize = 11
    widget.fill_color = (1, 1, 1)
    widget.border_color = (0.4, 0.4, 0.4)
    widget.border_width = 1
    page.add_widget(widget)

    # ---- Footer ----
    page.insert_text(
        pymupdf.Point(72, 780),
        "Acme Corp - Customer Experience Team",
        fontsize=9,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )
    page.insert_text(
        pymupdf.Point(380, 780),
        "Form Version 2.1 | 2025",
        fontsize=9,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince (Okular not available on this VM image; evince is the fallback)
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
