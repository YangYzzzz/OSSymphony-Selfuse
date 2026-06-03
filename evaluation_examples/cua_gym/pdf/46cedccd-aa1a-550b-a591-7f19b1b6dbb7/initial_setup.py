"""
Initial Setup: Create a scanned invoice PDF with no text layer
Task ID: pdf_mbc_074
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_074'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/scanned_invoice.pdf'


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

    # Step 1: Create a realistic-looking invoice as a rendered PDF using reportlab
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor, black, grey
    from reportlab.lib.units import inch
    import tempfile

    tmp_text_pdf = tempfile.mktemp(suffix='.pdf')
    width, height = letter
    c = canvas.Canvas(tmp_text_pdf, pagesize=letter)

    # Company header
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(HexColor("#1a3c6e"))
    c.drawString(72, height - 72, "Meridian Supply Co.")

    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor("#555555"))
    c.drawString(72, height - 92, "1247 Commerce Boulevard, Suite 300")
    c.drawString(72, height - 105, "Portland, OR 97205  |  Tel: (503) 555-0184  |  Fax: (503) 555-0185")

    # Invoice title
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(black)
    c.drawString(72, height - 155, "INVOICE")

    # Invoice details - right side
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(width - 72, height - 72, "Invoice Number:")
    c.drawRightString(width - 72, height - 90, "Invoice Date:")
    c.drawRightString(width - 72, height - 108, "Due Date:")
    c.drawRightString(width - 72, height - 126, "PO Number:")

    c.setFont("Helvetica", 11)
    c.drawRightString(width - 190, height - 72, "INV-2024-0847")
    c.drawRightString(width - 190, height - 90, "March 15, 2024")
    c.drawRightString(width - 190, height - 108, "April 14, 2024")
    c.drawRightString(width - 190, height - 126, "PO-78234")

    # Horizontal line
    c.setStrokeColor(HexColor("#1a3c6e"))
    c.setLineWidth(2)
    c.line(72, height - 170, width - 72, height - 170)

    # Bill To / Ship To
    y_addr = height - 200
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(HexColor("#1a3c6e"))
    c.drawString(72, y_addr, "Bill To:")
    c.drawString(320, y_addr, "Ship To:")

    c.setFont("Helvetica", 10)
    c.setFillColor(black)
    bill_to = [
        "Cascade Engineering Solutions",
        "Attn: Accounts Payable",
        "892 Industrial Park Drive",
        "Beaverton, OR 97006",
    ]
    ship_to = [
        "Cascade Engineering Solutions",
        "Warehouse B - Receiving Dock",
        "4510 NW Yeon Avenue",
        "Portland, OR 97210",
    ]
    for i, line in enumerate(bill_to):
        c.drawString(72, y_addr - 18 - (i * 15), line)
    for i, line in enumerate(ship_to):
        c.drawString(320, y_addr - 18 - (i * 15), line)

    # Table header
    table_top = height - 320
    c.setFillColor(HexColor("#1a3c6e"))
    c.rect(72, table_top - 5, width - 144, 22, fill=1, stroke=0)

    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(80, table_top, "Item #")
    c.drawString(140, table_top, "Description")
    c.drawString(360, table_top, "Qty")
    c.drawRightString(440, table_top, "Unit Price")
    c.drawRightString(width - 80, table_top, "Amount")

    # Table rows
    items = [
        ("MSC-4421", "Stainless Steel Hex Bolts 3/8\"-16 x 2\"", "250", "$0.42", "$105.00"),
        ("MSC-4422", "Stainless Steel Hex Nuts 3/8\"-16", "250", "$0.18", "$45.00"),
        ("MSC-7103", "Flat Washers SS 3/8\" (SAE)", "500", "$0.08", "$40.00"),
        ("MSC-2250", "Lock Washers SS 3/8\" Split", "250", "$0.12", "$30.00"),
        ("MSC-8815", "Socket Head Cap Screws M10x40mm", "100", "$1.25", "$125.00"),
        ("MSC-8816", "Socket Head Cap Screws M10x60mm", "75", "$1.65", "$123.75"),
        ("MSC-3340", "Thread Sealant Tape 1/2\" x 520\"", "12", "$3.50", "$42.00"),
        ("MSC-5567", "Cutting Fluid 1-Gallon Concentrate", "4", "$28.95", "$115.80"),
        ("MSC-6012", "Carbide End Mill 1/2\" 4-Flute", "6", "$34.50", "$207.00"),
        ("MSC-6019", "Carbide End Mill 3/4\" 4-Flute", "3", "$52.75", "$158.25"),
    ]

    c.setFillColor(black)
    c.setFont("Helvetica", 10)
    y = table_top - 25
    for i, (item_no, desc, qty, unit, amount) in enumerate(items):
        if i % 2 == 0:
            c.setFillColor(HexColor("#f0f4f8"))
            c.rect(72, y - 5, width - 144, 18, fill=1, stroke=0)
        c.setFillColor(black)
        c.drawString(80, y, item_no)
        c.drawString(140, y, desc)
        c.drawString(368, y, qty)
        c.drawRightString(440, y, unit)
        c.drawRightString(width - 80, y, amount)
        y -= 20

    # Bottom line under table
    c.setStrokeColor(HexColor("#1a3c6e"))
    c.setLineWidth(1)
    c.line(72, y + 5, width - 72, y + 5)

    # Totals
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawRightString(440, y, "Subtotal:")
    c.drawRightString(width - 80, y, "$991.80")

    y -= 18
    c.drawRightString(440, y, "Shipping & Handling:")
    c.drawRightString(width - 80, y, "$45.00")

    y -= 18
    c.drawRightString(440, y, "Tax (6.5%):")
    c.drawRightString(width - 80, y, "$64.47")

    y -= 22
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(HexColor("#1a3c6e"))
    c.drawRightString(440, y, "TOTAL DUE:")
    c.drawRightString(width - 80, y, "$1,101.27")

    # Payment terms
    y -= 50
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(black)
    c.drawString(72, y, "Payment Terms:")
    c.setFont("Helvetica", 10)
    c.drawString(170, y, "Net 30 Days")

    y -= 18
    c.setFont("Helvetica-Bold", 10)
    c.drawString(72, y, "Payment Methods:")
    c.setFont("Helvetica", 10)
    c.drawString(180, y, "Check, Wire Transfer, or ACH")

    y -= 18
    c.setFont("Helvetica-Bold", 10)
    c.drawString(72, y, "Wire Transfer Info:")
    c.setFont("Helvetica", 10)
    c.drawString(180, y, "First National Bank  |  Routing: 071000013  |  Acct: 3847291056")

    # Footer
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(grey)
    c.drawCentredString(width / 2, 50, "Thank you for your business! Please reference invoice number on all payments.")
    c.drawCentredString(width / 2, 38, "Questions? Contact billing@meridiansupply.com or call (503) 555-0184 ext 202")

    c.showPage()
    c.save()

    # Step 2: Render the text PDF to an image, then embed image into a new PDF
    # This simulates a "scanned" document - image only, no text layer
    import pymupdf

    text_doc = pymupdf.open(tmp_text_pdf)
    page = text_doc[0]
    # Render at 200 DPI for realistic scan quality
    mat = pymupdf.Matrix(200 / 72, 200 / 72)
    pix = page.get_pixmap(matrix=mat)

    # Add slight scan artifacts: save as JPEG to introduce compression artifacts
    import io
    from PIL import Image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Slight off-white tint to simulate scan
    import numpy as np
    arr = np.array(img, dtype=np.float32)
    # Add very subtle yellowish tint to whites
    mask = arr.mean(axis=2) > 240
    arr[mask] = arr[mask] * 0.98 + np.array([2, 1, 0], dtype=np.float32)
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr)

    # Save as JPEG (lossy) to simulate scanner output
    jpeg_buffer = io.BytesIO()
    img.save(jpeg_buffer, format='JPEG', quality=88)
    jpeg_bytes = jpeg_buffer.getvalue()

    text_doc.close()

    # Step 3: Create final scanned PDF - image only, no text layer
    scan_doc = pymupdf.open()
    scan_page = scan_doc.new_page(width=612, height=792)  # letter size
    img_rect = pymupdf.Rect(0, 0, 612, 792)
    scan_page.insert_image(img_rect, stream=jpeg_bytes)

    scan_doc.save(OUTPUT)
    scan_doc.close()

    # Clean up temp file
    os.unlink(tmp_text_pdf)

    # Verify no text layer exists
    verify_doc = pymupdf.open(OUTPUT)
    text = verify_doc[0].get_text("text").strip()
    verify_doc.close()
    if text:
        print(f"WARNING: Text layer detected in scanned PDF: {text[:100]}")
    else:
        print("VERIFIED: No text layer in scanned PDF (image-only)")

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup - open PDF in evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
