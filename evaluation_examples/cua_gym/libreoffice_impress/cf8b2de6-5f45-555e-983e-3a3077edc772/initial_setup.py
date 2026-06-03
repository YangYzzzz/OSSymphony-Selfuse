"""
Initial Setup: Architecture portfolio presentation task
Task ID: osworld_impress_new_presentation_images_007
Domain: libreoffice_impress

Creates 6 architecture image files in ~/portfolio/ directory.
No presentation file is created (the agent must create it).
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_impress_new_presentation_images_007'
PORTFOLIO_DIR = f'{WORKDIR}/portfolio'


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


def create_architecture_images():
    """Create realistic architecture portfolio images using Pillow."""
    from PIL import Image, ImageDraw, ImageFont
    import random

    os.makedirs(PORTFOLIO_DIR, exist_ok=True)

    # Color palettes for architecture images
    building_colors = [
        [(70, 90, 110), (130, 150, 170), (200, 210, 220), (240, 245, 250)],  # Steel blue
        [(80, 60, 40), (140, 110, 80), (200, 180, 150), (230, 220, 200)],    # Warm stone
        [(50, 70, 50), (100, 130, 100), (170, 190, 160), (220, 230, 215)],   # Green facade
    ]

    def draw_building_1(draw, width, height):
        """Modern glass tower building"""
        # Sky gradient background
        for y in range(height):
            ratio = y / height
            r = int(135 + ratio * 80)
            g = int(180 + ratio * 50)
            b = int(220 + ratio * 30)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        # Ground
        draw.rectangle([0, height * 3 // 4, width, height], fill=(100, 120, 90))
        # Main tower structure
        tower_l = width * 3 // 10
        tower_r = width * 7 // 10
        tower_t = height // 8
        tower_b = height * 3 // 4
        draw.rectangle([tower_l, tower_t, tower_r, tower_b], fill=(80, 100, 120))
        # Glass panels
        panel_w = (tower_r - tower_l) // 5
        panel_h = (tower_b - tower_t) // 12
        for row in range(12):
            for col in range(5):
                px = tower_l + col * panel_w + 2
                py = tower_t + row * panel_h + 2
                shade = 150 + (row % 2) * 20 + (col % 2) * 15
                draw.rectangle([px, py, px + panel_w - 4, py + panel_h - 4],
                               fill=(shade - 30, shade, shade + 20))
        # Building label
        draw.text((10, 10), "Meridian Tower", fill=(255, 255, 255))

    def draw_building_2(draw, width, height):
        """Historic stone office building"""
        # Background - overcast sky
        for y in range(height * 3 // 4):
            ratio = y / (height * 3 // 4)
            r = int(180 + ratio * 40)
            g = int(190 + ratio * 40)
            b = int(200 + ratio * 40)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        # Foreground street
        draw.rectangle([0, height * 3 // 4, width, height], fill=(90, 85, 80))
        # Stone facade
        facade_l = width // 6
        facade_r = width * 5 // 6
        facade_t = height // 6
        facade_b = height * 3 // 4
        draw.rectangle([facade_l, facade_t, facade_r, facade_b], fill=(160, 145, 125))
        # Stone row texture
        stone_h = 15
        for row in range((facade_b - facade_t) // stone_h):
            y_pos = facade_t + row * stone_h
            draw.line([(facade_l, y_pos), (facade_r, y_pos)], fill=(130, 118, 100), width=2)
        # Windows
        win_cols = 6
        win_rows = 5
        win_w = (facade_r - facade_l) // (win_cols * 2)
        win_h = (facade_b - facade_t) // (win_rows * 2)
        for wr in range(win_rows):
            for wc in range(win_cols):
                wx = facade_l + wc * ((facade_r - facade_l) // win_cols) + win_w // 2
                wy = facade_t + 20 + wr * ((facade_b - facade_t) // win_rows)
                draw.rectangle([wx, wy, wx + win_w, wy + win_h], fill=(60, 80, 120))
        draw.text((10, 10), "Heritage Commerce Center", fill=(50, 50, 50))

    def draw_building_3(draw, width, height):
        """Contemporary curved museum building"""
        # Gradient sky
        for y in range(height):
            ratio = y / height
            r = int(200 - ratio * 60)
            g = int(210 - ratio * 50)
            b = int(240 - ratio * 30)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        # Ground plane
        draw.rectangle([0, height * 7 // 10, width, height], fill=(180, 175, 160))
        # Museum body - curved form suggestion
        for i in range(20):
            offset = i * 2
            shade = 220 - i * 3
            draw.ellipse([width // 4 - offset, height // 3 + offset,
                          width * 3 // 4 + offset, height * 7 // 10 + offset],
                         fill=(shade, shade - 5, shade - 10))
        draw.ellipse([width // 4, height // 3, width * 3 // 4, height * 7 // 10],
                     fill=(230, 225, 215))
        # Entry feature
        draw.rectangle([width * 2 // 5, height * 55 // 100, width * 3 // 5, height * 7 // 10],
                       fill=(40, 40, 40))
        draw.text((10, 10), "Contemporary Arts Museum", fill=(30, 30, 60))

    def draw_interior_1(draw, width, height):
        """Open-plan office interior"""
        # Ceiling
        draw.rectangle([0, 0, width, height // 4], fill=(240, 238, 235))
        # Floor
        draw.rectangle([0, height * 3 // 4, width, height], fill=(180, 160, 130))
        # Floor planks
        plank_h = 8
        for row in range(10):
            y_pos = height * 3 // 4 + row * plank_h
            draw.line([(0, y_pos), (width, y_pos)], fill=(160, 140, 110), width=1)
        # Walls
        draw.rectangle([0, height // 4, width, height * 3 // 4], fill=(250, 248, 245))
        # Large windows on far wall
        win_count = 4
        win_w = width // (win_count * 2)
        for wc in range(win_count):
            wx = wc * (width // win_count) + width // (win_count * 4)
            wy = height // 4 + 20
            draw.rectangle([wx, wy, wx + win_w, height // 2], fill=(170, 200, 230))
            draw.line([(wx, wy), (wx, height // 2)], fill=(100, 100, 100), width=2)
            draw.line([(wx, (wy + height // 2) // 2), (wx + win_w, (wy + height // 2) // 2)],
                      fill=(100, 100, 100), width=1)
        # Desk cluster suggestion
        for i in range(3):
            dx = width // 4 + i * (width // 5)
            draw.rectangle([dx, height // 2, dx + width // 8, height * 2 // 3],
                           fill=(200, 190, 175))
        draw.text((10, 10), "Collaborative Workspace Level 3", fill=(60, 60, 60))

    def draw_interior_2(draw, width, height):
        """Luxury hotel lobby"""
        # Marble floor
        draw.rectangle([0, height // 2, width, height], fill=(230, 225, 215))
        for i in range(8):
            x1 = i * (width // 8)
            draw.line([(x1, height // 2), (x1, height)], fill=(210, 205, 195), width=1)
        for j in range(6):
            y1 = height // 2 + j * (height // 12)
            draw.line([(0, y1), (width, y1)], fill=(210, 205, 195), width=1)
        # Back wall with paneling
        draw.rectangle([0, 0, width, height // 2], fill=(200, 185, 160))
        # Paneling detail
        panel_count = 6
        panel_w = width // panel_count
        panel_h = height // 3
        for pc in range(panel_count):
            px = pc * panel_w + 5
            draw.rectangle([px, 20, px + panel_w - 10, 20 + panel_h], fill=(180, 165, 140))
            draw.rectangle([px + 5, 25, px + panel_w - 15, 20 + panel_h - 5],
                           fill=(170, 155, 130))
        # Chandelier
        draw.ellipse([width // 2 - 40, 0, width // 2 + 40, 60], fill=(230, 200, 120))
        for angle in range(0, 360, 30):
            import math
            ex = width // 2 + int(50 * math.cos(math.radians(angle)))
            ey = 30 + int(30 * math.sin(math.radians(angle)))
            draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 230, 150))
        draw.text((10, 10), "Grand Lobby - Harrington Hotel", fill=(80, 60, 40))

    def draw_site_plan(draw, width, height):
        """Architectural site plan (top-down)"""
        # Background - terrain
        draw.rectangle([0, 0, width, height], fill=(200, 215, 195))
        # Street grid
        draw.line([(0, height // 4), (width, height // 4)], fill=(160, 155, 150), width=6)
        draw.line([(0, height * 3 // 4), (width, height * 3 // 4)], fill=(160, 155, 150), width=6)
        draw.line([(width // 4, 0), (width // 4, height)], fill=(160, 155, 150), width=6)
        draw.line([(width * 3 // 4, 0), (width * 3 // 4, height)], fill=(160, 155, 150), width=6)
        # Building footprints
        # Main building - large rectangle
        draw.rectangle([width * 3 // 10, height * 3 // 10, width * 7 // 10, height * 7 // 10],
                       fill=(120, 110, 100), outline=(80, 70, 60), width=2)
        # Parking area
        draw.rectangle([width // 8, height * 3 // 10, width // 4 - 5, height * 7 // 10],
                       fill=(150, 145, 140))
        for row in range(5):
            py = height * 3 // 10 + row * ((height * 4 // 10) // 5)
            draw.line([(width // 8, py), (width // 4 - 5, py)], fill=(100, 95, 90), width=1)
        # Green spaces
        draw.ellipse([width * 7 // 10 + 10, height * 3 // 10, width * 3 // 4,
                      height // 2], fill=(100, 160, 100))
        draw.ellipse([width * 7 // 10 + 10, height // 2 + 5, width * 3 // 4,
                      height * 7 // 10], fill=(100, 160, 100))
        # Scale bar
        draw.line([(10, height - 20), (110, height - 20)], fill=(30, 30, 30), width=3)
        draw.line([(10, height - 25), (10, height - 15)], fill=(30, 30, 30), width=2)
        draw.line([(110, height - 25), (110, height - 15)], fill=(30, 30, 30), width=2)
        draw.text((10, height - 40), "Site Plan - Scale 1:500", fill=(30, 30, 30))
        # North arrow
        draw.polygon([(width - 30, 40), (width - 40, 70), (width - 30, 60),
                      (width - 20, 70)], fill=(30, 30, 30))
        draw.text((width - 35, 10), "N", fill=(30, 30, 30))

    # Image specs: (filename, width, height, draw_function, format)
    images = [
        ('building_1.jpg', 1200, 800, draw_building_1, 'JPEG'),
        ('building_2.jpg', 1200, 800, draw_building_2, 'JPEG'),
        ('building_3.jpg', 1200, 800, draw_building_3, 'JPEG'),
        ('interior_1.jpg', 1200, 800, draw_interior_1, 'JPEG'),
        ('interior_2.jpg', 1200, 800, draw_interior_2, 'JPEG'),
        ('site_plan.png', 1200, 900, draw_site_plan, 'PNG'),
    ]

    for fname, w, h, draw_fn, fmt in images:
        img = Image.new('RGB', (w, h), color=(200, 200, 200))
        draw = ImageDraw.Draw(img)
        draw_fn(draw, w, h)
        out_path = os.path.join(PORTFOLIO_DIR, fname)
        img.save(out_path, fmt)
        print(f'Created image: {out_path}')

    print(f'All 6 portfolio images created in {PORTFOLIO_DIR}')


def setup_initial():
    # Create portfolio directory with images
    create_architecture_images()

    # Ensure no presentation file exists (clean slate for the agent)
    pptx_path = f'{WORKDIR}/{TASK_ID}.pptx'
    if os.path.exists(pptx_path):
        os.remove(pptx_path)
        print(f'Removed existing presentation: {pptx_path}')

    # Open file manager showing the portfolio directory so agent can see the images
    launch_gui(f'nautilus "{PORTFOLIO_DIR}"', delay_sec=2.0)
    print('GUI_READY: opened file manager at portfolio directory with DISPLAY=:0')


setup_initial()
