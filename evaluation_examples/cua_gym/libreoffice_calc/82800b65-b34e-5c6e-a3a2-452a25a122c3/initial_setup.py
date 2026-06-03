"""
Initial Setup: Create a PDF with apparent redactions (black rectangles)
where some are proper (text removed) and some are improper (text still underneath).
Task ID: pdf_cr_069
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_069'
OUTPUT = f'{WORKDIR}/Desktop/redacted.pdf'


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
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    doc = pymupdf.open()

    # =========================================================
    # PAGE 1: "Meridian Healthcare - Patient Intake Summary"
    # Contains 3 redaction boxes:
    #   - Box 1: PROPER redaction (text removed, black rect only)
    #   - Box 2: IMPROPER redaction (text still under black rect)
    #   - Box 3: PROPER redaction (text removed, black rect only)
    # =========================================================
    page1 = doc.new_page(width=612, height=792)
    shape1 = page1.new_shape()

    # Title
    page1.insert_text(pymupdf.Point(72, 50), "Meridian Healthcare Group",
                       fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    page1.insert_text(pymupdf.Point(72, 72), "Patient Intake Summary - Confidential",
                       fontsize=14, fontname="heit", color=(0.3, 0.3, 0.3))

    # Horizontal rule
    shape1.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape1.finish(color=(0.6, 0.6, 0.6), width=1)

    # Section: Patient Information
    page1.insert_text(pymupdf.Point(72, 110), "Section 1: Patient Information",
                       fontsize=13, fontname="hebo", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(72, 135), "Patient Name:", fontsize=11, fontname="hebo")
    # PROPER REDACTION (Box 1): Text removed, only black rect
    # We do NOT insert the patient name text - just draw the black rect
    rect1 = pymupdf.Rect(180, 123, 350, 139)
    shape1.draw_rect(rect1)
    shape1.finish(color=(0, 0, 0), fill=(0, 0, 0), width=0.5)

    page1.insert_text(pymupdf.Point(72, 158), "Date of Birth:", fontsize=11, fontname="hebo")
    page1.insert_text(pymupdf.Point(180, 158), "March 14, 1987", fontsize=11, fontname="helv")

    page1.insert_text(pymupdf.Point(72, 180), "Medical Record #:", fontsize=11, fontname="hebo")
    # IMPROPER REDACTION (Box 2): Text IS underneath the black rect
    page1.insert_text(pymupdf.Point(195, 180), "MRN-2024-88431", fontsize=11, fontname="helv")
    rect2 = pymupdf.Rect(192, 168, 350, 184)
    shape1.draw_rect(rect2)
    shape1.finish(color=(0, 0, 0), fill=(0, 0, 0), width=0.5)

    page1.insert_text(pymupdf.Point(72, 203), "Insurance Provider:", fontsize=11, fontname="hebo")
    page1.insert_text(pymupdf.Point(210, 203), "BlueCross BlueShield PPO", fontsize=11, fontname="helv")

    page1.insert_text(pymupdf.Point(72, 226), "Policy Number:", fontsize=11, fontname="hebo")
    # PROPER REDACTION (Box 3): Text removed, only black rect
    rect3 = pymupdf.Rect(180, 214, 340, 230)
    shape1.draw_rect(rect3)
    shape1.finish(color=(0, 0, 0), fill=(0, 0, 0), width=0.5)

    # Section: Visit Details
    page1.insert_text(pymupdf.Point(72, 265), "Section 2: Visit Details",
                       fontsize=13, fontname="hebo", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(72, 290), "Primary Complaint:", fontsize=11, fontname="hebo")
    page1.insert_text(pymupdf.Point(210, 290),
                       "Persistent lower back pain radiating to left leg, duration 3 weeks.",
                       fontsize=11, fontname="helv")

    page1.insert_text(pymupdf.Point(72, 313), "Attending Physician:", fontsize=11, fontname="hebo")
    page1.insert_text(pymupdf.Point(220, 313), "Dr. Rebecca Thornton, MD", fontsize=11, fontname="helv")

    page1.insert_text(pymupdf.Point(72, 336), "Visit Date:", fontsize=11, fontname="hebo")
    page1.insert_text(pymupdf.Point(160, 336), "January 22, 2025", fontsize=11, fontname="helv")

    page1.insert_text(pymupdf.Point(72, 359), "Department:", fontsize=11, fontname="hebo")
    page1.insert_text(pymupdf.Point(170, 359), "Orthopedics - Spine Clinic", fontsize=11, fontname="helv")

    # Additional paragraph
    y = 400
    paragraph = (
        "The patient presented with complaints of chronic lower back pain that began "
        "approximately three weeks prior to the visit. The pain is described as a dull, "
        "constant ache in the lumbar region with intermittent sharp episodes radiating "
        "down the left leg to the knee. The patient reports difficulty sitting for "
        "prolonged periods and disturbed sleep due to discomfort. No history of trauma "
        "or previous spinal surgery. Family history includes degenerative disc disease "
        "(mother) and osteoarthritis (father). Current medications include ibuprofen "
        "400mg PRN and a muscle relaxant prescribed by the referring primary care physician."
    )
    page1.insert_textbox(pymupdf.Rect(72, y, 540, 560), paragraph,
                          fontsize=10, fontname="helv", color=(0, 0, 0),
                          align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Footer
    page1.insert_text(pymupdf.Point(72, 750), "Page 1 of 3",
                       fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))
    page1.insert_text(pymupdf.Point(350, 750),
                       "CONFIDENTIAL - Meridian Healthcare Group",
                       fontsize=9, fontname="heit", color=(0.5, 0.5, 0.5))

    shape1.commit()

    # =========================================================
    # PAGE 2: "Laboratory Results & Diagnostics"
    # Contains 2 redaction boxes:
    #   - Box 4: IMPROPER redaction (text still extractable)
    #   - Box 5: IMPROPER redaction (text still extractable)
    # =========================================================
    page2 = doc.new_page(width=612, height=792)
    shape2 = page2.new_shape()

    page2.insert_text(pymupdf.Point(72, 50), "Laboratory Results & Diagnostic Imaging",
                       fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    shape2.draw_line(pymupdf.Point(72, 60), pymupdf.Point(540, 60))
    shape2.finish(color=(0.6, 0.6, 0.6), width=1)

    # Lab results table header
    page2.insert_text(pymupdf.Point(72, 90), "Test", fontsize=11, fontname="hebo")
    page2.insert_text(pymupdf.Point(220, 90), "Result", fontsize=11, fontname="hebo")
    page2.insert_text(pymupdf.Point(340, 90), "Reference Range", fontsize=11, fontname="hebo")
    page2.insert_text(pymupdf.Point(480, 90), "Status", fontsize=11, fontname="hebo")

    shape2.draw_line(pymupdf.Point(72, 95), pymupdf.Point(540, 95))
    shape2.finish(color=(0.3, 0.3, 0.3), width=0.5)

    # Lab data rows
    lab_data = [
        ("Complete Blood Count", "WBC 7.2 K/uL", "4.5-11.0 K/uL", "Normal"),
        ("Hemoglobin", "13.8 g/dL", "12.0-16.0 g/dL", "Normal"),
        ("C-Reactive Protein", "4.7 mg/L", "0.0-3.0 mg/L", "HIGH"),
        ("ESR", "28 mm/hr", "0-20 mm/hr", "HIGH"),
        ("ANA Panel", "Negative", "Negative", "Normal"),
        ("Rheumatoid Factor", "< 10 IU/mL", "0-14 IU/mL", "Normal"),
        ("Vitamin D, 25-OH", "18 ng/mL", "30-100 ng/mL", "LOW"),
        ("Calcium", "9.4 mg/dL", "8.5-10.5 mg/dL", "Normal"),
    ]
    y = 115
    for test, result, ref, status in lab_data:
        page2.insert_text(pymupdf.Point(72, y), test, fontsize=10, fontname="helv")
        page2.insert_text(pymupdf.Point(220, y), result, fontsize=10, fontname="helv")
        page2.insert_text(pymupdf.Point(340, y), ref, fontsize=10, fontname="helv")
        color = (0.8, 0, 0) if status in ("HIGH", "LOW") else (0, 0.5, 0)
        page2.insert_text(pymupdf.Point(480, y), status, fontsize=10, fontname="hebo", color=color)
        y += 22

    # Imaging section
    y += 20
    page2.insert_text(pymupdf.Point(72, y), "Diagnostic Imaging Results",
                       fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 25

    page2.insert_text(pymupdf.Point(72, y), "MRI Lumbar Spine (01/22/2025):",
                       fontsize=11, fontname="hebo")
    y += 20
    mri_text = (
        "Findings: Disc desiccation at L4-L5 and L5-S1 levels. Mild posterior disc "
        "bulge at L4-L5 with slight impingement on the left L5 nerve root. No significant "
        "central canal stenosis. Facet joint hypertrophy at L5-S1 bilaterally. Vertebral "
        "body heights are maintained. No compression fractures identified. Conus medullaris "
        "terminates normally at L1 level."
    )
    page2.insert_textbox(pymupdf.Rect(72, y, 540, y + 80), mri_text,
                          fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    y += 95
    page2.insert_text(pymupdf.Point(72, y), "Radiologist:", fontsize=11, fontname="hebo")
    # IMPROPER REDACTION (Box 4): Text underneath
    page2.insert_text(pymupdf.Point(165, y), "Dr. Alan Westbrook, MD", fontsize=11, fontname="helv")
    rect4 = pymupdf.Rect(162, y - 12, 360, y + 4)
    shape2.draw_rect(rect4)
    shape2.finish(color=(0, 0, 0), fill=(0, 0, 0), width=0.5)

    y += 25
    page2.insert_text(pymupdf.Point(72, y), "Radiology Report ID:", fontsize=11, fontname="hebo")
    # IMPROPER REDACTION (Box 5): Text underneath
    page2.insert_text(pymupdf.Point(220, y), "RAD-2025-01-5578", fontsize=11, fontname="helv")
    rect5 = pymupdf.Rect(217, y - 12, 390, y + 4)
    shape2.draw_rect(rect5)
    shape2.finish(color=(0, 0, 0), fill=(0, 0, 0), width=0.5)

    # Footer
    page2.insert_text(pymupdf.Point(72, 750), "Page 2 of 3",
                       fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))
    page2.insert_text(pymupdf.Point(350, 750),
                       "CONFIDENTIAL - Meridian Healthcare Group",
                       fontsize=9, fontname="heit", color=(0.5, 0.5, 0.5))

    shape2.commit()

    # =========================================================
    # PAGE 3: "Treatment Plan & Follow-Up"
    # Contains 2 redaction boxes:
    #   - Box 6: PROPER redaction (text removed)
    #   - Box 7: IMPROPER redaction (text still extractable)
    # =========================================================
    page3 = doc.new_page(width=612, height=792)
    shape3 = page3.new_shape()

    page3.insert_text(pymupdf.Point(72, 50), "Treatment Plan & Follow-Up",
                       fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    shape3.draw_line(pymupdf.Point(72, 60), pymupdf.Point(540, 60))
    shape3.finish(color=(0.6, 0.6, 0.6), width=1)

    page3.insert_text(pymupdf.Point(72, 90), "Prescribed Treatment:",
                       fontsize=13, fontname="hebo", color=(0, 0, 0))

    treatments = [
        "1. Physical Therapy - 2x/week for 6 weeks (McKenzie method focus)",
        "2. Naproxen 500mg - twice daily with food for 2 weeks",
        "3. Cyclobenzaprine 10mg - at bedtime for muscle spasm relief",
        "4. Vitamin D3 supplementation - 2000 IU daily",
        "5. Lumbar support brace recommended for prolonged sitting",
        "6. Activity modification: avoid heavy lifting > 15 lbs",
    ]
    y = 115
    for t in treatments:
        page3.insert_text(pymupdf.Point(90, y), t, fontsize=10, fontname="helv")
        y += 20

    y += 15
    page3.insert_text(pymupdf.Point(72, y), "Referral Information:",
                       fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 25

    page3.insert_text(pymupdf.Point(72, y), "Referred to:", fontsize=11, fontname="hebo")
    page3.insert_text(pymupdf.Point(165, y), "Summit Physical Therapy & Rehabilitation",
                       fontsize=11, fontname="helv")
    y += 22

    page3.insert_text(pymupdf.Point(72, y), "Therapist:", fontsize=11, fontname="hebo")
    # PROPER REDACTION (Box 6): No text placed, just black rect
    rect6 = pymupdf.Rect(155, y - 12, 340, y + 4)
    shape3.draw_rect(rect6)
    shape3.finish(color=(0, 0, 0), fill=(0, 0, 0), width=0.5)

    y += 22
    page3.insert_text(pymupdf.Point(72, y), "Phone:", fontsize=11, fontname="hebo")
    page3.insert_text(pymupdf.Point(130, y), "(555) 412-8890", fontsize=11, fontname="helv")

    y += 35
    page3.insert_text(pymupdf.Point(72, y), "Follow-Up Appointment:",
                       fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 25
    page3.insert_text(pymupdf.Point(72, y),
                       "Scheduled: March 5, 2025 at 10:30 AM with Dr. Thornton",
                       fontsize=11, fontname="helv")
    y += 20
    page3.insert_text(pymupdf.Point(72, y),
                       "Location: Meridian Spine Clinic, Building C, Suite 240",
                       fontsize=11, fontname="helv")

    y += 35
    page3.insert_text(pymupdf.Point(72, y), "Patient Signature:", fontsize=11, fontname="hebo")
    # IMPROPER REDACTION (Box 7): Text underneath
    page3.insert_text(pymupdf.Point(195, y), "Elena Vasquez-Rodriguez",
                       fontsize=11, fontname="helv")
    rect7 = pymupdf.Rect(192, y - 12, 400, y + 4)
    shape3.draw_rect(rect7)
    shape3.finish(color=(0, 0, 0), fill=(0, 0, 0), width=0.5)

    y += 22
    page3.insert_text(pymupdf.Point(72, y), "Date Signed:", fontsize=11, fontname="hebo")
    page3.insert_text(pymupdf.Point(170, y), "January 22, 2025", fontsize=11, fontname="helv")

    # Disclaimer at bottom
    y = 680
    disclaimer = (
        "This document contains protected health information (PHI) as defined by HIPAA. "
        "Unauthorized disclosure is prohibited. Redacted sections contain personally "
        "identifiable information that has been obscured in compliance with data privacy "
        "regulations. Any concerns regarding redaction quality should be reported to the "
        "Health Information Management department."
    )
    page3.insert_textbox(pymupdf.Rect(72, y, 540, 740), disclaimer,
                          fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4),
                          align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Footer
    page3.insert_text(pymupdf.Point(72, 750), "Page 3 of 3",
                       fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))
    page3.insert_text(pymupdf.Point(350, 750),
                       "CONFIDENTIAL - Meridian Healthcare Group",
                       fontsize=9, fontname="heit", color=(0.5, 0.5, 0.5))

    shape3.commit()

    # Save
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open PDF in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
