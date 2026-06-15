"""
Initial Setup: Create a purchase order PDF form with checkboxes and radio buttons.
Task ID: pdf_fm_013
Domain: pdf

Creates ~/Documents/forms/purchase_order.pdf with:
- Text fields for order info
- Checkboxes: agree_to_terms (Off), subscribe_newsletter (Off)
- Radio-style checkboxes: standard_shipping (Off), express_shipping (Off), overnight_shipping (Off)
All unchecked.
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
TASK_ID = 'pdf_fm_013'
FORMS_DIR = f'{WORKDIR}/Documents/forms'
OUTPUT = f'{FORMS_DIR}/purchase_order.pdf'


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
    page = doc.new_page(width=612, height=792)  # Letter size

    # ---- Header ----
    page.insert_text(
        pymupdf.Point(72, 50),
        "Meridian Supply Co.",
        fontsize=22,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )
    page.insert_text(
        pymupdf.Point(72, 70),
        "1425 Commerce Blvd, Suite 300  |  Portland, OR 97201  |  (503) 555-0147",
        fontsize=8,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )

    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    page.insert_text(
        pymupdf.Point(72, 105),
        "PURCHASE ORDER FORM",
        fontsize=16,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # ---- Order Info Section ----
    y = 140
    labels_fields = [
        ("Order Number:", "order_number", "PO-2026-04187", y),
        ("Order Date:", "order_date", "2026-03-28", y + 35),
        ("Customer Name:", "customer_name", "Avery Nakamura", y + 70),
        ("Customer Email:", "customer_email", "a.nakamura@westridgedesigns.com", y + 105),
    ]

    for label, field_name, default_val, field_y in labels_fields:
        page.insert_text(
            pymupdf.Point(72, field_y),
            label,
            fontsize=10,
            fontname="hebo",
            color=(0, 0, 0),
        )
        widget = pymupdf.Widget()
        widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
        widget.field_name = field_name
        widget.field_value = default_val
        widget.rect = pymupdf.Rect(200, field_y - 12, 400, field_y + 5)
        widget.text_fontsize = 10
        widget.text_color = (0, 0, 0)
        widget.fill_color = (0.96, 0.96, 0.96)
        widget.border_color = (0.6, 0.6, 0.6)
        widget.border_width = 0.5
        page.add_widget(widget)

    # ---- Shipping Address ----
    addr_y = y + 150
    page.insert_text(
        pymupdf.Point(72, addr_y),
        "Shipping Address:",
        fontsize=10,
        fontname="hebo",
        color=(0, 0, 0),
    )
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "shipping_address"
    widget.field_value = "8721 Maple Ridge Dr, Unit 4B\nBoulder, CO 80302"
    widget.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
    widget.rect = pymupdf.Rect(200, addr_y - 12, 540, addr_y + 35)
    widget.text_fontsize = 9
    widget.text_color = (0, 0, 0)
    widget.fill_color = (0.96, 0.96, 0.96)
    widget.border_color = (0.6, 0.6, 0.6)
    widget.border_width = 0.5
    page.add_widget(widget)

    # ---- Order Items Table (static text) ----
    table_y = addr_y + 70
    page.insert_text(
        pymupdf.Point(72, table_y),
        "Order Items",
        fontsize=12,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    th_y = table_y + 20
    headers = ["Item", "SKU", "Qty", "Unit Price", "Total"]
    hx = [72, 220, 330, 390, 480]
    for i, h in enumerate(headers):
        page.insert_text(
            pymupdf.Point(hx[i], th_y),
            h,
            fontsize=9,
            fontname="hebo",
            color=(0.3, 0.3, 0.3),
        )

    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(72, th_y + 5), pymupdf.Point(540, th_y + 5))
    shape2.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape2.commit()

    items = [
        ("Ergonomic Desk Chair", "MC-4520-BLK", "2", "$349.00", "$698.00"),
        ("Standing Desk Converter", "SD-1180-WAL", "1", "$275.00", "$275.00"),
        ("Monitor Arm (Dual)", "MA-2200-SLV", "2", "$89.50", "$179.00"),
        ("Cable Management Kit", "CM-0055-WHT", "3", "$24.99", "$74.97"),
        ("LED Desk Lamp", "DL-7710-BLK", "2", "$62.00", "$124.00"),
    ]
    row_y = th_y + 20
    for item in items:
        for i, val in enumerate(item):
            page.insert_text(
                pymupdf.Point(hx[i], row_y),
                val,
                fontsize=9,
                fontname="helv",
                color=(0, 0, 0),
            )
        row_y += 16

    row_y += 5
    shape3 = page.new_shape()
    shape3.draw_line(pymupdf.Point(380, row_y - 8), pymupdf.Point(540, row_y - 8))
    shape3.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape3.commit()

    page.insert_text(pymupdf.Point(390, row_y + 5), "Subtotal:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(480, row_y + 5), "$1,350.97", fontsize=9, fontname="helv", color=(0, 0, 0))

    # ---- Shipping Method (using individually-named checkboxes to simulate radio buttons) ----
    ship_y = row_y + 40
    page.insert_text(
        pymupdf.Point(72, ship_y),
        "Shipping Method (select one):",
        fontsize=11,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    shipping_options = [
        ("standard_shipping", "Standard Shipping (5-7 business days) - Free", ship_y + 22),
        ("express_shipping", "Express Shipping (2-3 business days) - $14.99", ship_y + 42),
        ("overnight_shipping", "Overnight Shipping (next business day) - $29.99", ship_y + 62),
    ]

    for field_name, label, ry in shipping_options:
        widget = pymupdf.Widget()
        widget.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
        widget.field_name = field_name
        widget.field_value = "Off"
        widget.rect = pymupdf.Rect(90, ry - 10, 106, ry + 6)
        widget.border_color = (0.4, 0.4, 0.4)
        widget.border_width = 1
        page.add_widget(widget)

        page.insert_text(
            pymupdf.Point(112, ry + 2),
            label,
            fontsize=9,
            fontname="helv",
            color=(0, 0, 0),
        )

    # ---- Checkboxes ----
    cb_y = ship_y + 95
    page.insert_text(
        pymupdf.Point(72, cb_y),
        "Terms & Preferences:",
        fontsize=11,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    checkboxes = [
        ("agree_to_terms", "I agree to the Terms and Conditions of Meridian Supply Co.", cb_y + 22),
        ("subscribe_newsletter", "Subscribe to our monthly product newsletter", cb_y + 42),
    ]

    for field_name, label, cy in checkboxes:
        widget = pymupdf.Widget()
        widget.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
        widget.field_name = field_name
        widget.field_value = "Off"
        widget.rect = pymupdf.Rect(90, cy - 10, 106, cy + 6)
        widget.border_color = (0.4, 0.4, 0.4)
        widget.border_width = 1
        page.add_widget(widget)

        page.insert_text(
            pymupdf.Point(112, cy + 2),
            label,
            fontsize=9,
            fontname="helv",
            color=(0, 0, 0),
        )

    # ---- Footer ----
    page.insert_text(
        pymupdf.Point(72, 750),
        "Meridian Supply Co. - All orders subject to verification. Allow 24h for processing.",
        fontsize=7,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
