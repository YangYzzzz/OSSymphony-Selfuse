"""
Initial Setup: Create scanned invoice PDF (images only, no selectable text)
Task ID: pdf_gf1_010
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import io

WORKDIR = '/home/user'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/scanned_invoice.pdf'


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


def create_invoice_page_image(page_num):
    """Create a realistic invoice page as a PIL Image (no selectable text)."""
    from PIL import Image, ImageDraw, ImageFont

    # Create white page image at 150 DPI (letter size: 8.5x11 inches)
    width, height = 1275, 1650  # 8.5*150, 11*150
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    # Try to use a decent font, fall back to default
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except (OSError, IOError):
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 28)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 20)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 16)
            font_bold = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 16)
        except (OSError, IOError):
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_bold = ImageFont.load_default()

    if page_num == 1:
        # === PAGE 1: Invoice Header and Bill-To ===
        y = 80

        # Company name / logo area
        draw.text((100, y), "PINNACLE SUPPLY CO.", fill='black', font=font_large)
        y += 45
        draw.text((100, y), "1250 Commerce Boulevard, Suite 400", fill='gray', font=font_small)
        y += 25
        draw.text((100, y), "San Francisco, CA 94107", fill='gray', font=font_small)
        y += 25
        draw.text((100, y), "Phone: (415) 555-0198  |  Fax: (415) 555-0199", fill='gray', font=font_small)
        y += 25
        draw.text((100, y), "Email: billing@pinnaclesupply.com", fill='gray', font=font_small)

        # Horizontal line
        y += 40
        draw.line([(80, y), (width - 80, y)], fill='black', width=2)

        # INVOICE title
        y += 30
        draw.text((width // 2 - 60, y), "INVOICE", fill='black', font=font_large)

        # Invoice details (right side)
        y += 60
        draw.text((100, y), "Invoice Number:", fill='black', font=font_bold)
        draw.text((320, y), "INV-2024-00847", fill='black', font=font_small)
        y += 30
        draw.text((100, y), "Invoice Date:", fill='black', font=font_bold)
        draw.text((320, y), "March 15, 2024", fill='black', font=font_small)
        y += 30
        draw.text((100, y), "Due Date:", fill='black', font=font_bold)
        draw.text((320, y), "April 14, 2024", fill='black', font=font_small)
        y += 30
        draw.text((100, y), "Payment Terms:", fill='black', font=font_bold)
        draw.text((320, y), "Net 30", fill='black', font=font_small)

        # Another line
        y += 50
        draw.line([(80, y), (width - 80, y)], fill='gray', width=1)

        # Bill To / Ship To
        y += 30
        draw.text((100, y), "BILL TO:", fill='black', font=font_bold)
        draw.text((650, y), "SHIP TO:", fill='black', font=font_bold)
        y += 30
        draw.text((100, y), "Meridian Technologies Inc.", fill='black', font=font_small)
        draw.text((650, y), "Meridian Technologies Inc.", fill='black', font=font_small)
        y += 25
        draw.text((100, y), "Attn: Accounts Payable", fill='black', font=font_small)
        draw.text((650, y), "Attn: Warehouse Receiving", fill='black', font=font_small)
        y += 25
        draw.text((100, y), "742 Innovation Drive", fill='black', font=font_small)
        draw.text((650, y), "742 Innovation Drive", fill='black', font=font_small)
        y += 25
        draw.text((100, y), "Austin, TX 78701", fill='black', font=font_small)
        draw.text((650, y), "Austin, TX 78701", fill='black', font=font_small)
        y += 25
        draw.text((100, y), "Contact: Diana Reeves", fill='black', font=font_small)
        draw.text((650, y), "Contact: Marcus Chen", fill='black', font=font_small)

        # Purchase Order reference
        y += 50
        draw.line([(80, y), (width - 80, y)], fill='gray', width=1)
        y += 20
        draw.text((100, y), "Purchase Order:", fill='black', font=font_bold)
        draw.text((320, y), "PO-2024-3391", fill='black', font=font_small)
        y += 30
        draw.text((100, y), "Sales Rep:", fill='black', font=font_bold)
        draw.text((320, y), "Jonathan Park", fill='black', font=font_small)

        # Start of items table header
        y += 60
        draw.line([(80, y), (width - 80, y)], fill='black', width=2)
        y += 10
        draw.text((100, y), "Item", fill='black', font=font_bold)
        draw.text((420, y), "Description", fill='black', font=font_bold)
        draw.text((820, y), "Qty", fill='black', font=font_bold)
        draw.text((920, y), "Unit Price", fill='black', font=font_bold)
        draw.text((1080, y), "Amount", fill='black', font=font_bold)
        y += 30
        draw.line([(80, y), (width - 80, y)], fill='black', width=1)

        # First few line items on page 1
        items_p1 = [
            ("WH-5520", "Wireless Headset Pro X", "10", "$129.99", "$1,299.90"),
            ("KB-3310", "Mechanical Keyboard RGB", "15", "$89.50", "$1,342.50"),
            ("MN-2740", "27-inch 4K Monitor", "5", "$449.00", "$2,245.00"),
            ("DC-1180", "USB-C Docking Station", "8", "$175.00", "$1,400.00"),
            ("MS-4450", "Ergonomic Mouse Deluxe", "20", "$59.95", "$1,199.00"),
        ]

        for item in items_p1:
            y += 30
            draw.text((100, y), item[0], fill='black', font=font_small)
            draw.text((420, y), item[1], fill='black', font=font_small)
            draw.text((835, y), item[2], fill='black', font=font_small)
            draw.text((920, y), item[3], fill='black', font=font_small)
            draw.text((1080, y), item[4], fill='black', font=font_small)

        y += 40
        draw.line([(80, y), (width - 80, y)], fill='gray', width=1)

        # Footer note
        y += 30
        draw.text((100, y), "Continued on Page 2...", fill='gray', font=font_small)

        # Page number
        draw.text((width // 2 - 30, height - 60), "Page 1 of 2", fill='gray', font=font_small)

    elif page_num == 2:
        # === PAGE 2: Remaining items, totals, terms ===
        y = 80
        draw.text((100, y), "PINNACLE SUPPLY CO.", fill='black', font=font_large)
        y += 45
        draw.text((100, y), "Invoice INV-2024-00847 (continued)", fill='gray', font=font_medium)

        y += 50
        draw.line([(80, y), (width - 80, y)], fill='black', width=2)
        y += 10
        draw.text((100, y), "Item", fill='black', font=font_bold)
        draw.text((420, y), "Description", fill='black', font=font_bold)
        draw.text((820, y), "Qty", fill='black', font=font_bold)
        draw.text((920, y), "Unit Price", fill='black', font=font_bold)
        draw.text((1080, y), "Amount", fill='black', font=font_bold)
        y += 30
        draw.line([(80, y), (width - 80, y)], fill='black', width=1)

        items_p2 = [
            ("WC-8890", "1080p Webcam HD", "12", "$74.99", "$899.88"),
            ("SP-6670", "Desktop Speakers 2.1", "6", "$119.00", "$714.00"),
            ("LP-2200", "Laptop Stand Aluminum", "10", "$45.50", "$455.00"),
            ("CB-3340", "USB-C Cable 6ft (10pk)", "4", "$39.99", "$159.96"),
            ("PP-1150", "Surge Protector 12-Outlet", "8", "$34.95", "$279.60"),
        ]

        for item in items_p2:
            y += 30
            draw.text((100, y), item[0], fill='black', font=font_small)
            draw.text((420, y), item[1], fill='black', font=font_small)
            draw.text((835, y), item[2], fill='black', font=font_small)
            draw.text((920, y), item[3], fill='black', font=font_small)
            draw.text((1080, y), item[4], fill='black', font=font_small)

        # Totals section
        y += 60
        draw.line([(750, y), (width - 80, y)], fill='black', width=2)
        y += 15
        draw.text((780, y), "Subtotal:", fill='black', font=font_bold)
        draw.text((1060, y), "$9,994.84", fill='black', font=font_small)
        y += 30
        draw.text((780, y), "Shipping:", fill='black', font=font_bold)
        draw.text((1060, y), "$285.00", fill='black', font=font_small)
        y += 30
        draw.text((780, y), "Tax (8.25%):", fill='black', font=font_bold)
        draw.text((1060, y), "$824.57", fill='black', font=font_small)
        y += 35
        draw.line([(750, y), (width - 80, y)], fill='black', width=2)
        y += 15
        draw.text((780, y), "TOTAL DUE:", fill='black', font=font_large)
        draw.text((1040, y), "$11,104.41", fill='black', font=font_medium)

        # Payment instructions
        y += 80
        draw.line([(80, y), (width - 80, y)], fill='gray', width=1)
        y += 20
        draw.text((100, y), "PAYMENT INSTRUCTIONS:", fill='black', font=font_bold)
        y += 30
        draw.text((100, y), "Please remit payment to:", fill='black', font=font_small)
        y += 25
        draw.text((100, y), "Bank: First National Bank of California", fill='black', font=font_small)
        y += 25
        draw.text((100, y), "Account Name: Pinnacle Supply Co.", fill='black', font=font_small)
        y += 25
        draw.text((100, y), "Account Number: 4820-7731-0056", fill='black', font=font_small)
        y += 25
        draw.text((100, y), "Routing Number: 121000358", fill='black', font=font_small)

        # Terms
        y += 50
        draw.line([(80, y), (width - 80, y)], fill='gray', width=1)
        y += 20
        draw.text((100, y), "TERMS AND CONDITIONS:", fill='black', font=font_bold)
        y += 30
        draw.text((100, y), "1. Payment is due within 30 days of invoice date.", fill='black', font=font_small)
        y += 25
        draw.text((100, y), "2. Late payments subject to 1.5% monthly finance charge.", fill='black', font=font_small)
        y += 25
        draw.text((100, y), "3. All returns must be authorized within 15 days of receipt.", fill='black', font=font_small)

        # Thank you
        y += 60
        draw.text((100, y), "Thank you for your business!", fill='black', font=font_medium)

        # Page number
        draw.text((width // 2 - 30, height - 60), "Page 2 of 2", fill='gray', font=font_small)

    # Add slight noise/texture to simulate scan
    import random
    random.seed(42 + page_num)
    pixels = img.load()
    for _ in range(3000):
        rx = random.randint(0, width - 1)
        ry = random.randint(0, height - 1)
        gray = random.randint(220, 245)
        pixels[rx, ry] = (gray, gray, gray)

    return img


def create_scanned_pdf():
    """Create a 2-page scanned invoice PDF (images only, no selectable text)."""
    import pymupdf

    os.makedirs(DOCUMENTS, exist_ok=True)

    # Generate page images
    page1_img = create_invoice_page_image(1)
    page2_img = create_invoice_page_image(2)

    # Save images to byte buffers
    buf1 = io.BytesIO()
    page1_img.save(buf1, format='PNG')
    buf1.seek(0)

    buf2 = io.BytesIO()
    page2_img.save(buf2, format='PNG')
    buf2.seek(0)

    # Create PDF with images as pages (NO text layer)
    doc = pymupdf.open()

    for buf in [buf1, buf2]:
        img_data = buf.read()
        img_doc = pymupdf.open(stream=img_data, filetype="png")
        # Get image dimensions
        img_page = img_doc[0]
        img_rect = img_page.rect
        # Create a page matching letter size
        page = doc.new_page(width=612, height=792)
        # Insert image to fill page
        page.insert_image(page.rect, stream=img_data)
        img_doc.close()

    doc.save(OUTPUT)
    doc.close()
    print(f'Scanned invoice PDF created: {OUTPUT}')

    # Verify no selectable text
    verify_doc = pymupdf.open(OUTPUT)
    for i, page in enumerate(verify_doc):
        text = page.get_text()
        if text.strip():
            print(f'WARNING: Page {i+1} has selectable text: {text[:100]}')
        else:
            print(f'Page {i+1}: No selectable text (image-only) - OK')
    verify_doc.close()

    # Open in evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_scanned_pdf()
