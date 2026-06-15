"""
Initial Setup: Sort images by aspect ratio into subfolders
Task ID: osworld_multi_apps_media_image_007
Domain: os + gimp (multi-app)
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_media_image_007'
PICTURES_DIR = f'{WORKDIR}/pictures'
UNSORTED_DIR = f'{PICTURES_DIR}/unsorted'


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


def draw_label(draw, text, width, height, color=(30, 30, 30)):
    """Draw a centered label on the image."""
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", max(12, min(width, height) // 10))
    except Exception:
        font = ImageFont.load_default()
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
    except AttributeError:
        tw, th = draw.textsize(text, font=font)
    x = (width - tw) // 2
    y = (height - th) // 2
    draw.text((x, y), text, fill=color, font=font)


def create_image(path, width, height, bg_color, label, accent_color):
    """Create a simple image with background, border, and label."""
    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    # Border
    border = max(4, min(width, height) // 20)
    draw.rectangle([border, border, width - border - 1, height - border - 1],
                   outline=accent_color, width=border)
    # Diagonal lines for texture
    step = max(width, height) // 8
    for i in range(-max(width, height), max(width, height) * 2, step):
        draw.line([(i, 0), (i + max(width, height), max(width, height))],
                  fill=accent_color, width=1)
    # Label
    draw_label(draw, label, width, height, color=(20, 20, 20))
    img.save(path, "PNG")
    print(f"  Created: {path} ({width}x{height})")


def create_initial():
    # Clean up existing state and rebuild
    import shutil
    if os.path.exists(PICTURES_DIR):
        shutil.rmtree(PICTURES_DIR)

    os.makedirs(UNSORTED_DIR, exist_ok=True)
    # Do NOT create wide/, tall/, square/ — those are the task targets

    print(f"Creating 12 images in {UNSORTED_DIR}...")

    # 5 WIDE images (width > height)
    wide_images = [
        ("landscape_meadow.png",    1280, 720,  (210, 235, 200), "Meadow Landscape",    (80, 140, 60)),
        ("panorama_cityview.png",   1920, 1080, (180, 200, 230), "City Panorama",       (50, 80, 150)),
        ("banner_sunset.png",       800,  300,  (255, 210, 170), "Sunset Banner",       (200, 100, 30)),
        ("wide_ocean_scene.png",    1600, 900,  (150, 190, 220), "Ocean Scene",         (30, 90, 160)),
        ("desktop_wallpaper.png",   2560, 1440, (220, 200, 240), "Desktop Wallpaper",   (100, 60, 180)),
    ]

    # 4 TALL images (height > width)
    tall_images = [
        ("portrait_person.png",     600,  900,  (240, 215, 200), "Portrait Shot",       (160, 80, 40)),
        ("tall_building.png",       400,  1200, (200, 210, 230), "Tall Building",       (60, 80, 140)),
        ("phone_screenshot.png",    1080, 1920, (225, 235, 245), "Phone Screenshot",    (40, 110, 180)),
        ("infographic_chart.png",   500,  1100, (245, 240, 210), "Infographic Chart",   (140, 120, 30)),
    ]

    # 3 SQUARE images (width == height)
    square_images = [
        ("instagram_post.png",      1080, 1080, (245, 220, 230), "Instagram Post",      (180, 60, 100)),
        ("profile_avatar.png",      512,  512,  (220, 240, 220), "Profile Avatar",      (50, 130, 70)),
        ("album_cover.png",         800,  800,  (230, 220, 250), "Album Cover Art",     (90, 50, 160)),
    ]

    all_images = wide_images + tall_images + square_images
    for filename, w, h, bg, label, accent in all_images:
        path = os.path.join(UNSORTED_DIR, filename)
        create_image(path, w, h, bg, label, accent)

    # Verify image count
    created = os.listdir(UNSORTED_DIR)
    print(f"\nTotal images in unsorted: {len(created)}")
    for f in sorted(created):
        img = Image.open(os.path.join(UNSORTED_DIR, f))
        w, h = img.size
        ratio_type = "wide" if w > h else ("tall" if h > w else "square")
        print(f"  {f}: {w}x{h} -> {ratio_type}")

    print(f"\nInitial state created: {UNSORTED_DIR}")
    print("Wide: 5, Tall: 4, Square: 3")
    print("Subdirectories wide/, tall/, square/ do NOT exist (task must create them).")

    # GUI-ready startup: open GIMP with a file from unsorted for initial inspection
    # Also open a file manager to show the unsorted directory
    time.sleep(1.0)
    launch_gui(f'nautilus "{UNSORTED_DIR}"', delay_sec=2.0)
    launch_gui(f'gimp "{UNSORTED_DIR}/landscape_meadow.png"', delay_sec=3.0)
    print("GUI_READY: launched nautilus and GIMP with DISPLAY=:0")


create_initial()
