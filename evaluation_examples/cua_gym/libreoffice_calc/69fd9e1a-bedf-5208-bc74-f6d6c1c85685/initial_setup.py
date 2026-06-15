"""
Initial Setup: Create tileset.png on the Desktop and open it in GIMP.
Task ID: osworld_multi_apps_gimp_vscode_006
Domain: gimp + vscode (multi-app)
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_006'
TILESET_PATH = f'{WORKDIR}/tileset.png'

# Tileset layout: 6 columns x 4 rows, each tile is 64x64 pixels
TILE_W = 64
TILE_H = 64
COLS = 6
ROWS = 4
IMG_W = TILE_W * COLS  # 384
IMG_H = TILE_H * ROWS  # 256


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


def create_tileset():
    """Create a realistic-looking terrain tileset PNG."""
    # Terrain tile color palette (realistic terrain tile colors)
    # Each tile gets a distinct terrain-like color/pattern
    tile_colors = [
        # Row 0
        [(34, 139, 34),   (0, 100, 0),    (107, 142, 35),  (154, 205, 50), (85, 107, 47),  (0, 128, 0)],
        # Row 1
        [(210, 180, 140), (194, 178, 128), (222, 184, 135), (180, 130, 70), (160, 120, 60), (200, 160, 90)],
        # Row 2
        [(64, 64, 200),   (30, 144, 255),  (0, 191, 255),   (70, 130, 180),(100, 149, 237),(135, 206, 235)],
        # Row 3
        [(128, 128, 128), (105, 105, 105), (169, 169, 169), (119, 136, 153),(112, 128, 144),(192, 192, 192)],
    ]

    img = Image.new("RGB", (IMG_W, IMG_H), (200, 200, 200))
    draw = ImageDraw.Draw(img)

    for row in range(ROWS):
        for col in range(COLS):
            x0 = col * TILE_W
            y0 = row * TILE_H
            x1 = x0 + TILE_W
            y1 = y0 + TILE_H

            base_color = tile_colors[row][col]

            # Fill tile base color
            draw.rectangle([x0, y0, x1 - 1, y1 - 1], fill=base_color)

            # Add some texture variation within the tile
            r, g, b = base_color
            # Lighter inner region for texture
            inner_color = (min(255, r + 20), min(255, g + 20), min(255, b + 20))
            draw.rectangle([x0 + 8, y0 + 8, x1 - 9, y1 - 9], fill=inner_color)

            # Add a darker center dot as terrain feature
            dark_color = (max(0, r - 40), max(0, g - 40), max(0, b - 40))
            draw.ellipse([x0 + 22, y0 + 22, x0 + 42, y0 + 42], fill=dark_color)

            # Draw tile border (darker)
            border_color = (max(0, r - 60), max(0, g - 60), max(0, b - 60))
            draw.rectangle([x0, y0, x1 - 1, y1 - 1], outline=border_color, width=2)

    # Add grid lines to clearly delineate tiles
    line_color = (50, 50, 50)
    for c in range(COLS + 1):
        x = c * TILE_W
        draw.line([(x, 0), (x, IMG_H)], fill=line_color, width=1)
    for r in range(ROWS + 1):
        y = r * TILE_H
        draw.line([(0, y), (IMG_W, y)], fill=line_color, width=1)

    os.makedirs(WORKDIR, exist_ok=True)
    img.save(TILESET_PATH)
    print(f'Tileset created: {TILESET_PATH}')
    print(f'  Size: {img.size} ({COLS}x{ROWS} grid of {TILE_W}x{TILE_H} tiles)')
    print(f'  Tile at row=2, col=3 is at pixel box: ({3*TILE_W}, {2*TILE_H}, {4*TILE_W}, {3*TILE_H})')


def create_initial():
    create_tileset()

    # GUI-ready startup: open GIMP with the tileset
    launch_gui(f'gimp "{TILESET_PATH}"', delay_sec=3.0)
    print('GUI_READY: launched GIMP with tileset.png on DISPLAY=:0')


create_initial()
