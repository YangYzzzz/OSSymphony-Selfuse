"""
Initial Setup: Create accident report PDF with 6 embedded photographs
Task ID: pdf_legal_079
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

from PIL import Image, ImageDraw, ImageFont
import io
import random

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_079'
REPORT_DIR = f'{WORKDIR}/legal/personal_injury'
OUTPUT = f'{REPORT_DIR}/accident_report.pdf'
PHOTOS_DIR = f'{REPORT_DIR}/photos'


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


def create_synthetic_photo(width, height, label, color_base):
    """Create a synthetic photograph-like image with realistic appearance."""
    img = Image.new("RGB", (width, height), color_base)
    draw = ImageDraw.Draw(img)

    # Add some visual elements to make it look like a photo
    random.seed(hash(label))

    # Gradient background to simulate a scene
    for y in range(height):
        r = int(color_base[0] + (y / height) * 40 - 20)
        g = int(color_base[1] + (y / height) * 30 - 15)
        b = int(color_base[2] + (y / height) * 20 - 10)
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add shapes to simulate scene elements
    for _ in range(random.randint(3, 8)):
        x1 = random.randint(0, width - 50)
        y1 = random.randint(0, height - 50)
        x2 = x1 + random.randint(20, 100)
        y2 = y1 + random.randint(20, 80)
        shade = random.randint(60, 200)
        draw.rectangle([x1, y1, x2, y2], fill=(shade, shade - 20, shade - 10))

    # Add label text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
    draw.text((10, height - 30), label, fill=(255, 255, 255), font=font)

    # Add timestamp overlay
    draw.text((width - 180, height - 30), "2025-11-14 09:47", fill=(255, 255, 0), font=font)

    return img


def create_initial():
    # Create directory structure
    os.makedirs(REPORT_DIR, exist_ok=True)
    os.makedirs(PHOTOS_DIR, exist_ok=True)

    # Create 6 synthetic photographs
    photo_specs = [
        (640, 480, "Scene Overview - Intersection", (100, 120, 140)),
        (640, 480, "Vehicle Damage - Front", (80, 70, 65)),
        (480, 640, "Vehicle Damage - Rear", (90, 80, 70)),
        (640, 480, "Road Conditions - Skid Marks", (110, 110, 100)),
        (640, 480, "Traffic Signal - North", (70, 90, 130)),
        (480, 640, "Witness Perspective - East", (95, 105, 90)),
    ]

    photo_images = []
    for w, h, label, color in photo_specs:
        img = create_synthetic_photo(w, h, label, color)
        photo_images.append(img)

    # Build the PDF report
    doc = pymupdf.open()

    # ---- Page 1: Cover Page ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 120), "ACCIDENT INVESTIGATION REPORT",
                     fontsize=22, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 160), "Case No. PI-2025-4471",
                     fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 180), pymupdf.Point(540, 180))
    shape.finish(color=(0.1, 0.1, 0.4), width=2)
    shape.commit()

    details = [
        ("Date of Incident:", "November 14, 2025"),
        ("Time of Incident:", "09:47 AM EST"),
        ("Location:", "Intersection of Oak Boulevard & Maple Avenue, Hartford, CT 06103"),
        ("Reporting Officer:", "Sgt. Daniel Morales, Badge #4892"),
        ("Prepared By:", "Forensic Reconstruction Unit, Hartford PD"),
        ("Report Date:", "November 21, 2025"),
        ("Classification:", "Personal Injury - Multi-Vehicle Collision"),
        ("Status:", "Under Investigation"),
    ]
    y = 220
    for label, value in details:
        page.insert_text(pymupdf.Point(72, y), label, fontsize=11, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(230, y), value, fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))
        y += 22

    page.insert_text(pymupdf.Point(72, y + 30), "CONFIDENTIAL - LAW ENFORCEMENT SENSITIVE",
                     fontsize=10, fontname="hebo", color=(0.7, 0, 0))

    # ---- Page 2: Executive Summary ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "1. EXECUTIVE SUMMARY", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    summary_text = (
        "On November 14, 2025, at approximately 09:47 AM, a multi-vehicle collision occurred at the "
        "intersection of Oak Boulevard and Maple Avenue in Hartford, Connecticut. The incident involved "
        "three vehicles: a 2023 Toyota Camry (Vehicle A), a 2022 Ford F-150 (Vehicle B), and a 2024 "
        "Honda Civic (Vehicle C). Vehicle A, operated by Ms. Rachel Torres (DOB: 03/15/1988), was "
        "traveling northbound on Oak Boulevard when it entered the intersection on a yellow traffic signal. "
        "Vehicle B, operated by Mr. Kenneth Okafor (DOB: 07/22/1975), was traveling westbound on Maple "
        "Avenue and entered the intersection after the signal changed to green. The resulting T-bone "
        "collision caused Vehicle A to spin counterclockwise and strike Vehicle C, which was stopped at "
        "the southbound red light. Three individuals sustained injuries requiring medical transport to "
        "Hartford Hospital. Ms. Torres suffered a fractured left femur and multiple contusions. "
        "Mr. Okafor reported neck pain and was diagnosed with cervical strain. The rear passenger in "
        "Vehicle C, Ms. Diane Whitfield (DOB: 11/03/1992), sustained a mild concussion."
    )
    rect = pymupdf.Rect(72, 85, 540, 400)
    page.insert_textbox(rect, summary_text, fontsize=10.5, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 420), "2. PARTIES INVOLVED", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    parties_text = (
        "Vehicle A (2023 Toyota Camry, Silver, CT Plate: AB-34521)\n"
        "  Driver: Rachel Torres, 37, of 145 Elm Street, West Hartford, CT\n"
        "  Insurance: Progressive Policy #CTX-7891234\n\n"
        "Vehicle B (2022 Ford F-150, Black, CT Plate: JK-78934)\n"
        "  Driver: Kenneth Okafor, 50, of 892 Pine Ridge Road, Hartford, CT\n"
        "  Insurance: State Farm Policy #SFA-4567890\n\n"
        "Vehicle C (2024 Honda Civic, White, CT Plate: MN-12045)\n"
        "  Driver: Samuel Park, 29, of 301 River Lane, East Hartford, CT\n"
        "  Passenger: Diane Whitfield, 33, of 301 River Lane, East Hartford, CT\n"
        "  Insurance: GEICO Policy #GCO-2345678"
    )
    rect2 = pymupdf.Rect(72, 445, 540, 720)
    page.insert_textbox(rect2, parties_text, fontsize=10, fontname="helv", color=(0, 0, 0))

    # ---- Page 3: Scene Description + Photo 1 ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "3. SCENE DESCRIPTION", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    scene_text = (
        "The collision occurred at the signalized intersection of Oak Boulevard (north-south, 4 lanes) "
        "and Maple Avenue (east-west, 2 lanes). The road surface was dry asphalt in fair condition. "
        "Weather conditions at the time of the incident were clear with temperatures around 42 degrees "
        "Fahrenheit. Visibility was unrestricted. The speed limit on both roadways is 35 mph. The "
        "intersection is controlled by a standard 3-phase traffic signal. Review of signal maintenance "
        "records confirms the signal was functioning properly on the date of the incident."
    )
    rect = pymupdf.Rect(72, 85, 540, 230)
    page.insert_textbox(rect, scene_text, fontsize=10.5, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Embed Photo 1
    page.insert_text(pymupdf.Point(72, 250), "Figure 1: Scene Overview - Intersection of Oak Blvd & Maple Ave",
                     fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_buf = io.BytesIO()
    photo_images[0].save(img_buf, format="PNG")
    img_buf.seek(0)
    page.insert_image(pymupdf.Rect(72, 265, 540, 545), stream=img_buf.read())

    page.insert_text(pymupdf.Point(72, 565), "Photo taken by Sgt. Morales at 10:15 AM, facing south.",
                     fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))

    # ---- Page 4: Vehicle Damage Analysis + Photos 2-3 ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "4. VEHICLE DAMAGE ANALYSIS", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    damage_text = (
        "Vehicle A sustained severe front-end damage consistent with a broadside impact at approximately "
        "30-35 mph. The front bumper, hood, and radiator assembly were crushed. Both front airbags deployed. "
        "The driver-side door showed secondary impact damage from contact with Vehicle C."
    )
    rect = pymupdf.Rect(72, 85, 540, 180)
    page.insert_textbox(rect, damage_text, fontsize=10.5, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Embed Photo 2
    page.insert_text(pymupdf.Point(72, 195), "Figure 2: Vehicle A - Front Damage",
                     fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_buf = io.BytesIO()
    photo_images[1].save(img_buf, format="PNG")
    img_buf.seek(0)
    page.insert_image(pymupdf.Rect(72, 210, 540, 420), stream=img_buf.read())

    # Embed Photo 3
    page.insert_text(pymupdf.Point(72, 440), "Figure 3: Vehicle A - Rear Quarter Panel Damage",
                     fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_buf = io.BytesIO()
    photo_images[2].save(img_buf, format="PNG")
    img_buf.seek(0)
    page.insert_image(pymupdf.Rect(120, 455, 420, 740), stream=img_buf.read())

    # ---- Page 5: Vehicle B Damage + Photo 4 ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "4.2 Vehicle B Damage Assessment", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))

    vb_text = (
        "Vehicle B sustained moderate damage to the driver-side front quarter panel and wheel assembly. "
        "The front left tire was deflated upon impact, and the wheel rim showed deformation. The driver-side "
        "airbag did not deploy, which is consistent with the lateral angle of impact. Mr. Okafor's seatbelt "
        "was engaged at the time of the collision."
    )
    rect = pymupdf.Rect(72, 85, 540, 190)
    page.insert_textbox(rect, vb_text, fontsize=10.5, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Embed Photo 4
    page.insert_text(pymupdf.Point(72, 205), "Figure 4: Road Surface - Skid Mark Analysis",
                     fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_buf = io.BytesIO()
    photo_images[3].save(img_buf, format="PNG")
    img_buf.seek(0)
    page.insert_image(pymupdf.Rect(72, 220, 540, 500), stream=img_buf.read())

    additional = (
        "Skid marks from Vehicle A extended 47 feet from the point of initial braking to the point of "
        "impact, indicating the driver applied brakes approximately 2.1 seconds before collision. Using "
        "the drag factor of 0.72 for dry asphalt, the estimated speed at initial braking was 38 mph, "
        "exceeding the posted 35 mph speed limit."
    )
    rect = pymupdf.Rect(72, 520, 540, 650)
    page.insert_textbox(rect, additional, fontsize=10.5, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 6: Traffic Signal Analysis + Photo 5 ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "5. TRAFFIC SIGNAL ANALYSIS", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    signal_text = (
        "The traffic signal at Oak Boulevard and Maple Avenue operates on a fixed-time cycle of 90 seconds. "
        "The northbound/southbound phase (Oak Blvd) receives 40 seconds of green, 4 seconds of yellow, and "
        "2 seconds of all-red clearance. Signal camera footage was requested from the City of Hartford "
        "Department of Transportation. Preliminary review of timing records shows the signal transitioned "
        "from yellow to red for the northbound direction at 09:47:12 AM. Vehicle A entered the intersection "
        "at approximately 09:47:14 AM, approximately 2 seconds after the signal turned red."
    )
    rect = pymupdf.Rect(72, 85, 540, 250)
    page.insert_textbox(rect, signal_text, fontsize=10.5, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Embed Photo 5
    page.insert_text(pymupdf.Point(72, 265), "Figure 5: Traffic Signal - Northbound View",
                     fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_buf = io.BytesIO()
    photo_images[4].save(img_buf, format="PNG")
    img_buf.seek(0)
    page.insert_image(pymupdf.Rect(72, 280, 540, 560), stream=img_buf.read())

    # ---- Page 7: Witness Statements + Photo 6 ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "6. WITNESS STATEMENTS", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    witness_text = (
        "Witness 1: Maria Gonzalez, 44, pedestrian at northeast corner\n"
        "\"I was waiting to cross the street when I saw the silver car coming fast from the south. "
        "The light had just turned red but the car kept going. The black truck was already starting to go "
        "when they hit. It happened so fast.\"\n\n"
        "Witness 2: James Liu, 31, driver stopped at eastbound red light\n"
        "\"I was first in line at the red light on Maple. When my light turned green, I hesitated because "
        "I saw the silver car still coming. The truck next to me started to go right away. I heard the "
        "crash and then the silver car spun into the white car behind me.\""
    )
    rect = pymupdf.Rect(72, 85, 540, 340)
    page.insert_textbox(rect, witness_text, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # Embed Photo 6
    page.insert_text(pymupdf.Point(72, 355), "Figure 6: View from Witness Gonzalez Position (East Side)",
                     fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_buf = io.BytesIO()
    photo_images[5].save(img_buf, format="PNG")
    img_buf.seek(0)
    page.insert_image(pymupdf.Rect(120, 370, 420, 660), stream=img_buf.read())

    # ---- Page 8: Medical Summary ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "7. MEDICAL SUMMARY", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    medical_text = (
        "All three injured parties were transported to Hartford Hospital by AMR Ambulance Service.\n\n"
        "Rachel Torres (Vehicle A Driver):\n"
        "  - Left femoral shaft fracture (closed)\n"
        "  - Multiple contusions to left side of body\n"
        "  - Abrasions from airbag deployment\n"
        "  - Admitted for surgical fixation; estimated recovery 8-12 weeks\n"
        "  - Blood alcohol: 0.00 (tested at hospital per consent)\n\n"
        "Kenneth Okafor (Vehicle B Driver):\n"
        "  - Cervical strain (whiplash)\n"
        "  - Minor abrasion to left forearm from seatbelt\n"
        "  - Treated and released same day\n"
        "  - Blood alcohol: 0.00\n\n"
        "Diane Whitfield (Vehicle C Passenger):\n"
        "  - Grade 2 concussion\n"
        "  - Cervical strain\n"
        "  - Held for 24-hour observation, released November 15\n\n"
        "Samuel Park (Vehicle C Driver):\n"
        "  - No injuries reported\n"
        "  - Declined medical transport\n"
        "  - Examined at scene by EMT"
    )
    rect = pymupdf.Rect(72, 85, 540, 600)
    page.insert_textbox(rect, medical_text, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # ---- Page 9: Reconstruction Analysis ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "8. ACCIDENT RECONSTRUCTION", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    recon_text = (
        "Based on physical evidence, witness statements, and vehicle damage analysis, the following "
        "reconstruction of the collision sequence has been established:\n\n"
        "09:47:08 - Vehicle A approaches intersection at approximately 38 mph in the left lane of "
        "northbound Oak Boulevard. Signal is yellow.\n\n"
        "09:47:10 - Vehicle A driver applies brakes. Skid marks begin 47 feet south of intersection.\n\n"
        "09:47:12 - Signal transitions from yellow to red for northbound traffic. All-red clearance "
        "interval begins.\n\n"
        "09:47:14 - Signal turns green for eastbound/westbound Maple Avenue. Vehicle A enters "
        "intersection at approximately 28 mph, having reduced speed through braking but failing "
        "to stop.\n\n"
        "09:47:15 - Vehicle B begins to accelerate from stop on westbound Maple Avenue, entering "
        "the intersection.\n\n"
        "09:47:16 - Vehicle A strikes Vehicle B in a T-bone configuration, with Vehicle A's front "
        "impacting Vehicle B's driver-side front quarter. Impact speed estimated at 25-30 mph.\n\n"
        "09:47:17 - Post-impact, Vehicle A rotates counterclockwise approximately 120 degrees and "
        "slides northeast, striking the front of Vehicle C, which was stopped at the southbound red light.\n\n"
        "09:47:18 - All vehicles come to rest. Vehicle A facing approximately west, Vehicle B pushed "
        "2 feet northwest, Vehicle C pushed back approximately 3 feet."
    )
    rect = pymupdf.Rect(72, 85, 540, 700)
    page.insert_textbox(rect, recon_text, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # ---- Page 10: Conclusions and Signatures ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "9. CONCLUSIONS", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    conclusions = (
        "Based on the totality of evidence gathered during this investigation, the following conclusions "
        "are drawn:\n\n"
        "1. Vehicle A, operated by Rachel Torres, entered the intersection approximately 2 seconds after "
        "the traffic signal turned red, constituting a red-light violation.\n\n"
        "2. Vehicle A was traveling at approximately 38 mph in a 35 mph zone at the time braking was "
        "initiated, constituting a speed violation.\n\n"
        "3. Vehicle B, operated by Kenneth Okafor, entered the intersection on a valid green signal. "
        "No violations are attributed to Mr. Okafor.\n\n"
        "4. Vehicle C, operated by Samuel Park, was stationary at the time of secondary impact. "
        "No violations are attributed to Mr. Park.\n\n"
        "5. No evidence of mechanical failure was found in any of the three vehicles.\n\n"
        "6. No evidence of impairment (alcohol or drugs) was found for any of the involved drivers.\n\n"
        "7. Primary cause: Failure to obey traffic signal by Vehicle A operator.\n"
        "   Contributing factor: Exceeding posted speed limit by Vehicle A operator."
    )
    rect = pymupdf.Rect(72, 85, 540, 520)
    page.insert_textbox(rect, conclusions, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    page.insert_text(pymupdf.Point(72, 560), "PREPARED BY:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 610), pymupdf.Point(300, 610))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    page.insert_text(pymupdf.Point(72, 625), "Sgt. Daniel Morales, Badge #4892", fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 640), "Forensic Reconstruction Unit", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 655), "Hartford Police Department", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 670), "Date: November 21, 2025", fontsize=10, fontname="helv", color=(0, 0, 0))

    page.insert_text(pymupdf.Point(340, 560), "REVIEWED BY:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(340, 610), pymupdf.Point(540, 610))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    page.insert_text(pymupdf.Point(340, 625), "Lt. Barbara Chen", fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(340, 640), "Traffic Division Commander", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(340, 655), "Hartford Police Department", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(340, 670), "Date: November 22, 2025", fontsize=10, fontname="helv", color=(0, 0, 0))

    # Set metadata
    doc.set_metadata({
        "title": "Accident Investigation Report - Case PI-2025-4471",
        "author": "Hartford Police Department - Forensic Reconstruction Unit",
        "subject": "Multi-Vehicle Collision at Oak Blvd & Maple Ave",
        "keywords": "accident, collision, personal injury, traffic",
        "creator": "Hartford PD Forensic Unit",
    })

    # Set table of contents
    toc = [
        [1, "Executive Summary", 2],
        [1, "Parties Involved", 2],
        [1, "Scene Description", 3],
        [1, "Vehicle Damage Analysis", 4],
        [1, "Traffic Signal Analysis", 6],
        [1, "Witness Statements", 7],
        [1, "Medical Summary", 8],
        [1, "Accident Reconstruction", 9],
        [1, "Conclusions", 10],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Photos directory created: {PHOTOS_DIR}')
    print(f'PDF has 10 pages with 6 embedded photographs')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
