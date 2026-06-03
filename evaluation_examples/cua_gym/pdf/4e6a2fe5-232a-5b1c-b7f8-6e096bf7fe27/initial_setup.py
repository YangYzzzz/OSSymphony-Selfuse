"""
Initial Setup: Create a 100-page batch invoice PDF
Task ID: pdf_gf3_013
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import random

WORKDIR = '/home/user'
INVOICES_DIR = f'{WORKDIR}/invoices'
OUTPUT = f'{INVOICES_DIR}/batch_invoices.pdf'


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
    import pymupdf

    os.makedirs(INVOICES_DIR, exist_ok=True)

    # Make sure split/ does NOT exist
    split_dir = os.path.join(INVOICES_DIR, 'split')
    if os.path.exists(split_dir):
        import shutil
        shutil.rmtree(split_dir)

    doc = pymupdf.open()

    # Company and product data for realistic invoices
    companies = [
        ("Apex Manufacturing Co.", "1200 Industrial Pkwy, Detroit, MI 48201"),
        ("BrightWave Solutions", "450 Innovation Dr, Austin, TX 78701"),
        ("Cascade Logistics LLC", "890 Harbor Blvd, Seattle, WA 98101"),
        ("Dynamo Electronics Inc.", "3300 Circuit Ave, San Jose, CA 95112"),
        ("EverGreen Supplies", "67 Maple St, Portland, OR 97201"),
        ("FrostByte Data Systems", "1100 Cloud Ln, Denver, CO 80202"),
        ("Granite Construction Group", "550 Quarry Rd, Phoenix, AZ 85004"),
        ("Horizon Medical Devices", "200 Health Park Dr, Boston, MA 02101"),
        ("IronClad Security Services", "78 Shield Ave, Chicago, IL 60601"),
        ("JetStream Aerospace", "4400 Runway Blvd, Wichita, KS 67202"),
    ]

    products = [
        ("Industrial Bearings (SKU-4521)", 45.00),
        ("Precision Gears Set (SKU-7832)", 120.50),
        ("Hydraulic Pump Assembly (SKU-1190)", 340.00),
        ("Stainless Steel Fasteners (SKU-2205)", 12.75),
        ("Electrical Wire Spool 500ft (SKU-6618)", 89.99),
        ("Thermal Insulation Panels (SKU-3347)", 210.00),
        ("LED Display Module (SKU-5500)", 175.00),
        ("Rubber Gasket Assortment (SKU-8891)", 34.50),
        ("Titanium Alloy Rods (SKU-9102)", 520.00),
        ("Carbon Fiber Sheets (SKU-4003)", 310.00),
        ("Copper Tubing 20ft (SKU-1156)", 67.25),
        ("Safety Valve Kit (SKU-7744)", 145.00),
        ("Pneumatic Cylinder (SKU-2089)", 198.50),
        ("Optical Sensor Array (SKU-6321)", 425.00),
        ("Welding Rod Bundle (SKU-3578)", 28.00),
    ]

    payment_terms = ["Net 30", "Net 45", "Net 60", "Due on Receipt", "2/10 Net 30"]

    random.seed(42)  # Reproducible

    for inv_idx in range(1, 51):
        inv_num = f"INV-2024-{inv_idx:03d}"
        company = companies[inv_idx % len(companies)]
        company_name, company_addr = company

        # Generate random invoice date in 2024
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        inv_date = f"2024-{month:02d}-{day:02d}"
        terms = random.choice(payment_terms)

        # Pick 3-7 line items
        num_items = random.randint(3, 7)
        items = random.sample(products, num_items)

        # ---- PAGE 1: Invoice header + line items ----
        page1 = doc.new_page(width=612, height=792)  # Letter size

        # Invoice header
        page1.insert_text(pymupdf.Point(72, 60), f"Invoice #{inv_num}",
                          fontsize=18, fontname="hebo", color=(0, 0, 0.5))

        page1.insert_text(pymupdf.Point(72, 85), f"Date: {inv_date}",
                          fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
        page1.insert_text(pymupdf.Point(72, 100), f"Payment Terms: {terms}",
                          fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))

        # Bill To
        page1.insert_text(pymupdf.Point(72, 135), "Bill To:",
                          fontsize=11, fontname="hebo", color=(0, 0, 0))
        page1.insert_text(pymupdf.Point(72, 150), company_name,
                          fontsize=10, fontname="helv", color=(0, 0, 0))
        page1.insert_text(pymupdf.Point(72, 165), company_addr,
                          fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

        # From header
        page1.insert_text(pymupdf.Point(350, 135), "From:",
                          fontsize=11, fontname="hebo", color=(0, 0, 0))
        page1.insert_text(pymupdf.Point(350, 150), "Universal Trade Corp.",
                          fontsize=10, fontname="helv", color=(0, 0, 0))
        page1.insert_text(pymupdf.Point(350, 165), "999 Commerce St, New York, NY 10001",
                          fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))

        # Horizontal rule
        shape = page1.new_shape()
        shape.draw_line(pymupdf.Point(72, 190), pymupdf.Point(540, 190))
        shape.finish(color=(0.6, 0.6, 0.6), width=1)
        shape.commit()

        # Table header
        y = 210
        page1.insert_text(pymupdf.Point(72, y), "Item", fontsize=10, fontname="hebo")
        page1.insert_text(pymupdf.Point(320, y), "Qty", fontsize=10, fontname="hebo")
        page1.insert_text(pymupdf.Point(380, y), "Unit Price", fontsize=10, fontname="hebo")
        page1.insert_text(pymupdf.Point(470, y), "Amount", fontsize=10, fontname="hebo")

        y += 5
        shape2 = page1.new_shape()
        shape2.draw_line(pymupdf.Point(72, y), pymupdf.Point(540, y))
        shape2.finish(color=(0.8, 0.8, 0.8), width=0.5)
        shape2.commit()

        y += 15
        subtotal = 0.0
        for item_name, unit_price in items:
            qty = random.randint(1, 25)
            amount = qty * unit_price
            subtotal += amount

            page1.insert_text(pymupdf.Point(72, y), item_name,
                              fontsize=9, fontname="helv", color=(0, 0, 0))
            page1.insert_text(pymupdf.Point(325, y), str(qty),
                              fontsize=9, fontname="helv", color=(0, 0, 0))
            page1.insert_text(pymupdf.Point(385, y), f"${unit_price:,.2f}",
                              fontsize=9, fontname="helv", color=(0, 0, 0))
            page1.insert_text(pymupdf.Point(475, y), f"${amount:,.2f}",
                              fontsize=9, fontname="helv", color=(0, 0, 0))
            y += 18

        # Totals
        y += 10
        shape3 = page1.new_shape()
        shape3.draw_line(pymupdf.Point(370, y), pymupdf.Point(540, y))
        shape3.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape3.commit()

        y += 15
        tax_rate = 0.08
        tax = subtotal * tax_rate
        total = subtotal + tax

        page1.insert_text(pymupdf.Point(380, y), "Subtotal:",
                          fontsize=10, fontname="helv")
        page1.insert_text(pymupdf.Point(475, y), f"${subtotal:,.2f}",
                          fontsize=10, fontname="helv")
        y += 18
        page1.insert_text(pymupdf.Point(380, y), "Tax (8%):",
                          fontsize=10, fontname="helv")
        page1.insert_text(pymupdf.Point(475, y), f"${tax:,.2f}",
                          fontsize=10, fontname="helv")
        y += 18
        page1.insert_text(pymupdf.Point(380, y), "TOTAL:",
                          fontsize=12, fontname="hebo", color=(0, 0, 0.5))
        page1.insert_text(pymupdf.Point(475, y), f"${total:,.2f}",
                          fontsize=12, fontname="hebo", color=(0, 0, 0.5))

        # Footer on page 1
        page1.insert_text(pymupdf.Point(72, 740),
                          f"Page 1 of 2  |  {inv_num}  |  Universal Trade Corp.",
                          fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))

        # ---- PAGE 2: Payment details and notes ----
        page2 = doc.new_page(width=612, height=792)

        page2.insert_text(pymupdf.Point(72, 60), f"Invoice #{inv_num} — Payment Details",
                          fontsize=14, fontname="hebo", color=(0, 0, 0.5))

        y = 100
        page2.insert_text(pymupdf.Point(72, y), "Payment Instructions:",
                          fontsize=11, fontname="hebo", color=(0, 0, 0))
        y += 20
        page2.insert_text(pymupdf.Point(72, y), "Bank: First National Bank of New York",
                          fontsize=10, fontname="helv")
        y += 16
        page2.insert_text(pymupdf.Point(72, y), "Account Name: Universal Trade Corp.",
                          fontsize=10, fontname="helv")
        y += 16
        page2.insert_text(pymupdf.Point(72, y), f"Routing: 021000089  |  Account: 1234-5678-{inv_idx:04d}",
                          fontsize=10, fontname="helv")
        y += 16
        page2.insert_text(pymupdf.Point(72, y), f"Reference: {inv_num}",
                          fontsize=10, fontname="helv")

        y += 40
        page2.insert_text(pymupdf.Point(72, y), "Terms and Conditions:",
                          fontsize=11, fontname="hebo", color=(0, 0, 0))
        y += 20
        terms_text = (
            "1. Payment is due according to the terms stated on page 1. "
            "Late payments will incur a 1.5% monthly finance charge. "
            "2. All goods remain the property of Universal Trade Corp. until paid in full. "
            "3. Claims must be made within 14 days of receipt. "
            "4. Returns require prior written authorization (RMA number). "
            "5. Shipping charges are non-refundable."
        )
        page2.insert_textbox(
            pymupdf.Rect(72, y, 540, y + 120),
            terms_text,
            fontsize=9,
            fontname="helv",
            color=(0.3, 0.3, 0.3),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        y += 140
        page2.insert_text(pymupdf.Point(72, y), "Notes:",
                          fontsize=11, fontname="hebo", color=(0, 0, 0))
        y += 20
        notes = [
            f"Order processed by warehouse team on {inv_date}.",
            f"Shipping via standard freight, estimated 5-7 business days.",
            f"Customer PO reference: PO-{company_name[:3].upper()}-{random.randint(1000,9999)}",
            "For questions, contact accounts@universaltrade.com or call (212) 555-0199.",
        ]
        for note in notes:
            page2.insert_text(pymupdf.Point(90, y), f"• {note}",
                              fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
            y += 16

        # Footer on page 2
        page2.insert_text(pymupdf.Point(72, 740),
                          f"Page 2 of 2  |  {inv_num}  |  Universal Trade Corp.",
                          fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT)
    doc.close()
    print(f"Initial file created: {OUTPUT}")
    print(f"Total pages: 100 (50 invoices x 2 pages each)")

    # Verify split/ does not exist
    if not os.path.exists(os.path.join(INVOICES_DIR, 'split')):
        print("Confirmed: /home/user/invoices/split/ does NOT exist")

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print("GUI_READY: launched evince with DISPLAY=:0")


create_initial()
