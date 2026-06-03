"""
Initial Setup: Create a 150-page legal production document for Bates numbering task.
Task ID: pdf_legal_036
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_036'
PROD_DIR = f'{WORKDIR}/legal/production'
OUTPUT = f'{PROD_DIR}/batch_5.pdf'

# Page dimensions
PAGE_W, PAGE_H = 612, 792  # US Letter

# Realistic legal document content fragments
DOCUMENT_SECTIONS = [
    {
        "title": "CONFIDENTIAL - ATTORNEY WORK PRODUCT",
        "subtitle": "Meridian Technologies, Inc. v. Apex Digital Solutions, LLC",
        "case_no": "Case No. 2023-CV-04817",
        "court": "United States District Court, Southern District of New York",
    },
]

# Realistic deposition excerpts, contract clauses, emails, and memos
DEPOSITION_WITNESSES = [
    ("Dr. Rachel Whitmore", "Chief Technology Officer", "Meridian Technologies"),
    ("James Hartfield", "Vice President of Engineering", "Apex Digital Solutions"),
    ("Linda Matsumoto", "Director of Product Development", "Meridian Technologies"),
    ("Robert Callahan", "Senior Software Architect", "Apex Digital Solutions"),
    ("Dr. Priya Venkatesh", "Expert Witness - Patent Analysis", "Stanford University"),
]

CONTRACT_SECTIONS = [
    "Master Services Agreement", "Software License Agreement",
    "Non-Disclosure Agreement", "Statement of Work #14",
    "Amendment to MSA dated January 15, 2022",
    "Technical Specifications Appendix", "Service Level Agreement",
    "Data Processing Addendum", "Intellectual Property Assignment",
    "Indemnification Provisions",
]

EMAIL_SENDERS = [
    ("r.whitmore@meridiantech.com", "Dr. Rachel Whitmore"),
    ("j.hartfield@apexdigital.com", "James Hartfield"),
    ("l.matsumoto@meridiantech.com", "Linda Matsumoto"),
    ("m.chen@meridiantech.com", "Michael Chen"),
    ("s.patel@apexdigital.com", "Sandeep Patel"),
    ("k.johnson@lawfirmllp.com", "Katherine Johnson, Esq."),
    ("d.martinez@outsidecounsel.com", "David Martinez, Esq."),
]


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


def add_page_header(page, page_num):
    """Add a confidential header to each page."""
    page.insert_text(
        pymupdf.Point(72, 36),
        "CONFIDENTIAL - SUBJECT TO PROTECTIVE ORDER",
        fontsize=8,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )
    page.insert_text(
        pymupdf.Point(PAGE_W - 150, 36),
        f"Page {page_num}",
        fontsize=8,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )
    # Draw header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 42), pymupdf.Point(PAGE_W - 72, 42))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()


def create_cover_page(doc):
    """Create cover page for the production batch."""
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 200
    page.insert_text(pymupdf.Point(PAGE_W/2 - 150, y), "DOCUMENT PRODUCTION", fontsize=20, fontname="hebo", color=(0, 0, 0))
    y += 40
    page.insert_text(pymupdf.Point(PAGE_W/2 - 80, y), "BATCH 5", fontsize=16, fontname="hebo", color=(0, 0, 0))
    y += 50
    page.insert_text(pymupdf.Point(PAGE_W/2 - 180, y), "Meridian Technologies, Inc. v. Apex Digital Solutions, LLC", fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 20
    page.insert_text(pymupdf.Point(PAGE_W/2 - 100, y), "Case No. 2023-CV-04817", fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 20
    page.insert_text(pymupdf.Point(PAGE_W/2 - 170, y), "United States District Court, Southern District of New York", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 50
    page.insert_text(pymupdf.Point(PAGE_W/2 - 100, y), "Produced by: Meridian Technologies, Inc.", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 20
    page.insert_text(pymupdf.Point(PAGE_W/2 - 80, y), "Date: March 20, 2024", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 20
    page.insert_text(pymupdf.Point(PAGE_W/2 - 80, y), "Total Pages: 150", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 60

    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(100, y, PAGE_W - 100, y + 80))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    page.insert_text(pymupdf.Point(120, y + 20), "NOTICE: This production is made pursuant to the Stipulated", fontsize=9, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(120, y + 35), "Protective Order entered on September 8, 2023. All documents", fontsize=9, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(120, y + 50), "are designated CONFIDENTIAL and subject to the terms of the", fontsize=9, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(120, y + 65), "Protective Order.", fontsize=9, fontname="helv", color=(0, 0, 0))
    return page


def create_deposition_pages(doc, witness_idx, start_page_num, num_pages):
    """Create deposition transcript pages."""
    witness = DEPOSITION_WITNESSES[witness_idx % len(DEPOSITION_WITNESSES)]
    line_num = 1
    for p in range(num_pages):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        add_page_header(page, start_page_num + p)

        y = 60
        page.insert_text(pymupdf.Point(72, y), f"DEPOSITION OF {witness[0].upper()}", fontsize=10, fontname="hebo", color=(0, 0, 0))
        y += 15
        page.insert_text(pymupdf.Point(72, y), f"{witness[1]}, {witness[2]}", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
        y += 15
        page.insert_text(pymupdf.Point(72, y), f"Taken on: February {12 + witness_idx}, 2024", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
        y += 25

        # Deposition Q&A content
        qa_pairs = _get_deposition_qa(witness_idx, p)
        for q, a in qa_pairs:
            if y > PAGE_H - 80:
                break
            page.insert_text(pymupdf.Point(90, y), f"{line_num}", fontsize=9, fontname="cour", color=(0.5, 0.5, 0.5))
            line_num += 1
            page.insert_text(pymupdf.Point(120, y), f"Q.  {q}", fontsize=9, fontname="cour", color=(0, 0, 0))
            y += 14
            # Wrap answer text
            answer_lines = _wrap_text(a, 70)
            for al in answer_lines:
                if y > PAGE_H - 80:
                    break
                page.insert_text(pymupdf.Point(90, y), f"{line_num}", fontsize=9, fontname="cour", color=(0.5, 0.5, 0.5))
                line_num += 1
                page.insert_text(pymupdf.Point(120, y), f"A.  {al}" if al == answer_lines[0] else f"    {al}", fontsize=9, fontname="cour", color=(0, 0, 0))
                y += 14
            y += 8


def create_contract_pages(doc, section_idx, start_page_num, num_pages):
    """Create contract/agreement pages."""
    section = CONTRACT_SECTIONS[section_idx % len(CONTRACT_SECTIONS)]
    for p in range(num_pages):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        add_page_header(page, start_page_num + p)

        y = 60
        if p == 0:
            page.insert_text(pymupdf.Point(PAGE_W/2 - 120, y), section.upper(), fontsize=12, fontname="hebo", color=(0, 0, 0))
            y += 30
            page.insert_text(pymupdf.Point(72, y), "This agreement (\"Agreement\") is entered into as of", fontsize=10, fontname="helv", color=(0, 0, 0))
            y += 15
            page.insert_text(pymupdf.Point(72, y), f"January {15 + section_idx}, 2022, by and between:", fontsize=10, fontname="helv", color=(0, 0, 0))
            y += 25
            page.insert_text(pymupdf.Point(90, y), "Meridian Technologies, Inc., a Delaware corporation", fontsize=10, fontname="helv", color=(0, 0, 0))
            y += 15
            page.insert_text(pymupdf.Point(90, y), "(\"Client\" or \"Meridian\")", fontsize=10, fontname="heit", color=(0, 0, 0))
            y += 20
            page.insert_text(pymupdf.Point(72, y), "and", fontsize=10, fontname="helv", color=(0, 0, 0))
            y += 20
            page.insert_text(pymupdf.Point(90, y), "Apex Digital Solutions, LLC, a California limited liability company", fontsize=10, fontname="helv", color=(0, 0, 0))
            y += 15
            page.insert_text(pymupdf.Point(90, y), "(\"Provider\" or \"Apex\")", fontsize=10, fontname="heit", color=(0, 0, 0))
            y += 30

        clauses = _get_contract_clauses(section_idx, p)
        clause_num = p * 3 + 1
        for clause_title, clause_body in clauses:
            if y > PAGE_H - 100:
                break
            page.insert_text(pymupdf.Point(72, y), f"Section {clause_num}. {clause_title}", fontsize=10, fontname="hebo", color=(0, 0, 0))
            y += 18
            clause_num += 1
            lines = _wrap_text(clause_body, 80)
            for line in lines:
                if y > PAGE_H - 80:
                    break
                page.insert_text(pymupdf.Point(72, y), line, fontsize=9, fontname="helv", color=(0, 0, 0))
                y += 13
            y += 10


def create_email_pages(doc, email_idx, start_page_num, num_pages):
    """Create email correspondence pages."""
    sender = EMAIL_SENDERS[email_idx % len(EMAIL_SENDERS)]
    recipient = EMAIL_SENDERS[(email_idx + 1) % len(EMAIL_SENDERS)]
    for p in range(num_pages):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        add_page_header(page, start_page_num + p)

        y = 60
        # Email header
        page.insert_text(pymupdf.Point(72, y), "From:", fontsize=9, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(130, y), f"{sender[1]} <{sender[0]}>", fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 14
        page.insert_text(pymupdf.Point(72, y), "To:", fontsize=9, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(130, y), f"{recipient[1]} <{recipient[0]}>", fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 14
        page.insert_text(pymupdf.Point(72, y), "Date:", fontsize=9, fontname="hebo", color=(0, 0, 0))
        month = (email_idx % 12) + 1
        day = (p * 3 + email_idx) % 28 + 1
        page.insert_text(pymupdf.Point(130, y), f"{month:02d}/{day:02d}/2023 {9 + (email_idx % 8)}:{(p * 17) % 60:02d} AM EST", fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 14
        page.insert_text(pymupdf.Point(72, y), "Subject:", fontsize=9, fontname="hebo", color=(0, 0, 0))
        subjects = [
            "Re: Project Phoenix - Integration Timeline Update",
            "Fw: Q3 Deliverable Status and Milestone Review",
            "Re: Technical Specifications - Revised Architecture",
            "URGENT: Data Migration Issues - Production Environment",
            "Re: License Agreement Amendment - Final Review",
            "Weekly Status Report - Sprint 47",
            "Re: Vendor Performance Metrics - October 2023",
        ]
        page.insert_text(pymupdf.Point(130, y), subjects[(email_idx + p) % len(subjects)], fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 20

        # Separator line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(PAGE_W - 72, y))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()
        y += 15

        # Email body
        body = _get_email_body(email_idx, p)
        lines = _wrap_text(body, 80)
        for line in lines:
            if y > PAGE_H - 80:
                break
            page.insert_text(pymupdf.Point(72, y), line, fontsize=9, fontname="helv", color=(0, 0, 0))
            y += 13


def create_memo_pages(doc, memo_idx, start_page_num, num_pages):
    """Create internal memorandum pages."""
    for p in range(num_pages):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        add_page_header(page, start_page_num + p)

        y = 60
        if p == 0:
            page.insert_text(pymupdf.Point(PAGE_W/2 - 80, y), "INTERNAL MEMORANDUM", fontsize=14, fontname="hebo", color=(0, 0, 0))
            y += 30
            topics = [
                ("Project Phoenix Status Update", "Engineering Leadership Team", "Dr. Rachel Whitmore"),
                ("Vendor Assessment: Apex Digital Solutions", "Board of Directors", "Linda Matsumoto"),
                ("Technical Due Diligence Report", "General Counsel", "Michael Chen"),
                ("Risk Assessment - Platform Migration", "Executive Committee", "Dr. Priya Venkatesh"),
            ]
            topic = topics[memo_idx % len(topics)]
            page.insert_text(pymupdf.Point(72, y), "TO:", fontsize=10, fontname="hebo", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(140, y), topic[1], fontsize=10, fontname="helv", color=(0, 0, 0))
            y += 16
            page.insert_text(pymupdf.Point(72, y), "FROM:", fontsize=10, fontname="hebo", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(140, y), topic[2], fontsize=10, fontname="helv", color=(0, 0, 0))
            y += 16
            page.insert_text(pymupdf.Point(72, y), "DATE:", fontsize=10, fontname="hebo", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(140, y), f"November {10 + memo_idx * 3}, 2023", fontsize=10, fontname="helv", color=(0, 0, 0))
            y += 16
            page.insert_text(pymupdf.Point(72, y), "RE:", fontsize=10, fontname="hebo", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(140, y), topic[0], fontsize=10, fontname="helv", color=(0, 0, 0))
            y += 25

            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(PAGE_W - 72, y))
            shape.finish(color=(0, 0, 0), width=1)
            shape.commit()
            y += 20

        body = _get_memo_body(memo_idx, p)
        lines = _wrap_text(body, 80)
        for line in lines:
            if y > PAGE_H - 80:
                break
            page.insert_text(pymupdf.Point(72, y), line, fontsize=10, fontname="helv", color=(0, 0, 0))
            y += 14


def _wrap_text(text, max_chars):
    """Simple word wrap."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars:
            current_line = current_line + " " + word if current_line else word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines if lines else [""]


def _get_deposition_qa(witness_idx, page_idx):
    """Get realistic Q&A pairs for depositions."""
    all_qa = [
        [
            ("Can you describe your role at Meridian Technologies?", "I serve as Chief Technology Officer. I oversee all technology strategy, engineering teams, and product development initiatives across the organization."),
            ("How long have you held that position?", "I was appointed CTO in March of 2019, so approximately five years at this point."),
            ("Were you involved in the decision to engage Apex Digital Solutions?", "Yes, I was part of the evaluation committee that reviewed several vendors for the platform modernization project we called Project Phoenix."),
            ("What was the scope of Project Phoenix?", "Project Phoenix was a comprehensive initiative to migrate our legacy systems to a modern cloud-based architecture. The total budget was approximately fourteen point five million dollars over a three-year period."),
        ],
        [
            ("Mr. Hartfield, what is your current position?", "I am the Vice President of Engineering at Apex Digital Solutions, where I lead the technical delivery teams."),
            ("Were you assigned to the Meridian account?", "Yes. I was the primary technical lead responsible for the Meridian Technologies engagement from inception through delivery."),
            ("Can you walk us through the initial project timeline?", "The initial Statement of Work called for a phased delivery over eighteen months, with three major milestones at six-month intervals."),
            ("Were those milestones met?", "The first milestone was delivered on schedule. The second milestone experienced approximately six weeks of delay due to scope changes requested by Meridian's engineering team."),
        ],
        [
            ("Ms. Matsumoto, please describe your involvement with the Apex engagement.", "As Director of Product Development, I was responsible for defining the product requirements that Apex would implement as part of the platform migration."),
            ("Did you have regular communications with the Apex team?", "Yes, we had weekly status meetings and I communicated frequently with their project managers and technical leads via email and Microsoft Teams."),
            ("Were there any concerns raised about the quality of deliverables?", "Beginning in approximately August of 2023, we started identifying significant quality issues with the code being delivered. Unit test coverage was below our contractual minimum of eighty percent."),
            ("How did Meridian communicate these concerns?", "I personally raised the issues in our weekly status meetings and followed up with detailed written reports documenting each deficiency."),
        ],
        [
            ("Mr. Callahan, what was your specific role on the Meridian project?", "I was the Senior Software Architect responsible for designing the overall system architecture for the platform migration."),
            ("Did the architecture change during the project?", "Yes, there were several architectural revisions. Some were initiated by our team based on technical discoveries, and others were requested by Meridian."),
            ("Can you describe the most significant architectural change?", "The most significant change was the decision to move from a monolithic architecture to a microservices-based approach. This was requested by Dr. Whitmore in October 2022."),
            ("What impact did that change have on the timeline?", "It required us to fundamentally restructure our approach. We estimated an additional twelve to sixteen weeks of development time."),
        ],
        [
            ("Dr. Venkatesh, what is your area of expertise?", "I am a professor of Computer Science at Stanford University, specializing in software engineering practices, system architecture, and intellectual property analysis in technology disputes."),
            ("Have you been retained as an expert in this matter?", "Yes, I was retained by counsel for Meridian Technologies to provide an independent technical assessment of the deliverables produced by Apex Digital Solutions."),
            ("What materials did you review?", "I reviewed the complete source code repository, all technical documentation, the test suites, deployment configurations, and the contractual specifications including all statements of work and amendments."),
            ("What were your principal findings?", "My analysis identified three primary areas of concern: first, significant deviation from the agreed-upon architectural specifications; second, inadequate test coverage falling well below industry standards; and third, multiple instances of code that appeared to be copied from open-source projects without proper attribution or license compliance."),
        ],
    ]
    qa = all_qa[witness_idx % len(all_qa)]
    # Cycle through Q&A pairs based on page index
    start = (page_idx * 2) % len(qa)
    return qa[start:start+3] if start + 3 <= len(qa) else qa[start:] + qa[:3 - (len(qa) - start)]


def _get_contract_clauses(section_idx, page_idx):
    """Get contract clause content."""
    clauses = [
        [
            ("Definitions", "For purposes of this Agreement, the following terms shall have the meanings set forth below: \"Confidential Information\" means any and all non-public, proprietary information disclosed by either party to the other, whether in written, oral, electronic, or other form, including but not limited to trade secrets, business plans, financial data, customer lists, technical specifications, source code, algorithms, and product roadmaps."),
            ("Term and Termination", "This Agreement shall commence on the Effective Date and continue for a period of thirty-six (36) months, unless earlier terminated in accordance with this Section. Either party may terminate this Agreement for cause upon sixty (60) days written notice to the other party in the event of a material breach that remains uncured after such notice period."),
            ("Compensation and Payment Terms", "Client shall pay Provider in accordance with the fee schedule set forth in Exhibit A. All invoices shall be submitted monthly and shall be payable within thirty (30) days of receipt. Late payments shall accrue interest at the rate of one and one-half percent (1.5%) per month or the maximum rate permitted by applicable law, whichever is less."),
        ],
        [
            ("License Grant", "Subject to the terms and conditions of this Agreement, Provider hereby grants to Client a non-exclusive, non-transferable, worldwide license to use the Software solely for Client's internal business purposes. This license shall survive termination of the Agreement provided that all fees owed have been paid in full."),
            ("Intellectual Property Rights", "All pre-existing intellectual property of each party shall remain the sole property of such party. Any intellectual property created by Provider specifically for Client under this Agreement shall be deemed work-for-hire, and all right, title, and interest therein shall vest in Client upon full payment."),
            ("Warranty and Disclaimer", "Provider warrants that the Software shall materially conform to the specifications set forth in the applicable Statement of Work for a period of twelve (12) months following acceptance. EXCEPT AS EXPRESSLY SET FORTH HEREIN, PROVIDER MAKES NO WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE."),
        ],
        [
            ("Confidentiality Obligations", "Each party agrees to hold the other party's Confidential Information in strict confidence and not to disclose such information to any third party without the prior written consent of the disclosing party. Each party shall use the same degree of care to protect the other party's Confidential Information as it uses to protect its own confidential information, but in no event less than reasonable care."),
            ("Permitted Disclosures", "Notwithstanding the foregoing, a receiving party may disclose Confidential Information to the extent required by law, regulation, or court order, provided that the receiving party gives the disclosing party prompt written notice of such requirement and cooperates with the disclosing party's efforts to obtain a protective order or other appropriate remedy."),
            ("Return of Information", "Upon termination of this Agreement or upon request by the disclosing party, the receiving party shall promptly return or destroy all Confidential Information in its possession, including all copies, notes, and summaries thereof, and shall certify in writing that it has done so."),
        ],
    ]
    idx = section_idx % len(clauses)
    return clauses[idx]


def _get_email_body(email_idx, page_idx):
    """Get email body content."""
    bodies = [
        "Hi team, I wanted to provide an update on the current status of the integration work. As of this week, the API gateway components have been successfully deployed to the staging environment. However, we are still encountering intermittent failures with the authentication module that need to be resolved before we can proceed to production. The engineering team has identified the root cause as a race condition in the token refresh logic. A fix has been developed and is currently undergoing testing. I expect we will be ready for the production deployment by end of next week, pending successful completion of the regression test suite. Please review the attached test results and let me know if you have any questions or concerns. We should schedule a brief sync to align on the deployment timeline. Best regards.",

        "Following up on our discussion from the meeting yesterday, I have compiled the deliverable status report for the Q3 milestones. Overall, we are tracking at approximately seventy-eight percent completion against the planned schedule. The data migration workstream is on track, but the custom reporting module is behind schedule by approximately three weeks due to the additional requirements that were added in Change Request CR-2023-0047. I recommend we discuss the timeline implications during our next steering committee meeting. Additionally, the performance testing results show that the current architecture is meeting the ninety-nine point five percent uptime SLA requirement under normal load conditions, but we are seeing degradation under peak load scenarios that exceed the original capacity projections.",

        "Please find attached the revised technical specifications for the authentication and authorization framework. The key changes from the previous version include: migration from OAuth 2.0 to OpenID Connect for single sign-on capabilities, implementation of multi-factor authentication using TOTP and WebAuthn, enhanced session management with configurable timeout policies, and integration with the existing LDAP directory for user provisioning. These changes were requested during the architecture review meeting on October 15th. The estimated impact on the development timeline is an additional four to six weeks, which has been documented in the attached impact assessment. Please review and provide your feedback by end of business Friday.",

        "URGENT - We are experiencing critical issues with the data migration to the production environment. During the overnight batch processing run, approximately twelve thousand records failed to migrate due to a data format incompatibility between the legacy system and the new platform. The affected records are in the customer accounts and transaction history tables. The root cause appears to be related to the date format handling where the legacy system uses a non-standard date representation that was not accounted for in the migration scripts. We have rolled back the affected records and are implementing a hotfix. I need all hands on deck for the next forty-eight hours to resolve this issue before the next scheduled migration window.",

        "Dear Katherine, pursuant to our telephone conference earlier today, I am writing to confirm the proposed amendments to the Master Services Agreement between Meridian Technologies and Apex Digital Solutions. The key amendments include an extension of the delivery timeline for Phase 2 by ninety days, adjustment of the payment schedule to reflect the revised milestones, addition of enhanced testing requirements including mandatory code review by an independent third party, and inclusion of specific performance benchmarks that must be met prior to each milestone acceptance. Please prepare the amendment documentation for review by both parties. We would like to have this finalized and executed no later than December 15, 2023.",

        "Team, here is the weekly status report for Sprint 47. Completed items: user interface redesign for the dashboard module, implementation of the real-time notification system, database optimization for the reporting queries reducing average response time from four point two seconds to zero point eight seconds. In progress: integration testing for the payment processing module, security audit remediation items. Blocked: deployment of the analytics engine pending resolution of the third-party API compatibility issue. Risks: the upcoming holiday schedule may impact resource availability for the critical path items in Sprint 48 and 49.",

        "Hi Sandeep, I wanted to share the vendor performance metrics for October 2023. Overall satisfaction score: three point two out of five. Code quality index: seventy-two percent, which is below our target of eighty-five percent. On-time delivery rate: sixty-five percent, a decline from seventy-eight percent in September. Defect density: fourteen point seven defects per thousand lines of code, which significantly exceeds the contractual maximum of eight defects per thousand lines. These metrics indicate a continuing decline in performance that we need to address urgently. I recommend we schedule a formal performance review meeting with the Apex leadership team within the next two weeks.",
    ]
    return bodies[(email_idx + page_idx) % len(bodies)]


def _get_memo_body(memo_idx, page_idx):
    """Get memo body content."""
    memos = [
        "Executive Summary: This memorandum provides a comprehensive status update on Project Phoenix as of November 2023. The project, which was initiated in January 2022 with the objective of modernizing Meridian's core technology platform, has encountered significant challenges in the most recent quarter. Key areas of concern include persistent delays in milestone delivery, declining code quality metrics, and growing divergence between the contracted specifications and the actual deliverables. Current Status: As of the date of this memorandum, Phase 1 of the project has been completed, albeit with a cumulative delay of approximately fourteen weeks beyond the original timeline. Phase 2 is currently in progress and is tracking approximately six weeks behind the revised schedule. The total project expenditure to date is approximately eight point three million dollars against a Phase 1-2 budget of seven point one million dollars, representing a cost overrun of approximately seventeen percent. Technical Assessment: The engineering team has conducted a thorough review of the deliverables received from Apex Digital Solutions. Several significant technical deficiencies have been identified, including: inadequate error handling in critical system components, insufficient logging and monitoring capabilities, deviation from the agreed-upon coding standards and architectural patterns, and incomplete implementation of the security requirements outlined in the Statement of Work.",

        "Purpose: This memorandum presents the findings of the vendor assessment conducted for Apex Digital Solutions in connection with the ongoing platform modernization engagement. The assessment covers the period from project inception in January 2022 through October 2023. Methodology: The assessment was conducted using a combination of quantitative metrics analysis, qualitative stakeholder interviews, deliverable reviews, and comparison against contractual requirements and industry benchmarks. A total of twenty-three stakeholders were interviewed across engineering, product management, quality assurance, and project management functions. Findings: Overall, the assessment reveals a pattern of declining performance and growing disconnect between Apex's commitments and their actual delivery capabilities. While the initial phase of the engagement showed promise, subsequent phases have been marked by increasing quality issues, communication breakdowns, and resource allocation challenges. The vendor's technical team has experienced significant turnover, with four of the seven originally assigned senior engineers having departed the engagement.",

        "Background: This technical due diligence report has been prepared at the request of General Counsel in connection with the potential claims arising from the Meridian-Apex engagement. The report provides an independent technical assessment of the software deliverables produced by Apex Digital Solutions under the Master Services Agreement dated January 15, 2022, and the associated Statements of Work. Scope of Review: The review encompassed the following materials: complete source code repository including all branches and commit history, automated test suites and test coverage reports, system architecture documentation and design specifications, deployment scripts and infrastructure-as-code configurations, all change requests and their associated documentation, and correspondence between the technical teams. Key Technical Findings: The source code analysis reveals several areas where the deliverables fail to meet the contractual specifications and industry best practices.",

        "Risk Assessment Overview: This memorandum identifies and evaluates the key risks associated with the proposed platform migration from the legacy monolithic architecture to the microservices-based architecture recommended by Apex Digital Solutions. The assessment considers technical, operational, financial, and organizational risk factors. High-Priority Risks: Data integrity during migration represents the highest-priority risk. The migration involves approximately forty-seven million records across twelve database schemas, with complex referential integrity constraints. Any data corruption or loss during migration could result in significant business disruption and potential regulatory compliance issues. The current migration scripts have not been tested against the full production dataset, and the two test migrations conducted to date have revealed format compatibility issues affecting approximately two percent of records. Medium-Priority Risks: Service continuity during the cutover period presents moderate risk. The current plan calls for a phased migration with parallel operation of legacy and new systems for a period of ninety days.",
    ]
    return memos[memo_idx % len(memos)]


def create_initial():
    """Create the 150-page legal production document."""
    os.makedirs(PROD_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page 1: Cover page
    create_cover_page(doc)

    # Structure the 150 pages with diverse content
    # Pages 2-25: Deposition of Dr. Rachel Whitmore (24 pages)
    create_deposition_pages(doc, 0, 2, 24)

    # Pages 26-45: Master Services Agreement (20 pages)
    create_contract_pages(doc, 0, 26, 20)

    # Pages 46-65: Deposition of James Hartfield (20 pages)
    create_deposition_pages(doc, 1, 46, 20)

    # Pages 66-80: Email correspondence batch 1 (15 pages)
    create_email_pages(doc, 0, 66, 8)
    create_email_pages(doc, 1, 74, 7)

    # Pages 81-95: Software License Agreement (15 pages)
    create_contract_pages(doc, 1, 81, 15)

    # Pages 96-110: Deposition of Linda Matsumoto (15 pages)
    create_deposition_pages(doc, 2, 96, 15)

    # Pages 111-120: Internal Memos (10 pages)
    create_memo_pages(doc, 0, 111, 5)
    create_memo_pages(doc, 1, 116, 5)

    # Pages 121-135: Email correspondence batch 2 (15 pages)
    create_email_pages(doc, 2, 121, 5)
    create_email_pages(doc, 3, 126, 5)
    create_email_pages(doc, 4, 131, 5)

    # Pages 136-145: NDA and Statement of Work (10 pages)
    create_contract_pages(doc, 2, 136, 10)

    # Pages 146-150: Final memos (5 pages)
    create_memo_pages(doc, 2, 146, 3)
    create_memo_pages(doc, 3, 149, 2)

    # Verify we have exactly 150 pages
    current_count = doc.page_count
    if current_count < 150:
        # Add additional pages to reach 150
        for i in range(150 - current_count):
            page_num = current_count + i + 1
            page = doc.new_page(width=PAGE_W, height=PAGE_H)
            add_page_header(page, page_num)
            y = 60
            page.insert_text(pymupdf.Point(72, y), f"EXHIBIT {chr(65 + (i % 26))}-{i // 26 + 1}", fontsize=14, fontname="hebo", color=(0, 0, 0))
            y += 30
            body = _get_email_body(i, i)
            lines = _wrap_text(body, 80)
            for line in lines:
                if y > PAGE_H - 80:
                    break
                page.insert_text(pymupdf.Point(72, y), line, fontsize=9, fontname="helv", color=(0, 0, 0))
                y += 13
    elif current_count > 150:
        # Remove excess pages
        doc.select(list(range(150)))

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {doc.page_count}')
    doc.close()

    # Open in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
