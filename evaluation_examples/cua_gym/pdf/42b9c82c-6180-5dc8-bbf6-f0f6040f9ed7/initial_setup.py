"""
Initial Setup: Create contract body and exhibits PDFs for merging task
Task ID: pdf_pw_011
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_011'
LEGAL_DIR = f'{WORKDIR}/legal'
CONTRACT_BODY = f'{LEGAL_DIR}/contract_body.pdf'
CONTRACT_EXHIBITS = f'{LEGAL_DIR}/contract_exhibits.pdf'


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


def create_contract_body():
    """Create an 8-page contract body PDF with realistic legal content."""
    doc = pymupdf.open()

    sections = [
        ("ARTICLE I: PARTIES", [
            "This Professional Services Agreement (the \"Agreement\") is entered into as of March 15, 2025,",
            "by and between:",
            "",
            "Meridian Technology Solutions, Inc., a Delaware corporation with its principal offices at",
            "4500 Innovation Drive, Suite 800, San Jose, CA 95134 (\"Service Provider\"),",
            "",
            "and",
            "",
            "Coastal Healthcare Partners, LLC, a California limited liability company with its principal",
            "offices at 2200 Pacific Coast Highway, Suite 1200, Long Beach, CA 90802 (\"Client\").",
            "",
            "WHEREAS, Client desires to engage Service Provider to perform certain technology consulting",
            "and implementation services; and",
            "",
            "WHEREAS, Service Provider has the expertise, personnel, and resources necessary to perform",
            "such services on the terms and conditions set forth herein;",
            "",
            "NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein,",
            "and for other good and valuable consideration, the receipt and sufficiency of which are",
            "hereby acknowledged, the parties agree as follows.",
        ]),
        ("ARTICLE II: TERMS AND CONDITIONS", [
            "2.1 Term. This Agreement shall commence on April 1, 2025 (the \"Effective Date\") and",
            "shall continue for a period of twenty-four (24) months unless earlier terminated in",
            "accordance with the provisions of Article V.",
            "",
            "2.2 Renewal. This Agreement may be renewed for successive twelve (12) month periods",
            "upon mutual written agreement of both parties, provided that written notice of intent",
            "to renew is delivered no later than sixty (60) days prior to the expiration of the",
            "then-current term.",
            "",
            "2.3 Scope of Services. Service Provider shall perform the services described in",
            "Exhibit A attached hereto (the \"Services\"). Any modification to the scope of Services",
            "shall require a written change order signed by authorized representatives of both parties.",
            "",
            "2.4 Personnel. Service Provider shall assign qualified personnel to perform the Services.",
            "Key personnel may not be reassigned without prior written consent of Client.",
            "",
            "2.5 Performance Standards. Service Provider shall perform all Services in a professional",
            "and workmanlike manner consistent with industry best practices and applicable regulations.",
        ]),
        ("ARTICLE III: PAYMENT", [
            "3.1 Compensation. Client shall pay Service Provider the fees set forth in Exhibit B",
            "attached hereto. The total estimated value of this Agreement shall not exceed",
            "Two Million Four Hundred Thousand Dollars ($2,400,000.00) without prior written approval.",
            "",
            "3.2 Invoicing. Service Provider shall submit itemized invoices on a monthly basis,",
            "with each invoice detailing the Services performed, hours worked by personnel category,",
            "and any pre-approved expenses incurred during the billing period.",
            "",
            "3.3 Payment Terms. Client shall pay undisputed invoices within thirty (30) days of",
            "receipt. Late payments shall accrue interest at the rate of one and one-half percent",
            "(1.5%) per month, or the maximum rate permitted by applicable law, whichever is less.",
            "",
            "3.4 Expenses. Service Provider shall be reimbursed for reasonable, pre-approved",
            "out-of-pocket expenses incurred in connection with the performance of Services.",
            "All expenses exceeding Five Hundred Dollars ($500.00) require prior written approval.",
            "",
            "3.5 Taxes. Each party shall be responsible for its own taxes arising from this Agreement.",
            "Client shall not withhold any taxes from payments due to Service Provider unless required",
            "by applicable law, in which case Client shall provide documentation of such withholding.",
        ]),
        ("ARTICLE IV: OBLIGATIONS", [
            "4.1 Confidentiality. Each party acknowledges that it may receive Confidential Information",
            "(as defined herein) from the other party. Each party agrees to: (a) maintain the",
            "confidentiality of such information using the same degree of care it uses for its own",
            "confidential information, but no less than reasonable care; (b) not disclose such",
            "information to any third party without prior written consent; and (c) use such information",
            "solely for the purposes of this Agreement.",
            "",
            "4.2 Intellectual Property. All work product, deliverables, and materials created by",
            "Service Provider specifically for Client under this Agreement (\"Work Product\") shall be",
            "the exclusive property of Client upon full payment.",
            "",
            "4.3 Data Protection. Service Provider shall comply with all applicable data protection",
            "laws and regulations, including but not limited to HIPAA, CCPA, and any other relevant",
            "healthcare data privacy requirements.",
            "",
            "4.4 Insurance. Service Provider shall maintain the following insurance coverage throughout",
            "the term of this Agreement: (a) Commercial General Liability: $2,000,000 per occurrence;",
            "(b) Professional Liability: $5,000,000 per occurrence; (c) Cyber Liability: $3,000,000.",
        ]),
        ("ARTICLE V: TERMINATION", [
            "5.1 Termination for Convenience. Either party may terminate this Agreement for any reason",
            "upon ninety (90) days prior written notice to the other party.",
            "",
            "5.2 Termination for Cause. Either party may terminate this Agreement immediately upon",
            "written notice if the other party: (a) materially breaches this Agreement and fails to",
            "cure such breach within thirty (30) days after receiving written notice thereof;",
            "(b) becomes insolvent, files for bankruptcy, or makes an assignment for the benefit of",
            "creditors; or (c) engages in fraud or willful misconduct.",
            "",
            "5.3 Effect of Termination. Upon termination: (a) Service Provider shall cease performing",
            "Services and deliver all completed and in-progress Work Product to Client; (b) Client",
            "shall pay Service Provider for all Services performed and expenses incurred through the",
            "effective date of termination; (c) all licenses granted hereunder shall terminate.",
            "",
            "5.4 Survival. The provisions of Articles IV, VI, and VII shall survive termination of",
            "this Agreement for a period of three (3) years.",
        ]),
        ("ARTICLE VI: DISPUTE RESOLUTION", [
            "6.1 Negotiation. The parties shall attempt in good faith to resolve any dispute arising",
            "out of or relating to this Agreement through direct negotiation between senior executives",
            "of both parties. Such negotiations shall commence within ten (10) business days of",
            "written notice of the dispute.",
            "",
            "6.2 Mediation. If the dispute is not resolved through negotiation within thirty (30) days,",
            "the parties agree to submit the dispute to mediation under the rules of the American",
            "Arbitration Association before a mutually agreed-upon mediator.",
            "",
            "6.3 Arbitration. If mediation fails to resolve the dispute within sixty (60) days,",
            "the dispute shall be submitted to binding arbitration in San Francisco, California,",
            "under the Commercial Arbitration Rules of the American Arbitration Association.",
            "",
            "6.4 Governing Law. This Agreement shall be governed by and construed in accordance",
            "with the laws of the State of California, without regard to its conflict of laws provisions.",
            "",
            "6.5 Venue. Any legal proceedings arising from this Agreement shall be conducted in the",
            "state or federal courts located in San Francisco County, California.",
        ]),
        ("ARTICLE VII: AMENDMENTS", [
            "7.1 Modifications. No amendment or modification of this Agreement shall be valid or",
            "binding upon the parties unless made in writing and signed by authorized representatives",
            "of both parties.",
            "",
            "7.2 Waiver. The failure of either party to enforce any provision of this Agreement shall",
            "not constitute a waiver of such party's right to enforce such provision or any other",
            "provision in the future.",
            "",
            "7.3 Severability. If any provision of this Agreement is held to be invalid, illegal, or",
            "unenforceable, the remaining provisions shall continue in full force and effect.",
            "",
            "7.4 Entire Agreement. This Agreement, including all Exhibits attached hereto, constitutes",
            "the entire agreement between the parties with respect to the subject matter hereof and",
            "supersedes all prior negotiations, representations, warranties, commitments, offers,",
            "contracts and writings, whether oral or written.",
            "",
            "7.5 Counterparts. This Agreement may be executed in counterparts, each of which shall",
            "be deemed an original, and all of which together shall constitute one and the same",
            "instrument. Electronic signatures shall be deemed original signatures for all purposes.",
        ]),
        ("ARTICLE VIII: SIGNATURES", [
            "IN WITNESS WHEREOF, the parties hereto have caused this Agreement to be executed by",
            "their duly authorized representatives as of the date first written above.",
            "",
            "",
            "MERIDIAN TECHNOLOGY SOLUTIONS, INC.",
            "",
            "By: _________________________________",
            "Name: Dr. Elena Rodriguez",
            "Title: Chief Executive Officer",
            "Date: _______________________________",
            "",
            "",
            "COASTAL HEALTHCARE PARTNERS, LLC",
            "",
            "By: _________________________________",
            "Name: Robert Chen, M.D.",
            "Title: Managing Partner",
            "Date: _______________________________",
        ]),
    ]

    for section_title, paragraphs in sections:
        page = doc.new_page(width=612, height=792)  # Letter size

        # Section title
        page.insert_text(
            pymupdf.Point(72, 72),
            section_title,
            fontsize=16,
            fontname="hebo",
            color=(0, 0, 0.4),
        )

        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
        shape.finish(color=(0, 0, 0.4), width=1.5)
        shape.commit()

        # Body text
        y = 110
        for line in paragraphs:
            if line == "":
                y += 14
                continue
            page.insert_text(
                pymupdf.Point(72, y),
                line,
                fontsize=11,
                fontname="tiro",
                color=(0, 0, 0),
            )
            y += 16

    doc.save(CONTRACT_BODY)
    doc.close()
    print(f"Created: {CONTRACT_BODY} (8 pages)")


def create_contract_exhibits():
    """Create a 5-page exhibits PDF (Exhibit A through E)."""
    doc = pymupdf.open()

    exhibits = [
        ("EXHIBIT A: SCOPE OF SERVICES", [
            "1. Electronic Health Records (EHR) System Migration",
            "   - Migrate existing patient records from Legacy EMR v4.2 to CloudHealth Platform",
            "   - Data validation and integrity verification for 450,000+ patient records",
            "   - Custom interface development for radiology and laboratory systems",
            "   - Staff training for 1,200 clinical and administrative users",
            "",
            "2. Cybersecurity Infrastructure Upgrade",
            "   - Network security assessment and penetration testing",
            "   - Implementation of zero-trust architecture across 14 facility locations",
            "   - Deployment of endpoint detection and response (EDR) solution",
            "   - HIPAA compliance audit and remediation",
            "",
            "3. Telemedicine Platform Development",
            "   - Design and deployment of patient-facing telehealth application",
            "   - Integration with existing scheduling and billing systems",
            "   - HIPAA-compliant video conferencing infrastructure",
            "   - Mobile application for iOS and Android platforms",
        ]),
        ("EXHIBIT B: FEE SCHEDULE", [
            "Personnel Rates:",
            "",
            "  Senior Consultant              $275/hour",
            "  Project Manager                 $225/hour",
            "  Technical Architect             $300/hour",
            "  Software Developer              $200/hour",
            "  Data Analyst                    $175/hour",
            "  Quality Assurance Engineer      $185/hour",
            "  Training Specialist             $150/hour",
            "",
            "Fixed Fee Components:",
            "",
            "  EHR Migration (Phase 1)        $850,000",
            "  Cybersecurity Upgrade           $425,000",
            "  Telemedicine Platform           $675,000",
            "  Integration Testing             $210,000",
            "  Training & Documentation        $140,000",
            "",
            "Total Estimated Not-to-Exceed:   $2,400,000",
        ]),
        ("EXHIBIT C: PROJECT TIMELINE", [
            "Phase 1: Discovery & Planning (Months 1-3)",
            "  - Requirements gathering and stakeholder interviews",
            "  - Current state assessment and gap analysis",
            "  - Detailed project plan and resource allocation",
            "  - Risk assessment and mitigation strategy",
            "",
            "Phase 2: Design & Development (Months 4-9)",
            "  - System architecture design and approval",
            "  - EHR data migration planning and pilot testing",
            "  - Cybersecurity framework implementation",
            "  - Telemedicine platform prototype development",
            "",
            "Phase 3: Implementation (Months 10-18)",
            "  - Staged EHR migration across facility groups",
            "  - Security infrastructure deployment",
            "  - Telemedicine platform launch (beta then full)",
            "",
            "Phase 4: Optimization & Handoff (Months 19-24)",
            "  - Performance tuning and optimization",
            "  - Knowledge transfer and documentation",
            "  - Transition to Client internal IT support",
        ]),
        ("EXHIBIT D: SERVICE LEVEL AGREEMENTS", [
            "1. System Availability",
            "   - Production systems: 99.9% uptime (excluding scheduled maintenance)",
            "   - Scheduled maintenance windows: Sundays 2:00 AM - 6:00 AM PST",
            "   - Maximum unplanned downtime: 4 hours per calendar month",
            "",
            "2. Incident Response Times",
            "   - Severity 1 (System Down): Response within 15 minutes, resolution within 4 hours",
            "   - Severity 2 (Major Impact): Response within 1 hour, resolution within 8 hours",
            "   - Severity 3 (Minor Impact): Response within 4 hours, resolution within 2 business days",
            "   - Severity 4 (Low Impact): Response within 1 business day, resolution within 5 days",
            "",
            "3. Performance Metrics",
            "   - Page load time: < 3 seconds (95th percentile)",
            "   - API response time: < 500ms (99th percentile)",
            "   - Data migration accuracy: > 99.99%",
            "",
            "4. Penalties",
            "   - SLA breach credits: 5% of monthly fee per missed target, capped at 20%",
        ]),
        ("EXHIBIT E: DATA SECURITY REQUIREMENTS", [
            "1. Encryption Standards",
            "   - Data at rest: AES-256 encryption for all patient data",
            "   - Data in transit: TLS 1.3 minimum for all communications",
            "   - Key management: HSM-backed key storage with annual rotation",
            "",
            "2. Access Controls",
            "   - Role-based access control (RBAC) for all systems",
            "   - Multi-factor authentication (MFA) required for all users",
            "   - Privileged access management (PAM) for administrative accounts",
            "   - Quarterly access reviews and recertification",
            "",
            "3. Audit and Monitoring",
            "   - Comprehensive audit logging for all data access events",
            "   - Real-time security event monitoring (SIEM)",
            "   - Annual third-party security audit (SOC 2 Type II)",
            "   - Monthly vulnerability scanning and quarterly penetration testing",
            "",
            "4. Data Retention and Disposal",
            "   - Patient records: Retain per applicable state law (minimum 7 years)",
            "   - System logs: Retain for 3 years",
            "   - Secure disposal: NIST SP 800-88 compliant media sanitization",
        ]),
    ]

    for exhibit_title, content_lines in exhibits:
        page = doc.new_page(width=612, height=792)

        # Exhibit title
        page.insert_text(
            pymupdf.Point(72, 72),
            exhibit_title,
            fontsize=14,
            fontname="hebo",
            color=(0.4, 0, 0),
        )

        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
        shape.finish(color=(0.4, 0, 0), width=1.0)
        shape.commit()

        # Content
        y = 110
        for line in content_lines:
            if line == "":
                y += 12
                continue
            page.insert_text(
                pymupdf.Point(72, y),
                line,
                fontsize=10,
                fontname="tiro",
                color=(0, 0, 0),
            )
            y += 14

    doc.save(CONTRACT_EXHIBITS)
    doc.close()
    print(f"Created: {CONTRACT_EXHIBITS} (5 pages)")


def create_initial():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    # Remove any pre-existing merged file (should not exist)
    merged = f'{LEGAL_DIR}/complete_contract.pdf'
    if os.path.exists(merged):
        os.remove(merged)

    create_contract_body()
    create_contract_exhibits()

    # Open contract_body.pdf in Evince for the agent
    launch_gui(f'evince "{CONTRACT_BODY}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with contract_body.pdf on DISPLAY=:0')


create_initial()
