"""
Initial Setup: Create avatar.png (256x256 cartoon avatar on green background)
and a blank extract_avatar.py file on the Desktop.
Task ID: osworld_multi_apps_gimp_vscode_004
Domain: gimp + vscode (multi-app)
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw

DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_004'

AVATAR_PNG = f'{DESKTOP}/avatar.png'
EXTRACT_SCRIPT = f'{DESKTOP}/extract_avatar.py'


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


def create_avatar_image():
    """Create a 256x256 cartoon avatar on a solid green (#00FF00) background."""
    width, height = 256, 256
    green = (0, 255, 0)

    img = Image.new("RGBA", (width, height), color=green)
    draw = ImageDraw.Draw(img)

    # --- Draw a simple cartoon face (humanoid avatar) ---

    # Skin tone for face/body
    skin = (255, 200, 150, 255)
    dark_skin = (210, 160, 110, 255)
    shirt_color = (70, 130, 200, 255)
    hair_color = (60, 30, 10, 255)
    eye_white = (255, 255, 255, 255)
    pupil = (30, 30, 30, 255)
    mouth_color = (180, 60, 60, 255)

    # Body / torso (shirt)
    draw.rectangle([80, 168, 176, 240], fill=shirt_color)

    # Neck
    draw.rectangle([112, 152, 144, 170], fill=skin)

    # Head (face)
    draw.ellipse([72, 72, 184, 160], fill=skin)

    # Hair (top of head)
    draw.ellipse([72, 60, 184, 120], fill=hair_color)
    # Cover lower hair to show face
    draw.ellipse([78, 82, 178, 158], fill=skin)

    # Ears
    draw.ellipse([64, 100, 84, 126], fill=skin)
    draw.ellipse([172, 100, 192, 126], fill=skin)
    # Ear shadows
    draw.ellipse([68, 104, 80, 122], fill=dark_skin)
    draw.ellipse([176, 104, 188, 122], fill=dark_skin)

    # Eyes - left
    draw.ellipse([94, 100, 118, 118], fill=eye_white)
    draw.ellipse([101, 104, 113, 116], fill=pupil)
    # Eyes - right
    draw.ellipse([138, 100, 162, 118], fill=eye_white)
    draw.ellipse([145, 104, 157, 116], fill=pupil)

    # Eyebrows
    draw.arc([92, 92, 120, 106], start=200, end=340, fill=hair_color, width=3)
    draw.arc([136, 92, 164, 106], start=200, end=340, fill=hair_color, width=3)

    # Nose
    draw.ellipse([122, 118, 134, 130], fill=dark_skin)

    # Mouth (smile)
    draw.arc([106, 128, 150, 150], start=10, end=170, fill=mouth_color, width=3)

    # Arms
    draw.rectangle([48, 168, 82, 232], fill=shirt_color)
    draw.rectangle([174, 168, 208, 232], fill=shirt_color)

    # Hands
    draw.ellipse([42, 224, 82, 248], fill=skin)
    draw.ellipse([174, 224, 214, 248], fill=skin)

    # Save as RGBA PNG (green background visible as RGB)
    img_rgb = img.convert("RGB")
    # Re-paste with green background to ensure pure green BG
    final = Image.new("RGB", (width, height), (0, 255, 0))
    final.paste(img_rgb)
    final.save(AVATAR_PNG)
    print(f'Created: {AVATAR_PNG}')


def create_blank_script():
    """Create a blank (stub) extract_avatar.py file on the Desktop."""
    content = "# Write your background removal script here\n"
    os.makedirs(DESKTOP, exist_ok=True)
    with open(EXTRACT_SCRIPT, 'w') as f:
        f.write(content)
    print(f'Created: {EXTRACT_SCRIPT}')


def main():
    os.makedirs(DESKTOP, exist_ok=True)

    create_avatar_image()
    create_blank_script()

    # Open GIMP with avatar.png
    launch_gui(f'gimp "{AVATAR_PNG}"', delay_sec=3.0)

    # Open VSCode with extract_avatar.py
    launch_gui(f'code "{EXTRACT_SCRIPT}"', delay_sec=2.0)

    print('GUI_READY: launched GIMP with avatar.png and VSCode with extract_avatar.py (DISPLAY=:0)')


main()
