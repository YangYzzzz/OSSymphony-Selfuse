"""
Initial Setup: Divide timeline.png into three vertical slices and sort by blue channel
Task ID: osworld_multi_apps_gimp_os_027
Domain: multi_apps (gimp + os)
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_gimp_os_027'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/timeline.png'


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


def create_initial():
    os.makedirs(DESKTOP, exist_ok=True)

    # Create a 900x300 timeline image with three visually distinct sections
    # Each section is 300x300 pixels with varied colors
    # IMPORTANT: The three slices must have clearly different average blue channel values
    # so the sorting task is meaningful:
    #   Slice 0 (x: 0-299):   warm orange/red tones   → LOW blue  (~40)
    #   Slice 1 (x: 300-599): green/yellow tones       → MEDIUM blue (~90)
    #   Slice 2 (x: 600-899): cool blue/indigo tones   → HIGH blue (~200)

    img = Image.new("RGB", (900, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # --- Slice 0: warm orange/red timeline section (low blue) ---
    # Background: warm amber
    draw.rectangle([0, 0, 299, 299], fill=(220, 140, 40))
    # Decorative elements: dark red bars and orange highlights
    draw.rectangle([10, 40, 290, 80], fill=(180, 60, 20))
    draw.rectangle([10, 100, 290, 130], fill=(240, 160, 60))
    draw.rectangle([10, 150, 200, 180], fill=(200, 80, 30))
    draw.rectangle([10, 200, 250, 230], fill=(255, 170, 80))
    draw.rectangle([10, 250, 160, 280], fill=(185, 55, 15))
    # Timeline markers
    for i in range(5):
        x = 30 + i * 55
        draw.rectangle([x, 260, x + 20, 295], fill=(160, 50, 10))
    # Label area
    draw.rectangle([20, 10, 280, 35], fill=(250, 200, 100))
    draw.rectangle([30, 15, 130, 30], fill=(220, 120, 30))

    # --- Slice 1: green/teal timeline section (medium blue) ---
    # Background: medium green
    draw.rectangle([300, 0, 599, 299], fill=(60, 160, 90))
    # Decorative elements: dark green and teal accents
    draw.rectangle([310, 40, 590, 80], fill=(30, 110, 60))
    draw.rectangle([310, 100, 590, 130], fill=(80, 180, 120))
    draw.rectangle([310, 150, 500, 180], fill=(40, 130, 70))
    draw.rectangle([310, 200, 550, 230], fill=(100, 200, 140))
    draw.rectangle([310, 250, 460, 280], fill=(25, 100, 55))
    # Timeline markers
    for i in range(5):
        x = 330 + i * 55
        draw.rectangle([x, 260, x + 20, 295], fill=(20, 90, 50))
    # Label area
    draw.rectangle([320, 10, 580, 35], fill=(140, 220, 160))
    draw.rectangle([330, 15, 430, 30], fill=(50, 150, 80))

    # --- Slice 2: blue/indigo timeline section (high blue) ---
    # Background: deep blue
    draw.rectangle([600, 0, 899, 299], fill=(50, 100, 210))
    # Decorative elements: indigo and sky-blue accents
    draw.rectangle([610, 40, 890, 80], fill=(30, 60, 180))
    draw.rectangle([610, 100, 890, 130], fill=(80, 140, 240))
    draw.rectangle([610, 150, 800, 180], fill=(40, 80, 200))
    draw.rectangle([610, 200, 850, 230], fill=(100, 160, 255))
    draw.rectangle([610, 250, 760, 280], fill=(20, 50, 170))
    # Timeline markers
    for i in range(5):
        x = 630 + i * 55
        draw.rectangle([x, 260, x + 20, 295], fill=(15, 40, 160))
    # Label area
    draw.rectangle([620, 10, 880, 35], fill=(150, 190, 255))
    draw.rectangle([630, 15, 730, 30], fill=(40, 90, 220))

    # Add some diagonal gradient-like texture across the full width
    # using numpy for slight variations to make it look more realistic
    arr = np.array(img)

    # Add subtle noise to make it look less artificial (but not too much)
    rng = np.random.default_rng(seed=42)
    noise = rng.integers(-10, 11, size=arr.shape, dtype=np.int16)
    arr = np.clip(arr.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    img = Image.fromarray(arr)
    img.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # Verify the blue averages to confirm they're distinct enough
    w_slice = 300
    for i in range(3):
        sl = np.array(img)[0:300, i*w_slice:(i+1)*w_slice]
        avg_blue = float(sl[:, :, 2].mean())
        print(f'  Slice {i} avg blue: {avg_blue:.1f}')

    # GUI-ready startup: open a terminal so the agent can run Python commands
    # Also open a file manager on the Desktop so agent can see the file
    launch_gui('bash -c "DISPLAY=:0 gnome-terminal -- bash"', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')


create_initial()
