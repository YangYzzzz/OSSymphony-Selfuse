"""
Initial Setup: Create 5 scanned receipt image-only PDFs
Task ID: pdf_fin_035
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import io

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_035'
SCAN_DIR = f'{WORKDIR}/finance/scanned_receipts'
SEARCH_DIR = f'{WORKDIR}/finance/searchable_receipts'


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


def create_receipt_image(receipt_data):
    """Create a realistic receipt image using Pillow and return PNG bytes."""
    from PIL import Image, ImageDraw, ImageFont

    # Receipt dimensions (thermal receipt style)
    width = 400
    line_height = 22
    padding = 20
    lines = receipt_data['lines']
    height = padding * 2 + len(lines) * line_height + 40

    img = Image.new('L', (width, height), color=245)  # light gray background
    draw = ImageDraw.Draw(img)

    # Use default font (monospace-like)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
        font_bold = font

    y = padding

    for line in lines:
        if line.get('bold'):
            draw.text((padding, y), line['text'], fill=20, font=font_bold)
        elif line.get('center'):
            bbox = draw.textbbox((0, 0), line['text'], font=font)
            tw = bbox[2] - bbox[0]
            x = (width - tw) // 2
            draw.text((x, y), line['text'], fill=30, font=font)
        else:
            draw.text((padding, y), line['text'], fill=30, font=font)
        y += line_height

    # Add slight noise to simulate scan
    import random
    pixels = img.load()
    for _ in range(500):
        rx = random.randint(0, width - 1)
        ry = random.randint(0, height - 1)
        pixels[rx, ry] = random.randint(200, 240)

    # Convert to RGB for PDF embedding
    img_rgb = img.convert('RGB')
    buf = io.BytesIO()
    img_rgb.save(buf, format='PNG')
    return buf.getvalue(), width, height


def create_image_only_pdf(image_bytes, img_width, img_height, output_path):
    """Create a PDF with only an embedded image (no text layer)."""
    import pymupdf

    # Create PDF page sized to match receipt aspect ratio
    # Scale to A4-ish width
    pdf_width = 400
    pdf_height = img_height
    doc = pymupdf.open()
    page = doc.new_page(width=pdf_width, height=pdf_height)

    # Insert image filling the entire page
    page.insert_image(
        pymupdf.Rect(0, 0, pdf_width, pdf_height),
        stream=image_bytes,
    )

    doc.save(output_path)
    doc.close()


def create_initial():
    os.makedirs(SCAN_DIR, exist_ok=True)
    os.makedirs(SEARCH_DIR, exist_ok=True)

    # 5 different realistic receipts
    receipts = [
        {
            'lines': [
                {'text': 'GREENFIELD GROCERY', 'bold': True, 'center': True},
                {'text': '245 Oak Street, Portland, OR 97201', 'center': True},
                {'text': 'Tel: (503) 555-0147', 'center': True},
                {'text': '================================'},
                {'text': 'Date: 2025-11-03  Time: 14:23'},
                {'text': 'Cashier: Maria  Register: 04'},
                {'text': '--------------------------------'},
                {'text': 'Organic Bananas     2.49'},
                {'text': 'Whole Milk 1gal     4.29'},
                {'text': 'Sourdough Bread     5.99'},
                {'text': 'Cheddar Cheese      6.49'},
                {'text': 'Free Range Eggs     7.29'},
                {'text': 'Baby Spinach        3.99'},
                {'text': 'Olive Oil 500ml     8.49'},
                {'text': 'Greek Yogurt x2     6.98'},
                {'text': '--------------------------------'},
                {'text': 'Subtotal           45.01'},
                {'text': 'Tax (8.5%)          3.83'},
                {'text': 'TOTAL              49.84', 'bold': True},
                {'text': '================================'},
                {'text': 'VISA ****4821'},
                {'text': 'Auth: 739204'},
                {'text': ''},
                {'text': 'Thank you for shopping!', 'center': True},
            ]
        },
        {
            'lines': [
                {'text': 'SUNRISE COFFEE HOUSE', 'bold': True, 'center': True},
                {'text': '18 Elm Ave, Seattle, WA 98101', 'center': True},
                {'text': 'Tel: (206) 555-0293', 'center': True},
                {'text': '================================'},
                {'text': 'Date: 2025-11-05  Time: 08:47'},
                {'text': 'Server: Jake  Order #: 1087'},
                {'text': '--------------------------------'},
                {'text': 'Latte Grande        5.50'},
                {'text': 'Croissant           3.75'},
                {'text': 'Avocado Toast       9.50'},
                {'text': 'Fresh OJ            4.25'},
                {'text': '--------------------------------'},
                {'text': 'Subtotal           23.00'},
                {'text': 'Tax (10.1%)         2.32'},
                {'text': 'TOTAL              25.32', 'bold': True},
                {'text': '================================'},
                {'text': 'AMEX ****7156'},
                {'text': 'Auth: 482917'},
                {'text': ''},
                {'text': 'Have a great day!', 'center': True},
            ]
        },
        {
            'lines': [
                {'text': 'METRO OFFICE SUPPLY', 'bold': True, 'center': True},
                {'text': '900 Market St, San Francisco, CA', 'center': True},
                {'text': 'Tel: (415) 555-0381', 'center': True},
                {'text': '================================'},
                {'text': 'Date: 2025-11-07  Time: 11:15'},
                {'text': 'Trans #: 20251107-3342'},
                {'text': '--------------------------------'},
                {'text': 'Printer Paper A4    12.99'},
                {'text': 'Ballpoint Pen x10    8.49'},
                {'text': 'Sticky Notes 3pk     5.79'},
                {'text': 'Binder Clips Lg      4.29'},
                {'text': 'Whiteboard Marker    6.99'},
                {'text': 'USB-C Cable 6ft      9.99'},
                {'text': '--------------------------------'},
                {'text': 'Subtotal           48.54'},
                {'text': 'Tax (8.625%)        4.19'},
                {'text': 'TOTAL              52.73', 'bold': True},
                {'text': '================================'},
                {'text': 'MC ****3290'},
                {'text': 'Auth: 591043'},
                {'text': ''},
                {'text': 'Returns within 30 days w/receipt', 'center': True},
            ]
        },
        {
            'lines': [
                {'text': 'BELLA TRATTORIA', 'bold': True, 'center': True},
                {'text': '77 Pine Road, Austin, TX 78701', 'center': True},
                {'text': 'Tel: (512) 555-0562', 'center': True},
                {'text': '================================'},
                {'text': 'Date: 2025-11-09  Time: 19:38'},
                {'text': 'Server: Sofia  Table: 12'},
                {'text': '--------------------------------'},
                {'text': 'Bruschetta           9.50'},
                {'text': 'Caesar Salad         8.75'},
                {'text': 'Margherita Pizza    14.00'},
                {'text': 'Penne Arrabiata     13.50'},
                {'text': 'Tiramisu             8.00'},
                {'text': 'Sparkling Water      3.50'},
                {'text': 'House Red Wine      11.00'},
                {'text': '--------------------------------'},
                {'text': 'Subtotal           68.25'},
                {'text': 'Tax (8.25%)         5.63'},
                {'text': 'Tip (20%)          13.65'},
                {'text': 'TOTAL              87.53', 'bold': True},
                {'text': '================================'},
                {'text': 'VISA ****9134'},
                {'text': 'Auth: 826471'},
                {'text': ''},
                {'text': 'Grazie! Come again!', 'center': True},
            ]
        },
        {
            'lines': [
                {'text': 'CITY HARDWARE & HOME', 'bold': True, 'center': True},
                {'text': '520 Broadway, Denver, CO 80203', 'center': True},
                {'text': 'Tel: (720) 555-0714', 'center': True},
                {'text': '================================'},
                {'text': 'Date: 2025-11-11  Time: 10:05'},
                {'text': 'Cashier: Tom  Register: 02'},
                {'text': '--------------------------------'},
                {'text': 'LED Bulb 60W 4pk    11.99'},
                {'text': 'Duct Tape 2in        5.49'},
                {'text': 'WD-40 11oz           6.29'},
                {'text': 'Sandpaper 120 10pk   4.79'},
                {'text': 'Paint Roller Kit     8.99'},
                {'text': '--------------------------------'},
                {'text': 'Subtotal           37.55'},
                {'text': 'Tax (8.81%)         3.31'},
                {'text': 'TOTAL              40.86', 'bold': True},
                {'text': '================================'},
                {'text': 'DEBIT ****6078'},
                {'text': 'Auth: 103758'},
                {'text': ''},
                {'text': 'Thank you! Visit us online', 'center': True},
                {'text': 'www.cityhardware.com', 'center': True},
            ]
        },
    ]

    for i, receipt in enumerate(receipts, 1):
        filename = f'receipt_{i:03d}.pdf'
        output_path = os.path.join(SCAN_DIR, filename)
        img_bytes, w, h = create_receipt_image(receipt)
        create_image_only_pdf(img_bytes, w, h, output_path)
        print(f'Created scanned receipt: {output_path}')

    print(f'Empty searchable directory ready: {SEARCH_DIR}')

    # Open file manager showing the scanned receipts directory
    launch_gui(f'nautilus "{SCAN_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus with DISPLAY=:0')


create_initial()
