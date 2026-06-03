"""
Initial Setup: Create robot_sprite.png for pixel-art background removal task
Task ID: osworld_multi_apps_gimp_vscode_012
Domain: gimp + vscode (multi-app)
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw
import numpy as np

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_gimp_vscode_012'
DESKTOP = f'{WORKDIR}/Desktop'
SPRITE_PATH = f'{DESKTOP}/robot_sprite.png'


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


def create_robot_sprite():
    """
    Create a 96x96 pixel-art robot on a sky-blue background.
    Sky-blue background: RGB(135, 206, 235)
    Robot is drawn in grays, dark gray, and accent colors.
    """
    WIDTH, HEIGHT = 96, 96
    BG_COLOR = (135, 206, 235)  # sky blue

    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # --- Robot body (center ~48x48 area, offset from top) ---
    # Colors
    ROBOT_GRAY   = (160, 160, 175)
    DARK_GRAY    = ( 80,  80,  95)
    LIGHT_GRAY   = (200, 200, 215)
    ACCENT_RED   = (220,  60,  60)
    ACCENT_BLUE  = ( 60, 100, 220)
    EYE_GLOW     = ( 60, 240, 180)
    BLACK        = ( 20,  20,  20)

    # Head: 28x22, centered at x=34..62, y=14..36
    head_x0, head_y0, head_x1, head_y1 = 34, 14, 62, 36
    draw.rectangle([head_x0, head_y0, head_x1, head_y1], fill=ROBOT_GRAY, outline=DARK_GRAY)

    # Antenna: 1px wide, 5px tall, centered
    draw.rectangle([47, 9, 49, 14], fill=DARK_GRAY)
    draw.rectangle([46, 7, 50, 10], fill=ACCENT_RED)

    # Eyes: two 5x5 glowing squares
    draw.rectangle([38, 19, 43, 24], fill=EYE_GLOW, outline=BLACK)
    draw.rectangle([53, 19, 58, 24], fill=EYE_GLOW, outline=BLACK)

    # Mouth/speaker: 3 small dark rectangles
    draw.rectangle([40, 29, 43, 31], fill=DARK_GRAY)
    draw.rectangle([46, 29, 50, 31], fill=DARK_GRAY)
    draw.rectangle([53, 29, 56, 31], fill=DARK_GRAY)

    # Body: 30x26, centered at x=33..63, y=37..63
    body_x0, body_y0, body_x1, body_y1 = 33, 37, 63, 63
    draw.rectangle([body_x0, body_y0, body_x1, body_y1], fill=LIGHT_GRAY, outline=DARK_GRAY)

    # Chest panel
    draw.rectangle([38, 41, 58, 58], fill=ROBOT_GRAY, outline=DARK_GRAY)
    # Chest lights
    draw.rectangle([40, 43, 44, 47], fill=ACCENT_RED)
    draw.rectangle([46, 43, 50, 47], fill=ACCENT_BLUE)
    draw.rectangle([52, 43, 56, 47], fill=ACCENT_RED)
    # Chest grille
    for row in range(3):
        draw.rectangle([40, 50+row*2, 56, 50+row*2+1], fill=DARK_GRAY)

    # Shoulders
    draw.rectangle([24, 38, 33, 55], fill=ROBOT_GRAY, outline=DARK_GRAY)  # left shoulder
    draw.rectangle([63, 38, 72, 55], fill=ROBOT_GRAY, outline=DARK_GRAY)  # right shoulder

    # Arms: 6x16, hanging from shoulders
    draw.rectangle([26, 55, 32, 71], fill=LIGHT_GRAY, outline=DARK_GRAY)  # left arm
    draw.rectangle([64, 55, 70, 71], fill=LIGHT_GRAY, outline=DARK_GRAY)  # right arm

    # Hands
    draw.rectangle([25, 71, 33, 76], fill=ROBOT_GRAY, outline=DARK_GRAY)
    draw.rectangle([63, 71, 71, 76], fill=ROBOT_GRAY, outline=DARK_GRAY)

    # Legs: 10x16 each
    draw.rectangle([35, 64, 45, 80], fill=LIGHT_GRAY, outline=DARK_GRAY)  # left leg
    draw.rectangle([51, 64, 61, 80], fill=LIGHT_GRAY, outline=DARK_GRAY)  # right leg

    # Feet: slightly wider, 2px shorter
    draw.rectangle([33, 80, 47, 86], fill=ROBOT_GRAY, outline=DARK_GRAY)
    draw.rectangle([49, 80, 63, 86], fill=ROBOT_GRAY, outline=DARK_GRAY)

    return img


def create_initial():
    # Make sure Desktop exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Create the robot sprite
    img = create_robot_sprite()
    img.save(SPRITE_PATH)
    print(f'Created: {SPRITE_PATH}')

    # Ensure no output files exist yet (pre-task state)
    for f in ['robot_gimp.png', 'robot_code.png', 'robot_extract.py']:
        p = f'{DESKTOP}/{f}'
        if os.path.exists(p):
            os.remove(p)
            print(f'Removed pre-existing: {p}')

    # GUI-ready: Open GIMP with the sprite
    launch_gui(f'gimp "{SPRITE_PATH}"', delay_sec=3.0)
    print('GUI_READY: launched GIMP with robot_sprite.png on DISPLAY=:0')


create_initial()
