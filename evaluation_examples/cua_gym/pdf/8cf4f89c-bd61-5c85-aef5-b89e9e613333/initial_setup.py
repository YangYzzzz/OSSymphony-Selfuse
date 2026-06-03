"""
Initial Setup: Create a 3-page invoice PDF with no stamps or annotations.
Task ID: pdf_ro_045
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_045'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/invoice.pdf'

LETTER_W, LETTER_H = 612, 792


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
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # ── Page 1: Invoice header + line items ──
    page1 = doc.new_page(width=LETTER_W, height=LETTER_H)

    # Company header
    page1.insert_text(pymupdf.Point(72, 60), "Meridian Logistics Inc.", fontsize=22, fontname="hebo", color=(0.1, 0.2, 0.5))
    page1.insert_text(pymupdf.Point(72, 80), "1500 Commerce Boulevard, Suite 400", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page1.insert_text(pymupdf.Point(72, 94), "Portland, OR 97201  |  (503) 555-8742  |  billing@meridianlogistics.com", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    # Horizontal rule
    shape1 = page1.new_shape()
    shape1.draw_line(pymupdf.Point(72, 110), pymupdf.Point(540, 110))
    shape1.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape1.commit()

    # Invoice title and number
    page1.insert_text(pymupdf.Point(72, 140), "INVOICE", fontsize=28, fontname="hebo", color=(0.1, 0.2, 0.5))
    page1.insert_text(pymupdf.Point(400, 135), "Invoice #: INV-2025-03847", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(400, 152), "Date: March 15, 2025", fontsize=10, fontname="helv", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(400, 166), "Due Date: April 14, 2025", fontsize=10, fontname="helv", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(400, 180), "PO Number: PO-9921-A", fontsize=10, fontname="helv", color=(0, 0, 0))

    # Bill To
    page1.insert_text(pymupdf.Point(72, 180), "Bill To:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 196), "Cascade Manufacturing Ltd.", fontsize=10, fontname="helv", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 210), "Attn: Sarah Chen, Accounts Payable", fontsize=10, fontname="helv", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 224), "2800 Industrial Parkway", fontsize=10, fontname="helv", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 238), "Seattle, WA 98134", fontsize=10, fontname="helv", color=(0, 0, 0))

    # Table header
    y_start = 275
    headers = ["Item", "Description", "Qty", "Unit Price", "Total"]
    x_positions = [72, 120, 340, 400, 480]

    # Header background
    shape1b = page1.new_shape()
    shape1b.draw_rect(pymupdf.Rect(70, y_start - 14, 542, y_start + 4))
    shape1b.finish(fill=(0.1, 0.2, 0.5), color=(0.1, 0.2, 0.5))
    shape1b.commit()

    for i, h in enumerate(headers):
        page1.insert_text(pymupdf.Point(x_positions[i], y_start), h, fontsize=10, fontname="hebo", color=(1, 1, 1))

    # Line items
    items = [
        ("1", "Full Truckload Shipping - Portland to Seattle", "3", "$1,850.00", "$5,550.00"),
        ("2", "LTL Freight - Portland to San Francisco", "1", "$975.00", "$975.00"),
        ("3", "Refrigerated Container Rental (7 days)", "2", "$420.00", "$840.00"),
        ("4", "Warehouse Storage - Bay C (March 1-15)", "1", "$1,200.00", "$1,200.00"),
        ("5", "Pallet Wrapping & Labeling Service", "45", "$12.50", "$562.50"),
        ("6", "Customs Documentation Processing", "2", "$350.00", "$700.00"),
        ("7", "Forklift Loading/Unloading", "6", "$185.00", "$1,110.00"),
        ("8", "Express Delivery Surcharge", "1", "$450.00", "$450.00"),
        ("9", "Fuel Surcharge (8.5%)", "1", "$471.75", "$471.75"),
        ("10", "Insurance - Cargo Coverage ($50k)", "1", "$275.00", "$275.00"),
        ("11", "Route Planning & Optimization", "1", "$600.00", "$600.00"),
        ("12", "GPS Tracking Service (per shipment)", "4", "$35.00", "$140.00"),
    ]

    y = y_start + 22
    for idx, item in enumerate(items):
        bg_color = (0.95, 0.95, 0.98) if idx % 2 == 0 else (1, 1, 1)
        shape_row = page1.new_shape()
        shape_row.draw_rect(pymupdf.Rect(70, y - 12, 542, y + 6))
        shape_row.finish(fill=bg_color, color=bg_color)
        shape_row.commit()
        for i, val in enumerate(item):
            page1.insert_text(pymupdf.Point(x_positions[i], y), val, fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 20

    # Page 1 footer
    page1.insert_text(pymupdf.Point(260, 760), "Page 1 of 3", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # ── Page 2: Additional items + subtotals ──
    page2 = doc.new_page(width=LETTER_W, height=LETTER_H)

    page2.insert_text(pymupdf.Point(72, 50), "Meridian Logistics Inc.", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.5))
    page2.insert_text(pymupdf.Point(72, 66), "Invoice #: INV-2025-03847 (continued)", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    # More line items
    extra_items = [
        ("13", "Driver Wait Time (2.5 hrs @ $85/hr)", "1", "$212.50", "$212.50"),
        ("14", "Liftgate Delivery Service", "3", "$95.00", "$285.00"),
        ("15", "Saturday Delivery Premium", "1", "$325.00", "$325.00"),
    ]

    y2_start = 100
    # Header
    shape2h = page2.new_shape()
    shape2h.draw_rect(pymupdf.Rect(70, y2_start - 14, 542, y2_start + 4))
    shape2h.finish(fill=(0.1, 0.2, 0.5), color=(0.1, 0.2, 0.5))
    shape2h.commit()
    for i, h in enumerate(headers):
        page2.insert_text(pymupdf.Point(x_positions[i], y2_start), h, fontsize=10, fontname="hebo", color=(1, 1, 1))

    y2 = y2_start + 22
    for idx, item in enumerate(extra_items):
        bg_color = (0.95, 0.95, 0.98) if idx % 2 == 0 else (1, 1, 1)
        shape_r2 = page2.new_shape()
        shape_r2.draw_rect(pymupdf.Rect(70, y2 - 12, 542, y2 + 6))
        shape_r2.finish(fill=bg_color, color=bg_color)
        shape_r2.commit()
        for i, val in enumerate(item):
            page2.insert_text(pymupdf.Point(x_positions[i], y2), val, fontsize=9, fontname="helv", color=(0, 0, 0))
        y2 += 20

    # Totals section
    y_totals = y2 + 30
    shape2_line = page2.new_shape()
    shape2_line.draw_line(pymupdf.Point(350, y_totals), pymupdf.Point(542, y_totals))
    shape2_line.finish(color=(0.1, 0.2, 0.5), width=1)
    shape2_line.commit()

    totals = [
        ("Subtotal:", "$12,696.75"),
        ("Tax (0%):", "$0.00"),
        ("Shipping Credit:", "-$150.00"),
        ("Total Due:", "$12,546.75"),
    ]

    y_t = y_totals + 20
    for label, value in totals:
        bold = "hebo" if label == "Total Due:" else "helv"
        sz = 12 if label == "Total Due:" else 10
        page2.insert_text(pymupdf.Point(370, y_t), label, fontsize=sz, fontname=bold, color=(0, 0, 0))
        page2.insert_text(pymupdf.Point(480, y_t), value, fontsize=sz, fontname=bold, color=(0, 0, 0))
        y_t += 18

    # Payment terms
    y_terms = y_t + 40
    page2.insert_text(pymupdf.Point(72, y_terms), "Payment Terms & Conditions", fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.5))
    terms = [
        "1. Payment is due within 30 days of the invoice date.",
        "2. Late payments are subject to a 1.5% monthly finance charge.",
        "3. All disputes must be reported within 15 days of receipt.",
        "4. Returned checks incur a $35.00 processing fee.",
        "5. Wire transfer payments should reference invoice number INV-2025-03847.",
    ]
    y_tn = y_terms + 20
    for t in terms:
        page2.insert_text(pymupdf.Point(82, y_tn), t, fontsize=9, fontname="helv", color=(0, 0, 0))
        y_tn += 16

    page2.insert_text(pymupdf.Point(260, 760), "Page 2 of 3", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # ── Page 3: Payment instructions and notes ──
    page3 = doc.new_page(width=LETTER_W, height=LETTER_H)

    page3.insert_text(pymupdf.Point(72, 50), "Meridian Logistics Inc.", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.5))
    page3.insert_text(pymupdf.Point(72, 66), "Invoice #: INV-2025-03847 - Payment Information", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    shape3_line = page3.new_shape()
    shape3_line.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape3_line.finish(color=(0.1, 0.2, 0.5), width=1)
    shape3_line.commit()

    page3.insert_text(pymupdf.Point(72, 110), "Payment Methods", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.5))

    payment_info = [
        ("Bank Wire Transfer:", ""),
        ("  Bank Name:", "First National Commerce Bank"),
        ("  Account Name:", "Meridian Logistics Inc."),
        ("  Account Number:", "8847-2201-5563"),
        ("  Routing Number:", "021-000-089"),
        ("  SWIFT Code:", "FNCBUS33"),
        ("", ""),
        ("ACH Payment:", ""),
        ("  Same routing and account as above.", ""),
        ("", ""),
        ("Check Payment:", ""),
        ("  Make payable to: Meridian Logistics Inc.", ""),
        ("  Mail to: 1500 Commerce Blvd, Suite 400, Portland, OR 97201", ""),
    ]

    y3 = 140
    for label, value in payment_info:
        if not label and not value:
            y3 += 10
            continue
        if not value:
            page3.insert_text(pymupdf.Point(82, y3), label, fontsize=10, fontname="hebo", color=(0, 0, 0))
        else:
            page3.insert_text(pymupdf.Point(82, y3), label, fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
            page3.insert_text(pymupdf.Point(220, y3), value, fontsize=9, fontname="helv", color=(0, 0, 0))
        y3 += 16

    # Notes
    y_notes = y3 + 30
    page3.insert_text(pymupdf.Point(72, y_notes), "Notes", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.5))
    notes = [
        "Thank you for your continued business with Meridian Logistics.",
        "For questions regarding this invoice, please contact Marcus Johnson",
        "at (503) 555-8742 ext. 204 or marcus.johnson@meridianlogistics.com.",
        "",
        "Shipment tracking numbers:",
        "  MLI-TRK-20250301-A:  Portland -> Seattle (delivered 03/05)",
        "  MLI-TRK-20250303-B:  Portland -> San Francisco (delivered 03/08)",
        "  MLI-TRK-20250307-C:  Portland -> Seattle (delivered 03/10)",
        "  MLI-TRK-20250312-D:  Portland -> Seattle (delivered 03/14)",
    ]
    y_n = y_notes + 20
    for n in notes:
        if n == "":
            y_n += 8
            continue
        page3.insert_text(pymupdf.Point(82, y_n), n, fontsize=9, fontname="helv", color=(0, 0, 0))
        y_n += 15

    # Footer
    shape3_foot = page3.new_shape()
    shape3_foot.draw_line(pymupdf.Point(72, 720), pymupdf.Point(540, 720))
    shape3_foot.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape3_foot.commit()

    page3.insert_text(pymupdf.Point(160, 740), "Meridian Logistics Inc. - Delivering Excellence Since 2003", fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
    page3.insert_text(pymupdf.Point(260, 760), "Page 3 of 3", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
