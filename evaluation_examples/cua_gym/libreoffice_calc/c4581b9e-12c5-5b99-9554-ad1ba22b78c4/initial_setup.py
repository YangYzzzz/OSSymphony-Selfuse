"""
Initial Setup: Multi-app workflow - PDF invoice extraction to Calc + Impress
Task ID: pdf_cross_142
Domain: libreoffice_calc
Creates: ~/Documents/invoices/ directory with 3 PDF invoices
  - vendor_a.pdf: 5 items, $3,200 total
  - vendor_b.pdf: 8 items, $5,750 total
  - vendor_c.pdf: 4 items, $2,100 total
MUST NOT create: Calc spreadsheet, Impress file, or exported PDF
"""

import os
import shlex
import subprocess
import time

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import black, grey, HexColor
from reportlab.lib.units import inch

WORKDIR = '/home/user'
INVOICES_DIR = f'{WORKDIR}/Documents/invoices'


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


def create_invoice_pdf(output_path, vendor_name, invoice_number, date, items):
    """
    Create a realistic vendor invoice PDF.
    items: list of (description, qty, unit_price) where qty * unit_price = amount
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    styles = getSampleStyleSheet()
    story = []

    # Header
    title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Title'],
        fontSize=22,
        textColor=HexColor("#1F3864"),
        spaceAfter=4,
    )
    info_style = ParagraphStyle(
        'InvoiceInfo',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor("#333333"),
        spaceAfter=2,
    )
    story.append(Paragraph("INVOICE", title_style))
    story.append(Paragraph(f"<b>Vendor:</b> {vendor_name}", info_style))
    story.append(Paragraph(f"<b>Invoice Number:</b> {invoice_number}", info_style))
    story.append(Paragraph(f"<b>Invoice Date:</b> {date}", info_style))
    story.append(Paragraph(f"<b>Bill To:</b> Acme Corp., 1500 Market St, San Francisco, CA 94105", info_style))
    story.append(Spacer(1, 0.2 * inch))

    # Line items table
    total = sum(qty * unit_price for (_, qty, unit_price) in items)
    table_data = [["#", "Description", "Qty", "Unit Price", "Amount"]]
    for i, (desc, qty, unit_price) in enumerate(items, 1):
        amount = qty * unit_price
        table_data.append([
            str(i),
            desc,
            str(qty),
            f"${unit_price:,.2f}",
            f"${amount:,.2f}",
        ])
    table_data.append(["", "", "", "Subtotal:", f"${total:,.2f}"])
    table_data.append(["", "", "", "Tax (0%):", "$0.00"])
    table_data.append(["", "", "", "TOTAL DUE:", f"${total:,.2f}"])

    col_widths = [0.4 * inch, 3.1 * inch, 0.6 * inch, 1.15 * inch, 1.15 * inch]
    table = Table(table_data, colWidths=col_widths)
    num_items = len(items)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1F3864")),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#FFFFFF")),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, num_items), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, num_items), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, num_items), [HexColor("#FFFFFF"), HexColor("#F0F4FA")]),
        ('ALIGN', (2, 1), (-1, num_items), 'RIGHT'),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('FONTNAME', (3, -3), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (3, -3), (-1, -1), 9),
        ('ALIGN', (3, -3), (-1, -1), 'RIGHT'),
        ('FONTNAME', (3, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (3, -1), (-1, -1), 10),
        ('BACKGROUND', (3, -1), (-1, -1), HexColor("#D6E4F0")),
        ('GRID', (0, 0), (-1, num_items), 0.5, grey),
        ('LINEABOVE', (0, -3), (-1, -3), 1, black),
        ('LINEBELOW', (0, -1), (-1, -1), 1, black),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.25 * inch))

    note_style = ParagraphStyle(
        'Note',
        parent=styles['Normal'],
        fontSize=9,
        textColor=HexColor("#666666"),
    )
    story.append(Paragraph("Payment Terms: Net 30. Please remit payment to the billing address above.", note_style))
    story.append(Paragraph("Thank you for your business!", note_style))

    doc.build(story)
    actual_total = sum(qty * unit_price for (_, qty, unit_price) in items)
    print(f"Created: {output_path}  (items={len(items)}, total=${actual_total:,.2f})")


def main():
    os.makedirs(INVOICES_DIR, exist_ok=True)

    # ---- Vendor A: TechSupplies Inc. — 5 items, $3,200 total ----
    # Verify: 4*85 + 2*485 + 6*45 + 1*820 + 8*100
    #       = 340 + 970 + 270 + 820 + 800 = 3,200 ✓
    vendor_a_items = [
        ("HP LaserJet Pro Toner Cartridge (Black, 4-pack)", 4, 85.00),
        ("Ergonomic Mesh Office Chair - Model EX200", 2, 485.00),
        ("USB-C Hub 7-Port (Anker PowerExpand)", 6, 45.00),
        ("27-inch IPS Monitor - ViewSonic VA2759-SMH", 1, 820.00),
        ("Wireless Keyboard & Mouse Combo (Logitech MK540)", 8, 100.00),
    ]
    create_invoice_pdf(
        f"{INVOICES_DIR}/vendor_a.pdf",
        vendor_name="TechSupplies Inc.",
        invoice_number="INV-2025-0471",
        date="March 10, 2025",
        items=vendor_a_items,
    )

    # ---- Vendor B: OfficeGear Solutions — 8 items, $5,750 total ----
    # Verify: 1*1200 + 10*55 + 5*150 + 3*180 + 2*320 + 12*45 + 10*65 + 5*176
    #       = 1200 + 550 + 750 + 540 + 640 + 540 + 650 + 880 = 5,750 ✓
    vendor_b_items = [
        ("Cloud Storage Enterprise Subscription (5TB, Annual)", 1, 1200.00),
        ("Adjustable Laptop Stand - Aluminum Alloy", 10, 55.00),
        ("External SSD 1TB - Samsung T7 Portable", 5, 150.00),
        ("Conference Room Webcam - Logitech C930e", 3, 180.00),
        ("Network Switch 24-Port Gigabit Managed", 2, 320.00),
        ("Surge Protector 8-Outlet 1080J", 12, 45.00),
        ("15.6\" Business Laptop Bag - Waterproof", 10, 65.00),
        ("Desk Cable Management Kit (50-piece Pro Set)", 5, 176.00),
    ]
    create_invoice_pdf(
        f"{INVOICES_DIR}/vendor_b.pdf",
        vendor_name="OfficeGear Solutions",
        invoice_number="INV-2025-0382",
        date="March 12, 2025",
        items=vendor_b_items,
    )

    # ---- Vendor C: OfficeSupply Direct — 4 items, $2,100 total ----
    # Verify: 3*195 + 15*45 + 8*42 + 1*504
    #       = 585 + 675 + 336 + 504 = 2,100 ✓
    vendor_c_items = [
        ("Magnetic Whiteboard 6ft x 4ft with Tray", 3, 195.00),
        ("Printer Paper A4 80gsm (Case of 10 reams)", 15, 45.00),
        ("Heavy-Duty Stapler + 5000 Staples Bundle", 8, 42.00),
        ("Steel 3-Drawer Filing Cabinet with Lock", 1, 504.00),
    ]
    create_invoice_pdf(
        f"{INVOICES_DIR}/vendor_c.pdf",
        vendor_name="OfficeSupply Direct",
        invoice_number="INV-2025-0519",
        date="March 15, 2025",
        items=vendor_c_items,
    )

    print(f"\nAll 3 invoices created in: {INVOICES_DIR}")
    print("Initial state complete (PDF invoices only — no Calc/Impress files).")

    # GUI-ready: open Nautilus showing invoices directory
    launch_gui(f'nautilus "{INVOICES_DIR}"', delay_sec=2.0)
    # Also open vendor_a.pdf in evince so the agent can read an invoice
    launch_gui(f'evince "{INVOICES_DIR}/vendor_a.pdf"', delay_sec=2.0)

    print("GUI_READY: launched Nautilus + Evince with DISPLAY=:0")


main()
