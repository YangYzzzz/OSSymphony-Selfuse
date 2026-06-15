"""
Initial Setup: Create a manual PDF with misordered pages for page-order verification task.
Task ID: pdf_cr_064
Domain: pdf

Creates /home/user/Desktop/manual.pdf - an 8-page manual where each page has a
printed page number ("Page N") but some pages are physically out of order.
Specifically: physical positions are [1, 3, 2, 4, 6, 5, 7, 8] meaning
pages 2&3 are swapped and pages 5&6 are swapped.
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user/Desktop'
TASK_ID = 'pdf_cr_064'
OUTPUT = f'{WORKDIR}/manual.pdf'

# Page dimensions (Letter size)
WIDTH, HEIGHT = 612, 792

# The printed page numbers in physical order.
# Physical page 1 has "Page 1", physical page 2 has "Page 3", etc.
PRINTED_ORDER = [1, 3, 2, 4, 6, 5, 7, 8]

# Manual chapter titles corresponding to the printed page number
CHAPTER_CONTENT = {
    1: ("Introduction", "Welcome to the Equipment Operations Manual. This document provides comprehensive guidelines for the safe and efficient operation of industrial machinery in your facility. All personnel must read this manual before operating any equipment."),
    2: ("Safety Protocols", "Before operating any machinery, ensure all safety guards are in place. Personal protective equipment (PPE) including safety glasses, steel-toed boots, and hearing protection must be worn at all times. Emergency stop buttons are located on each machine panel."),
    3: ("Equipment Overview", "The Model X-450 CNC milling machine features a 3-axis configuration with automated tool changer. Maximum spindle speed is 12,000 RPM with a working envelope of 800mm x 500mm x 400mm. The control panel is located on the right side of the unit."),
    4: ("Operating Procedures", "Step 1: Power on the main breaker located at the rear of the machine. Step 2: Initialize the control system by pressing the green START button. Step 3: Load the workpiece onto the fixture table and secure with appropriate clamps. Step 4: Load the G-code program via USB or network transfer."),
    5: ("Maintenance Schedule", "Daily: Check coolant levels and top off as needed. Weekly: Inspect drive belts for wear and tension. Monthly: Lubricate all linear guide rails using ISO VG 68 oil. Quarterly: Replace spindle filters and calibrate tool length sensors. Annually: Full alignment check by certified technician."),
    6: ("Troubleshooting", "Error E-101: Spindle overload detected. Reduce feed rate or depth of cut. Error E-205: Coolant pressure low. Check pump and filter for blockages. Error E-310: Axis limit reached. Verify workpiece coordinates and home position. Error E-415: Tool breakage detected. Replace tool and re-run tool length measurement."),
    7: ("Warranty Information", "This equipment is covered under a 24-month limited warranty from date of purchase. Coverage includes manufacturing defects in materials and workmanship. Consumable parts such as cutting tools, filters, and belts are excluded. Contact ServicePro International at 1-800-555-0147 for warranty claims."),
    8: ("Appendix: Technical Specifications", "Power requirement: 480V 3-phase 60Hz, 30A. Machine weight: 4,200 kg. Footprint: 2.1m x 1.8m x 2.3m (L x W x H). Positional accuracy: +/- 0.005mm. Repeatability: +/- 0.003mm. Maximum workpiece weight: 250 kg. Control system: Fanuc 0i-MF Plus."),
}

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

    doc = pymupdf.open()

    for physical_pos, printed_num in enumerate(PRINTED_ORDER, 1):
        page = doc.new_page(width=WIDTH, height=HEIGHT)
        title, body_text = CHAPTER_CONTENT[printed_num]

        # Header line
        page.insert_text(
            pymupdf.Point(72, 50),
            "Equipment Operations Manual",
            fontsize=10,
            fontname="heit",
            color=(0.4, 0.4, 0.4),
        )

        # Horizontal rule under header
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 58), pymupdf.Point(540, 58))
        shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape.commit()

        # Chapter title
        page.insert_text(
            pymupdf.Point(72, 100),
            f"Chapter {printed_num}: {title}",
            fontsize=18,
            fontname="hebo",
            color=(0.1, 0.1, 0.4),
        )

        # Body text
        body_rect = pymupdf.Rect(72, 130, 540, 700)
        page.insert_textbox(
            body_rect,
            body_text,
            fontsize=12,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Footer with printed page number
        footer_text = f"Page {printed_num}"
        page.insert_text(
            pymupdf.Point(280, 760),
            footer_text,
            fontsize=11,
            fontname="helv",
            color=(0.3, 0.3, 0.3),
        )

        # Footer rule
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(72, 740), pymupdf.Point(540, 740))
        shape2.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape2.commit()

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')

create_initial()
