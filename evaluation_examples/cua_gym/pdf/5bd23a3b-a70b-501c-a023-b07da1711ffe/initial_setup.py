"""
Initial Setup: Create a 4-page lease amendment PDF
Task ID: pdf_legal_085
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_085'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/lease_amendment.pdf'


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
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()

    # ========== PAGE 1: Title & Recitals ==========
    page1 = doc.new_page(width=612, height=792)  # Letter size

    # Title block
    page1.insert_text(
        pymupdf.Point(72, 60),
        "FIRST AMENDMENT TO RESIDENTIAL LEASE AGREEMENT",
        fontsize=16,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Horizontal rule
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 70), pymupdf.Point(540, 70))
    shape.finish(color=(0, 0, 0), width=1.5)
    shape.commit()

    body_text = [
        ("THIS FIRST AMENDMENT TO RESIDENTIAL LEASE AGREEMENT", 100, "hebo", 11),
        ('(this "Amendment") is made and entered into as of March 15, 2024,', 115, "helv", 11),
        ("by and between the following parties:", 130, "helv", 11),
        ("", 150, "helv", 11),
        ("LANDLORD:", 165, "hebo", 11),
        ("Meridian Property Holdings, LLC", 180, "helv", 11),
        ("a Delaware limited liability company", 195, "helv", 11),
        ("Principal Office: 4200 Westfield Boulevard, Suite 300", 210, "helv", 10),
        ("Indianapolis, IN 46208", 225, "helv", 10),
        ("Contact: Victoria R. Ashworth, Managing Partner", 240, "helv", 10),
        ("", 260, "helv", 11),
        ("TENANT:", 275, "hebo", 11),
        ("Jonathan M. Prescott and Elena K. Prescott", 290, "helv", 11),
        ("(collectively, the \"Tenant\")", 305, "helv", 11),
        ("Current Address: 1847 Oakridge Lane, Unit 4B", 320, "helv", 10),
        ("Indianapolis, IN 46220", 335, "helv", 10),
        ("", 355, "helv", 11),
        ("RECITALS", 375, "hebo", 13),
        ("", 395, "helv", 11),
    ]

    for text, y, font, size in body_text:
        if text:
            page1.insert_text(pymupdf.Point(72, y), text, fontsize=size, fontname=font, color=(0, 0, 0))

    recital_text = (
        "WHEREAS, Landlord and Tenant entered into that certain Residential Lease Agreement "
        "dated September 1, 2022 (the \"Original Lease\") for the premises located at 1847 "
        "Oakridge Lane, Unit 4B, Indianapolis, Indiana 46220 (the \"Premises\"); and\n\n"
        "WHEREAS, the Original Lease is currently in effect with a term expiring on August 31, "
        "2024; and\n\n"
        "WHEREAS, Landlord and Tenant desire to amend certain terms and conditions of the "
        "Original Lease as set forth herein;\n\n"
        "NOW, THEREFORE, in consideration of the mutual covenants and agreements contained "
        "herein, and for other good and valuable consideration, the receipt and sufficiency "
        "of which are hereby acknowledged, the parties agree as follows:"
    )

    rect = pymupdf.Rect(72, 400, 540, 700)
    page1.insert_textbox(rect, recital_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 2: Amendment Terms ==========
    page2 = doc.new_page(width=612, height=792)

    page2.insert_text(pymupdf.Point(72, 60), "AMENDMENT TERMS", fontsize=14, fontname="hebo", color=(0, 0, 0))

    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 70), pymupdf.Point(540, 70))
    shape2.finish(color=(0, 0, 0), width=1.0)
    shape2.commit()

    sections = [
        ("1. EXTENSION OF LEASE TERM", 95, "hebo", 11),
        ("", 110, "helv", 10),
        ("Section 2.1 of the Original Lease is hereby amended to extend the lease term for", 115, "helv", 10),
        ("an additional period of twenty-four (24) months, commencing on September 1, 2024,", 130, "helv", 10),
        ("and expiring on August 31, 2026, unless sooner terminated in accordance with the", 145, "helv", 10),
        ("terms of the Original Lease as amended hereby.", 160, "helv", 10),
        ("", 180, "helv", 10),
        ("2. RENT ADJUSTMENT", 195, "hebo", 11),
        ("", 210, "helv", 10),
        ("Section 3.1 of the Original Lease is hereby amended as follows:", 215, "helv", 10),
        ("", 235, "helv", 10),
        ("  (a) Effective September 1, 2024, the monthly base rent shall be increased from", 240, "helv", 10),
        ("      One Thousand Eight Hundred Dollars ($1,800.00) to One Thousand Nine Hundred", 255, "helv", 10),
        ("      Fifty Dollars ($1,950.00) per month.", 270, "helv", 10),
        ("", 290, "helv", 10),
        ("  (b) Effective September 1, 2025, the monthly base rent shall be further increased", 295, "helv", 10),
        ("      to Two Thousand One Hundred Dollars ($2,100.00) per month.", 310, "helv", 10),
        ("", 330, "helv", 10),
        ("  (c) All rent payments shall continue to be due on the first day of each calendar", 335, "helv", 10),
        ("      month and shall be payable in accordance with Section 3.2 of the Original Lease.", 350, "helv", 10),
        ("", 370, "helv", 10),
        ("3. PET ADDENDUM", 385, "hebo", 11),
        ("", 400, "helv", 10),
        ("A new Section 12 is hereby added to the Original Lease:", 405, "helv", 10),
        ("", 420, "helv", 10),
        ("Tenant shall be permitted to keep one (1) domestic cat on the Premises, subject to", 425, "helv", 10),
        ("a non-refundable pet fee of Three Hundred Dollars ($300.00) due upon execution of", 440, "helv", 10),
        ("this Amendment, and an additional monthly pet rent of Fifty Dollars ($50.00).", 455, "helv", 10),
        ("Tenant shall be responsible for any damage caused by the pet and shall comply with", 470, "helv", 10),
        ("all applicable local ordinances regarding pet ownership.", 485, "helv", 10),
        ("", 505, "helv", 10),
        ("4. PARKING SPACE ASSIGNMENT", 520, "hebo", 11),
        ("", 535, "helv", 10),
        ("Section 8.3 of the Original Lease is hereby amended to assign Tenant one (1)", 540, "helv", 10),
        ("additional covered parking space, designated as Space #47B, for an additional", 555, "helv", 10),
        ("monthly fee of Seventy-Five Dollars ($75.00).", 570, "helv", 10),
        ("", 590, "helv", 10),
        ("5. UTILITY RESPONSIBILITY", 605, "hebo", 11),
        ("", 620, "helv", 10),
        ("Effective September 1, 2024, Section 6.2 of the Original Lease is amended to", 625, "helv", 10),
        ("transfer responsibility for water and sewer charges from Landlord to Tenant.", 640, "helv", 10),
        ("Tenant shall establish accounts directly with Indianapolis Water Utilities within", 655, "helv", 10),
        ("thirty (30) days of the effective date of this Amendment.", 670, "helv", 10),
    ]

    for text, y, font, size in sections:
        if text:
            page2.insert_text(pymupdf.Point(72, y), text, fontsize=size, fontname=font, color=(0, 0, 0))

    # Page number
    page2.insert_text(pymupdf.Point(290, 770), "- 2 -", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))

    # ========== PAGE 3: Additional Terms & Conditions ==========
    page3 = doc.new_page(width=612, height=792)

    page3.insert_text(pymupdf.Point(72, 60), "ADDITIONAL TERMS AND CONDITIONS", fontsize=14, fontname="hebo", color=(0, 0, 0))

    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, 70), pymupdf.Point(540, 70))
    shape3.finish(color=(0, 0, 0), width=1.0)
    shape3.commit()

    addl_sections = [
        ("6. MAINTENANCE AND REPAIRS", 95, "hebo", 11),
        ("", 110, "helv", 10),
        ("Section 9.1 of the Original Lease is supplemented to provide that Tenant shall be", 115, "helv", 10),
        ("responsible for routine maintenance of the HVAC system, including filter replacement", 130, "helv", 10),
        ("every ninety (90) days. Landlord shall continue to be responsible for major HVAC", 145, "helv", 10),
        ("repairs and replacement of the system.", 160, "helv", 10),
        ("", 180, "helv", 10),
        ("7. INSURANCE REQUIREMENTS", 195, "hebo", 11),
        ("", 210, "helv", 10),
        ("Tenant shall maintain renter's insurance with minimum coverage of One Hundred", 215, "helv", 10),
        ("Thousand Dollars ($100,000.00) for personal liability and Fifty Thousand Dollars", 230, "helv", 10),
        ("($50,000.00) for personal property. Proof of insurance shall be provided to", 245, "helv", 10),
        ("Landlord within thirty (30) days of execution of this Amendment and upon each", 260, "helv", 10),
        ("annual renewal thereafter.", 275, "helv", 10),
        ("", 295, "helv", 10),
        ("8. RIGHT OF FIRST REFUSAL", 310, "hebo", 11),
        ("", 325, "helv", 10),
        ("In the event Landlord decides to sell the Premises during the extended lease term,", 330, "helv", 10),
        ("Tenant shall have a right of first refusal to purchase the Premises at the same", 345, "helv", 10),
        ("price and upon the same terms as any bona fide third-party offer received by", 360, "helv", 10),
        ("Landlord. Tenant shall have fifteen (15) business days from receipt of written", 375, "helv", 10),
        ("notice to exercise this right.", 390, "helv", 10),
        ("", 410, "helv", 10),
        ("9. SUBLETTING", 425, "hebo", 11),
        ("", 440, "helv", 10),
        ("Section 11.1 of the Original Lease is amended to permit subletting of the", 445, "helv", 10),
        ("Premises with prior written consent of Landlord, which consent shall not be", 460, "helv", 10),
        ("unreasonably withheld. Any sublessee must meet Landlord's standard tenant", 475, "helv", 10),
        ("qualification criteria and execute a sublease agreement approved by Landlord.", 490, "helv", 10),
        ("", 510, "helv", 10),
        ("10. GENERAL PROVISIONS", 525, "hebo", 11),
        ("", 540, "helv", 10),
        ("  (a) This Amendment shall be binding upon and inure to the benefit of the", 545, "helv", 10),
        ("      parties hereto and their respective heirs, successors, and assigns.", 560, "helv", 10),
        ("", 575, "helv", 10),
        ("  (b) Except as expressly modified by this Amendment, all terms and conditions", 580, "helv", 10),
        ("      of the Original Lease shall remain in full force and effect.", 595, "helv", 10),
        ("", 610, "helv", 10),
        ("  (c) This Amendment may be executed in counterparts, each of which shall be", 615, "helv", 10),
        ("      deemed an original and all of which together shall constitute one and the", 630, "helv", 10),
        ("      same instrument.", 645, "helv", 10),
    ]

    for text, y, font, size in addl_sections:
        if text:
            page3.insert_text(pymupdf.Point(72, y), text, fontsize=size, fontname=font, color=(0, 0, 0))

    page3.insert_text(pymupdf.Point(290, 770), "- 3 -", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))

    # ========== PAGE 4: Signature Block ==========
    page4 = doc.new_page(width=612, height=792)

    page4.insert_text(pymupdf.Point(72, 60), "SIGNATURES", fontsize=14, fontname="hebo", color=(0, 0, 0))

    shape4 = page4.new_shape()
    shape4.draw_line(pymupdf.Point(72, 70), pymupdf.Point(540, 70))
    shape4.finish(color=(0, 0, 0), width=1.0)
    shape4.commit()

    sig_text = (
        "IN WITNESS WHEREOF, the parties hereto have executed this First Amendment to "
        "Residential Lease Agreement as of the date first written above."
    )
    rect4 = pymupdf.Rect(72, 90, 540, 140)
    page4.insert_textbox(rect4, sig_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    sig_items = [
        ("LANDLORD:", 175, "hebo", 11),
        ("Meridian Property Holdings, LLC", 195, "helv", 10),
        ("", 220, "helv", 10),
        ("By: _________________________________", 240, "helv", 10),
        ("Name: Victoria R. Ashworth", 260, "helv", 10),
        ("Title: Managing Partner", 275, "helv", 10),
        ("Date: _________________________________", 295, "helv", 10),
        ("", 325, "helv", 10),
        ("TENANT:", 345, "hebo", 11),
        ("", 365, "helv", 10),
        ("_________________________________", 385, "helv", 10),
        ("Jonathan M. Prescott", 405, "helv", 10),
        ("Date: _________________________________", 425, "helv", 10),
        ("", 455, "helv", 10),
        ("_________________________________", 475, "helv", 10),
        ("Elena K. Prescott", 495, "helv", 10),
        ("Date: _________________________________", 515, "helv", 10),
        ("", 545, "helv", 10),
        ("ACKNOWLEDGMENT OF RECEIPT", 565, "hebo", 11),
        ("", 580, "helv", 10),
        ("Each party acknowledges receipt of a fully executed copy of this Amendment.", 585, "helv", 10),
        ("This Amendment becomes effective as of the date first written above.", 600, "helv", 10),
    ]

    for text, y, font, size in sig_items:
        if text:
            page4.insert_text(pymupdf.Point(72, y), text, fontsize=size, fontname=font, color=(0, 0, 0))

    page4.insert_text(pymupdf.Point(290, 770), "- 4 -", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))

    # Save
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
