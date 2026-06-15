"""
Initial Setup: Create a single-page promotional flyer PDF
Task ID: pdf_ro_039
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_039'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/flyer.pdf'


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
    # Create a single Letter-size page (promotional flyer)
    page = doc.new_page(width=612, height=792)

    # --- Header banner background ---
    shape = page.new_shape()
    # Top banner rectangle
    shape.draw_rect(pymupdf.Rect(0, 0, 612, 140))
    shape.finish(color=None, fill=(0.16, 0.31, 0.60))  # Deep blue fill
    shape.commit()

    # --- Title text ---
    page.insert_text(
        pymupdf.Point(72, 55),
        "GRAND OPENING",
        fontsize=36,
        fontname="hebo",
        color=(1, 1, 1),  # White
    )

    page.insert_text(
        pymupdf.Point(72, 85),
        "Riverside Community Arts Center",
        fontsize=18,
        fontname="helv",
        color=(0.85, 0.90, 1.0),
    )

    page.insert_text(
        pymupdf.Point(72, 115),
        "Saturday, June 14, 2025 | 10:00 AM - 6:00 PM",
        fontsize=12,
        fontname="heit",
        color=(0.85, 0.90, 1.0),
    )

    # --- Decorative line ---
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(72, 160), pymupdf.Point(540, 160))
    shape2.finish(color=(0.16, 0.31, 0.60), width=2)
    shape2.commit()

    # --- Event description ---
    desc_rect = pymupdf.Rect(72, 175, 540, 310)
    page.insert_textbox(
        desc_rect,
        "Join us for the grand opening of the Riverside Community Arts Center! "
        "Experience a day filled with live performances, interactive art workshops, "
        "local food vendors, and family-friendly activities. Our new 15,000 sq ft "
        "facility features a 200-seat theater, three gallery spaces, ceramics studio, "
        "and a rooftop sculpture garden overlooking the Willamette River.\n\n"
        "Admission is FREE. All ages welcome.",
        fontsize=11,
        fontname="helv",
        color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # --- Schedule section header ---
    shape3 = page.new_shape()
    shape3.draw_rect(pymupdf.Rect(72, 320, 540, 348))
    shape3.finish(color=None, fill=(0.93, 0.94, 0.97))
    shape3.commit()

    page.insert_text(
        pymupdf.Point(80, 340),
        "EVENT SCHEDULE",
        fontsize=13,
        fontname="hebo",
        color=(0.16, 0.31, 0.60),
    )

    # --- Schedule items ---
    schedule = [
        ("10:00 AM", "Opening Ceremony & Ribbon Cutting"),
        ("10:30 AM", "Gallery Walk: 'Visions of the Pacific Northwest'"),
        ("11:00 AM", "Kids' Art Workshop: Paint Your Own Canvas"),
        ("12:00 PM", "Live Jazz Performance by The River Quintet"),
        ("1:00 PM", "Ceramics Demonstration with Maria Gonzalez"),
        ("2:00 PM", "Poetry Reading: Local Authors Showcase"),
        ("3:00 PM", "Dance Performance by Cascade Youth Ballet"),
        ("4:00 PM", "Sculpture Garden Tour & Outdoor Reception"),
        ("5:00 PM", "Closing Remarks & Community Art Unveiling"),
    ]

    y_pos = 365
    for time_str, event in schedule:
        page.insert_text(
            pymupdf.Point(90, y_pos),
            time_str,
            fontsize=9,
            fontname="hebo",
            color=(0.16, 0.31, 0.60),
        )
        page.insert_text(
            pymupdf.Point(170, y_pos),
            event,
            fontsize=9,
            fontname="helv",
            color=(0.2, 0.2, 0.2),
        )
        y_pos += 18

    # --- Decorative divider ---
    shape4 = page.new_shape()
    shape4.draw_line(pymupdf.Point(72, y_pos + 10), pymupdf.Point(540, y_pos + 10))
    shape4.finish(color=(0.80, 0.82, 0.88), width=1)
    shape4.commit()

    # --- Sponsors / Info section ---
    info_y = y_pos + 30
    page.insert_text(
        pymupdf.Point(72, info_y),
        "LOCATION & CONTACT",
        fontsize=11,
        fontname="hebo",
        color=(0.16, 0.31, 0.60),
    )

    info_lines = [
        "Riverside Community Arts Center",
        "2450 River Road, Portland, OR 97201",
        "Phone: (503) 555-0147  |  Email: info@riversidearts.org",
        "Web: www.riversidearts.org",
    ]
    info_y += 18
    for line in info_lines:
        page.insert_text(
            pymupdf.Point(72, info_y),
            line,
            fontsize=9,
            fontname="helv",
            color=(0.3, 0.3, 0.3),
        )
        info_y += 14

    # --- Footer banner ---
    shape5 = page.new_shape()
    shape5.draw_rect(pymupdf.Rect(0, 740, 612, 792))
    shape5.finish(color=None, fill=(0.16, 0.31, 0.60))
    shape5.commit()

    page.insert_text(
        pymupdf.Point(72, 768),
        "Free Parking Available  |  Wheelchair Accessible  |  ASL Interpreters On-Site",
        fontsize=8,
        fontname="helv",
        color=(1, 1, 1),
    )

    # --- Decorative shapes ---
    shape6 = page.new_shape()
    # Small colored circles for visual flair
    for cx, clr in [(500, (0.90, 0.30, 0.25)), (520, (0.20, 0.65, 0.40)), (540, (0.95, 0.70, 0.15))]:
        shape6.draw_circle(pymupdf.Point(cx, 130), 6)
        shape6.finish(color=None, fill=clr)
    shape6.commit()

    # Set metadata
    doc.set_metadata({
        "title": "Grand Opening - Riverside Community Arts Center",
        "author": "Riverside Arts Foundation",
        "subject": "Grand Opening Event Flyer",
        "creator": "Design Team",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Launch Evince to show the flyer
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
