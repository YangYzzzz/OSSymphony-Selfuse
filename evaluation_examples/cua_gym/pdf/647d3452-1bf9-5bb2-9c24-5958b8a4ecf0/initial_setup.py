"""
Initial Setup: Create a multi-page PDF with several invoices concatenated together.
Task ID: pdf_cr_063
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_063'
OUTPUT = f'{WORKDIR}/Desktop/invoice_batch.pdf'

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
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    doc = pymupdf.open()

    # Define invoices with realistic data
    invoices = [
        {
            "number": "1047",
            "date": "2025-01-15",
            "company": "Meridian Software Solutions",
            "address": "4521 Innovation Drive, Suite 300\nSan Jose, CA 95134",
            "bill_to": "Greenfield Manufacturing Inc.\n892 Industrial Blvd\nPortland, OR 97201",
            "items": [
                ("Enterprise License - Annual", 1, 12500.00),
                ("Implementation Services", 40, 175.00),
                ("Data Migration Package", 1, 3200.00),
                ("Staff Training (on-site, 3 days)", 1, 4500.00),
            ],
            "tax_rate": 0.0825,
        },
        {
            "number": "1048",
            "date": "2025-01-22",
            "company": "Meridian Software Solutions",
            "address": "4521 Innovation Drive, Suite 300\nSan Jose, CA 95134",
            "bill_to": "Coastal Healthcare Partners\n1200 Bayshore Avenue\nMiami, FL 33131",
            "items": [
                ("Cloud Hosting - Monthly (Premium)", 12, 899.00),
                ("API Integration Module", 1, 5600.00),
                ("24/7 Priority Support - Annual", 1, 8400.00),
                ("Security Audit & Compliance Review", 1, 6750.00),
            ],
            "tax_rate": 0.07,
        },
        {
            "number": "1053",
            "date": "2025-02-03",
            "company": "Meridian Software Solutions",
            "address": "4521 Innovation Drive, Suite 300\nSan Jose, CA 95134",
            "bill_to": "Summit Financial Advisors LLC\n3300 Tower Plaza, Floor 18\nChicago, IL 60601",
            "items": [
                ("Custom Dashboard Development", 80, 195.00),
                ("Database Optimization", 1, 4200.00),
                ("Quarterly Maintenance Contract", 4, 2100.00),
                ("SSL Certificate - Wildcard (2yr)", 1, 450.00),
                ("Backup & Disaster Recovery Setup", 1, 3800.00),
            ],
            "tax_rate": 0.0625,
        },
        {
            "number": "1061",
            "date": "2025-02-18",
            "company": "Meridian Software Solutions",
            "address": "4521 Innovation Drive, Suite 300\nSan Jose, CA 95134",
            "bill_to": "Redwood Logistics Corp.\n7744 Commerce Way\nDallas, TX 75201",
            "items": [
                ("Fleet Management Module", 1, 18500.00),
                ("GPS Integration Service", 1, 7200.00),
                ("Mobile App Deployment (iOS + Android)", 1, 12000.00),
                ("User Acceptance Testing", 30, 150.00),
            ],
            "tax_rate": 0.0825,
        },
        {
            "number": "1072",
            "date": "2025-03-05",
            "company": "Meridian Software Solutions",
            "address": "4521 Innovation Drive, Suite 300\nSan Jose, CA 95134",
            "bill_to": "Evergreen Education Foundation\n560 Campus Circle\nBoston, MA 02108",
            "items": [
                ("Learning Management System License", 1, 9800.00),
                ("Content Authoring Tools", 5, 1200.00),
                ("Student Portal Customization", 60, 185.00),
                ("Video Streaming Integration", 1, 5500.00),
                ("Annual Hosting & Maintenance", 1, 6200.00),
            ],
            "tax_rate": 0.0625,
        },
    ]

    for inv in invoices:
        page = doc.new_page(width=612, height=792)  # Letter size

        y = 50  # current y position

        # Company header
        page.insert_text(pymupdf.Point(72, y), inv["company"],
                         fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
        y += 18
        for addr_line in inv["address"].split("\n"):
            page.insert_text(pymupdf.Point(72, y), addr_line,
                             fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
            y += 12

        # Invoice header
        y += 20
        page.insert_text(pymupdf.Point(72, y), f"Invoice #{inv['number']}",
                         fontsize=22, fontname="hebo", color=(0, 0, 0))

        page.insert_text(pymupdf.Point(400, y), f"Date: {inv['date']}",
                         fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))

        # Horizontal rule
        y += 15
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(540, y))
        shape.finish(color=(0.6, 0.6, 0.6), width=1)
        shape.commit()

        # Bill To
        y += 20
        page.insert_text(pymupdf.Point(72, y), "Bill To:",
                         fontsize=10, fontname="hebo", color=(0.3, 0.3, 0.3))
        y += 14
        for bt_line in inv["bill_to"].split("\n"):
            page.insert_text(pymupdf.Point(72, y), bt_line,
                             fontsize=10, fontname="helv", color=(0, 0, 0))
            y += 13

        # Table header
        y += 25
        cols = [72, 300, 370, 440, 510]  # Description, Qty, Unit Price, Amount
        headers = ["Description", "Qty", "Unit Price", "Amount"]

        # Header background
        shape2 = page.new_shape()
        shape2.draw_rect(pymupdf.Rect(70, y - 12, 542, y + 4))
        shape2.finish(fill=(0.15, 0.15, 0.4), color=(0.15, 0.15, 0.4))
        shape2.commit()

        for i, hdr in enumerate(headers):
            page.insert_text(pymupdf.Point(cols[i], y), hdr,
                             fontsize=10, fontname="hebo", color=(1, 1, 1))
        y += 18

        # Line items
        subtotal = 0.0
        for desc, qty, unit_price in inv["items"]:
            amount = qty * unit_price
            subtotal += amount
            page.insert_text(pymupdf.Point(cols[0], y), desc,
                             fontsize=10, fontname="helv", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(cols[1], y), str(qty),
                             fontsize=10, fontname="helv", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(cols[2], y), f"${unit_price:,.2f}",
                             fontsize=10, fontname="helv", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(cols[3], y), f"${amount:,.2f}",
                             fontsize=10, fontname="helv", color=(0, 0, 0))
            y += 16

        # Subtotal, Tax, Total
        y += 10
        shape3 = page.new_shape()
        shape3.draw_line(pymupdf.Point(400, y), pymupdf.Point(540, y))
        shape3.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape3.commit()

        y += 15
        tax = subtotal * inv["tax_rate"]
        total = subtotal + tax

        page.insert_text(pymupdf.Point(400, y), "Subtotal:",
                         fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
        page.insert_text(pymupdf.Point(480, y), f"${subtotal:,.2f}",
                         fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 15

        page.insert_text(pymupdf.Point(400, y), f"Tax ({inv['tax_rate']*100:.2f}%):",
                         fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
        page.insert_text(pymupdf.Point(480, y), f"${tax:,.2f}",
                         fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 15

        shape4 = page.new_shape()
        shape4.draw_line(pymupdf.Point(400, y), pymupdf.Point(540, y))
        shape4.finish(color=(0, 0, 0), width=1)
        shape4.commit()

        y += 15
        page.insert_text(pymupdf.Point(400, y), "Total:",
                         fontsize=13, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(480, y), f"${total:,.2f}",
                         fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.4))

        # Footer
        page.insert_text(pymupdf.Point(72, 750),
                         "Payment Terms: Net 30 | Thank you for your business!",
                         fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify content
    doc2 = pymupdf.open(OUTPUT)
    print(f'Pages: {doc2.page_count}')
    for i in range(doc2.page_count):
        text = doc2[i].get_text("text")
        # Find invoice number
        for line in text.split('\n'):
            if 'Invoice #' in line:
                print(f'  Page {i+1}: {line.strip()}')
            if line.strip().startswith('Total:'):
                # This is the label; the amount is nearby
                pass
    doc2.close()

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
