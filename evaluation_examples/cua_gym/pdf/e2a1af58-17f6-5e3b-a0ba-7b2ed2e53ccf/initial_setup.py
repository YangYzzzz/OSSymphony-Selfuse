"""
Initial Setup: Create a 2-page fillable tax form with 5 empty form fields
Task ID: pdf_ro_006
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_006'
FORMS_DIR = f'{WORKDIR}/forms'
OUTPUT = f'{FORMS_DIR}/tax_form.pdf'


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

    # ===== PAGE 1: Personal Information & Filing Status =====
    page1 = doc.new_page(width=612, height=792)  # Letter size

    # Header
    page1.insert_text(
        pymupdf.Point(72, 50),
        "FEDERAL INCOME TAX RETURN",
        fontsize=18,
        fontname="hebo",
        color=(0, 0, 0.5),
    )
    page1.insert_text(
        pymupdf.Point(72, 70),
        "Form 1040-EZ  |  Tax Year 2025",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # Horizontal line
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0, 0.5), width=1.5)
    shape.commit()

    # Section 1: Personal Information
    page1.insert_text(pymupdf.Point(72, 110), "Section 1: Personal Information",
                      fontsize=14, fontname="hebo", color=(0, 0, 0))

    # Taxpayer Name label and field
    page1.insert_text(pymupdf.Point(72, 145), "Taxpayer Name:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "taxpayer_name"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(200, 130, 500, 150)
    widget.text_fontsize = 11
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.97, 0.97, 0.97)
    widget.border_color = (0.4, 0.4, 0.4)
    widget.border_width = 1
    page1.add_widget(widget)

    # SSN label and field
    page1.insert_text(pymupdf.Point(72, 195), "Social Security Number:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "ssn"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(250, 180, 450, 200)
    widget.text_fontsize = 11
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.97, 0.97, 0.97)
    widget.border_color = (0.4, 0.4, 0.4)
    widget.border_width = 1
    page1.add_widget(widget)

    # Section 2: Filing Status
    page1.insert_text(pymupdf.Point(72, 250), "Section 2: Filing Status",
                      fontsize=14, fontname="hebo", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(72, 285), "Filing Status:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 300),
                      "(Single, Married Filing Jointly, Married Filing Separately, Head of Household)",
                      fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4))
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "filing_status"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(200, 270, 450, 290)
    widget.text_fontsize = 11
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.97, 0.97, 0.97)
    widget.border_color = (0.4, 0.4, 0.4)
    widget.border_width = 1
    page1.add_widget(widget)

    # Additional static content for realism
    page1.insert_text(pymupdf.Point(72, 350), "Instructions:",
                      fontsize=12, fontname="hebo", color=(0, 0, 0))
    instructions = (
        "Please fill in all fields completely and accurately. Use blue or black ink if "
        "completing by hand. For electronic filing, type your responses in the form fields "
        "provided. Ensure your Social Security Number is entered in the format XXX-XX-XXXX. "
        "Select your filing status from the options listed above. If you are unsure of your "
        "filing status, refer to the IRS Publication 501 for guidance."
    )
    page1.insert_textbox(
        pymupdf.Rect(72, 365, 540, 500),
        instructions,
        fontsize=10,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Footer on page 1
    page1.insert_text(pymupdf.Point(72, 750), "Form 1040-EZ (2025)  |  Page 1 of 2",
                      fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # ===== PAGE 2: Income & Tax Computation =====
    page2 = doc.new_page(width=612, height=792)

    # Header
    page2.insert_text(
        pymupdf.Point(72, 50),
        "FEDERAL INCOME TAX RETURN (continued)",
        fontsize=16,
        fontname="hebo",
        color=(0, 0, 0.5),
    )

    # Horizontal line
    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 65), pymupdf.Point(540, 65))
    shape2.finish(color=(0, 0, 0.5), width=1.5)
    shape2.commit()

    # Section 3: Income
    page2.insert_text(pymupdf.Point(72, 95), "Section 3: Income",
                      fontsize=14, fontname="hebo", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(72, 130), "Gross Income:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(72, 145),
                      "(Wages, salaries, tips, and other compensation as reported on W-2)",
                      fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4))
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "gross_income"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(200, 115, 400, 135)
    widget.text_fontsize = 11
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.97, 0.97, 0.97)
    widget.border_color = (0.4, 0.4, 0.4)
    widget.border_width = 1
    page2.add_widget(widget)

    # Section 4: Tax Computation
    page2.insert_text(pymupdf.Point(72, 195), "Section 4: Tax Computation",
                      fontsize=14, fontname="hebo", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(72, 230), "Tax Owed:",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(72, 245),
                      "(Total federal income tax liability for the tax year)",
                      fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4))
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "tax_owed"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(200, 215, 400, 235)
    widget.text_fontsize = 11
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.97, 0.97, 0.97)
    widget.border_color = (0.4, 0.4, 0.4)
    widget.border_width = 1
    page2.add_widget(widget)

    # Tax table reference (static content for realism)
    page2.insert_text(pymupdf.Point(72, 290), "Reference: Tax Rate Schedule (2025)",
                      fontsize=12, fontname="hebo", color=(0, 0, 0))

    tax_table = [
        ("Taxable Income Range", "Tax Rate"),
        ("$0 - $11,600", "10%"),
        ("$11,601 - $47,150", "12%"),
        ("$47,151 - $100,525", "22%"),
        ("$100,526 - $191,950", "24%"),
        ("$191,951 - $243,725", "32%"),
        ("$243,726 - $609,350", "35%"),
        ("Over $609,350", "37%"),
    ]

    y_start = 310
    for i, (bracket, rate) in enumerate(tax_table):
        y = y_start + i * 18
        font = "hebo" if i == 0 else "helv"
        page2.insert_text(pymupdf.Point(100, y), bracket, fontsize=10, fontname=font, color=(0, 0, 0))
        page2.insert_text(pymupdf.Point(350, y), rate, fontsize=10, fontname=font, color=(0, 0, 0))

    # Signature block
    page2.insert_text(pymupdf.Point(72, 520), "Declaration:",
                      fontsize=12, fontname="hebo", color=(0, 0, 0))
    page2.insert_textbox(
        pymupdf.Rect(72, 535, 540, 600),
        "Under penalties of perjury, I declare that I have examined this return and "
        "accompanying schedules and statements, and to the best of my knowledge and belief, "
        "they are true, correct, and complete.",
        fontsize=9,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Signature line
    shape3 = page2.new_shape()
    shape3.draw_line(pymupdf.Point(72, 640), pymupdf.Point(350, 640))
    shape3.finish(color=(0, 0, 0), width=0.5)
    shape3.draw_line(pymupdf.Point(380, 640), pymupdf.Point(540, 640))
    shape3.finish(color=(0, 0, 0), width=0.5)
    shape3.commit()
    page2.insert_text(pymupdf.Point(72, 655), "Signature", fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4))
    page2.insert_text(pymupdf.Point(380, 655), "Date", fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4))

    # Footer on page 2
    page2.insert_text(pymupdf.Point(72, 750), "Form 1040-EZ (2025)  |  Page 2 of 2",
                      fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
