"""
Initial Setup: Create a 4-page architectural blueprints PDF
Task ID: pdf_mbc_076
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/blueprints.pdf'


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


def draw_title_block(page, shape, title, sheet_num, scale="1:100"):
    """Draw a standard architectural title block in the bottom-right corner."""
    w = page.rect.width
    h = page.rect.height

    # Title block border (bottom-right)
    tb_x0 = w - 250
    tb_y0 = h - 80
    tb_x1 = w - 20
    tb_y1 = h - 20
    shape.draw_rect(pymupdf.Rect(tb_x0, tb_y0, tb_x1, tb_y1))
    shape.finish(color=(0, 0, 0), width=1.5)

    # Horizontal divider
    shape.draw_line(pymupdf.Point(tb_x0, tb_y0 + 25), pymupdf.Point(tb_x1, tb_y0 + 25))
    shape.finish(color=(0, 0, 0), width=0.5)

    # Vertical divider
    mid_x = tb_x0 + (tb_x1 - tb_x0) * 0.6
    shape.draw_line(pymupdf.Point(mid_x, tb_y0 + 25), pymupdf.Point(mid_x, tb_y1))
    shape.finish(color=(0, 0, 0), width=0.5)

    # Title text
    page.insert_text(pymupdf.Point(tb_x0 + 8, tb_y0 + 18), title,
                     fontsize=10, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(tb_x0 + 8, tb_y0 + 42), "Meridian Architecture Group",
                     fontsize=7, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(tb_x0 + 8, tb_y0 + 54), "Project: Oakwood Residences",
                     fontsize=7, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(mid_x + 8, tb_y0 + 42), f"Sheet {sheet_num} of 4",
                     fontsize=7, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(mid_x + 8, tb_y0 + 54), f"Scale: {scale}",
                     fontsize=7, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(tb_x0 + 8, tb_y0 + 68), "Date: 2025-11-14",
                     fontsize=6, fontname="helv", color=(0.4, 0.4, 0.4))


def draw_border(page, shape):
    """Draw a standard drawing border with margin lines."""
    w = page.rect.width
    h = page.rect.height
    # Outer border
    shape.draw_rect(pymupdf.Rect(15, 15, w - 15, h - 15))
    shape.finish(color=(0, 0, 0), width=2.0)
    # Inner border
    shape.draw_rect(pymupdf.Rect(25, 25, w - 25, h - 25))
    shape.finish(color=(0, 0, 0), width=0.5)


def draw_page1_ground_floor(page):
    """Page 1: Ground Floor Plan"""
    shape = page.new_shape()
    draw_border(page, shape)

    # Title
    page.insert_text(pymupdf.Point(40, 55), "A-101: GROUND FLOOR PLAN",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))

    # Draw outer walls of a building footprint
    ox, oy = 80, 100  # origin
    scale_f = 1.0

    # Main rectangle (outer walls)
    walls = pymupdf.Rect(ox, oy, ox + 400, oy + 300)
    shape.draw_rect(walls)
    shape.finish(color=(0, 0, 0), width=2.5)

    # Interior walls
    # Horizontal divider (hallway)
    shape.draw_line(pymupdf.Point(ox, oy + 150), pymupdf.Point(ox + 400, oy + 150))
    shape.finish(color=(0, 0, 0), width=1.5)

    # Vertical walls creating rooms
    shape.draw_line(pymupdf.Point(ox + 160, oy), pymupdf.Point(ox + 160, oy + 150))
    shape.finish(color=(0, 0, 0), width=1.5)

    shape.draw_line(pymupdf.Point(ox + 280, oy), pymupdf.Point(ox + 280, oy + 150))
    shape.finish(color=(0, 0, 0), width=1.5)

    shape.draw_line(pymupdf.Point(ox + 200, oy + 150), pymupdf.Point(ox + 200, oy + 300))
    shape.finish(color=(0, 0, 0), width=1.5)

    # Door arcs (simple indicators)
    for dx, dy in [(ox + 70, oy + 145), (ox + 220, oy + 145), (ox + 340, oy + 145)]:
        shape.draw_line(pymupdf.Point(dx, dy), pymupdf.Point(dx + 30, dy))
        shape.finish(color=(0, 0, 0), width=0.5, dashes="[2 2]")

    # Room labels
    page.insert_text(pymupdf.Point(ox + 40, oy + 80), "LIVING ROOM",
                     fontsize=8, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(ox + 42, oy + 92), "4.2m x 3.8m",
                     fontsize=6, fontname="helv", color=(0.4, 0.4, 0.4))

    page.insert_text(pymupdf.Point(ox + 180, oy + 80), "KITCHEN",
                     fontsize=8, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(ox + 175, oy + 92), "3.0m x 3.8m",
                     fontsize=6, fontname="helv", color=(0.4, 0.4, 0.4))

    page.insert_text(pymupdf.Point(ox + 300, oy + 80), "GARAGE",
                     fontsize=8, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(ox + 295, oy + 92), "3.0m x 3.8m",
                     fontsize=6, fontname="helv", color=(0.4, 0.4, 0.4))

    page.insert_text(pymupdf.Point(ox + 50, oy + 230), "DINING ROOM",
                     fontsize=8, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(ox + 52, oy + 242), "5.0m x 3.8m",
                     fontsize=6, fontname="helv", color=(0.4, 0.4, 0.4))

    page.insert_text(pymupdf.Point(ox + 240, oy + 230), "STUDY",
                     fontsize=8, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(ox + 235, oy + 242), "5.0m x 3.8m",
                     fontsize=6, fontname="helv", color=(0.4, 0.4, 0.4))

    # Dimension lines
    page.insert_text(pymupdf.Point(ox + 170, oy - 10), "10.0 m",
                     fontsize=7, fontname="helv", color=(0, 0, 0.6))
    shape.draw_line(pymupdf.Point(ox, oy - 5), pymupdf.Point(ox + 400, oy - 5))
    shape.finish(color=(0, 0, 0.6), width=0.3)

    page.insert_text(pymupdf.Point(ox + 410, oy + 145), "7.6 m",
                     fontsize=7, fontname="helv", color=(0, 0, 0.6))
    shape.draw_line(pymupdf.Point(ox + 405, oy), pymupdf.Point(ox + 405, oy + 300))
    shape.finish(color=(0, 0, 0.6), width=0.3)

    # North arrow indicator
    page.insert_text(pymupdf.Point(530, 100), "N",
                     fontsize=12, fontname="hebo", color=(0, 0, 0))
    shape.draw_line(pymupdf.Point(536, 105), pymupdf.Point(536, 130))
    shape.finish(color=(0, 0, 0), width=1.5)
    shape.draw_line(pymupdf.Point(536, 105), pymupdf.Point(531, 115))
    shape.finish(color=(0, 0, 0), width=1.0)
    shape.draw_line(pymupdf.Point(536, 105), pymupdf.Point(541, 115))
    shape.finish(color=(0, 0, 0), width=1.0)

    draw_title_block(page, shape, "A-101: Ground Floor Plan", "1")
    shape.commit()


def draw_page2_first_floor(page):
    """Page 2: First Floor Plan"""
    shape = page.new_shape()
    draw_border(page, shape)

    page.insert_text(pymupdf.Point(40, 55), "A-102: FIRST FLOOR PLAN",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))

    ox, oy = 80, 100

    # Main rectangle
    walls = pymupdf.Rect(ox, oy, ox + 400, oy + 300)
    shape.draw_rect(walls)
    shape.finish(color=(0, 0, 0), width=2.5)

    # Hallway
    shape.draw_line(pymupdf.Point(ox + 180, oy), pymupdf.Point(ox + 180, oy + 300))
    shape.finish(color=(0, 0, 0), width=1.5)

    # Horizontal division upper area
    shape.draw_line(pymupdf.Point(ox, oy + 160), pymupdf.Point(ox + 180, oy + 160))
    shape.finish(color=(0, 0, 0), width=1.5)

    # Horizontal division right side
    shape.draw_line(pymupdf.Point(ox + 180, oy + 140), pymupdf.Point(ox + 400, oy + 140))
    shape.finish(color=(0, 0, 0), width=1.5)

    # Bathroom partition
    shape.draw_line(pymupdf.Point(ox + 300, oy + 140), pymupdf.Point(ox + 300, oy + 300))
    shape.finish(color=(0, 0, 0), width=1.5)

    # Room labels
    page.insert_text(pymupdf.Point(ox + 40, oy + 80), "MASTER BEDROOM",
                     fontsize=8, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(ox + 45, oy + 92), "4.5m x 4.0m",
                     fontsize=6, fontname="helv", color=(0.4, 0.4, 0.4))

    page.insert_text(pymupdf.Point(ox + 40, oy + 230), "BEDROOM 2",
                     fontsize=8, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(ox + 42, oy + 242), "4.5m x 3.5m",
                     fontsize=6, fontname="helv", color=(0.4, 0.4, 0.4))

    page.insert_text(pymupdf.Point(ox + 240, oy + 70), "BEDROOM 3",
                     fontsize=8, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(ox + 242, oy + 82), "5.5m x 3.5m",
                     fontsize=6, fontname="helv", color=(0.4, 0.4, 0.4))

    page.insert_text(pymupdf.Point(ox + 200, oy + 220), "BATHROOM 1",
                     fontsize=8, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(ox + 202, oy + 232), "3.0m x 4.0m",
                     fontsize=6, fontname="helv", color=(0.4, 0.4, 0.4))

    page.insert_text(pymupdf.Point(ox + 320, oy + 220), "BATH 2",
                     fontsize=8, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(ox + 318, oy + 232), "2.5m x 4.0m",
                     fontsize=6, fontname="helv", color=(0.4, 0.4, 0.4))

    # Staircase indicator
    stair_x, stair_y = ox + 350, oy + 50
    for i in range(6):
        shape.draw_line(pymupdf.Point(stair_x, stair_y + i * 10),
                        pymupdf.Point(stair_x + 40, stair_y + i * 10))
        shape.finish(color=(0, 0, 0), width=0.5)
    page.insert_text(pymupdf.Point(stair_x + 5, stair_y + 70), "DN",
                     fontsize=7, fontname="helv", color=(0, 0, 0))

    draw_title_block(page, shape, "A-102: First Floor Plan", "2")
    shape.commit()


def draw_page3_front_elevation(page):
    """Page 3: Front Elevation"""
    shape = page.new_shape()
    draw_border(page, shape)

    page.insert_text(pymupdf.Point(40, 55), "A-201: FRONT ELEVATION",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))

    ox, oy = 100, 150

    # Ground level line
    shape.draw_line(pymupdf.Point(ox - 30, oy + 200), pymupdf.Point(ox + 380, oy + 200))
    shape.finish(color=(0, 0, 0), width=1.0, dashes="[5 3]")
    page.insert_text(pymupdf.Point(ox - 30, oy + 215), "GROUND LEVEL 0.00",
                     fontsize=6, fontname="helv", color=(0.4, 0.4, 0.4))

    # Foundation
    shape.draw_rect(pymupdf.Rect(ox, oy + 200, ox + 350, oy + 215))
    shape.finish(color=(0, 0, 0), fill=(0.85, 0.85, 0.85), width=1.0)

    # Ground floor walls
    shape.draw_rect(pymupdf.Rect(ox, oy + 80, ox + 350, oy + 200))
    shape.finish(color=(0, 0, 0), width=1.5)

    # First floor walls
    shape.draw_rect(pymupdf.Rect(ox, oy - 40, ox + 350, oy + 80))
    shape.finish(color=(0, 0, 0), width=1.5)

    # Roof (triangle)
    shape.draw_polyline([
        pymupdf.Point(ox - 15, oy - 40),
        pymupdf.Point(ox + 175, oy - 100),
        pymupdf.Point(ox + 365, oy - 40),
        pymupdf.Point(ox - 15, oy - 40),
    ])
    shape.finish(color=(0, 0, 0), width=1.5)

    # Windows - ground floor
    for wx in [ox + 30, ox + 140, ox + 250]:
        shape.draw_rect(pymupdf.Rect(wx, oy + 110, wx + 60, oy + 170))
        shape.finish(color=(0, 0, 0), fill=(0.9, 0.95, 1.0), width=0.8)
        # Window cross
        shape.draw_line(pymupdf.Point(wx + 30, oy + 110), pymupdf.Point(wx + 30, oy + 170))
        shape.finish(color=(0, 0, 0), width=0.3)
        shape.draw_line(pymupdf.Point(wx, oy + 140), pymupdf.Point(wx + 60, oy + 140))
        shape.finish(color=(0, 0, 0), width=0.3)

    # Windows - first floor
    for wx in [ox + 30, ox + 140, ox + 250]:
        shape.draw_rect(pymupdf.Rect(wx, oy - 10, wx + 60, oy + 50))
        shape.finish(color=(0, 0, 0), fill=(0.9, 0.95, 1.0), width=0.8)
        shape.draw_line(pymupdf.Point(wx + 30, oy - 10), pymupdf.Point(wx + 30, oy + 50))
        shape.finish(color=(0, 0, 0), width=0.3)
        shape.draw_line(pymupdf.Point(wx, oy + 20), pymupdf.Point(wx + 60, oy + 20))
        shape.finish(color=(0, 0, 0), width=0.3)

    # Front door
    shape.draw_rect(pymupdf.Rect(ox + 155, oy + 120, ox + 195, oy + 200))
    shape.finish(color=(0, 0, 0), fill=(0.5, 0.35, 0.2), width=1.0)

    # Height annotations
    page.insert_text(pymupdf.Point(ox + 365, oy + 140), "+3.00m",
                     fontsize=6, fontname="helv", color=(0, 0, 0.6))
    page.insert_text(pymupdf.Point(ox + 365, oy + 20), "+6.00m",
                     fontsize=6, fontname="helv", color=(0, 0, 0.6))
    page.insert_text(pymupdf.Point(ox + 365, oy - 75), "+9.20m",
                     fontsize=6, fontname="helv", color=(0, 0, 0.6))

    draw_title_block(page, shape, "A-201: Front Elevation", "3", "1:50")
    shape.commit()


def draw_page4_section(page):
    """Page 4: Cross Section"""
    shape = page.new_shape()
    draw_border(page, shape)

    page.insert_text(pymupdf.Point(40, 55), "A-301: CROSS SECTION A-A",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))

    ox, oy = 120, 140

    # Ground line
    shape.draw_line(pymupdf.Point(ox - 40, oy + 210), pymupdf.Point(ox + 340, oy + 210))
    shape.finish(color=(0, 0, 0), width=1.0, dashes="[5 3]")
    page.insert_text(pymupdf.Point(ox - 40, oy + 225), "GL 0.00",
                     fontsize=6, fontname="helv", color=(0.4, 0.4, 0.4))

    # Foundation
    shape.draw_rect(pymupdf.Rect(ox - 10, oy + 210, ox + 310, oy + 240))
    shape.finish(color=(0, 0, 0), fill=(0.8, 0.8, 0.8), width=1.0)
    # Hatching for foundation
    for i in range(0, 320, 8):
        shape.draw_line(pymupdf.Point(ox - 10 + i, oy + 240),
                        pymupdf.Point(ox - 10 + i + 15, oy + 210))
        shape.finish(color=(0.5, 0.5, 0.5), width=0.2)

    # Left wall (section cut - thick)
    shape.draw_rect(pymupdf.Rect(ox, oy + 10, ox + 15, oy + 210))
    shape.finish(color=(0, 0, 0), fill=(0.6, 0.6, 0.6), width=2.0)

    # Right wall
    shape.draw_rect(pymupdf.Rect(ox + 285, oy + 10, ox + 300, oy + 210))
    shape.finish(color=(0, 0, 0), fill=(0.6, 0.6, 0.6), width=2.0)

    # Floor slab (first floor level)
    shape.draw_rect(pymupdf.Rect(ox, oy + 100, ox + 300, oy + 112))
    shape.finish(color=(0, 0, 0), fill=(0.7, 0.7, 0.7), width=1.0)

    # Roof structure
    shape.draw_polyline([
        pymupdf.Point(ox - 20, oy + 10),
        pymupdf.Point(ox + 150, oy - 50),
        pymupdf.Point(ox + 320, oy + 10),
        pymupdf.Point(ox - 20, oy + 10),
    ])
    shape.finish(color=(0, 0, 0), width=1.5)

    # Roof rafters
    for rx in range(0, 300, 50):
        shape.draw_line(pymupdf.Point(ox + rx, oy + 10),
                        pymupdf.Point(ox + 150, oy - 50))
        shape.finish(color=(0, 0, 0), width=0.3)

    # Internal walls
    shape.draw_rect(pymupdf.Rect(ox + 140, oy + 112, ox + 155, oy + 210))
    shape.finish(color=(0, 0, 0), fill=(0.6, 0.6, 0.6), width=1.0)

    # Level labels
    page.insert_text(pymupdf.Point(ox + 320, oy + 208), "Ground Floor +0.00",
                     fontsize=6, fontname="helv", color=(0, 0, 0.6))
    page.insert_text(pymupdf.Point(ox + 320, oy + 108), "First Floor +3.00",
                     fontsize=6, fontname="helv", color=(0, 0, 0.6))
    page.insert_text(pymupdf.Point(ox + 320, oy + 8), "Eaves +6.00",
                     fontsize=6, fontname="helv", color=(0, 0, 0.6))
    page.insert_text(pymupdf.Point(ox + 170, oy - 45), "Ridge +9.20",
                     fontsize=6, fontname="helv", color=(0, 0, 0.6))

    # Section cut indicator
    page.insert_text(pymupdf.Point(ox + 100, oy + 260), "SECTION A-A",
                     fontsize=9, fontname="hebo", color=(0, 0, 0))

    # Dimension annotations
    shape.draw_line(pymupdf.Point(ox - 25, oy + 210), pymupdf.Point(ox - 25, oy + 100))
    shape.finish(color=(0, 0, 0.6), width=0.3)
    page.insert_text(pymupdf.Point(ox - 55, oy + 160), "3.00m",
                     fontsize=6, fontname="helv", color=(0, 0, 0.6))

    shape.draw_line(pymupdf.Point(ox - 25, oy + 100), pymupdf.Point(ox - 25, oy + 10))
    shape.finish(color=(0, 0, 0.6), width=0.3)
    page.insert_text(pymupdf.Point(ox - 55, oy + 60), "3.00m",
                     fontsize=6, fontname="helv", color=(0, 0, 0.6))

    draw_title_block(page, shape, "A-301: Cross Section A-A", "4", "1:50")
    shape.commit()


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Create a 4-page architectural blueprint PDF (A3 landscape for blueprints)
    doc = pymupdf.open()

    # Page 1: Ground Floor Plan
    page1 = doc.new_page(width=595, height=842)  # A4 portrait
    draw_page1_ground_floor(page1)

    # Page 2: First Floor Plan
    page2 = doc.new_page(width=595, height=842)
    draw_page2_first_floor(page2)

    # Page 3: Front Elevation
    page3 = doc.new_page(width=595, height=842)
    draw_page3_front_elevation(page3)

    # Page 4: Cross Section
    page4 = doc.new_page(width=595, height=842)
    draw_page4_section(page4)

    # Set metadata
    doc.set_metadata({
        "title": "Oakwood Residences - Architectural Blueprints",
        "author": "Meridian Architecture Group",
        "subject": "Architectural Drawings",
        "creator": "CAD Export",
    })

    # Set TOC
    doc.set_toc([
        [1, "A-101: Ground Floor Plan", 1],
        [1, "A-102: First Floor Plan", 2],
        [1, "A-201: Front Elevation", 3],
        [1, "A-301: Cross Section A-A", 4],
    ])

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Make sure tiff_output directory does NOT exist
    import shutil
    tiff_dir = f'{DOCS_DIR}/tiff_output'
    if os.path.exists(tiff_dir):
        shutil.rmtree(tiff_dir)

    # Open PDF in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
