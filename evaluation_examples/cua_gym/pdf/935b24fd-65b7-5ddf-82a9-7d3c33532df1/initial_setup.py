"""
Initial Setup: Create a scanned police report PDF (image-only, no text layer)
Task ID: pdf_legal_069
Domain: pdf

Creates a 3-page scanned police report at /home/user/legal/personal_injury/police_report_scan.pdf
The pages are rendered as images (no searchable text layer) to simulate a scanned document.
"""

import os
import shlex
import subprocess
import time

# We use reportlab to create realistic typed text, then render pages to images via PyMuPDF,
# then reassemble as image-only PDF.

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_069'
OUTPUT_DIR = f'{WORKDIR}/legal/personal_injury'
OUTPUT = f'{OUTPUT_DIR}/police_report_scan.pdf'


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


def create_source_pdf(tmp_path):
    """Create a realistic police report PDF with text (temporary, will be converted to images)."""
    import pymupdf

    doc = pymupdf.open()

    # ========== PAGE 1: Report Header & Incident Information ==========
    page1 = doc.new_page(width=612, height=792)  # Letter size

    # Header box
    shape = page1.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 30, 576, 90))
    shape.finish(color=(0, 0, 0), width=2)
    shape.draw_line(pymupdf.Point(36, 60), pymupdf.Point(576, 60))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    page1.insert_text(pymupdf.Point(180, 52), "MILLBROOK POLICE DEPARTMENT", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(220, 82), "TRAFFIC CRASH REPORT", fontsize=11, fontname="hebo", color=(0, 0, 0))

    # Report number and date fields
    page1.insert_text(pymupdf.Point(40, 115), "Report No:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(105, 115), "MPD-2025-04817", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(300, 115), "Date of Report:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(385, 115), "03/14/2025", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(40, 135), "Date of Crash:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(125, 135), "03/13/2025", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(300, 135), "Time of Crash:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(385, 135), "17:42", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(40, 155), "Day of Week:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(120, 155), "Thursday", fontsize=9, fontname="helv", color=(0, 0, 0))

    # Section: Location
    shape = page1.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 170, 576, 190))
    shape.finish(color=(0, 0, 0), fill=(0.9, 0.9, 0.9), width=1)
    shape.commit()
    page1.insert_text(pymupdf.Point(40, 185), "LOCATION OF CRASH", fontsize=9, fontname="hebo", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(40, 210), "Street/Highway:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(135, 210), "Westbound SR-44 at intersection with Oak Ridge Blvd", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(40, 230), "City:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(70, 230), "Millbrook", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(200, 230), "County:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(245, 230), "Elmore", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(350, 230), "State:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(385, 230), "Alabama", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(40, 250), "Latitude:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(95, 250), "32.4982", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(200, 250), "Longitude:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(260, 250), "-86.3694", fontsize=9, fontname="helv", color=(0, 0, 0))

    # Section: Crash Type checkboxes
    shape = page1.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 270, 576, 290))
    shape.finish(color=(0, 0, 0), fill=(0.9, 0.9, 0.9), width=1)
    shape.commit()
    page1.insert_text(pymupdf.Point(40, 285), "CRASH CLASSIFICATION", fontsize=9, fontname="hebo", color=(0, 0, 0))

    # Checkboxes - simulated
    checkbox_items = [
        ("Property Damage Only", False, 40, 310),
        ("Injury", True, 200, 310),
        ("Fatal", False, 300, 310),
        ("Hit and Run", False, 380, 310),
    ]
    for label, checked, x, y in checkbox_items:
        shape = page1.new_shape()
        shape.draw_rect(pymupdf.Rect(x, y - 10, x + 10, y))
        shape.finish(color=(0, 0, 0), width=0.8)
        shape.commit()
        if checked:
            # Draw X inside checkbox
            page1.insert_text(pymupdf.Point(x + 1, y - 1), "X", fontsize=9, fontname="hebo", color=(0, 0, 0))
        page1.insert_text(pymupdf.Point(x + 14, y), label, fontsize=8, fontname="helv", color=(0, 0, 0))

    # Weather / Road conditions
    shape = page1.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 330, 576, 350))
    shape.finish(color=(0, 0, 0), fill=(0.9, 0.9, 0.9), width=1)
    shape.commit()
    page1.insert_text(pymupdf.Point(40, 345), "CONDITIONS", fontsize=9, fontname="hebo", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(40, 370), "Weather:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(95, 370), "Clear", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(200, 370), "Road Surface:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(280, 370), "Dry", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(350, 370), "Lighting:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(400, 370), "Daylight", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(40, 390), "Traffic Control:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(130, 390), "Signal light (functioning)", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(350, 390), "Speed Limit:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(420, 390), "45 mph", fontsize=9, fontname="helv", color=(0, 0, 0))

    # Section: Reporting Officer
    shape = page1.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 410, 576, 430))
    shape.finish(color=(0, 0, 0), fill=(0.9, 0.9, 0.9), width=1)
    shape.commit()
    page1.insert_text(pymupdf.Point(40, 425), "REPORTING OFFICER", fontsize=9, fontname="hebo", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(40, 450), "Officer Name:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(120, 450), "Sgt. James R. Whitfield", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(300, 450), "Badge No:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(360, 450), "2741", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(430, 450), "Unit:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(460, 450), "Patrol Division B", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(40, 470), "Agency:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(90, 470), "Millbrook Police Department", fontsize=9, fontname="helv", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(300, 470), "ORI:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(330, 470), "AL0260200", fontsize=9, fontname="helv", color=(0, 0, 0))

    # Handwritten note at bottom of page 1
    page1.insert_text(pymupdf.Point(40, 520), "Officer Notes:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    # Simulate handwriting with italic courier
    page1.insert_text(pymupdf.Point(40, 540), "Arrived on scene at 17:48. Both vehicles still in", fontsize=9, fontname="coit", color=(0.15, 0.15, 0.4))
    page1.insert_text(pymupdf.Point(40, 555), "intersection. EMS already dispatched. Driver 1", fontsize=9, fontname="coit", color=(0.15, 0.15, 0.4))
    page1.insert_text(pymupdf.Point(40, 570), "complaining of neck pain. See page 3 for full narrative.", fontsize=9, fontname="coit", color=(0.15, 0.15, 0.4))

    # Footer
    page1.insert_text(pymupdf.Point(250, 760), "Page 1 of 3", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))

    # ========== PAGE 2: Involved Parties & Vehicle Information ==========
    page2 = doc.new_page(width=612, height=792)

    # Driver 1 section
    shape = page2.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 30, 576, 50))
    shape.finish(color=(0, 0, 0), fill=(0.9, 0.9, 0.9), width=1)
    shape.commit()
    page2.insert_text(pymupdf.Point(40, 45), "DRIVER / VEHICLE 1", fontsize=9, fontname="hebo", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(40, 70), "Name:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(80, 70), "Martinez, Elena Sophia", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(300, 70), "DOB:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(330, 70), "08/22/1989", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(430, 70), "Sex:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(455, 70), "F", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(40, 90), "Address:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(95, 90), "1247 Magnolia Drive, Millbrook, AL 36054", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(40, 110), "DL No:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(85, 110), "8471293", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(200, 110), "DL State:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(255, 110), "AL", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(320, 110), "Insurance:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(380, 110), "State Farm #SF-4429817", fontsize=9, fontname="helv", color=(0, 0, 0))

    # Vehicle 1
    page2.insert_text(pymupdf.Point(40, 140), "Vehicle:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(90, 140), "2021 Honda Accord EX-L", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(300, 140), "Color:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(335, 140), "Silver", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(40, 160), "License Plate:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(120, 160), "AL 7BC-4921", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(300, 160), "VIN:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(330, 160), "1HGCV2F34MA019845", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(40, 180), "Damage:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(95, 180), "Front-end: hood, bumper, radiator. Airbags deployed.", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(40, 200), "Towed:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(80, 200), "Yes - Carter's Towing, Millbrook", fontsize=9, fontname="helv", color=(0, 0, 0))

    # Injury info
    page2.insert_text(pymupdf.Point(40, 220), "Injury:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(80, 220), "Cervical strain (neck), contusion to left wrist. Transported by EMS to Baptist South.", fontsize=8, fontname="helv", color=(0, 0, 0))

    # Divider
    shape = page2.new_shape()
    shape.draw_line(pymupdf.Point(36, 245), pymupdf.Point(576, 245))
    shape.finish(color=(0, 0, 0), width=1.5)
    shape.commit()

    # Driver 2 section
    shape = page2.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 255, 576, 275))
    shape.finish(color=(0, 0, 0), fill=(0.9, 0.9, 0.9), width=1)
    shape.commit()
    page2.insert_text(pymupdf.Point(40, 270), "DRIVER / VEHICLE 2", fontsize=9, fontname="hebo", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(40, 295), "Name:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(80, 295), "Thompson, David Allen", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(300, 295), "DOB:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(330, 295), "11/05/1974", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(430, 295), "Sex:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(455, 295), "M", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(40, 315), "Address:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(95, 315), "892 Pine Valley Court, Prattville, AL 36067", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(40, 335), "DL No:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(85, 335), "5839201", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(200, 335), "DL State:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(255, 335), "AL", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(320, 335), "Insurance:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(380, 335), "GEICO #GK-9918274", fontsize=9, fontname="helv", color=(0, 0, 0))

    # Vehicle 2
    page2.insert_text(pymupdf.Point(40, 365), "Vehicle:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(90, 365), "2019 Ford F-150 XLT", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(300, 365), "Color:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(335, 365), "White", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(40, 385), "License Plate:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(120, 385), "AL 3DF-8803", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(300, 385), "VIN:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(330, 385), "1FTEW1EP4KFA38291", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(40, 405), "Damage:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(95, 405), "Driver-side door, quarter panel dented. Driveable.", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(40, 425), "Towed:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(80, 425), "No", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(40, 445), "Injury:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(80, 445), "None reported. Refused medical attention.", fontsize=9, fontname="helv", color=(0, 0, 0))

    # Witness section
    shape = page2.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 475, 576, 495))
    shape.finish(color=(0, 0, 0), fill=(0.9, 0.9, 0.9), width=1)
    shape.commit()
    page2.insert_text(pymupdf.Point(40, 490), "WITNESSES", fontsize=9, fontname="hebo", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(40, 515), "1. Name:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(95, 515), "Patricia Owens", fontsize=9, fontname="helv", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(250, 515), "Phone:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(290, 515), "(334) 555-8192", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(55, 535), "Address:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(105, 535), "405 Deatsville Hwy, Millbrook, AL 36054", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(55, 555), "Statement:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(55, 572), "\"I was stopped at the red light on Oak Ridge facing north. The silver car", fontsize=8, fontname="coit", color=(0.15, 0.15, 0.4))
    page2.insert_text(pymupdf.Point(55, 585), "ran the red light going west on SR-44 and the truck hit it on the side.\"", fontsize=8, fontname="coit", color=(0.15, 0.15, 0.4))

    page2.insert_text(pymupdf.Point(40, 615), "2. Name:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(95, 615), "Robert Kim", fontsize=9, fontname="helv", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(250, 615), "Phone:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(290, 615), "(334) 555-3047", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(55, 635), "Address:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(105, 635), "7621 Coosada Road, Wetumpka, AL 36092", fontsize=9, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(55, 655), "Statement:", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(55, 672), "\"I was behind the truck heading south on Oak Ridge. The Honda came", fontsize=8, fontname="coit", color=(0.15, 0.15, 0.4))
    page2.insert_text(pymupdf.Point(55, 685), "through without stopping. The truck couldn't avoid it.\"", fontsize=8, fontname="coit", color=(0.15, 0.15, 0.4))

    # Footer
    page2.insert_text(pymupdf.Point(250, 760), "Page 2 of 3", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))

    # ========== PAGE 3: Narrative, Diagram, Signature ==========
    page3 = doc.new_page(width=612, height=792)

    # Narrative section
    shape = page3.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 30, 576, 50))
    shape.finish(color=(0, 0, 0), fill=(0.9, 0.9, 0.9), width=1)
    shape.commit()
    page3.insert_text(pymupdf.Point(40, 45), "OFFICER NARRATIVE", fontsize=9, fontname="hebo", color=(0, 0, 0))

    narrative_lines = [
        "On Thursday, March 13, 2025, at approximately 17:42 hours, I was dispatched to the intersection",
        "of SR-44 and Oak Ridge Blvd regarding a two-vehicle traffic crash with injuries.",
        "",
        "Upon arrival at 17:48 hours, I observed a silver 2021 Honda Accord (Vehicle 1) and a white",
        "2019 Ford F-150 (Vehicle 2) in the southeast quadrant of the intersection. Vehicle 1 had",
        "significant front-end damage and fluid leakage. Vehicle 2 had moderate damage to the",
        "driver-side door and quarter panel.",
        "",
        "Investigation revealed that Vehicle 1, operated by Elena S. Martinez, was traveling westbound on",
        "SR-44. Vehicle 2, operated by David A. Thompson, was traveling southbound on Oak Ridge Blvd.",
        "According to witness statements and traffic signal analysis, Vehicle 1 entered the intersection",
        "against a red signal. Vehicle 2 had a green signal and struck Vehicle 1 in a T-bone collision",
        "on the driver side.",
        "",
        "Martinez stated she \"thought the light was still yellow\" but acknowledged she may have",
        "misjudged. Thompson stated he had a green light and could not stop in time.",
        "",
        "Martinez complained of neck pain and left wrist pain. She was evaluated by EMS (Unit A-7) and",
        "transported to Baptist Medical Center South for further evaluation. Thompson was uninjured and",
        "refused medical evaluation.",
        "",
        "Traffic signal camera footage has been requested from City Traffic Engineering (reference",
        "request #TE-2025-0314-001).",
        "",
        "Based on physical evidence, witness statements, and my investigation, Driver 1 (Martinez) is",
        "cited for: Disregarding a Traffic Control Device, Alabama Code Section 32-5A-32.",
        "",
        "Citation Number: MC-2025-07841",
    ]

    y = 72
    for line in narrative_lines:
        if line:
            page3.insert_text(pymupdf.Point(45, y), line, fontsize=8.5, fontname="helv", color=(0, 0, 0))
        y += 14

    # Diagram area
    y_diag = y + 10
    shape = page3.new_shape()
    shape.draw_rect(pymupdf.Rect(36, y_diag, 576, y_diag + 20))
    shape.finish(color=(0, 0, 0), fill=(0.9, 0.9, 0.9), width=1)
    shape.commit()
    page3.insert_text(pymupdf.Point(40, y_diag + 15), "CRASH DIAGRAM (see attached)", fontsize=9, fontname="hebo", color=(0, 0, 0))

    # Simple intersection diagram
    diag_y = y_diag + 30
    shape = page3.new_shape()
    # Horizontal road
    shape.draw_rect(pymupdf.Rect(150, diag_y + 30, 450, diag_y + 70))
    shape.finish(color=(0.5, 0.5, 0.5), fill=(0.85, 0.85, 0.85), width=0.5)
    # Vertical road
    shape.draw_rect(pymupdf.Rect(270, diag_y, 330, diag_y + 100))
    shape.finish(color=(0.5, 0.5, 0.5), fill=(0.85, 0.85, 0.85), width=0.5)
    shape.commit()

    page3.insert_text(pymupdf.Point(155, diag_y + 25), "SR-44 (WB)", fontsize=7, fontname="helv", color=(0.3, 0.3, 0.3))
    page3.insert_text(pymupdf.Point(335, diag_y + 12), "Oak Ridge (SB)", fontsize=7, fontname="helv", color=(0.3, 0.3, 0.3))

    # Collision point
    page3.insert_text(pymupdf.Point(285, diag_y + 55), "X", fontsize=14, fontname="hebo", color=(1, 0, 0))

    # Signature section
    sig_y = diag_y + 120
    shape = page3.new_shape()
    shape.draw_rect(pymupdf.Rect(36, sig_y, 576, sig_y + 20))
    shape.finish(color=(0, 0, 0), fill=(0.9, 0.9, 0.9), width=1)
    shape.commit()
    page3.insert_text(pymupdf.Point(40, sig_y + 15), "OFFICER CERTIFICATION", fontsize=9, fontname="hebo", color=(0, 0, 0))

    page3.insert_text(pymupdf.Point(40, sig_y + 40), "I certify that the information contained in this report is accurate to the best of my knowledge.", fontsize=8, fontname="helv", color=(0, 0, 0))

    # Simulated signature
    page3.insert_text(pymupdf.Point(40, sig_y + 65), "Sgt. James R. Whitfield", fontsize=11, fontname="tiit", color=(0.1, 0.1, 0.3))
    shape = page3.new_shape()
    shape.draw_line(pymupdf.Point(40, sig_y + 70), pymupdf.Point(200, sig_y + 70))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    page3.insert_text(pymupdf.Point(40, sig_y + 82), "Signature", fontsize=7, fontname="helv", color=(0.4, 0.4, 0.4))

    page3.insert_text(pymupdf.Point(250, sig_y + 65), "03/14/2025", fontsize=9, fontname="helv", color=(0, 0, 0))
    shape = page3.new_shape()
    shape.draw_line(pymupdf.Point(250, sig_y + 70), pymupdf.Point(350, sig_y + 70))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    page3.insert_text(pymupdf.Point(250, sig_y + 82), "Date", fontsize=7, fontname="helv", color=(0.4, 0.4, 0.4))

    page3.insert_text(pymupdf.Point(400, sig_y + 65), "Badge #2741", fontsize=9, fontname="helv", color=(0, 0, 0))
    shape = page3.new_shape()
    shape.draw_line(pymupdf.Point(400, sig_y + 70), pymupdf.Point(500, sig_y + 70))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    page3.insert_text(pymupdf.Point(400, sig_y + 82), "Badge Number", fontsize=7, fontname="helv", color=(0.4, 0.4, 0.4))

    # Footer
    page3.insert_text(pymupdf.Point(250, 760), "Page 3 of 3", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))

    doc.save(tmp_path)
    doc.close()


def convert_to_scanned(tmp_path, output_path):
    """Convert the text PDF to an image-only PDF (simulating a scan).
    Renders each page as an image and reassembles into a new PDF with no text layer."""
    import pymupdf

    src = pymupdf.open(tmp_path)
    out = pymupdf.open()

    for i in range(src.page_count):
        page = src[i]
        # Render at 200 DPI for realistic scan quality
        mat = pymupdf.Matrix(200 / 72, 200 / 72)
        pix = page.get_pixmap(matrix=mat)

        # Add slight gray tint to simulate scan
        # Create new page same size
        new_page = out.new_page(width=page.rect.width, height=page.rect.height)
        img_rect = pymupdf.Rect(0, 0, page.rect.width, page.rect.height)
        new_page.insert_image(img_rect, pixmap=pix)

    out.save(output_path)
    out.close()
    src.close()


def create_initial():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    tmp_path = '/tmp/police_report_source.pdf'

    # Step 1: Create a text-based source PDF
    create_source_pdf(tmp_path)

    # Step 2: Convert to image-only (scanned) PDF
    convert_to_scanned(tmp_path, OUTPUT)

    # Clean up temp
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

    print(f'Initial file created: {OUTPUT}')

    # Verify no text layer
    import pymupdf
    doc = pymupdf.open(OUTPUT)
    for i in range(doc.page_count):
        text = doc[i].get_text("text").strip()
        if text:
            print(f'WARNING: Page {i} has text: {text[:50]}...')
        else:
            print(f'Page {i}: no text layer (image-only scan) - OK')
    print(f'Total pages: {doc.page_count}')
    doc.close()

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
