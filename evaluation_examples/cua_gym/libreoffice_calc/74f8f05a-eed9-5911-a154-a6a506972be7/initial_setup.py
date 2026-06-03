"""
Initial Setup: Create tree_sprite.png (pixel-art tree on pink background) on Desktop.
Task ID: osworld_multi_apps_gimp_vscode_015
Domain: gimp + vscode (multi-app)
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_015'
OUTPUT = f'{DESKTOP}/tree_sprite.png'


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


def create_tree_sprite():
    """Create a 128x128 pixel-art tree on a bright pink background."""
    os.makedirs(DESKTOP, exist_ok=True)

    # Canvas: 128x128, bright pink background (chroma-key pink)
    PINK = (255, 0, 255)   # bright magenta-pink
    DARK_GREEN = (34, 85, 34)
    MID_GREEN = (56, 130, 56)
    LIGHT_GREEN = (80, 175, 80)
    TRUNK_BROWN = (101, 67, 33)
    DARK_TRUNK = (80, 50, 20)

    img = Image.new("RGBA", (128, 128), color=PINK + (255,))
    draw = ImageDraw.Draw(img)

    # Draw trunk (center bottom)
    # Trunk: x=56-72, y=88-112
    draw.rectangle([56, 88, 72, 112], fill=TRUNK_BROWN + (255,))
    draw.rectangle([60, 90, 68, 112], fill=DARK_TRUNK + (255,))

    # Draw tree canopy: three overlapping triangles for a conical pine tree

    # Bottom tier (widest): triangle from (20,90) to (108,90) to (64,58)
    draw.polygon([(20, 90), (108, 90), (64, 58)], fill=DARK_GREEN + (255,))
    # Middle tier: triangle from (28,70) to (100,70) to (64,42)
    draw.polygon([(28, 70), (100, 70), (64, 42)], fill=MID_GREEN + (255,))
    # Top tier (narrowest): triangle from (38,52) to (90,52) to (64,24)
    draw.polygon([(38, 52), (90, 52), (64, 24)], fill=LIGHT_GREEN + (255,))

    # Add some pixel-art detail dots (lighter green highlights)
    HIGHLIGHT = (110, 210, 110)
    for pos in [(50, 65), (70, 60), (45, 75), (80, 72), (60, 45), (68, 38)]:
        draw.ellipse([pos[0]-2, pos[1]-2, pos[0]+2, pos[1]+2], fill=HIGHLIGHT + (255,))

    # Convert to RGB (no alpha) for the sprite — GIMP will use fuzzy select on the pink
    img_rgb = img.convert("RGB")
    img_rgb.save(OUTPUT)
    print(f"Created tree_sprite.png at {OUTPUT}")
    print(f"  Size: {img_rgb.size}")
    print(f"  Mode: {img_rgb.mode}")
    print(f"  Background color: {PINK} (bright pink for chroma-key removal)")


def main():
    create_tree_sprite()

    # Verify file created
    if os.path.isfile(OUTPUT):
        print(f"Verified: {OUTPUT} exists.")
    else:
        raise RuntimeError(f"Failed to create {OUTPUT}")

    # Open tree_sprite.png in GIMP for the agent
    launch_gui(f'gimp "{OUTPUT}"', delay_sec=3.0)
    print("GUI_READY: Launched GIMP with tree_sprite.png (DISPLAY=:0)")

    # Also open VSCode so agent can create extract_tree.py
    launch_gui(f'code "{DESKTOP}"', delay_sec=2.0)
    print("GUI_READY: Launched VSCode with Desktop folder (DISPLAY=:0)")


main()
