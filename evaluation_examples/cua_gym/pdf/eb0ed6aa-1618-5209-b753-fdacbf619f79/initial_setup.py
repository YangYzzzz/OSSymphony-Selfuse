"""
Initial Setup: Create a 20-page photo book PDF with high-res images, non-embedded fonts, empty metadata
Task ID: pdf_pw_007
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import struct
import zlib

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

def create_png_bytes_fast(width, height, r, g, b, pattern_seed=0):
    """Create a PNG image in memory using numpy for speed."""
    import numpy as np
    rng = np.random.RandomState(pattern_seed)

    # Create gradient base
    x_grad = np.linspace(-40, 40, width).astype(np.float32)
    y_grad = np.linspace(-40, 40, height).astype(np.float32)

    # Build channels with gradient + noise
    noise_r = rng.randint(-20, 21, size=(height, width), dtype=np.int16)
    noise_g = rng.randint(-20, 21, size=(height, width), dtype=np.int16)
    noise_b = rng.randint(-30, 31, size=(height, width), dtype=np.int16)

    ch_r = np.clip(r + x_grad[None, :] + noise_r, 0, 255).astype(np.uint8)
    ch_g = np.clip(g + y_grad[:, None] + noise_g, 0, 255).astype(np.uint8)
    ch_b = np.clip(b + noise_b, 0, 255).astype(np.uint8)

    # Interleave RGB and prepend filter byte per row
    rgb = np.stack([ch_r, ch_g, ch_b], axis=-1)  # (H, W, 3)
    # Prepend filter byte (0) to each row
    filter_col = np.zeros((height, 1), dtype=np.uint8)
    rows_with_filter = np.concatenate([filter_col, rgb.reshape(height, -1)], axis=1)
    raw_data = rows_with_filter.tobytes()

    compressed = zlib.compress(raw_data, 1)  # Low compression to keep file large

    def png_chunk(chunk_type, data):
        chunk = chunk_type + data
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', zlib.crc32(chunk) & 0xFFFFFFFF)

    png = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    png += png_chunk(b'IHDR', ihdr_data)
    png += png_chunk(b'IDAT', compressed)
    png += png_chunk(b'IEND', b'')
    return png


def create_initial():
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    WORKDIR = '/home/user'
    TASK_ID = 'pdf_pw_007'
    PUBDIR = f'{WORKDIR}/publishing'
    OUTPUT = f'{PUBDIR}/photo_book.pdf'

    os.makedirs(PUBDIR, exist_ok=True)

    doc = pymupdf.open()

    # Page themes for a realistic photo book
    page_themes = [
        ("Summer Memories", "A collection of our favorite moments from the summer of 2025"),
        ("Beach Day - June 15", "The whole family enjoyed a perfect day at Malibu Beach"),
        ("Sunset at Santa Monica Pier", "Golden hour painted the sky in shades of amber and coral"),
        ("Hiking Trail Adventures", "We explored the scenic trails of Griffith Park together"),
        ("BBQ at Grandma's", "The annual family barbecue brought everyone together again"),
        ("Fourth of July Fireworks", "Spectacular display over the harbor lit up the night sky"),
        ("Summer Road Trip - Day 1", "Starting our journey from Los Angeles to the Grand Canyon"),
        ("Grand Canyon Overlook", "The breathtaking view from the South Rim at dawn"),
        ("Camping Under the Stars", "Our first night camping in Sedona was absolutely magical"),
        ("Lake Powell Adventures", "Kayaking and swimming in the crystal clear waters"),
        ("Mountain Biking in Moab", "An exhilarating ride through the red rock desert trails"),
        ("Farmers Market Sundays", "Fresh produce and handmade crafts every Sunday morning"),
        ("Garden Party - July 20", "Elena's birthday celebration in the backyard garden"),
        ("Summer Concert Series", "Live music at the Hollywood Bowl under the evening sky"),
        ("Beach Volleyball Tournament", "Our team made it to the semifinals this year"),
        ("Surfing Lessons", "The kids finally stood up on their boards for the first time"),
        ("Ice Cream Adventures", "Trying every flavor at the new gelato shop downtown"),
        ("Stargazing at Joshua Tree", "The Milky Way was visible in all its glory"),
        ("Last Day of Summer", "Bittersweet farewell to an unforgettable season"),
        ("Photo Credits & Acknowledgments", "All photos by Elena Rodriguez and family members"),
    ]

    # Color themes for images (RGB base colors for each page)
    color_themes = [
        (70, 130, 180),   # steel blue - cover
        (135, 206, 235),  # sky blue - beach
        (255, 165, 80),   # orange - sunset
        (34, 139, 34),    # forest green - hiking
        (210, 105, 30),   # chocolate - BBQ
        (25, 25, 112),    # midnight blue - fireworks
        (188, 143, 143),  # rosy brown - road trip
        (205, 92, 92),    # indian red - canyon
        (72, 61, 139),    # dark slate blue - camping
        (0, 139, 139),    # dark cyan - lake
        (178, 34, 34),    # firebrick - biking
        (85, 107, 47),    # dark olive green - market
        (219, 112, 147),  # pale violet red - party
        (106, 90, 205),   # slate blue - concert
        (244, 164, 96),   # sandy brown - volleyball
        (0, 128, 128),    # teal - surfing
        (255, 182, 193),  # light pink - ice cream
        (47, 79, 79),     # dark slate gray - stargazing
        (255, 140, 0),    # dark orange - last day
        (128, 128, 128),  # gray - credits
    ]

    for i, (title, caption) in enumerate(page_themes):
        page = doc.new_page(width=612, height=792)  # Letter size

        # Insert a large image (simulating high-res photo at 300+ DPI)
        # For a 6x4 inch image area at 300 DPI = 1800x1200 pixels
        img_w, img_h = 1800, 1200
        r, g, b = color_themes[i]
        png_data = create_png_bytes_fast(img_w, img_h, r, g, b, pattern_seed=i * 1000)

        # Place image in a large area on the page
        if i == 0:
            # Cover page - full page image
            img_rect = pymupdf.Rect(36, 100, 576, 620)
        elif i == 19:
            # Credits page - smaller image
            img_rect = pymupdf.Rect(156, 200, 456, 400)
        else:
            # Regular pages - large photo area
            img_rect = pymupdf.Rect(56, 120, 556, 580)

        page.insert_image(img_rect, stream=png_data)

        # Add title text
        if i == 0:
            # Cover page
            page.insert_text(
                pymupdf.Point(306, 60),
                title,
                fontsize=28,
                fontname="hebo",
                color=(0.1, 0.1, 0.3),
            )
            page.insert_text(
                pymupdf.Point(106, 660),
                caption,
                fontsize=14,
                fontname="tiit",
                color=(0.3, 0.3, 0.3),
            )
            page.insert_text(
                pymupdf.Point(206, 720),
                "Photos by Elena Rodriguez",
                fontsize=12,
                fontname="helv",
                color=(0.4, 0.4, 0.4),
            )
        else:
            # Regular pages
            page.insert_text(
                pymupdf.Point(56, 80),
                title,
                fontsize=20,
                fontname="hebo",
                color=(0.15, 0.15, 0.35),
            )
            page.insert_text(
                pymupdf.Point(56, 620),
                caption,
                fontsize=11,
                fontname="tiit",
                color=(0.35, 0.35, 0.35),
            )
            # Page number
            page.insert_text(
                pymupdf.Point(296, 760),
                str(i + 1),
                fontsize=10,
                fontname="helv",
                color=(0.5, 0.5, 0.5),
            )

    # Explicitly clear metadata
    doc.set_metadata({
        "title": "",
        "author": "",
        "subject": "",
        "keywords": "",
        "creator": "",
        "producer": "",
    })

    doc.save(OUTPUT, deflate=False)  # No deflation to keep file larger
    doc.close()

    file_size = os.path.getsize(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print(f'File size: {file_size / (1024*1024):.1f} MB')
    print(f'Pages: 20')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
