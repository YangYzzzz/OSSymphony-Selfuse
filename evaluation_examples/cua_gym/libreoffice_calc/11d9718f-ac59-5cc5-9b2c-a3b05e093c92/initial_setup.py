"""
Initial Setup: Create an 8-page legal contract PDF with 'confidential' in various forms
Task ID: pdf_cr_049
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_049'
OUTPUT = f'{WORKDIR}/Desktop/contract.pdf'

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

    # Page dimensions
    W, H = 612, 792  # US Letter

    # Common formatting
    MARGIN_LEFT = 72
    MARGIN_RIGHT = 540
    TITLE_SIZE = 18
    HEADING_SIZE = 14
    BODY_SIZE = 11
    LINE_HEIGHT = 16

    def add_header_footer(page, page_num):
        """Add header and footer to each page."""
        # Header line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(MARGIN_LEFT, 50), pymupdf.Point(MARGIN_RIGHT, 50))
        shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
        shape.commit()
        page.insert_text(pymupdf.Point(MARGIN_LEFT, 45), "Sterling & Associates LLP",
                         fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4))
        page.insert_text(pymupdf.Point(450, 45), f"Contract Ref: SA-2025-0847",
                         fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))
        # Footer
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(MARGIN_LEFT, 750), pymupdf.Point(MARGIN_RIGHT, 750))
        shape2.finish(color=(0.3, 0.3, 0.3), width=0.5)
        shape2.commit()
        page.insert_text(pymupdf.Point(MARGIN_LEFT, 770), "CONFIDENTIAL - For Authorized Personnel Only",
                         fontsize=7, fontname="hebo", color=(0.6, 0.0, 0.0))
        page.insert_text(pymupdf.Point(500, 770), f"Page {page_num}",
                         fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))

    # ========== PAGE 1: Title Page ==========
    p1 = doc.new_page(width=W, height=H)
    p1.insert_text(pymupdf.Point(150, 200), "MASTER SERVICES AGREEMENT",
                   fontsize=TITLE_SIZE, fontname="hebo", color=(0.1, 0.1, 0.3))
    p1.insert_text(pymupdf.Point(180, 240), "Professional Consulting Services",
                   fontsize=14, fontname="helv", color=(0.2, 0.2, 0.2))

    # Parties
    rect = pymupdf.Rect(MARGIN_LEFT, 300, MARGIN_RIGHT, 450)
    p1.insert_textbox(rect,
        "Between:\n\n"
        "Sterling & Associates LLP (hereinafter referred to as \"the Provider\")\n"
        "Registered at 1420 Commerce Boulevard, Suite 700, Chicago, IL 60601\n\n"
        "And:\n\n"
        "Meridian Technologies Inc. (hereinafter referred to as \"the Client\")\n"
        "Registered at 8900 Innovation Drive, San Jose, CA 95134",
        fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0), align=0)

    p1.insert_text(pymupdf.Point(MARGIN_LEFT, 490), "Effective Date: March 15, 2025",
                   fontsize=BODY_SIZE, fontname="hebo", color=(0, 0, 0))
    p1.insert_text(pymupdf.Point(MARGIN_LEFT, 510), "Contract Duration: 24 months",
                   fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0))

    # Confidential notice on title page
    rect2 = pymupdf.Rect(150, 600, 462, 660)
    p1.insert_textbox(rect2,
        "This document is strictly Confidential and is intended solely for the "
        "use of the named parties. Unauthorized distribution is prohibited.",
        fontsize=10, fontname="heit", color=(0.5, 0.0, 0.0), align=1)

    add_header_footer(p1, 1)

    # ========== PAGE 2: Definitions & Scope ==========
    p2 = doc.new_page(width=W, height=H)
    add_header_footer(p2, 2)

    p2.insert_text(pymupdf.Point(MARGIN_LEFT, 80), "1. DEFINITIONS AND INTERPRETATION",
                   fontsize=HEADING_SIZE, fontname="hebo", color=(0.1, 0.1, 0.3))

    defs_text = (
        '1.1 In this Agreement, unless the context otherwise requires, the following terms '
        'shall have the meanings set forth below:\n\n'
        '"Confidential Information" means any and all non-public, proprietary, or trade secret '
        'information disclosed by either party to the other, whether orally, in writing, or by '
        'inspection of tangible objects, including but not limited to: business plans, financial '
        'data, customer lists, technical specifications, software source code, algorithms, '
        'marketing strategies, and any materials marked as confidential or proprietary.\n\n'
        '1.2 "Deliverables" means the work products, reports, analyses, software, documentation, '
        'and other materials to be provided by the Provider under this Agreement.\n\n'
        '1.3 "Intellectual Property" means patents, copyrights, trademarks, trade secrets, and '
        'any other proprietary rights recognized under applicable law.\n\n'
        '1.4 "Services" means the professional consulting services described in Schedule A, '
        'including any modifications agreed upon in writing by both parties.'
    )
    rect3 = pymupdf.Rect(MARGIN_LEFT, 100, MARGIN_RIGHT, 380)
    p2.insert_textbox(rect3, defs_text, fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0), align=3)

    p2.insert_text(pymupdf.Point(MARGIN_LEFT, 400), "2. SCOPE OF SERVICES",
                   fontsize=HEADING_SIZE, fontname="hebo", color=(0.1, 0.1, 0.3))

    scope_text = (
        '2.1 The Provider shall deliver the Services as outlined in Schedule A attached hereto. '
        'All work shall be performed in accordance with industry best practices and applicable '
        'professional standards.\n\n'
        '2.2 The Provider shall assign qualified personnel with appropriate expertise to perform '
        'the Services. The Client may request replacement of any assigned personnel, provided '
        'such request is made in writing with reasonable justification.\n\n'
        '2.3 Any changes to the scope of Services shall require a written amendment signed by '
        'authorized representatives of both parties. Such amendments shall specify the impact '
        'on timelines, deliverables, and compensation.'
    )
    rect4 = pymupdf.Rect(MARGIN_LEFT, 420, MARGIN_RIGHT, 650)
    p2.insert_textbox(rect4, scope_text, fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0), align=3)

    # ========== PAGE 3: Compensation & Payment ==========
    p3 = doc.new_page(width=W, height=H)
    add_header_footer(p3, 3)

    p3.insert_text(pymupdf.Point(MARGIN_LEFT, 80), "3. COMPENSATION AND PAYMENT TERMS",
                   fontsize=HEADING_SIZE, fontname="hebo", color=(0.1, 0.1, 0.3))

    comp_text = (
        '3.1 The Client shall pay the Provider a total fee of Four Hundred Seventy-Five Thousand '
        'US Dollars ($475,000.00) for the Services, payable in accordance with the milestone '
        'schedule set forth in Schedule B.\n\n'
        '3.2 Invoices shall be submitted within fifteen (15) business days following completion '
        'of each milestone. Payment shall be due within thirty (30) calendar days of receipt '
        'of a properly submitted invoice.\n\n'
        '3.3 Late payments shall accrue interest at the rate of 1.5% per month or the maximum '
        'rate permitted by applicable law, whichever is less.\n\n'
        '3.4 The Provider shall maintain detailed time and expense records, which shall be made '
        'available for review by the Client upon reasonable request. All expense claims must be '
        'supported by original receipts or other acceptable documentation.'
    )
    rect5 = pymupdf.Rect(MARGIN_LEFT, 100, MARGIN_RIGHT, 360)
    p3.insert_textbox(rect5, comp_text, fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0), align=3)

    p3.insert_text(pymupdf.Point(MARGIN_LEFT, 380), "4. TERM AND TERMINATION",
                   fontsize=HEADING_SIZE, fontname="hebo", color=(0.1, 0.1, 0.3))

    term_text = (
        '4.1 This Agreement shall commence on the Effective Date and shall remain in force for '
        'a period of twenty-four (24) months, unless terminated earlier in accordance with this '
        'Section.\n\n'
        '4.2 Either party may terminate this Agreement for convenience upon ninety (90) days '
        'prior written notice to the other party.\n\n'
        '4.3 Either party may terminate this Agreement immediately upon written notice if the '
        'other party commits a material breach and fails to cure such breach within thirty (30) '
        'days of receiving written notice specifying the breach.\n\n'
        '4.4 Upon termination, the Provider shall deliver all completed Deliverables and return '
        'all confidential materials belonging to the Client within fifteen (15) business days.'
    )
    rect6 = pymupdf.Rect(MARGIN_LEFT, 400, MARGIN_RIGHT, 700)
    p3.insert_textbox(rect6, term_text, fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0), align=3)

    # ========== PAGE 4: Confidentiality ==========
    p4 = doc.new_page(width=W, height=H)
    add_header_footer(p4, 4)

    p4.insert_text(pymupdf.Point(MARGIN_LEFT, 80), "5. CONFIDENTIALITY OBLIGATIONS",
                   fontsize=HEADING_SIZE, fontname="hebo", color=(0.1, 0.1, 0.3))

    conf_text = (
        '5.1 Each party acknowledges that in the course of performing under this Agreement, it '
        'may receive or have access to Confidential Information of the other party. Each party '
        'agrees to hold all such Confidential Information in strict confidence.\n\n'
        '5.2 The receiving party shall not disclose any confidential materials to any third party '
        'without the prior written consent of the disclosing party, except to those employees, '
        'contractors, or advisors who have a legitimate need to know and who are bound by '
        'confidentiality obligations no less restrictive than those contained herein.\n\n'
        '5.3 The obligations of confidentiality shall not apply to information that: (a) is or '
        'becomes publicly available through no fault of the receiving party; (b) was rightfully '
        'in the possession of the receiving party prior to disclosure; (c) is independently '
        'developed by the receiving party without reference to the CONFIDENTIAL material; or '
        '(d) is required to be disclosed by law or regulation.\n\n'
        '5.4 Upon termination or expiration of this Agreement, each party shall promptly return '
        'or destroy all Confidential Information received from the other party, and shall certify '
        'such return or destruction in writing. This obligation extends to all copies, extracts, '
        'and summaries of confidential documents.\n\n'
        '5.5 The confidentiality obligations set forth in this Section shall survive the '
        'termination or expiration of this Agreement for a period of five (5) years.'
    )
    rect7 = pymupdf.Rect(MARGIN_LEFT, 100, MARGIN_RIGHT, 520)
    p4.insert_textbox(rect7, conf_text, fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0), align=3)

    p4.insert_text(pymupdf.Point(MARGIN_LEFT, 540), "6. INTELLECTUAL PROPERTY",
                   fontsize=HEADING_SIZE, fontname="hebo", color=(0.1, 0.1, 0.3))

    ip_text = (
        '6.1 All Intellectual Property rights in the Deliverables created specifically for the '
        'Client under this Agreement shall vest in the Client upon full payment. The Provider '
        'retains ownership of all pre-existing tools, methodologies, and frameworks.\n\n'
        '6.2 The Provider grants the Client a perpetual, non-exclusive license to use any '
        'pre-existing materials incorporated into the Deliverables.'
    )
    rect8 = pymupdf.Rect(MARGIN_LEFT, 560, MARGIN_RIGHT, 720)
    p4.insert_textbox(rect8, ip_text, fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0), align=3)

    # ========== PAGE 5: Liability & Indemnification ==========
    p5 = doc.new_page(width=W, height=H)
    add_header_footer(p5, 5)

    p5.insert_text(pymupdf.Point(MARGIN_LEFT, 80), "7. LIABILITY AND INDEMNIFICATION",
                   fontsize=HEADING_SIZE, fontname="hebo", color=(0.1, 0.1, 0.3))

    liab_text = (
        '7.1 The Provider shall indemnify and hold harmless the Client from any claims, damages, '
        'or losses arising from the Provider\'s negligence or willful misconduct in performing '
        'the Services.\n\n'
        '7.2 The Client shall indemnify and hold harmless the Provider from any claims arising '
        'from the Client\'s use of the Deliverables in a manner not contemplated by this Agreement.\n\n'
        '7.3 IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, '
        'CONSEQUENTIAL, OR PUNITIVE DAMAGES, REGARDLESS OF THE CAUSE OF ACTION OR THE THEORY '
        'OF LIABILITY, EVEN IF SUCH PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.\n\n'
        '7.4 The aggregate liability of the Provider under this Agreement shall not exceed the '
        'total fees paid or payable under this Agreement during the twelve (12) month period '
        'preceding the claim.'
    )
    rect9 = pymupdf.Rect(MARGIN_LEFT, 100, MARGIN_RIGHT, 380)
    p5.insert_textbox(rect9, liab_text, fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0), align=3)

    p5.insert_text(pymupdf.Point(MARGIN_LEFT, 400), "8. REPRESENTATIONS AND WARRANTIES",
                   fontsize=HEADING_SIZE, fontname="hebo", color=(0.1, 0.1, 0.3))

    warr_text = (
        '8.1 Each party represents that it has the legal authority to enter into this Agreement '
        'and to perform its obligations hereunder.\n\n'
        '8.2 The Provider warrants that the Services shall be performed in a professional and '
        'workmanlike manner consistent with generally accepted industry standards.\n\n'
        '8.3 The Provider warrants that the Deliverables shall not infringe upon the intellectual '
        'property rights of any third party. Any breach involving confidential trade secrets '
        'shall be subject to immediate remediation.\n\n'
        '8.4 EXCEPT AS EXPRESSLY SET FORTH IN THIS AGREEMENT, NEITHER PARTY MAKES ANY '
        'WARRANTIES, WHETHER EXPRESS, IMPLIED, OR STATUTORY, INCLUDING WITHOUT LIMITATION ANY '
        'IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.'
    )
    rect10 = pymupdf.Rect(MARGIN_LEFT, 420, MARGIN_RIGHT, 700)
    p5.insert_textbox(rect10, warr_text, fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0), align=3)

    # ========== PAGE 6: Dispute Resolution ==========
    p6 = doc.new_page(width=W, height=H)
    add_header_footer(p6, 6)

    p6.insert_text(pymupdf.Point(MARGIN_LEFT, 80), "9. DISPUTE RESOLUTION",
                   fontsize=HEADING_SIZE, fontname="hebo", color=(0.1, 0.1, 0.3))

    disp_text = (
        '9.1 The parties agree to attempt to resolve any dispute arising out of or relating to '
        'this Agreement through good faith negotiation. Either party may initiate negotiations '
        'by providing written notice describing the dispute to the other party.\n\n'
        '9.2 If the parties are unable to resolve the dispute through negotiation within thirty '
        '(30) days, either party may submit the dispute to binding arbitration administered by '
        'the American Arbitration Association under its Commercial Arbitration Rules.\n\n'
        '9.3 The arbitration shall be conducted in Chicago, Illinois, before a panel of three '
        'arbitrators. The arbitrators shall have expertise in commercial contracts and technology '
        'services. All arbitration proceedings shall be treated as confidential by both parties.\n\n'
        '9.4 The decision of the arbitrators shall be final and binding upon both parties. '
        'Judgment upon the award may be entered in any court of competent jurisdiction.\n\n'
        '9.5 Notwithstanding the foregoing, either party may seek injunctive relief in a court '
        'of competent jurisdiction to prevent the unauthorized use or disclosure of Confidential '
        'Information or to protect its Intellectual Property rights.'
    )
    rect11 = pymupdf.Rect(MARGIN_LEFT, 100, MARGIN_RIGHT, 430)
    p6.insert_textbox(rect11, disp_text, fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0), align=3)

    p6.insert_text(pymupdf.Point(MARGIN_LEFT, 450), "10. DATA PROTECTION AND PRIVACY",
                   fontsize=HEADING_SIZE, fontname="hebo", color=(0.1, 0.1, 0.3))

    data_text = (
        '10.1 Each party shall comply with all applicable data protection laws and regulations, '
        'including but not limited to the General Data Protection Regulation (GDPR) and the '
        'California Consumer Privacy Act (CCPA).\n\n'
        '10.2 The Provider shall implement and maintain appropriate technical and organizational '
        'measures to protect personal data processed in connection with the Services. All data '
        'handling procedures must comply with the confidential data protection standards '
        'established by the Client.\n\n'
        '10.3 In the event of a data breach affecting personal data, the Provider shall notify '
        'the Client within seventy-two (72) hours of becoming aware of the breach.'
    )
    rect12 = pymupdf.Rect(MARGIN_LEFT, 470, MARGIN_RIGHT, 700)
    p6.insert_textbox(rect12, data_text, fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0), align=3)

    # ========== PAGE 7: General Provisions ==========
    p7 = doc.new_page(width=W, height=H)
    add_header_footer(p7, 7)

    p7.insert_text(pymupdf.Point(MARGIN_LEFT, 80), "11. GENERAL PROVISIONS",
                   fontsize=HEADING_SIZE, fontname="hebo", color=(0.1, 0.1, 0.3))

    gen_text = (
        '11.1 Force Majeure. Neither party shall be liable for any failure or delay in '
        'performing its obligations due to circumstances beyond its reasonable control, '
        'including acts of God, natural disasters, pandemics, war, terrorism, strikes, '
        'government orders, or failures of telecommunications networks.\n\n'
        '11.2 Assignment. Neither party may assign this Agreement without the prior written '
        'consent of the other party, except that either party may assign this Agreement to an '
        'affiliate or in connection with a merger, acquisition, or sale of substantially all '
        'its assets.\n\n'
        '11.3 Notices. All notices under this Agreement shall be in writing and delivered by '
        'certified mail, overnight courier, or email with confirmed receipt to the addresses '
        'specified on the signature page.\n\n'
        '11.4 Governing Law. This Agreement shall be governed by and construed in accordance '
        'with the laws of the State of Illinois, without regard to its conflict of laws '
        'provisions.\n\n'
        '11.5 Entire Agreement. This Agreement, including all Schedules and Exhibits attached '
        'hereto, constitutes the entire agreement between the parties with respect to the '
        'subject matter hereof and supersedes all prior negotiations, representations, and '
        'agreements. All confidential arrangements previously discussed are incorporated herein.\n\n'
        '11.6 Severability. If any provision of this Agreement is held to be invalid or '
        'unenforceable, the remaining provisions shall continue in full force and effect.\n\n'
        '11.7 Waiver. The failure of either party to enforce any right under this Agreement '
        'shall not constitute a waiver of such right.'
    )
    rect13 = pymupdf.Rect(MARGIN_LEFT, 100, MARGIN_RIGHT, 600)
    p7.insert_textbox(rect13, gen_text, fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0), align=3)

    # ========== PAGE 8: Signatures ==========
    p8 = doc.new_page(width=W, height=H)
    add_header_footer(p8, 8)

    p8.insert_text(pymupdf.Point(MARGIN_LEFT, 80), "12. EXECUTION",
                   fontsize=HEADING_SIZE, fontname="hebo", color=(0.1, 0.1, 0.3))

    exec_text = (
        'IN WITNESS WHEREOF, the parties hereto have executed this Master Services Agreement '
        'as of the Effective Date first written above. By signing below, each party confirms '
        'that it has read and understood all terms, including the Confidential Information '
        'provisions set forth in Section 5.'
    )
    rect14 = pymupdf.Rect(MARGIN_LEFT, 100, MARGIN_RIGHT, 180)
    p8.insert_textbox(rect14, exec_text, fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0), align=3)

    # Signature blocks
    y_start = 220
    for party, name, title in [
        ("FOR THE PROVIDER:", "Robert A. Sterling", "Managing Partner"),
        ("FOR THE CLIENT:", "Dr. Priya Ramanathan", "Chief Executive Officer"),
    ]:
        p8.insert_text(pymupdf.Point(MARGIN_LEFT, y_start), party,
                       fontsize=BODY_SIZE, fontname="hebo", color=(0, 0, 0))
        p8.insert_text(pymupdf.Point(MARGIN_LEFT, y_start + 20), "Sterling & Associates LLP" if "PROVIDER" in party else "Meridian Technologies Inc.",
                       fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0))

        # Signature line
        shape = p8.new_shape()
        shape.draw_line(pymupdf.Point(MARGIN_LEFT, y_start + 70), pymupdf.Point(300, y_start + 70))
        shape.finish(color=(0, 0, 0), width=0.5)
        shape.commit()

        p8.insert_text(pymupdf.Point(MARGIN_LEFT, y_start + 85), f"Name: {name}",
                       fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0))
        p8.insert_text(pymupdf.Point(MARGIN_LEFT, y_start + 100), f"Title: {title}",
                       fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0))
        p8.insert_text(pymupdf.Point(MARGIN_LEFT, y_start + 115), "Date: March 15, 2025",
                       fontsize=BODY_SIZE, fontname="helv", color=(0, 0, 0))

        y_start += 160

    # Final confidential notice
    p8.insert_text(pymupdf.Point(MARGIN_LEFT, 620),
                   "NOTICE: This executed agreement contains CONFIDENTIAL business terms.",
                   fontsize=10, fontname="hebo", color=(0.6, 0.0, 0.0))
    p8.insert_text(pymupdf.Point(MARGIN_LEFT, 640),
                   "Distribution of this document beyond authorized signatories requires written",
                   fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))
    p8.insert_text(pymupdf.Point(MARGIN_LEFT, 655),
                   "approval from the Legal Department of both parties.",
                   fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))

    # Set metadata
    doc.set_metadata({
        "title": "Master Services Agreement - SA-2025-0847",
        "author": "Sterling & Associates LLP",
        "subject": "Professional Consulting Services Contract",
        "keywords": "contract, services, consulting, confidential",
        "creator": "Legal Document System",
    })

    # Set TOC
    toc = [
        [1, "1. Definitions and Interpretation", 2],
        [1, "2. Scope of Services", 2],
        [1, "3. Compensation and Payment Terms", 3],
        [1, "4. Term and Termination", 3],
        [1, "5. Confidentiality Obligations", 4],
        [1, "6. Intellectual Property", 4],
        [1, "7. Liability and Indemnification", 5],
        [1, "8. Representations and Warranties", 5],
        [1, "9. Dispute Resolution", 6],
        [1, "10. Data Protection and Privacy", 6],
        [1, "11. General Provisions", 7],
        [1, "12. Execution", 8],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify the file and count occurrences for reference
    doc = pymupdf.open(OUTPUT)
    print(f'Page count: {doc.page_count}')
    for i in range(doc.page_count):
        text = doc[i].get_text("text").lower()
        count = text.count("confidential")
        if count > 0:
            print(f'  Page {i+1}: {count} occurrence(s) of "confidential"')
    doc.close()

    # Open PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
