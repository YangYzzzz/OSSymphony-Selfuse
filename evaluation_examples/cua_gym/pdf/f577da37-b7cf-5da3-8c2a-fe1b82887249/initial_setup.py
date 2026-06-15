"""
Setup script for pdf_basic_151:
  Task: Open ~/Desktop/inspection_checklist.pdf in Evince, navigate to page 2,
        delete the existing highlight annotation on the word 'passed', then add
        a new red highlight to the word 'failed' on the same page. Save the document.

  Creates:
    - ~/Desktop/inspection_checklist.pdf  — 4-page inspection checklist PDF
                                            with a yellow highlight on 'passed'
                                            on page 2
"""

import os
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DESKTOP_DIR = os.path.expanduser("~/Desktop")
PDF_PATH = os.path.join(DESKTOP_DIR, "inspection_checklist.pdf")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI application on VM display without blocking."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        command.split(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_inspection_checklist():
    """Create a 4-page inspection checklist PDF with a yellow highlight on 'passed'."""
    doc = pymupdf.open()

    # --- Page 1: Header / Overview ---
    page1 = doc.new_page(width=612, height=792)
    page1.insert_text(pymupdf.Point(72, 72), "FACILITY INSPECTION CHECKLIST",
                      fontsize=18, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 110), "Inspection Date: 2024-06-15",
                      fontsize=12, fontname="helv", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 130), "Inspector: J. Martinez",
                      fontsize=12, fontname="helv", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 150), "Site: Building A - Manufacturing Floor",
                      fontsize=12, fontname="helv", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 190), "Section 1: General Safety",
                      fontsize=14, fontname="hebo", color=(0, 0, 0))
    lines_p1 = [
        "1.1  Emergency exits clearly marked and unobstructed ......... passed",
        "1.2  Fire extinguishers present and within service date ....... passed",
        "1.3  First aid kits stocked and accessible .................... passed",
        "1.4  Hazardous materials properly labeled and stored .......... passed",
        "1.5  Personal protective equipment available to all staff ..... passed",
    ]
    y = 220
    for line in lines_p1:
        page1.insert_text(pymupdf.Point(72, y), line, fontsize=11, fontname="helv",
                          color=(0, 0, 0))
        y += 22

    # --- Page 2: Structural / Equipment Checks ---
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 72), "Section 2: Structural & Equipment",
                      fontsize=14, fontname="hebo", color=(0, 0, 0))
    lines_p2 = [
        "2.1  Floor surfaces clean, dry, and free of obstacles ......... passed",
        "2.2  Machinery guards installed and in good condition .......... failed",
        "2.3  Electrical panels accessible, doors closed ............... passed",
        "2.4  Overhead crane inspected and load-tested ................. passed",
        "2.5  Ventilation systems operational .......................... failed",
        "2.6  Noise levels within acceptable limits .................... passed",
        "2.7  Lighting adequate throughout the facility ................ passed",
    ]
    y = 110
    for line in lines_p2:
        page2.insert_text(pymupdf.Point(72, y), line, fontsize=11, fontname="helv",
                          color=(0, 0, 0))
        y += 22

    page2.insert_text(pymupdf.Point(72, 290), "Notes:",
                      fontsize=12, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(72, 312),
                      "Item 2.2: Guard on lathe #3 requires immediate replacement.",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(72, 328),
                      "Item 2.5: HVAC unit in bay 4 is out of service pending repair.",
                      fontsize=10, fontname="helv", color=(0, 0, 0))

    # Add a yellow highlight on the FIRST occurrence of 'passed' on page 2
    instances = page2.search_for("passed")
    if instances:
        highlight = page2.add_highlight_annot(instances[0])
        highlight.set_colors(stroke=(1, 1, 0))  # yellow
        highlight.update()

    # --- Page 3: Environmental / Compliance ---
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(72, 72), "Section 3: Environmental Compliance",
                      fontsize=14, fontname="hebo", color=(0, 0, 0))
    lines_p3 = [
        "3.1  Waste disposal procedures followed ...................... passed",
        "3.2  Chemical storage compliant with regulations ............. passed",
        "3.3  Spill containment equipment in place .................... failed",
        "3.4  Air emissions within permit limits ...................... passed",
        "3.5  Water discharge managed and monitored ................... passed",
    ]
    y = 110
    for line in lines_p3:
        page3.insert_text(pymupdf.Point(72, y), line, fontsize=11, fontname="helv",
                          color=(0, 0, 0))
        y += 22

    # --- Page 4: Summary ---
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(pymupdf.Point(72, 72), "Inspection Summary",
                      fontsize=16, fontname="hebo", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(72, 110),
                      "Total items inspected: 17",
                      fontsize=12, fontname="helv", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(72, 132),
                      "Items passed: 13",
                      fontsize=12, fontname="helv", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(72, 154),
                      "Items failed: 3",
                      fontsize=12, fontname="helv", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(72, 176),
                      "Items N/A: 1",
                      fontsize=12, fontname="helv", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(72, 218),
                      "Corrective actions required: See items 2.2, 2.5, 3.3",
                      fontsize=11, fontname="helv", color=(0.7, 0, 0))
    page4.insert_text(pymupdf.Point(72, 260),
                      "Inspector Signature: _________________________",
                      fontsize=11, fontname="helv", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(72, 290),
                      "Date: ___________________",
                      fontsize=11, fontname="helv", color=(0, 0, 0))

    os.makedirs(DESKTOP_DIR, exist_ok=True)
    doc.save(PDF_PATH)
    doc.close()
    print(f"Created: {PDF_PATH}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def create_initial():
    """Create initial state and launch Evince on page 2."""
    create_inspection_checklist()
    # Open at page 2 (0-indexed → --page-index=1)
    launch_gui(f'evince --page-index=1 "{PDF_PATH}"', delay_sec=2.0)


create_initial()
