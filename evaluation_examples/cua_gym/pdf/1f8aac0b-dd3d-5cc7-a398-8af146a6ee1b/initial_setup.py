"""
Initial Setup: Create a fillable W-2 tax form PDF with empty fields
Task ID: pdf_basic_072
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
OUTPUT = f'{WORKDIR}/tax_form_w2.pdf'


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
    # Ensure Desktop directory exists
    os.makedirs(WORKDIR, exist_ok=True)

    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)  # Letter size

    # --- Title and header ---
    shape = page.new_shape()
    # Header background
    shape.draw_rect(pymupdf.Rect(36, 30, 576, 80))
    shape.finish(color=(0.1, 0.2, 0.5), fill=(0.1, 0.2, 0.5), width=0)
    shape.commit()

    page.insert_text(
        pymupdf.Point(180, 60),
        "Form W-2  Wage and Tax Statement",
        fontsize=16,
        fontname="hebo",
        color=(1, 1, 1),
    )
    page.insert_text(
        pymupdf.Point(36, 95),
        "Tax Year: 2024",
        fontsize=10,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )

    # --- Section: Employer Information ---
    page.insert_text(
        pymupdf.Point(36, 130),
        "EMPLOYER INFORMATION",
        fontsize=11,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(36, 135), pymupdf.Point(576, 135))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    # --- Employer Name field ---
    page.insert_text(
        pymupdf.Point(36, 160),
        "Employer Name:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "Employer Name"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(150, 147, 450, 167)
    widget.text_fontsize = 11
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.97, 0.97, 1.0)
    widget.border_color = (0.3, 0.3, 0.6)
    widget.border_width = 1
    page.add_widget(widget)

    # --- Section: Employee Information ---
    page.insert_text(
        pymupdf.Point(36, 195),
        "EMPLOYEE & WAGE INFORMATION",
        fontsize=11,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(36, 200), pymupdf.Point(576, 200))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    # --- Wages field ---
    page.insert_text(
        pymupdf.Point(36, 228),
        "Wages, Tips, Other Compensation:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(36, 243),
        "(Box 1)",
        fontsize=8,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "Wages"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(260, 217, 430, 237)
    widget.text_fontsize = 11
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.97, 0.97, 1.0)
    widget.border_color = (0.3, 0.3, 0.6)
    widget.border_width = 1
    page.add_widget(widget)

    # --- Federal Tax Withheld field ---
    page.insert_text(
        pymupdf.Point(36, 275),
        "Federal Income Tax Withheld:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(36, 290),
        "(Box 2)",
        fontsize=8,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "Federal Tax Withheld"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(260, 264, 430, 284)
    widget.text_fontsize = 11
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.97, 0.97, 1.0)
    widget.border_color = (0.3, 0.3, 0.6)
    widget.border_width = 1
    page.add_widget(widget)

    # --- State Tax Information ---
    page.insert_text(
        pymupdf.Point(36, 330),
        "STATE TAX INFORMATION",
        fontsize=11,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(36, 335), pymupdf.Point(576, 335))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    # --- State field ---
    page.insert_text(
        pymupdf.Point(36, 363),
        "State:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(36, 378),
        "(2-letter code, e.g., NY, CA)",
        fontsize=8,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "State"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(100, 352, 200, 372)
    widget.text_fontsize = 11
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.97, 0.97, 1.0)
    widget.border_color = (0.3, 0.3, 0.6)
    widget.border_width = 1
    page.add_widget(widget)

    # --- Instructions footer ---
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 680, 576, 720))
    shape.finish(color=(0.8, 0.8, 0.8), fill=(0.95, 0.95, 0.95), width=0.5)
    shape.commit()
    page.insert_text(
        pymupdf.Point(45, 695),
        "Instructions: Fill in all required fields above. All monetary amounts should be in USD.",
        fontsize=9,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(45, 710),
        "Save the form after completing all fields. Keep a copy for your records.",
        fontsize=9,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # Set metadata
    doc.set_metadata({
        "title": "Form W-2 Wage and Tax Statement 2024",
        "author": "IRS",
        "subject": "W-2 Tax Form",
        "keywords": "W-2, wages, tax, federal, state",
        "creator": "CUA-Gym Setup",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
