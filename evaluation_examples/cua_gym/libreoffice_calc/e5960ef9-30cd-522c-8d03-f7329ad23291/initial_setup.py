"""
Initial Setup: Open landscape.jpg in GIMP, apply saturation +40, export as landscape_vivid.jpg, set as wallpaper
Task ID: osworld_multi_apps_media_image_003
Domain: gimp + os (multi-app)
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw
import numpy as np

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'osworld_multi_apps_media_image_003'
PICTURES_DIR = f'{WORKDIR}/pictures'
INITIAL_IMAGE = f'{PICTURES_DIR}/landscape.jpg'


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


def create_landscape_image(path: str):
    """Create a realistic-looking landscape photograph using Pillow."""
    width, height = 1280, 720
    img = Image.new("RGB", (width, height))
    pixels = np.zeros((height, width, 3), dtype=np.uint8)

    # Sky gradient (upper 45%): light blue to deeper blue
    sky_height = int(height * 0.45)
    for y in range(sky_height):
        t = y / sky_height
        r = int(135 + (70 - 135) * t)
        g = int(206 + (130 - 206) * t)
        b = int(235 + (180 - 235) * t)
        pixels[y, :] = [r, g, b]

    # Mountain range (middle 20%): purple-grey mountains
    mountain_start = sky_height
    mountain_height = int(height * 0.20)
    for x in range(width):
        # Create irregular mountain silhouette
        peak = mountain_start + int(
            mountain_height * 0.3 * abs(np.sin(x / 120.0)) +
            mountain_height * 0.2 * abs(np.sin(x / 60.0 + 1.3)) +
            mountain_height * 0.1 * abs(np.sin(x / 30.0 + 0.7))
        )
        for y in range(mountain_start, mountain_start + mountain_height):
            if y >= peak:
                # Mountain body: warm grey-purple
                shade = max(0, 255 - int((y - peak) * 2.5))
                r = int(100 + shade * 0.3)
                g = int(90 + shade * 0.28)
                b = int(110 + shade * 0.32)
                pixels[y, x] = [
                    min(255, r),
                    min(255, g),
                    min(255, b)
                ]
            else:
                # Still sky at mountain top
                t = y / sky_height
                r = int(135 + (70 - 135) * min(t, 1.0))
                g = int(206 + (130 - 206) * min(t, 1.0))
                b = int(235 + (180 - 235) * min(t, 1.0))
                pixels[y, x] = [r, g, b]

    # Green hillside / meadow (next 20%)
    meadow_start = mountain_start + mountain_height
    meadow_height = int(height * 0.20)
    for y in range(meadow_start, meadow_start + meadow_height):
        t = (y - meadow_start) / meadow_height
        for x in range(width):
            # Varied green with slight undulation
            variation = int(10 * np.sin(x / 80.0) + 5 * np.cos(x / 40.0))
            r = int(60 + t * 30 + variation // 3)
            g = int(110 + t * 40 + variation)
            b = int(40 + t * 20)
            pixels[y, x] = [
                max(0, min(255, r)),
                max(0, min(255, g)),
                max(0, min(255, b))
            ]

    # River/lake reflection (thin band ~5%)
    river_start = meadow_start + meadow_height
    river_height = int(height * 0.05)
    for y in range(river_start, river_start + river_height):
        for x in range(width):
            # Reflective blue water
            ripple = int(8 * np.sin(x / 25.0 + y / 5.0))
            pixels[y, x] = [
                max(0, min(255, 70 + ripple)),
                max(0, min(255, 130 + ripple)),
                max(0, min(255, 170 + ripple))
            ]

    # Foreground (bottom ~10%): darker grass/earth
    fg_start = river_start + river_height
    for y in range(fg_start, height):
        t = (y - fg_start) / (height - fg_start)
        for x in range(width):
            variation = int(8 * np.sin(x / 50.0))
            r = int(45 + t * 20 + variation)
            g = int(80 + t * 25 + variation)
            b = int(30 + t * 10)
            pixels[y, x] = [
                max(0, min(255, r)),
                max(0, min(255, g)),
                max(0, min(255, b))
            ]

    # Add a few white clouds in the sky
    draw_img = Image.fromarray(pixels)
    draw = ImageDraw.Draw(draw_img)
    # Cloud 1 (left)
    for cx, cy, rx, ry in [
        (220, 90, 90, 30), (260, 75, 70, 25), (300, 85, 80, 28)
    ]:
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                     fill=(240, 243, 248))
    # Cloud 2 (right)
    for cx, cy, rx, ry in [
        (900, 110, 80, 28), (940, 95, 65, 22), (975, 108, 72, 26)
    ]:
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                     fill=(238, 241, 246))

    draw_img.save(path, 'JPEG', quality=92)
    print(f'Landscape image created: {path}')


def create_initial():
    # Create pictures directory
    os.makedirs(PICTURES_DIR, exist_ok=True)

    # Create the initial landscape.jpg
    create_landscape_image(INITIAL_IMAGE)

    # Verify the file was created
    assert os.path.isfile(INITIAL_IMAGE), f"Failed to create {INITIAL_IMAGE}"
    file_size = os.path.getsize(INITIAL_IMAGE)
    print(f'File size: {file_size} bytes')

    # GUI-ready startup: open landscape.jpg in GIMP
    launch_gui(f'gimp "{INITIAL_IMAGE}"', delay_sec=3.0)
    print('GUI_READY: launched GIMP with landscape.jpg using DISPLAY=:0')


create_initial()
