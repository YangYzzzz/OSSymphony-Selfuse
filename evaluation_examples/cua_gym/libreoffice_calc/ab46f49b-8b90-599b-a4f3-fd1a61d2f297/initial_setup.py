"""
Initial Setup: Create map_sprite.png with three map pin icons on light-grey background
Task ID: osworld_multi_apps_gimp_vscode_007
Domain: gimp + vscode (multi-app)
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_gimp_vscode_007'
DESKTOP = '/home/user/Desktop'
OUTPUT = f'{DESKTOP}/map_sprite.png'


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


def draw_map_pin(draw, cx, cy, radius=28, pin_color=(220, 60, 60), outline_color=(160, 30, 30)):
    """Draw a map pin / location marker at center (cx, cy).

    A map pin consists of:
    - A teardrop / circle-with-point shape pointing downward
    - A small white inner circle (hole)
    """
    # Main pin body: circle at top
    top_r = radius
    top_cx = cx
    top_cy = cy - radius // 2

    # Draw the circle (head of pin)
    draw.ellipse(
        [top_cx - top_r, top_cy - top_r, top_cx + top_r, top_cy + top_r],
        fill=pin_color,
        outline=outline_color,
        width=2
    )

    # Draw the pointy bottom: triangle pointing downward
    point_tip_y = cy + radius + radius // 2
    left_x = cx - top_r // 2
    right_x = cx + top_r // 2
    start_y = top_cy + top_r - 4

    draw.polygon(
        [(left_x, start_y), (right_x, start_y), (cx, point_tip_y)],
        fill=pin_color,
        outline=outline_color,
    )

    # Inner white circle (hole in center of pin head)
    inner_r = radius // 3
    draw.ellipse(
        [top_cx - inner_r, top_cy - inner_r, top_cx + inner_r, top_cy + inner_r],
        fill=(255, 255, 255),
        outline=outline_color,
        width=1
    )


def create_initial():
    os.makedirs(DESKTOP, exist_ok=True)

    # Image dimensions: wide enough for 3 pins side by side
    width = 300
    height = 120
    bg_color = (210, 210, 210)  # light grey background

    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw three map pins at evenly spaced horizontal positions
    pin_positions = [
        (50, 55),   # left pin
        (150, 55),  # center pin
        (250, 55),  # right pin
    ]

    pin_colors = [
        ((220, 60, 60), (160, 30, 30)),    # red
        ((60, 140, 220), (30, 90, 160)),   # blue
        ((60, 200, 100), (30, 140, 60)),   # green
    ]

    for (cx, cy), (fill, outline) in zip(pin_positions, pin_colors):
        draw_map_pin(draw, cx, cy, radius=28, pin_color=fill, outline_color=outline)

    img.save(OUTPUT, "PNG")
    print(f'Initial file created: {OUTPUT}')

    # Ensure no leftover output files from previous runs
    for leftover in [
        f'{DESKTOP}/map_sprite_gimp.png',
        f'{DESKTOP}/map_sprite_code.png',
        f'{DESKTOP}/clean_markers.py',
    ]:
        if os.path.exists(leftover):
            os.remove(leftover)
            print(f'Removed leftover: {leftover}')

    # GUI-ready startup: open GIMP with the map_sprite.png file
    launch_gui(f'gimp "{OUTPUT}"', delay_sec=3.0)
    # Also open VSCode on the Desktop folder so the agent can write the Python script
    launch_gui(f'code "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched GIMP and VSCode with DISPLAY=:0')


create_initial()
