"""
Initial Setup: Create 75-page defense exhibits PDF for Bates numbering task
Task ID: pdf_legal_029
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_029'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/defense_exhibits.pdf'

# Page dimensions (Letter size)
PAGE_W, PAGE_H = 612, 792


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


def build_exhibit_content():
    """Return a list of 75 (title, body_paragraphs) tuples for exhibit pages."""
    exhibits = []

    # Exhibit categories with realistic legal content
    deposition_names = [
        ("Margaret Chen", "Chief Financial Officer", "Vertex Dynamics Corp."),
        ("Robert Hargrove", "Senior Vice President of Operations", "Vertex Dynamics Corp."),
        ("Anya Petrova", "Director of Compliance", "Vertex Dynamics Corp."),
        ("Thomas Whitfield", "External Auditor", "Keating & Associates LLP"),
        ("Diana Morales", "Former Board Member", "Vertex Dynamics Corp."),
        ("James Okonkwo", "IT Systems Administrator", "Vertex Dynamics Corp."),
        ("Sarah Lindqvist", "Head of Human Resources", "Vertex Dynamics Corp."),
        ("William Tanaka", "Product Development Lead", "Vertex Dynamics Corp."),
    ]

    contract_parties = [
        ("Vertex Dynamics Corp.", "Apex Manufacturing LLC"),
        ("Vertex Dynamics Corp.", "Northern Ridge Holdings"),
        ("Vertex Dynamics Corp.", "Clearwater Distribution Inc."),
        ("Vertex Dynamics Corp.", "Pacific Standard Technologies"),
        ("Vertex Dynamics Corp.", "Meridian Capital Partners"),
    ]

    # Pages 1-8: Deposition excerpts
    for i, (name, title, company) in enumerate(deposition_names):
        exhibits.append((
            f"EXHIBIT D-{i+1}: Deposition of {name}",
            [
                f"DEPOSITION OF {name.upper()}",
                f"Title: {title}, {company}",
                f"Date: {['January 15', 'February 3', 'February 28', 'March 12', 'March 27', 'April 8', 'April 22', 'May 5'][i]}, 2025",
                f"Location: Law Offices of Brennan, Caldwell & Associates, 1200 Market Street, Suite 400, San Francisco, CA 94102",
                "",
                f"Q: {name.split()[0]}, can you state your full name and current title for the record?",
                f"A: My name is {name}, and I currently serve as {title} at {company}.",
                "",
                "Q: How long have you held this position?",
                f"A: I've been in this role since {'2019' if i < 4 else '2021'}. Prior to that, I held various positions within the organization.",
                "",
                f"Q: Are you familiar with the transactions at issue in this litigation?",
                f"A: Yes, I am. In my capacity as {title}, I had direct involvement with the matters pertaining to the disputed contractual obligations.",
                "",
                "Q: Can you describe the nature of your involvement?",
                f"A: Certainly. I was responsible for overseeing the {'financial reporting' if i == 0 else 'operational aspects' if i == 1 else 'regulatory compliance' if i == 2 else 'audit review' if i == 3 else 'strategic governance' if i == 4 else 'technical infrastructure' if i == 5 else 'personnel management' if i == 6 else 'product specifications'} related to the agreement in question.",
                "",
                "[Continued on subsequent pages]",
            ]
        ))

    # Pages 9-16: Deposition continuations
    for i, (name, title, company) in enumerate(deposition_names):
        exhibits.append((
            f"EXHIBIT D-{i+1} (Continued): Deposition of {name}",
            [
                f"DEPOSITION OF {name.upper()} -- CONTINUED",
                "",
                "Q: Were you present at the meeting on September 14, 2024?",
                f"A: Yes, I attended that meeting in my capacity as {title}.",
                "",
                "Q: What was discussed at that meeting?",
                "A: The primary topics included the quarterly performance review, the status of the Apex Manufacturing contract, and certain compliance concerns that had been raised by our internal audit team.",
                "",
                "Q: Can you elaborate on those compliance concerns?",
                "A: The internal audit identified several discrepancies in the billing records associated with the Northern Ridge Holdings account. These discrepancies totaled approximately $2.3 million over the fiscal year.",
                "",
                "Q: What action was taken in response to these findings?",
                "A: We initiated an internal investigation and retained outside counsel. The board was notified within 48 hours pursuant to our corporate governance charter.",
                "",
                f"COUNSEL FOR PLAINTIFF: Objection, calls for speculation.",
                f"THE WITNESS: I can only speak to what I directly observed and the reports I received.",
                "",
                "[Deposition continues]",
            ]
        ))

    # Pages 17-26: Contract documents
    contract_titles = [
        "Master Services Agreement",
        "Amendment No. 1 to Master Services Agreement",
        "Statement of Work No. 2024-07",
        "Non-Disclosure Agreement",
        "Supply Chain Partnership Agreement",
        "Licensing Agreement",
        "Amendment No. 2 to Master Services Agreement",
        "Service Level Agreement",
        "Indemnification Agreement",
        "Termination Notice",
    ]
    for i, ctitle in enumerate(contract_titles):
        party_a, party_b = contract_parties[i % len(contract_parties)]
        date_str = f"{'January' if i < 3 else 'April' if i < 6 else 'July' if i < 9 else 'October'} {10 + i}, 2024"
        exhibits.append((
            f"EXHIBIT D-{17+i}: {ctitle}",
            [
                ctitle.upper(),
                "",
                f"This {ctitle} (the 'Agreement') is entered into as of {date_str}, by and between:",
                "",
                f"  {party_a} ('Party A'), a Delaware corporation with principal offices at 500 Innovation Drive, San Jose, CA 95134",
                "",
                f"  and",
                "",
                f"  {party_b} ('Party B'), a {'California' if i % 2 == 0 else 'New York'} {'corporation' if i % 3 == 0 else 'limited liability company'} with principal offices at {1000 + i * 100} Commerce Boulevard, {'Los Angeles, CA 90017' if i % 2 == 0 else 'New York, NY 10022'}",
                "",
                "WHEREAS, the parties wish to establish the terms and conditions under which Party A shall provide certain services to Party B;",
                "",
                f"WHEREAS, Party B has expressed interest in engaging Party A for {'consulting services' if i < 3 else 'technology licensing' if i < 6 else 'supply chain management' if i < 9 else 'contract wind-down'};",
                "",
                "NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth herein, and for other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the parties agree as follows:",
                "",
                f"1. SCOPE OF SERVICES",
                f"   Party A shall provide the services described in the attached Schedule A, which is incorporated herein by reference.",
                "",
                f"2. TERM",
                f"   This Agreement shall commence on {date_str} and continue for a period of {'twelve (12)' if i < 5 else 'twenty-four (24)'} months unless earlier terminated in accordance with Section 8.",
                "",
                f"3. COMPENSATION",
                f"   Party B shall pay Party A a total fee of ${(i+1) * 150000 + 50000:,.2f} payable in {'monthly' if i < 5 else 'quarterly'} installments.",
            ]
        ))

    # Pages 27-36: Financial records
    financial_docs = [
        "Quarterly Revenue Report Q1 2024",
        "Quarterly Revenue Report Q2 2024",
        "Quarterly Revenue Report Q3 2024",
        "Quarterly Revenue Report Q4 2024",
        "Annual Consolidated Balance Sheet FY2024",
        "Accounts Receivable Aging Summary",
        "Wire Transfer Records - September 2024",
        "Wire Transfer Records - October 2024",
        "Expense Report Summary - Executive Division",
        "Budget Variance Analysis FY2024",
    ]
    for i, fdoc in enumerate(financial_docs):
        exhibits.append((
            f"EXHIBIT D-{27+i}: {fdoc}",
            [
                f"VERTEX DYNAMICS CORP.",
                f"{fdoc.upper()}",
                f"{'CONFIDENTIAL - SUBJECT TO PROTECTIVE ORDER' if i < 7 else 'ATTORNEYS EYES ONLY'}",
                "",
                f"Prepared by: Finance Department",
                f"Date: {'March 31' if i == 0 else 'June 30' if i == 1 else 'September 30' if i == 2 else 'December 31' if i == 3 else 'January 15' if i == 4 else 'December 31' if i == 5 else 'October 1' if i == 6 else 'November 1' if i == 7 else 'December 15' if i == 8 else 'January 20'}, {'2024' if i < 8 else '2025'}",
                "",
                "=" * 60,
                "",
                f"{'Revenue Summary:' if i < 4 else 'Financial Data:'}",
                f"  Total Revenue: ${(4500000 + i * 320000):,.2f}",
                f"  Cost of Goods Sold: ${(2100000 + i * 145000):,.2f}",
                f"  Gross Profit: ${(2400000 + i * 175000):,.2f}",
                f"  Operating Expenses: ${(1800000 + i * 95000):,.2f}",
                f"  Net Income: ${(600000 + i * 80000):,.2f}",
                "",
                f"  Accounts Receivable: ${(3200000 + i * 210000):,.2f}",
                f"  Accounts Payable: ${(2100000 + i * 130000):,.2f}",
                f"  Cash and Equivalents: ${(8500000 + i * 450000):,.2f}",
                "",
                "Notes:",
                f"  - {'Quarterly figures include adjustments for accrued liabilities' if i < 4 else 'Figures are subject to final audit review'}",
                f"  - All amounts in USD",
            ]
        ))

    # Pages 37-46: Email correspondence
    email_senders = [
        ("m.chen@vertexdynamics.com", "Margaret Chen"),
        ("r.hargrove@vertexdynamics.com", "Robert Hargrove"),
        ("legal@vertexdynamics.com", "Legal Department"),
        ("j.brennan@brennancaldwell.com", "John Brennan, Esq."),
        ("a.petrova@vertexdynamics.com", "Anya Petrova"),
        ("d.morales@boardmember.com", "Diana Morales"),
        ("cfo@apexmfg.com", "Kevin Walsh"),
        ("j.okonkwo@vertexdynamics.com", "James Okonkwo"),
        ("s.lindqvist@vertexdynamics.com", "Sarah Lindqvist"),
        ("t.whitfield@keatingllp.com", "Thomas Whitfield"),
    ]
    email_subjects = [
        "Re: Q3 Revenue Reconciliation Discrepancies",
        "FW: Urgent - Northern Ridge Billing Audit Findings",
        "Re: Board Notification - Compliance Investigation",
        "Privileged & Confidential: Litigation Strategy Update",
        "Re: Regulatory Filing Deadline Extension Request",
        "Board Resolution - Special Committee Formation",
        "Re: Outstanding Invoice Dispute - Account #VD-2024-0847",
        "Server Access Logs - September 14 Meeting Records",
        "Personnel File Request - Compliance Investigation",
        "Preliminary Audit Findings - Confidential Draft",
    ]
    for i in range(10):
        sender_email, sender_name = email_senders[i]
        recipient_email, recipient_name = email_senders[(i + 3) % len(email_senders)]
        exhibits.append((
            f"EXHIBIT D-{37+i}: Email Correspondence",
            [
                "PRINTED EMAIL CORRESPONDENCE",
                "",
                f"From: {sender_name} <{sender_email}>",
                f"To: {recipient_name} <{recipient_email}>",
                f"Date: {'August' if i < 3 else 'September' if i < 6 else 'October' if i < 8 else 'November'} {5 + i * 2}, 2024 {9 + i}:{'15' if i % 2 == 0 else '47'} {'AM' if i < 5 else 'PM'} PST",
                f"Subject: {email_subjects[i]}",
                "",
                "-" * 60,
                "",
                f"Dear {recipient_name.split()[0]},",
                "",
                f"I am writing regarding the {'financial discrepancies' if i < 3 else 'compliance matters' if i < 6 else 'ongoing investigation' if i < 8 else 'audit findings'} that were discussed in our recent meeting.",
                "",
                f"As you are aware, the {'internal audit team' if i % 2 == 0 else 'external counsel'} has identified several areas of concern that require immediate attention. Specifically:",
                "",
                f"  1. The {'billing records' if i < 4 else 'transaction logs'} for the period ending September 30, 2024, show {'unexplained variances totaling $2.3 million' if i < 3 else 'irregular patterns in the approval workflow' if i < 6 else 'inconsistencies with the reported figures'}.",
                "",
                f"  2. {'Several key documents appear to have been modified after the initial filing deadline.' if i % 3 == 0 else 'The timeline of events does not align with the statements provided during the preliminary review.' if i % 3 == 1 else 'Additional supporting documentation has been requested but not yet received from the relevant department heads.'}",
                "",
                f"Please {'review the attached summary' if i < 5 else 'provide your response'} by {'end of business Friday' if i % 2 == 0 else 'close of business Monday'}. This matter is {'time-sensitive' if i < 5 else 'of the highest priority'}.",
                "",
                f"Best regards,",
                f"{sender_name}",
            ]
        ))

    # Pages 47-56: Expert reports and analysis
    expert_topics = [
        ("Dr. Katherine Reeves", "Forensic Accounting", "Analysis of Financial Irregularities in Vertex Dynamics Billing Records"),
        ("Prof. Alan Chambers", "Corporate Governance", "Assessment of Board Oversight Practices and Fiduciary Duties"),
        ("Dr. Nina Vasquez", "Digital Forensics", "Examination of Electronic Document Metadata and Access Logs"),
        ("Dr. Richard Holm", "Statistical Analysis", "Statistical Sampling of Transaction Records and Error Rate Analysis"),
        ("Patricia Nakamura, CPA", "Damages Quantification", "Estimated Damages and Lost Profits Calculation"),
        ("Dr. Samuel Osei", "Industry Standards", "Comparison of Vertex Dynamics Practices to Industry Benchmarks"),
        ("Dr. Elena Marchetti", "Regulatory Compliance", "Review of SEC Filing Compliance and Disclosure Obligations"),
        ("Prof. David Kessler", "Contract Interpretation", "Analysis of Ambiguous Contract Provisions and Industry Custom"),
        ("Dr. Lisa Chang", "Economic Analysis", "Market Impact Assessment and Competitive Harm Evaluation"),
        ("Michael Torres, CFA", "Valuation", "Enterprise Valuation and Fair Market Value Determination"),
    ]
    for i, (expert, field, topic) in enumerate(expert_topics):
        exhibits.append((
            f"EXHIBIT D-{47+i}: Expert Report - {expert}",
            [
                "EXPERT REPORT",
                "",
                f"Prepared by: {expert}",
                f"Field of Expertise: {field}",
                f"Date: {'November' if i < 5 else 'December'} {1 + i * 3}, 2024",
                "",
                f"Re: {topic}",
                "",
                "=" * 60,
                "",
                "I. QUALIFICATIONS",
                "",
                f"I, {expert}, have been retained by counsel for the defense to provide expert analysis in the matter of Meridian Capital Partners v. Vertex Dynamics Corp., Case No. 2024-CV-08847.",
                "",
                f"I hold a {'Ph.D.' if 'Dr.' in expert or 'Prof.' in expert else 'professional certification'} in {field} from {'Stanford University' if i < 3 else 'Columbia University' if i < 6 else 'MIT' if i < 8 else 'the University of Chicago'}. I have over {15 + i} years of experience in {field.lower()} and have served as an expert witness in {20 + i * 3} prior engagements.",
                "",
                "II. SUMMARY OF OPINIONS",
                "",
                f"Based on my review of the documents produced in this litigation, my analysis of the {'financial records' if i < 4 else 'electronic evidence' if i < 7 else 'industry data'}, and my professional experience, I have formed the following opinions:",
                "",
                f"  1. The {'financial discrepancies' if i < 3 else 'procedural irregularities' if i < 6 else 'contractual disputes'} identified by the plaintiff {'do not rise to the level of' if i % 2 == 0 else 'are inconsistent with allegations of'} {'intentional misconduct' if i < 5 else 'systemic failure'}.",
                "",
                f"  2. The {'accounting practices' if i < 4 else 'business processes' if i < 7 else 'market conditions'} employed by Vertex Dynamics were {'consistent with' if i % 2 == 0 else 'within the reasonable range of'} industry standards during the relevant period.",
                "",
                "[Full report continues in supplemental filing]",
            ]
        ))

    # Pages 57-66: Corporate records and meeting minutes
    corp_docs = [
        "Board of Directors Meeting Minutes - July 15, 2024",
        "Board of Directors Meeting Minutes - August 22, 2024",
        "Board of Directors Meeting Minutes - September 14, 2024",
        "Special Committee Meeting Minutes - October 3, 2024",
        "Special Committee Meeting Minutes - October 18, 2024",
        "Corporate Resolution No. 2024-031",
        "Corporate Resolution No. 2024-042",
        "Shareholder Communication - Q3 2024",
        "Internal Memorandum - Risk Assessment",
        "Internal Memorandum - Remediation Plan",
    ]
    for i, cdoc in enumerate(corp_docs):
        exhibits.append((
            f"EXHIBIT D-{57+i}: {cdoc}",
            [
                f"VERTEX DYNAMICS CORP.",
                f"{cdoc.upper()}",
                "CONFIDENTIAL",
                "",
                f"{'Date: ' + ['July 15', 'August 22', 'September 14', 'October 3', 'October 18', 'October 25', 'November 8', 'November 15', 'November 22', 'December 1'][i] + ', 2024'}",
                f"{'Location: Corporate Headquarters, Board Room A' if i < 5 else 'Prepared by: Office of the General Counsel'}",
                "",
                "=" * 60,
                "",
                f"{'ATTENDEES:' if i < 5 else 'SUBJECT:'}",
                "",
                f"{'  - Diana Morales (Chair)' if i < 5 else '  Re: ' + ('Authorization of external investigation' if i == 5 else 'Retention of forensic accounting firm' if i == 6 else 'Quarterly update to shareholders' if i == 7 else 'Comprehensive risk assessment of current litigation' if i == 8 else 'Proposed remediation measures and timeline')}",
                f"{'  - Margaret Chen (CFO)' if i < 5 else ''}",
                f"{'  - Robert Hargrove (SVP Operations)' if i < 5 else ''}",
                f"{'  - General Counsel (via telephone)' if i < 5 else ''}",
                "",
                f"{'MINUTES:' if i < 5 else 'BODY:'}",
                "",
                f"{'The meeting was called to order at ' + ['10:00 AM', '2:30 PM', '9:00 AM', '11:00 AM', '3:00 PM'][i % 5] + '.' if i < 5 else 'This memorandum sets forth the findings and recommendations of the undersigned.'}",
                "",
                f"The {'board discussed' if i < 5 else 'document addresses'} the following matters:",
                f"  1. {'Status of ongoing litigation with Meridian Capital Partners' if i < 3 else 'Progress of internal investigation' if i < 5 else 'Recommended courses of action'}",
                f"  2. {'Financial impact assessment and reserve requirements' if i < 4 else 'Risk mitigation strategies' if i < 7 else 'Implementation timeline and resource allocation'}",
                f"  3. {'Communications strategy for stakeholders' if i < 6 else 'Compliance enhancement measures'}",
                "",
                f"{'The board voted unanimously to approve the proposed action items.' if i < 5 else 'This document is protected by attorney-client privilege and work product doctrine.'}",
            ]
        ))

    # Pages 67-75: Miscellaneous exhibits
    misc_docs = [
        "Organizational Chart - Vertex Dynamics Corp.",
        "Timeline of Key Events (January - December 2024)",
        "Summary of Disputed Transactions",
        "Insurance Coverage Summary - D&O Policy",
        "Third-Party Vendor Compliance Certifications",
        "Internal Whistleblower Report (Redacted)",
        "External Counsel Engagement Letter",
        "Settlement Demand Analysis",
        "Demonstrative Exhibit - Funds Flow Diagram",
    ]
    for i, mdoc in enumerate(misc_docs):
        exhibits.append((
            f"EXHIBIT D-{67+i}: {mdoc}",
            [
                mdoc.upper(),
                "",
                f"Case: Meridian Capital Partners v. Vertex Dynamics Corp.",
                f"Case No.: 2024-CV-08847",
                f"Court: United States District Court, Northern District of California",
                "",
                "=" * 60,
                "",
                f"{'This exhibit presents' if i < 5 else 'This document contains'} {'the corporate organizational structure of Vertex Dynamics as of September 2024.' if i == 0 else 'a chronological summary of material events during the relevant period.' if i == 1 else 'an itemized listing of the 47 transactions in dispute, totaling $14,729,384.50.' if i == 2 else 'coverage details for the Directors and Officers liability insurance policy, Policy No. VD-DO-2024-001.' if i == 3 else 'certifications received from third-party vendors confirming compliance with applicable regulations.' if i == 4 else 'the substance of reports received through the company anonymous reporting hotline (personal identifying information redacted pursuant to court order).' if i == 5 else 'the terms of engagement between Vertex Dynamics Corp. and Brennan, Caldwell & Associates for legal representation in this matter.' if i == 6 else 'a detailed analysis of the plaintiff settlement demand of $45,000,000 and the defense valuation of reasonable exposure.' if i == 7 else 'a visual representation of the flow of funds between Vertex Dynamics, its subsidiaries, and the entities at issue in this litigation.'}",
                "",
                f"Prepared for use in connection with the defense of the above-captioned matter.",
                "",
                f"Date prepared: {'November' if i < 5 else 'December'} {5 + i * 2}, 2024",
                f"Prepared by: {'Brennan, Caldwell & Associates' if i % 2 == 0 else 'Vertex Dynamics Legal Department'}",
                "",
                "CONFIDENTIAL - SUBJECT TO PROTECTIVE ORDER",
                "",
                "[Document content follows]",
                "",
                f"{'This page intentionally left partially blank for annotation purposes.' if i == 8 else 'See attached schedules for supporting detail.'}",
            ]
        ))

    return exhibits


def create_initial():
    # Ensure directory exists
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()
    exhibits = build_exhibit_content()

    for page_idx, (title, paragraphs) in enumerate(exhibits):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)

        # Header line
        page.insert_text(
            pymupdf.Point(72, 50),
            "Meridian Capital Partners v. Vertex Dynamics Corp. | Case No. 2024-CV-08847",
            fontsize=8,
            fontname="cour",
            color=(0.4, 0.4, 0.4),
        )

        # Horizontal rule under header
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 55), pymupdf.Point(540, 55))
        shape.finish(color=(0.4, 0.4, 0.4), width=0.5)
        shape.commit()

        # Exhibit title
        page.insert_text(
            pymupdf.Point(72, 80),
            title,
            fontsize=13,
            fontname="hebo",
            color=(0, 0, 0),
        )

        # Body content
        y_pos = 110
        for para in paragraphs:
            if para == "":
                y_pos += 8
                continue
            if para.startswith("=") or para.startswith("-" * 10):
                # Draw a line
                shape = page.new_shape()
                shape.draw_line(pymupdf.Point(72, y_pos - 2), pymupdf.Point(540, y_pos - 2))
                shape.finish(color=(0, 0, 0), width=0.5)
                shape.commit()
                y_pos += 10
                continue

            # Use textbox for wrapping
            rect = pymupdf.Rect(72, y_pos, 540, y_pos + 60)
            fontname = "hebo" if para.isupper() and len(para) > 5 else "helv"
            fontsize = 10 if fontname == "hebo" else 9.5

            excess = page.insert_textbox(
                rect,
                para,
                fontsize=fontsize,
                fontname=fontname,
                color=(0, 0, 0),
            )
            # Estimate lines used
            chars_per_line = 75
            lines = max(1, (len(para) + chars_per_line - 1) // chars_per_line)
            y_pos += lines * 13 + 4

            if y_pos > 740:
                break  # Don't overflow page

        # Footer
        page.insert_text(
            pymupdf.Point(72, 770),
            f"Page {page_idx + 1} of 75",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )
        page.insert_text(
            pymupdf.Point(400, 770),
            "DEFENSE EXHIBITS - CONFIDENTIAL",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 75')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
