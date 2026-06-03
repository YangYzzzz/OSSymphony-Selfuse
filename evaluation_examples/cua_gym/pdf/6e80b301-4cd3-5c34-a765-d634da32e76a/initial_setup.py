"""
Initial Setup: Create a 16-page lease agreement PDF with realistic legal content.
Task ID: pdf_legal_031
Domain: pdf
The PDF must contain 'Tenant' ~30 times, 'Landlord' ~28 times, 'Default' ~8 times.
No highlight annotations - those are what the agent must add.
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_031'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/lease_agreement.pdf'

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

def create_lease_agreement():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page layout constants
    PAGE_W, PAGE_H = 612, 792  # US Letter
    MARGIN_LEFT = 72
    MARGIN_RIGHT = 540
    MARGIN_TOP = 72
    MARGIN_BOTTOM = 720
    TEXT_WIDTH = MARGIN_RIGHT - MARGIN_LEFT

    # We will build each page with insert_textbox calls.
    # The lease agreement has standard sections typical of a residential lease.

    sections = []

    # ----- PAGE 1: Title & Parties -----
    sections.append({
        "title": "RESIDENTIAL LEASE AGREEMENT",
        "body": (
            "This Residential Lease Agreement (\"Agreement\") is entered into as of "
            "March 15, 2025, by and between the following parties:\n\n"
            "Landlord: Greenfield Property Management LLC, a Delaware limited liability "
            "company, with its principal office located at 4500 Elm Street, Suite 200, "
            "Wilmington, DE 19801 (hereinafter referred to as \"Landlord\").\n\n"
            "Tenant: Alexandra Rivera and Michael Chen, individuals residing at "
            "782 Oakwood Avenue, Apt 3B, Hartford, CT 06103 (hereinafter collectively "
            "referred to as \"Tenant\").\n\n"
            "WHEREAS, the Landlord is the owner of certain real property located at "
            "1250 Maple Ridge Drive, Unit 7C, New Haven, CT 06510 (the \"Premises\"); and\n\n"
            "WHEREAS, the Landlord desires to lease the Premises to the Tenant, and "
            "the Tenant desires to lease the Premises from the Landlord for the term "
            "and upon the conditions set forth herein;\n\n"
            "NOW, THEREFORE, in consideration of the mutual covenants and agreements "
            "contained herein, and for other good and valuable consideration, the receipt "
            "and sufficiency of which are hereby acknowledged, the Landlord and the "
            "Tenant agree as follows:"
        )
    })

    # ----- PAGE 2: Term & Rent -----
    sections.append({
        "title": "ARTICLE 1: TERM OF LEASE",
        "body": (
            "1.1 Lease Term. The Landlord hereby leases the Premises to the Tenant "
            "for a period of twelve (12) months, commencing on April 1, 2025 and "
            "terminating on March 31, 2026 (the \"Lease Term\"), unless sooner terminated "
            "in accordance with the provisions of this Agreement.\n\n"
            "1.2 Renewal. Upon expiration of the initial Lease Term, this Agreement "
            "shall automatically convert to a month-to-month tenancy under the same terms "
            "and conditions, unless either the Landlord or the Tenant provides written "
            "notice of termination at least sixty (60) days prior to the end of the "
            "then-current term.\n\n"
            "1.3 Early Termination. The Tenant may terminate this Agreement prior to "
            "the expiration of the Lease Term by providing the Landlord with ninety (90) "
            "days written notice and payment of an early termination fee equal to two (2) "
            "months' rent.\n\n"
            "ARTICLE 2: RENT\n\n"
            "2.1 Monthly Rent. The Tenant agrees to pay the Landlord a monthly rent "
            "of Two Thousand Four Hundred Dollars ($2,400.00) for the use and occupancy "
            "of the Premises.\n\n"
            "2.2 Payment Due Date. Rent shall be due and payable on the first (1st) day "
            "of each calendar month during the Lease Term. The Tenant shall make rent "
            "payments to the Landlord via electronic funds transfer, certified check, or "
            "money order.\n\n"
            "2.3 Late Fee. If the Tenant fails to pay rent within five (5) business days "
            "after the due date, the Tenant shall pay a late fee of seventy-five dollars "
            "($75.00) per day until the rent is paid in full."
        )
    })

    # ----- PAGE 3: Security Deposit -----
    sections.append({
        "title": "ARTICLE 3: SECURITY DEPOSIT",
        "body": (
            "3.1 Deposit Amount. Upon execution of this Agreement, the Tenant shall "
            "deliver to the Landlord a security deposit in the amount of Four Thousand "
            "Eight Hundred Dollars ($4,800.00) (the \"Security Deposit\").\n\n"
            "3.2 Use of Deposit. The Landlord may use the Security Deposit to remedy "
            "any Default by the Tenant under this Agreement, including but not limited to "
            "unpaid rent, repair of damages beyond normal wear and tear, and cleaning costs.\n\n"
            "3.3 Return of Deposit. The Landlord shall return the Security Deposit, less "
            "any amounts lawfully deducted, to the Tenant within thirty (30) days after "
            "the Tenant vacates the Premises and returns all keys to the Landlord. The "
            "Landlord shall provide the Tenant with an itemized statement of any deductions.\n\n"
            "3.4 Non-Application. The Tenant shall not apply the Security Deposit as the "
            "last month's rent without prior written consent of the Landlord.\n\n"
            "ARTICLE 4: USE OF PREMISES\n\n"
            "4.1 Permitted Use. The Tenant shall use the Premises solely for residential "
            "purposes and shall not conduct any business or commercial activity therein "
            "without the prior written consent of the Landlord.\n\n"
            "4.2 Occupancy. The Premises shall be occupied solely by the Tenant and the "
            "following authorized occupants: Alexandra Rivera and Michael Chen. No additional "
            "persons shall reside at the Premises without the written consent of the Landlord."
        )
    })

    # ----- PAGE 4: Maintenance & Repairs -----
    sections.append({
        "title": "ARTICLE 5: MAINTENANCE AND REPAIRS",
        "body": (
            "5.1 Landlord Obligations. The Landlord shall maintain the structural "
            "components of the Premises, including the roof, exterior walls, foundation, "
            "and all building systems (plumbing, electrical, HVAC) in good working order. "
            "The Landlord shall respond to emergency repair requests within twenty-four (24) "
            "hours and non-emergency requests within seventy-two (72) hours.\n\n"
            "5.2 Tenant Obligations. The Tenant shall maintain the interior of the Premises "
            "in a clean, safe, and sanitary condition. The Tenant shall promptly notify the "
            "Landlord of any maintenance issues, defects, or damage to the Premises. The "
            "Tenant shall be responsible for repairs necessitated by the Tenant's negligence "
            "or misuse.\n\n"
            "5.3 Alterations. The Tenant shall not make any alterations, additions, or "
            "improvements to the Premises without the prior written consent of the Landlord. "
            "Any approved alterations shall become the property of the Landlord upon "
            "termination of this Agreement, unless the Landlord directs the Tenant to "
            "remove them and restore the Premises to its original condition.\n\n"
            "5.4 Pest Control. The Landlord shall be responsible for pest control treatments "
            "at the Premises. The Tenant shall maintain the Premises in a manner that does "
            "not attract pests and shall notify the Landlord immediately upon discovering "
            "any infestation."
        )
    })

    # ----- PAGE 5: Utilities & Services -----
    sections.append({
        "title": "ARTICLE 6: UTILITIES AND SERVICES",
        "body": (
            "6.1 Landlord-Provided Utilities. The Landlord shall be responsible for "
            "providing and paying for the following utilities: water, sewer, and trash "
            "removal services.\n\n"
            "6.2 Tenant-Provided Utilities. The Tenant shall be responsible for "
            "establishing accounts and paying for the following utilities: electricity, "
            "natural gas, internet, cable television, and telephone services. The Tenant "
            "shall ensure all utility accounts remain current during the Lease Term.\n\n"
            "6.3 Service Interruption. The Landlord shall not be liable to the Tenant for "
            "any interruption or failure of utility services caused by circumstances beyond "
            "the Landlord's reasonable control.\n\n"
            "ARTICLE 7: INSURANCE\n\n"
            "7.1 Landlord Insurance. The Landlord shall maintain property insurance covering "
            "the building and common areas. The Landlord's insurance does not cover the "
            "Tenant's personal property.\n\n"
            "7.2 Tenant Insurance. The Tenant is strongly encouraged to obtain and maintain "
            "renter's insurance covering the Tenant's personal property, liability, and "
            "additional living expenses. The Tenant shall provide proof of insurance to the "
            "Landlord upon request.\n\n"
            "7.3 Liability. The Landlord shall not be liable for any damage to the Tenant's "
            "personal property caused by fire, theft, water damage, or any other cause, "
            "except where such damage results from the Landlord's negligence."
        )
    })

    # ----- PAGE 6: Access & Entry -----
    sections.append({
        "title": "ARTICLE 8: ACCESS AND ENTRY",
        "body": (
            "8.1 Landlord Access. The Landlord or the Landlord's agents may enter the "
            "Premises at reasonable times for the following purposes: (a) to inspect the "
            "Premises; (b) to make necessary repairs, alterations, or improvements; "
            "(c) to supply agreed-upon services; (d) to exhibit the Premises to prospective "
            "tenants, buyers, or lenders; and (e) in case of emergency.\n\n"
            "8.2 Notice Requirement. Except in cases of emergency, the Landlord shall "
            "provide the Tenant with at least twenty-four (24) hours written notice before "
            "entering the Premises. The Landlord shall make reasonable efforts to schedule "
            "entry at times convenient to the Tenant.\n\n"
            "8.3 Emergency Access. The Landlord may enter the Premises without prior notice "
            "in the event of an emergency, including but not limited to fire, flood, gas "
            "leak, or other conditions that pose an immediate threat to the health or safety "
            "of the occupants or the integrity of the property.\n\n"
            "8.4 Tenant Cooperation. The Tenant shall cooperate with the Landlord to "
            "facilitate reasonable access to the Premises and shall not unreasonably "
            "withhold consent for entry by the Landlord or the Landlord's authorized agents.\n\n"
            "ARTICLE 9: PARKING\n\n"
            "9.1 Assigned Parking. The Landlord shall provide the Tenant with one (1) "
            "designated parking space in the building garage, identified as Space #47. The "
            "Tenant shall not use any other parking space without the Landlord's permission."
        )
    })

    # ----- PAGE 7: Rules & Regulations -----
    sections.append({
        "title": "ARTICLE 10: RULES AND REGULATIONS",
        "body": (
            "10.1 Community Rules. The Tenant agrees to comply with all rules and "
            "regulations established by the Landlord for the building and common areas, "
            "as may be amended from time to time. The Landlord shall provide the Tenant "
            "with a copy of the current rules upon execution of this Agreement.\n\n"
            "10.2 Noise. The Tenant shall not create or permit any unreasonable noise "
            "or disturbance that may interfere with the quiet enjoyment of other tenants. "
            "Quiet hours shall be observed between 10:00 PM and 8:00 AM daily.\n\n"
            "10.3 Pets. The Tenant shall not keep any pets on the Premises without the "
            "prior written consent of the Landlord. If pets are approved, the Tenant shall "
            "pay a non-refundable pet deposit of Three Hundred Dollars ($300.00) and a "
            "monthly pet rent of Fifty Dollars ($50.00). The Tenant shall be responsible "
            "for any damage caused by pets.\n\n"
            "10.4 Smoking. Smoking of any kind, including electronic cigarettes, is strictly "
            "prohibited inside the Premises and within twenty-five (25) feet of any building "
            "entrance or window. Violation of this provision may result in immediate "
            "termination of this Agreement by the Landlord.\n\n"
            "10.5 Waste Disposal. The Tenant shall dispose of all garbage and recyclable "
            "materials in the designated containers provided by the Landlord. The Tenant "
            "shall not leave trash in hallways, stairwells, or common areas."
        )
    })

    # ----- PAGE 8: Subletting & Assignment -----
    sections.append({
        "title": "ARTICLE 11: SUBLETTING AND ASSIGNMENT",
        "body": (
            "11.1 Prohibition. The Tenant shall not sublet the Premises or any portion "
            "thereof, nor assign this Agreement or any interest herein, without the prior "
            "written consent of the Landlord, which consent shall not be unreasonably "
            "withheld.\n\n"
            "11.2 Short-Term Rentals. The Tenant is expressly prohibited from listing the "
            "Premises on any short-term rental platform, including but not limited to "
            "Airbnb, VRBO, HomeAway, or similar services. Violation of this provision "
            "constitutes a material breach and grounds for immediate Default.\n\n"
            "11.3 Liability. In the event the Landlord consents to a sublease, the Tenant "
            "shall remain fully liable for all obligations under this Agreement. The "
            "subtenant shall be bound by all terms and conditions of this Agreement.\n\n"
            "ARTICLE 12: LANDLORD'S REPRESENTATIONS\n\n"
            "12.1 Authority. The Landlord represents and warrants that the Landlord has "
            "full authority to enter into this Agreement and to lease the Premises to the "
            "Tenant.\n\n"
            "12.2 Habitability. The Landlord represents that the Premises is in a habitable "
            "condition and complies with all applicable building codes and housing regulations "
            "as of the commencement date of this Agreement.\n\n"
            "12.3 Quiet Enjoyment. The Landlord covenants that the Tenant, upon paying the "
            "rent and performing all obligations hereunder, shall peacefully and quietly hold "
            "and enjoy the Premises during the Lease Term without hindrance from the Landlord."
        )
    })

    # ----- PAGE 9: Default -----
    sections.append({
        "title": "ARTICLE 13: DEFAULT AND REMEDIES",
        "body": (
            "13.1 Tenant Default. The occurrence of any of the following events shall "
            "constitute a Default by the Tenant under this Agreement:\n\n"
            "(a) Failure to pay rent or any other monetary obligation within ten (10) days "
            "after the date such payment is due;\n\n"
            "(b) Failure to perform any other obligation under this Agreement within thirty "
            "(30) days after written notice from the Landlord specifying the Default;\n\n"
            "(c) Abandonment of the Premises for a period of fifteen (15) or more "
            "consecutive days without notice to the Landlord;\n\n"
            "(d) Making any false or misleading statement in the Tenant's rental application;\n\n"
            "(e) Engaging in illegal activity on or about the Premises.\n\n"
            "13.2 Landlord Remedies. In the event of a Default by the Tenant, the Landlord "
            "may pursue any one or more of the following remedies:\n\n"
            "(a) Terminate this Agreement by providing written notice to the Tenant;\n\n"
            "(b) Re-enter and take possession of the Premises in accordance with applicable law;\n\n"
            "(c) Recover from the Tenant all damages incurred by the Landlord by reason of "
            "the Tenant's Default, including but not limited to the cost of recovering "
            "possession, expenses of reletting, and any rent deficiency;\n\n"
            "(d) Pursue any other remedy available at law or in equity."
        )
    })

    # ----- PAGE 10: Default continued & Termination -----
    sections.append({
        "title": "ARTICLE 13 (CONTINUED): DEFAULT AND REMEDIES",
        "body": (
            "13.3 Landlord Default. The Landlord shall be in Default under this Agreement "
            "if the Landlord fails to perform any material obligation required of the "
            "Landlord hereunder and such failure continues for thirty (30) days after "
            "written notice from the Tenant specifying the Default.\n\n"
            "13.4 Tenant Remedies. In the event of a Default by the Landlord, the Tenant "
            "may pursue any one or more of the following remedies:\n\n"
            "(a) Terminate this Agreement by providing written notice to the Landlord;\n\n"
            "(b) Withhold rent until the Default is cured, to the extent permitted by "
            "applicable law;\n\n"
            "(c) Make necessary repairs and deduct the cost from future rent payments, "
            "provided the Tenant gives the Landlord reasonable notice and opportunity "
            "to cure;\n\n"
            "(d) Pursue any other remedy available at law or in equity.\n\n"
            "ARTICLE 14: TERMINATION AND SURRENDER\n\n"
            "14.1 Surrender. Upon termination of this Agreement, the Tenant shall surrender "
            "the Premises in the same condition as received, reasonable wear and tear "
            "excepted. The Tenant shall remove all personal property and return all keys "
            "to the Landlord.\n\n"
            "14.2 Holdover. If the Tenant remains in possession of the Premises after "
            "expiration of the Lease Term without the Landlord's written consent, the "
            "Tenant shall be deemed a holdover tenant. The Landlord may charge the Tenant "
            "rent at one hundred fifty percent (150%) of the then-current monthly rent."
        )
    })

    # ----- PAGE 11: Indemnification -----
    sections.append({
        "title": "ARTICLE 15: INDEMNIFICATION",
        "body": (
            "15.1 Tenant Indemnification. The Tenant shall indemnify, defend, and hold "
            "harmless the Landlord from and against any and all claims, actions, damages, "
            "liabilities, and expenses (including reasonable attorneys' fees) arising from "
            "the Tenant's use and occupancy of the Premises, the Tenant's breach of this "
            "Agreement, or the negligence or willful misconduct of the Tenant or the "
            "Tenant's guests and invitees.\n\n"
            "15.2 Landlord Indemnification. The Landlord shall indemnify, defend, and hold "
            "harmless the Tenant from and against any and all claims, actions, damages, "
            "liabilities, and expenses (including reasonable attorneys' fees) arising from "
            "the Landlord's negligence or willful misconduct in the maintenance and "
            "operation of the building and common areas.\n\n"
            "ARTICLE 16: GOVERNING LAW AND DISPUTE RESOLUTION\n\n"
            "16.1 Governing Law. This Agreement shall be governed by and construed in "
            "accordance with the laws of the State of Connecticut, without regard to its "
            "conflict of laws principles.\n\n"
            "16.2 Mediation. In the event of any dispute arising under this Agreement, the "
            "Landlord and the Tenant agree to first attempt to resolve the dispute through "
            "good faith mediation before pursuing litigation.\n\n"
            "16.3 Venue. Any legal action arising from this Agreement shall be brought in "
            "the courts of New Haven County, Connecticut. Both the Landlord and the Tenant "
            "consent to the jurisdiction of such courts."
        )
    })

    # ----- PAGE 12: Notices -----
    sections.append({
        "title": "ARTICLE 17: NOTICES",
        "body": (
            "17.1 Method of Notice. All notices required or permitted under this Agreement "
            "shall be in writing and shall be deemed delivered when: (a) personally delivered "
            "to the intended recipient; (b) sent by certified mail, return receipt requested, "
            "postage prepaid; or (c) sent by recognized overnight courier.\n\n"
            "17.2 Addresses. Notices to the Landlord shall be sent to:\n\n"
            "Greenfield Property Management LLC\n"
            "Attn: Property Manager\n"
            "4500 Elm Street, Suite 200\n"
            "Wilmington, DE 19801\n"
            "Email: leasing@greenfieldpm.com\n\n"
            "Notices to the Tenant shall be sent to the Premises address:\n\n"
            "Alexandra Rivera and Michael Chen\n"
            "1250 Maple Ridge Drive, Unit 7C\n"
            "New Haven, CT 06510\n"
            "Email: a.rivera@email.com\n\n"
            "17.3 Change of Address. Either the Landlord or the Tenant may change the "
            "address for notices by providing written notice to the other party in "
            "accordance with this Article.\n\n"
            "ARTICLE 18: LEAD-BASED PAINT DISCLOSURE\n\n"
            "18.1 Disclosure. The Landlord hereby discloses that the building containing "
            "the Premises was constructed in 1987. Based on building records, there are no "
            "known lead-based paint or lead-based paint hazards in the Premises. The Tenant "
            "acknowledges receipt of the EPA pamphlet \"Protect Your Family From Lead in "
            "Your Home.\""
        )
    })

    # ----- PAGE 13: Additional Terms -----
    sections.append({
        "title": "ARTICLE 19: ADDITIONAL TERMS AND CONDITIONS",
        "body": (
            "19.1 Force Majeure. Neither the Landlord nor the Tenant shall be liable for "
            "failure to perform obligations under this Agreement if such failure is caused "
            "by events beyond reasonable control, including but not limited to natural "
            "disasters, acts of government, pandemic, or civil unrest.\n\n"
            "19.2 Severability. If any provision of this Agreement is held to be invalid, "
            "illegal, or unenforceable, the remaining provisions shall continue in full "
            "force and effect.\n\n"
            "19.3 Entire Agreement. This Agreement constitutes the entire agreement between "
            "the Landlord and the Tenant regarding the lease of the Premises and supersedes "
            "all prior negotiations, representations, warranties, and agreements between "
            "the parties.\n\n"
            "19.4 Amendments. This Agreement may not be amended or modified except by a "
            "written instrument signed by both the Landlord and the Tenant.\n\n"
            "19.5 Waiver. The failure of the Landlord or the Tenant to enforce any provision "
            "of this Agreement shall not constitute a waiver of the right to enforce such "
            "provision or any other provision in the future.\n\n"
            "19.6 Binding Effect. This Agreement shall be binding upon and inure to the "
            "benefit of the Landlord and the Tenant and their respective heirs, executors, "
            "administrators, successors, and permitted assigns."
        )
    })

    # ----- PAGE 14: Compliance & Accessibility -----
    sections.append({
        "title": "ARTICLE 20: COMPLIANCE AND ACCESSIBILITY",
        "body": (
            "20.1 Fair Housing. The Landlord and the Tenant acknowledge that this Agreement "
            "is subject to all applicable federal, state, and local fair housing laws. The "
            "Landlord does not discriminate on the basis of race, color, religion, sex, "
            "national origin, disability, familial status, or any other protected class.\n\n"
            "20.2 ADA Compliance. The Landlord shall make reasonable accommodations for "
            "the Tenant if the Tenant or any authorized occupant has a disability, in "
            "accordance with applicable law. The Tenant shall submit accommodation requests "
            "to the Landlord in writing.\n\n"
            "20.3 Code Compliance. The Tenant shall comply with all applicable laws, "
            "ordinances, and regulations in the Tenant's use of the Premises. The Tenant "
            "shall not use the Premises for any unlawful purpose.\n\n"
            "20.4 Environmental. The Tenant shall not store or use any hazardous materials "
            "on the Premises, except for ordinary household cleaning products used in "
            "reasonable quantities. The Tenant shall notify the Landlord immediately upon "
            "discovery of any environmental hazard.\n\n"
            "20.5 Emergency Procedures. The Tenant acknowledges receipt of the building "
            "emergency evacuation plan. The Tenant shall familiarize all occupants with "
            "emergency exits and procedures. The Landlord maintains fire alarms and "
            "sprinkler systems in compliance with applicable fire codes."
        )
    })

    # ----- PAGE 15: Attachments & Exhibits -----
    sections.append({
        "title": "ARTICLE 21: ATTACHMENTS AND EXHIBITS",
        "body": (
            "The following attachments and exhibits are incorporated into and made a part "
            "of this Agreement:\n\n"
            "Exhibit A: Floor Plan of the Premises\n"
            "Exhibit B: Move-In/Move-Out Condition Report\n"
            "Exhibit C: Building Rules and Regulations\n"
            "Exhibit D: Lead-Based Paint Disclosure Form\n"
            "Exhibit E: Pet Addendum (if applicable)\n\n"
            "The Tenant acknowledges that the Tenant has received, read, and agreed to "
            "all attachments and exhibits listed above. In the event of a conflict between "
            "this Agreement and any attachment or exhibit, the terms of this Agreement "
            "shall prevail unless the attachment or exhibit specifically states otherwise.\n\n"
            "21.1 Condition Report. The Landlord and the Tenant shall jointly complete "
            "the Move-In Condition Report (Exhibit B) within three (3) business days of "
            "the Tenant taking possession of the Premises. This report shall document "
            "the condition of the Premises at the commencement of the Lease Term and "
            "shall serve as the baseline for assessing damages upon termination.\n\n"
            "21.2 Additional Documents. The Landlord may require the Tenant to sign "
            "additional documents reasonably related to the tenancy, including but not "
            "limited to crime-free housing addenda and mold disclosure forms."
        )
    })

    # ----- PAGE 16: Signatures -----
    sections.append({
        "title": "SIGNATURES",
        "body": (
            "IN WITNESS WHEREOF, the Landlord and the Tenant have executed this "
            "Residential Lease Agreement as of the date first written above.\n\n\n"
            "LANDLORD:\n\n"
            "Greenfield Property Management LLC\n\n"
            "By: ___________________________________\n"
            "Name: Jonathan Whitfield\n"
            "Title: Senior Property Manager\n"
            "Date: March 15, 2025\n\n\n"
            "TENANT:\n\n"
            "___________________________________\n"
            "Alexandra Rivera\n"
            "Date: March 15, 2025\n\n\n"
            "___________________________________\n"
            "Michael Chen\n"
            "Date: March 15, 2025\n\n\n"
            "WITNESS:\n\n"
            "___________________________________\n"
            "Name: Patricia Gomez\n"
            "Date: March 15, 2025\n\n\n"
            "This Agreement has been reviewed and approved by legal counsel for the "
            "Landlord and made available for review by the Tenant's legal counsel prior "
            "to execution."
        )
    })

    # Build the PDF
    for i, section in enumerate(sections):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)

        # Page header
        page.insert_text(
            pymupdf.Point(MARGIN_LEFT, 50),
            "RESIDENTIAL LEASE AGREEMENT - Greenfield Property Management LLC",
            fontsize=8,
            fontname="heit",
            color=(0.4, 0.4, 0.4),
        )

        # Horizontal rule under header
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(MARGIN_LEFT, 56), pymupdf.Point(MARGIN_RIGHT, 56))
        shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape.commit()

        # Section title
        y_pos = MARGIN_TOP + 10
        page.insert_text(
            pymupdf.Point(MARGIN_LEFT, y_pos),
            section["title"],
            fontsize=14,
            fontname="hebo",
            color=(0, 0, 0),
        )
        y_pos += 24

        # Body text in textbox
        rect = pymupdf.Rect(MARGIN_LEFT, y_pos, MARGIN_RIGHT, MARGIN_BOTTOM - 20)
        page.insert_textbox(
            rect,
            section["body"],
            fontsize=10.5,
            fontname="tiro",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Footer with page number
        page.insert_text(
            pymupdf.Point(PAGE_W / 2 - 20, PAGE_H - 30),
            f"Page {i + 1} of {len(sections)}",
            fontsize=8,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

    # Set metadata
    doc.set_metadata({
        "title": "Residential Lease Agreement - 1250 Maple Ridge Drive",
        "author": "Greenfield Property Management LLC",
        "subject": "Residential Lease Agreement",
        "keywords": "lease, agreement, rental, residential",
        "creator": "Legal Document Generator",
        "producer": "PyMuPDF",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Count occurrences for verification
    doc = pymupdf.open(OUTPUT)
    full_text = ""
    for page in doc:
        full_text += page.get_text("text")
    doc.close()

    tenant_count = full_text.count("Tenant")
    landlord_count = full_text.count("Landlord")
    default_count = full_text.count("Default")
    print(f'Word counts - Tenant: {tenant_count}, Landlord: {landlord_count}, Default: {default_count}')
    print(f'Page count: {len(sections)}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_lease_agreement()
