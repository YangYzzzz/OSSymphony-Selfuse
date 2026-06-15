"""
Initial Setup: Create mosaic.png on the Desktop — a 900x900 image with a 3x3 grid
of 9 distinct colored tiles arranged in NON-hue order (shuffled).
Task ID: osworld_multi_apps_gimp_os_021
Domain: gimp / os
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_os_021'
OUTPUT = f'{WORKDIR}/mosaic.png'

TILE_SIZE = 300   # Each tile is 300x300 pixels
GRID = 3          # 3x3 grid → 900x900 total


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
    os.makedirs(WORKDIR, exist_ok=True)

    # 9 vivid, distinct colors covering the hue spectrum WITHOUT wrap-around ambiguity.
    # All hues fall in [0°, 290°], so sorting descending = unambiguous cool-to-warm.
    # Arranged in a SHUFFLED (non-hue-sorted) order so the agent must reorder them.
    #
    # Shuffled layout (grid positions 0..8):
    #   Pos 0: Green       hue~120°
    #   Pos 1: Deep-Blue   hue~240°
    #   Pos 2: Red         hue~0°
    #   Pos 3: Violet      hue~287°
    #   Pos 4: Cyan        hue~180°
    #   Pos 5: Orange      hue~33°
    #   Pos 6: Indigo      hue~268°
    #   Pos 7: Blue        hue~215°
    #   Pos 8: Yellow      hue~54°
    tiles_colors_shuffled = [
        ( 30, 180,  30),  # Pos 0 → Green       hue ≈ 120°
        ( 50,  50, 220),  # Pos 1 → Deep-Blue   hue ≈ 240°
        (220,  40,  40),  # Pos 2 → Red         hue ≈ 0°
        (180,  30, 220),  # Pos 3 → Violet      hue ≈ 287°
        ( 30, 200, 200),  # Pos 4 → Cyan        hue ≈ 180°
        (255, 140,   0),  # Pos 5 → Orange      hue ≈ 33°
        (120,  30, 220),  # Pos 6 → Indigo      hue ≈ 268°
        ( 30, 100, 200),  # Pos 7 → Blue        hue ≈ 215°
        (230, 210,  30),  # Pos 8 → Yellow      hue ≈ 54°
    ]

    # Create 900x900 canvas
    mosaic = Image.new("RGB", (GRID * TILE_SIZE, GRID * TILE_SIZE), color=(200, 200, 200))

    for idx, color in enumerate(tiles_colors_shuffled):
        row = idx // GRID
        col = idx % GRID
        x0 = col * TILE_SIZE
        y0 = row * TILE_SIZE

        # Create a solid-color tile with a thin dark border for visual clarity
        tile = Image.new("RGB", (TILE_SIZE, TILE_SIZE), color=color)
        draw = ImageDraw.Draw(tile)
        draw.rectangle([0, 0, TILE_SIZE - 1, TILE_SIZE - 1], outline=(30, 30, 30), width=4)

        mosaic.paste(tile, (x0, y0))

    mosaic.save(OUTPUT, format="PNG")
    print(f'Initial mosaic created: {OUTPUT}')
    print(f'  Size: {mosaic.size[0]}x{mosaic.size[1]} pixels')
    print(f'  Tiles: {GRID}x{GRID} grid, each {TILE_SIZE}x{TILE_SIZE} pixels')
    print(f'  Tile colors (shuffled, NOT hue-sorted): {tiles_colors_shuffled}')

    # GUI-ready startup: open a terminal so the agent can run Python commands
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: gnome-terminal launched with DISPLAY=:0')


create_initial()
