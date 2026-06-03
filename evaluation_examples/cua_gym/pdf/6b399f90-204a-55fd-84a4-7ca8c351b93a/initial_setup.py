"""
Initial Setup: Create a 16-page legal contract with 'DRAFT' watermark on every page.
Task ID: pdf_legal_073
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_073'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/final_contract.pdf'

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

# Contract content organized by page
CONTRACT_SECTIONS = [
    # Page 1: Title Page
    {
        "title": "MASTER SERVICES AGREEMENT",
        "content": [
            "",
            "",
            "MASTER SERVICES AGREEMENT",
            "",
            "Contract No.: MSA-2025-04871",
            "",
            "Between:",
            "",
            "MERIDIAN TECHNOLOGIES, INC.",
            "a Delaware corporation",
            '("Service Provider")',
            "",
            "and",
            "",
            "CASCADE FINANCIAL GROUP, LLC",
            "a New York limited liability company",
            '("Client")',
            "",
            "Effective Date: March 15, 2025",
            "",
            "THIS MASTER SERVICES AGREEMENT (this \"Agreement\") is entered into",
            "as of the Effective Date set forth above, by and between the parties",
            "identified above.",
        ]
    },
    # Page 2: Recitals and Definitions
    {
        "title": "RECITALS AND DEFINITIONS",
        "content": [
            "RECITALS",
            "",
            "WHEREAS, Service Provider is engaged in the business of providing",
            "information technology consulting, software development, and related",
            "professional services;",
            "",
            "WHEREAS, Client desires to engage Service Provider to perform certain",
            "services as described herein and in the Statements of Work executed",
            "pursuant to this Agreement;",
            "",
            "NOW, THEREFORE, in consideration of the mutual covenants and",
            "agreements hereinafter set forth, and for other good and valuable",
            "consideration, the receipt and sufficiency of which are hereby",
            "acknowledged, the parties agree as follows:",
            "",
            "ARTICLE 1 - DEFINITIONS",
            "",
            '1.1 "Affiliate" means any entity that directly or indirectly controls,',
            "is controlled by, or is under common control with a party.",
            "",
            '1.2 "Confidential Information" means all non-public information',
            "disclosed by either party to the other party, whether orally, in",
            "writing, or by inspection of tangible objects.",
            "",
            '1.3 "Deliverables" means all work product, documents, software, code,',
            "reports, and other materials created by Service Provider under an SOW.",
            "",
            '1.4 "Intellectual Property Rights" means all patents, copyrights,',
            "trademarks, trade secrets, and other intellectual property rights.",
        ]
    },
    # Page 3: Scope of Services
    {
        "title": "SCOPE OF SERVICES",
        "content": [
            "ARTICLE 2 - SCOPE OF SERVICES",
            "",
            "2.1 Services. Service Provider shall provide the services described",
            "in each Statement of Work (\"SOW\") executed by both parties pursuant",
            "to this Agreement. Each SOW shall be substantially in the form",
            "attached hereto as Exhibit A.",
            "",
            "2.2 Statements of Work. Each SOW shall include, at a minimum:",
            "  (a) A detailed description of the services to be performed;",
            "  (b) The deliverables to be provided;",
            "  (c) The timeline and milestones for completion;",
            "  (d) The fees and payment schedule;",
            "  (e) Any specific terms applicable to that SOW.",
            "",
            "2.3 Personnel. Service Provider shall assign qualified personnel",
            "to perform the services. Service Provider may, with Client's prior",
            "written consent (not to be unreasonably withheld), substitute",
            "personnel of equivalent or greater qualifications.",
            "",
            "2.4 Standard of Performance. Service Provider shall perform all",
            "services in a professional and workmanlike manner consistent with",
            "industry standards and in accordance with applicable laws and",
            "regulations.",
            "",
            "2.5 Client Obligations. Client shall:",
            "  (a) Provide reasonable access to its facilities and systems;",
            "  (b) Designate a project manager as a single point of contact;",
            "  (c) Provide timely feedback and approvals as reasonably required.",
        ]
    },
    # Page 4: Compensation
    {
        "title": "COMPENSATION AND PAYMENT",
        "content": [
            "ARTICLE 3 - COMPENSATION AND PAYMENT",
            "",
            "3.1 Fees. Client shall pay Service Provider the fees set forth in",
            "each applicable SOW. Unless otherwise specified in the SOW:",
            "  (a) Time and materials engagements shall be billed at the rates",
            "      set forth in Exhibit B;",
            "  (b) Fixed-fee engagements shall be invoiced upon completion of",
            "      the milestones specified in the SOW.",
            "",
            "3.2 Expenses. Client shall reimburse Service Provider for all",
            "reasonable, pre-approved, out-of-pocket expenses incurred in",
            "connection with the performance of services.",
            "",
            "3.3 Invoicing. Service Provider shall submit invoices monthly in",
            "arrears. Each invoice shall include reasonable detail of services",
            "performed and expenses incurred.",
            "",
            "3.4 Payment Terms. Client shall pay all undisputed invoices within",
            "thirty (30) days of receipt. Late payments shall bear interest at",
            "the lesser of 1.5% per month or the maximum rate permitted by law.",
            "",
            "3.5 Taxes. Fees are exclusive of all taxes. Client shall be",
            "responsible for all sales, use, and other taxes, excluding taxes",
            "based on Service Provider's income.",
            "",
            "3.6 Rate Adjustments. Service Provider may adjust its standard",
            "rates annually, effective January 1 of each year, with at least",
            "sixty (60) days prior written notice to Client.",
        ]
    },
    # Page 5: Intellectual Property
    {
        "title": "INTELLECTUAL PROPERTY",
        "content": [
            "ARTICLE 4 - INTELLECTUAL PROPERTY RIGHTS",
            "",
            "4.1 Pre-Existing IP. Each party retains all right, title, and",
            "interest in its pre-existing intellectual property. Neither party",
            "grants the other any rights in its pre-existing IP except as",
            "expressly stated herein.",
            "",
            "4.2 Work Product Ownership. Subject to Section 4.3, all Deliverables",
            "created by Service Provider specifically for Client under an SOW",
            "shall be considered works made for hire and shall be the exclusive",
            "property of Client upon full payment of all applicable fees.",
            "",
            "4.3 Service Provider Tools. Service Provider retains ownership of",
            "all tools, methodologies, frameworks, libraries, and know-how that:",
            "  (a) Were developed prior to or independently of this Agreement;",
            "  (b) Are of general applicability and not specific to Client.",
            "",
            "Service Provider hereby grants Client a non-exclusive, perpetual,",
            "royalty-free license to use such tools solely as incorporated in",
            "the Deliverables.",
            "",
            "4.4 Feedback. If Client provides suggestions or feedback regarding",
            "Service Provider's services or products, Service Provider may freely",
            "use such feedback without obligation to Client.",
            "",
            "4.5 Open Source. Service Provider shall identify any open source",
            "components included in the Deliverables and shall ensure compliance",
            "with applicable open source licenses.",
        ]
    },
    # Page 6: Confidentiality
    {
        "title": "CONFIDENTIALITY",
        "content": [
            "ARTICLE 5 - CONFIDENTIALITY",
            "",
            "5.1 Obligations. Each party (the \"Receiving Party\") agrees to:",
            "  (a) Hold all Confidential Information of the other party (the",
            "      \"Disclosing Party\") in strict confidence;",
            "  (b) Not disclose Confidential Information to any third party",
            "      without the prior written consent of the Disclosing Party;",
            "  (c) Use Confidential Information solely for the purposes of",
            "      performing its obligations under this Agreement;",
            "  (d) Protect Confidential Information with at least the same degree",
            "      of care as it uses to protect its own confidential information,",
            "      but in no event less than reasonable care.",
            "",
            "5.2 Exceptions. Confidential Information does not include information",
            "that: (a) is or becomes publicly available through no fault of the",
            "Receiving Party; (b) was in the Receiving Party's possession prior",
            "to disclosure; (c) is independently developed by the Receiving Party;",
            "or (d) is rightfully received from a third party without restriction.",
            "",
            "5.3 Required Disclosure. If the Receiving Party is required by law",
            "or regulation to disclose Confidential Information, it shall provide",
            "prompt notice to the Disclosing Party and cooperate in seeking a",
            "protective order.",
            "",
            "5.4 Duration. The confidentiality obligations shall survive for",
            "five (5) years after the termination of this Agreement.",
        ]
    },
    # Page 7: Representations and Warranties
    {
        "title": "REPRESENTATIONS AND WARRANTIES",
        "content": [
            "ARTICLE 6 - REPRESENTATIONS AND WARRANTIES",
            "",
            "6.1 Mutual Representations. Each party represents and warrants that:",
            "  (a) It is duly organized, validly existing, and in good standing;",
            "  (b) It has full power and authority to enter into this Agreement;",
            "  (c) The execution of this Agreement does not conflict with any",
            "      other agreement to which it is a party.",
            "",
            "6.2 Service Provider Warranties. Service Provider represents and",
            "warrants that:",
            "  (a) The services shall be performed in a professional manner",
            "      consistent with generally accepted industry standards;",
            "  (b) The Deliverables shall substantially conform to the",
            "      specifications set forth in the applicable SOW;",
            "  (c) The Deliverables shall not infringe upon any third-party",
            "      intellectual property rights;",
            "  (d) Service Provider personnel shall have the necessary skills",
            "      and qualifications to perform the services.",
            "",
            "6.3 Warranty Period. Service Provider shall correct any",
            "non-conforming Deliverables at no additional charge if Client",
            "notifies Service Provider within ninety (90) days of delivery.",
            "",
            "6.4 Disclaimer. EXCEPT AS EXPRESSLY SET FORTH IN THIS AGREEMENT,",
            "SERVICE PROVIDER MAKES NO OTHER WARRANTIES, EXPRESS OR IMPLIED,",
            "INCLUDING WITHOUT LIMITATION ANY IMPLIED WARRANTIES OF",
            "MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.",
        ]
    },
    # Page 8: Indemnification
    {
        "title": "INDEMNIFICATION",
        "content": [
            "ARTICLE 7 - INDEMNIFICATION",
            "",
            "7.1 By Service Provider. Service Provider shall indemnify, defend,",
            "and hold harmless Client and its officers, directors, employees,",
            "and agents from and against any third-party claims, losses, damages,",
            "liabilities, and expenses (including reasonable attorneys' fees)",
            "arising out of or relating to:",
            "  (a) Any breach of Service Provider's representations or warranties;",
            "  (b) Any infringement or misappropriation of third-party IP rights",
            "      by the Deliverables;",
            "  (c) The negligence or willful misconduct of Service Provider or",
            "      its personnel.",
            "",
            "7.2 By Client. Client shall indemnify, defend, and hold harmless",
            "Service Provider from and against any third-party claims arising",
            "out of or relating to:",
            "  (a) Client's use of the Deliverables in a manner not contemplated",
            "      by this Agreement;",
            "  (b) Client-provided materials that infringe third-party rights;",
            "  (c) The negligence or willful misconduct of Client.",
            "",
            "7.3 Indemnification Procedure. The indemnified party shall:",
            "  (a) Provide prompt written notice of any claim;",
            "  (b) Grant the indemnifying party sole control of the defense;",
            "  (c) Provide reasonable cooperation and assistance.",
            "",
            "7.4 The indemnified party may participate in the defense at its own",
            "expense with counsel of its own choosing.",
        ]
    },
    # Page 9: Limitation of Liability
    {
        "title": "LIMITATION OF LIABILITY",
        "content": [
            "ARTICLE 8 - LIMITATION OF LIABILITY",
            "",
            "8.1 Exclusion of Consequential Damages. IN NO EVENT SHALL EITHER",
            "PARTY BE LIABLE TO THE OTHER PARTY FOR ANY INDIRECT, INCIDENTAL,",
            "SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING WITHOUT",
            "LIMITATION LOSS OF PROFITS, LOSS OF DATA, BUSINESS INTERRUPTION,",
            "OR LOSS OF GOODWILL, ARISING OUT OF OR RELATING TO THIS AGREEMENT,",
            "REGARDLESS OF THE CAUSE OF ACTION OR THE THEORY OF LIABILITY.",
            "",
            "8.2 Cap on Liability. EXCEPT FOR OBLIGATIONS UNDER ARTICLE 5",
            "(CONFIDENTIALITY) AND ARTICLE 7 (INDEMNIFICATION), THE TOTAL",
            "AGGREGATE LIABILITY OF EITHER PARTY UNDER THIS AGREEMENT SHALL",
            "NOT EXCEED THE GREATER OF: (A) THE TOTAL FEES PAID OR PAYABLE",
            "UNDER THIS AGREEMENT DURING THE TWELVE (12) MONTH PERIOD",
            "IMMEDIATELY PRECEDING THE EVENT GIVING RISE TO THE CLAIM; OR",
            "(B) FIVE HUNDRED THOUSAND DOLLARS ($500,000).",
            "",
            "8.3 Exceptions. The limitations set forth in this Article 8 shall",
            "not apply to:",
            "  (a) A party's breach of its confidentiality obligations;",
            "  (b) A party's indemnification obligations under Article 7;",
            "  (c) Damages arising from a party's gross negligence or willful",
            "      misconduct;",
            "  (d) Claims for infringement of intellectual property rights.",
            "",
            "8.4 Essential Basis. The parties acknowledge that the limitations",
            "and exclusions in this Article 8 reflect a fair allocation of risk",
            "and form an essential basis of the bargain between the parties.",
        ]
    },
    # Page 10: Term and Termination
    {
        "title": "TERM AND TERMINATION",
        "content": [
            "ARTICLE 9 - TERM AND TERMINATION",
            "",
            "9.1 Term. This Agreement shall commence on the Effective Date and",
            "shall continue for a period of three (3) years (the \"Initial Term\"),",
            "unless earlier terminated in accordance with this Article 9.",
            "",
            "9.2 Renewal. Upon expiration of the Initial Term, this Agreement",
            "shall automatically renew for successive one (1) year periods",
            "(each a \"Renewal Term\"), unless either party provides written",
            "notice of non-renewal at least ninety (90) days prior to the",
            "expiration of the then-current term.",
            "",
            "9.3 Termination for Convenience. Either party may terminate this",
            "Agreement or any SOW upon sixty (60) days' prior written notice.",
            "",
            "9.4 Termination for Cause. Either party may terminate this",
            "Agreement immediately upon written notice if the other party:",
            "  (a) Materially breaches this Agreement and fails to cure such",
            "      breach within thirty (30) days of receiving written notice;",
            "  (b) Becomes insolvent or files for bankruptcy protection;",
            "  (c) Makes an assignment for the benefit of creditors.",
            "",
            "9.5 Effect of Termination. Upon termination:",
            "  (a) Client shall pay all fees for services rendered through the",
            "      effective date of termination;",
            "  (b) Service Provider shall deliver all completed Deliverables;",
            "  (c) Each party shall return the other's Confidential Information.",
        ]
    },
    # Page 11: Data Protection
    {
        "title": "DATA PROTECTION",
        "content": [
            "ARTICLE 10 - DATA PROTECTION AND SECURITY",
            "",
            "10.1 Data Processing. To the extent Service Provider processes",
            "personal data on behalf of Client, Service Provider shall:",
            "  (a) Process such data only in accordance with Client's documented",
            "      instructions;",
            "  (b) Implement appropriate technical and organizational measures",
            "      to protect personal data;",
            "  (c) Promptly notify Client of any data breach or security incident;",
            "  (d) Assist Client in responding to data subject requests.",
            "",
            "10.2 Security Measures. Service Provider shall maintain:",
            "  (a) Industry-standard encryption for data in transit and at rest;",
            "  (b) Access controls limiting data access to authorized personnel;",
            "  (c) Regular security assessments and penetration testing;",
            "  (d) Business continuity and disaster recovery procedures;",
            "  (e) Employee training on data protection and security.",
            "",
            "10.3 Sub-processors. Service Provider shall not engage any",
            "sub-processor to process personal data without Client's prior",
            "written consent. Service Provider shall remain fully liable for",
            "the acts and omissions of its sub-processors.",
            "",
            "10.4 Audit Rights. Client shall have the right, upon thirty (30)",
            "days' prior written notice, to audit Service Provider's data",
            "processing activities and security measures.",
            "",
            "10.5 Compliance. Both parties shall comply with all applicable data",
            "protection laws, including but not limited to GDPR, CCPA, and any",
            "other relevant privacy regulations.",
        ]
    },
    # Page 12: Insurance
    {
        "title": "INSURANCE",
        "content": [
            "ARTICLE 11 - INSURANCE",
            "",
            "11.1 Required Coverage. Throughout the term of this Agreement,",
            "Service Provider shall maintain the following insurance coverage:",
            "",
            "  (a) Commercial General Liability Insurance:",
            "      - Per occurrence limit: $2,000,000",
            "      - General aggregate limit: $4,000,000",
            "",
            "  (b) Professional Liability (Errors & Omissions) Insurance:",
            "      - Per claim limit: $5,000,000",
            "      - Aggregate limit: $10,000,000",
            "",
            "  (c) Cyber Liability Insurance:",
            "      - Per occurrence limit: $3,000,000",
            "      - Aggregate limit: $5,000,000",
            "",
            "  (d) Workers' Compensation Insurance as required by applicable law.",
            "",
            "  (e) Commercial Automobile Liability Insurance:",
            "      - Combined single limit: $1,000,000",
            "",
            "11.2 Certificates. Service Provider shall provide Client with",
            "certificates of insurance evidencing the required coverage upon",
            "request. Such certificates shall name Client as an additional",
            "insured under the Commercial General Liability policy.",
            "",
            "11.3 Notice of Cancellation. Service Provider shall provide Client",
            "with at least thirty (30) days' prior written notice of any",
            "material change or cancellation of required coverage.",
        ]
    },
    # Page 13: Dispute Resolution
    {
        "title": "DISPUTE RESOLUTION",
        "content": [
            "ARTICLE 12 - DISPUTE RESOLUTION",
            "",
            "12.1 Negotiation. The parties shall first attempt to resolve any",
            "dispute arising out of or relating to this Agreement through good",
            "faith negotiation between senior executives of each party.",
            "",
            "12.2 Mediation. If the dispute is not resolved through negotiation",
            "within thirty (30) days, the parties shall submit the dispute to",
            "mediation administered by the American Arbitration Association",
            "(\"AAA\") under its Commercial Mediation Procedures.",
            "",
            "12.3 Arbitration. If mediation fails to resolve the dispute within",
            "sixty (60) days, the dispute shall be finally resolved by binding",
            "arbitration administered by the AAA under its Commercial Arbitration",
            "Rules. The arbitration shall be conducted by a single arbitrator",
            "mutually selected by the parties.",
            "",
            "12.4 Venue. All mediation and arbitration proceedings shall take",
            "place in New York, New York.",
            "",
            "12.5 Governing Law. This Agreement shall be governed by and",
            "construed in accordance with the laws of the State of New York,",
            "without giving effect to any choice or conflict of law provision.",
            "",
            "12.6 Injunctive Relief. Notwithstanding the foregoing, either party",
            "may seek injunctive or other equitable relief in any court of",
            "competent jurisdiction to protect its intellectual property rights",
            "or Confidential Information.",
            "",
            "12.7 Attorneys' Fees. The prevailing party in any dispute shall be",
            "entitled to recover its reasonable attorneys' fees and costs.",
        ]
    },
    # Page 14: General Provisions (Part 1)
    {
        "title": "GENERAL PROVISIONS",
        "content": [
            "ARTICLE 13 - GENERAL PROVISIONS",
            "",
            "13.1 Independent Contractor. Service Provider is an independent",
            "contractor and not an employee, agent, joint venturer, or partner",
            "of Client. Service Provider shall be solely responsible for all",
            "taxes, benefits, and insurance for its personnel.",
            "",
            "13.2 Assignment. Neither party may assign this Agreement without",
            "the prior written consent of the other party, except that either",
            "party may assign this Agreement to an Affiliate or in connection",
            "with a merger, acquisition, or sale of substantially all of its",
            "assets.",
            "",
            "13.3 Force Majeure. Neither party shall be liable for any failure",
            "or delay in performance due to circumstances beyond its reasonable",
            "control, including but not limited to acts of God, war, terrorism,",
            "pandemics, government actions, labor disputes, or infrastructure",
            "failures.",
            "",
            "13.4 Notices. All notices under this Agreement shall be in writing",
            "and shall be deemed effective upon:",
            "  (a) Personal delivery;",
            "  (b) The second business day after mailing by certified mail;",
            "  (c) The business day after sending by overnight courier;",
            "  (d) The business day after sending by email with confirmation.",
            "",
            "13.5 Severability. If any provision of this Agreement is held to",
            "be invalid or unenforceable, the remaining provisions shall continue",
            "in full force and effect.",
        ]
    },
    # Page 15: General Provisions (Part 2)
    {
        "title": "GENERAL PROVISIONS (CONTINUED)",
        "content": [
            "13.6 Waiver. The failure of either party to enforce any provision",
            "of this Agreement shall not constitute a waiver of that party's",
            "right to enforce such provision in the future.",
            "",
            "13.7 Entire Agreement. This Agreement, together with all SOWs and",
            "Exhibits, constitutes the entire agreement between the parties with",
            "respect to its subject matter and supersedes all prior or",
            "contemporaneous agreements, representations, and understandings.",
            "",
            "13.8 Amendments. This Agreement may only be amended by a written",
            "instrument signed by both parties.",
            "",
            "13.9 Counterparts. This Agreement may be executed in counterparts,",
            "each of which shall be deemed an original, and all of which together",
            "shall constitute one and the same instrument.",
            "",
            "13.10 Survival. The following provisions shall survive termination",
            "or expiration of this Agreement: Articles 4 (Intellectual Property),",
            "5 (Confidentiality), 7 (Indemnification), 8 (Limitation of",
            "Liability), 10 (Data Protection), and 12 (Dispute Resolution).",
            "",
            "13.11 Publicity. Neither party shall use the other party's name,",
            "logo, or trademarks in any publicity or marketing materials without",
            "the prior written consent of the other party.",
            "",
            "13.12 Third-Party Beneficiaries. This Agreement is for the sole",
            "benefit of the parties hereto and their permitted successors and",
            "assigns. Nothing in this Agreement shall confer any rights upon any",
            "third party.",
        ]
    },
    # Page 16: Signature Page
    {
        "title": "SIGNATURE PAGE",
        "content": [
            "IN WITNESS WHEREOF, the parties hereto have caused this Master",
            "Services Agreement to be executed by their duly authorized",
            "representatives as of the Effective Date.",
            "",
            "",
            "MERIDIAN TECHNOLOGIES, INC.",
            "",
            "",
            "By: _________________________________",
            "Name: Victoria R. Blackwell",
            "Title: Chief Executive Officer",
            "Date: March 15, 2025",
            "",
            "",
            "",
            "CASCADE FINANCIAL GROUP, LLC",
            "",
            "",
            "By: _________________________________",
            "Name: Jonathan M. Hargrove",
            "Title: Managing Partner",
            "Date: March 15, 2025",
            "",
            "",
            "",
            "WITNESS:",
            "",
            "By: _________________________________",
            "Name: Patricia S. Whitfield",
            "Title: General Counsel, Meridian Technologies",
            "Date: March 15, 2025",
        ]
    },
]


def create_initial():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()

    for page_idx, section in enumerate(CONTRACT_SECTIONS):
        # Create A4 page
        page = doc.new_page(width=595, height=842)

        # Page header line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 60), pymupdf.Point(523, 60))
        shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
        shape.commit()

        # Header text: contract number on left, page number on right
        page.insert_text(
            pymupdf.Point(72, 55),
            "MSA-2025-04871  |  MASTER SERVICES AGREEMENT",
            fontsize=8,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )
        page.insert_text(
            pymupdf.Point(490, 55),
            f"Page {page_idx + 1} of 16",
            fontsize=8,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

        # Section title
        if page_idx == 0:
            # Title page - centered large text
            y_start = 200
            page.insert_text(
                pymupdf.Point(150, y_start),
                "MASTER SERVICES AGREEMENT",
                fontsize=22,
                fontname="hebo",
                color=(0.1, 0.1, 0.3),
            )
            y_pos = y_start + 40
            for line in section["content"][3:]:  # Skip the first few empty/title lines
                page.insert_text(
                    pymupdf.Point(150, y_pos),
                    line,
                    fontsize=12 if line.startswith(("MERIDIAN", "CASCADE", "Effective")) else 11,
                    fontname="hebo" if line.startswith(("MERIDIAN", "CASCADE")) else "tiro",
                    color=(0, 0, 0),
                )
                y_pos += 18
        else:
            # Regular content pages
            y_pos = 85
            for line in section["content"]:
                # Determine formatting
                is_article = line.startswith("ARTICLE") or line.startswith("13.")
                is_section = (line and line[0].isdigit() and '.' in line[:4]
                              and not line.startswith("13."))
                is_caps = line.isupper() and len(line) > 5
                is_indent = line.startswith("  ")

                if is_article or is_caps:
                    fontname = "hebo"
                    fontsize = 12
                    color = (0.1, 0.1, 0.3)
                elif is_section:
                    fontname = "tibo"
                    fontsize = 10.5
                    color = (0, 0, 0)
                else:
                    fontname = "tiro"
                    fontsize = 10.5
                    color = (0, 0, 0)

                x_pos = 90 if is_indent else 72
                if line == "":
                    y_pos += 8
                else:
                    page.insert_text(
                        pymupdf.Point(x_pos, y_pos),
                        line,
                        fontsize=fontsize,
                        fontname=fontname,
                        color=color,
                    )
                    y_pos += 16

        # Footer line
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(72, 800), pymupdf.Point(523, 800))
        shape2.finish(color=(0.3, 0.3, 0.3), width=0.5)
        shape2.commit()

        # Footer text
        page.insert_text(
            pymupdf.Point(72, 815),
            "CONFIDENTIAL",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )
        page.insert_text(
            pymupdf.Point(380, 815),
            "Meridian Technologies / Cascade Financial",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Add DRAFT watermark as a large gray text overlay
        # Use morph parameter with a rotation matrix for diagonal placement
        text_point = pymupdf.Point(297, 421)  # center of A4 page
        morph = (text_point, pymupdf.Matrix(45))  # rotate 45 degrees around center
        page.insert_text(
            pymupdf.Point(180, 440),
            "DRAFT",
            fontsize=80,
            fontname="hebo",
            color=(0.85, 0.85, 0.85),
            overlay=True,
            morph=morph,
        )

    # Set metadata
    doc.set_metadata({
        "title": "Master Services Agreement - MSA-2025-04871",
        "author": "Meridian Technologies Legal Department",
        "subject": "Master Services Agreement between Meridian Technologies and Cascade Financial Group",
        "keywords": "contract, services, agreement, legal, MSA",
        "creator": "Legal Document System",
        "producer": "PyMuPDF",
    })

    # Add table of contents (bookmarks)
    toc = []
    for i, section in enumerate(CONTRACT_SECTIONS):
        toc.append([1, section["title"], i + 1])
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
