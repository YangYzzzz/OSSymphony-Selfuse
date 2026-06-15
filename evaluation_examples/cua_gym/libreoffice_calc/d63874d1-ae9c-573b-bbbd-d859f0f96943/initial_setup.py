"""
Initial Setup: cityscape.png on Desktop for GIMP warm color processing task
Task ID: osworld_multi_apps_gimp_os_025
Domain: gimp + os (multi-app)
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw
import numpy as np

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_os_025'
OUTPUT = f'{WORKDIR}/cityscape.png'

# Image dimensions specified in task context
IMG_WIDTH = 1500
IMG_HEIGHT = 600


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


def create_cityscape():
    """Create a realistic-looking city skyline photo (1500x600)."""
    img = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), color=(135, 180, 220))  # sky blue
    draw = ImageDraw.Draw(img)
    pixels = np.array(img, dtype=np.float32)

    # --- Sky gradient (top portion) ---
    for y in range(IMG_HEIGHT // 2):
        factor = 1.0 - (y / (IMG_HEIGHT // 2)) * 0.3
        pixels[y, :, 0] = np.clip(135 * factor + 40 * (1 - factor), 0, 255)  # R
        pixels[y, :, 1] = np.clip(180 * factor + 80 * (1 - factor), 0, 255)  # G
        pixels[y, :, 2] = np.clip(220 * factor + 140 * (1 - factor), 0, 255) # B

    img = Image.fromarray(pixels.astype(np.uint8))
    draw = ImageDraw.Draw(img)

    # --- Ground / road ---
    draw.rectangle([0, IMG_HEIGHT - 80, IMG_WIDTH, IMG_HEIGHT], fill=(60, 60, 65))
    # Road markings
    for x in range(0, IMG_WIDTH, 80):
        draw.rectangle([x + 20, IMG_HEIGHT - 45, x + 60, IMG_HEIGHT - 35], fill=(220, 220, 180))

    # --- Building definitions: (x, y_top, width, height, color) ---
    buildings = [
        # Left district - low-rise commercial
        (10,   300, 80,  270, (80,  85,  95)),
        (95,   320, 60,  250, (90,  92, 100)),
        (160,  280, 100, 290, (75,  80,  90)),
        (265,  260, 70,  310, (85,  88,  98)),
        (340,  240, 50,  330, (95,  95, 105)),
        # Center-left - mid-rise
        (395,  200, 90,  370, (70,  75,  85)),
        (490,  180, 110, 390, (80,  82,  92)),
        (605,  150, 80,  420, (65,  70,  82)),
        # Center - skyscrapers
        (690,   80, 100, 490, (55,  60,  75)),
        (795,   50, 120, 520, (60,  62,  78)),
        (920,   90, 90,  480, (65,  68,  80)),
        # Center-right - mid-rise
        (1015, 160, 100, 410, (70,  73,  85)),
        (1120, 190, 80,  380, (75,  78,  90)),
        (1205, 220, 70,  350, (80,  82,  95)),
        # Right district - low-rise
        (1280, 260, 90,  310, (85,  88, 100)),
        (1375, 290, 70,  280, (90,  92, 105)),
        (1450, 310, 45,  260, (95,  95, 108)),
    ]

    for (bx, by, bw, bh, bcolor) in buildings:
        # Building body
        draw.rectangle([bx, by, bx + bw, IMG_HEIGHT - 80], fill=bcolor)
        # Windows (slightly brighter yellow-white)
        win_color = (min(bcolor[0] + 40, 255), min(bcolor[1] + 35, 255), min(bcolor[2] + 10, 255))
        dark_win  = (max(bcolor[0] - 10, 0),  max(bcolor[1] - 10, 0),  max(bcolor[2] - 5, 0))
        win_w, win_h, gap_x, gap_y = 10, 12, 18, 18
        start_y = by + 15
        start_x = bx + 8
        for wy in range(start_y, IMG_HEIGHT - 100, gap_y + win_h):
            for wx in range(start_x, bx + bw - 8, gap_x + win_w):
                # ~60% windows lit
                import random
                random.seed(bx * 1000 + wx * 100 + wy)
                col = win_color if random.random() > 0.4 else dark_win
                draw.rectangle([wx, wy, wx + win_w, wy + win_h], fill=col)

    # --- Street lights ---
    for x in range(50, IMG_WIDTH, 200):
        draw.line([(x, IMG_HEIGHT - 80), (x, IMG_HEIGHT - 160)], fill=(180, 175, 160), width=3)
        draw.ellipse([x - 10, IMG_HEIGHT - 175, x + 10, IMG_HEIGHT - 155], fill=(240, 235, 200))

    # --- Some foreground elements (trees / cars) ---
    tree_positions = [130, 330, 530, 730, 930, 1130, 1330]
    for tx in tree_positions:
        # Trunk
        draw.rectangle([tx, IMG_HEIGHT - 120, tx + 8, IMG_HEIGHT - 80], fill=(90, 60, 40))
        # Canopy
        draw.ellipse([tx - 18, IMG_HEIGHT - 160, tx + 26, IMG_HEIGHT - 110], fill=(40, 90, 45))

    # A parked car (left side)
    draw.rectangle([200, IMG_HEIGHT - 95, 280, IMG_HEIGHT - 82], fill=(180, 40, 40))
    draw.ellipse([210, IMG_HEIGHT - 82, 230, IMG_HEIGHT - 70], fill=(30, 30, 30))
    draw.ellipse([255, IMG_HEIGHT - 82, 275, IMG_HEIGHT - 70], fill=(30, 30, 30))

    # Reflection on road surface
    road_arr = np.array(img, dtype=np.float32)
    for y in range(IMG_HEIGHT - 78, IMG_HEIGHT - 50):
        road_arr[y, :, 0] = np.clip(road_arr[y, :, 0] * 1.1, 0, 255)
        road_arr[y, :, 1] = np.clip(road_arr[y, :, 1] * 1.05, 0, 255)
    img = Image.fromarray(road_arr.astype(np.uint8))

    # Slight atmospheric haze in the distance (desaturate slightly by blending with gray)
    haze = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), (160, 170, 185))
    haze_arr = np.array(haze, dtype=np.float32)
    img_arr  = np.array(img,  dtype=np.float32)
    haze_factor = np.zeros((IMG_HEIGHT, IMG_WIDTH), dtype=np.float32)
    for y in range(IMG_HEIGHT // 2):
        haze_factor[y, :] = 0.15 * (1.0 - y / (IMG_HEIGHT // 2))
    for c in range(3):
        img_arr[:, :, c] = img_arr[:, :, c] * (1 - haze_factor) + haze_arr[:, :, c] * haze_factor
    img = Image.fromarray(img_arr.clip(0, 255).astype(np.uint8))

    img.save(OUTPUT, format='PNG')
    print(f'Initial cityscape created: {OUTPUT}')
    print(f'Image size: {img.size}')


def create_initial():
    os.makedirs(WORKDIR, exist_ok=True)

    # Make sure no warm-processed version exists (pre-clean)
    warm_path = f'{WORKDIR}/cityscape_warm.png'
    if os.path.exists(warm_path):
        os.remove(warm_path)
        print(f'Removed pre-existing {warm_path}')

    create_cityscape()

    # GUI-ready startup: open GIMP with the cityscape image and a terminal
    launch_gui(f'gimp "{OUTPUT}"', delay_sec=3.0)
    launch_gui('gnome-terminal', delay_sec=1.5)
    print('GUI_READY: launched GIMP and terminal with DISPLAY=:0')


create_initial()
