"""
Initial Setup: Create placeholder images and open blank LibreOffice Impress
Task ID: impress_wf_004
Domain: libreoffice_impress
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
TASK_ID = 'impress_wf_004'

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

def create_placeholder_images():
    """Create two realistic-looking 800x600 placeholder JPEGs on the Desktop."""
    from PIL import Image, ImageDraw, ImageFont

    os.makedirs(DESKTOP, exist_ok=True)

    # before_office.jpg - warm beige tones suggesting an old office
    img_before = Image.new('RGB', (800, 600), (210, 195, 170))
    draw = ImageDraw.Draw(img_before)
    # Draw some rectangles to simulate furniture/desks
    draw.rectangle([50, 300, 350, 550], fill=(160, 140, 110))   # old desk
    draw.rectangle([400, 250, 750, 550], fill=(150, 130, 100))  # old shelf
    draw.rectangle([100, 100, 300, 280], fill=(180, 170, 150))  # window
    draw.rectangle([500, 50, 700, 230], fill=(190, 180, 160))   # whiteboard
    # Add some lines for detail
    draw.line([(0, 550), (800, 550)], fill=(120, 100, 80), width=3)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except Exception:
        font = ImageFont.load_default()
    draw.text((300, 570), "Old Office", fill=(100, 80, 60), font=font)
    img_before.save(f'{DESKTOP}/before_office.jpg', 'JPEG', quality=85)
    print(f'Created: {DESKTOP}/before_office.jpg')

    # after_office.jpg - bright modern tones suggesting a renovated office
    img_after = Image.new('RGB', (800, 600), (230, 240, 250))
    draw = ImageDraw.Draw(img_after)
    # Modern furniture shapes
    draw.rectangle([50, 300, 350, 550], fill=(80, 130, 190))    # modern desk
    draw.rectangle([400, 250, 750, 550], fill=(100, 160, 210))  # modern shelf
    draw.rectangle([100, 100, 300, 280], fill=(200, 220, 240))  # large window
    draw.rectangle([500, 50, 700, 230], fill=(240, 240, 240))   # monitor
    draw.rectangle([520, 70, 680, 210], fill=(50, 50, 50))      # screen
    draw.line([(0, 550), (800, 550)], fill=(180, 190, 200), width=3)
    draw.text((280, 570), "Renovated Office", fill=(60, 90, 130), font=font)
    img_after.save(f'{DESKTOP}/after_office.jpg', 'JPEG', quality=85)
    print(f'Created: {DESKTOP}/after_office.jpg')

def create_initial():
    create_placeholder_images()

    # Open LibreOffice Impress with a blank presentation
    launch_gui('libreoffice --impress', delay_sec=3.0)
    print('GUI_READY: LibreOffice Impress launched with blank presentation')

create_initial()
