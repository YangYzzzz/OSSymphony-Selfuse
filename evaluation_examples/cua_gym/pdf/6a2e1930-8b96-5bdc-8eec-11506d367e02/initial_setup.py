"""
Initial Setup: Create a 5-page architectural blueprint PDF
Task ID: pdf_ro_014
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_014'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/blueprint.pdf'


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
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: Title Page ---
    page = doc.new_page(width=612, height=792)  # Letter size
    # Title
    page.insert_text(
        pymupdf.Point(72, 120),
        "GREENFIELD CORPORATE CAMPUS",
        fontsize=24,
        fontname="hebo",
        color=(0.1, 0.1, 0.3),
    )
    page.insert_text(
        pymupdf.Point(72, 155),
        "Architectural Design Package",
        fontsize=16,
        fontname="helv",
        color=(0.2, 0.2, 0.4),
    )
    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 175), pymupdf.Point(540, 175))
    shape.finish(color=(0.3, 0.3, 0.5), width=2)
    shape.commit()

    # Project details
    details = [
        ("Project Number:", "GCC-2025-0847"),
        ("Client:", "Meridian Properties LLC"),
        ("Architect:", "Thornton & Associates Architecture"),
        ("Lead Designer:", "Dr. Elena Vasquez, AIA, LEED AP"),
        ("Structural Engineer:", "Reynolds Structural Group"),
        ("Date:", "March 15, 2025"),
        ("Revision:", "Rev C - Permit Set"),
        ("Location:", "2450 Innovation Drive, Austin, TX 78759"),
    ]
    y = 220
    for label, value in details:
        page.insert_text(pymupdf.Point(72, y), label, fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
        page.insert_text(pymupdf.Point(220, y), value, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 22

    # Footer
    page.insert_text(
        pymupdf.Point(72, 740),
        "CONFIDENTIAL - For Permit Review Only",
        fontsize=9,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )

    # --- Page 2: Site Plan Overview ---
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 60), "SITE PLAN OVERVIEW", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.3))
    page2.insert_text(pymupdf.Point(72, 80), "Sheet A-101", fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))

    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 90), pymupdf.Point(540, 90))
    shape2.finish(color=(0.3, 0.3, 0.5), width=1)
    shape2.commit()

    site_text = (
        "The Greenfield Corporate Campus occupies a 12.4-acre parcel at the intersection of "
        "Innovation Drive and Lakewood Boulevard. The site plan integrates three primary structures: "
        "Building A (4-story office tower, 185,000 SF), Building B (2-story research facility, 72,000 SF), "
        "and Building C (parking garage with ground-floor retail, 450 spaces). "
        "Landscaping follows xeriscape principles with native Texas plantings, permeable hardscape, "
        "and a 1.2-acre retention pond serving dual stormwater and aesthetic functions."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 110, 540, 260),
        site_text,
        fontsize=11,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Draw simplified site boundary
    shape2b = page2.new_shape()
    shape2b.draw_rect(pymupdf.Rect(100, 300, 510, 700))
    shape2b.finish(color=(0.3, 0.3, 0.3), width=1.5)
    # Building A outline
    shape2b.draw_rect(pymupdf.Rect(150, 360, 310, 500))
    shape2b.finish(color=(0, 0, 0.6), width=1)
    # Building B outline
    shape2b.draw_rect(pymupdf.Rect(350, 380, 470, 480))
    shape2b.finish(color=(0, 0, 0.6), width=1)
    # Parking structure
    shape2b.draw_rect(pymupdf.Rect(180, 560, 380, 660))
    shape2b.finish(color=(0.4, 0.4, 0.4), width=1, dashes="[4 2]")
    shape2b.commit()

    page2.insert_text(pymupdf.Point(200, 440), "Building A", fontsize=9, fontname="hebo", color=(0, 0, 0.6))
    page2.insert_text(pymupdf.Point(380, 440), "Bldg B", fontsize=9, fontname="hebo", color=(0, 0, 0.6))
    page2.insert_text(pymupdf.Point(240, 620), "Parking C", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))

    # --- Page 3: Floor Plan (this is the target page for annotations) ---
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(72, 60), "BUILDING A - GROUND FLOOR PLAN", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.3))
    page3.insert_text(pymupdf.Point(72, 80), "Sheet A-201  |  Scale: 1/8\" = 1'-0\"", fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))

    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, 90), pymupdf.Point(540, 90))
    shape3.finish(color=(0.3, 0.3, 0.5), width=1)
    shape3.commit()

    # Floor plan - outer walls
    shape3b = page3.new_shape()
    shape3b.draw_rect(pymupdf.Rect(80, 120, 530, 700))
    shape3b.finish(color=(0, 0, 0), width=2)

    # Internal partitions - lobby area
    shape3b.draw_rect(pymupdf.Rect(80, 120, 280, 320))
    shape3b.finish(color=(0, 0, 0), width=1)
    # Conference rooms
    shape3b.draw_rect(pymupdf.Rect(280, 120, 400, 250))
    shape3b.finish(color=(0, 0, 0), width=1)
    shape3b.draw_rect(pymupdf.Rect(400, 120, 530, 250))
    shape3b.finish(color=(0, 0, 0), width=1)
    # Open office area
    shape3b.draw_rect(pymupdf.Rect(80, 320, 530, 550))
    shape3b.finish(color=(0, 0, 0), width=0.5, dashes="[2 2]")
    # Restrooms / utility
    shape3b.draw_rect(pymupdf.Rect(80, 550, 200, 700))
    shape3b.finish(color=(0, 0, 0), width=1)
    shape3b.draw_rect(pymupdf.Rect(200, 550, 320, 700))
    shape3b.finish(color=(0, 0, 0), width=1)
    # Elevator core
    shape3b.draw_rect(pymupdf.Rect(320, 550, 420, 700))
    shape3b.finish(color=(0.5, 0.5, 0.5), fill=(0.9, 0.9, 0.9), width=1)
    # Stairwell
    shape3b.draw_rect(pymupdf.Rect(420, 550, 530, 700))
    shape3b.finish(color=(0, 0, 0), width=1)

    shape3b.commit()

    # Room labels
    page3.insert_text(pymupdf.Point(140, 230), "LOBBY", fontsize=10, fontname="hebo", color=(0.2, 0.2, 0.2))
    page3.insert_text(pymupdf.Point(130, 250), "1,920 SF", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))
    page3.insert_text(pymupdf.Point(300, 190), "CONF A", fontsize=8, fontname="hebo", color=(0.2, 0.2, 0.2))
    page3.insert_text(pymupdf.Point(300, 205), "480 SF", fontsize=7, fontname="helv", color=(0.4, 0.4, 0.4))
    page3.insert_text(pymupdf.Point(430, 190), "CONF B", fontsize=8, fontname="hebo", color=(0.2, 0.2, 0.2))
    page3.insert_text(pymupdf.Point(430, 205), "520 SF", fontsize=7, fontname="helv", color=(0.4, 0.4, 0.4))
    page3.insert_text(pymupdf.Point(250, 440), "OPEN OFFICE", fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
    page3.insert_text(pymupdf.Point(250, 460), "8,280 SF", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page3.insert_text(pymupdf.Point(100, 630), "WOMEN", fontsize=8, fontname="hebo", color=(0.2, 0.2, 0.2))
    page3.insert_text(pymupdf.Point(225, 630), "MEN", fontsize=8, fontname="hebo", color=(0.2, 0.2, 0.2))
    page3.insert_text(pymupdf.Point(340, 630), "ELEV", fontsize=8, fontname="hebo", color=(0.4, 0.4, 0.4))
    page3.insert_text(pymupdf.Point(450, 630), "STAIR", fontsize=8, fontname="hebo", color=(0.4, 0.4, 0.4))

    # Compass rose indicator
    page3.insert_text(pymupdf.Point(500, 750), "N", fontsize=14, fontname="hebo", color=(0, 0, 0))

    # --- Page 4: Elevations ---
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(pymupdf.Point(72, 60), "BUILDING A - EXTERIOR ELEVATIONS", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.3))
    page4.insert_text(pymupdf.Point(72, 80), "Sheet A-301  |  Scale: 1/16\" = 1'-0\"", fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))

    shape4 = page4.new_shape()
    shape4.draw_line(pymupdf.Point(72, 90), pymupdf.Point(540, 90))
    shape4.finish(color=(0.3, 0.3, 0.5), width=1)
    shape4.commit()

    # North elevation
    page4.insert_text(pymupdf.Point(72, 120), "NORTH ELEVATION", fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
    shape4b = page4.new_shape()
    shape4b.draw_rect(pymupdf.Rect(100, 140, 500, 320))
    shape4b.finish(color=(0, 0, 0), width=1)
    # Window grid
    for row in range(4):
        for col in range(6):
            x = 120 + col * 60
            y = 155 + row * 40
            shape4b.draw_rect(pymupdf.Rect(x, y, x + 40, y + 25))
            shape4b.finish(color=(0.3, 0.5, 0.7), fill=(0.8, 0.9, 1.0), width=0.5)
    shape4b.commit()

    # South elevation
    page4.insert_text(pymupdf.Point(72, 370), "SOUTH ELEVATION", fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
    shape4c = page4.new_shape()
    shape4c.draw_rect(pymupdf.Rect(100, 390, 500, 570))
    shape4c.finish(color=(0, 0, 0), width=1)
    # Curtain wall
    for col in range(8):
        x = 110 + col * 48
        shape4c.draw_rect(pymupdf.Rect(x, 400, x + 35, 560))
        shape4c.finish(color=(0.3, 0.5, 0.7), fill=(0.85, 0.92, 1.0), width=0.5)
    shape4c.commit()

    # Floor level markers
    for i, label in enumerate(["L1 (0'-0\")", "L2 (14'-6\")", "L3 (28'-0\")", "L4 (41'-6\")"]):
        page4.insert_text(pymupdf.Point(510, 305 - i * 40), label, fontsize=7, fontname="helv", color=(0.3, 0.3, 0.3))

    # --- Page 5: Mechanical Schedule ---
    page5 = doc.new_page(width=612, height=792)
    page5.insert_text(pymupdf.Point(72, 60), "MECHANICAL EQUIPMENT SCHEDULE", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.3))
    page5.insert_text(pymupdf.Point(72, 80), "Sheet M-101", fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))

    shape5 = page5.new_shape()
    shape5.draw_line(pymupdf.Point(72, 90), pymupdf.Point(540, 90))
    shape5.finish(color=(0.3, 0.3, 0.5), width=1)
    shape5.commit()

    # Equipment table
    headers = ["Tag", "Description", "Capacity", "Location", "Manufacturer"]
    col_widths = [50, 140, 80, 100, 100]
    x_start = 72
    y_start = 120

    # Header row background
    shape5b = page5.new_shape()
    shape5b.draw_rect(pymupdf.Rect(x_start, y_start - 15, x_start + sum(col_widths), y_start + 2))
    shape5b.finish(fill=(0.15, 0.15, 0.35), width=0)
    shape5b.commit()

    x = x_start
    for i, h in enumerate(headers):
        page5.insert_text(pymupdf.Point(x + 3, y_start), h, fontsize=8, fontname="hebo", color=(1, 1, 1))
        x += col_widths[i]

    equipment = [
        ("AHU-1", "Air Handling Unit - VAV", "25,000 CFM", "Mech Rm 101", "Trane"),
        ("AHU-2", "Air Handling Unit - VAV", "18,000 CFM", "Mech Rm 102", "Trane"),
        ("RTU-1", "Rooftop Packaged Unit", "15 Ton", "Roof", "Carrier"),
        ("RTU-2", "Rooftop Packaged Unit", "12 Ton", "Roof", "Carrier"),
        ("CHL-1", "Water-Cooled Chiller", "200 Ton", "Mech Rm 103", "York"),
        ("CHL-2", "Water-Cooled Chiller", "200 Ton", "Mech Rm 103", "York"),
        ("CT-1", "Cooling Tower", "400 Ton", "Roof", "Marley"),
        ("BLR-1", "Condensing Gas Boiler", "2,000 MBH", "Mech Rm 104", "Lochinvar"),
        ("BLR-2", "Condensing Gas Boiler", "2,000 MBH", "Mech Rm 104", "Lochinvar"),
        ("EF-1", "Exhaust Fan - Restroom", "1,200 CFM", "Roof", "Greenheck"),
        ("EF-2", "Exhaust Fan - Kitchen", "2,500 CFM", "Roof", "Greenheck"),
        ("P-1", "Chilled Water Pump", "75 HP", "Mech Rm 103", "Bell & Gossett"),
        ("P-2", "Hot Water Pump", "25 HP", "Mech Rm 104", "Bell & Gossett"),
    ]

    for r, row_data in enumerate(equipment):
        y = y_start + 20 + r * 18
        x = x_start
        # Alternating row color
        if r % 2 == 0:
            shape5c = page5.new_shape()
            shape5c.draw_rect(pymupdf.Rect(x_start, y - 12, x_start + sum(col_widths), y + 5))
            shape5c.finish(fill=(0.94, 0.94, 0.97), width=0)
            shape5c.commit()
        for c, val in enumerate(row_data):
            page5.insert_text(pymupdf.Point(x + 3, y), val, fontsize=8, fontname="helv", color=(0.1, 0.1, 0.1))
            x += col_widths[c]

    # Notes
    notes_y = y_start + 20 + len(equipment) * 18 + 30
    page5.insert_text(pymupdf.Point(72, notes_y), "NOTES:", fontsize=10, fontname="hebo", color=(0.2, 0.2, 0.2))
    notes = [
        "1. All equipment shall be installed per manufacturer's recommendations.",
        "2. Verify all rough-in dimensions prior to equipment delivery.",
        "3. Contractor to provide vibration isolation for all rotating equipment.",
        "4. See Specification Section 23 00 00 for detailed requirements.",
        "5. Equipment selections subject to final engineering approval.",
    ]
    for i, note in enumerate(notes):
        page5.insert_text(pymupdf.Point(72, notes_y + 20 + i * 16), note, fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2))

    # Set metadata
    doc.set_metadata({
        "title": "Greenfield Corporate Campus - Architectural Design Package",
        "author": "Thornton & Associates Architecture",
        "subject": "Architectural Blueprint - Permit Set Rev C",
        "creator": "CAD Export",
    })

    # Set TOC
    toc = [
        [1, "Title Page", 1],
        [1, "Site Plan Overview", 2],
        [1, "Ground Floor Plan", 3],
        [1, "Exterior Elevations", 4],
        [1, "Mechanical Schedule", 5],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince at page 3 (the floor plan page)
    launch_gui(f'evince --page-index=3 "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
