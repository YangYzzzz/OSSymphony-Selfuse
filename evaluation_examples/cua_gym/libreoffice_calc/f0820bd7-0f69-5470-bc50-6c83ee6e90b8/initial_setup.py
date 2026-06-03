"""
Initial Setup: Create logo_v2.png on the Desktop for GIMP + VSCode drop shadow task.
Task ID: osworld_multi_apps_gimp_vscode_013
Domain: multi_apps (gimp + vscode)
"""

import os
import shlex
import subprocess
import time
import math

# PIL imports — these run on the VM
from PIL import Image, ImageDraw, ImageFont

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_gimp_vscode_013'
DESKTOP = f'{WORKDIR}/Desktop'
LOGO_PATH = f'{DESKTOP}/logo_v2.png'


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


def create_logo():
    """Create a realistic brand logo (400x200) on a white background."""
    os.makedirs(DESKTOP, exist_ok=True)

    # Create a 400x200 white canvas
    img = Image.new("RGB", (400, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Draw a stylized logo mark: a bold hexagon with interior star
    # Hexagon centered at (100, 100), radius 70
    cx, cy, r = 100, 100, 70
    hex_pts = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        hex_pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(hex_pts, fill=(41, 98, 255), outline=(20, 50, 180))

    # Inner star / accent inside hex — white so it shows up as logo mark
    inner_r = 35
    star_pts = []
    for i in range(10):
        angle = math.radians(36 * i - 90)
        rr = inner_r if i % 2 == 0 else inner_r * 0.45
        star_pts.append((cx + rr * math.cos(angle), cy + rr * math.sin(angle)))
    draw.polygon(star_pts, fill=(255, 255, 255))

    # Draw brand name text to the right of the hex icon
    # Use a large bold-style font; fall back to default if truetype not available
    font_path_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    font_large = None
    font_small = None
    for fp in font_path_candidates:
        if os.path.isfile(fp):
            try:
                font_large = ImageFont.truetype(fp, 42)
                font_small = ImageFont.truetype(fp, 18)
                break
            except Exception:
                continue

    if font_large is None:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Company name — "NEXOVA"
    draw.text((190, 60), "NEXOVA", fill=(30, 30, 50), font=font_large)
    # Tagline below
    draw.text((192, 115), "Creative Solutions", fill=(100, 100, 120), font=font_small)

    # Thin separator line under tagline
    draw.line([(190, 140), (390, 140)], fill=(200, 200, 215), width=2)

    # Small footer text
    draw.text((192, 150), "www.nexova.io", fill=(150, 150, 170), font=font_small)

    img.save(LOGO_PATH, "PNG")
    print(f"Initial logo created: {LOGO_PATH}")


def create_initial():
    create_logo()

    # Ensure no pre-existing output files (idempotent cleanup)
    for fname in ['logo_shadow_gimp.png', 'logo_shadow_code.png', 'logo_shadow.py']:
        fpath = os.path.join(DESKTOP, fname)
        if os.path.exists(fpath):
            os.remove(fpath)
            print(f"Removed pre-existing: {fpath}")

    # GUI-ready startup: open GIMP with the logo, and VSCode on the Desktop folder
    launch_gui(f'gimp "{LOGO_PATH}"', delay_sec=3.0)
    launch_gui(f'code "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched GIMP and VSCode with DISPLAY=:0')


create_initial()
