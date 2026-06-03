"""
Initial Setup: Create 6 invoice PDFs in /home/user/Documents/invoices/ and an empty invoices_paid/ directory.
Task ID: pdf_gf1_031
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_031'
INVOICES_DIR = f'{WORKDIR}/Documents/invoices'
PAID_DIR = f'{WORKDIR}/Documents/invoices_paid'


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


# Invoice data for 6 invoices with varying page counts and content
INVOICES = [
    {
        "filename": "invoice_001.pdf",
        "pages": 1,
        "company": "Meridian Technologies LLC",
        "invoice_num": "INV-2025-0417",
        "date": "March 12, 2025",
        "due_date": "April 11, 2025",
        "client": "Apex Manufacturing Corp",
        "client_addr": "1420 Industrial Blvd, Suite 300\nDetroit, MI 48201",
        "items": [
            ("Cloud Infrastructure Setup", 1, 4500.00),
            ("Database Migration Service", 1, 3200.00),
            ("Security Audit (40 hrs @ $175/hr)", 40, 175.00),
            ("SSL Certificate (Annual)", 2, 149.99),
        ],
    },
    {
        "filename": "invoice_002.pdf",
        "pages": 2,
        "company": "Greenfield Consulting Group",
        "invoice_num": "GCG-8823",
        "date": "February 28, 2025",
        "due_date": "March 30, 2025",
        "client": "Riverside Community Hospital",
        "client_addr": "890 Healthcare Drive\nPortland, OR 97201",
        "items": [
            ("Strategic Planning Workshop (3 days)", 3, 2800.00),
            ("Market Analysis Report", 1, 5500.00),
            ("Stakeholder Interviews (12 sessions)", 12, 450.00),
            ("Competitive Landscape Assessment", 1, 3750.00),
            ("Executive Summary Presentation", 1, 1200.00),
            ("Follow-up Consultation (8 hrs)", 8, 325.00),
            ("Travel Expenses - Portland", 1, 1842.50),
        ],
    },
    {
        "filename": "invoice_003.pdf",
        "pages": 1,
        "company": "Stellar Design Studio",
        "invoice_num": "SDS-2025-0091",
        "date": "March 5, 2025",
        "due_date": "April 4, 2025",
        "client": "NovaBrew Coffee Roasters",
        "client_addr": "234 Artisan Way\nAustin, TX 78701",
        "items": [
            ("Brand Identity Package", 1, 8500.00),
            ("Logo Design (3 concepts)", 1, 2500.00),
            ("Business Card Design", 1, 350.00),
            ("Letterhead & Envelope Design", 1, 450.00),
            ("Social Media Kit (5 templates)", 5, 180.00),
        ],
    },
    {
        "filename": "invoice_004.pdf",
        "pages": 2,
        "company": "Precision Engineering Solutions",
        "invoice_num": "PES-44291",
        "date": "January 15, 2025",
        "due_date": "February 14, 2025",
        "client": "Titan Aerospace Industries",
        "client_addr": "7700 Skypark Drive, Bldg C\nHuntsville, AL 35802",
        "items": [
            ("Structural Analysis - Wing Assembly", 1, 12500.00),
            ("FEA Simulation (48 compute hours)", 48, 95.00),
            ("Material Testing - Composite Panels", 6, 780.00),
            ("Technical Documentation Package", 1, 3200.00),
            ("Quality Assurance Review", 1, 2100.00),
            ("Prototype Fabrication Support", 1, 6800.00),
            ("On-site Consultation (3 days)", 3, 1950.00),
            ("Revision Cycle (2 iterations)", 2, 1500.00),
        ],
    },
    {
        "filename": "invoice_005.pdf",
        "pages": 1,
        "company": "Harmony Event Planning",
        "invoice_num": "HEP-2025-0233",
        "date": "March 20, 2025",
        "due_date": "April 19, 2025",
        "client": "Lakewood Country Club",
        "client_addr": "15 Fairway Lane\nScottsdale, AZ 85251",
        "items": [
            ("Annual Gala Event Coordination", 1, 7500.00),
            ("Venue Decoration Package", 1, 3200.00),
            ("Catering Management Fee", 1, 1800.00),
            ("Entertainment Booking", 1, 2500.00),
            ("Photography Coverage (6 hrs)", 6, 275.00),
        ],
    },
    {
        "filename": "invoice_006.pdf",
        "pages": 2,
        "company": "DataVault Analytics Inc.",
        "invoice_num": "DVA-10582",
        "date": "February 10, 2025",
        "due_date": "March 12, 2025",
        "client": "Pacific Northwest Credit Union",
        "client_addr": "4500 Commerce Street, Floor 8\nSeattle, WA 98101",
        "items": [
            ("Customer Segmentation Analysis", 1, 9200.00),
            ("Predictive Model Development", 1, 14500.00),
            ("Dashboard Design & Implementation", 1, 6300.00),
            ("Data Pipeline Architecture", 1, 8100.00),
            ("Staff Training (2-day workshop)", 2, 3500.00),
            ("Monthly Maintenance Contract (Q1)", 3, 2200.00),
            ("API Integration Module", 1, 4800.00),
            ("Documentation & Knowledge Transfer", 1, 2750.00),
        ],
    },
]


def create_invoice_page(page, inv, items_for_page, page_num, total_pages, subtotal=None, tax=None, total=None):
    """Render invoice content onto a PDF page."""
    width = page.rect.width
    height = page.rect.height

    # Company header
    page.insert_text(pymupdf.Point(72, 60), inv["company"], fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 80), "Professional Services", fontsize=10, fontname="heit", color=(0.4, 0.4, 0.4))

    # INVOICE label
    page.insert_text(pymupdf.Point(400, 60), "INVOICE", fontsize=22, fontname="hebo", color=(0.15, 0.15, 0.15))

    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(width - 72, 95))
    shape.finish(color=(0.7, 0.7, 0.7), width=1.5)
    shape.commit()

    # Invoice details
    page.insert_text(pymupdf.Point(72, 120), f"Invoice #: {inv['invoice_num']}", fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 135), f"Date: {inv['date']}", fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 150), f"Due Date: {inv['due_date']}", fontsize=10, fontname="helv", color=(0, 0, 0))

    # Bill To
    page.insert_text(pymupdf.Point(350, 120), "Bill To:", fontsize=10, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(350, 135), inv["client"], fontsize=10, fontname="helv", color=(0, 0, 0))
    y_addr = 150
    for line in inv["client_addr"].split("\n"):
        page.insert_text(pymupdf.Point(350, y_addr), line, fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
        y_addr += 13

    # Table header
    table_top = 200
    headers = ["Description", "Qty", "Unit Price", "Amount"]
    col_x = [72, 330, 400, 480]

    # Header background
    shape2 = page.new_shape()
    shape2.draw_rect(pymupdf.Rect(72, table_top - 5, width - 72, table_top + 15))
    shape2.finish(fill=(0.15, 0.15, 0.4), color=(0.15, 0.15, 0.4))
    shape2.commit()

    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(col_x[i], table_top + 10), h, fontsize=9, fontname="hebo", color=(1, 1, 1))

    # Table rows
    y = table_top + 30
    for desc, qty, unit_price in items_for_page:
        amount = qty * unit_price
        page.insert_text(pymupdf.Point(col_x[0], y), desc, fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(col_x[1], y), str(qty), fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(col_x[2], y), f"${unit_price:,.2f}", fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(col_x[3], y), f"${amount:,.2f}", fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 20

        # Light row separator
        shape3 = page.new_shape()
        shape3.draw_line(pymupdf.Point(72, y - 7), pymupdf.Point(width - 72, y - 7))
        shape3.finish(color=(0.85, 0.85, 0.85), width=0.5)
        shape3.commit()

    # Show totals only on last page
    if subtotal is not None:
        y += 15
        shape4 = page.new_shape()
        shape4.draw_line(pymupdf.Point(400, y - 5), pymupdf.Point(width - 72, y - 5))
        shape4.finish(color=(0, 0, 0), width=1)
        shape4.commit()

        page.insert_text(pymupdf.Point(400, y + 10), "Subtotal:", fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(480, y + 10), f"${subtotal:,.2f}", fontsize=10, fontname="helv", color=(0, 0, 0))

        page.insert_text(pymupdf.Point(400, y + 28), f"Tax (8.5%):", fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(480, y + 28), f"${tax:,.2f}", fontsize=10, fontname="helv", color=(0, 0, 0))

        shape5 = page.new_shape()
        shape5.draw_line(pymupdf.Point(400, y + 35), pymupdf.Point(width - 72, y + 35))
        shape5.finish(color=(0, 0, 0), width=1.5)
        shape5.commit()

        page.insert_text(pymupdf.Point(400, y + 52), "Total Due:", fontsize=12, fontname="hebo", color=(0.1, 0.1, 0.4))
        page.insert_text(pymupdf.Point(480, y + 52), f"${total:,.2f}", fontsize=12, fontname="hebo", color=(0.1, 0.1, 0.4))

    # Footer
    if total_pages > 1:
        page.insert_text(pymupdf.Point(72, height - 50),
                         f"Page {page_num} of {total_pages}",
                         fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Terms at bottom of last page
    if page_num == total_pages and subtotal is not None:
        terms_y = height - 90
        page.insert_text(pymupdf.Point(72, terms_y), "Payment Terms:", fontsize=8, fontname="hebo", color=(0.3, 0.3, 0.3))
        page.insert_text(pymupdf.Point(72, terms_y + 13), "Net 30 days. Late payments subject to 1.5% monthly interest.", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))
        page.insert_text(pymupdf.Point(72, terms_y + 26), "Please include invoice number with your payment.", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))


def create_invoice(inv, filepath):
    """Create a single invoice PDF."""
    doc = pymupdf.open()
    total_pages = inv["pages"]
    items = inv["items"]

    if total_pages == 1:
        page = doc.new_page(width=612, height=792)  # Letter size
        subtotal = sum(qty * price for _, qty, price in items)
        tax = round(subtotal * 0.085, 2)
        total = round(subtotal + tax, 2)
        create_invoice_page(page, inv, items, 1, 1, subtotal, tax, total)
    else:
        # Split items across pages
        mid = len(items) // 2
        items_p1 = items[:mid]
        items_p2 = items[mid:]

        # Page 1 - first half of items, no totals
        page1 = doc.new_page(width=612, height=792)
        create_invoice_page(page1, inv, items_p1, 1, 2)

        # Page 2 - second half of items with totals
        page2 = doc.new_page(width=612, height=792)
        subtotal = sum(qty * price for _, qty, price in items)
        tax = round(subtotal * 0.085, 2)
        total = round(subtotal + tax, 2)
        create_invoice_page(page2, inv, items_p2, 2, 2, subtotal, tax, total)

    doc.save(filepath)
    doc.close()
    print(f"Created: {filepath} ({total_pages} page(s))")


def create_initial():
    # Create directories
    os.makedirs(INVOICES_DIR, exist_ok=True)
    os.makedirs(PAID_DIR, exist_ok=True)

    # Create all 6 invoices
    for inv in INVOICES:
        filepath = os.path.join(INVOICES_DIR, inv["filename"])
        create_invoice(inv, filepath)

    print(f"\nAll invoices created in {INVOICES_DIR}")
    print(f"Empty paid directory ready at {PAID_DIR}")

    # Open file manager to show invoices directory
    launch_gui(f'nautilus "{INVOICES_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched Nautilus with DISPLAY=:0")


create_initial()
