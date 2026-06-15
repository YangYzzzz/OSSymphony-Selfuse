"""
Initial Setup: Create unsigned contract PDF and prepare environment for digital signing task.
Task ID: pdf_gf3_022
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_022'
CONTRACTS_DIR = f'{WORKDIR}/contracts'
SCRIPTS_DIR = f'{WORKDIR}/scripts'

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
    # Ensure directories exist
    os.makedirs(CONTRACTS_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # Install required libraries for the task
    subprocess.run(
        ['pip3', 'install', 'cryptography', 'pyhanko', 'pyhanko-certvalidator'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    try:
        import pymupdf
    except ImportError:
        subprocess.run(['pip3', 'install', 'PyMuPDF'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import pymupdf

    OUTPUT = f'{CONTRACTS_DIR}/unsigned_contract.pdf'

    # Create a realistic 10-page contract PDF
    doc = pymupdf.open()

    # Common layout
    PAGE_W, PAGE_H = 612, 792  # US Letter
    MARGIN_L = 72
    MARGIN_R = 540
    MARGIN_T = 72
    MARGIN_B = 720
    LINE_H = 14

    def add_header_footer(page, page_num, total_pages):
        """Add consistent header/footer to each page."""
        # Header line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(MARGIN_L, 60), pymupdf.Point(MARGIN_R, 60))
        shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
        shape.commit()
        page.insert_text(pymupdf.Point(MARGIN_L, 55), "Meridian Technologies Inc.", fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4))
        page.insert_text(pymupdf.Point(440, 55), "CONFIDENTIAL", fontsize=8, fontname="hebo", color=(0.7, 0.2, 0.2))
        # Footer
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(MARGIN_L, PAGE_H - 50), pymupdf.Point(MARGIN_R, PAGE_H - 50))
        shape2.finish(color=(0.3, 0.3, 0.3), width=0.5)
        shape2.commit()
        page.insert_text(pymupdf.Point(MARGIN_L, PAGE_H - 38), f"Contract No. MTI-2025-0847 | Page {page_num} of {total_pages}", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # ---- PAGE 1: Title Page ----
    p = doc.new_page(width=PAGE_W, height=PAGE_H)
    p.insert_text(pymupdf.Point(160, 200), "SOFTWARE DEVELOPMENT", fontsize=22, fontname="hebo", color=(0.1, 0.1, 0.4))
    p.insert_text(pymupdf.Point(155, 230), "SERVICES AGREEMENT", fontsize=22, fontname="hebo", color=(0.1, 0.1, 0.4))
    shape = p.new_shape()
    shape.draw_line(pymupdf.Point(160, 240), pymupdf.Point(452, 240))
    shape.finish(color=(0.1, 0.1, 0.4), width=2)
    shape.commit()
    p.insert_text(pymupdf.Point(180, 290), "Contract No. MTI-2025-0847", fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(190, 340), "Between", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(130, 380), "Meridian Technologies Inc.", fontsize=16, fontname="hebo", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(165, 400), "(\"Service Provider\")", fontsize=11, fontname="helv", color=(0.4, 0.4, 0.4))
    p.insert_text(pymupdf.Point(265, 430), "and", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(155, 470), "Cascade Financial Group LLC", fontsize=16, fontname="hebo", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(230, 490), "(\"Client\")", fontsize=11, fontname="helv", color=(0.4, 0.4, 0.4))
    p.insert_text(pymupdf.Point(200, 550), "Effective Date: March 15, 2025", fontsize=12, fontname="helv", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(195, 575), "Expiration Date: March 14, 2027", fontsize=12, fontname="helv", color=(0, 0, 0))
    add_header_footer(p, 1, 10)

    # ---- PAGE 2: Recitals and Definitions ----
    p = doc.new_page(width=PAGE_W, height=PAGE_H)
    add_header_footer(p, 2, 10)
    y = MARGIN_T + 10
    p.insert_text(pymupdf.Point(MARGIN_L, y), "ARTICLE 1 - RECITALS AND DEFINITIONS", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30

    recitals = [
        "WHEREAS, the Service Provider is engaged in the business of software development, consulting, and related technology services;",
        "WHEREAS, the Client desires to engage the Service Provider to develop, implement, and maintain certain software applications and systems as described herein;",
        "WHEREAS, the parties wish to set forth their respective rights, duties, and obligations with respect to such services;",
        "NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth herein, and for other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the parties agree as follows:",
    ]
    for text in recitals:
        rect = pymupdf.Rect(MARGIN_L, y, MARGIN_R, y + 60)
        p.insert_textbox(rect, text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 55

    y += 10
    p.insert_text(pymupdf.Point(MARGIN_L, y), "1.1 Definitions", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 20
    definitions = [
        '"Deliverables" means all software, code, documentation, and other materials produced by Service Provider under this Agreement.',
        '"Project Plan" means the detailed scope, timeline, and milestones document attached as Exhibit A.',
        '"Acceptance Criteria" means the functional and performance specifications set forth in the Project Plan.',
        '"Confidential Information" means all proprietary data, trade secrets, business processes, and technical information disclosed by either party.',
        '"Intellectual Property" means all patents, copyrights, trademarks, trade secrets, and other proprietary rights.',
    ]
    for defn in definitions:
        rect = pymupdf.Rect(MARGIN_L + 20, y, MARGIN_R, y + 45)
        p.insert_textbox(rect, defn, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 42

    # ---- PAGE 3: Scope of Services ----
    p = doc.new_page(width=PAGE_W, height=PAGE_H)
    add_header_footer(p, 3, 10)
    y = MARGIN_T + 10
    p.insert_text(pymupdf.Point(MARGIN_L, y), "ARTICLE 2 - SCOPE OF SERVICES", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30

    scope_sections = [
        ("2.1 Primary Services", [
            "Design, develop, and deploy a cloud-based enterprise resource planning (ERP) system tailored to Client's financial operations.",
            "Integration with Client's existing Oracle database infrastructure and SAP business intelligence platform.",
            "Development of RESTful API endpoints for third-party vendor connectivity.",
            "Implementation of role-based access control (RBAC) with multi-factor authentication.",
            "Creation of automated reporting dashboards using React and D3.js visualization libraries.",
        ]),
        ("2.2 Support Services", [
            "Provide 24/7 technical support during the first 90 days post-deployment.",
            "Conduct monthly system health checks and performance optimization reviews.",
            "Deliver quarterly security audits and vulnerability assessments.",
        ]),
    ]

    for section_title, items in scope_sections:
        p.insert_text(pymupdf.Point(MARGIN_L, y), section_title, fontsize=12, fontname="hebo", color=(0, 0, 0))
        y += 20
        for item in items:
            rect = pymupdf.Rect(MARGIN_L + 20, y, MARGIN_R, y + 42)
            bullet_text = f"\u2022 {item}"
            p.insert_textbox(rect, bullet_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
            y += 38
        y += 10

    # ---- PAGE 4: Timeline and Milestones ----
    p = doc.new_page(width=PAGE_W, height=PAGE_H)
    add_header_footer(p, 4, 10)
    y = MARGIN_T + 10
    p.insert_text(pymupdf.Point(MARGIN_L, y), "ARTICLE 3 - PROJECT TIMELINE AND MILESTONES", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30

    p.insert_text(pymupdf.Point(MARGIN_L, y), "3.1 Project Phases", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 20

    milestones = [
        ("Phase 1: Discovery & Planning", "March 15 - April 30, 2025", "$85,000"),
        ("Phase 2: Architecture Design", "May 1 - June 15, 2025", "$120,000"),
        ("Phase 3: Core Development", "June 16 - October 31, 2025", "$340,000"),
        ("Phase 4: Integration & Testing", "November 1 - December 31, 2025", "$175,000"),
        ("Phase 5: UAT & Deployment", "January 1 - February 28, 2026", "$95,000"),
        ("Phase 6: Post-Launch Support", "March 1 - May 31, 2026", "$60,000"),
    ]

    # Table header
    p.insert_text(pymupdf.Point(MARGIN_L + 10, y), "Phase", fontsize=10, fontname="hebo", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(280, y), "Timeline", fontsize=10, fontname="hebo", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(460, y), "Budget", fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 5
    shape = p.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, y), pymupdf.Point(MARGIN_R, y))
    shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
    shape.commit()
    y += 15

    for phase, timeline, budget in milestones:
        p.insert_text(pymupdf.Point(MARGIN_L + 10, y), phase, fontsize=10, fontname="helv", color=(0, 0, 0))
        p.insert_text(pymupdf.Point(280, y), timeline, fontsize=10, fontname="helv", color=(0, 0, 0))
        p.insert_text(pymupdf.Point(460, y), budget, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 20

    y += 15
    p.insert_text(pymupdf.Point(MARGIN_L, y), "3.2 Total Contract Value: $875,000", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 30
    rect = pymupdf.Rect(MARGIN_L, y, MARGIN_R, y + 80)
    p.insert_textbox(rect, "Payment shall be made in accordance with the milestone completion schedule. Each phase payment is due within thirty (30) calendar days of written acceptance of the corresponding Deliverables by Client. Late payments shall accrue interest at the rate of 1.5% per month or the maximum rate permitted by applicable law, whichever is less.", fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- PAGE 5: Intellectual Property ----
    p = doc.new_page(width=PAGE_W, height=PAGE_H)
    add_header_footer(p, 5, 10)
    y = MARGIN_T + 10
    p.insert_text(pymupdf.Point(MARGIN_L, y), "ARTICLE 4 - INTELLECTUAL PROPERTY RIGHTS", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30

    ip_sections = [
        ("4.1 Ownership of Deliverables", "Upon full payment of all fees due under this Agreement, all Intellectual Property rights in and to the Deliverables shall be assigned to and vest exclusively in the Client. Service Provider hereby irrevocably assigns to Client all right, title, and interest in the Deliverables, including all patents, copyrights, and trade secrets embodied therein."),
        ("4.2 Pre-Existing IP", "Service Provider retains all rights to its pre-existing intellectual property, tools, methodologies, and frameworks (collectively, \"Provider Tools\"). To the extent any Provider Tools are incorporated into the Deliverables, Service Provider grants Client a perpetual, non-exclusive, royalty-free license to use such Provider Tools solely as part of the Deliverables."),
        ("4.3 Third-Party Components", "Service Provider shall identify all third-party software components, libraries, and frameworks incorporated into the Deliverables. All such components shall be subject to commercially reasonable open-source licenses compatible with Client's intended use."),
        ("4.4 Work Product Documentation", "Service Provider shall maintain comprehensive documentation of all development work, including source code comments, API documentation, architecture diagrams, and user manuals sufficient for Client or its designees to independently maintain and extend the Deliverables."),
    ]

    for title, text in ip_sections:
        p.insert_text(pymupdf.Point(MARGIN_L, y), title, fontsize=12, fontname="hebo", color=(0, 0, 0))
        y += 18
        rect = pymupdf.Rect(MARGIN_L, y, MARGIN_R, y + 70)
        p.insert_textbox(rect, text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 75

    # ---- PAGE 6: Confidentiality ----
    p = doc.new_page(width=PAGE_W, height=PAGE_H)
    add_header_footer(p, 6, 10)
    y = MARGIN_T + 10
    p.insert_text(pymupdf.Point(MARGIN_L, y), "ARTICLE 5 - CONFIDENTIALITY", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30

    conf_sections = [
        ("5.1 Obligations", "Each party agrees to hold all Confidential Information of the other party in strict confidence and not to disclose such information to any third party without the prior written consent of the disclosing party. The receiving party shall protect Confidential Information using at least the same degree of care it uses to protect its own confidential information, but in no event less than reasonable care."),
        ("5.2 Exceptions", "Confidential Information shall not include information that: (a) is or becomes publicly available through no fault of the receiving party; (b) was known to the receiving party prior to disclosure; (c) is independently developed by the receiving party without reference to the Confidential Information; or (d) is rightfully received from a third party without restriction on disclosure."),
        ("5.3 Duration", "The obligations of confidentiality shall survive termination of this Agreement for a period of five (5) years from the date of disclosure of the applicable Confidential Information."),
        ("5.4 Return of Materials", "Upon termination or expiration of this Agreement, each party shall promptly return or destroy all copies of the other party's Confidential Information in its possession, except as required by law or regulation."),
    ]

    for title, text in conf_sections:
        p.insert_text(pymupdf.Point(MARGIN_L, y), title, fontsize=12, fontname="hebo", color=(0, 0, 0))
        y += 18
        rect = pymupdf.Rect(MARGIN_L, y, MARGIN_R, y + 70)
        p.insert_textbox(rect, text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 75

    # ---- PAGE 7: Warranties and Liability ----
    p = doc.new_page(width=PAGE_W, height=PAGE_H)
    add_header_footer(p, 7, 10)
    y = MARGIN_T + 10
    p.insert_text(pymupdf.Point(MARGIN_L, y), "ARTICLE 6 - WARRANTIES AND LIMITATION OF LIABILITY", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30

    warranty_sections = [
        ("6.1 Service Provider Warranties", "Service Provider represents and warrants that: (a) it has the requisite skill, experience, and qualifications to perform the services; (b) the Deliverables will conform to the Acceptance Criteria for a period of twelve (12) months following acceptance; (c) the Deliverables will not infringe upon any third party's intellectual property rights; and (d) all services will be performed in a professional and workmanlike manner consistent with industry standards."),
        ("6.2 Disclaimer", "EXCEPT AS EXPRESSLY SET FORTH HEREIN, NEITHER PARTY MAKES ANY WARRANTIES, EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT."),
        ("6.3 Limitation of Liability", "IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING OUT OF OR RELATED TO THIS AGREEMENT, REGARDLESS OF THE THEORY OF LIABILITY. THE TOTAL CUMULATIVE LIABILITY OF SERVICE PROVIDER SHALL NOT EXCEED THE TOTAL FEES PAID OR PAYABLE UNDER THIS AGREEMENT."),
        ("6.4 Indemnification", "Service Provider shall indemnify, defend, and hold harmless Client and its officers, directors, employees, and agents from and against any and all claims, damages, losses, costs, and expenses (including reasonable attorneys' fees) arising from: (a) any breach of Service Provider's warranties; (b) any negligent or wrongful act or omission of Service Provider; or (c) any infringement of third-party intellectual property rights."),
    ]

    for title, text in warranty_sections:
        p.insert_text(pymupdf.Point(MARGIN_L, y), title, fontsize=12, fontname="hebo", color=(0, 0, 0))
        y += 18
        rect = pymupdf.Rect(MARGIN_L, y, MARGIN_R, y + 72)
        p.insert_textbox(rect, text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 78

    # ---- PAGE 8: Termination ----
    p = doc.new_page(width=PAGE_W, height=PAGE_H)
    add_header_footer(p, 8, 10)
    y = MARGIN_T + 10
    p.insert_text(pymupdf.Point(MARGIN_L, y), "ARTICLE 7 - TERMINATION", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30

    term_sections = [
        ("7.1 Termination for Cause", "Either party may terminate this Agreement upon written notice if the other party materially breaches any provision of this Agreement and fails to cure such breach within thirty (30) days after receipt of written notice specifying the breach in reasonable detail."),
        ("7.2 Termination for Convenience", "Client may terminate this Agreement for any reason upon sixty (60) days' prior written notice. In such event, Client shall pay Service Provider for all services performed and expenses incurred through the effective date of termination, plus a termination fee equal to ten percent (10%) of the remaining unbilled contract value."),
        ("7.3 Effect of Termination", "Upon termination: (a) Service Provider shall promptly deliver to Client all completed and in-progress Deliverables; (b) all licenses granted hereunder shall survive termination; (c) each party shall return or destroy the other party's Confidential Information; and (d) Sections 4, 5, 6, and 8 shall survive termination."),
    ]

    for title, text in term_sections:
        p.insert_text(pymupdf.Point(MARGIN_L, y), title, fontsize=12, fontname="hebo", color=(0, 0, 0))
        y += 18
        rect = pymupdf.Rect(MARGIN_L, y, MARGIN_R, y + 65)
        p.insert_textbox(rect, text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 70

    y += 20
    p.insert_text(pymupdf.Point(MARGIN_L, y), "ARTICLE 8 - DISPUTE RESOLUTION", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30

    disp_sections = [
        ("8.1 Negotiation", "The parties shall first attempt to resolve any dispute arising under this Agreement through good faith negotiation between senior executives of each party for a period of thirty (30) days."),
        ("8.2 Mediation", "If negotiation fails, the parties agree to submit the dispute to non-binding mediation administered by the American Arbitration Association under its Commercial Mediation Procedures."),
        ("8.3 Arbitration", "If mediation fails to resolve the dispute within sixty (60) days, the dispute shall be finally resolved by binding arbitration conducted in San Francisco, California, in accordance with the rules of the American Arbitration Association."),
    ]

    for title, text in disp_sections:
        p.insert_text(pymupdf.Point(MARGIN_L, y), title, fontsize=12, fontname="hebo", color=(0, 0, 0))
        y += 18
        rect = pymupdf.Rect(MARGIN_L, y, MARGIN_R, y + 50)
        p.insert_textbox(rect, text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 55

    # ---- PAGE 9: General Provisions ----
    p = doc.new_page(width=PAGE_W, height=PAGE_H)
    add_header_footer(p, 9, 10)
    y = MARGIN_T + 10
    p.insert_text(pymupdf.Point(MARGIN_L, y), "ARTICLE 9 - GENERAL PROVISIONS", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30

    general_sections = [
        ("9.1 Governing Law", "This Agreement shall be governed by and construed in accordance with the laws of the State of California, without giving effect to its conflict of law principles."),
        ("9.2 Entire Agreement", "This Agreement, including all Exhibits attached hereto, constitutes the entire agreement between the parties with respect to the subject matter hereof and supersedes all prior and contemporaneous agreements, understandings, negotiations, and discussions, whether oral or written."),
        ("9.3 Amendments", "No modification or amendment of this Agreement shall be effective unless in writing and signed by authorized representatives of both parties."),
        ("9.4 Waiver", "The failure of either party to enforce any provision of this Agreement shall not constitute a waiver of future enforcement of that or any other provision."),
        ("9.5 Severability", "If any provision of this Agreement is held to be invalid or unenforceable, such provision shall be struck and the remaining provisions shall remain in full force and effect."),
        ("9.6 Assignment", "Neither party may assign this Agreement without the prior written consent of the other party, except that either party may assign this Agreement to a successor in connection with a merger, acquisition, or sale of substantially all of its assets."),
        ("9.7 Force Majeure", "Neither party shall be liable for any delay or failure to perform due to causes beyond its reasonable control, including but not limited to acts of God, war, terrorism, pandemic, natural disaster, government action, or failure of third-party telecommunications networks."),
        ("9.8 Notices", "All notices under this Agreement shall be in writing and shall be deemed given when delivered personally, sent by registered mail, or transmitted by email with confirmed receipt to the addresses set forth on the signature page."),
    ]

    for title, text in general_sections:
        p.insert_text(pymupdf.Point(MARGIN_L, y), title, fontsize=11, fontname="hebo", color=(0, 0, 0))
        y += 16
        rect = pymupdf.Rect(MARGIN_L, y, MARGIN_R, y + 48)
        p.insert_textbox(rect, text, fontsize=9.5, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 50

    # ---- PAGE 10: Signature Page ----
    p = doc.new_page(width=PAGE_W, height=PAGE_H)
    add_header_footer(p, 10, 10)
    y = MARGIN_T + 10
    p.insert_text(pymupdf.Point(MARGIN_L, y), "SIGNATURE PAGE", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 40

    p.insert_text(pymupdf.Point(MARGIN_L, y), "IN WITNESS WHEREOF, the parties hereto have executed this Software Development Services Agreement as of the Effective Date first written above.", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 50

    # Service Provider signature block
    p.insert_text(pymupdf.Point(MARGIN_L, y), "SERVICE PROVIDER:", fontsize=12, fontname="hebo", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(MARGIN_L, y + 20), "Meridian Technologies Inc.", fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 50
    shape = p.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, y), pymupdf.Point(300, y))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    p.insert_text(pymupdf.Point(MARGIN_L, y + 15), "Signature", fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))
    y += 35
    shape2 = p.new_shape()
    shape2.draw_line(pymupdf.Point(MARGIN_L, y), pymupdf.Point(300, y))
    shape2.finish(color=(0, 0, 0), width=0.5)
    shape2.commit()
    p.insert_text(pymupdf.Point(MARGIN_L, y + 15), "Name and Title", fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))
    y += 35
    shape3 = p.new_shape()
    shape3.draw_line(pymupdf.Point(MARGIN_L, y), pymupdf.Point(300, y))
    shape3.finish(color=(0, 0, 0), width=0.5)
    shape3.commit()
    p.insert_text(pymupdf.Point(MARGIN_L, y + 15), "Date", fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))

    y += 60

    # Client signature block
    p.insert_text(pymupdf.Point(MARGIN_L, y), "CLIENT:", fontsize=12, fontname="hebo", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(MARGIN_L, y + 20), "Cascade Financial Group LLC", fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 50
    shape4 = p.new_shape()
    shape4.draw_line(pymupdf.Point(MARGIN_L, y), pymupdf.Point(300, y))
    shape4.finish(color=(0, 0, 0), width=0.5)
    shape4.commit()
    p.insert_text(pymupdf.Point(MARGIN_L, y + 15), "Signature", fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))
    y += 35
    shape5 = p.new_shape()
    shape5.draw_line(pymupdf.Point(MARGIN_L, y), pymupdf.Point(300, y))
    shape5.finish(color=(0, 0, 0), width=0.5)
    shape5.commit()
    p.insert_text(pymupdf.Point(MARGIN_L, y + 15), "Name and Title", fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))
    y += 35
    shape6 = p.new_shape()
    shape6.draw_line(pymupdf.Point(MARGIN_L, y), pymupdf.Point(300, y))
    shape6.finish(color=(0, 0, 0), width=0.5)
    shape6.commit()
    p.insert_text(pymupdf.Point(MARGIN_L, y + 15), "Date", fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))

    # Set metadata
    doc.set_metadata({
        "title": "Software Development Services Agreement - MTI-2025-0847",
        "author": "Meridian Technologies Inc.",
        "subject": "Software Development Contract",
        "keywords": "contract, software, development, services, agreement",
        "creator": "Legal Operations Department",
        "producer": "Contract Management System",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 10')

    # Open the contract in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
