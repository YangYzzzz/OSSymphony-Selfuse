"""
Initial Setup: Create two versions of a contract PDF for diff comparison
Task ID: pdf_aw_049
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_049'
DOCS_DIR = f'{WORKDIR}/docs'
V1_PATH = f'{DOCS_DIR}/contract_v1.pdf'
V2_PATH = f'{DOCS_DIR}/contract_v2.pdf'


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


# ---------- Contract content shared by both versions ----------

PAGE_WIDTH, PAGE_HEIGHT = 595, 842  # A4

# Each page is a list of (y_offset, text, fontname, fontsize) tuples
# We'll define all 8 pages of contract_v1 content

CONTRACT_TITLE = "MASTER SERVICE AGREEMENT"
CONTRACT_SUBTITLE = "Between Nextera Solutions Inc. and Pinnacle Dynamics Corp."

# Page contents for V1 (the base contract)
V1_PAGES = [
    # Page 1 - Title and Introduction
    [
        (60, CONTRACT_TITLE, "hebo", 18),
        (90, CONTRACT_SUBTITLE, "heit", 12),
        (120, "Agreement Date: January 15, 2025", "helv", 11),
        (140, "Agreement Number: MSA-2025-00847", "helv", 11),
        (175, "1. PARTIES", "hebo", 14),
        (200, 'This Master Service Agreement ("Agreement") is entered into by and between:', "helv", 11),
        (225, "Nextera Solutions Inc., a Delaware corporation with principal offices at", "helv", 11),
        (245, "2400 Innovation Drive, Suite 500, San Jose, CA 95134 (hereinafter referred", "helv", 11),
        (265, 'to as the "Service Provider");', "helv", 11),
        (290, "and", "helv", 11),
        (315, "Pinnacle Dynamics Corp., a New York corporation with principal offices at", "helv", 11),
        (335, "780 Enterprise Boulevard, Floor 12, New York, NY 10001 (hereinafter", "helv", 11),
        (355, 'referred to as the "Client").', "helv", 11),
        (390, "2. RECITALS", "hebo", 14),
        (415, "WHEREAS, the Service Provider is engaged in the business of providing", "helv", 11),
        (435, "enterprise software development, cloud infrastructure management, and", "helv", 11),
        (455, "technical consulting services; and", "helv", 11),
        (480, "WHEREAS, the Client desires to engage the Service Provider to perform", "helv", 11),
        (500, "certain services as described in the Statement of Work attached hereto;", "helv", 11),
        (525, "NOW, THEREFORE, in consideration of the mutual covenants and agreements", "helv", 11),
        (545, "herein contained, the parties agree as follows.", "helv", 11),
    ],
    # Page 2 - Scope of Services (will differ in V2)
    [
        (60, "3. SCOPE OF SERVICES", "hebo", 14),
        (85, "3.1 The Service Provider shall provide the following services to the Client:", "helv", 11),
        (110, "  (a) Custom software development for the Client's inventory management", "helv", 11),
        (130, "      system, including design, coding, testing, and deployment.", "helv", 11),
        (155, "  (b) Cloud infrastructure setup and management on Amazon Web Services", "helv", 11),
        (175, "      (AWS), including server provisioning, load balancing, and monitoring.", "helv", 11),
        (200, "  (c) Technical consulting for system architecture and technology stack", "helv", 11),
        (220, "      selection, delivered through weekly advisory sessions.", "helv", 11),
        (250, "3.2 The Service Provider shall assign a dedicated project manager to", "helv", 11),
        (270, "oversee all deliverables and serve as the primary point of contact.", "helv", 11),
        (300, "3.3 All services shall be performed in accordance with industry best", "helv", 11),
        (320, "practices and the quality standards set forth in Appendix B.", "helv", 11),
        (350, "3.4 The Service Provider shall deliver monthly progress reports to the", "helv", 11),
        (370, "Client detailing work completed, milestones achieved, and any issues", "helv", 11),
        (390, "encountered during the reporting period.", "helv", 11),
    ],
    # Page 3 - Term and Termination
    [
        (60, "4. TERM AND TERMINATION", "hebo", 14),
        (85, "4.1 This Agreement shall commence on February 1, 2025 and shall", "helv", 11),
        (105, "continue for an initial term of twenty-four (24) months, unless earlier", "helv", 11),
        (125, "terminated in accordance with this Section.", "helv", 11),
        (155, "4.2 Either party may terminate this Agreement for convenience by", "helv", 11),
        (175, "providing ninety (90) days' prior written notice to the other party.", "helv", 11),
        (205, "4.3 Either party may terminate this Agreement immediately upon written", "helv", 11),
        (225, "notice if the other party:", "helv", 11),
        (250, "  (a) Commits a material breach of this Agreement and fails to cure", "helv", 11),
        (270, "      such breach within thirty (30) days after receiving written notice;", "helv", 11),
        (295, "  (b) Becomes insolvent, files for bankruptcy, or has a receiver", "helv", 11),
        (315, "      appointed for a substantial portion of its assets;", "helv", 11),
        (340, "  (c) Ceases to conduct business in the normal course of operations.", "helv", 11),
        (370, "4.4 Upon termination, the Service Provider shall deliver all completed", "helv", 11),
        (390, "work products and documentation to the Client within fifteen (15)", "helv", 11),
        (410, "business days of the effective date of termination.", "helv", 11),
    ],
    # Page 4 - Compensation (will differ in V2)
    [
        (60, "5. COMPENSATION AND PAYMENT", "hebo", 14),
        (85, "5.1 The Client shall pay the Service Provider the following fees:", "helv", 11),
        (110, "  (a) Software Development: $185.00 per hour for senior developers", "helv", 11),
        (130, "      and $145.00 per hour for mid-level developers.", "helv", 11),
        (155, "  (b) Cloud Infrastructure: A fixed monthly fee of $12,500.00 for", "helv", 11),
        (175, "      standard management services.", "helv", 11),
        (200, "  (c) Technical Consulting: $275.00 per hour for consulting sessions.", "helv", 11),
        (230, "5.2 The Service Provider shall submit invoices on a monthly basis,", "helv", 11),
        (250, "due within thirty (30) days of receipt. Late payments shall accrue", "helv", 11),
        (270, "interest at a rate of 1.5% per month.", "helv", 11),
        (300, "5.3 The Client shall reimburse the Service Provider for pre-approved", "helv", 11),
        (320, "travel and out-of-pocket expenses within fifteen (15) days of", "helv", 11),
        (340, "submission of expense reports with supporting documentation.", "helv", 11),
        (370, "5.4 All fees are exclusive of applicable taxes. The Client shall be", "helv", 11),
        (390, "responsible for all sales, use, and similar taxes arising from this", "helv", 11),
        (410, "Agreement, excluding taxes based on the Service Provider's income.", "helv", 11),
    ],
    # Page 5 - Intellectual Property (will differ in V2)
    [
        (60, "6. INTELLECTUAL PROPERTY RIGHTS", "hebo", 14),
        (85, "6.1 All intellectual property developed by the Service Provider under", "helv", 11),
        (105, "this Agreement shall be owned by the Client upon full payment of all", "helv", 11),
        (125, "fees associated with such work.", "helv", 11),
        (155, "6.2 The Service Provider retains ownership of all pre-existing", "helv", 11),
        (175, "intellectual property, tools, frameworks, and methodologies used in", "helv", 11),
        (195, "performing the services. The Service Provider grants the Client a", "helv", 11),
        (215, "non-exclusive, perpetual license to use such pre-existing materials", "helv", 11),
        (235, "as incorporated into the deliverables.", "helv", 11),
        (265, "6.3 The Client shall retain all ownership rights to its proprietary", "helv", 11),
        (285, "data, business processes, trade secrets, and confidential information", "helv", 11),
        (305, "provided to the Service Provider during the course of this Agreement.", "helv", 11),
        (335, "6.4 Neither party shall use the other party's trademarks, logos, or", "helv", 11),
        (355, "brand assets without prior written consent, except as required for", "helv", 11),
        (375, "performance under this Agreement.", "helv", 11),
    ],
    # Page 6 - Confidentiality
    [
        (60, "7. CONFIDENTIALITY", "hebo", 14),
        (85, "7.1 Each party agrees to hold in strict confidence all Confidential", "helv", 11),
        (105, "Information received from the other party. Confidential Information", "helv", 11),
        (125, "includes, but is not limited to: technical data, trade secrets,", "helv", 11),
        (145, "business plans, customer lists, financial information, and any", "helv", 11),
        (165, "information designated as confidential.", "helv", 11),
        (195, "7.2 The receiving party shall:", "helv", 11),
        (220, "  (a) Use Confidential Information solely for purposes of performing", "helv", 11),
        (240, "      obligations under this Agreement;", "helv", 11),
        (265, "  (b) Restrict disclosure to employees and contractors who have a", "helv", 11),
        (285, "      legitimate need to know and are bound by confidentiality", "helv", 11),
        (305, "      obligations no less protective than this Section;", "helv", 11),
        (330, "  (c) Not disclose Confidential Information to any third party", "helv", 11),
        (350, "      without prior written consent of the disclosing party.", "helv", 11),
        (380, "7.3 These confidentiality obligations shall survive the termination", "helv", 11),
        (400, "of this Agreement for a period of five (5) years.", "helv", 11),
    ],
    # Page 7 - Liability and Indemnification (will differ in V2)
    [
        (60, "8. LIMITATION OF LIABILITY", "hebo", 14),
        (85, "8.1 IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY INDIRECT,", "helv", 11),
        (105, "INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING", "helv", 11),
        (125, "WITHOUT LIMITATION, LOSS OF PROFITS, DATA, USE, OR GOODWILL.", "helv", 11),
        (155, "8.2 The total aggregate liability of the Service Provider under this", "helv", 11),
        (175, "Agreement shall not exceed the total fees paid by the Client during", "helv", 11),
        (195, "the twelve (12) months preceding the event giving rise to liability.", "helv", 11),
        (225, "9. INDEMNIFICATION", "hebo", 14),
        (250, "9.1 The Service Provider shall indemnify and hold harmless the Client", "helv", 11),
        (270, "from any third-party claims arising from the Service Provider's", "helv", 11),
        (290, "negligence or willful misconduct in performing the services.", "helv", 11),
        (320, "9.2 The Client shall indemnify and hold harmless the Service Provider", "helv", 11),
        (340, "from any claims arising from the Client's use of deliverables in a", "helv", 11),
        (360, "manner not contemplated by this Agreement.", "helv", 11),
    ],
    # Page 8 - General Provisions and Signatures
    [
        (60, "10. GENERAL PROVISIONS", "hebo", 14),
        (85, "10.1 Governing Law: This Agreement shall be governed by the laws of", "helv", 11),
        (105, "the State of Delaware, without regard to conflict of laws principles.", "helv", 11),
        (135, "10.2 Dispute Resolution: Any disputes shall be resolved through", "helv", 11),
        (155, "binding arbitration in accordance with the rules of the American", "helv", 11),
        (175, "Arbitration Association, conducted in San Jose, California.", "helv", 11),
        (205, "10.3 Entire Agreement: This Agreement, including all appendices and", "helv", 11),
        (225, "Statements of Work, constitutes the entire agreement between the", "helv", 11),
        (245, "parties and supersedes all prior negotiations and agreements.", "helv", 11),
        (275, "10.4 Amendment: This Agreement may only be amended by a written", "helv", 11),
        (295, "instrument signed by authorized representatives of both parties.", "helv", 11),
        (340, "IN WITNESS WHEREOF, the parties have executed this Agreement as of", "helv", 11),
        (360, "the date first written above.", "helv", 11),
        (410, "____________________________          ____________________________", "helv", 11),
        (430, "Elena Vasquez, CEO                    Robert Thornton, COO", "helv", 11),
        (450, "Nextera Solutions Inc.                Pinnacle Dynamics Corp.", "helv", 11),
        (475, "Date: January 15, 2025                Date: January 15, 2025", "helv", 11),
    ],
]

# V2 modifications: pages 2, 4, 5, 7 have text changes
V2_PAGES = [p[:] for p in V1_PAGES]  # deep enough copy of lists

# Page 2 (index 1) - Scope changes
V2_PAGES[1] = [
    (60, "3. SCOPE OF SERVICES", "hebo", 14),
    (85, "3.1 The Service Provider shall provide the following services to the Client:", "helv", 11),
    (110, "  (a) Custom software development for the Client's inventory management", "helv", 11),
    (130, "      and order processing system, including design, coding, testing,", "helv", 11),
    (150, "      deployment, and post-launch support for ninety (90) days.", "helv", 11),
    (175, "  (b) Cloud infrastructure setup and management on Amazon Web Services", "helv", 11),
    (195, "      (AWS) and Microsoft Azure, including server provisioning, load", "helv", 11),
    (215, "      balancing, auto-scaling configuration, and 24/7 monitoring.", "helv", 11),
    (240, "  (c) Technical consulting for system architecture, technology stack", "helv", 11),
    (260, "      selection, and security assessment, delivered through bi-weekly", "helv", 11),
    (280, "      advisory sessions and quarterly review meetings.", "helv", 11),
    (310, "3.2 The Service Provider shall assign a dedicated project manager and a", "helv", 11),
    (330, "technical lead to oversee all deliverables and serve as primary contacts.", "helv", 11),
    (360, "3.3 All services shall be performed in accordance with industry best", "helv", 11),
    (380, "practices, ISO 27001 standards, and the quality standards set forth", "helv", 11),
    (400, "in Appendix B.", "helv", 11),
    (430, "3.4 The Service Provider shall deliver bi-weekly progress reports to the", "helv", 11),
    (450, "Client detailing work completed, milestones achieved, risks identified,", "helv", 11),
    (470, "and mitigation strategies for any issues encountered.", "helv", 11),
]

# Page 4 (index 3) - Compensation changes
V2_PAGES[3] = [
    (60, "5. COMPENSATION AND PAYMENT", "hebo", 14),
    (85, "5.1 The Client shall pay the Service Provider the following fees:", "helv", 11),
    (110, "  (a) Software Development: $195.00 per hour for senior developers,", "helv", 11),
    (130, "      $155.00 per hour for mid-level developers, and $95.00 per hour", "helv", 11),
    (150, "      for junior developers.", "helv", 11),
    (175, "  (b) Cloud Infrastructure: A fixed monthly fee of $15,000.00 for", "helv", 11),
    (195, "      standard management services across AWS and Azure platforms.", "helv", 11),
    (220, "  (c) Technical Consulting: $295.00 per hour for consulting sessions,", "helv", 11),
    (240, "      with a minimum engagement of four (4) hours per session.", "helv", 11),
    (270, "5.2 The Service Provider shall submit invoices on a bi-weekly basis,", "helv", 11),
    (290, "due within forty-five (45) days of receipt. Late payments shall accrue", "helv", 11),
    (310, "interest at a rate of 1.0% per month.", "helv", 11),
    (340, "5.3 The Client shall reimburse the Service Provider for pre-approved", "helv", 11),
    (360, "travel and out-of-pocket expenses within thirty (30) days of", "helv", 11),
    (380, "submission of expense reports with supporting documentation.", "helv", 11),
    (410, "5.4 All fees are exclusive of applicable taxes. The Client shall be", "helv", 11),
    (430, "responsible for all sales, use, and similar taxes arising from this", "helv", 11),
    (450, "Agreement, excluding taxes based on the Service Provider's income.", "helv", 11),
    (475, "5.5 An annual rate adjustment of up to 5% may be applied upon thirty", "helv", 11),
    (495, "(30) days written notice at the beginning of each contract year.", "helv", 11),
]

# Page 5 (index 4) - IP changes
V2_PAGES[4] = [
    (60, "6. INTELLECTUAL PROPERTY RIGHTS", "hebo", 14),
    (85, "6.1 All intellectual property developed by the Service Provider under", "helv", 11),
    (105, "this Agreement shall be owned by the Client upon full payment of all", "helv", 11),
    (125, "fees associated with such work. This includes source code, documentation,", "helv", 11),
    (145, "designs, and all related materials.", "helv", 11),
    (175, "6.2 The Service Provider retains ownership of all pre-existing", "helv", 11),
    (195, "intellectual property, tools, frameworks, and methodologies used in", "helv", 11),
    (215, "performing the services. The Service Provider grants the Client a", "helv", 11),
    (235, "non-exclusive, royalty-free, perpetual license to use such pre-existing", "helv", 11),
    (255, "materials as incorporated into the deliverables.", "helv", 11),
    (285, "6.3 The Client shall retain all ownership rights to its proprietary", "helv", 11),
    (305, "data, business processes, trade secrets, and confidential information", "helv", 11),
    (325, "provided to the Service Provider during the course of this Agreement.", "helv", 11),
    (355, "6.4 Neither party shall use the other party's trademarks, logos, or", "helv", 11),
    (375, "brand assets without prior written consent.", "helv", 11),
    (405, "6.5 Upon termination, the Service Provider shall transfer all work", "helv", 11),
    (425, "product, including intermediate deliverables and development artifacts,", "helv", 11),
    (445, "to the Client within ten (10) business days.", "helv", 11),
]

# Page 7 (index 6) - Liability changes
V2_PAGES[6] = [
    (60, "8. LIMITATION OF LIABILITY", "hebo", 14),
    (85, "8.1 IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY INDIRECT,", "helv", 11),
    (105, "INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING", "helv", 11),
    (125, "WITHOUT LIMITATION, LOSS OF PROFITS, DATA, USE, OR GOODWILL, EXCEPT", "helv", 11),
    (145, "IN CASES OF GROSS NEGLIGENCE OR WILLFUL MISCONDUCT.", "helv", 11),
    (175, "8.2 The total aggregate liability of the Service Provider under this", "helv", 11),
    (195, "Agreement shall not exceed two times (2x) the total fees paid by the", "helv", 11),
    (215, "Client during the twelve (12) months preceding the event giving rise", "helv", 11),
    (235, "to liability.", "helv", 11),
    (265, "9. INDEMNIFICATION", "hebo", 14),
    (290, "9.1 The Service Provider shall indemnify, defend, and hold harmless the", "helv", 11),
    (310, "Client and its affiliates from any third-party claims arising from the", "helv", 11),
    (330, "Service Provider's negligence, willful misconduct, or breach of", "helv", 11),
    (350, "confidentiality obligations in performing the services.", "helv", 11),
    (380, "9.2 The Client shall indemnify and hold harmless the Service Provider", "helv", 11),
    (400, "from any claims arising from the Client's use of deliverables in a", "helv", 11),
    (420, "manner not contemplated by this Agreement or in violation of applicable", "helv", 11),
    (440, "laws and regulations.", "helv", 11),
]


def create_pdf(pages_content, output_path):
    """Create a PDF document from page content definitions."""
    doc = pymupdf.open()
    for page_data in pages_content:
        page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
        for y, text, fontname, fontsize in page_data:
            page.insert_text(
                pymupdf.Point(60, y),
                text,
                fontname=fontname,
                fontsize=fontsize,
                color=(0, 0, 0),
            )
    doc.save(output_path)
    doc.close()
    print(f"Created: {output_path}")


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Create contract_v1.pdf
    create_pdf(V1_PAGES, V1_PATH)

    # Create contract_v2.pdf
    create_pdf(V2_PAGES, V2_PATH)

    print(f"Initial files created in {DOCS_DIR}")

    # Open both PDFs in Evince for the agent to view
    launch_gui(f'evince "{V1_PATH}"', delay_sec=2.0)
    launch_gui(f'evince "{V2_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with both contract PDFs with DISPLAY=:0')


create_initial()
