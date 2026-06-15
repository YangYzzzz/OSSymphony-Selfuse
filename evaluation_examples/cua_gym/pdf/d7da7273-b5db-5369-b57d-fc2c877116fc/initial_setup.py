"""
Initial Setup: Create a fillable PDF tax form 1099 with 15 form fields
Task ID: pdf_gf3_027
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_027'
FORMS_DIR = f'{WORKDIR}/forms'
OUTPUT = f'{FORMS_DIR}/tax_form_1099.pdf'


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
    # --- Page 1: Payer and Recipient Information ---
    page1 = doc.new_page(width=612, height=792)  # Letter size

    # Title
    page1.insert_text(
        pymupdf.Point(72, 50),
        "FORM 1099-MISC",
        fontsize=20,
        fontname="hebo",
        color=(0, 0, 0.5),
    )
    page1.insert_text(
        pymupdf.Point(72, 72),
        "Miscellaneous Income",
        fontsize=14,
        fontname="helv",
        color=(0, 0, 0.5),
    )
    page1.insert_text(
        pymupdf.Point(72, 92),
        "Department of the Treasury - Internal Revenue Service",
        fontsize=9,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # Draw horizontal rule
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 100), pymupdf.Point(540, 100))
    shape.finish(color=(0, 0, 0.5), width=1.5)
    shape.commit()

    # Section: Payer Information
    page1.insert_text(pymupdf.Point(72, 125), "PAYER'S INFORMATION", fontsize=11, fontname="hebo", color=(0, 0, 0))

    # Field labels and form fields
    y_pos = 145

    # Field 1: PayerName (text)
    page1.insert_text(pymupdf.Point(72, y_pos), "Payer's Name:", fontsize=10, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "PayerName"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, y_pos - 12, 540, y_pos + 5)
    w.text_fontsize = 10
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 0.5
    page1.add_widget(w)

    y_pos += 30
    # Field 2: PayerTIN (text)
    page1.insert_text(pymupdf.Point(72, y_pos), "Payer's TIN:", fontsize=10, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "PayerTIN"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, y_pos - 12, 400, y_pos + 5)
    w.text_fontsize = 10
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 0.5
    page1.add_widget(w)

    y_pos += 35
    # Section: Recipient Information
    page1.insert_text(pymupdf.Point(72, y_pos), "RECIPIENT'S INFORMATION", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y_pos += 22

    # Field 3: Name (text) - REQUIRED
    page1.insert_text(pymupdf.Point(72, y_pos), "Recipient's Name *:", fontsize=10, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "Name"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, y_pos - 12, 540, y_pos + 5)
    w.text_fontsize = 10
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 0.5
    page1.add_widget(w)

    y_pos += 30
    # Field 4: TaxID (text) - REQUIRED
    page1.insert_text(pymupdf.Point(72, y_pos), "Tax ID (SSN/EIN) *:", fontsize=10, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "TaxID"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, y_pos - 12, 400, y_pos + 5)
    w.text_fontsize = 10
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 0.5
    page1.add_widget(w)

    y_pos += 30
    # Field 5: Address (text)
    page1.insert_text(pymupdf.Point(72, y_pos), "Street Address:", fontsize=10, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "Address"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, y_pos - 12, 540, y_pos + 5)
    w.text_fontsize = 10
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 0.5
    page1.add_widget(w)

    y_pos += 30
    # Field 6: City (text)
    page1.insert_text(pymupdf.Point(72, y_pos), "City:", fontsize=10, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "City"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, y_pos - 12, 350, y_pos + 5)
    w.text_fontsize = 10
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 0.5
    page1.add_widget(w)

    # Field 7: State (text)
    page1.insert_text(pymupdf.Point(365, y_pos), "State:", fontsize=10, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "State"
    w.field_value = ""
    w.rect = pymupdf.Rect(410, y_pos - 12, 470, y_pos + 5)
    w.text_fontsize = 10
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 0.5
    page1.add_widget(w)

    # Field 8: ZipCode (text)
    page1.insert_text(pymupdf.Point(480, y_pos), "Zip:", fontsize=10, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "ZipCode"
    w.field_value = ""
    w.rect = pymupdf.Rect(505, y_pos - 12, 540, y_pos + 5)
    w.text_fontsize = 10
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 0.5
    page1.add_widget(w)

    y_pos += 30
    # Field 9: AccountNumber (text)
    page1.insert_text(pymupdf.Point(72, y_pos), "Account Number:", fontsize=10, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "AccountNumber"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, y_pos - 12, 400, y_pos + 5)
    w.text_fontsize = 10
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 0.5
    page1.add_widget(w)

    y_pos += 35
    # Section: Income and Tax
    shape2 = page1.new_shape()
    shape2.draw_line(pymupdf.Point(72, y_pos - 10), pymupdf.Point(540, y_pos - 10))
    shape2.finish(color=(0, 0, 0.5), width=1)
    shape2.commit()

    page1.insert_text(pymupdf.Point(72, y_pos + 5), "INCOME AND TAX INFORMATION", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y_pos += 27

    # Field 10: Amount (text) - REQUIRED
    page1.insert_text(pymupdf.Point(72, y_pos), "Total Amount *:", fontsize=10, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "Amount"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, y_pos - 12, 350, y_pos + 5)
    w.text_fontsize = 10
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 0.5
    page1.add_widget(w)

    y_pos += 30
    # Field 11: FederalTax (text)
    page1.insert_text(pymupdf.Point(72, y_pos), "Federal Tax Withheld:", fontsize=10, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "FederalTax"
    w.field_value = ""
    w.rect = pymupdf.Rect(220, y_pos - 12, 350, y_pos + 5)
    w.text_fontsize = 10
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 0.5
    page1.add_widget(w)

    y_pos += 30
    # Field 12: StateTax (text)
    page1.insert_text(pymupdf.Point(72, y_pos), "State Tax Withheld:", fontsize=10, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "StateTax"
    w.field_value = ""
    w.rect = pymupdf.Rect(220, y_pos - 12, 350, y_pos + 5)
    w.text_fontsize = 10
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 0.5
    page1.add_widget(w)

    y_pos += 30
    # Field 13: DateFiled (text)
    page1.insert_text(pymupdf.Point(72, y_pos), "Date Filed:", fontsize=10, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "DateFiled"
    w.field_value = ""
    w.rect = pymupdf.Rect(200, y_pos - 12, 350, y_pos + 5)
    w.text_fontsize = 10
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.5, 0.5, 0.5)
    w.border_width = 0.5
    page1.add_widget(w)

    y_pos += 35
    # Section: Checkboxes
    shape3 = page1.new_shape()
    shape3.draw_line(pymupdf.Point(72, y_pos - 10), pymupdf.Point(540, y_pos - 10))
    shape3.finish(color=(0, 0, 0.5), width=1)
    shape3.commit()

    page1.insert_text(pymupdf.Point(72, y_pos + 5), "ADDITIONAL OPTIONS", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y_pos += 27

    # Field 14: Corrected (checkbox)
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "Corrected"
    w.field_value = "Off"
    w.rect = pymupdf.Rect(72, y_pos - 12, 92, y_pos + 5)
    w.border_color = (0, 0, 0)
    w.border_width = 1
    page1.add_widget(w)
    page1.insert_text(pymupdf.Point(100, y_pos), "CORRECTED (if checked)", fontsize=10, fontname="helv")

    y_pos += 25
    # Field 15: SecondTIN (checkbox)
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "SecondTIN"
    w.field_value = "Off"
    w.rect = pymupdf.Rect(72, y_pos - 12, 92, y_pos + 5)
    w.border_color = (0, 0, 0)
    w.border_width = 1
    page1.add_widget(w)
    page1.insert_text(pymupdf.Point(100, y_pos), "2nd TIN not.", fontsize=10, fontname="helv")

    # Footer
    y_pos += 40
    page1.insert_text(
        pymupdf.Point(72, y_pos),
        "* Required fields. Fields marked with * must be filled before submission.",
        fontsize=8,
        fontname="heit",
        color=(0.4, 0.4, 0.4),
    )
    page1.insert_text(
        pymupdf.Point(72, y_pos + 14),
        "Form 1099-MISC (Rev. 01-2025)  |  Cat. No. 14425J  |  IRS.gov/Form1099MISC",
        fontsize=8,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify field count
    verify_doc = pymupdf.open(OUTPUT)
    field_count = 0
    for page in verify_doc:
        for widget in page.widgets():
            field_count += 1
            print(f'  Field: {widget.field_name} ({widget.field_type_string})')
    verify_doc.close()
    print(f'Total form fields: {field_count}')

    # Install pdfrw and ensure PyMuPDF is available for the agent
    subprocess.run(['pip3', 'install', 'pdfrw', 'PyMuPDF'], capture_output=True)

    # Open the PDF in evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
