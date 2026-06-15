"""
Initial Setup: Create a scanned receipt image PDF (no text layer)
Task ID: pdf_fin_015
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

from PIL import Image, ImageDraw, ImageFont

WORKDIR = '/home/user'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/scanned_receipt.pdf'


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


def create_receipt_image():
    """Create a realistic restaurant receipt as a raster image."""
    # Receipt dimensions (typical thermal receipt proportions)
    width, height = 600, 900
    img = Image.new('RGB', (width, height), color=(252, 250, 245))
    draw = ImageDraw.Draw(img)

    # Try to use a monospace font, fall back to default
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 22)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
    except (IOError, OSError):
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf", 22)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 16)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 14)
        except (IOError, OSError):
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()

    color = (30, 30, 30)
    y = 30

    # Restaurant header
    draw.text((width // 2, y), "THE GOLDEN FORK", fill=color, font=font_large, anchor="mt")
    y += 35
    draw.text((width // 2, y), "RESTAURANT & BAR", fill=color, font=font_medium, anchor="mt")
    y += 25
    draw.text((width // 2, y), "425 Market Street, Suite 100", fill=color, font=font_small, anchor="mt")
    y += 20
    draw.text((width // 2, y), "San Francisco, CA 94105", fill=color, font=font_small, anchor="mt")
    y += 20
    draw.text((width // 2, y), "Tel: (415) 555-0178", fill=color, font=font_small, anchor="mt")
    y += 30

    # Separator
    draw.line([(40, y), (width - 40, y)], fill=color, width=1)
    y += 15

    # Date and receipt info
    draw.text((50, y), "Date: 03/15/2025", fill=color, font=font_medium)
    y += 22
    draw.text((50, y), "Time: 07:32 PM", fill=color, font=font_medium)
    y += 22
    draw.text((50, y), "Server: Maria T.", fill=color, font=font_medium)
    y += 22
    draw.text((50, y), "Table: 14", fill=color, font=font_medium)
    y += 22
    draw.text((50, y), "Receipt #: 20250315-0847", fill=color, font=font_medium)
    y += 30

    # Separator
    draw.line([(40, y), (width - 40, y)], fill=color, width=1)
    y += 15

    # Column headers
    draw.text((50, y), "Item", fill=color, font=font_medium)
    draw.text((380, y), "Qty", fill=color, font=font_medium)
    draw.text((460, y), "Amount", fill=color, font=font_medium)
    y += 25

    # Separator
    draw.line([(40, y), (width - 40, y)], fill=(120, 120, 120), width=1)
    y += 10

    # Items
    items = [
        ("Caesar Salad", "1", "$12.50"),
        ("Grilled Salmon", "2", "$56.00"),
        ("Mushroom Risotto", "1", "$24.00"),
        ("Wagyu Beef Burger", "1", "$32.00"),
        ("Truffle Fries", "1", "$14.50"),
        ("Sparkling Water", "3", "$13.50"),
        ("House Red Wine", "2", "$28.00"),
        ("Tiramisu", "2", "$22.00"),
        ("Espresso", "2", "$9.00"),
    ]

    for item_name, qty, amount in items:
        draw.text((50, y), item_name, fill=color, font=font_small)
        draw.text((395, y), qty, fill=color, font=font_small)
        draw.text((460, y), amount, fill=color, font=font_small)
        y += 22

    y += 10
    # Separator
    draw.line([(40, y), (width - 40, y)], fill=color, width=1)
    y += 15

    # Totals
    draw.text((300, y), "Subtotal:", fill=color, font=font_medium)
    draw.text((460, y), "$211.50", fill=color, font=font_medium)
    y += 25
    draw.text((300, y), "Tax (8.625%):", fill=color, font=font_medium)
    draw.text((460, y), "$18.24", fill=color, font=font_medium)
    y += 25
    draw.line([(290, y), (width - 40, y)], fill=color, width=1)
    y += 10
    draw.text((300, y), "TOTAL:", fill=color, font=font_large)
    draw.text((450, y), "$229.74", fill=color, font=font_large)
    y += 35

    # Separator
    draw.line([(40, y), (width - 40, y)], fill=color, width=1)
    y += 15

    # Payment info
    draw.text((50, y), "Payment: Visa ****4821", fill=color, font=font_medium)
    y += 22
    draw.text((50, y), "Auth Code: 739201", fill=color, font=font_medium)
    y += 30

    # Tip and Total with Tip
    draw.text((50, y), "Tip:  _______________", fill=color, font=font_medium)
    y += 25
    draw.text((50, y), "Total: _______________", fill=color, font=font_medium)
    y += 30

    # Signature line
    draw.text((50, y), "Signature: _______________", fill=color, font=font_medium)
    y += 35

    # Footer
    draw.text((width // 2, y), "Thank you for dining with us!", fill=color, font=font_small, anchor="mt")
    y += 20
    draw.text((width // 2, y), "Visit us at www.goldenfork.com", fill=color, font=font_small, anchor="mt")

    # Add some slight noise/texture to simulate scan artifacts
    import random
    random.seed(42)
    pixels = img.load()
    for _ in range(800):
        rx = random.randint(0, width - 1)
        ry = random.randint(0, height - 1)
        r, g, b = pixels[rx, ry]
        noise = random.randint(-15, 15)
        pixels[rx, ry] = (
            max(0, min(255, r + noise)),
            max(0, min(255, g + noise)),
            max(0, min(255, b + noise))
        )

    return img


def create_initial():
    os.makedirs(FINANCE_DIR, exist_ok=True)

    # Step 1: Create receipt as a raster image
    receipt_img = create_receipt_image()
    tmp_img_path = '/tmp/receipt_scan.png'
    receipt_img.save(tmp_img_path, 'PNG')

    # Step 2: Convert image to a single-page PDF (image-only, no text layer)
    doc = pymupdf.open()
    # Create page matching receipt aspect ratio
    img_w, img_h = receipt_img.size
    # Scale to fit A4-ish page width (595 points), maintain aspect ratio
    page_width = 595
    page_height = int(page_width * img_h / img_w)
    page = doc.new_page(width=page_width, height=page_height)

    # Insert the receipt image to fill the entire page
    img_rect = pymupdf.Rect(0, 0, page_width, page_height)
    page.insert_image(img_rect, filename=tmp_img_path)

    doc.save(OUTPUT)
    doc.close()

    # Clean up temp file
    os.remove(tmp_img_path)

    print(f'Initial file created: {OUTPUT}')

    # Verify no text layer
    verify_doc = pymupdf.open(OUTPUT)
    text = verify_doc[0].get_text("text").strip()
    verify_doc.close()
    if text:
        print(f'WARNING: Text layer detected in initial PDF: "{text[:100]}"')
    else:
        print('Verified: No text layer in initial PDF (image-only scan)')

    # GUI-ready startup: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
