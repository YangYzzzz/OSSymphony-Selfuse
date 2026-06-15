"""
Initial Setup: UI Elements strip image for GIMP/VSCode extraction task
Task ID: osworld_multi_apps_gimp_vscode_010
Domain: gimp + vscode (multi-app)

Creates ui_elements.png on the Desktop: a 480x30 pixel horizontal strip
containing 6 UI button states (normal, hover, pressed, disabled, focused, selected)
each 80x30 pixels on a white background.

The agent must:
1. Open ui_elements.png in GIMP, remove background, slice into 6 button_N.png files
2. Write extract_ui.py in VSCode to automate the same slicing → button_N_code.png
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_gimp_vscode_010'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/ui_elements.png'


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

    # Strip dimensions: 6 buttons × 80px wide, 30px tall
    BUTTON_W = 80
    BUTTON_H = 30
    NUM_BUTTONS = 6
    STRIP_W = BUTTON_W * NUM_BUTTONS
    STRIP_H = BUTTON_H

    # Create white background strip
    img = Image.new("RGB", (STRIP_W, STRIP_H), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Define 6 button state styles
    # Each button: (label, fill_color, outline_color, text_color)
    button_styles = [
        # normal - standard blue button
        ("Normal",    (70,  130, 180), (50,  100, 150), (255, 255, 255)),
        # hover - lighter blue
        ("Hover",     (100, 160, 210), (70,  130, 180), (255, 255, 255)),
        # pressed - dark blue / pushed in
        ("Pressed",   (40,   80, 120), (20,   50,  90), (200, 220, 255)),
        # disabled - gray
        ("Disabled",  (180, 180, 180), (140, 140, 140), (220, 220, 220)),
        # focused - blue with yellow border accent
        ("Focused",   (70,  130, 180), (255, 200,   0), (255, 255, 255)),
        # selected - teal/green highlight
        ("Selected",  (46,  160, 120), (30,  120,  90), (255, 255, 255)),
    ]

    for i, (label, fill, outline, text_color) in enumerate(button_styles):
        x0 = i * BUTTON_W
        x1 = x0 + BUTTON_W - 1
        y0 = 0
        y1 = BUTTON_H - 1

        # Fill button rectangle
        draw.rectangle([x0 + 2, y0 + 2, x1 - 2, y1 - 2], fill=fill)
        # Draw outline border
        draw.rectangle([x0 + 2, y0 + 2, x1 - 2, y1 - 2], outline=outline, width=2)

        # Draw simple text label (small characters using lines, no font needed)
        # Just draw a centered darker mark to distinguish each state
        center_x = x0 + BUTTON_W // 2
        center_y = y0 + BUTTON_H // 2

        # Draw a small indicator circle in center to distinguish buttons
        r = 4
        draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r],
                     fill=text_color, outline=outline)

        # Draw state number for easy visual identification
        # Use a simple digit drawn with lines
        digit = str(i + 1)
        draw.text((center_x - 3, center_y - 6), digit, fill=text_color)

    img.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print(f'Strip dimensions: {STRIP_W}x{STRIP_H} px, 6 buttons x 80px each')

    # Verify file was created
    if os.path.isfile(OUTPUT):
        size = os.path.getsize(OUTPUT)
        print(f'File size: {size} bytes')
    else:
        print('ERROR: File was not created!')
        return

    # GUI-ready startup: open GIMP with the ui_elements.png file
    # Also open VSCode for the script writing part
    launch_gui(f'gimp "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched GIMP with ui_elements.png using DISPLAY=:0')

    # Give GIMP time to load, then launch VSCode for script editing
    launch_gui(f'code "{WORKDIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with /home/user workspace using DISPLAY=:0')


create_initial()
