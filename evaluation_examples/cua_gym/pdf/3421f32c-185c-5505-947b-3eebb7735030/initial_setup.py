"""
Initial Setup: Create a 10-page contract draft PDF for signature page insertion task.
Task ID: pdf_gf2_020
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_020'
OUTPUT_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{OUTPUT_DIR}/contract_draft.pdf'


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
    import pymupdf

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()  # new empty PDF

    # Page dimensions (Letter size)
    W, H = 612, 792

    # Content margins
    LEFT = 72
    RIGHT = W - 72
    TOP = 72
    CONTENT_WIDTH = RIGHT - LEFT

    # --- Pages 1-5: Contract Clause Sections ---

    clauses = [
        {
            "title": "PROFESSIONAL SERVICES AGREEMENT",
            "subtitle": "Between Meridian Technologies Inc. and Cascade Solutions LLC",
            "body": (
                "This Professional Services Agreement ('Agreement') is entered into as of March 15, 2025, "
                "by and between Meridian Technologies Inc., a Delaware corporation with principal offices at "
                "4200 Innovation Drive, Suite 800, San Jose, CA 95134 ('Client'), and Cascade Solutions LLC, "
                "an Oregon limited liability company with principal offices at 1750 Pearl Street, Suite 300, "
                "Portland, OR 97209 ('Provider').\n\n"
                "WHEREAS, Client desires to engage Provider to perform certain professional consulting and "
                "software development services; and\n\n"
                "WHEREAS, Provider has the expertise and resources to perform such services;\n\n"
                "NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth herein, "
                "and for other good and valuable consideration, the receipt and sufficiency of which are hereby "
                "acknowledged, the parties agree as follows."
            ),
        },
        {
            "title": "ARTICLE I - SCOPE OF SERVICES",
            "subtitle": "",
            "body": (
                "1.1 Services. Provider shall perform the professional services described in one or more "
                "Statements of Work ('SOW') attached hereto or subsequently executed by the parties. Each "
                "SOW shall specify the scope, deliverables, timeline, and fees for the applicable engagement.\n\n"
                "1.2 Standard of Care. Provider shall perform all Services in a professional and workmanlike "
                "manner consistent with generally accepted industry standards and practices. Provider shall "
                "assign qualified personnel with appropriate skills and experience.\n\n"
                "1.3 Change Orders. Any changes to the scope of Services shall be documented in a written "
                "Change Order signed by authorized representatives of both parties. No verbal modifications "
                "shall be binding unless subsequently confirmed in writing.\n\n"
                "1.4 Subcontracting. Provider may engage subcontractors to perform portions of the Services, "
                "provided that Provider remains responsible for the performance and quality of all work and "
                "obtains Client's prior written consent for any subcontractor engagement.\n\n"
                "1.5 Client Responsibilities. Client shall provide reasonable access to its facilities, systems, "
                "personnel, and information as necessary for Provider to perform the Services. Client shall "
                "designate a project manager to serve as the primary point of contact."
            ),
        },
        {
            "title": "ARTICLE II - COMPENSATION AND PAYMENT",
            "subtitle": "",
            "body": (
                "2.1 Fees. Client shall pay Provider the fees set forth in each applicable SOW. Unless "
                "otherwise specified, fees shall be calculated on a time-and-materials basis at the hourly "
                "rates specified in Exhibit A.\n\n"
                "2.2 Invoicing. Provider shall submit itemized invoices on a monthly basis, detailing hours "
                "worked, tasks performed, and expenses incurred. Invoices shall be submitted to the Client's "
                "accounts payable department at invoices@meridiantech.com.\n\n"
                "2.3 Payment Terms. Client shall pay all undisputed amounts within thirty (30) calendar days "
                "of receipt of a valid invoice. Late payments shall accrue interest at a rate of 1.5% per month "
                "or the maximum rate permitted by applicable law, whichever is less.\n\n"
                "2.4 Expenses. Reasonable travel and out-of-pocket expenses incurred by Provider in connection "
                "with the Services shall be reimbursed by Client, provided such expenses are pre-approved in "
                "writing and supported by receipts. Travel expenses shall not exceed $5,000 per calendar quarter "
                "without additional written approval.\n\n"
                "2.5 Taxes. Each party shall be responsible for its own taxes arising from this Agreement. "
                "Provider is an independent contractor and is responsible for all federal, state, and local taxes "
                "on compensation received under this Agreement."
            ),
        },
        {
            "title": "ARTICLE III - INTELLECTUAL PROPERTY",
            "subtitle": "",
            "body": (
                "3.1 Work Product. All deliverables, inventions, discoveries, and works of authorship created "
                "by Provider in the course of performing Services ('Work Product') shall be the sole and "
                "exclusive property of Client. Provider hereby assigns to Client all right, title, and interest "
                "in and to such Work Product.\n\n"
                "3.2 Pre-Existing Materials. Provider retains all right, title, and interest in any tools, "
                "frameworks, libraries, or methodologies that were developed by Provider prior to or "
                "independently of the Services ('Pre-Existing Materials'). To the extent any Pre-Existing "
                "Materials are incorporated into the Work Product, Provider grants Client a perpetual, "
                "non-exclusive, royalty-free license to use such materials.\n\n"
                "3.3 Confidentiality of Work Product. Provider shall treat all Work Product as Confidential "
                "Information of Client and shall not disclose, publish, or use any Work Product except as "
                "authorized by Client in writing.\n\n"
                "3.4 Moral Rights. To the extent permitted by applicable law, Provider waives any moral rights "
                "in the Work Product and shall ensure that all Provider personnel do the same."
            ),
        },
        {
            "title": "ARTICLE IV - CONFIDENTIALITY AND DATA PROTECTION",
            "subtitle": "",
            "body": (
                "4.1 Definition. 'Confidential Information' means any non-public information disclosed by "
                "either party to the other in connection with this Agreement, including but not limited to "
                "trade secrets, business plans, financial data, customer lists, technical specifications, "
                "source code, and personnel information.\n\n"
                "4.2 Obligations. The receiving party shall: (a) use Confidential Information solely for the "
                "purposes of this Agreement; (b) protect Confidential Information with at least the same "
                "degree of care as it protects its own confidential information, but in no event less than "
                "reasonable care; (c) limit disclosure to employees and subcontractors who have a need to "
                "know and are bound by confidentiality obligations no less restrictive than those herein.\n\n"
                "4.3 Exclusions. Confidential Information does not include information that: (a) is or becomes "
                "publicly available through no fault of the receiving party; (b) was rightfully in the receiving "
                "party's possession before disclosure; (c) is independently developed without use of the "
                "disclosing party's Confidential Information; or (d) is rightfully obtained from a third party "
                "without restriction.\n\n"
                "4.4 Duration. The obligations of confidentiality shall survive the termination of this "
                "Agreement for a period of five (5) years."
            ),
        },
    ]

    # --- Pages 6-10: Exhibits ---

    exhibits = [
        {
            "title": "EXHIBIT A - RATE SCHEDULE",
            "subtitle": "Effective Date: March 15, 2025",
            "body": (
                "The following hourly rates shall apply to Services performed under this Agreement:\n\n"
                "Senior Software Architect ............ $285/hour\n"
                "Lead Developer ........................ $245/hour\n"
                "Software Developer .................... $195/hour\n"
                "QA Engineer ........................... $175/hour\n"
                "Project Manager ....................... $210/hour\n"
                "Technical Writer ...................... $145/hour\n"
                "UI/UX Designer ........................ $205/hour\n"
                "DevOps Engineer ....................... $225/hour\n\n"
                "Rates are subject to annual adjustment not to exceed 5% per year. Any rate changes require "
                "sixty (60) days' prior written notice. Weekend and holiday work shall be billed at 1.5x the "
                "applicable hourly rate."
            ),
        },
        {
            "title": "EXHIBIT B - STATEMENT OF WORK #001",
            "subtitle": "Cloud Migration and Modernization",
            "body": (
                "Project Overview: Migration of Client's legacy on-premises ERP system to a cloud-native "
                "architecture on AWS, including containerization, database migration, and API modernization.\n\n"
                "Phase 1 - Assessment & Planning (Weeks 1-4)\n"
                "  - Infrastructure audit and dependency mapping\n"
                "  - Cloud architecture design and cost modeling\n"
                "  - Risk assessment and mitigation planning\n"
                "  - Deliverable: Migration Strategy Document\n\n"
                "Phase 2 - Core Migration (Weeks 5-16)\n"
                "  - Database migration to Amazon RDS/Aurora\n"
                "  - Application containerization with Docker/ECS\n"
                "  - API gateway implementation\n"
                "  - Deliverable: Migrated core services\n\n"
                "Phase 3 - Testing & Optimization (Weeks 17-22)\n"
                "  - Performance testing and optimization\n"
                "  - Security audit and penetration testing\n"
                "  - User acceptance testing\n"
                "  - Deliverable: Test reports and sign-off\n\n"
                "Estimated Total: 2,400 hours | Budget: $528,000"
            ),
        },
        {
            "title": "EXHIBIT C - SERVICE LEVEL AGREEMENT",
            "subtitle": "",
            "body": (
                "1. Availability. Provider shall maintain a minimum uptime of 99.5% for all production "
                "services during each calendar month, measured using industry-standard monitoring tools.\n\n"
                "2. Response Times. Provider shall respond to incidents as follows:\n"
                "   Severity 1 (Critical): Response within 30 minutes, resolution within 4 hours\n"
                "   Severity 2 (High): Response within 2 hours, resolution within 8 hours\n"
                "   Severity 3 (Medium): Response within 4 hours, resolution within 24 hours\n"
                "   Severity 4 (Low): Response within 1 business day, resolution within 5 business days\n\n"
                "3. Penalties. If Provider fails to meet the availability target in any calendar month, "
                "Client shall receive a service credit equal to 5% of that month's fees for each 0.1% "
                "below the target, up to a maximum credit of 25% of the monthly fees.\n\n"
                "4. Reporting. Provider shall deliver monthly service reports detailing uptime metrics, "
                "incident logs, and resolution statistics."
            ),
        },
        {
            "title": "EXHIBIT D - INSURANCE REQUIREMENTS",
            "subtitle": "",
            "body": (
                "Provider shall maintain the following insurance coverage throughout the term of this "
                "Agreement and for a period of two (2) years following termination:\n\n"
                "1. Commercial General Liability: $2,000,000 per occurrence / $5,000,000 aggregate\n"
                "2. Professional Liability (E&O): $3,000,000 per claim / $5,000,000 aggregate\n"
                "3. Cyber Liability: $5,000,000 per claim / $10,000,000 aggregate\n"
                "4. Workers' Compensation: As required by applicable law\n"
                "5. Commercial Auto Liability: $1,000,000 combined single limit\n\n"
                "Provider shall name Client as an additional insured on all policies except Workers' "
                "Compensation and Professional Liability. Provider shall provide certificates of insurance "
                "within ten (10) business days of execution of this Agreement and upon each annual renewal.\n\n"
                "Provider shall provide Client with thirty (30) days' prior written notice of any material "
                "change in, cancellation, or non-renewal of any required insurance coverage."
            ),
        },
        {
            "title": "EXHIBIT E - ACCEPTABLE USE AND SECURITY POLICY",
            "subtitle": "",
            "body": (
                "1. Access Controls. Provider personnel shall access Client systems only through approved "
                "VPN connections using multi-factor authentication. All access credentials shall be unique "
                "to each individual and shall not be shared.\n\n"
                "2. Data Handling. Provider shall encrypt all Client data in transit (TLS 1.2 or higher) "
                "and at rest (AES-256 or equivalent). Provider shall not store Client data on personal "
                "devices or unauthorized cloud storage services.\n\n"
                "3. Background Checks. Provider shall ensure that all personnel with access to Client "
                "systems or data have undergone background checks consistent with industry standards.\n\n"
                "4. Incident Reporting. Provider shall report any actual or suspected security incident "
                "to Client's security team within four (4) hours of discovery. Provider shall cooperate "
                "fully with Client's incident response procedures.\n\n"
                "5. Audit Rights. Client reserves the right to audit Provider's security practices and "
                "controls upon reasonable notice. Provider shall cooperate with such audits and promptly "
                "remediate any identified deficiencies."
            ),
        },
    ]

    # Create all 10 pages
    all_sections = clauses + exhibits
    for i, section in enumerate(all_sections):
        page = doc.new_page(width=W, height=H)

        y = TOP

        # Page number at bottom
        page.insert_text(
            pymupdf.Point(W / 2 - 10, H - 36),
            f"Page {i + 1} of 10",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Title
        page.insert_text(
            pymupdf.Point(LEFT, y + 14),
            section["title"],
            fontsize=14,
            fontname="hebo",
            color=(0, 0, 0),
        )
        y += 30

        # Subtitle if present
        if section["subtitle"]:
            page.insert_text(
                pymupdf.Point(LEFT, y + 12),
                section["subtitle"],
                fontsize=11,
                fontname="tiit",
                color=(0.3, 0.3, 0.3),
            )
            y += 25

        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(LEFT, y), pymupdf.Point(RIGHT, y))
        shape.finish(color=(0, 0, 0), width=0.5)
        shape.commit()
        y += 15

        # Body text
        text_rect = pymupdf.Rect(LEFT, y, RIGHT, H - 60)
        page.insert_textbox(
            text_rect,
            section["body"],
            fontsize=10.5,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Pages: 10')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
