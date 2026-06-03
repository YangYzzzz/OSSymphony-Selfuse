"""
Initial Setup: Create a multi-page PDF with high-resolution embedded images (~20MB)
Task ID: pdf_gf1_036
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import struct
import zlib

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_036'
OUTPUT = f'{WORKDIR}/Documents/photo_report.pdf'

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

def create_png_bytes(width, height, r, g, b, pattern_type='gradient'):
    """Create a raw PNG image in memory with varied patterns to simulate real photos.
    Returns PNG bytes. Uses gradient/noise patterns to create realistic file sizes."""
    import random
    random.seed(r * 1000 + g * 100 + b + width + pattern_type.__hash__() % 10000)

    rows = []
    for y in range(height):
        row = b'\x00'  # filter byte: None
        for x in range(width):
            if pattern_type == 'gradient':
                # Diagonal gradient with color variation
                t = (x + y) / (width + height)
                pr = int(r * (1 - t) + (255 - r) * t) % 256
                pg = int(g * (1 - t) + (255 - g) * t) % 256
                pb = int(b * (1 - t) + (255 - b) * t) % 256
            elif pattern_type == 'blocks':
                block_size = 40
                bx = (x // block_size) % 3
                by = (y // block_size) % 3
                pr = (r + bx * 60 + by * 30) % 256
                pg = (g + by * 50 + bx * 20) % 256
                pb = (b + (bx + by) * 40) % 256
            elif pattern_type == 'circles':
                cx, cy = width // 2, height // 2
                dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                ring = int(dist / 30) % 4
                pr = (r + ring * 50) % 256
                pg = (g + ring * 30) % 256
                pb = (b + ring * 70) % 256
            elif pattern_type == 'stripes':
                stripe = ((x + y) // 20) % 5
                pr = (r + stripe * 45) % 256
                pg = (g + stripe * 35) % 256
                pb = (b + stripe * 55) % 256
            else:  # noise-like
                noise = random.randint(-30, 30)
                pr = max(0, min(255, r + noise + (x % 50)))
                pg = max(0, min(255, g + noise + (y % 40)))
                pb = max(0, min(255, b + noise))
            row += bytes([pr, pg, pb])
        rows.append(row)

    raw_data = b''.join(rows)

    # Build PNG manually with NO compression to maximize file size
    def make_chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        return struct.pack('>I', len(data)) + c + crc

    # PNG signature
    png = b'\x89PNG\r\n\x1a\n'

    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    png += make_chunk(b'IHDR', ihdr_data)

    # IDAT - use compression level 0 (store) to keep file large
    compressed = zlib.compress(raw_data, 0)
    png += make_chunk(b'IDAT', compressed)

    # IEND
    png += make_chunk(b'IEND', b'')

    return png


def create_initial():
    import pymupdf

    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions - Letter size
    W, H = 612, 792

    # Define 5 pages with different product themes
    pages_config = [
        {
            'title': 'Luminance Pro X7 - Wireless Headphones',
            'subtitle': 'Product Photography Report - Premium Audio Line',
            'body': 'The Luminance Pro X7 represents our flagship wireless headphone offering. '
                    'Featuring adaptive noise cancellation, 40mm beryllium drivers, and a '
                    '38-hour battery life, this product targets the premium consumer segment. '
                    'All photographs were captured at 300 DPI for print-ready marketing materials.',
            'img_color': (180, 60, 40),
            'pattern': 'gradient',
        },
        {
            'title': 'AeroVista Smart Watch - Series 4',
            'subtitle': 'Lifestyle Product Shots - Outdoor Campaign',
            'body': 'The AeroVista Series 4 smart watch features a titanium case, sapphire crystal '
                    'display, and advanced health monitoring sensors including blood oxygen and ECG. '
                    'These product images showcase the watch in outdoor adventure settings for the '
                    'upcoming Q3 marketing campaign across digital and print channels.',
            'img_color': (40, 100, 180),
            'pattern': 'blocks',
        },
        {
            'title': 'Ember Home Diffuser - Ceramic Collection',
            'subtitle': 'Home Decor Product Line - Studio Photography',
            'body': 'The Ember Ceramic Collection features handcrafted aromatherapy diffusers '
                    'in five colorways: Sandstone, Ocean Mist, Forest Moss, Sunset Clay, and '
                    'Midnight Slate. Studio photography captured fine texture details of the '
                    'ceramic glaze and brushed copper accent rings at high resolution.',
            'img_color': (120, 90, 60),
            'pattern': 'circles',
        },
        {
            'title': 'Velocity Carbon Road Bike - Frame Detail',
            'subtitle': 'Engineering Documentation - Carbon Fiber Layup',
            'body': 'High-resolution documentation of the Velocity Pro carbon fiber frame '
                    'construction. Images capture the monocoque layup pattern, internal cable '
                    'routing channels, and bottom bracket junction. These reference photographs '
                    'are used by the engineering team for quality assurance inspection.',
            'img_color': (50, 50, 50),
            'pattern': 'stripes',
        },
        {
            'title': 'TerraBrew Espresso Machine - Matte Black Edition',
            'subtitle': 'E-Commerce Product Gallery - Final Selection',
            'body': 'Final selection of product photographs for the TerraBrew Matte Black '
                    'Edition espresso machine. Images include the main unit, portafilter detail, '
                    'steam wand close-up, and drip tray assembly. Selected for the online store '
                    'product page and comparison charts on partner retail sites.',
            'img_color': (30, 30, 35),
            'pattern': 'noise',
        },
    ]

    for i, config in enumerate(pages_config):
        page = doc.new_page(width=W, height=H)

        # Title
        page.insert_text(
            pymupdf.Point(50, 60),
            config['title'],
            fontsize=18,
            fontname="hebo",
            color=(0.1, 0.1, 0.1),
        )

        # Subtitle
        page.insert_text(
            pymupdf.Point(50, 85),
            config['subtitle'],
            fontsize=11,
            fontname="heit",
            color=(0.4, 0.4, 0.4),
        )

        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(50, 95), pymupdf.Point(562, 95))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()

        # Body text
        text_rect = pymupdf.Rect(50, 110, 562, 190)
        page.insert_textbox(
            text_rect,
            config['body'],
            fontsize=10,
            fontname="helv",
            color=(0.2, 0.2, 0.2),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Insert a large high-res image (2400x1800 pixels = 8x6 inches at 300 DPI)
        r, g, b = config['img_color']
        img_bytes = create_png_bytes(2400, 1800, r, g, b, config['pattern'])

        img_rect = pymupdf.Rect(50, 200, 562, 584)  # large display area
        page.insert_image(img_rect, stream=img_bytes)

        # Page footer
        page.insert_text(
            pymupdf.Point(50, 760),
            f'Photo Report  |  Page {i + 1} of 5  |  Confidential - Internal Use Only',
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Second smaller image (1200x900 at 300 DPI)
        img_bytes2 = create_png_bytes(1200, 900, (r + 80) % 256, (g + 60) % 256, (b + 40) % 256, config['pattern'])
        img_rect2 = pymupdf.Rect(50, 594, 306, 740)
        page.insert_image(img_rect2, stream=img_bytes2)

        # Caption
        page.insert_text(
            pymupdf.Point(320, 620),
            f'Detail view {i + 1}: Close-up texture',
            fontsize=9,
            fontname="heit",
            color=(0.3, 0.3, 0.3),
        )

    doc.save(OUTPUT, deflate=False)  # no extra compression to keep large
    doc.close()

    file_size = os.path.getsize(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print(f'File size: {file_size / (1024*1024):.1f} MB')
    print(f'Pages: 5')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
