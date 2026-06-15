"""
Initial Setup: Create a 10-page legal agreement PDF with signature blocks on pages 4, 6, and 8.
Task ID: pdf_gf2_029
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_029'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/signed_agreement.pdf'


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

    # Page dimensions: US Letter
    W, H = 612, 792

    # --- Content for 10 pages of a legal services agreement ---

    page_contents = [
        # Page 1: Title page
        {
            "title": "MASTER SERVICES AGREEMENT",
            "body": [
                ("hebo", 14, "Between:"),
                ("helv", 12, "Meridian Technologies Inc. ('Client')"),
                ("helv", 12, "123 Innovation Boulevard, Suite 400"),
                ("helv", 12, "San Francisco, CA 94105"),
                ("helv", 12, ""),
                ("hebo", 14, "And:"),
                ("helv", 12, "Apex Consulting Group LLC ('Consultant')"),
                ("helv", 12, "456 Enterprise Way, Floor 12"),
                ("helv", 12, "New York, NY 10001"),
                ("helv", 12, ""),
                ("helv", 12, "Agreement Date: March 15, 2025"),
                ("helv", 12, "Contract Number: MSA-2025-04782"),
                ("helv", 12, ""),
                ("helv", 11, "This Master Services Agreement ('Agreement') sets forth the terms and"),
                ("helv", 11, "conditions under which Consultant shall provide professional services to"),
                ("helv", 11, "Client as described in the Statements of Work attached hereto."),
            ],
            "has_signature": False,
        },
        # Page 2: Scope of Services
        {
            "title": "SECTION 1: SCOPE OF SERVICES",
            "body": [
                ("helv", 11, "1.1 Consultant agrees to provide the following categories of services:"),
                ("helv", 11, ""),
                ("helv", 11, "    (a) Strategic technology consulting and advisory services"),
                ("helv", 11, "    (b) Software architecture design and review"),
                ("helv", 11, "    (c) Quality assurance and testing framework implementation"),
                ("helv", 11, "    (d) Project management and delivery oversight"),
                ("helv", 11, "    (e) Training and knowledge transfer programs"),
                ("helv", 11, ""),
                ("helv", 11, "1.2 The specific deliverables, timelines, and resource allocations for"),
                ("helv", 11, "each engagement shall be detailed in individual Statements of Work"),
                ("helv", 11, "('SOW'), which shall be executed by both parties and incorporated"),
                ("helv", 11, "into this Agreement by reference."),
                ("helv", 11, ""),
                ("helv", 11, "1.3 Consultant shall assign qualified personnel with appropriate"),
                ("helv", 11, "expertise and experience to perform the services. Client reserves"),
                ("helv", 11, "the right to request replacement of any Consultant personnel who"),
                ("helv", 11, "do not meet reasonable performance standards."),
                ("helv", 11, ""),
                ("hebo", 12, "SECTION 2: COMPENSATION AND PAYMENT TERMS"),
                ("helv", 11, ""),
                ("helv", 11, "2.1 Client shall compensate Consultant at the rates specified in"),
                ("helv", 11, "each SOW. Standard hourly rates are as follows:"),
                ("helv", 11, "    - Senior Consultant: $275/hour"),
                ("helv", 11, "    - Lead Architect: $325/hour"),
                ("helv", 11, "    - Project Director: $375/hour"),
                ("helv", 11, ""),
                ("helv", 11, "2.2 Consultant shall submit detailed invoices on a bi-weekly basis."),
                ("helv", 11, "Payment shall be due within thirty (30) days of invoice receipt."),
            ],
            "has_signature": False,
        },
        # Page 3: Confidentiality
        {
            "title": "SECTION 3: CONFIDENTIALITY AND DATA PROTECTION",
            "body": [
                ("helv", 11, "3.1 Each party acknowledges that during the course of this Agreement,"),
                ("helv", 11, "it may receive or have access to Confidential Information belonging"),
                ("helv", 11, "to the other party. 'Confidential Information' includes but is not"),
                ("helv", 11, "limited to trade secrets, business plans, financial data, customer"),
                ("helv", 11, "lists, technical specifications, and proprietary software."),
                ("helv", 11, ""),
                ("helv", 11, "3.2 The receiving party agrees to:"),
                ("helv", 11, "    (a) Maintain the confidentiality of all Confidential Information"),
                ("helv", 11, "    (b) Use Confidential Information solely for purposes of this Agreement"),
                ("helv", 11, "    (c) Restrict disclosure to employees with a need to know"),
                ("helv", 11, "    (d) Implement reasonable security measures to prevent unauthorized"),
                ("helv", 11, "        access, use, or disclosure"),
                ("helv", 11, ""),
                ("helv", 11, "3.3 These confidentiality obligations shall survive the termination of"),
                ("helv", 11, "this Agreement for a period of five (5) years."),
                ("helv", 11, ""),
                ("hebo", 12, "SECTION 4: INTELLECTUAL PROPERTY"),
                ("helv", 11, ""),
                ("helv", 11, "4.1 All deliverables created by Consultant specifically for Client"),
                ("helv", 11, "under this Agreement ('Work Product') shall be considered works"),
                ("helv", 11, "made for hire and shall be the exclusive property of Client."),
                ("helv", 11, ""),
                ("helv", 11, "4.2 Consultant retains all rights to pre-existing intellectual"),
                ("helv", 11, "property, tools, methodologies, and frameworks ('Consultant IP')."),
                ("helv", 11, "Consultant grants Client a non-exclusive, perpetual license to use"),
                ("helv", 11, "any Consultant IP incorporated into the Work Product."),
            ],
            "has_signature": False,
        },
        # Page 4: Term and Termination + SIGNATURE BLOCK
        {
            "title": "SECTION 5: TERM AND TERMINATION",
            "body": [
                ("helv", 11, "5.1 This Agreement shall commence on the Agreement Date and continue"),
                ("helv", 11, "for an initial term of twenty-four (24) months, unless earlier"),
                ("helv", 11, "terminated as provided herein."),
                ("helv", 11, ""),
                ("helv", 11, "5.2 Either party may terminate this Agreement:"),
                ("helv", 11, "    (a) For convenience, upon sixty (60) days' prior written notice"),
                ("helv", 11, "    (b) For cause, upon thirty (30) days' written notice if the other"),
                ("helv", 11, "        party materially breaches this Agreement and fails to cure"),
                ("helv", 11, "        such breach within the notice period"),
                ("helv", 11, "    (c) Immediately, if the other party becomes insolvent, files for"),
                ("helv", 11, "        bankruptcy, or ceases to operate in the normal course"),
                ("helv", 11, ""),
                ("helv", 11, "5.3 Upon termination, Consultant shall deliver all completed and"),
                ("helv", 11, "in-progress Work Product to Client and return all Confidential"),
                ("helv", 11, "Information within fifteen (15) business days."),
                ("helv", 11, ""),
                ("helv", 11, "5.4 Client shall pay Consultant for all services rendered through"),
                ("helv", 11, "the effective date of termination."),
            ],
            "has_signature": True,
            "signer_name": "Robert J. Harrington",
            "signer_title": "Chief Executive Officer, Meridian Technologies Inc.",
        },
        # Page 5: Liability and Indemnification
        {
            "title": "SECTION 6: LIABILITY AND INDEMNIFICATION",
            "body": [
                ("helv", 11, "6.1 LIMITATION OF LIABILITY. IN NO EVENT SHALL EITHER PARTY BE"),
                ("helv", 11, "LIABLE TO THE OTHER FOR ANY INDIRECT, INCIDENTAL, SPECIAL,"),
                ("helv", 11, "CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING OUT OF OR RELATED TO"),
                ("helv", 11, "THIS AGREEMENT, REGARDLESS OF THE THEORY OF LIABILITY."),
                ("helv", 11, ""),
                ("helv", 11, "6.2 The maximum aggregate liability of either party under this"),
                ("helv", 11, "Agreement shall not exceed the total fees paid or payable during"),
                ("helv", 11, "the twelve (12) month period preceding the event giving rise"),
                ("helv", 11, "to the claim."),
                ("helv", 11, ""),
                ("helv", 11, "6.3 Consultant shall indemnify and hold harmless Client from any"),
                ("helv", 11, "third-party claims arising from:"),
                ("helv", 11, "    (a) Consultant's negligence or willful misconduct"),
                ("helv", 11, "    (b) Infringement of third-party intellectual property rights"),
                ("helv", 11, "    (c) Violation of applicable laws or regulations"),
                ("helv", 11, ""),
                ("helv", 11, "6.4 Client shall indemnify and hold harmless Consultant from any"),
                ("helv", 11, "third-party claims arising from Client's use of the Work Product"),
                ("helv", 11, "in a manner not contemplated by this Agreement."),
                ("helv", 11, ""),
                ("hebo", 12, "SECTION 7: REPRESENTATIONS AND WARRANTIES"),
                ("helv", 11, ""),
                ("helv", 11, "7.1 Consultant represents and warrants that:"),
                ("helv", 11, "    (a) It has the authority to enter into this Agreement"),
                ("helv", 11, "    (b) Services will be performed in a professional manner"),
                ("helv", 11, "    (c) Work Product will not infringe third-party rights"),
            ],
            "has_signature": False,
        },
        # Page 6: Dispute Resolution + SIGNATURE BLOCK
        {
            "title": "SECTION 8: DISPUTE RESOLUTION",
            "body": [
                ("helv", 11, "8.1 The parties agree to attempt to resolve any dispute arising"),
                ("helv", 11, "out of or relating to this Agreement through good-faith negotiation."),
                ("helv", 11, ""),
                ("helv", 11, "8.2 If the dispute cannot be resolved through negotiation within"),
                ("helv", 11, "thirty (30) days, the parties agree to submit the dispute to"),
                ("helv", 11, "mediation administered by the American Arbitration Association"),
                ("helv", 11, "in accordance with its Commercial Mediation Procedures."),
                ("helv", 11, ""),
                ("helv", 11, "8.3 If mediation is unsuccessful, any remaining dispute shall be"),
                ("helv", 11, "resolved by binding arbitration conducted in San Francisco, CA,"),
                ("helv", 11, "in accordance with the Commercial Arbitration Rules of the AAA."),
                ("helv", 11, ""),
                ("helv", 11, "8.4 The arbitrator's decision shall be final and binding, and"),
                ("helv", 11, "judgment upon the award rendered may be entered in any court"),
                ("helv", 11, "having jurisdiction thereof."),
                ("helv", 11, ""),
                ("helv", 11, "8.5 Notwithstanding the foregoing, either party may seek injunctive"),
                ("helv", 11, "relief in any court of competent jurisdiction to prevent"),
                ("helv", 11, "irreparable harm related to breach of confidentiality obligations."),
            ],
            "has_signature": True,
            "signer_name": "Victoria L. Chen",
            "signer_title": "Managing Partner, Apex Consulting Group LLC",
        },
        # Page 7: Insurance and Compliance
        {
            "title": "SECTION 9: INSURANCE AND COMPLIANCE",
            "body": [
                ("helv", 11, "9.1 Consultant shall maintain the following insurance coverages"),
                ("helv", 11, "throughout the term of this Agreement:"),
                ("helv", 11, "    (a) Commercial General Liability: $2,000,000 per occurrence"),
                ("helv", 11, "    (b) Professional Liability (E&O): $5,000,000 per occurrence"),
                ("helv", 11, "    (c) Cyber Liability: $3,000,000 per occurrence"),
                ("helv", 11, "    (d) Workers' Compensation: As required by applicable law"),
                ("helv", 11, ""),
                ("helv", 11, "9.2 Consultant shall provide certificates of insurance upon request"),
                ("helv", 11, "and shall name Client as an additional insured on the CGL policy."),
                ("helv", 11, ""),
                ("hebo", 12, "SECTION 10: COMPLIANCE WITH LAWS"),
                ("helv", 11, ""),
                ("helv", 11, "10.1 Both parties shall comply with all applicable federal, state,"),
                ("helv", 11, "and local laws, regulations, and ordinances in performance of"),
                ("helv", 11, "their obligations under this Agreement."),
                ("helv", 11, ""),
                ("helv", 11, "10.2 Consultant shall comply with all applicable data protection"),
                ("helv", 11, "laws including but not limited to CCPA, GDPR (where applicable),"),
                ("helv", 11, "and industry-specific regulations such as HIPAA and SOX."),
                ("helv", 11, ""),
                ("helv", 11, "10.3 Each party shall maintain reasonable physical, technical,"),
                ("helv", 11, "and administrative safeguards to protect personal data processed"),
                ("helv", 11, "in connection with this Agreement."),
            ],
            "has_signature": False,
        },
        # Page 8: General Provisions + SIGNATURE BLOCK
        {
            "title": "SECTION 11: GENERAL PROVISIONS",
            "body": [
                ("helv", 11, "11.1 Entire Agreement. This Agreement, together with all SOWs and"),
                ("helv", 11, "exhibits attached hereto, constitutes the entire agreement between"),
                ("helv", 11, "the parties and supersedes all prior negotiations and agreements."),
                ("helv", 11, ""),
                ("helv", 11, "11.2 Amendment. This Agreement may not be modified except by a"),
                ("helv", 11, "written instrument signed by both parties."),
                ("helv", 11, ""),
                ("helv", 11, "11.3 Assignment. Neither party may assign this Agreement without"),
                ("helv", 11, "the prior written consent of the other party, except in connection"),
                ("helv", 11, "with a merger, acquisition, or sale of substantially all assets."),
                ("helv", 11, ""),
                ("helv", 11, "11.4 Governing Law. This Agreement shall be governed by and construed"),
                ("helv", 11, "in accordance with the laws of the State of California."),
                ("helv", 11, ""),
                ("helv", 11, "11.5 Severability. If any provision of this Agreement is held to be"),
                ("helv", 11, "invalid or unenforceable, the remaining provisions shall continue"),
                ("helv", 11, "in full force and effect."),
            ],
            "has_signature": True,
            "signer_name": "David M. Thornton",
            "signer_title": "General Counsel, Meridian Technologies Inc.",
        },
        # Page 9: Statement of Work
        {
            "title": "EXHIBIT A: STATEMENT OF WORK #001",
            "body": [
                ("hebo", 12, "Project: Enterprise Cloud Migration Platform"),
                ("helv", 11, "SOW Effective Date: April 1, 2025"),
                ("helv", 11, "Estimated Completion: September 30, 2025"),
                ("helv", 11, ""),
                ("hebo", 11, "1. Project Objectives"),
                ("helv", 11, "Design and implement a cloud-native migration platform enabling"),
                ("helv", 11, "seamless transition of Client's on-premises infrastructure to AWS."),
                ("helv", 11, ""),
                ("hebo", 11, "2. Key Deliverables"),
                ("helv", 11, "    2.1 Cloud Architecture Design Document"),
                ("helv", 11, "    2.2 Migration Automation Toolkit"),
                ("helv", 11, "    2.3 Data Migration Pipeline (ETL Framework)"),
                ("helv", 11, "    2.4 Security and Compliance Assessment Report"),
                ("helv", 11, "    2.5 Performance Testing and Validation Report"),
                ("helv", 11, "    2.6 Operations Runbook and Training Materials"),
                ("helv", 11, ""),
                ("hebo", 11, "3. Resource Allocation"),
                ("helv", 11, "    - 1 Lead Architect (full-time, 6 months)"),
                ("helv", 11, "    - 2 Senior Consultants (full-time, 6 months)"),
                ("helv", 11, "    - 1 Project Director (part-time, 6 months)"),
                ("helv", 11, ""),
                ("hebo", 11, "4. Estimated Budget"),
                ("helv", 11, "    Total Estimated Cost: $1,248,000"),
                ("helv", 11, "    Payment Milestones: 25% at kickoff, 25% at midpoint,"),
                ("helv", 11, "    25% at delivery, 25% upon final acceptance"),
            ],
            "has_signature": False,
        },
        # Page 10: Additional Terms
        {
            "title": "EXHIBIT B: ADDITIONAL TERMS AND CONDITIONS",
            "body": [
                ("hebo", 12, "Non-Solicitation"),
                ("helv", 11, "During the term of this Agreement and for twelve (12) months"),
                ("helv", 11, "following termination, neither party shall directly or indirectly"),
                ("helv", 11, "solicit or hire any employee of the other party who was involved"),
                ("helv", 11, "in the performance of this Agreement, without prior written consent."),
                ("helv", 11, ""),
                ("hebo", 12, "Force Majeure"),
                ("helv", 11, "Neither party shall be liable for any failure to perform its"),
                ("helv", 11, "obligations under this Agreement to the extent such failure is"),
                ("helv", 11, "caused by circumstances beyond its reasonable control, including"),
                ("helv", 11, "natural disasters, pandemics, government actions, or infrastructure"),
                ("helv", 11, "failures."),
                ("helv", 11, ""),
                ("hebo", 12, "Notice Requirements"),
                ("helv", 11, "All notices under this Agreement shall be in writing and delivered"),
                ("helv", 11, "by certified mail, overnight courier, or email with confirmation"),
                ("helv", 11, "of receipt to the addresses set forth on page 1 of this Agreement."),
                ("helv", 11, ""),
                ("hebo", 12, "Counterparts"),
                ("helv", 11, "This Agreement may be executed in counterparts, each of which"),
                ("helv", 11, "shall be deemed an original and all of which together shall"),
                ("helv", 11, "constitute one and the same instrument. Electronic signatures"),
                ("helv", 11, "shall be deemed valid and binding."),
                ("helv", 11, ""),
                ("helv", 10, "--- End of Master Services Agreement MSA-2025-04782 ---"),
            ],
            "has_signature": False,
        },
    ]

    for page_idx, content in enumerate(page_contents):
        page = doc.new_page(width=W, height=H)

        # Page header
        page.insert_text(
            pymupdf.Point(72, 36),
            f"MSA-2025-04782  |  Meridian Technologies Inc. v. Apex Consulting Group LLC",
            fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5),
        )
        # Horizontal line under header
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 42), pymupdf.Point(540, 42))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()

        # Page title
        y = 72
        page.insert_text(
            pymupdf.Point(72, y),
            content["title"],
            fontsize=16, fontname="hebo", color=(0, 0, 0),
        )
        y += 30

        # Body text
        for font, size, text in content["body"]:
            if text == "":
                y += 8
                continue
            page.insert_text(
                pymupdf.Point(72, y),
                text,
                fontsize=size, fontname=font, color=(0, 0, 0),
            )
            y += size + 4

        # Signature block on pages 4, 6, 8 (indices 3, 5, 7)
        if content.get("has_signature"):
            sig_y0 = 650
            # Draw a separator line above signature area
            shape2 = page.new_shape()
            shape2.draw_line(pymupdf.Point(72, sig_y0 - 5), pymupdf.Point(540, sig_y0 - 5))
            shape2.finish(color=(0, 0, 0), width=0.5)
            shape2.commit()

            # Signature line
            page.insert_text(
                pymupdf.Point(72, sig_y0 + 15),
                "Signature: _______________________________",
                fontsize=11, fontname="helv", color=(0, 0, 0),
            )

            # Simulated handwritten signature (using italic bold font)
            page.insert_text(
                pymupdf.Point(160, sig_y0 + 14),
                content["signer_name"],
                fontsize=14, fontname="tibi", color=(0.1, 0.1, 0.4),
            )

            # Printed name
            page.insert_text(
                pymupdf.Point(72, sig_y0 + 35),
                f"Printed Name: {content['signer_name']}",
                fontsize=11, fontname="helv", color=(0, 0, 0),
            )

            # Title
            page.insert_text(
                pymupdf.Point(72, sig_y0 + 52),
                f"Title: {content['signer_title']}",
                fontsize=10, fontname="helv", color=(0, 0, 0),
            )

            # Date
            page.insert_text(
                pymupdf.Point(72, sig_y0 + 66),
                "Date: March 15, 2025",
                fontsize=11, fontname="helv", color=(0, 0, 0),
            )

        # Page footer
        page.insert_text(
            pymupdf.Point(280, 772),
            f"Page {page_idx + 1} of 10",
            fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
