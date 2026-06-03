"""
Initial Setup: Create a scanned invoice PDF (image-only, no text layer)
Task ID: pdf_gf2_012
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
SCANS_DIR = f'{WORKDIR}/scans'
OUTPUT = f'{SCANS_DIR}/invoice_scan.pdf'


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


def create_invoice_page_image(page_num, width=2480, height=3508):
    """Create a realistic scanned invoice page as a PIL Image.
    Resolution: 300 DPI for A4 (2480x3508 px).
    """
    from PIL import Image, ImageDraw, ImageFont
    import random

    # Create slightly off-white background to simulate scan
    bg_color = (248, 246, 243)
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Try to use a monospace/serif font; fall back to default
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 42)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except Exception:
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 64)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 42)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 36)
            font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 28)
        except Exception:
            font_large = ImageFont.load_default()
            font_medium = font_large
            font_small = font_large
            font_tiny = font_large

    text_color = (30, 30, 30)
    gray_color = (100, 100, 100)
    line_color = (180, 180, 180)

    if page_num == 1:
        # === PAGE 1: Invoice Header + First set of line items ===
        y = 120

        # Company header
        draw.text((160, y), "Meridian Technology Solutions Inc.", fill=text_color, font=font_large)
        y += 90
        draw.text((160, y), "1425 Innovation Boulevard, Suite 300", fill=gray_color, font=font_small)
        y += 50
        draw.text((160, y), "San Francisco, CA 94107", fill=gray_color, font=font_small)
        y += 50
        draw.text((160, y), "Tel: (415) 555-8234  |  Fax: (415) 555-8235", fill=gray_color, font=font_tiny)
        y += 50
        draw.text((160, y), "www.meridiantech.com  |  billing@meridiantech.com", fill=gray_color, font=font_tiny)
        y += 80

        # Horizontal line
        draw.line([(120, y), (width - 120, y)], fill=line_color, width=3)
        y += 50

        # INVOICE title
        draw.text((160, y), "INVOICE", fill=(0, 51, 102), font=font_large)
        y += 100

        # Invoice details (left side)
        draw.text((160, y), "Invoice Number:", fill=gray_color, font=font_small)
        draw.text((600, y), "INV-2026-0042", fill=text_color, font=font_small)
        y += 55
        draw.text((160, y), "Invoice Date:", fill=gray_color, font=font_small)
        draw.text((600, y), "March 15, 2026", fill=text_color, font=font_small)
        y += 55
        draw.text((160, y), "Due Date:", fill=gray_color, font=font_small)
        draw.text((600, y), "April 14, 2026", fill=text_color, font=font_small)
        y += 55
        draw.text((160, y), "Payment Terms:", fill=gray_color, font=font_small)
        draw.text((600, y), "Net 30", fill=text_color, font=font_small)
        y += 55
        draw.text((160, y), "Purchase Order:", fill=gray_color, font=font_small)
        draw.text((600, y), "PO-2026-1187", fill=text_color, font=font_small)
        y += 90

        # Bill To / Ship To
        col2_x = 1300
        draw.text((160, y), "BILL TO:", fill=(0, 51, 102), font=font_medium)
        draw.text((col2_x, y), "SHIP TO:", fill=(0, 51, 102), font=font_medium)
        y += 60
        draw.text((160, y), "Apex Digital Corp.", fill=text_color, font=font_small)
        draw.text((col2_x, y), "Apex Digital Corp.", fill=text_color, font=font_small)
        y += 48
        draw.text((160, y), "Attn: Rachel Nguyen", fill=text_color, font=font_small)
        draw.text((col2_x, y), "Warehouse B, Dock 4", fill=text_color, font=font_small)
        y += 48
        draw.text((160, y), "890 Commerce Drive", fill=text_color, font=font_small)
        draw.text((col2_x, y), "890 Commerce Drive", fill=text_color, font=font_small)
        y += 48
        draw.text((160, y), "Austin, TX 78701", fill=text_color, font=font_small)
        draw.text((col2_x, y), "Austin, TX 78701", fill=text_color, font=font_small)
        y += 48
        draw.text((160, y), "rachel.nguyen@apexdigital.com", fill=text_color, font=font_tiny)
        y += 80

        # Separator line
        draw.line([(120, y), (width - 120, y)], fill=line_color, width=3)
        y += 30

        # Table header
        headers = [("Item", 160), ("Description", 400), ("Qty", 1400), ("Unit Price", 1600), ("Amount", 2000)]
        # Header background
        draw.rectangle([(120, y - 5), (width - 120, y + 50)], fill=(0, 51, 102))
        for hdr_text, hdr_x in headers:
            draw.text((hdr_x, y), hdr_text, fill=(255, 255, 255), font=font_small)
        y += 65

        # Line items (first page)
        items_page1 = [
            ("1", "Enterprise Server Rack - 42U", "2", "$4,250.00", "$8,500.00"),
            ("2", "Network Switch 48-Port PoE+", "6", "$1,890.00", "$11,340.00"),
            ("3", "Fiber Optic Cable Cat6a (100m)", "12", "$185.00", "$2,220.00"),
            ("4", "UPS Battery Backup 3000VA", "4", "$2,150.00", "$8,600.00"),
            ("5", "SSD Storage Drive 2TB NVMe", "16", "$345.00", "$5,520.00"),
            ("6", "Server RAM DDR5 64GB Kit", "8", "$489.00", "$3,912.00"),
            ("7", "Cable Management Panel 2U", "10", "$75.00", "$750.00"),
        ]

        for i, (num, desc, qty, unit, amount) in enumerate(items_page1):
            row_bg = bg_color if i % 2 == 0 else (238, 238, 238)
            draw.rectangle([(120, y - 5), (width - 120, y + 48)], fill=row_bg)
            draw.text((180, y), num, fill=text_color, font=font_small)
            draw.text((400, y), desc, fill=text_color, font=font_small)
            draw.text((1420, y), qty, fill=text_color, font=font_small)
            draw.text((1600, y), unit, fill=text_color, font=font_small)
            draw.text((2000, y), amount, fill=text_color, font=font_small)
            y += 55

        # Bottom line
        draw.line([(120, y), (width - 120, y)], fill=line_color, width=2)
        y += 30
        draw.text((160, y), "Continued on next page...", fill=gray_color, font=font_tiny)

        # Footer
        draw.text((160, height - 120), "Page 1 of 3", fill=gray_color, font=font_tiny)

    elif page_num == 2:
        # === PAGE 2: Remaining line items + subtotal section ===
        y = 120

        draw.text((160, y), "Meridian Technology Solutions Inc.", fill=text_color, font=font_medium)
        y += 60
        draw.text((160, y), "Invoice: INV-2026-0042 (continued)", fill=gray_color, font=font_small)
        y += 70

        # Separator
        draw.line([(120, y), (width - 120, y)], fill=line_color, width=3)
        y += 30

        # Table header repeated
        headers = [("Item", 160), ("Description", 400), ("Qty", 1400), ("Unit Price", 1600), ("Amount", 2000)]
        draw.rectangle([(120, y - 5), (width - 120, y + 50)], fill=(0, 51, 102))
        for hdr_text, hdr_x in headers:
            draw.text((hdr_x, y), hdr_text, fill=(255, 255, 255), font=font_small)
        y += 65

        items_page2 = [
            ("8", "Rack-Mount Console KVM Switch", "3", "$1,275.00", "$3,825.00"),
            ("9", "Cooling Fan Unit Industrial", "6", "$420.00", "$2,520.00"),
            ("10", "PDU Intelligent 30A 240V", "4", "$1,680.00", "$6,720.00"),
            ("11", "Server CPU Intel Xeon Gold", "4", "$3,295.00", "$13,180.00"),
            ("12", "Ethernet Patch Panel 48-Port", "8", "$225.00", "$1,800.00"),
            ("13", "Anti-Static Floor Tiles (box)", "20", "$95.00", "$1,900.00"),
            ("14", "Fire Suppression Unit FM-200", "2", "$5,800.00", "$11,600.00"),
            ("15", "Installation & Configuration", "1", "$8,500.00", "$8,500.00"),
        ]

        for i, (num, desc, qty, unit, amount) in enumerate(items_page2):
            row_bg = bg_color if i % 2 == 0 else (238, 238, 238)
            draw.rectangle([(120, y - 5), (width - 120, y + 48)], fill=row_bg)
            draw.text((180, y), num, fill=text_color, font=font_small)
            draw.text((400, y), desc, fill=text_color, font=font_small)
            draw.text((1420, y), qty, fill=text_color, font=font_small)
            draw.text((1600, y), unit, fill=text_color, font=font_small)
            draw.text((2000, y), amount, fill=text_color, font=font_small)
            y += 55

        # Separator line
        draw.line([(120, y), (width - 120, y)], fill=line_color, width=2)
        y += 50

        # Subtotal section
        draw.text((1400, y), "Subtotal:", fill=text_color, font=font_medium)
        draw.text((1950, y), "$90,887.00", fill=text_color, font=font_medium)
        y += 60
        draw.text((1400, y), "Tax (8.25%):", fill=text_color, font=font_small)
        draw.text((1950, y), "$7,498.18", fill=text_color, font=font_small)
        y += 55
        draw.text((1400, y), "Shipping:", fill=text_color, font=font_small)
        draw.text((1950, y), "$1,250.00", fill=text_color, font=font_small)
        y += 55
        draw.line([(1400, y), (width - 120, y)], fill=text_color, width=2)
        y += 20
        draw.text((1400, y), "TOTAL DUE:", fill=(0, 51, 102), font=font_large)
        draw.text((1900, y), "$99,635.18", fill=(0, 51, 102), font=font_large)

        # Footer
        draw.text((160, height - 120), "Page 2 of 3", fill=gray_color, font=font_tiny)

    elif page_num == 3:
        # === PAGE 3: Payment info, terms, and notes ===
        y = 120

        draw.text((160, y), "Meridian Technology Solutions Inc.", fill=text_color, font=font_medium)
        y += 60
        draw.text((160, y), "Invoice: INV-2026-0042 - Payment Information", fill=gray_color, font=font_small)
        y += 70

        draw.line([(120, y), (width - 120, y)], fill=line_color, width=3)
        y += 50

        draw.text((160, y), "PAYMENT INSTRUCTIONS", fill=(0, 51, 102), font=font_medium)
        y += 70

        draw.text((160, y), "Bank Name:", fill=gray_color, font=font_small)
        draw.text((600, y), "Pacific Commerce Bank", fill=text_color, font=font_small)
        y += 55
        draw.text((160, y), "Account Name:", fill=gray_color, font=font_small)
        draw.text((600, y), "Meridian Technology Solutions Inc.", fill=text_color, font=font_small)
        y += 55
        draw.text((160, y), "Account Number:", fill=gray_color, font=font_small)
        draw.text((600, y), "7842-0156-3391", fill=text_color, font=font_small)
        y += 55
        draw.text((160, y), "Routing Number:", fill=gray_color, font=font_small)
        draw.text((600, y), "021-000-089", fill=text_color, font=font_small)
        y += 55
        draw.text((160, y), "SWIFT Code:", fill=gray_color, font=font_small)
        draw.text((600, y), "PCBKUS66", fill=text_color, font=font_small)
        y += 55
        draw.text((160, y), "Reference:", fill=gray_color, font=font_small)
        draw.text((600, y), "INV-2026-0042", fill=text_color, font=font_small)
        y += 90

        draw.line([(120, y), (width - 120, y)], fill=line_color, width=2)
        y += 50

        draw.text((160, y), "TERMS AND CONDITIONS", fill=(0, 51, 102), font=font_medium)
        y += 70

        terms = [
            "1. Payment is due within 30 days of invoice date.",
            "2. Late payments will incur a 1.5% monthly finance charge.",
            "3. All goods remain property of Meridian Technology Solutions",
            "   Inc. until full payment is received.",
            "4. Returns must be authorized within 15 business days of delivery.",
            "5. Warranty: 36 months for hardware, 12 months for installation.",
            "6. Prices quoted in USD. International payments subject to",
            "   applicable exchange rates at time of transaction.",
            "7. This invoice is governed by the laws of the State of California.",
        ]
        for line in terms:
            draw.text((180, y), line, fill=text_color, font=font_small)
            y += 50

        y += 40
        draw.line([(120, y), (width - 120, y)], fill=line_color, width=2)
        y += 50

        draw.text((160, y), "NOTES", fill=(0, 51, 102), font=font_medium)
        y += 65
        notes = [
            "Thank you for your business. For questions regarding this invoice,",
            "please contact our accounts receivable department at (415) 555-8234",
            "ext. 201 or email billing@meridiantech.com.",
            "",
            "Authorized Signature: ____________________________",
            "",
            "Date: March 15, 2026",
        ]
        for line in notes:
            draw.text((180, y), line, fill=text_color, font=font_small)
            y += 48

        # Footer
        draw.text((160, height - 120), "Page 3 of 3", fill=gray_color, font=font_tiny)
        draw.text((160, height - 70), "Meridian Technology Solutions Inc. | Tax ID: 94-3847291", fill=gray_color, font=font_tiny)

    # Add slight scan artifacts (noise, slight rotation effect)
    # Add some random specks to simulate scan noise
    import random
    random.seed(42 + page_num)
    for _ in range(200):
        x = random.randint(0, width - 1)
        y_noise = random.randint(0, height - 1)
        c = random.randint(180, 220)
        draw.point((x, y_noise), fill=(c, c, c))

    return img


def create_initial():
    from PIL import Image
    import pymupdf

    os.makedirs(SCANS_DIR, exist_ok=True)

    # Create a PDF where each page is purely an image (no text layer)
    doc = pymupdf.open()

    for page_num in range(1, 4):
        # Generate the invoice page as an image
        img = create_invoice_page_image(page_num)

        # Save image to a temporary file
        tmp_img_path = f'/tmp/invoice_page_{page_num}.png'
        img.save(tmp_img_path, 'PNG')

        # Create A4 page and insert image to fill the whole page
        page = doc.new_page(width=595, height=842)  # A4 in points
        page_rect = pymupdf.Rect(0, 0, 595, 842)
        page.insert_image(page_rect, filename=tmp_img_path)

        # Clean up temp file
        os.remove(tmp_img_path)

    doc.save(OUTPUT)
    doc.close()

    print(f'Initial file created: {OUTPUT}')

    # Verify: no text layer
    doc = pymupdf.open(OUTPUT)
    for i in range(doc.page_count):
        text = doc[i].get_text("text").strip()
        print(f'Page {i+1} text length: {len(text)} (should be 0 or near 0)')
    doc.close()

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
