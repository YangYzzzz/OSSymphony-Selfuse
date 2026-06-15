"""
Initial Setup: Create a 16-page lease agreement PDF with rental terms on page 8.
Task ID: pdf_fm_049
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_049'
OUTPUT_DIR = f'{WORKDIR}/Documents/legal'
OUTPUT = f'{OUTPUT_DIR}/lease_agreement.pdf'

# Page dimensions (Letter size)
W, H = 612, 792

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


def add_page_text(doc, title, body_paragraphs, page_number):
    """Add a page with a title and body paragraphs."""
    page = doc.new_page(width=W, height=H)

    # Page border lines
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 50), pymupdf.Point(W - 72, 50))
    shape.finish(color=(0.3, 0.3, 0.3), width=1.0)
    shape.draw_line(pymupdf.Point(72, H - 50), pymupdf.Point(W - 72, H - 50))
    shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
    shape.commit()

    # Title
    page.insert_text(pymupdf.Point(72, 80), title, fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))

    # Body paragraphs
    y = 110
    for para in body_paragraphs:
        rect = pymupdf.Rect(72, y, W - 72, H - 70)
        excess = page.insert_textbox(rect, para, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        # Estimate how much vertical space was consumed
        lines_approx = max(1, len(para) // 65 + 1)
        y += lines_approx * 14 + 8
        if y > H - 100:
            break

    # Page number footer
    page.insert_text(pymupdf.Point(W / 2 - 10, H - 35), f"Page {page_number}", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    return page


def create_initial():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc = pymupdf.open()

    # --- Page 1: Cover Page ---
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(W/2 - 120, 250), "RESIDENTIAL LEASE AGREEMENT", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.3))
    p.insert_text(pymupdf.Point(W/2 - 80, 290), "Between", fontsize=12, fontname="tiit", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(W/2 - 110, 320), "Greenfield Property Management LLC", fontsize=13, fontname="hebo", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(W/2 - 40, 345), "(Landlord)", fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))
    p.insert_text(pymupdf.Point(W/2 - 15, 380), "and", fontsize=12, fontname="tiit", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(W/2 - 60, 410), "Aisha Patel & David Nakamura", fontsize=13, fontname="hebo", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(W/2 - 35, 435), "(Tenants)", fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))
    p.insert_text(pymupdf.Point(W/2 - 90, 500), "Property: 742 Evergreen Terrace, Apt 3B", fontsize=11, fontname="helv", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(W/2 - 80, 520), "Springfield, OR 97477", fontsize=11, fontname="helv", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(W/2 - 60, 570), "Effective Date: March 1, 2025", fontsize=11, fontname="hebo", color=(0.1, 0.1, 0.3))
    p.insert_text(pymupdf.Point(W/2 - 10, H - 35), "Page 1", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 2: Table of Contents ---
    add_page_text(doc, "TABLE OF CONTENTS", [
        "1. Parties and Premises .......................... 3",
        "2. Term of Lease .................................. 4",
        "3. Rent and Payment Terms ........................ 5",
        "4. Utilities and Services ........................ 6",
        "5. Maintenance and Repairs ....................... 7",
        "6. Security Deposit and Additional Fees ......... 8",
        "7. Rules and Restrictions ....................... 8",
        "8. Parking and Common Areas ..................... 9",
        "9. Insurance Requirements ....................... 10",
        "10. Early Termination ........................... 11",
        "11. Subletting and Assignment ................... 12",
        "12. Entry and Inspection ........................ 13",
        "13. Liability and Indemnification ............... 14",
        "14. Dispute Resolution .......................... 15",
        "15. Signatures .................................. 16",
    ], 2)

    # --- Page 3: Parties and Premises ---
    add_page_text(doc, "SECTION 1: PARTIES AND PREMISES", [
        "1.1 LANDLORD: Greenfield Property Management LLC, a limited liability company organized under the laws of the State of Oregon, with its principal office at 1200 Commerce Drive, Suite 450, Springfield, OR 97477 (hereinafter referred to as \"Landlord\").",
        "1.2 TENANT(S): Aisha Patel and David Nakamura (hereinafter collectively referred to as \"Tenants\"), currently residing at 558 Oak Boulevard, Portland, OR 97205.",
        "1.3 PREMISES: The residential property located at 742 Evergreen Terrace, Apartment 3B, Springfield, OR 97477, consisting of approximately 1,150 square feet, including two (2) bedrooms, one (1) bathroom, a living room, kitchen, and dedicated storage unit #3B in the basement level.",
        "1.4 CONDITION: The Tenants acknowledge that they have inspected the Premises and accept them in their current condition, subject to the move-in inspection checklist attached as Exhibit A. Any pre-existing damage noted on the checklist shall not be charged against the Tenants' security deposit upon move-out.",
        "1.5 PERMITTED USE: The Premises shall be used exclusively as a private residential dwelling for the Tenants and their approved household members. No commercial, industrial, or professional activities may be conducted on the Premises without prior written consent of the Landlord.",
    ], 3)

    # --- Page 4: Term of Lease ---
    add_page_text(doc, "SECTION 2: TERM OF LEASE", [
        "2.1 INITIAL TERM: This Lease shall commence on March 1, 2025, and shall continue for a period of twelve (12) months, expiring on February 28, 2026 (the \"Initial Term\").",
        "2.2 RENEWAL: Upon expiration of the Initial Term, this Lease shall automatically convert to a month-to-month tenancy unless either party provides at least sixty (60) days written notice of intent to terminate or unless a new lease agreement is executed.",
        "2.3 EARLY OCCUPANCY: If the Landlord permits the Tenants to occupy the Premises prior to the commencement date, such occupancy shall be subject to all terms and conditions of this Lease, and Tenants shall pay a prorated rent for the early occupancy period.",
        "2.4 HOLDOVER: If the Tenants remain in possession of the Premises after the expiration of this Lease without executing a new agreement, the Tenants shall be considered holdover tenants and shall be subject to a monthly rent increase of fifteen percent (15%) above the then-current rate.",
        "2.5 MOVE-IN DATE: The Tenants shall take possession of the Premises no later than March 5, 2025. Failure to take possession within this period without prior arrangement may result in forfeiture of the security deposit and cancellation of this Lease.",
    ], 4)

    # --- Page 5: Rent and Payment ---
    add_page_text(doc, "SECTION 3: RENT AND PAYMENT TERMS", [
        "3.1 MONTHLY RENT: The Tenants agree to pay a monthly rent of One Thousand Eight Hundred Fifty Dollars ($1,850.00) for the duration of the Initial Term. Rent shall be due on the first (1st) day of each calendar month.",
        "3.2 PAYMENT METHOD: Rent shall be payable via electronic funds transfer (EFT), certified check, or money order made payable to Greenfield Property Management LLC. Cash payments are not accepted. Online payment portal: pay.greenfieldpm.com.",
        "3.3 LATE FEES: If rent is not received by the fifth (5th) day of the month, a late fee of Seventy-Five Dollars ($75.00) shall be assessed. An additional fee of Ten Dollars ($10.00) per day shall accrue for each subsequent day the rent remains unpaid, up to a maximum of Two Hundred Dollars ($200.00).",
        "3.4 RETURNED PAYMENTS: A fee of Fifty Dollars ($50.00) shall be charged for any returned or dishonored payment. After two (2) returned payments, the Landlord may require all future payments to be made by certified funds only.",
        "3.5 RENT INCREASES: For any renewal period, the Landlord may increase the monthly rent by providing at least ninety (90) days written notice. Annual increases shall not exceed five percent (5%) of the current rent unless market conditions or property tax increases justify a higher adjustment.",
        "3.6 PRORATION: If this Lease begins or ends on a date other than the first or last day of a calendar month, the rent for that partial month shall be prorated based on a thirty (30) day month.",
    ], 5)

    # --- Page 6: Utilities ---
    add_page_text(doc, "SECTION 4: UTILITIES AND SERVICES", [
        "4.1 TENANT RESPONSIBILITIES: The Tenants shall be responsible for establishing and maintaining accounts for the following utilities: electricity (Pacific Power), natural gas (NW Natural), internet/cable (provider of choice), and telephone service.",
        "4.2 LANDLORD RESPONSIBILITIES: The Landlord shall provide and pay for the following services: water and sewer, garbage and recycling collection, and common area maintenance including hallway lighting and elevator service.",
        "4.3 UTILITY TRANSFER: Tenants must transfer all applicable utility accounts into their names within three (3) business days of the commencement date. Failure to do so may result in disconnection of services, for which the Landlord shall not be held liable.",
        "4.4 CONSERVATION: Tenants agree to use all utilities in a reasonable and responsible manner. Excessive utility usage that results in damage to the Premises or building systems may be charged to the Tenants.",
        "4.5 INTERRUPTION: The Landlord shall not be liable for any interruption of utility services caused by circumstances beyond the Landlord's reasonable control, including but not limited to natural disasters, municipal service failures, or third-party construction activities.",
    ], 6)

    # --- Page 7: Maintenance ---
    add_page_text(doc, "SECTION 5: MAINTENANCE AND REPAIRS", [
        "5.1 TENANT OBLIGATIONS: The Tenants shall maintain the Premises in a clean, sanitary, and safe condition. Tenants shall promptly report any maintenance issues, damage, or hazardous conditions to the Landlord in writing via the maintenance portal at maintenance.greenfieldpm.com.",
        "5.2 LANDLORD OBLIGATIONS: The Landlord shall maintain the structural components of the building, including the roof, exterior walls, foundation, plumbing systems, electrical systems, HVAC systems, and common areas in compliance with all applicable building codes and regulations.",
        "5.3 MINOR REPAIRS: Tenants shall be responsible for minor repairs costing Seventy-Five Dollars ($75.00) or less, including but not limited to replacement of light bulbs, smoke detector batteries, air filters (replaced quarterly), and minor drain unclogging.",
        "5.4 EMERGENCY REPAIRS: In the event of an emergency that threatens life, safety, or significant property damage (such as burst pipes, gas leaks, or electrical fires), Tenants shall immediately contact emergency services (911) and then notify the Landlord's emergency line at (541) 555-0199.",
        "5.5 ALTERATIONS: Tenants shall not make any structural alterations, additions, or improvements to the Premises without prior written consent from the Landlord. This includes but is not limited to painting walls, installing fixtures, modifying built-in shelving, or altering flooring.",
        "5.6 APPLIANCES: The Landlord provides the following appliances in working condition: refrigerator, electric stove/oven, dishwasher, and washer/dryer hookups. The Landlord shall repair or replace these appliances if they fail due to normal wear and tear.",
    ], 7)

    # --- Page 8: Security Deposit and Rules (KEY PAGE) ---
    p8 = doc.new_page(width=W, height=H)
    shape = p8.new_shape()
    shape.draw_line(pymupdf.Point(72, 50), pymupdf.Point(W - 72, 50))
    shape.finish(color=(0.3, 0.3, 0.3), width=1.0)
    shape.draw_line(pymupdf.Point(72, H - 50), pymupdf.Point(W - 72, H - 50))
    shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
    shape.commit()

    p8.insert_text(pymupdf.Point(72, 80), "SECTION 6: SECURITY DEPOSIT AND ADDITIONAL FEES", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))

    y = 110
    sec6_paras = [
        "6.1 SECURITY DEPOSIT: Upon execution of this Lease, the Tenants shall pay a security deposit of $2,500 to the Landlord. This deposit shall be held in a separate, interest-bearing trust account at First National Bank of Springfield, in accordance with Oregon Revised Statutes Section 90.300.",
        "6.2 DEPOSIT RETURN: The security deposit, less any lawful deductions, shall be returned to the Tenants within thirty-one (31) days after the termination of this Lease and the Tenants' complete vacation of the Premises. An itemized statement of any deductions shall accompany any partial return.",
        "6.3 PERMITTED DEDUCTIONS: The Landlord may deduct from the security deposit for: (a) unpaid rent or late fees; (b) repair of damage caused by the Tenants beyond normal wear and tear; (c) cleaning costs if the Premises are not returned in a condition comparable to the move-in inspection; (d) replacement of unreturned keys or access devices.",
        "6.4 MOVE-IN FEE: A non-refundable move-in administrative fee of Two Hundred Dollars ($200.00) is due at lease signing. This covers administrative processing, key issuance, and building access programming.",
    ]

    for para in sec6_paras:
        rect = pymupdf.Rect(72, y, W - 72, H - 70)
        page_excess = p8.insert_textbox(rect, para, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        lines_approx = max(1, len(para) // 65 + 1)
        y += lines_approx * 14 + 8

    # Section 7 on same page
    y += 10
    p8.insert_text(pymupdf.Point(72, y), "SECTION 7: RULES AND RESTRICTIONS", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    y += 25

    sec7_paras = [
        "7.1 PET POLICY: There shall be no pets allowed on the Premises, including but not limited to dogs, cats, birds, reptiles, rodents, and fish aquariums exceeding ten (10) gallons. Service animals certified under the Americans with Disabilities Act are exempt from this restriction.",
        "7.2 NOISE: Tenants shall maintain reasonable noise levels at all times. Quiet hours are enforced from 10:00 PM to 8:00 AM daily. Repeated noise complaints may constitute grounds for lease termination.",
        "7.3 SMOKING: Smoking of any kind, including electronic cigarettes and vaporizers, is strictly prohibited inside the Premises and within twenty-five (25) feet of any building entrance, window, or ventilation intake.",
    ]

    for para in sec7_paras:
        rect = pymupdf.Rect(72, y, W - 72, H - 70)
        page_excess = p8.insert_textbox(rect, para, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        lines_approx = max(1, len(para) // 65 + 1)
        y += lines_approx * 14 + 8

    p8.insert_text(pymupdf.Point(W / 2 - 10, H - 35), "Page 8", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 9: Parking and Common Areas ---
    add_page_text(doc, "SECTION 8: PARKING AND COMMON AREAS", [
        "8.1 PARKING: Each unit is assigned one (1) covered parking space. The Tenants are assigned Space #27 in the underground parking garage. Additional parking spaces may be leased at a rate of Seventy-Five Dollars ($75.00) per month, subject to availability.",
        "8.2 VEHICLE REQUIREMENTS: All vehicles parked on the property must be currently registered, insured, and in operable condition. Recreational vehicles, boats, trailers, and commercial vehicles exceeding one (1) ton are prohibited.",
        "8.3 COMMON AREAS: Tenants shall have access to the following common areas: lobby, hallways, laundry room (Building B basement), fitness center (hours: 5:00 AM - 11:00 PM), rooftop terrace (hours: 8:00 AM - 10:00 PM), and package room.",
        "8.4 STORAGE: Each unit includes one (1) basement storage unit (approximately 4' x 6'). The storage unit must be secured with a Tenant-provided lock. The Landlord is not responsible for items stored in the unit.",
        "8.5 BICYCLES: Bicycle storage is available in the designated racks in the parking garage. Bicycles may not be stored in hallways, stairwells, or balconies.",
    ], 9)

    # --- Page 10: Insurance ---
    add_page_text(doc, "SECTION 9: INSURANCE REQUIREMENTS", [
        "9.1 RENTER'S INSURANCE: The Tenants are required to obtain and maintain a renter's insurance policy with minimum coverage of One Hundred Thousand Dollars ($100,000) in personal liability and Fifty Thousand Dollars ($50,000) in personal property coverage throughout the duration of this Lease.",
        "9.2 PROOF OF INSURANCE: Tenants shall provide proof of insurance to the Landlord prior to or on the commencement date and upon each renewal. The Landlord must be listed as an \"Additional Interested Party\" on the policy.",
        "9.3 LANDLORD INSURANCE: The Landlord maintains a commercial property insurance policy covering the building structure and common areas. This policy does not cover Tenants' personal belongings or liability.",
        "9.4 WAIVER: Tenants acknowledge that the Landlord is not liable for loss or damage to Tenants' personal property caused by theft, fire, water damage, or any other peril, except where such loss results from the Landlord's gross negligence or willful misconduct.",
    ], 10)

    # --- Page 11: Early Termination ---
    add_page_text(doc, "SECTION 10: EARLY TERMINATION", [
        "10.1 TENANT TERMINATION: Tenants may terminate this Lease early by providing sixty (60) days written notice and paying an early termination fee equal to two (2) months' rent ($3,700.00). The security deposit return shall be subject to standard deduction procedures.",
        "10.2 LANDLORD TERMINATION: The Landlord may terminate this Lease for material breach, including but not limited to: failure to pay rent for fifteen (15) or more days, unauthorized occupants, illegal activity on the Premises, or repeated violations of lease terms after written notice.",
        "10.3 MILITARY CLAUSE: In accordance with the Servicemembers Civil Relief Act (SCRA), Tenants who are active-duty military personnel may terminate this Lease with thirty (30) days written notice upon receipt of deployment orders or permanent change of station (PCS) orders.",
        "10.4 DOMESTIC VIOLENCE: In accordance with Oregon law (ORS 90.453), a Tenant who is a victim of domestic violence, sexual assault, or stalking may terminate this Lease with fourteen (14) days written notice and appropriate documentation.",
        "10.5 CASUALTY: If the Premises are rendered uninhabitable due to fire, flood, or other casualty not caused by the Tenants, either party may terminate this Lease immediately upon written notice.",
    ], 11)

    # --- Page 12: Subletting ---
    add_page_text(doc, "SECTION 11: SUBLETTING AND ASSIGNMENT", [
        "11.1 PROHIBITION: The Tenants shall not sublet the Premises or any part thereof, nor assign this Lease or any interest herein, without the prior written consent of the Landlord. Such consent shall not be unreasonably withheld.",
        "11.2 SHORT-TERM RENTALS: Listing the Premises on any short-term rental platform (including Airbnb, VRBO, or similar services) is strictly prohibited and shall constitute a material breach of this Lease.",
        "11.3 GUESTS: Guests may stay on the Premises for a maximum of fourteen (14) consecutive days or twenty-one (21) cumulative days in any twelve-month period. Extended stays require written authorization from the Landlord.",
        "11.4 UNAUTHORIZED OCCUPANTS: Any person residing on the Premises who is not listed on this Lease and has not been approved by the Landlord shall be considered an unauthorized occupant. Discovery of unauthorized occupants constitutes a material breach.",
    ], 12)

    # --- Page 13: Entry and Inspection ---
    add_page_text(doc, "SECTION 12: ENTRY AND INSPECTION", [
        "12.1 LANDLORD ACCESS: The Landlord or authorized agents may enter the Premises for the purposes of inspection, maintenance, repair, showing to prospective tenants or buyers, or in case of emergency.",
        "12.2 NOTICE: Except in cases of emergency, the Landlord shall provide at least twenty-four (24) hours written notice prior to entry. Entry shall occur during reasonable hours (8:00 AM to 6:00 PM) unless otherwise agreed upon.",
        "12.3 INSPECTIONS: The Landlord may conduct routine inspections of the Premises no more than once per quarter, with appropriate advance notice. Move-in and move-out inspections shall be conducted jointly with the Tenants when possible.",
        "12.4 EMERGENCY ACCESS: The Landlord may enter the Premises without notice in case of emergency, including but not limited to fire, flooding, gas leak, or reasonable belief that the Premises have been abandoned.",
        "12.5 LOCK CHANGES: Tenants shall not change or add locks to any doors without prior written consent from the Landlord. The Landlord must be provided with a copy of any approved new keys.",
    ], 13)

    # --- Page 14: Liability ---
    add_page_text(doc, "SECTION 13: LIABILITY AND INDEMNIFICATION", [
        "13.1 TENANT LIABILITY: The Tenants shall be liable for any damage to the Premises, common areas, or other tenants' property caused by the Tenants, their household members, guests, or invitees.",
        "13.2 INDEMNIFICATION: The Tenants agree to indemnify, defend, and hold harmless the Landlord from and against any and all claims, actions, damages, liability, and expense in connection with loss of life, personal injury, or damage to property arising from the Tenants' use of the Premises.",
        "13.3 LANDLORD LIABILITY: The Landlord shall not be liable for any injury or damage caused by other tenants, third parties, or conditions beyond the Landlord's reasonable control, except where such injury or damage results from the Landlord's failure to maintain the Premises in accordance with applicable building codes.",
        "13.4 MOLD: The Landlord has inspected the Premises and is not aware of any mold contamination. Tenants agree to maintain adequate ventilation and promptly report any signs of mold or moisture intrusion.",
        "13.5 LEAD PAINT: The Premises were constructed after 1978; therefore, lead-based paint disclosure is not applicable. However, Tenants shall be provided with the EPA pamphlet \"Protect Your Family From Lead in Your Home\" as required by federal law.",
    ], 14)

    # --- Page 15: Dispute Resolution ---
    add_page_text(doc, "SECTION 14: DISPUTE RESOLUTION", [
        "14.1 MEDIATION: In the event of any dispute arising under this Lease, the parties agree to first attempt resolution through mediation conducted by a mutually agreed-upon mediator. Mediation costs shall be shared equally between the parties.",
        "14.2 ARBITRATION: If mediation fails to resolve the dispute within thirty (30) days, the parties agree to binding arbitration in accordance with the rules of the American Arbitration Association. The arbitration shall be conducted in Lane County, Oregon.",
        "14.3 GOVERNING LAW: This Lease shall be governed by and construed in accordance with the laws of the State of Oregon, including the Oregon Residential Landlord and Tenant Act (ORS Chapter 90).",
        "14.4 ATTORNEY'S FEES: In any legal action to enforce this Lease, the prevailing party shall be entitled to recover reasonable attorney's fees and court costs from the non-prevailing party.",
        "14.5 SEVERABILITY: If any provision of this Lease is found to be invalid or unenforceable by a court of competent jurisdiction, the remaining provisions shall continue in full force and effect.",
        "14.6 ENTIRE AGREEMENT: This Lease, together with all exhibits and addenda, constitutes the entire agreement between the parties. No oral statements or prior written correspondence shall alter the terms herein.",
    ], 15)

    # --- Page 16: Signatures ---
    p16 = doc.new_page(width=W, height=H)
    shape = p16.new_shape()
    shape.draw_line(pymupdf.Point(72, 50), pymupdf.Point(W - 72, 50))
    shape.finish(color=(0.3, 0.3, 0.3), width=1.0)
    shape.draw_line(pymupdf.Point(72, H - 50), pymupdf.Point(W - 72, H - 50))
    shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
    shape.commit()

    p16.insert_text(pymupdf.Point(72, 80), "SECTION 15: SIGNATURES", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))

    p16.insert_text(pymupdf.Point(72, 120), "IN WITNESS WHEREOF, the parties have executed this Residential Lease Agreement", fontsize=10, fontname="helv", color=(0, 0, 0))
    p16.insert_text(pymupdf.Point(72, 134), "as of the date first written above.", fontsize=10, fontname="helv", color=(0, 0, 0))

    p16.insert_text(pymupdf.Point(72, 180), "LANDLORD:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    p16.insert_text(pymupdf.Point(72, 210), "Signature: ___________________________________", fontsize=10, fontname="helv", color=(0, 0, 0))
    p16.insert_text(pymupdf.Point(72, 235), "Name: Robert Greenfield, Managing Partner", fontsize=10, fontname="helv", color=(0, 0, 0))
    p16.insert_text(pymupdf.Point(72, 255), "Date: March 1, 2025", fontsize=10, fontname="helv", color=(0, 0, 0))

    p16.insert_text(pymupdf.Point(72, 310), "TENANT 1:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    p16.insert_text(pymupdf.Point(72, 340), "Signature: ___________________________________", fontsize=10, fontname="helv", color=(0, 0, 0))
    p16.insert_text(pymupdf.Point(72, 365), "Name: Aisha Patel", fontsize=10, fontname="helv", color=(0, 0, 0))
    p16.insert_text(pymupdf.Point(72, 385), "Date: March 1, 2025", fontsize=10, fontname="helv", color=(0, 0, 0))

    p16.insert_text(pymupdf.Point(72, 440), "TENANT 2:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    p16.insert_text(pymupdf.Point(72, 470), "Signature: ___________________________________", fontsize=10, fontname="helv", color=(0, 0, 0))
    p16.insert_text(pymupdf.Point(72, 495), "Name: David Nakamura", fontsize=10, fontname="helv", color=(0, 0, 0))
    p16.insert_text(pymupdf.Point(72, 515), "Date: March 1, 2025", fontsize=10, fontname="helv", color=(0, 0, 0))

    p16.insert_text(pymupdf.Point(W / 2 - 10, H - 35), "Page 16", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Set TOC
    toc = [
        [1, "Cover Page", 1],
        [1, "Table of Contents", 2],
        [1, "Section 1: Parties and Premises", 3],
        [1, "Section 2: Term of Lease", 4],
        [1, "Section 3: Rent and Payment Terms", 5],
        [1, "Section 4: Utilities and Services", 6],
        [1, "Section 5: Maintenance and Repairs", 7],
        [1, "Section 6: Security Deposit and Additional Fees", 8],
        [1, "Section 7: Rules and Restrictions", 8],
        [1, "Section 8: Parking and Common Areas", 9],
        [1, "Section 9: Insurance Requirements", 10],
        [1, "Section 10: Early Termination", 11],
        [1, "Section 11: Subletting and Assignment", 12],
        [1, "Section 12: Entry and Inspection", 13],
        [1, "Section 13: Liability and Indemnification", 14],
        [1, "Section 14: Dispute Resolution", 15],
        [1, "Section 15: Signatures", 16],
    ]
    doc.set_toc(toc)

    # Set metadata
    doc.set_metadata({
        "title": "Residential Lease Agreement - 742 Evergreen Terrace Apt 3B",
        "author": "Greenfield Property Management LLC",
        "subject": "Lease Agreement between Greenfield Property Management and Patel/Nakamura",
        "keywords": "lease, rental, agreement, residential",
        "creator": "Greenfield Property Management",
        "producer": "PyMuPDF",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 16')

    # Verify key text on page 8 (0-indexed = page 7)
    verify_doc = pymupdf.open(OUTPUT)
    p8 = verify_doc[7]
    # Use search_for which handles line-wrapped text
    assert p8.search_for("security deposit of $2,500"), "Missing 'security deposit of $2,500' on page 8"
    assert p8.search_for("no pets allowed"), "Missing 'no pets allowed' on page 8"
    verify_doc.close()
    print("Verified: key phrases present on page 8")

    # Open in Evince on page 8 (0-indexed page 7, but evince uses 1-indexed page-index internally; --page-index is 0-based)
    launch_gui(f'evince --page-index=7 "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
