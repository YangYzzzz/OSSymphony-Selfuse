"""
Initial Setup: Create contract_v1.pdf and contract_v2.pdf for diff comparison task
Task ID: pdf_pw_015
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_015'
LEGAL_DIR = f'{WORKDIR}/legal'
V1_PATH = f'{LEGAL_DIR}/contract_v1.pdf'
V2_PATH = f'{LEGAL_DIR}/contract_v2.pdf'

# ── Contract content for 10 pages ──
# Each page is a list of (fontname, fontsize, text) items
# V2 changes are on pages 2, 4, 5, 7, 9 (0-indexed: 1, 3, 4, 6, 8)

PAGE_TITLE_FONT = "hebo"
PAGE_TITLE_SIZE = 16
BODY_FONT = "helv"
BODY_SIZE = 11
SECTION_FONT = "hebo"
SECTION_SIZE = 13

# Define contract pages (shared between v1 and v2, with diffs noted)
CONTRACT_PAGES_V1 = [
    # Page 1 - Title / Preamble
    {
        "title": "SERVICES AGREEMENT",
        "subtitle": "Contract No. SA-2025-04871",
        "sections": [
            ("1. PARTIES", [
                'This Services Agreement ("Agreement") is entered into as of March 15, 2025,',
                'by and between Meridian Technologies Inc., a Delaware corporation with principal',
                'offices at 4200 Innovation Drive, Suite 800, San Jose, CA 95134 ("Provider"),',
                'and Cascade Financial Group LLC, a New York limited liability company with',
                'principal offices at 1 Liberty Plaza, 38th Floor, New York, NY 10006 ("Client").',
            ]),
            ("2. RECITALS", [
                'WHEREAS, Provider specializes in enterprise software development, cloud',
                'infrastructure management, and data analytics services; and',
                'WHEREAS, Client desires to engage Provider to deliver certain technology',
                'services as described herein; and',
                'WHEREAS, both parties wish to set forth the terms and conditions governing',
                'such engagement;',
                'NOW, THEREFORE, in consideration of the mutual covenants and agreements',
                'contained herein, the parties agree as follows:',
            ]),
        ]
    },
    # Page 2 - Scope of Services (DIFF PAGE - 2 changes)
    {
        "title": "",
        "subtitle": "",
        "sections": [
            ("3. SCOPE OF SERVICES", [
                '3.1 Provider shall deliver the following services to Client:',
                '    (a) Custom software development for Client\'s trading platform,',
                '        including front-end interfaces and back-end processing systems;',
                '    (b) Cloud infrastructure setup and management on Amazon Web Services,',  # V2: "Microsoft Azure"
                '        including server provisioning, load balancing, and auto-scaling;',
                '    (c) Data analytics and reporting dashboard development using',
                '        real-time market data feeds;',
                '    (d) Integration with Client\'s existing portfolio management systems',
                '        including Bloomberg Terminal and Reuters Eikon connections.',
                '',
                '3.2 All services shall be performed in accordance with industry best',
                'practices and applicable professional standards. Provider shall assign',
                'a dedicated project manager and a team of no fewer than eight (8)',  # V2: "twelve (12)"
                'qualified engineers to the engagement.',
            ]),
            ("4. PROJECT TIMELINE", [
                '4.1 The project shall commence on April 1, 2025 and is expected to',
                'be completed by December 31, 2025 ("Project Term").',
                '',
                '4.2 Key milestones:',
                '    Phase 1 - Requirements & Design: April 1 - May 15, 2025',
                '    Phase 2 - Core Development: May 16 - August 31, 2025',
                '    Phase 3 - Integration & Testing: September 1 - November 15, 2025',
                '    Phase 4 - Deployment & Handoff: November 16 - December 31, 2025',
            ]),
        ]
    },
    # Page 3 - Compensation
    {
        "title": "",
        "subtitle": "",
        "sections": [
            ("5. COMPENSATION", [
                '5.1 Client shall pay Provider a total fixed fee of Two Million Four',
                'Hundred Thousand Dollars ($2,400,000) for the services described in',
                'Section 3, payable in monthly installments of $266,666.67.',
                '',
                '5.2 Payment terms: Net 30 days from receipt of invoice. Provider',
                'shall submit invoices on the first business day of each month.',
                '',
                '5.3 Late payments shall accrue interest at a rate of 1.5% per month',
                'or the maximum rate permitted by law, whichever is less.',
                '',
                '5.4 Provider shall be reimbursed for pre-approved travel expenses,',
                'software licenses, and third-party service costs, not to exceed',
                '$150,000 in aggregate over the Project Term.',
            ]),
            ("6. INTELLECTUAL PROPERTY", [
                '6.1 All work product, deliverables, source code, documentation, and',
                'related materials created by Provider specifically for Client under',
                'this Agreement ("Work Product") shall be the exclusive property of Client.',
                '',
                '6.2 Provider retains ownership of all pre-existing tools, frameworks,',
                'libraries, and methodologies ("Provider Tools") used in delivering the',
                'services. Provider grants Client a perpetual, non-exclusive license to',
                'use Provider Tools as embedded in the Work Product.',
            ]),
        ]
    },
    # Page 4 - Confidentiality (DIFF PAGE - 2 changes)
    {
        "title": "",
        "subtitle": "",
        "sections": [
            ("7. CONFIDENTIALITY", [
                '7.1 Each party acknowledges that it may receive confidential and',
                'proprietary information of the other party ("Confidential Information").',
                'Confidential Information includes, but is not limited to: trade secrets,',
                'business plans, financial data, customer lists, technical specifications,',
                'source code, algorithms, and marketing strategies.',
                '',
                '7.2 The receiving party shall:',
                '    (a) Hold all Confidential Information in strict confidence;',
                '    (b) Not disclose Confidential Information to any third party without',
                '        prior written consent of the disclosing party;',
                '    (c) Use Confidential Information solely for purposes of this Agreement;',
                '    (d) Protect Confidential Information using the same degree of care it',
                '        uses for its own confidential information, but no less than',
                '        reasonable care.',
                '',
                '7.3 Confidentiality obligations shall survive for a period of three (3)',  # V2: "five (5)"
                'years following termination or expiration of this Agreement.',
            ]),
            ("8. DATA SECURITY", [
                '8.1 Provider shall implement and maintain administrative, physical, and',
                'technical safeguards to protect Client data, including:',
                '    (a) AES-256 encryption for data at rest and TLS 1.2 for data in transit;',  # V2: "TLS 1.3"
                '    (b) Multi-factor authentication for all system access;',
                '    (c) Regular security audits and penetration testing;',
                '    (d) SOC 2 Type II compliance certification.',
            ]),
        ]
    },
    # Page 5 - Warranties (DIFF PAGE - 2 changes)
    {
        "title": "",
        "subtitle": "",
        "sections": [
            ("9. REPRESENTATIONS AND WARRANTIES", [
                '9.1 Provider represents and warrants that:',
                '    (a) It has the legal right and authority to enter into this Agreement;',
                '    (b) The services will be performed in a professional and workmanlike manner;',
                '    (c) The Work Product will not infringe upon any intellectual property',
                '        rights of any third party;',
                '    (d) It maintains adequate insurance coverage, including professional',
                '        liability insurance of not less than $5,000,000 per occurrence.',  # V2: "$10,000,000"
                '',
                '9.2 Client represents and warrants that:',
                '    (a) It has the legal right and authority to enter into this Agreement;',
                '    (b) It will provide timely access to systems, data, and personnel',
                '        as reasonably requested by Provider;',
                '    (c) It will designate a project liaison to coordinate with Provider.',
            ]),
            ("10. LIMITATION OF LIABILITY", [
                '10.1 IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY INDIRECT,',
                'INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING OUT OF',
                'OR RELATED TO THIS AGREEMENT.',
                '',
                "10.2 Provider's total aggregate liability under this Agreement shall",
                'not exceed the total fees paid by Client under this Agreement during',
                'the twelve (12) month period preceding the event giving rise to the claim.',  # V2: "twenty-four (24) month"
                '',
                '10.3 The foregoing limitations shall not apply to:',
                '    (a) Breaches of confidentiality obligations;',
                '    (b) Infringement of intellectual property rights;',
                '    (c) Willful misconduct or gross negligence.',
            ]),
        ]
    },
    # Page 6 - Termination
    {
        "title": "",
        "subtitle": "",
        "sections": [
            ("11. TERM AND TERMINATION", [
                '11.1 This Agreement shall be effective as of the date first written',
                'above and shall continue until completion of the services or December',
                '31, 2025, whichever occurs first, unless terminated earlier in',
                'accordance with this Section.',
                '',
                '11.2 Either party may terminate this Agreement:',
                '    (a) For cause, upon thirty (30) days written notice if the other',
                '        party materially breaches this Agreement and fails to cure such',
                '        breach within the notice period;',
                '    (b) For convenience, upon sixty (60) days prior written notice;',
                '    (c) Immediately, if the other party becomes insolvent, files for',
                '        bankruptcy, or makes an assignment for the benefit of creditors.',
                '',
                '11.3 Upon termination:',
                '    (a) Client shall pay for all services performed through the date',
                '        of termination;',
                '    (b) Provider shall deliver all completed and in-progress Work Product;',
                '    (c) Each party shall return or destroy Confidential Information;',
                '    (d) Sections 6, 7, 8, 10, and 14 shall survive termination.',
            ]),
        ]
    },
    # Page 7 - Indemnification (DIFF PAGE - 1 change)
    {
        "title": "",
        "subtitle": "",
        "sections": [
            ("12. INDEMNIFICATION", [
                '12.1 Provider shall indemnify, defend, and hold harmless Client and',
                'its officers, directors, employees, and agents from and against any',
                'and all claims, damages, losses, costs, and expenses (including',
                'reasonable attorneys\' fees) arising out of or relating to:',
                '    (a) Any breach of Provider\'s representations, warranties, or',
                '        obligations under this Agreement;',
                '    (b) Any claim that the Work Product infringes upon any third-party',
                '        intellectual property rights;',
                '    (c) Provider\'s negligence or willful misconduct in performing the services.',
                '',
                '12.2 Client shall indemnify, defend, and hold harmless Provider from',
                'claims arising out of:',
                '    (a) Client\'s use of the Work Product in a manner not contemplated',
                '        by this Agreement;',
                '    (b) Client\'s breach of its obligations under this Agreement;',
                '    (c) Any third-party claims related to Client\'s business operations.',
                '',
                '12.3 The indemnified party shall provide prompt written notice of any',
                'claim within fifteen (15) business days of becoming aware of such claim.',  # V2: "ten (10) business days"
            ]),
        ]
    },
    # Page 8 - Dispute Resolution
    {
        "title": "",
        "subtitle": "",
        "sections": [
            ("13. DISPUTE RESOLUTION", [
                '13.1 The parties shall attempt to resolve any dispute arising out of',
                'or relating to this Agreement through good faith negotiation.',
                '',
                '13.2 If negotiation fails to resolve the dispute within thirty (30)',
                'days, the parties agree to submit the dispute to binding arbitration',
                'administered by the American Arbitration Association ("AAA") under its',
                'Commercial Arbitration Rules.',
                '',
                '13.3 Arbitration shall be conducted:',
                '    (a) In New York, New York;',
                '    (b) Before a panel of three (3) arbitrators;',
                '    (c) In the English language;',
                '    (d) In accordance with the Federal Arbitration Act.',
                '',
                '13.4 The arbitrators shall have the authority to award any remedy',
                'available under applicable law, including injunctive relief and',
                'specific performance. The arbitrators\' decision shall be final and',
                'binding upon both parties.',
                '',
                '13.5 Each party shall bear its own costs of arbitration; the fees of',
                'the arbitrators and AAA shall be shared equally.',
            ]),
        ]
    },
    # Page 9 - General Provisions (DIFF PAGE - 1 change)
    {
        "title": "",
        "subtitle": "",
        "sections": [
            ("14. GENERAL PROVISIONS", [
                '14.1 Governing Law. This Agreement shall be governed by and construed',
                'in accordance with the laws of the State of New York, without regard',
                'to its conflict of laws provisions.',
                '',
                '14.2 Entire Agreement. This Agreement, including all exhibits and',
                'schedules attached hereto, constitutes the entire agreement between',
                'the parties and supersedes all prior negotiations, representations,',
                'and agreements relating to the subject matter hereof.',
                '',
                '14.3 Amendments. This Agreement may not be amended or modified except',
                'by a written instrument signed by both parties.',
                '',
                '14.4 Assignment. Neither party may assign this Agreement without the',
                'prior written consent of the other party, except that either party',
                'may assign this Agreement to a successor in connection with a merger,',
                'acquisition, or sale of all or substantially all of its assets.',
                '',
                '14.5 Force Majeure. Neither party shall be liable for failure or delay',
                'in performance due to causes beyond its reasonable control, including',
                'but not limited to: natural disasters, war, terrorism, pandemic,',
                'government actions, or failure of third-party telecommunications.',  # V2: "third-party telecommunications or power infrastructure."
                '',
                '14.6 Notices. All notices under this Agreement shall be in writing and',
                'delivered by certified mail, overnight courier, or email to the',
                'addresses set forth above.',
            ]),
        ]
    },
    # Page 10 - Signatures
    {
        "title": "",
        "subtitle": "",
        "sections": [
            ("15. EXECUTION", [
                'IN WITNESS WHEREOF, the parties hereto have executed this Agreement',
                'as of the date first written above.',
                '',
                '',
                'MERIDIAN TECHNOLOGIES INC.',
                '',
                'By: _________________________________',
                'Name: Dr. Elena Vasquez',
                'Title: Chief Executive Officer',
                'Date: March 15, 2025',
                '',
                '',
                'CASCADE FINANCIAL GROUP LLC',
                '',
                'By: _________________________________',
                'Name: Jonathan R. Blackwell',
                'Title: Managing Partner',
                'Date: March 15, 2025',
            ]),
            ("EXHIBIT A - SERVICE LEVEL AGREEMENTS", [
                'Uptime Guarantee: 99.95%',
                'Response Time for Critical Issues: 1 hour',
                'Response Time for High Priority Issues: 4 hours',
                'Response Time for Medium Priority Issues: 8 hours',
                'Response Time for Low Priority Issues: 24 hours',
                'Scheduled Maintenance Window: Sundays 2:00 AM - 6:00 AM EST',
            ]),
        ]
    },
]

# Define the 8 changes for V2
# Each change: (page_0indexed, section_idx, line_idx, original_text, new_text)
CHANGES = [
    # Page 2 (idx 1): 2 changes
    (1, 0, 3, '        including server provisioning, load balancing, and auto-scaling;',
              '        including server provisioning, load balancing, and auto-scaling;'),  # Change is in line above
    # Actually define changes as full-line replacements:
]

# It's simpler to define V2 pages as copies with specific text substitutions
V2_SUBSTITUTIONS = {
    # page_0indexed: [(old_substring, new_substring), ...]
    1: [
        ('Cloud infrastructure setup and management on Amazon Web Services,',
         'Cloud infrastructure setup and management on Microsoft Azure,'),
        ('a team of no fewer than eight (8)',
         'a team of no fewer than twelve (12)'),
    ],
    3: [
        ('survive for a period of three (3)',
         'survive for a period of five (5)'),
        ('AES-256 encryption for data at rest and TLS 1.2 for data in transit;',
         'AES-256 encryption for data at rest and TLS 1.3 for data in transit;'),
    ],
    4: [
        ('liability insurance of not less than $5,000,000 per occurrence.',
         'liability insurance of not less than $10,000,000 per occurrence.'),
        ('the twelve (12) month period preceding the event giving rise to the claim.',
         'the twenty-four (24) month period preceding the event giving rise to the claim.'),
    ],
    6: [
        ('claim within fifteen (15) business days of becoming aware of such claim.',
         'claim within ten (10) business days of becoming aware of such claim.'),
    ],
    8: [
        ('government actions, or failure of third-party telecommunications.',
         'government actions, or failure of third-party telecommunications or power infrastructure.'),
    ],
}


def build_contract_pdf(output_path, pages_data):
    """Build a 10-page contract PDF from structured page data."""
    doc = pymupdf.open()

    LEFT_MARGIN = 72
    RIGHT_MARGIN = 523
    TOP_MARGIN = 72
    BOTTOM_MARGIN = 770
    LINE_HEIGHT = 14

    for page_idx, page_data in enumerate(pages_data):
        page = doc.new_page(width=595, height=842)
        y = TOP_MARGIN

        # Page title (only page 1)
        if page_data["title"]:
            page.insert_text(
                pymupdf.Point((LEFT_MARGIN + RIGHT_MARGIN) / 2 - 80, y),
                page_data["title"],
                fontsize=PAGE_TITLE_SIZE,
                fontname=PAGE_TITLE_FONT,
                color=(0, 0, 0.4),
            )
            y += 28

        if page_data["subtitle"]:
            page.insert_text(
                pymupdf.Point((LEFT_MARGIN + RIGHT_MARGIN) / 2 - 70, y),
                page_data["subtitle"],
                fontsize=BODY_SIZE,
                fontname=BODY_FONT,
                color=(0.3, 0.3, 0.3),
            )
            y += 30

        for section_title, lines in page_data["sections"]:
            # Section header
            y += 8
            page.insert_text(
                pymupdf.Point(LEFT_MARGIN, y),
                section_title,
                fontsize=SECTION_SIZE,
                fontname=SECTION_FONT,
                color=(0, 0, 0),
            )
            y += 20

            # Section body lines
            for line in lines:
                if line == '':
                    y += 8
                    continue
                page.insert_text(
                    pymupdf.Point(LEFT_MARGIN, y),
                    line,
                    fontsize=BODY_SIZE,
                    fontname=BODY_FONT,
                    color=(0, 0, 0),
                )
                y += LINE_HEIGHT

        # Page number footer
        page.insert_text(
            pymupdf.Point((LEFT_MARGIN + RIGHT_MARGIN) / 2 - 10, 820),
            f"- {page_idx + 1} -",
            fontsize=9,
            fontname=BODY_FONT,
            color=(0.5, 0.5, 0.5),
        )

    doc.save(output_path)
    doc.close()


def apply_substitutions(pages_data, substitutions):
    """Apply text substitutions to create V2 pages. Returns a deep copy."""
    import copy
    v2_pages = copy.deepcopy(pages_data)
    for page_idx, subs in substitutions.items():
        page = v2_pages[page_idx]
        for section_idx, (section_title, lines) in enumerate(page["sections"]):
            new_lines = []
            for line in lines:
                for old_text, new_text in subs:
                    if old_text in line:
                        line = line.replace(old_text, new_text)
                new_lines.append(line)
            page["sections"][section_idx] = (section_title, new_lines)
    return v2_pages


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
    # Create legal directory
    os.makedirs(LEGAL_DIR, exist_ok=True)

    # Build V1
    build_contract_pdf(V1_PATH, CONTRACT_PAGES_V1)
    print(f'Created: {V1_PATH}')

    # Build V2 with substitutions
    v2_pages = apply_substitutions(CONTRACT_PAGES_V1, V2_SUBSTITUTIONS)
    build_contract_pdf(V2_PATH, v2_pages)
    print(f'Created: {V2_PATH}')

    # Verify no diff report exists (should not, fresh env)
    diff_report = f'{LEGAL_DIR}/contract_diff_report.pdf'
    if os.path.exists(diff_report):
        os.remove(diff_report)
        print(f'Removed pre-existing diff report: {diff_report}')

    # Open V1 in Evince for the agent
    launch_gui(f'evince "{V1_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched evince with contract_v1.pdf on DISPLAY=:0')


create_initial()
