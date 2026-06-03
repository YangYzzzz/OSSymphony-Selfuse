"""
Initial Setup: Image processing pipeline task
Task ID: osworld_multi_apps_media_image_010
Domain: multi_apps (gimp/os/vlc)

Creates:
  - /home/user/pictures/raw/ with 10 JPEG images
  - /home/user/pictures/processed/ (empty directory)
  - /home/user/scripts/ (empty directory, no process_images.py)
  - Opens a file manager showing /home/user/pictures/raw/ for the GUI agent
"""

import os
import shlex
import subprocess
import time
import random
from PIL import Image, ImageDraw, ImageFont

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_media_image_010'

RAW_DIR = f'{WORKDIR}/pictures/raw'
PROCESSED_DIR = f'{WORKDIR}/pictures/processed'
SCRIPTS_DIR = f'{WORKDIR}/scripts'


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


def create_realistic_image(width: int, height: int, seed: int, title: str) -> Image.Image:
    """Create a realistic-looking photo-like image with scenery/content."""
    random.seed(seed)

    # Create base image with gradient sky or landscape
    img = Image.new("RGB", (width, height))
    pixels = img.load()

    # Sky gradient (top portion)
    sky_height = height * 2 // 3
    sky_colors = [
        (135, 206, 235),  # sky blue
        (100, 180, 220),
        (70, 130, 180),   # steel blue
        (255, 200, 100),  # sunset orange
        (200, 100, 50),   # deep sunset
    ]
    sky_top, sky_bottom = sky_colors[seed % len(sky_colors)], sky_colors[(seed + 1) % len(sky_colors)]

    for y in range(sky_height):
        ratio = y / max(1, sky_height - 1)
        r = int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * ratio)
        g = int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * ratio)
        b = int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * ratio)
        for x in range(width):
            noise = random.randint(-5, 5)
            pixels[x, y] = (
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise)),
            )

    # Ground/landscape (bottom portion)
    ground_colors = [
        (34, 139, 34),   # forest green
        (139, 90, 43),   # brown earth
        (200, 200, 150), # sandy
        (60, 120, 60),   # dark green
        (180, 160, 120), # dry grass
    ]
    ground_color = ground_colors[seed % len(ground_colors)]

    for y in range(sky_height, height):
        ratio = (y - sky_height) / max(1, height - sky_height - 1)
        r = int(ground_color[0] * (1 - ratio * 0.3))
        g = int(ground_color[1] * (1 - ratio * 0.3))
        b = int(ground_color[2] * (1 - ratio * 0.3))
        for x in range(width):
            noise = random.randint(-10, 10)
            pixels[x, y] = (
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise)),
            )

    # Draw some shapes to make it look more realistic
    draw = ImageDraw.Draw(img)

    # Sun or moon
    sun_x = width // 4 + (seed % 3) * (width // 4)
    sun_y = height // 5
    sun_r = 40 + (seed % 20)
    sun_color = (255, 240, 80) if seed % 2 == 0 else (255, 255, 255)
    draw.ellipse([sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r], fill=sun_color)

    # Mountains / hills
    for i in range(3):
        mx = width * i // 3 + (seed % 50)
        my = sky_height - 80 - i * 30
        mw = 200 + (seed % 100)
        mh = 150 + (seed % 80)
        mountain_color = (80 + i * 20, 100 + i * 10, 60 + i * 15)
        draw.ellipse([mx - mw // 2, my, mx + mw // 2, my + mh * 2], fill=mountain_color)

    # Add title text as label (not a watermark)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except Exception:
        font = ImageFont.load_default()

    # Small label in top-left corner
    label_text = title
    draw.rectangle([5, 5, 250, 30], fill=(0, 0, 0, 180))
    draw.text((10, 8), label_text, fill=(255, 255, 255), font=font)

    return img


def create_initial():
    """Create initial state: raw JPEG images, empty processed dir, scripts dir."""

    # Create directory structure
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # Image filenames (10 realistic photo names)
    image_names = [
        "mountain_sunrise_01.jpg",
        "forest_path_02.jpg",
        "coastal_view_03.jpg",
        "desert_landscape_04.jpg",
        "city_skyline_05.jpg",
        "river_valley_06.jpg",
        "autumn_leaves_07.jpg",
        "snowy_peak_08.jpg",
        "tropical_beach_09.jpg",
        "meadow_flowers_10.jpg",
    ]

    # Varied image sizes (some large, some smaller, all will need resize consideration)
    image_sizes = [
        (2560, 1920),  # 4:3 landscape
        (1440, 2160),  # portrait - tall
        (3840, 2160),  # 4K landscape
        (2048, 1536),  # 4:3
        (1920, 1080),  # HD - already at max
        (2400, 1600),  # 3:2
        (1600, 2400),  # 3:2 portrait
        (3200, 2400),  # large landscape
        (1280, 960),   # smaller image
        (2560, 1440),  # 16:9 landscape
    ]

    print(f"Creating {len(image_names)} JPEG images in {RAW_DIR}...")

    for i, (name, size) in enumerate(zip(image_names, image_sizes)):
        filepath = os.path.join(RAW_DIR, name)
        # Use a short display label
        label = name.replace("_", " ").replace(".jpg", "").title()
        img = create_realistic_image(size[0], size[1], seed=i + 1, title=label)
        img.save(filepath, "JPEG", quality=92)
        print(f"  Created: {name} ({size[0]}x{size[1]})")

    # Verify created files
    created = os.listdir(RAW_DIR)
    print(f"\nRaw images directory: {RAW_DIR}")
    print(f"Files created: {len(created)}")
    for f in sorted(created):
        fpath = os.path.join(RAW_DIR, f)
        size_kb = os.path.getsize(fpath) // 1024
        print(f"  {f} ({size_kb} KB)")

    print(f"\nProcessed images directory (empty): {PROCESSED_DIR}")
    print(f"Scripts directory (empty): {SCRIPTS_DIR}")

    # GUI-ready startup: open file manager on raw images directory
    # This gives the agent context for where the images are
    launch_gui(f'nautilus "{RAW_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched file manager showing raw images with DISPLAY=:0")


create_initial()
