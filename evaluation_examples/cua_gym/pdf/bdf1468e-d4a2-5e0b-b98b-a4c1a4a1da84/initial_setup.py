"""
Initial Setup: Create three plaintiff exhibit PDFs for trial preparation.
Task ID: pdf_legal_018
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_018'
TRIAL_DIR = f'{WORKDIR}/legal/trial'


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


def create_exhibit_1():
    """Plaintiff Exhibit 1: Employment Agreement (8 pages)."""
    doc = pymupdf.open()
    W, H = 612, 792  # Letter size

    # Page 1 - Title page
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 120), "PLAINTIFF'S EXHIBIT 1", fontsize=20, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 160), "EMPLOYMENT AGREEMENT", fontsize=16, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 200), "Between", fontsize=12, fontname="tiit", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 225), "Meridian Technologies, Inc.", fontsize=14, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 250), "and", fontsize=12, fontname="tiit", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 275), "Dr. Sarah L. Whitfield", fontsize=14, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 320), "Effective Date: March 15, 2022", fontsize=11, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 345), "Document Reference: MT-EA-2022-0347", fontsize=10, fontname="cour", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(72, 700), "CONFIDENTIAL", fontsize=10, fontname="hebo", color=(0.6, 0, 0))

    # Page 2 - Recitals and Definitions
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "RECITALS", fontsize=14, fontname="hebo", color=(0, 0, 0))
    recitals = (
        "WHEREAS, the Company is engaged in the business of developing and commercializing advanced "
        "semiconductor design software and related intellectual property;\n\n"
        "WHEREAS, Employee possesses specialized knowledge and expertise in computational lithography "
        "algorithms, EDA tool development, and semiconductor process optimization;\n\n"
        "WHEREAS, the Company desires to employ Employee as Vice President of Engineering, Advanced "
        "Design Automation Division, and Employee desires to accept such employment;\n\n"
        "NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth herein, and "
        "for other good and valuable consideration, the receipt and sufficiency of which are hereby "
        "acknowledged, the parties agree as follows:"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 400), recitals, fontsize=11, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 430), "ARTICLE I - DEFINITIONS", fontsize=13, fontname="hebo", color=(0, 0, 0))
    defs = (
        '1.1 "Affiliate" means any entity that directly or indirectly controls, is controlled by, '
        "or is under common control with the Company.\n\n"
        '1.2 "Confidential Information" means all proprietary data, trade secrets, technical know-how, '
        "business strategies, customer lists, source code, algorithms, and other non-public information "
        "belonging to the Company or its Affiliates.\n\n"
        '1.3 "Intellectual Property" means all inventions, discoveries, designs, works of authorship, '
        "software, documentation, and any other creative works."
    )
    page.insert_textbox(pymupdf.Rect(72, 455, 540, 750), defs, fontsize=10.5, fontname="tiro", color=(0, 0, 0))

    # Page 3 - Employment Terms
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "ARTICLE II - EMPLOYMENT TERMS", fontsize=13, fontname="hebo", color=(0, 0, 0))
    terms = (
        "2.1 Position and Duties. Employee shall serve as Vice President of Engineering, Advanced "
        "Design Automation Division. Employee shall report directly to the Chief Technology Officer "
        "and shall be responsible for leading a team of approximately 85 engineers.\n\n"
        "2.2 Term. The initial term of this Agreement shall commence on March 15, 2022, and shall "
        "continue for a period of three (3) years, unless earlier terminated in accordance with "
        "Article VI hereof.\n\n"
        "2.3 Location. Employee's primary work location shall be the Company's headquarters at "
        "4500 Innovation Parkway, Suite 1200, Austin, Texas 78759. Remote work arrangements may "
        "be approved at the discretion of the CTO.\n\n"
        "2.4 Exclusivity. During the term of employment, Employee shall devote substantially all "
        "of her professional time, attention, and energies to the performance of her duties. "
        "Employee shall not, without the prior written consent of the Board, engage in any other "
        "business activity that would materially interfere with Employee's obligations hereunder."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 700), terms, fontsize=11, fontname="tiro", color=(0, 0, 0))

    # Page 4 - Compensation
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "ARTICLE III - COMPENSATION AND BENEFITS", fontsize=13, fontname="hebo", color=(0, 0, 0))
    comp = (
        "3.1 Base Salary. The Company shall pay Employee an annual base salary of Four Hundred "
        "Twenty-Five Thousand Dollars ($425,000.00), payable in accordance with the Company's "
        "regular payroll schedule, subject to applicable withholdings.\n\n"
        "3.2 Annual Bonus. Employee shall be eligible for an annual performance bonus of up to "
        "forty percent (40%) of the Base Salary, based on the achievement of performance targets "
        "established by the Compensation Committee.\n\n"
        "3.3 Equity Compensation. Subject to Board approval, Employee shall receive an initial "
        "equity grant of 150,000 restricted stock units (RSUs), vesting over four (4) years with "
        "a one-year cliff.\n\n"
        "3.4 Signing Bonus. The Company shall pay Employee a one-time signing bonus of Seventy-Five "
        "Thousand Dollars ($75,000.00) within thirty (30) days of the Effective Date.\n\n"
        "3.5 Benefits. Employee shall be entitled to participate in all employee benefit plans, "
        "programs, and arrangements made available to senior executives, including medical, dental, "
        "vision, life insurance, and 401(k) retirement plan."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 700), comp, fontsize=11, fontname="tiro", color=(0, 0, 0))

    # Page 5 - IP and Non-Compete
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "ARTICLE IV - INTELLECTUAL PROPERTY", fontsize=13, fontname="hebo", color=(0, 0, 0))
    ip_text = (
        "4.1 Work Product Assignment. Employee hereby assigns and agrees to assign to the Company "
        "all right, title, and interest in and to any and all Intellectual Property conceived, "
        "developed, or reduced to practice during the term of employment.\n\n"
        "4.2 Prior Inventions. Employee has disclosed on Exhibit A attached hereto a complete list "
        "of all inventions that Employee owns or has an interest in prior to the Effective Date.\n\n"
        "4.3 Cooperation. Employee shall execute all documents and take all actions reasonably "
        "necessary to secure the Company's rights in any Intellectual Property.\n\n"
        "4.4 Non-Competition. For a period of twelve (12) months following termination, Employee "
        "shall not directly or indirectly engage in any Competing Business within North America, "
        "Europe, or the Asia-Pacific region.\n\n"
        "4.5 Non-Solicitation. For a period of eighteen (18) months following termination, Employee "
        "shall not solicit any employee, consultant, or customer of the Company."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 700), ip_text, fontsize=11, fontname="tiro", color=(0, 0, 0))

    # Page 6 - Confidentiality
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "ARTICLE V - CONFIDENTIALITY", fontsize=13, fontname="hebo", color=(0, 0, 0))
    conf = (
        "5.1 Non-Disclosure. Employee shall not, during or after the term of employment, disclose, "
        "use, or permit the use of any Confidential Information except as required in the performance "
        "of Employee's duties or as expressly authorized in writing by the Company.\n\n"
        "5.2 Return of Materials. Upon termination of employment, Employee shall promptly return "
        "all documents, records, files, notebooks, computer disks, and other materials containing "
        "or relating to Confidential Information.\n\n"
        "5.3 Injunctive Relief. Employee acknowledges that any breach of this Article V would cause "
        "irreparable harm to the Company for which monetary damages would be inadequate, and the "
        "Company shall be entitled to seek injunctive relief without the necessity of proving actual "
        "damages or posting any bond."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 600), conf, fontsize=11, fontname="tiro", color=(0, 0, 0))

    # Page 7 - Termination
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "ARTICLE VI - TERMINATION", fontsize=13, fontname="hebo", color=(0, 0, 0))
    term = (
        "6.1 Termination for Cause. The Company may terminate Employee's employment immediately "
        "for Cause, including: (a) material breach of this Agreement; (b) conviction of a felony; "
        "(c) willful misconduct causing material harm to the Company; or (d) continued failure to "
        "perform duties after written notice.\n\n"
        "6.2 Termination Without Cause. The Company may terminate Employee's employment without "
        "Cause upon thirty (30) days' written notice, subject to the severance provisions of "
        "Section 6.4.\n\n"
        "6.3 Resignation. Employee may resign upon thirty (30) days' written notice to the Company.\n\n"
        "6.4 Severance. In the event of termination without Cause, the Company shall provide "
        "Employee with: (a) twelve (12) months of continued base salary; (b) COBRA premium "
        "reimbursement for twelve (12) months; and (c) acceleration of 25% of unvested equity."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 650), term, fontsize=11, fontname="tiro", color=(0, 0, 0))

    # Page 8 - Signatures
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "ARTICLE VII - GENERAL PROVISIONS", fontsize=13, fontname="hebo", color=(0, 0, 0))
    general = (
        "7.1 Governing Law. This Agreement shall be governed by and construed in accordance with "
        "the laws of the State of Texas.\n\n"
        "7.2 Entire Agreement. This Agreement constitutes the entire agreement between the parties "
        "and supersedes all prior negotiations and agreements.\n\n"
        "7.3 Amendment. This Agreement may not be amended except by a written instrument signed "
        "by both parties."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 350), general, fontsize=11, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 400), "IN WITNESS WHEREOF, the parties have executed this Agreement.", fontsize=11, fontname="tiit", color=(0, 0, 0))
    # Signature lines
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 500), pymupdf.Point(300, 500))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.draw_line(pymupdf.Point(320, 500), pymupdf.Point(540, 500))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    page.insert_text(pymupdf.Point(72, 515), "Dr. Sarah L. Whitfield", fontsize=10, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 530), "Employee", fontsize=9, fontname="tiit", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(320, 515), "James R. Thornton, CEO", fontsize=10, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(320, 530), "Meridian Technologies, Inc.", fontsize=9, fontname="tiit", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(72, 570), "Date: March 15, 2022", fontsize=10, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(320, 570), "Date: March 15, 2022", fontsize=10, fontname="tiro", color=(0, 0, 0))

    doc.save(f'{TRIAL_DIR}/plaintiff_exhibit_1.pdf')
    doc.close()
    print(f'Created plaintiff_exhibit_1.pdf (8 pages)')


def create_exhibit_2():
    """Plaintiff Exhibit 2: Internal Communications / Email Chain (12 pages)."""
    doc = pymupdf.open()
    W, H = 612, 792

    # Page 1 - Cover
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 120), "PLAINTIFF'S EXHIBIT 2", fontsize=20, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 160), "INTERNAL COMMUNICATIONS", fontsize=16, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 200), "Email Correspondence Between Key Personnel", fontsize=12, fontname="tiit", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 240), "Date Range: June 2023 - November 2023", fontsize=11, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 265), "Bates Reference: Originally produced as MT-PROD-004521 through MT-PROD-004532", fontsize=9, fontname="cour", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(72, 700), "CONFIDENTIAL - ATTORNEYS' EYES ONLY", fontsize=10, fontname="hebo", color=(0.6, 0, 0))

    emails = [
        {
            "from": "j.thornton@meridiantech.com",
            "to": "s.whitfield@meridiantech.com",
            "cc": "m.chen@meridiantech.com",
            "date": "June 14, 2023, 9:47 AM CDT",
            "subject": "RE: Q2 Milestone Review - Design Automation Division",
            "body": (
                "Sarah,\n\nI reviewed the Q2 milestone report and I'm concerned about the timeline "
                "for Project Helios. The board is expecting a demo-ready prototype by September 30. "
                "Can you provide an updated resource allocation plan by end of week?\n\n"
                "Also, I noticed the computational lithography module is behind by approximately "
                "six weeks. What are the primary bottlenecks? Do we need to bring in additional "
                "contractors from the Bangalore team?\n\n"
                "Let's schedule a call for Thursday to discuss. Please include David Park from "
                "the product team.\n\nBest regards,\nJames"
            ),
        },
        {
            "from": "s.whitfield@meridiantech.com",
            "to": "j.thornton@meridiantech.com",
            "cc": "m.chen@meridiantech.com, d.park@meridiantech.com",
            "date": "June 14, 2023, 2:23 PM CDT",
            "subject": "RE: Q2 Milestone Review - Design Automation Division",
            "body": (
                "James,\n\nThank you for the heads up on the board expectations. I want to be "
                "transparent about the current situation:\n\n"
                "1. The lithography module delay is primarily due to the unexpected complexity "
                "in the multi-patterning optimization algorithm. Our initial estimates did not "
                "account for the new EUV constraints from TSMC's N3E process node.\n\n"
                "2. I've already reallocated three senior engineers from the DRC team to Helios. "
                "However, I must flag that this has created a staffing gap that could impact our "
                "Q3 DRC deliverables to Samsung.\n\n"
                "3. Regarding contractors - I would strongly recommend against it at this stage. "
                "The IP sensitivity of the Helios algorithms makes onboarding external resources "
                "risky. I've documented my concerns in the attached risk assessment.\n\n"
                "Thursday works. I'll send a calendar invite for 2 PM.\n\nSarah"
            ),
        },
        {
            "from": "j.thornton@meridiantech.com",
            "to": "s.whitfield@meridiantech.com",
            "date": "July 8, 2023, 11:15 AM CDT",
            "subject": "URGENT: Board Presentation Materials Needed",
            "body": (
                "Sarah,\n\nThe board meeting has been moved up to July 18. I need the following "
                "from your division by July 14:\n\n"
                "- Updated Helios timeline with revised milestones\n"
                "- Budget variance report for Q2\n"
                "- Headcount justification for the proposed 12 new hires\n"
                "- Technical risk assessment for the Samsung DRC gap\n\n"
                "I know this is tight, but the investors are getting nervous about our R&D burn "
                "rate. We need to show strong execution.\n\nJames"
            ),
        },
        {
            "from": "s.whitfield@meridiantech.com",
            "to": "j.thornton@meridiantech.com",
            "date": "July 9, 2023, 8:02 AM CDT",
            "subject": "RE: URGENT: Board Presentation Materials Needed",
            "body": (
                "James,\n\nUnderstood. My team will have everything ready by EOD July 13. "
                "However, I want to go on record that presenting the Helios timeline without "
                "the caveats I outlined in my June 28 memo would be misleading to the board.\n\n"
                "The September 30 demo date is achievable ONLY if we maintain current staffing "
                "levels and do not divert any more resources to the emergency patches for the "
                "v4.2 release. If marketing continues to promise features we haven't scoped, "
                "something will have to give.\n\n"
                "I'd like to present to the board directly on the technical risks. Can you "
                "allocate 15 minutes for me in the agenda?\n\nSarah"
            ),
        },
        {
            "from": "m.chen@meridiantech.com",
            "to": "s.whitfield@meridiantech.com",
            "date": "August 22, 2023, 4:56 PM CDT",
            "subject": "FW: Customer Escalation - GlobalFoundries Integration Issue",
            "body": (
                "Sarah,\n\nForwarding this from the support team. GlobalFoundries is reporting "
                "critical failures in the OPC module when processing their 12nm FinFET designs. "
                "They've threatened to withhold the Q3 license renewal ($2.8M annual contract) "
                "unless we resolve this within two weeks.\n\n"
                "I've done initial triage - it appears to be related to the refactoring work "
                "we did in Sprint 47. The regression tests passed, but they didn't cover GF's "
                "specific process corner cases.\n\n"
                "Recommended action: Pull Marcus Rivera and two engineers from Helios to form "
                "a tiger team. Estimated fix time: 8-10 business days.\n\n"
                "I know this impacts the September demo, but losing GF would be devastating.\n\n"
                "Michael Chen\nSenior Director, Engineering"
            ),
        },
        {
            "from": "s.whitfield@meridiantech.com",
            "to": "m.chen@meridiantech.com",
            "cc": "j.thornton@meridiantech.com",
            "date": "August 22, 2023, 6:31 PM CDT",
            "subject": "RE: FW: Customer Escalation - GlobalFoundries Integration Issue",
            "body": (
                "Michael,\n\nApproved. Pull Marcus and assign Priya Kapoor and Tom Zhang to the "
                "tiger team. This is exactly the scenario I warned about in my July 9 email to "
                "James.\n\n"
                "James - please note that this GF escalation will push the Helios demo to "
                "no earlier than October 15. I've attached an updated Gantt chart. The board "
                "needs to understand that we cannot simultaneously fight fires and build new "
                "products with the same engineers.\n\n"
                "I'm requesting an emergency budget allocation of $340,000 for temporary "
                "contractor support to backfill the Helios positions. Without it, we're looking "
                "at November at the earliest.\n\nSarah"
            ),
        },
        {
            "from": "j.thornton@meridiantech.com",
            "to": "s.whitfield@meridiantech.com",
            "date": "September 5, 2023, 10:18 AM CDT",
            "subject": "RE: Helios Timeline and Resource Request",
            "body": (
                "Sarah,\n\nI've discussed the contractor budget with the CFO. The request is "
                "denied. We need to find a way to deliver Helios on the original timeline "
                "without additional spending.\n\n"
                "I understand the challenges, but the board has made it clear that the September "
                "target is a commitment, not a guideline. Please find a way to make it work.\n\n"
                "Also, going forward, please loop in HR before making any team reassignments "
                "above 2 FTEs. We need to maintain proper governance.\n\nJames"
            ),
        },
        {
            "from": "s.whitfield@meridiantech.com",
            "to": "j.thornton@meridiantech.com",
            "date": "September 5, 2023, 3:44 PM CDT",
            "subject": "RE: Helios Timeline and Resource Request",
            "body": (
                "James,\n\nI must be direct: maintaining the September timeline without additional "
                "resources is not feasible. I've run the numbers three different ways and every "
                "scenario shows a minimum 3-week overrun.\n\n"
                "Forcing the team to crunch will result in technical debt, increased defect rates, "
                "and potential burnout of key personnel. We've already lost two senior engineers "
                "this quarter to competitors offering better work-life balance.\n\n"
                "I'm willing to present a compressed plan that delivers a limited demo by "
                "September 30 (core lithography features only, without the full DFM integration), "
                "with the complete deliverable by October 22. This is the most aggressive "
                "realistic timeline I can offer.\n\n"
                "If the board requires the full demo by September 30, I need the contractor "
                "budget or a written acknowledgment that the quality standards are being "
                "deliberately relaxed.\n\nSarah"
            ),
        },
        {
            "from": "j.thornton@meridiantech.com",
            "to": "s.whitfield@meridiantech.com",
            "date": "November 2, 2023, 8:30 AM CDT",
            "subject": "Performance Review Discussion - Confidential",
            "body": (
                "Sarah,\n\nI'd like to schedule a meeting to discuss your mid-year performance "
                "review. Please keep November 8 at 10 AM open.\n\n"
                "As you know, the Helios project missed its demo deadline and the board expressed "
                "significant displeasure at the October meeting. While I understand the technical "
                "challenges, leadership accountability is an area we need to address.\n\n"
                "Please prepare a self-assessment document covering:\n"
                "- Key achievements in 2023\n"
                "- Areas for improvement\n"
                "- 2024 goals and commitments\n\n"
                "James"
            ),
        },
        {
            "from": "s.whitfield@meridiantech.com",
            "to": "personal.swhitfield@gmail.com",
            "date": "November 2, 2023, 9:15 PM CDT",
            "subject": "FW: Performance Review Discussion - Confidential",
            "body": (
                "Forwarding for my records. They're setting up the narrative to blame me for "
                "the Helios delays. I predicted every single issue months in advance and was "
                "denied the resources to address them.\n\n"
                "Meeting with attorney Rebecca Torres on Monday to discuss options. Preserving "
                "all email records per her advice.\n\n"
                "Also saved copies of the June 28 risk memo, the July 9 email, and the "
                "September 5 exchange. These clearly show I flagged the timeline risks "
                "repeatedly and was overridden.\n\n- S"
            ),
        },
    ]

    # Create email pages (pages 2-12, with some emails spanning continuation)
    email_idx = 0
    for pg_num in range(1, 12):
        page = doc.new_page(width=W, height=H)
        y_pos = 72

        # Header
        page.insert_text(pymupdf.Point(72, y_pos), f"Internal Communications - Page {pg_num}", fontsize=9, fontname="cour", color=(0.5, 0.5, 0.5))
        y_pos += 30

        while email_idx < len(emails) and y_pos < 600:
            email = emails[email_idx]
            # Draw separator
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, y_pos), pymupdf.Point(540, y_pos))
            shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
            shape.commit()
            y_pos += 15

            page.insert_text(pymupdf.Point(72, y_pos), f"From: {email['from']}", fontsize=9, fontname="cobo", color=(0, 0, 0))
            y_pos += 14
            page.insert_text(pymupdf.Point(72, y_pos), f"To: {email['to']}", fontsize=9, fontname="cour", color=(0, 0, 0))
            y_pos += 14
            if 'cc' in email:
                page.insert_text(pymupdf.Point(72, y_pos), f"Cc: {email['cc']}", fontsize=9, fontname="cour", color=(0, 0, 0))
                y_pos += 14
            page.insert_text(pymupdf.Point(72, y_pos), f"Date: {email['date']}", fontsize=9, fontname="cour", color=(0, 0, 0))
            y_pos += 14
            page.insert_text(pymupdf.Point(72, y_pos), f"Subject: {email['subject']}", fontsize=9, fontname="cobo", color=(0, 0, 0.5))
            y_pos += 20

            body_rect = pymupdf.Rect(72, y_pos, 540, 740)
            excess = page.insert_textbox(body_rect, email['body'], fontsize=9.5, fontname="tiro", color=(0, 0, 0))
            if excess < 0:
                # Text didn't all fit, estimate used height
                y_pos = 745
            else:
                # Approximate how much vertical space was used
                lines = email['body'].count('\n') + len(email['body']) // 65
                y_pos += min(lines * 12, 680)

            email_idx += 1
            y_pos += 20

    doc.save(f'{TRIAL_DIR}/plaintiff_exhibit_2.pdf')
    doc.close()
    print(f'Created plaintiff_exhibit_2.pdf (12 pages)')


def create_exhibit_3():
    """Plaintiff Exhibit 3: Performance Metrics Report (5 pages)."""
    doc = pymupdf.open()
    W, H = 612, 792

    # Page 1 - Cover
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 120), "PLAINTIFF'S EXHIBIT 3", fontsize=20, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 160), "PERFORMANCE METRICS REPORT", fontsize=16, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 200), "Advanced Design Automation Division", fontsize=13, fontname="tiro", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(72, 225), "Fiscal Year 2023 - Quarters 1 through 3", fontsize=12, fontname="tiro", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(72, 265), "Prepared by: Office of the Chief Technology Officer", fontsize=10, fontname="tiit", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(72, 285), "Distribution: Board of Directors, Executive Committee", fontsize=10, fontname="tiit", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(72, 305), "Classification: CONFIDENTIAL - INTERNAL USE ONLY", fontsize=10, fontname="hebo", color=(0.6, 0, 0))

    # Page 2 - Division Overview
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "1. DIVISION OVERVIEW", fontsize=14, fontname="hebo", color=(0, 0, 0))
    overview = (
        "The Advanced Design Automation Division (ADAD) is responsible for the development and "
        "maintenance of Meridian Technologies' core EDA product suite, including the Helios "
        "computational lithography platform, DRC verification tools, and OPC optimization engines.\n\n"
        "Under the leadership of VP Engineering Dr. Sarah Whitfield, the division has grown from "
        "72 to 85 engineers during FY2023, representing an 18% headcount increase. Key accomplishments "
        "include:\n\n"
        "  - Successful deployment of v4.1 to 14 enterprise customers\n"
        "  - Patent filings: 7 new applications (4 granted)\n"
        "  - Customer satisfaction score: 4.2/5.0 (industry avg: 3.7)\n"
        "  - Revenue attribution: $47.3M (32% of company total)\n"
        "  - Employee retention rate: 89% (down from 94% in FY2022)"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 450), overview, fontsize=11, fontname="tiro", color=(0, 0, 0))

    page.insert_text(pymupdf.Point(72, 470), "2. PROJECT STATUS SUMMARY", fontsize=14, fontname="hebo", color=(0, 0, 0))
    # Simple table using text
    headers = f"{'Project':<20}{'Status':<15}{'Schedule':<15}{'Budget':<12}{'Risk':<10}"
    page.insert_text(pymupdf.Point(72, 500), headers, fontsize=9, fontname="cobo", color=(0, 0, 0))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 505), pymupdf.Point(540, 505))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    projects = [
        ("Helios v1.0", "In Progress", "6 wks behind", "$12.4M", "HIGH"),
        ("DRC Suite v4.2", "In Progress", "On track", "$5.1M", "MEDIUM"),
        ("OPC Engine v3.5", "Complete", "2 wks early", "$3.8M", "LOW"),
        ("Samsung Custom", "In Progress", "3 wks behind", "$8.2M", "HIGH"),
        ("GF Integration", "Escalated", "Critical", "$2.1M", "CRITICAL"),
    ]
    y = 520
    for proj in projects:
        line = f"{proj[0]:<20}{proj[1]:<15}{proj[2]:<15}{proj[3]:<12}{proj[4]:<10}"
        page.insert_text(pymupdf.Point(72, y), line, fontsize=9, fontname="cour", color=(0, 0, 0))
        y += 14

    # Page 3 - Budget Analysis
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "3. BUDGET ANALYSIS", fontsize=14, fontname="hebo", color=(0, 0, 0))
    budget = (
        "Total Division Budget (FY2023): $31,600,000\n"
        "YTD Expenditure (through Q3): $25,847,000 (81.8% of annual budget)\n"
        "Projected Year-End Spend: $33,200,000 (105.1% - OVER BUDGET)\n\n"
        "Budget Variance Drivers:\n\n"
        "  1. Unplanned contractor costs for GF escalation: +$340,000\n"
        "  2. Additional cloud compute for Helios testing: +$285,000\n"
        "  3. Recruiting costs for 13 new hires (vs. 8 planned): +$195,000\n"
        "  4. Emergency license renewal for 3rd-party IP blocks: +$480,000\n"
        "  5. Conference and training (under budget): -$120,000\n"
        "  6. Travel reduction due to remote meetings: -$85,000\n\n"
        "Net Projected Overrun: $1,600,000 (5.1%)\n\n"
        "Note: VP Whitfield submitted a budget amendment request on August 22, 2023, which was "
        "denied by the CFO on September 5, 2023. The denial memo cited 'company-wide cost "
        "containment measures' as the primary reason."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 650), budget, fontsize=10.5, fontname="tiro", color=(0, 0, 0))

    # Page 4 - Timeline Analysis
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "4. HELIOS PROJECT TIMELINE ANALYSIS", fontsize=14, fontname="hebo", color=(0, 0, 0))
    timeline = (
        "Original Board-Approved Timeline:\n"
        "  - Phase 1 (Core Engine): Jan 2023 - Apr 2023 [COMPLETED - on time]\n"
        "  - Phase 2 (Lithography Module): May 2023 - Jul 2023 [COMPLETED - 3 weeks late]\n"
        "  - Phase 3 (DFM Integration): Aug 2023 - Sep 2023 [IN PROGRESS - delayed]\n"
        "  - Phase 4 (Demo/Beta): Sep 30, 2023 [MISSED]\n\n"
        "Key Delay Events:\n\n"
        "  June 14: VP Whitfield flagged EUV constraint complexity (est. +3 weeks)\n"
        "  July 9: VP Whitfield requested board presentation time to explain risks\n"
        "  August 22: GF escalation diverted 3 engineers from Helios\n"
        "  September 5: Contractor budget request denied by CFO\n"
        "  September 30: Original demo deadline missed\n"
        "  October 15: Limited demo delivered (core features only)\n"
        "  October 22: Revised full demo target\n\n"
        "Assessment: The project delays were primarily caused by (1) underestimation of technical "
        "complexity in the initial planning phase, (2) unplanned resource diversions to handle "
        "customer escalations, and (3) denial of requested supplementary resources. VP Whitfield's "
        "engineering team executed at a high level given the constraints."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 680), timeline, fontsize=10.5, fontname="tiro", color=(0, 0, 0))

    # Page 5 - Team Performance
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "5. TEAM PERFORMANCE METRICS", fontsize=14, fontname="hebo", color=(0, 0, 0))
    team = (
        "Engineering Velocity (Story Points per Sprint):\n"
        "  Q1 Average: 127 pts/sprint (target: 120) - EXCEEDS\n"
        "  Q2 Average: 134 pts/sprint (target: 125) - EXCEEDS\n"
        "  Q3 Average: 118 pts/sprint (target: 130) - BELOW (due to GF diversion)\n\n"
        "Code Quality Metrics:\n"
        "  Defect Density: 0.23 defects/KLOC (industry avg: 0.45)\n"
        "  Code Review Coverage: 98.7%\n"
        "  Unit Test Coverage: 91.2%\n"
        "  CI/CD Pipeline Success Rate: 96.4%\n\n"
        "Employee Satisfaction (Anonymous Survey - September 2023):\n"
        "  Overall Satisfaction: 3.8/5.0 (down from 4.3 in March)\n"
        "  Work-Life Balance: 2.9/5.0 (significant concern)\n"
        "  Leadership Support: 4.4/5.0\n"
        "  Career Growth: 4.1/5.0\n"
        "  Resource Adequacy: 2.4/5.0 (critical concern)\n\n"
        "Attrition Analysis:\n"
        "  Departures YTD: 9 engineers (7 voluntary, 2 involuntary)\n"
        "  Exit Interview Theme: 78% cited 'unsustainable workload' as primary factor\n"
        "  Key Loss: Dr. Raj Patel (Principal Engineer, lithography lead) to Synopsys, August 2023"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 700), team, fontsize=10.5, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 720), "END OF REPORT", fontsize=10, fontname="hebo", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(72, 740), "Prepared: October 28, 2023 | Distribution restricted per NDA-2023-0891", fontsize=8, fontname="cour", color=(0.5, 0.5, 0.5))

    doc.save(f'{TRIAL_DIR}/plaintiff_exhibit_3.pdf')
    doc.close()
    print(f'Created plaintiff_exhibit_3.pdf (5 pages)')


def main():
    # Create directory structure
    os.makedirs(TRIAL_DIR, exist_ok=True)

    # Create exhibits
    create_exhibit_1()
    create_exhibit_2()
    create_exhibit_3()

    # Verify page counts
    for name, expected in [('plaintiff_exhibit_1.pdf', 8), ('plaintiff_exhibit_2.pdf', 12), ('plaintiff_exhibit_3.pdf', 5)]:
        doc = pymupdf.open(f'{TRIAL_DIR}/{name}')
        actual = doc.page_count
        doc.close()
        print(f'  {name}: {actual} pages (expected {expected})')
        assert actual == expected, f"Page count mismatch for {name}: got {actual}, expected {expected}"

    # Open exhibit 1 in Evince for GUI-ready state
    launch_gui(f'evince "{TRIAL_DIR}/plaintiff_exhibit_1.pdf"', delay_sec=2.0)
    print('GUI_READY: launched Evince with exhibit 1')


main()
