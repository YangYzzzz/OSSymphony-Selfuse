"""
Initial Setup: GIMP sprite sheet extraction + VSCode Python script task
Task ID: osworld_multi_apps_gimp_vscode_009
Domain: gimp + vscode (multi-app)

Creates:
  - /home/user/Desktop/enemies_sheet.png (128x128 RGBA sprite sheet, 2x2 grid of 64x64 sprites)
Opens:
  - GIMP with enemies_sheet.png
  - VSCode with Desktop folder
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_009'
SHEET_PATH = f'{WORKDIR}/enemies_sheet.png'

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

def draw_enemy_sprite(draw, ox, oy, style):
    """Draw a pixel-art style enemy at offset (ox, oy) in 64x64 space.
    style: 0-3 for four different enemy designs.
    """
    # Each sprite is unique with different colors and shapes
    if style == 0:
        # Top-left: Red goblin-like creature
        # Body
        draw.rectangle([ox+20, oy+24, ox+44, oy+50], fill=(200, 40, 40, 255))
        # Head
        draw.ellipse([ox+18, oy+10, ox+46, oy+34], fill=(220, 80, 60, 255))
        # Eyes
        draw.rectangle([ox+24, oy+16, ox+28, oy+22], fill=(255, 255, 50, 255))
        draw.rectangle([ox+36, oy+16, ox+40, oy+22], fill=(255, 255, 50, 255))
        # Pupils
        draw.rectangle([ox+25, oy+17, ox+27, oy+21], fill=(0, 0, 0, 255))
        draw.rectangle([ox+37, oy+17, ox+39, oy+21], fill=(0, 0, 0, 255))
        # Mouth
        draw.line([ox+26, oy+28, ox+38, oy+28], fill=(50, 0, 0, 255), width=2)
        # Arms
        draw.rectangle([ox+8, oy+28, ox+20, oy+38], fill=(200, 40, 40, 255))
        draw.rectangle([ox+44, oy+28, ox+56, oy+38], fill=(200, 40, 40, 255))
        # Legs
        draw.rectangle([ox+22, oy+50, ox+30, oy+60], fill=(170, 30, 30, 255))
        draw.rectangle([ox+34, oy+50, ox+42, oy+60], fill=(170, 30, 30, 255))
        # Outline
        draw.rectangle([ox+18, oy+10, ox+46, oy+34], outline=(100, 20, 20, 255), width=1)
        draw.rectangle([ox+20, oy+24, ox+44, oy+50], outline=(100, 20, 20, 255), width=1)

    elif style == 1:
        # Top-right: Blue slime creature
        # Body (rounded blob)
        draw.ellipse([ox+12, oy+20, ox+52, oy+56], fill=(60, 100, 220, 255))
        # Highlights
        draw.ellipse([ox+18, oy+22, ox+34, oy+36], fill=(120, 160, 255, 200))
        # Eyes
        draw.ellipse([ox+22, oy+26, ox+30, oy+36], fill=(255, 255, 255, 255))
        draw.ellipse([ox+34, oy+26, ox+42, oy+36], fill=(255, 255, 255, 255))
        draw.ellipse([ox+24, oy+28, ox+29, oy+34], fill=(10, 10, 80, 255))
        draw.ellipse([ox+36, oy+28, ox+41, oy+34], fill=(10, 10, 80, 255))
        # Smile
        draw.arc([ox+24, oy+36, ox+40, oy+48], start=0, end=180, fill=(10, 10, 80, 255), width=2)
        # Drip
        draw.polygon([(ox+28, oy+54), (ox+32, oy+62), (ox+36, oy+54)], fill=(60, 100, 220, 255))
        # Outline
        draw.ellipse([ox+12, oy+20, ox+52, oy+56], outline=(20, 50, 150, 255), width=1)

    elif style == 2:
        # Bottom-left: Green bat/ghost
        # Body
        draw.ellipse([ox+16, oy+16, ox+48, oy+44], fill=(50, 180, 80, 255))
        # Wings
        draw.polygon([(ox+16, oy+28), (ox+4, oy+14), (ox+16, oy+14)], fill=(30, 140, 60, 255))
        draw.polygon([(ox+48, oy+28), (ox+60, oy+14), (ox+48, oy+14)], fill=(30, 140, 60, 255))
        # Wing membrane
        draw.polygon([(ox+4, oy+14), (ox+10, oy+24), (ox+16, oy+24)], fill=(40, 160, 70, 200))
        draw.polygon([(ox+60, oy+14), (ox+54, oy+24), (ox+48, oy+24)], fill=(40, 160, 70, 200))
        # Eyes (angry slant)
        draw.polygon([(ox+22, oy+24), (ox+30, oy+22), (ox+30, oy+28)], fill=(255, 50, 50, 255))
        draw.polygon([(ox+42, oy+24), (ox+34, oy+22), (ox+34, oy+28)], fill=(255, 50, 50, 255))
        # Fangs
        draw.polygon([(ox+26, oy+36), (ox+29, oy+42), (ox+32, oy+36)], fill=(255, 255, 255, 255))
        draw.polygon([(ox+32, oy+36), (ox+35, oy+42), (ox+38, oy+36)], fill=(255, 255, 255, 255))
        # Tail
        draw.line([ox+32, oy+44, ox+32, oy+56], fill=(30, 140, 60, 255), width=3)
        draw.ellipse([ox+28, oy+54, ox+36, oy+62], fill=(50, 180, 80, 255))
        # Outline
        draw.ellipse([ox+16, oy+16, ox+48, oy+44], outline=(20, 80, 30, 255), width=1)

    elif style == 3:
        # Bottom-right: Purple wizard/mage enemy
        # Robe
        draw.polygon([(ox+20, oy+32), (ox+14, oy+58), (ox+50, oy+58), (ox+44, oy+32)],
                     fill=(140, 40, 180, 255))
        # Head
        draw.ellipse([ox+20, oy+14, ox+44, oy+38], fill=(230, 190, 150, 255))
        # Hat (cone)
        draw.polygon([(ox+32, oy+2), (ox+16, oy+18), (ox+48, oy+18)], fill=(80, 20, 120, 255))
        draw.line([ox+32, oy+2, ox+16, oy+18], fill=(60, 10, 90, 255), width=1)
        draw.line([ox+32, oy+2, ox+48, oy+18], fill=(60, 10, 90, 255), width=1)
        # Hat band
        draw.rectangle([ox+16, oy+16, ox+48, oy+20], fill=(200, 180, 40, 255))
        # Eyes (glowing)
        draw.ellipse([ox+24, oy+20, ox+30, oy+28], fill=(255, 220, 50, 255))
        draw.ellipse([ox+34, oy+20, ox+40, oy+28], fill=(255, 220, 50, 255))
        draw.ellipse([ox+26, oy+22, ox+29, oy+26], fill=(180, 100, 0, 255))
        draw.ellipse([ox+36, oy+22, ox+39, oy+26], fill=(180, 100, 0, 255))
        # Staff
        draw.line([ox+48, oy+32, ox+56, oy+58], fill=(100, 60, 20, 255), width=3)
        draw.ellipse([ox+44, oy+26, ox+56, oy+38], fill=(80, 200, 240, 255))
        draw.ellipse([ox+46, oy+28, ox+54, oy+36], fill=(200, 240, 255, 220))
        # Outline
        draw.ellipse([ox+20, oy+14, ox+44, oy+38], outline=(160, 110, 80, 255), width=1)


def create_initial():
    os.makedirs(WORKDIR, exist_ok=True)

    # Create 128x128 RGBA sprite sheet (2x2 grid of 64x64 sprites)
    sheet = Image.new("RGBA", (128, 128), (0, 0, 0, 0))  # transparent background
    draw = ImageDraw.Draw(sheet)

    # Draw 4 sprites in 2x2 grid
    # Sprite 0: top-left  (offset 0,0)
    # Sprite 1: top-right (offset 64,0)
    # Sprite 2: bottom-left (offset 0,64)
    # Sprite 3: bottom-right (offset 64,64)
    draw_enemy_sprite(draw, ox=0,  oy=0,  style=0)
    draw_enemy_sprite(draw, ox=64, oy=0,  style=1)
    draw_enemy_sprite(draw, ox=0,  oy=64, style=2)
    draw_enemy_sprite(draw, ox=64, oy=64, style=3)

    sheet.save(SHEET_PATH)
    print(f'Sprite sheet created: {SHEET_PATH}')
    print(f'Size: {sheet.size}')

    # Verify sheet dimensions
    check = Image.open(SHEET_PATH)
    assert check.size == (128, 128), f"Expected 128x128, got {check.size}"
    print(f'Verified: sheet is 128x128 RGBA with transparent background')

    # GUI-ready startup: open GIMP with the sprite sheet, then VSCode with Desktop
    launch_gui(f'gimp "{SHEET_PATH}"', delay_sec=3.0)
    launch_gui(f'code "{WORKDIR}"', delay_sec=2.0)
    print('GUI_READY: launched GIMP with enemies_sheet.png and VSCode with Desktop folder (DISPLAY=:0)')

create_initial()
