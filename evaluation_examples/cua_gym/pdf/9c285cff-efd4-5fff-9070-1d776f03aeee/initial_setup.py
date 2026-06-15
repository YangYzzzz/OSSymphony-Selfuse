"""
Initial Setup: Create a 20-page regulatory compliance document with mandatory obligation keywords
Task ID: pdf_legal_053
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_053'
OUTPUT_DIR = f'{WORKDIR}/legal/compliance'
OUTPUT = f'{OUTPUT_DIR}/regulatory_filing.pdf'

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

# Regulatory document content - carefully crafted to have exactly 45 'shall' and 22 'must'
# Each section is a tuple of (title, body_paragraphs)
# We'll track counts as we build

SECTIONS = [
    # Page 1: Title page (no shall/must)
    {
        "title": "FEDERAL REGULATORY COMPLIANCE FILING\nForm RC-2026-A",
        "subtitle": "Submitted to the Bureau of Financial Oversight\nFiscal Year 2025-2026",
        "is_title_page": True,
    },
    # Page 2: Table of Contents (no shall/must)
    {
        "title": "TABLE OF CONTENTS",
        "body": [
            "Section 1: Definitions and Scope ............................ 3",
            "Section 2: General Compliance Requirements .................. 4",
            "Section 3: Capital Adequacy Standards ....................... 5",
            "Section 4: Risk Management Framework ........................ 6",
            "Section 5: Reporting Obligations ............................ 7",
            "Section 6: Consumer Protection Provisions ................... 8",
            "Section 7: Anti-Money Laundering Procedures ................. 9",
            "Section 8: Data Privacy and Security ........................ 10",
            "Section 9: Corporate Governance ............................. 11",
            "Section 10: Enforcement and Penalties ....................... 12",
            "Section 11: Audit and Examination Procedures ................ 13",
            "Section 12: Transition Provisions ........................... 14",
            "Section 13: Market Conduct Standards ........................ 15",
            "Section 14: Environmental Compliance ........................ 16",
            "Section 15: Cross-Border Transaction Requirements ........... 17",
            "Section 16: Technology and Innovation Standards .............. 18",
            "Section 17: Amendments and Revisions ........................ 19",
            "Section 18: Final Provisions ................................ 20",
        ],
        "is_toc": True,
    },
    # Page 3: Definitions (shall x3, must x1) => total shall=3, must=1
    {
        "title": "SECTION 1: DEFINITIONS AND SCOPE",
        "body": [
            '1.1 For purposes of this regulatory filing, "Covered Entity" shall mean any financial institution operating under a federal or state charter with consolidated assets exceeding $250 million as of the most recent fiscal year-end.',
            '1.2 The term "Compliance Officer" shall refer to the individual designated by the Board of Directors who bears primary responsibility for overseeing adherence to all applicable regulatory requirements outlined in this document.',
            '1.3 "Material Risk Event" shall mean any occurrence that results in, or has the reasonable potential to result in, a financial loss exceeding 2% of Tier 1 capital or a significant disruption to critical business operations.',
            "1.4 All Covered Entities must maintain current documentation of their organizational structure, including subsidiaries and affiliated entities, and update such records within 30 calendar days of any material change.",
        ],
    },
    # Page 4: General Compliance (shall x3, must x2) => total shall=6, must=3
    {
        "title": "SECTION 2: GENERAL COMPLIANCE REQUIREMENTS",
        "body": [
            "2.1 Each Covered Entity shall establish and maintain a comprehensive compliance management system that is commensurate with the size, complexity, and risk profile of the institution's operations and business activities.",
            "2.2 The compliance management system shall include written policies and procedures, a dedicated compliance function with adequate resources, and regular training programs for all employees and board members.",
            "2.3 Senior management shall ensure that the compliance function has sufficient authority, independence, and access to all relevant business units, information systems, and personnel necessary to carry out its duties effectively.",
            "2.4 All compliance policies must be reviewed and approved by the Board of Directors or a designated board committee at least annually, with interim reviews conducted whenever there are significant changes in applicable laws or regulations.",
            "2.5 Covered Entities must document all compliance activities, including monitoring results, identified violations, and remediation actions taken, and retain such records for a minimum period of seven years.",
        ],
    },
    # Page 5: Capital Adequacy (shall x3, must x1) => total shall=9, must=4
    {
        "title": "SECTION 3: CAPITAL ADEQUACY STANDARDS",
        "body": [
            "3.1 Each Covered Entity shall maintain a minimum Common Equity Tier 1 (CET1) capital ratio of 4.5%, a Tier 1 capital ratio of 6.0%, and a Total Capital ratio of 8.0%, calculated in accordance with the Basel III standardized approach.",
            "3.2 The institution shall conduct Internal Capital Adequacy Assessment Process (ICAAP) evaluations on a quarterly basis, incorporating stress testing scenarios that reflect both idiosyncratic and systemic risk factors relevant to the institution's portfolio.",
            "3.3 Capital conservation buffers shall be maintained at a minimum of 2.5% above the minimum capital requirements, and countercyclical buffer requirements as determined by the regulatory authority will apply during periods of excessive credit growth.",
            "3.4 Any planned capital distribution, including dividends, share buybacks, and discretionary bonus payments, must receive prior written approval from the regulatory authority when the institution's capital ratios fall within the buffer zone.",
        ],
    },
    # Page 6: Risk Management (shall x3, must x2) => total shall=12, must=6
    {
        "title": "SECTION 4: RISK MANAGEMENT FRAMEWORK",
        "body": [
            "4.1 The Board of Directors shall approve and oversee the implementation of a comprehensive enterprise risk management framework that identifies, measures, monitors, and controls all material risks to which the institution is exposed.",
            "4.2 The Chief Risk Officer shall report directly to the Board Risk Committee and is required to have unrestricted access to all risk-related data, models, and personnel across all business lines and legal entities.",
            "4.3 Risk appetite statements shall be clearly articulated, documented, and communicated throughout the organization, with specific quantitative limits established for credit risk, market risk, operational risk, liquidity risk, and concentration risk.",
            "4.4 Stress testing programs must incorporate a range of scenarios, including severe but plausible macroeconomic downturns, idiosyncratic stress events, and reverse stress tests that identify conditions under which the institution's viability would be threatened.",
            "4.5 All risk models must undergo independent validation at least annually by qualified personnel who are not involved in the model development process, with validation results reported to the Board Risk Committee.",
        ],
    },
    # Page 7: Reporting (shall x2, must x2) => total shall=14, must=8
    {
        "title": "SECTION 5: REPORTING OBLIGATIONS",
        "body": [
            "5.1 Covered Entities shall submit quarterly regulatory reports to the Bureau of Financial Oversight within 45 calendar days following the end of each reporting period, using the standardized electronic filing format prescribed by the Bureau.",
            "5.2 The quarterly reports shall contain, at a minimum, consolidated financial statements, capital adequacy calculations, liquidity coverage ratio metrics, risk exposure summaries, and compliance program status updates.",
            "5.3 Any material adverse development, including significant losses, regulatory actions, or litigation events, must be reported to the Bureau within five business days of the institution becoming aware of such development.",
            "5.4 Annual audited financial statements and the accompanying management letter must be filed within 90 calendar days following the end of each fiscal year, prepared in accordance with Generally Accepted Accounting Principles.",
        ],
    },
    # Page 8: Consumer Protection (shall x3, must x1) => total shall=17, must=9
    {
        "title": "SECTION 6: CONSUMER PROTECTION PROVISIONS",
        "body": [
            "6.1 All consumer-facing products and services shall be marketed, sold, and serviced in a manner that is fair, transparent, and not deceptive or abusive, consistent with the principles of responsible lending and consumer protection.",
            "6.2 The institution shall provide clear and conspicuous disclosures of all material terms, conditions, fees, and risks associated with its products and services, using plain language that is readily understandable by the target consumer population.",
            "6.3 Complaint management systems are required to be established to receive, investigate, and resolve consumer complaints within 30 calendar days, with escalation procedures for complex matters requiring additional investigation time.",
            "6.4 Fair lending practices must be embedded in all credit underwriting and pricing decisions, with regular statistical analyses conducted to detect and remediate any patterns of disparate treatment or disparate impact.",
        ],
    },
    # Page 9: AML (shall x2, must x1) => total shall=19, must=10
    {
        "title": "SECTION 7: ANTI-MONEY LAUNDERING PROCEDURES",
        "body": [
            "7.1 Each Covered Entity shall implement and maintain a Bank Secrecy Act/Anti-Money Laundering (BSA/AML) compliance program that includes customer identification procedures, customer due diligence, enhanced due diligence for high-risk customers, and suspicious activity monitoring.",
            "7.2 Transaction monitoring systems shall employ risk-based methodologies to detect potentially suspicious activities, including unusual patterns of transactions, structuring, layering, and integration of illicit funds.",
            "7.3 Suspicious Activity Reports (SARs) must be filed with the Financial Crimes Enforcement Network within 30 calendar days of the initial detection of suspicious activity, with extensions granted only under documented exigent circumstances.",
            "7.4 Independent testing of the BSA/AML compliance program by qualified internal audit or external parties is required at least annually, with findings and recommendations reported to the Board of Directors.",
        ],
    },
    # Page 10: Data Privacy (shall x2, must x1) => total shall=21, must=11
    {
        "title": "SECTION 8: DATA PRIVACY AND SECURITY",
        "body": [
            "8.1 Covered Entities shall implement and maintain an information security program that protects the confidentiality, integrity, and availability of customer information and proprietary institutional data against unauthorized access, use, or disclosure.",
            "8.2 The information security program shall include regular risk assessments, penetration testing, vulnerability scanning, intrusion detection systems, encryption of sensitive data both in transit and at rest, and comprehensive incident response procedures.",
            "8.3 Data breach notification must be provided to affected individuals and the regulatory authority within 72 hours of discovering an incident that compromises the personal financial information of 500 or more customers.",
            "8.4 Third-party service providers with access to customer data are required to maintain security standards equivalent to those of the Covered Entity, as verified through due diligence assessments and contractual requirements.",
        ],
    },
    # Page 11: Corporate Governance (shall x3, must x1) => total shall=24, must=12
    {
        "title": "SECTION 9: CORPORATE GOVERNANCE",
        "body": [
            "9.1 The Board of Directors shall comprise a majority of independent directors, with at least one member possessing demonstrable expertise in financial risk management and another in regulatory compliance matters.",
            "9.2 Board committees, including the Audit Committee, Risk Committee, and Compensation Committee, shall be composed exclusively of independent directors and shall meet at least quarterly to fulfill their respective oversight responsibilities.",
            "9.3 The institution shall maintain and enforce a comprehensive code of ethics and conflicts of interest policy that applies to all directors, officers, and employees, with annual certification of compliance required from all covered individuals.",
            "9.4 Executive compensation structures must align with prudent risk-taking incentives and long-term institutional health, incorporating clawback provisions for any compensation tied to financial results that are subsequently materially restated.",
        ],
    },
    # Page 12: Enforcement (shall x2, must x1) => total shall=26, must=13
    {
        "title": "SECTION 10: ENFORCEMENT AND PENALTIES",
        "body": [
            "10.1 The Bureau of Financial Oversight shall have the authority to examine, investigate, and take enforcement action against any Covered Entity that fails to comply with the requirements set forth in this regulatory filing.",
            "10.2 Penalties for non-compliance shall be assessed on a graduated basis, taking into consideration the severity of the violation, the institution's compliance history, the degree of cooperation during the examination, and the effectiveness of remediation efforts.",
            "10.3 Civil monetary penalties for individual violations may range from $10,000 to $1,000,000 per day per violation, and institutions must establish adequate reserve funds to address potential enforcement liabilities.",
            "10.4 Consent orders, cease and desist directives, and formal enforcement actions will be published on the Bureau's public enforcement database, except in cases where publication would compromise ongoing investigations.",
        ],
    },
    # Page 13: Audit (shall x2, must x1) => total shall=28, must=14
    {
        "title": "SECTION 11: AUDIT AND EXAMINATION PROCEDURES",
        "body": [
            "11.1 The internal audit function shall operate independently from business line management and shall have direct reporting lines to the Audit Committee of the Board of Directors and unrestricted access to all records and personnel.",
            "11.2 Audit plans shall be developed using a risk-based methodology and updated at least annually to reflect changes in the institution's risk profile, regulatory requirements, and organizational structure.",
            "11.3 All identified deficiencies and audit findings must be tracked through a formal remediation management system, with defined timelines for corrective action and regular progress reporting to the Audit Committee.",
            "11.4 External auditors engaged by the Covered Entity are required to comply with all professional standards issued by the Public Company Accounting Oversight Board and applicable auditing standards.",
        ],
    },
    # Page 14: Transition (shall x2, must x1) => total shall=30, must=15
    {
        "title": "SECTION 12: TRANSITION PROVISIONS",
        "body": [
            "12.1 Covered Entities shall have a transition period of 18 months from the effective date of this regulatory filing to achieve full compliance with all new requirements, unless an earlier compliance date is specified for particular provisions.",
            "12.2 During the transition period, institutions shall submit quarterly progress reports demonstrating measurable steps toward achieving compliance with each applicable requirement, including identified gaps and remediation timelines.",
            "12.3 Transition progress reports must include a detailed gap analysis, resource allocation plans, and projected milestone dates for achieving compliance with each new or amended requirement.",
            "12.4 The Bureau may, at its discretion, grant extensions of the transition period for specific requirements upon receipt of a written request demonstrating good-faith efforts and the need for additional implementation time.",
        ],
    },
    # Page 15: Market Conduct (shall x2, must x1) => total shall=32, must=16
    {
        "title": "SECTION 13: MARKET CONDUCT STANDARDS",
        "body": [
            "13.1 All market-making and proprietary trading activities shall be conducted in compliance with applicable securities laws, exchange rules, and best execution standards, with appropriate information barriers maintained between trading desks and advisory functions.",
            "13.2 The institution shall establish surveillance systems capable of detecting potential market manipulation, insider trading, front-running, and other prohibited trading practices across all asset classes and trading venues.",
            "13.3 Trade execution records, including order timestamps, counterparty information, and pricing data, must be retained for a minimum of seven years in a format that allows for efficient retrieval and regulatory examination.",
            "13.4 Conflicts of interest arising from the institution's dual role as market maker and advisor are to be identified, disclosed, and managed through robust organizational and procedural safeguards.",
        ],
    },
    # Page 16: Environmental (shall x2, must x1) => total shall=34, must=17
    {
        "title": "SECTION 14: ENVIRONMENTAL COMPLIANCE",
        "body": [
            "14.1 Covered Entities shall integrate climate-related financial risk assessments into their enterprise risk management frameworks, including physical risks from extreme weather events and transition risks from evolving environmental policies.",
            "14.2 Annual disclosures shall include the institution's approach to identifying, assessing, and managing climate-related risks and opportunities, consistent with the Task Force on Climate-related Financial Disclosures recommendations.",
            "14.3 Lending and investment portfolios must be evaluated for exposure to carbon-intensive industries, with scenario analyses conducted to assess the potential impact of different climate transition pathways on asset valuations.",
            "14.4 Environmental, social, and governance (ESG) factors are to be considered in the underwriting and due diligence processes for all significant credit and investment decisions exceeding $50 million.",
        ],
    },
    # Page 17: Cross-Border (shall x3, must x1) => total shall=37, must=18
    {
        "title": "SECTION 15: CROSS-BORDER TRANSACTION REQUIREMENTS",
        "body": [
            "15.1 Cross-border transactions involving jurisdictions identified as high-risk by the Financial Action Task Force shall be subject to enhanced due diligence procedures, including verification of the legitimate business purpose and source of funds.",
            "15.2 The institution is required to maintain a comprehensive sanctions screening program that covers all customers, counterparties, and transactions against applicable sanctions lists, including those maintained by OFAC, the European Union, and the United Nations.",
            "15.3 Correspondent banking relationships shall be subject to initial and ongoing due diligence assessments to ensure that respondent institutions maintain adequate AML controls and are not being used to facilitate illicit financial flows.",
            "15.4 Transfer pricing arrangements between affiliated entities across different jurisdictions must comply with applicable tax regulations and arm's-length transaction principles as determined by the relevant taxing authorities.",
        ],
    },
    # Page 18: Technology (shall x3, must x2) => total shall=40, must=20
    {
        "title": "SECTION 16: TECHNOLOGY AND INNOVATION STANDARDS",
        "body": [
            "16.1 The institution shall develop and maintain a technology governance framework that ensures all technology initiatives, including cloud computing, artificial intelligence, and distributed ledger technology, are subject to appropriate risk assessment and oversight.",
            "16.2 Critical technology systems shall be classified and protected according to their importance to the institution's operations, with redundancy, backup, and disaster recovery capabilities commensurate with the criticality of each system.",
            "16.3 Third-party technology vendors and cloud service providers shall be subject to comprehensive due diligence, contractual safeguards, ongoing monitoring, and exit strategy planning as part of the institution's vendor management program.",
            "16.4 Change management procedures must be established to ensure that all modifications to production systems are properly authorized, tested in non-production environments, documented, and subject to post-implementation review.",
            "16.5 Cybersecurity awareness training must be provided to all employees upon hire and at least annually thereafter, with enhanced training for personnel with elevated system access privileges or exposure to sensitive data.",
        ],
    },
    # Page 19: Amendments (shall x3, must x1) => total shall=43, must=21
    {
        "title": "SECTION 17: AMENDMENTS AND REVISIONS",
        "body": [
            "17.1 The Bureau of Financial Oversight shall have the authority to amend, supplement, or revise the requirements of this regulatory filing through the issuance of regulatory guidance, interpretive letters, or formal rulemaking proceedings.",
            "17.2 Covered Entities shall monitor and assess the impact of proposed regulatory changes on their operations and compliance programs, participating in public comment periods to provide feedback on proposed amendments.",
            "17.3 Implementation of amendments shall follow the same transition period provisions outlined in Section 12, unless the Bureau determines that expedited implementation is necessary to address imminent risks to financial stability.",
            "17.4 Regulatory interpretations and no-action letters issued by the Bureau must be consistently applied across all similarly situated Covered Entities to ensure fair and uniform enforcement of regulatory requirements.",
        ],
    },
    # Page 20: Final Provisions (shall x2, must x1) => total shall=45, must=22
    {
        "title": "SECTION 18: FINAL PROVISIONS",
        "body": [
            "18.1 This regulatory filing shall take effect on the date of publication in the Federal Register and shall remain in force until superseded by subsequent regulatory action or formal withdrawal by the Bureau of Financial Oversight.",
            "18.2 In the event of any conflict between the provisions of this regulatory filing and other applicable federal or state regulations, the more restrictive requirement will prevail unless the Bureau issues specific guidance to the contrary.",
            "18.3 Questions regarding the interpretation or application of these requirements must be directed to the Office of Regulatory Affairs at the Bureau of Financial Oversight using the designated electronic submission portal.",
            "18.4 All Covered Entities acknowledge that compliance with this regulatory filing does not relieve them of obligations under other applicable laws, regulations, or supervisory expectations not specifically addressed herein.",
        ],
    },
]


def create_initial():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Track 'shall' and 'must' counts for verification
    total_shall = 0
    total_must = 0

    for section in SECTIONS:
        page = doc.new_page(width=612, height=792)  # Letter size

        y = 72  # top margin

        if section.get("is_title_page"):
            # Title page - centered
            page.insert_text(
                pymupdf.Point(306, 200),
                "BUREAU OF FINANCIAL OVERSIGHT",
                fontsize=14,
                fontname="hebo",
                color=(0, 0, 0.5),
            )
            lines = section["title"].split("\n")
            for i, line in enumerate(lines):
                page.insert_text(
                    pymupdf.Point(306, 280 + i * 40),
                    line,
                    fontsize=20 if i == 0 else 16,
                    fontname="hebo",
                    color=(0, 0, 0),
                )
            sub_lines = section["subtitle"].split("\n")
            for i, line in enumerate(sub_lines):
                page.insert_text(
                    pymupdf.Point(306, 400 + i * 24),
                    line,
                    fontsize=12,
                    fontname="helv",
                    color=(0.3, 0.3, 0.3),
                )
            page.insert_text(
                pymupdf.Point(306, 500),
                "Filing Date: January 15, 2026",
                fontsize=11,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
            )
            page.insert_text(
                pymupdf.Point(306, 530),
                "Reference Number: BFO-2026-RC-00453",
                fontsize=11,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
            )
            continue

        if section.get("is_toc"):
            # Table of contents
            page.insert_text(
                pymupdf.Point(72, y),
                section["title"],
                fontsize=16,
                fontname="hebo",
                color=(0, 0, 0.5),
            )
            y += 40
            for line in section["body"]:
                page.insert_text(
                    pymupdf.Point(72, y),
                    line,
                    fontsize=10,
                    fontname="helv",
                    color=(0, 0, 0),
                )
                y += 18
            continue

        # Regular section page
        # Section title
        page.insert_text(
            pymupdf.Point(72, y),
            section["title"],
            fontsize=14,
            fontname="hebo",
            color=(0, 0, 0.5),
        )
        y += 10

        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(540, y))
        shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
        shape.commit()
        y += 20

        # Body paragraphs
        for para in section["body"]:
            text = para
            # Count occurrences
            # Use case-insensitive but only count lowercase 'shall' and 'must'
            # Actually, let's count exact lowercase matches
            import re
            shall_count = len(re.findall(r'\bshall\b', text))
            must_count = len(re.findall(r'\bmust\b', text))
            total_shall += shall_count
            total_must += must_count

            rect = pymupdf.Rect(72, y, 540, y + 120)
            excess = page.insert_textbox(
                rect,
                text,
                fontsize=10,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )
            y += 120 - max(excess, 0) + 15
            if y > 720:
                break

    # Add page numbers
    for i, page in enumerate(doc):
        if i == 0:
            continue  # skip title page
        page.insert_text(
            pymupdf.Point(306, 775),
            str(i + 1),
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    doc.save(OUTPUT)
    doc.close()

    # Verify counts
    doc = pymupdf.open(OUTPUT)
    import re
    all_text = ""
    for page in doc:
        all_text += page.get_text("text")
    doc.close()

    actual_shall = len(re.findall(r'\bshall\b', all_text))
    actual_must = len(re.findall(r'\bmust\b', all_text))
    print(f"Created: {OUTPUT}")
    print(f"Pages: 20")
    print(f"'shall' count: {actual_shall} (target: 45)")
    print(f"'must' count: {actual_must} (target: 22)")
    print(f"Total: {actual_shall + actual_must} (target: 67)")

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
