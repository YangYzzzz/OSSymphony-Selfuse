"""
Initial Setup: Create a large photo album PDF with 30 pages of full-resolution PNG images.
Task ID: pdf_mbc_082
Domain: pdf
Target: ~120MB PDF, 30 pages with PNG images
"""

import os
import io
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_082'
OUTPUT_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{OUTPUT_DIR}/photo_album.pdf'
DONE_MARKER = '/tmp/initial_setup_done'


def launch_gui(command: str, delay_sec: float = 1.0):
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
    import numpy as np
    from PIL import Image

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    album_titles = [
        "Sunset at Malibu Beach", "Mountain Trail Hike", "City Skyline at Dusk",
        "Cherry Blossoms in Kyoto", "Northern Lights in Iceland", "Rainforest Canopy Walk",
        "Venice Canal Reflections", "Safari Wildlife Encounter", "Greek Island Village",
        "Autumn Foliage in Vermont", "Desert Sand Dunes", "Underwater Coral Reef",
        "London Bridge at Night", "Alpine Meadow Wildflowers", "Tropical Waterfall",
        "New York Times Square", "Lavender Fields in Provence", "Rocky Mountain Peaks",
        "Bali Rice Terraces", "Aurora Borealis Finland", "Grand Canyon Overlook",
        "Tokyo Neon Streets", "Machu Picchu Sunrise", "Norwegian Fjord Vista",
        "Sahara Stargazing", "Amazon River Expedition", "Santorini White Houses",
        "Canadian Rockies Lake", "African Savanna Sunset", "Patagonia Glacier"
    ]

    # Target: ~4MB per PNG image -> ~120MB total
    # Use 1200x1600 images with moderate noise (compresses to ~4MB as PNG)
    img_width = 1200
    img_height = 1600

    doc = pymupdf.open()

    for i in range(30):
        print(f"Page {i+1}/30: {album_titles[i]}", flush=True)

        page = doc.new_page(width=595, height=842)

        page.insert_text(
            pymupdf.Point(297, 30),
            album_titles[i],
            fontsize=14,
            fontname="hebo",
            color=(0.2, 0.2, 0.2),
        )

        page.insert_text(
            pymupdf.Point(280, 830),
            f"Page {i+1} of 30",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Create photo-like images: smooth gradients + moderate noise
        # These compress poorly as PNG (targeting ~4MB each) but well as JPEG
        rng = np.random.RandomState(i * 42 + 7)

        # Base: smooth color gradient (like a landscape photo)
        y = np.linspace(0, 1, img_height, dtype=np.float32).reshape(-1, 1)
        x = np.linspace(0, 1, img_width, dtype=np.float32).reshape(1, -1)

        # Different color schemes per image
        phase_r = (i * 2.1 + 0.5)
        phase_g = (i * 1.7 + 1.2)
        phase_b = (i * 3.3 + 0.8)

        r_base = (np.sin(y * phase_r * np.pi + x * 1.5) * 0.5 + 0.5) * 200 + 30
        g_base = (np.sin(y * phase_g * np.pi + x * 2.0) * 0.5 + 0.5) * 200 + 30
        b_base = (np.sin(y * phase_b * np.pi + x * 1.8) * 0.5 + 0.5) * 200 + 30

        # Add moderate noise (~20% of range) to prevent PNG compression
        noise_r = rng.normal(0, 25, size=(img_height, img_width)).astype(np.float32)
        noise_g = rng.normal(0, 25, size=(img_height, img_width)).astype(np.float32)
        noise_b = rng.normal(0, 25, size=(img_height, img_width)).astype(np.float32)

        r = np.clip(r_base + noise_r, 0, 255).astype(np.uint8)
        g = np.clip(g_base + noise_g, 0, 255).astype(np.uint8)
        b = np.clip(b_base + noise_b, 0, 255).astype(np.uint8)

        img_array = np.stack([r, g, b], axis=2)

        img = Image.fromarray(img_array, 'RGB')
        buf = io.BytesIO()
        img.save(buf, format='PNG', compress_level=1)
        png_data = buf.getvalue()

        img_rect = pymupdf.Rect(30, 45, 565, 815)
        page.insert_image(img_rect, stream=png_data)

    print("Saving PDF...", flush=True)
    doc.save(OUTPUT)
    doc.close()

    file_size = os.path.getsize(OUTPUT)
    print(f"Created: {OUTPUT}")
    print(f"Size: {file_size / (1024*1024):.1f} MB")
    print(f"Pages: 30")

    with open(DONE_MARKER, 'w') as f:
        f.write(f"done:{file_size}")

    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
