"""
Initial Setup: Create A3 landscape engineering drawings PDF
Task ID: pdf_pw_028
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_028'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/a3_drawings.pdf'

# A3 landscape dimensions in points
A3_W = 1190.55
A3_H = 841.89


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


def draw_engineering_page(doc, page_num, title, description):
    """Draw a single engineering drawing page with diagrams and annotations."""
    page = doc.new_page(width=A3_W, height=A3_H)

    # Title block (bottom-right corner, traditional engineering drawing style)
    # Draw border around entire page
    shape = page.new_shape()

    # Outer border
    margin = 30
    shape.draw_rect(pymupdf.Rect(margin, margin, A3_W - margin, A3_H - margin))
    shape.finish(color=(0, 0, 0), width=2.0)

    # Inner border
    shape.draw_rect(pymupdf.Rect(margin + 5, margin + 5, A3_W - margin - 5, A3_H - margin - 5))
    shape.finish(color=(0, 0, 0), width=0.5)

    # Title block area (bottom-right)
    tb_x = A3_W - 350
    tb_y = A3_H - 150
    shape.draw_rect(pymupdf.Rect(tb_x, tb_y, A3_W - margin - 5, A3_H - margin - 5))
    shape.finish(color=(0, 0, 0), width=1.0)

    # Horizontal dividers in title block
    for dy in [30, 60, 90]:
        shape.draw_line(pymupdf.Point(tb_x, tb_y + dy), pymupdf.Point(A3_W - margin - 5, tb_y + dy))
        shape.finish(color=(0, 0, 0), width=0.5)

    # Vertical divider in title block
    shape.draw_line(pymupdf.Point(tb_x + 170, tb_y), pymupdf.Point(tb_x + 170, A3_H - margin - 5))
    shape.finish(color=(0, 0, 0), width=0.5)

    shape.commit()

    # Title block text
    page.insert_text(pymupdf.Point(tb_x + 10, tb_y + 20), "ACME Engineering Corp.", fontsize=10, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(tb_x + 10, tb_y + 50), f"Drawing: {title}", fontsize=9, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(tb_x + 10, tb_y + 80), f"Sheet {page_num} of 8", fontsize=9, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(tb_x + 10, tb_y + 110), "Scale: 1:50", fontsize=9, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(tb_x + 180, tb_y + 20), "Date: 2025-11-15", fontsize=9, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(tb_x + 180, tb_y + 50), "Rev: C", fontsize=9, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(tb_x + 180, tb_y + 80), "Drawn by: J. Martinez", fontsize=9, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(tb_x + 180, tb_y + 110), "Checked: R. Nakamura", fontsize=9, fontname="helv", color=(0, 0, 0))

    # Drawing title (top area)
    page.insert_text(pymupdf.Point(60, 65), title, fontsize=18, fontname="hebo", color=(0, 0, 0.3))
    page.insert_text(pymupdf.Point(60, 85), description, fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))

    # Draw engineering content unique to each page
    shape2 = page.new_shape()

    if page_num == 1:
        # Site plan with rectangles representing buildings
        cx, cy = 500, 380
        shape2.draw_rect(pymupdf.Rect(cx - 200, cy - 150, cx + 200, cy + 150))
        shape2.finish(color=(0, 0, 0), width=1.5)
        shape2.draw_rect(pymupdf.Rect(cx - 150, cy - 100, cx - 50, cy))
        shape2.finish(color=(0, 0, 0.6), fill=(0.85, 0.85, 1.0), width=1.0)
        shape2.draw_rect(pymupdf.Rect(cx + 30, cy - 120, cx + 170, cy + 80))
        shape2.finish(color=(0, 0, 0.6), fill=(0.85, 0.85, 1.0), width=1.0)
        # Dimension lines
        shape2.draw_line(pymupdf.Point(cx - 200, cy + 180), pymupdf.Point(cx + 200, cy + 180))
        shape2.finish(color=(1, 0, 0), width=0.5)
        page.insert_text(pymupdf.Point(cx - 20, cy + 175), "40.0 m", fontsize=8, fontname="helv", color=(1, 0, 0))

    elif page_num == 2:
        # Floor plan - ground floor
        cx, cy = 500, 350
        shape2.draw_rect(pymupdf.Rect(cx - 250, cy - 180, cx + 250, cy + 180))
        shape2.finish(color=(0, 0, 0), width=2.0)
        # Interior walls
        shape2.draw_line(pymupdf.Point(cx - 250, cy), pymupdf.Point(cx + 50, cy))
        shape2.finish(color=(0, 0, 0), width=1.5)
        shape2.draw_line(pymupdf.Point(cx + 50, cy - 180), pymupdf.Point(cx + 50, cy + 180))
        shape2.finish(color=(0, 0, 0), width=1.5)
        # Door arc
        shape2.draw_circle(pymupdf.Point(cx + 50, cy), 40)
        shape2.finish(color=(0, 0, 0), width=0.5)

    elif page_num == 3:
        # Elevation - front view
        cx, cy = 500, 380
        shape2.draw_rect(pymupdf.Rect(cx - 220, cy - 160, cx + 220, cy + 100))
        shape2.finish(color=(0, 0, 0), width=1.5)
        # Roof triangle
        shape2.draw_polyline([
            pymupdf.Point(cx - 230, cy - 160),
            pymupdf.Point(cx, cy - 260),
            pymupdf.Point(cx + 230, cy - 160),
            pymupdf.Point(cx - 230, cy - 160),
        ])
        shape2.finish(color=(0, 0, 0), width=1.5)
        # Windows
        for wx in [-140, -40, 60, 140]:
            shape2.draw_rect(pymupdf.Rect(cx + wx - 25, cy - 100, cx + wx + 25, cy - 20))
            shape2.finish(color=(0, 0, 0.5), fill=(0.8, 0.9, 1.0), width=0.8)

    elif page_num == 4:
        # Cross section
        cx, cy = 500, 380
        shape2.draw_rect(pymupdf.Rect(cx - 200, cy - 120, cx + 200, cy + 120))
        shape2.finish(color=(0, 0, 0), width=1.5)
        # Floor slabs
        for fy in [-60, 0, 60]:
            shape2.draw_line(pymupdf.Point(cx - 200, cy + fy), pymupdf.Point(cx + 200, cy + fy))
            shape2.finish(color=(0.4, 0.4, 0.4), width=1.0)
        # Hatching for cut materials
        for hx in range(-190, 200, 15):
            shape2.draw_line(pymupdf.Point(cx + hx, cy + 120), pymupdf.Point(cx + hx + 30, cy + 150))
            shape2.finish(color=(0.5, 0.5, 0.5), width=0.3)

    elif page_num == 5:
        # Structural detail - beam connection
        cx, cy = 500, 380
        shape2.draw_rect(pymupdf.Rect(cx - 80, cy - 200, cx + 80, cy + 200))
        shape2.finish(color=(0, 0, 0), width=2.0)
        shape2.draw_rect(pymupdf.Rect(cx - 250, cy - 30, cx - 80, cy + 30))
        shape2.finish(color=(0, 0, 0), width=2.0)
        shape2.draw_rect(pymupdf.Rect(cx + 80, cy - 30, cx + 250, cy + 30))
        shape2.finish(color=(0, 0, 0), width=2.0)
        # Bolts
        for bx in [-60, -30, 30, 60]:
            for by in [-15, 15]:
                shape2.draw_circle(pymupdf.Point(cx + bx, cy + by), 5)
                shape2.finish(color=(0, 0, 0), fill=(0.3, 0.3, 0.3), width=0.5)

    elif page_num == 6:
        # Electrical layout
        cx, cy = 480, 360
        shape2.draw_rect(pymupdf.Rect(cx - 220, cy - 180, cx + 220, cy + 180))
        shape2.finish(color=(0, 0, 0), width=1.0)
        # Wiring paths
        points = [
            pymupdf.Point(cx - 200, cy - 100),
            pymupdf.Point(cx - 50, cy - 100),
            pymupdf.Point(cx - 50, cy + 50),
            pymupdf.Point(cx + 150, cy + 50),
        ]
        shape2.draw_polyline(points)
        shape2.finish(color=(1, 0, 0), width=1.0)
        # Switch symbols
        for sx, sy in [(-200, -100), (-50, -100), (150, 50)]:
            shape2.draw_circle(pymupdf.Point(cx + sx, cy + sy), 8)
            shape2.finish(color=(1, 0, 0), width=1.0)

    elif page_num == 7:
        # Plumbing isometric
        cx, cy = 500, 380
        # Vertical pipe
        shape2.draw_line(pymupdf.Point(cx, cy - 200), pymupdf.Point(cx, cy + 150))
        shape2.finish(color=(0, 0, 0.8), width=2.0)
        # Horizontal branches
        for hy in [-120, -40, 60]:
            shape2.draw_line(pymupdf.Point(cx, cy + hy), pymupdf.Point(cx + 200, cy + hy))
            shape2.finish(color=(0, 0, 0.8), width=1.5)
            # Valve symbol
            shape2.draw_polyline([
                pymupdf.Point(cx + 90, cy + hy - 10),
                pymupdf.Point(cx + 100, cy + hy),
                pymupdf.Point(cx + 90, cy + hy + 10),
            ])
            shape2.finish(color=(0, 0, 0.8), width=1.0)
            shape2.draw_polyline([
                pymupdf.Point(cx + 110, cy + hy - 10),
                pymupdf.Point(cx + 100, cy + hy),
                pymupdf.Point(cx + 110, cy + hy + 10),
            ])
            shape2.finish(color=(0, 0, 0.8), width=1.0)

    elif page_num == 8:
        # Schedule / specifications table
        page.insert_text(pymupdf.Point(80, 140), "Material Schedule", fontsize=14, fontname="hebo", color=(0, 0, 0))
        # Table header
        cols = [80, 230, 430, 630, 830]
        headers = ["Item", "Description", "Material", "Quantity", "Notes"]
        y_start = 170
        row_h = 30
        for i, (col, hdr) in enumerate(zip(cols, headers)):
            page.insert_text(pymupdf.Point(col + 5, y_start + 18), hdr, fontsize=10, fontname="hebo", color=(0, 0, 0))

        # Table data
        table_data = [
            ["F-001", "Foundation Pad Type A", "Concrete C30", "12", "See dwg 04"],
            ["F-002", "Foundation Pad Type B", "Concrete C30", "8", "See dwg 04"],
            ["S-001", "Steel Column HEB 300", "S355 Steel", "24", "Hot-dip galv."],
            ["S-002", "Steel Beam IPE 400", "S355 Steel", "36", "Fire rated"],
            ["S-003", "Steel Brace CHS 168.3", "S355 Steel", "16", ""],
            ["W-001", "Ext. Wall Panel 200mm", "Precast Concrete", "48", "Insulated"],
            ["W-002", "Int. Partition 100mm", "Plasterboard", "62", "Acoustic rated"],
            ["R-001", "Roof Truss Type A", "Glulam Timber", "14", "See dwg 03"],
            ["E-001", "Main Distribution Board", "Copper/Steel", "2", "See dwg 06"],
            ["P-001", "Main Riser Pipe DN100", "HDPE", "4", "See dwg 07"],
        ]
        for r, row in enumerate(table_data):
            y = y_start + (r + 1) * row_h
            for col, val in zip(cols, row):
                page.insert_text(pymupdf.Point(col + 5, y + 18), val, fontsize=9, fontname="helv", color=(0, 0, 0))

        # Draw table grid
        n_rows = len(table_data) + 1
        for i in range(n_rows + 1):
            y = y_start + i * row_h
            shape2.draw_line(pymupdf.Point(cols[0], y), pymupdf.Point(930, y))
            shape2.finish(color=(0, 0, 0), width=0.5)
        for col in cols + [930]:
            shape2.draw_line(pymupdf.Point(col, y_start), pymupdf.Point(col, y_start + n_rows * row_h))
            shape2.finish(color=(0, 0, 0), width=0.5)

    # Add common annotations for all pages
    page.insert_text(pymupdf.Point(60, A3_H - 40), f"ACME-2025-{page_num:03d}-C", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(A3_W - 200, 65), "CONFIDENTIAL", fontsize=10, fontname="hebo", color=(0.8, 0, 0))

    shape2.commit()


def create_initial():
    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = pymupdf.open()

    # Create 8 engineering drawing pages
    pages_info = [
        (1, "Site Plan - General Layout", "Overall site arrangement showing building positions and access roads"),
        (2, "Ground Floor Plan", "Detailed floor plan with room dimensions and wall positions"),
        (3, "Front Elevation", "Main facade showing window positions and roof profile"),
        (4, "Cross Section A-A", "Transverse section showing floor levels and structural elements"),
        (5, "Structural Detail - Beam Connection", "Steel beam-to-column connection detail at Grid B3"),
        (6, "Electrical Layout - Ground Floor", "Power distribution and switching arrangement"),
        (7, "Plumbing Isometric", "Cold and hot water distribution risers and branch connections"),
        (8, "Material Schedule", "Complete bill of materials and specifications summary"),
    ]

    for num, title, desc in pages_info:
        draw_engineering_page(doc, num, title, desc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 8, Format: A3 landscape ({A3_W} x {A3_H} pts)')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
