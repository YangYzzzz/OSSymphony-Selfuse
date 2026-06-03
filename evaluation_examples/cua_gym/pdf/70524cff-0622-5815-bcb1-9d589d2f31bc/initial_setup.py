"""
Initial Setup: Create a 45-page deposition exhibits bundle PDF
Task ID: pdf_legal_044
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
TASK_ID = 'pdf_legal_044'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/depo_exhibits.pdf'

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


def add_page_header(page, exhibit_num, page_in_exhibit, total_in_exhibit):
    """Add a standard legal header/footer to each page."""
    # Header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(54, 50), pymupdf.Point(558, 50))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()

    page.insert_text(
        pymupdf.Point(54, 44),
        f"DEPOSITION EXHIBITS - CASE NO. 2025-CV-03891",
        fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4),
    )

    # Footer
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(54, 748), pymupdf.Point(558, 748))
    shape2.finish(color=(0, 0, 0), width=0.5)
    shape2.commit()

    page.insert_text(
        pymupdf.Point(54, 766),
        f"Exhibit {exhibit_num} - Page {page_in_exhibit} of {total_in_exhibit}",
        fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4),
    )
    page.insert_text(
        pymupdf.Point(460, 766),
        "CONFIDENTIAL",
        fontsize=8, fontname="hebo", color=(0.6, 0, 0),
    )


def create_exhibit_1(doc):
    """Exhibit 1: Employment Agreement (pages 1-10)"""
    # Page 1 - Cover/Title
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    add_page_header(page, 1, 1, 10)
    page.insert_text(pymupdf.Point(180, 120), "EMPLOYMENT AGREEMENT", fontsize=18, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(200, 150), "Between Meridian Technologies, Inc.", fontsize=12, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(260, 170), "and Sarah K. Whitfield", fontsize=12, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(240, 200), "Effective Date: March 15, 2024", fontsize=11, fontname="heit", color=(0, 0, 0))

    agreement_text = (
        "This Employment Agreement ('Agreement') is entered into as of March 15, 2024, by and between "
        "Meridian Technologies, Inc., a Delaware corporation with its principal place of business at "
        "4500 Innovation Drive, Suite 800, San Jose, California 95134 ('Company'), and Sarah K. Whitfield, "
        "an individual residing at 2718 Elm Street, Palo Alto, California 94301 ('Employee').\n\n"
        "RECITALS\n\n"
        "WHEREAS, the Company desires to employ Employee as Vice President of Product Development, "
        "and Employee desires to be employed by the Company in such capacity, subject to the terms "
        "and conditions set forth herein;\n\n"
        "WHEREAS, Employee possesses specialized knowledge, skills, and experience in software product "
        "management and development that are valuable to the Company;\n\n"
        "NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth below, and "
        "for other good and valuable consideration, the receipt and sufficiency of which are hereby "
        "acknowledged, the parties agree as follows:"
    )
    rect = pymupdf.Rect(54, 240, 558, 720)
    page.insert_textbox(rect, agreement_text, fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Pages 2-10 - Agreement body
    sections = [
        ("1. POSITION AND DUTIES", [
            "1.1 Position. The Company hereby employs Employee as Vice President of Product Development, "
            "reporting directly to the Chief Technology Officer, Dr. James R. Harrington.",
            "1.2 Duties. Employee shall perform such duties and responsibilities as are customarily associated "
            "with the position of Vice President of Product Development, including but not limited to: "
            "(a) overseeing product roadmap development; (b) managing a team of approximately forty-five (45) "
            "product managers and designers; (c) coordinating with engineering leadership on feature prioritization; "
            "(d) presenting product strategy to the Board of Directors on a quarterly basis.",
            "1.3 Best Efforts. Employee shall devote her full business time, attention, skill, and best efforts "
            "to the performance of her duties hereunder.",
            "1.4 Location. Employee's primary work location shall be the Company's San Jose headquarters, with "
            "the option to work remotely up to two (2) days per week.",
        ]),
        ("2. COMPENSATION AND BENEFITS", [
            "2.1 Base Salary. The Company shall pay Employee an annual base salary of Three Hundred Twenty-Five "
            "Thousand Dollars ($325,000.00), payable in accordance with the Company's standard payroll practices.",
            "2.2 Annual Bonus. Employee shall be eligible for an annual performance bonus of up to forty percent "
            "(40%) of her base salary, based on achievement of mutually agreed-upon performance objectives.",
            "2.3 Equity Compensation. Subject to approval by the Board of Directors, Employee shall be granted "
            "an initial stock option to purchase 150,000 shares of the Company's common stock at the fair market "
            "value on the date of grant, vesting over four (4) years with a one-year cliff.",
            "2.4 Benefits. Employee shall be entitled to participate in all employee benefit plans and programs "
            "made available to similarly situated senior executives, including health insurance, dental and vision "
            "coverage, 401(k) retirement plan with company match up to 6%, and life insurance.",
        ]),
        ("3. TERM AND TERMINATION", [
            "3.1 Term. This Agreement shall commence on the Effective Date and shall continue until terminated "
            "by either party as provided herein.",
            "3.2 Termination Without Cause. The Company may terminate Employee's employment without Cause upon "
            "thirty (30) days' prior written notice. In such event, Employee shall be entitled to twelve (12) "
            "months of base salary continuation and COBRA premium subsidies.",
            "3.3 Termination for Cause. The Company may terminate Employee's employment for Cause, as defined "
            "in Section 3.5, immediately upon written notice. Employee shall not be entitled to severance.",
            "3.4 Resignation. Employee may resign upon thirty (30) days' prior written notice to the Company.",
            "3.5 Definition of Cause. For purposes of this Agreement, 'Cause' shall mean: (a) conviction of a "
            "felony; (b) material breach of this Agreement; (c) willful misconduct or gross negligence in "
            "performance of duties; (d) fraud or dishonesty materially affecting the Company.",
        ]),
        ("4. CONFIDENTIALITY AND NON-COMPETE", [
            "4.1 Confidential Information. Employee acknowledges that during the course of employment, she will "
            "have access to and become acquainted with confidential and proprietary information belonging to the "
            "Company, including but not limited to: trade secrets, customer lists, pricing strategies, product "
            "development plans, financial data, and marketing strategies.",
            "4.2 Non-Disclosure. Employee agrees not to disclose, publish, or make use of any Confidential "
            "Information at any time during or after her employment, except as required in the performance of "
            "her duties or as authorized in writing by the Company.",
            "4.3 Non-Competition. For a period of twelve (12) months following termination of employment, "
            "Employee shall not directly or indirectly engage in any business that competes with the Company's "
            "core product lines within the United States.",
            "4.4 Non-Solicitation. For a period of eighteen (18) months following termination, Employee shall "
            "not solicit any employee, consultant, or contractor of the Company to leave their engagement.",
        ]),
        ("5. INTELLECTUAL PROPERTY", [
            "5.1 Work Product Assignment. Employee hereby assigns to the Company all right, title, and interest "
            "in any inventions, developments, improvements, or discoveries made during the course of employment.",
            "5.2 Prior Inventions. Employee has disclosed to the Company all prior inventions listed in Appendix A.",
            "5.3 Cooperation. Employee agrees to execute any documents and take any actions reasonably requested "
            "by the Company to perfect its ownership rights in Work Product.",
        ]),
        ("6. GENERAL PROVISIONS", [
            "6.1 Governing Law. This Agreement shall be governed by the laws of the State of California.",
            "6.2 Entire Agreement. This Agreement constitutes the entire agreement between the parties and "
            "supersedes all prior agreements, understandings, and negotiations.",
            "6.3 Amendment. This Agreement may not be amended except by a written instrument signed by both parties.",
            "6.4 Severability. If any provision of this Agreement is held invalid, the remaining provisions "
            "shall continue in full force and effect.",
            "6.5 Notices. All notices under this Agreement shall be in writing and delivered to the addresses "
            "listed in the preamble.",
            "\n\nIN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.\n\n"
            "MERIDIAN TECHNOLOGIES, INC.\n\n"
            "By: ________________________________\n"
            "    Robert A. Chen, Chief Executive Officer\n"
            "    Date: March 15, 2024\n\n"
            "EMPLOYEE\n\n"
            "________________________________\n"
            "Sarah K. Whitfield\n"
            "Date: March 15, 2024",
        ]),
    ]

    # Distribute sections across pages 2-10
    current_section_idx = 0
    for pg_num in range(2, 11):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        add_page_header(page, 1, pg_num, 10)
        y_pos = 72
        while current_section_idx < len(sections) and y_pos < 700:
            title, paragraphs = sections[current_section_idx]
            page.insert_text(pymupdf.Point(54, y_pos), title, fontsize=12, fontname="hebo", color=(0, 0, 0))
            y_pos += 20
            for para in paragraphs:
                rect = pymupdf.Rect(54, y_pos, 558, y_pos + 120)
                excess = page.insert_textbox(rect, para, fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
                # Estimate lines used
                lines_approx = max(1, len(para) // 80)
                y_pos += min(120, lines_approx * 14 + 10)
                if y_pos >= 700:
                    break
            if y_pos < 700:
                current_section_idx += 1
                y_pos += 15


def create_exhibit_2(doc):
    """Exhibit 2: Email Correspondence (pages 11-25)"""
    emails = [
        {
            "from": "j.harrington@meridiantech.com",
            "to": "s.whitfield@meridiantech.com",
            "date": "April 2, 2024, 9:15 AM",
            "subject": "Re: Q2 Product Roadmap Review",
            "body": (
                "Sarah,\n\nThanks for the updated roadmap presentation. I've reviewed it with the executive "
                "team and we have a few concerns about the timeline for Project Horizon. The board is expecting "
                "a demo at the June meeting, and the current schedule shows completion in late July.\n\n"
                "Can we discuss pulling in the Phase 2 deliverables? I think if we reallocate resources from "
                "the legacy migration project, we can make the June deadline.\n\n"
                "Also, please schedule a meeting with the engineering leads for this Thursday.\n\n"
                "Best,\nJames"
            ),
        },
        {
            "from": "s.whitfield@meridiantech.com",
            "to": "j.harrington@meridiantech.com",
            "cc": "m.torres@meridiantech.com, a.patel@meridiantech.com",
            "date": "April 2, 2024, 11:42 AM",
            "subject": "Re: Re: Q2 Product Roadmap Review",
            "body": (
                "James,\n\nI understand the pressure from the board. However, I want to flag some risks with "
                "accelerating the Horizon timeline:\n\n"
                "1. The integration testing phase cannot be compressed without significant quality risk.\n"
                "2. Pulling engineers from the legacy migration will delay the security patches that compliance "
                "has flagged as critical.\n"
                "3. The UX research for the new onboarding flow isn't complete yet.\n\n"
                "I propose a compromise: we deliver a limited demo for the June board meeting showing the "
                "core workflow, while keeping the full release on the July schedule. This way we can show "
                "progress without cutting corners on quality.\n\n"
                "I've already reached out to Marcus Torres and Anita Patel to set up Thursday's meeting. "
                "Time is 2:00 PM in Conference Room B.\n\n"
                "Best,\nSarah"
            ),
        },
        {
            "from": "m.torres@meridiantech.com",
            "to": "s.whitfield@meridiantech.com",
            "date": "April 3, 2024, 3:28 PM",
            "subject": "Engineering Resource Allocation - Confidential",
            "body": (
                "Sarah,\n\nHeads up - I just got word from HR that two of my senior engineers on the Horizon "
                "team (David Kim and Lisa Chen) have submitted their resignations, effective April 30. They're "
                "both moving to Vertex Labs.\n\n"
                "This puts us in a really difficult position with the accelerated timeline. We'd need to "
                "backfill immediately, and even then, new hires won't be productive for at least 6-8 weeks.\n\n"
                "I wanted to tell you before the Thursday meeting so we can present a unified front. I think "
                "we need to have an honest conversation with James about what's realistic.\n\n"
                "Marcus"
            ),
        },
        {
            "from": "s.whitfield@meridiantech.com",
            "to": "legal@meridiantech.com",
            "date": "April 5, 2024, 8:05 AM",
            "subject": "Review Request: Non-Compete Enforcement",
            "body": (
                "Dear Legal Team,\n\nI need an urgent review of the non-compete clauses in the employment "
                "agreements for David Kim and Lisa Chen. Both are senior engineers on Project Horizon who have "
                "given notice and plan to join Vertex Labs, one of our direct competitors.\n\n"
                "Given the sensitive nature of the technology they've been working on, I'm concerned about "
                "potential IP exposure. Please advise on:\n\n"
                "1. Enforceability of their non-compete clauses under California law\n"
                "2. Options for protecting our trade secrets\n"
                "3. Recommended exit interview protocols\n\n"
                "This is time-sensitive as their last day is April 30.\n\n"
                "Thank you,\nSarah Whitfield\nVP, Product Development"
            ),
        },
        {
            "from": "r.chen@meridiantech.com",
            "to": "s.whitfield@meridiantech.com",
            "date": "April 8, 2024, 4:30 PM",
            "subject": "Board Meeting Preparation",
            "body": (
                "Sarah,\n\nI've been briefed on the engineering departures. This is obviously concerning, "
                "but I don't want to panic the board. For the upcoming presentation, please prepare:\n\n"
                "1. Updated project timeline with risk factors clearly identified\n"
                "2. Mitigation plan for the staffing gaps\n"
                "3. Competitive analysis showing our position vs. Vertex Labs\n"
                "4. Budget request for expedited recruiting\n\n"
                "Let's meet tomorrow at 8:30 AM to review before I send materials to the board.\n\n"
                "Robert"
            ),
        },
    ]

    for pg_num in range(15):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        add_page_header(page, 2, pg_num + 1, 15)

        email_idx = pg_num // 3
        if email_idx < len(emails):
            email = emails[email_idx]
            sub_page = pg_num % 3

            if sub_page == 0:
                y = 72
                # Email header block
                page.insert_text(pymupdf.Point(54, y), f"From: {email['from']}", fontsize=10, fontname="hebo", color=(0, 0, 0))
                y += 16
                page.insert_text(pymupdf.Point(54, y), f"To: {email['to']}", fontsize=10, fontname="helv", color=(0, 0, 0))
                y += 16
                if 'cc' in email:
                    page.insert_text(pymupdf.Point(54, y), f"Cc: {email['cc']}", fontsize=10, fontname="helv", color=(0, 0, 0))
                    y += 16
                page.insert_text(pymupdf.Point(54, y), f"Date: {email['date']}", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
                y += 16
                page.insert_text(pymupdf.Point(54, y), f"Subject: {email['subject']}", fontsize=10, fontname="hebo", color=(0, 0, 0))
                y += 8

                # Separator line
                shape = page.new_shape()
                shape.draw_line(pymupdf.Point(54, y), pymupdf.Point(558, y))
                shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
                shape.commit()
                y += 14

                # Body
                rect = pymupdf.Rect(54, y, 558, 720)
                page.insert_textbox(rect, email['body'], fontsize=10, fontname="tiro", color=(0, 0, 0))
            else:
                # Continuation pages with additional context text
                continuation_texts = [
                    "--- Thread continues ---\n\nAdditional attachments and forwarded correspondence related to "
                    "the above email chain are preserved in this section for reference. Document metadata and "
                    "timestamps have been verified against the company email server logs.\n\n"
                    "Note: This email was flagged for legal hold on April 10, 2024 as part of the internal "
                    "investigation into the departure of key engineering personnel and potential trade secret "
                    "misappropriation concerns.",
                    "This page intentionally contains supplementary notes and annotations added during the "
                    "document review process conducted by Morrison & Foerster LLP on behalf of Meridian "
                    "Technologies, Inc.\n\n"
                    "Review Status: PRIVILEGED AND CONFIDENTIAL\n"
                    "Attorney Work Product\n"
                    "Reviewed by: Associate Jennifer Walsh, Esq.\n"
                    f"Review Date: May {12 + pg_num}, 2024",
                ]
                text = continuation_texts[sub_page - 1] if sub_page - 1 < len(continuation_texts) else "Page reserved for additional correspondence."
                rect = pymupdf.Rect(54, 72, 558, 720)
                page.insert_textbox(rect, text, fontsize=10, fontname="tiro", color=(0, 0, 0))
        else:
            # Additional correspondence pages
            rect = pymupdf.Rect(54, 72, 558, 720)
            filler_text = (
                f"SUPPLEMENTAL CORRESPONDENCE - PAGE {pg_num + 1}\n\n"
                "This page contains additional email correspondence and internal memoranda related to the "
                "departures of David Kim and Lisa Chen from Meridian Technologies, Inc. The documents were "
                "produced in response to discovery requests served on April 22, 2024.\n\n"
                "All documents on this page have been reviewed for privilege by outside counsel and have been "
                "designated as non-privileged and responsive to Request for Production No. 14.\n\n"
                "Bates Number Range: MERIDIAN-00" + str(1200 + pg_num * 3).zfill(4) + " through MERIDIAN-00" + str(1202 + pg_num * 3).zfill(4)
            )
            page.insert_textbox(rect, filler_text, fontsize=10, fontname="tiro", color=(0, 0, 0))


def create_exhibit_3(doc):
    """Exhibit 3: Financial Records (pages 26-34)"""
    # Page 1 - Financial Summary Title
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    add_page_header(page, 3, 1, 9)
    page.insert_text(pymupdf.Point(150, 100), "MERIDIAN TECHNOLOGIES, INC.", fontsize=16, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(170, 125), "Quarterly Financial Summary - FY2024", fontsize=13, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(200, 150), "Prepared by: CFO Office", fontsize=10, fontname="heit", color=(0.3, 0.3, 0.3))

    # Simple financial table
    y_start = 200
    headers = ["Category", "Q1 2024", "Q2 2024 (Proj.)", "YoY Change"]
    col_x = [54, 180, 330, 470]

    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(col_x[i], y_start), h, fontsize=10, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(54, y_start + 5), pymupdf.Point(558, y_start + 5))
    shape.finish(color=(0, 0, 0), width=0.8)
    shape.commit()

    data_rows = [
        ["Revenue", "$48,250,000", "$52,100,000", "+8.0%"],
        ["COGS", "$19,300,000", "$20,840,000", "+7.9%"],
        ["Gross Profit", "$28,950,000", "$31,260,000", "+8.0%"],
        ["R&D Expenses", "$12,400,000", "$14,200,000", "+14.5%"],
        ["S&M Expenses", "$8,750,000", "$9,100,000", "+4.0%"],
        ["G&A Expenses", "$3,200,000", "$3,350,000", "+4.7%"],
        ["Operating Income", "$4,600,000", "$4,610,000", "+0.2%"],
        ["Net Income", "$3,680,000", "$3,688,000", "+0.2%"],
        ["Headcount", "487", "512", "+5.1%"],
        ["Burn Rate", "$14.2M/mo", "$15.1M/mo", "+6.3%"],
    ]

    for r_idx, row in enumerate(data_rows):
        y = y_start + 22 + r_idx * 18
        for c_idx, val in enumerate(row):
            fname = "tiro" if c_idx == 0 else "helv"
            page.insert_text(pymupdf.Point(col_x[c_idx], y), val, fontsize=9, fontname=fname, color=(0, 0, 0))

    # Remaining pages for exhibit 3
    exhibit3_content = [
        "BALANCE SHEET SUMMARY\n\nAssets:\n  Cash and Equivalents: $78,400,000\n  Accounts Receivable: $22,150,000\n  "
        "Property & Equipment: $15,800,000\n  Intangible Assets: $34,200,000\n  Goodwill: $45,600,000\n  "
        "Total Assets: $196,150,000\n\nLiabilities:\n  Accounts Payable: $8,900,000\n  "
        "Accrued Liabilities: $12,300,000\n  Long-Term Debt: $25,000,000\n  Deferred Revenue: $18,700,000\n  "
        "Total Liabilities: $64,900,000\n\nShareholders' Equity: $131,250,000",

        "PROJECT HORIZON - BUDGET ALLOCATION\n\nApproved Budget: $18,500,000\nSpent to Date (Q1): $4,200,000\n"
        "Remaining: $14,300,000\n\nBreakdown by Category:\n  Engineering Salaries: $8,200,000\n  "
        "Cloud Infrastructure: $3,400,000\n  Third-Party Licenses: $1,800,000\n  QA & Testing: $2,100,000\n  "
        "Contingency: $3,000,000\n\nBudget Risk: HIGH\nReason: Departure of senior engineers requires "
        "expedited recruiting at premium rates. Estimated additional cost: $1,200,000 - $1,800,000 for "
        "recruitment fees and signing bonuses.",

        "COMPENSATION ANALYSIS - VP LEVEL AND ABOVE\n\n"
        "Sarah K. Whitfield, VP Product Development:\n  Base: $325,000  Bonus Target: 40%  Equity: 150,000 options\n\n"
        "Marcus A. Torres, VP Engineering:\n  Base: $340,000  Bonus Target: 40%  Equity: 175,000 options\n\n"
        "Anita R. Patel, VP Design:\n  Base: $295,000  Bonus Target: 35%  Equity: 120,000 options\n\n"
        "James R. Harrington, CTO:\n  Base: $425,000  Bonus Target: 50%  Equity: 300,000 options\n\n"
        "Robert A. Chen, CEO:\n  Base: $500,000  Bonus Target: 75%  Equity: 500,000 options\n\n"
        "Total VP+ Compensation (base only): $1,885,000\n"
        "Total VP+ Compensation (w/ target bonus): $2,649,250",

        "INVESTOR RELATIONS - SERIES C DETAILS\n\n"
        "Series C Funding Round: $75,000,000\n"
        "Lead Investor: Granite Point Ventures\n"
        "Participating: Sequoia Capital, Andreessen Horowitz, Lightspeed Venture Partners\n"
        "Pre-Money Valuation: $450,000,000\n"
        "Post-Money Valuation: $525,000,000\n\n"
        "Board Seats: 2 (1 Granite Point, 1 Independent)\n"
        "Anti-Dilution: Broad-based weighted average\n"
        "Liquidation Preference: 1x non-participating\n\n"
        "Key Milestones for Series D Consideration:\n"
        "  - ARR > $200M by Q4 2025\n"
        "  - Customer count > 2,000 enterprise accounts\n"
        "  - Gross margin > 75%\n"
        "  - Net Revenue Retention > 130%",

        "AUDIT NOTES - INDEPENDENT AUDITOR OBSERVATIONS\n\n"
        "Auditor: Deloitte & Touche LLP\n"
        "Audit Period: FY2023\n"
        "Opinion: Unqualified (Clean)\n\n"
        "Management Letter Observations:\n"
        "1. Revenue Recognition: We noted three instances where revenue was recognized prior to "
        "completion of all performance obligations. Total amount: $890,000. Correcting entries were made.\n\n"
        "2. Related Party Transactions: Board member Dr. Patricia Langford serves on the advisory board "
        "of CloudSync Partners, a vendor receiving $240,000/year. Proper disclosure recommended.\n\n"
        "3. Stock Option Accounting: The Black-Scholes assumptions used for option valuation should be "
        "updated to reflect current market volatility. Impact estimated at $340,000.\n\n"
        "4. Internal Controls: One material weakness identified in the procurement approval workflow. "
        "Purchase orders exceeding $50,000 were approved by department heads without CFO review in "
        "approximately 15% of sampled transactions.",

        "TAX SUMMARY AND PROVISIONS\n\n"
        "Federal Income Tax Provision: $1,380,000\n"
        "State Income Tax Provision: $552,000\n"
        "Deferred Tax Asset: $4,200,000\n"
        "R&D Tax Credit: $2,850,000\n\n"
        "Net Operating Loss Carryforward: $12,400,000\n"
        "Expected Utilization: FY2024-FY2026\n\n"
        "Transfer Pricing: All intercompany transactions with Meridian Technologies Ireland, Ltd. "
        "have been conducted at arm's length per the Company's transfer pricing study prepared by "
        "PricewaterhouseCoopers.",

        "ACCOUNTS RECEIVABLE AGING REPORT\n\n"
        "Current (0-30 days):     $14,200,000 (64.1%)\n"
        "31-60 days:               $4,500,000 (20.3%)\n"
        "61-90 days:               $2,100,000  (9.5%)\n"
        "91-120 days:                $850,000  (3.8%)\n"
        "Over 120 days:              $500,000  (2.3%)\n"
        "Total:                   $22,150,000\n\n"
        "Allowance for Doubtful Accounts: $660,000 (3.0%)\n\n"
        "Top 5 Outstanding Balances:\n"
        "  1. Global Financial Services Corp.  $3,200,000  Current\n"
        "  2. Nexus Health Systems            $2,400,000  31-60 days\n"
        "  3. Pacific Rim Trading Co.         $1,800,000  Current\n"
        "  4. United Defense Contractors      $1,500,000  61-90 days\n"
        "  5. Evergreen Energy Partners       $1,100,000  Current",

        "REVENUE BY PRODUCT LINE\n\n"
        "Product A - Enterprise Platform:   $28,500,000  (59.1%)\n"
        "Product B - Analytics Suite:        $11,200,000  (23.2%)\n"
        "Product C - Mobile SDK:              $4,800,000  (10.0%)\n"
        "Professional Services:               $3,750,000   (7.8%)\n"
        "Total Revenue:                      $48,250,000\n\n"
        "Recurring Revenue: $39,200,000 (81.2%)\n"
        "One-time Revenue:   $9,050,000 (18.8%)\n\n"
        "Customer Churn Rate: 4.2% (annual)\n"
        "Net Revenue Retention: 128%\n"
        "Average Contract Value: $96,500\n"
        "Number of Enterprise Customers: 500",
    ]

    for i, content in enumerate(exhibit3_content):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        add_page_header(page, 3, i + 2, 9)
        rect = pymupdf.Rect(54, 72, 558, 720)
        page.insert_textbox(rect, content, fontsize=10, fontname="tiro", color=(0, 0, 0))


def create_exhibit_4(doc):
    """Exhibit 4: Internal Investigation Report (pages 35-45)"""
    # Title page
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    add_page_header(page, 4, 1, 11)
    page.insert_text(pymupdf.Point(120, 150), "PRIVILEGED AND CONFIDENTIAL", fontsize=14, fontname="hebo", color=(0.7, 0, 0))
    page.insert_text(pymupdf.Point(130, 180), "ATTORNEY-CLIENT PRIVILEGED", fontsize=14, fontname="hebo", color=(0.7, 0, 0))

    page.insert_text(pymupdf.Point(100, 240), "INTERNAL INVESTIGATION REPORT", fontsize=18, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(120, 270), "Re: Potential Trade Secret Misappropriation", fontsize=13, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(150, 300), "Investigation of David Kim and Lisa Chen", fontsize=12, fontname="helv", color=(0, 0, 0))

    page.insert_text(pymupdf.Point(54, 360), "Prepared by:", fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(54, 376), "Morrison & Foerster LLP", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(54, 392), "425 Market Street, San Francisco, CA 94105", fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(54, 408), "Lead Partner: Katherine M. Davenport, Esq.", fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(54, 440), "Date: May 28, 2024", fontsize=10, fontname="helv", color=(0, 0, 0))

    investigation_pages = [
        "I. EXECUTIVE SUMMARY\n\n"
        "Morrison & Foerster LLP was retained by Meridian Technologies, Inc. ('Meridian' or the 'Company') "
        "on April 10, 2024, to investigate potential trade secret misappropriation by departing employees "
        "David Kim (Senior Software Engineer) and Lisa Chen (Senior Platform Architect).\n\n"
        "Both employees resigned on April 1, 2024, and disclosed their intent to join Vertex Labs, Inc. "
        "('Vertex'), a direct competitor in the enterprise software platform market.\n\n"
        "Key Findings:\n"
        "1. David Kim accessed and downloaded 847 files from the Project Horizon repository in the 72 hours "
        "prior to submitting his resignation.\n"
        "2. Lisa Chen sent 14 emails with attachments to her personal email address between March 15-31, 2024.\n"
        "3. Both employees had access to Meridian's core algorithmic trade secrets, including the proprietary "
        "data processing pipeline known internally as 'Phoenix Engine.'\n"
        "4. Digital forensic analysis of company-issued laptops revealed use of personal USB drives on "
        "March 28 and March 29, 2024.",

        "II. BACKGROUND\n\n"
        "A. The Employees\n\n"
        "David Kim joined Meridian in January 2021 as a Software Engineer and was promoted to Senior Software "
        "Engineer in July 2022. His primary responsibilities included development of the Phoenix Engine's "
        "core processing algorithms. He had Level 4 security clearance, granting access to all source code "
        "repositories and architectural documentation.\n\n"
        "Lisa Chen joined Meridian in March 2020 as a Platform Architect and was promoted to Senior Platform "
        "Architect in October 2022. She was responsible for the overall system architecture of the Enterprise "
        "Platform product, including database schema design, API specifications, and cloud infrastructure "
        "configurations. She held Level 4 security clearance.\n\n"
        "B. Vertex Labs\n\n"
        "Vertex Labs, Inc. is a venture-backed startup founded in 2022 by former Google engineers. Vertex "
        "recently raised a $120 million Series B round and has publicly announced its intention to compete "
        "directly with Meridian's Enterprise Platform product. Vertex's CEO, Michael Torres (no relation to "
        "Meridian's Marcus Torres), has been quoted in TechCrunch stating Vertex aims to 'redefine enterprise "
        "data processing with next-generation algorithms.'",

        "III. INVESTIGATION METHODOLOGY\n\n"
        "The investigation was conducted from April 10 through May 25, 2024, and included the following:\n\n"
        "A. Digital Forensics\n"
        "  - Analysis of company-issued laptops for both employees (conducted by Stroz Friedberg)\n"
        "  - Review of email server logs for the period January 1 - April 30, 2024\n"
        "  - Audit of source code repository access logs (GitHub Enterprise)\n"
        "  - Review of VPN access logs and file server access records\n"
        "  - Analysis of cloud storage access patterns (AWS S3, Google Drive)\n\n"
        "B. Witness Interviews\n"
        "  - Marcus Torres, VP Engineering (Kim and Chen's direct manager)\n"
        "  - Sarah Whitfield, VP Product Development\n"
        "  - Four members of the Project Horizon development team\n"
        "  - IT Security team members\n\n"
        "C. Document Review\n"
        "  - Employment agreements, including non-compete and NDA provisions\n"
        "  - Exit interview documentation\n"
        "  - Company IT security policies\n"
        "  - Project Horizon access control lists and permissions",

        "IV. FINDINGS - DAVID KIM\n\n"
        "A. Unusual Access Patterns\n\n"
        "Repository access logs reveal that between March 29 and April 1, 2024, David Kim cloned or "
        "downloaded 847 files from the Project Horizon repository. This represents a 1,200% increase "
        "over his typical monthly access pattern of approximately 65-70 files.\n\n"
        "The accessed files include:\n"
        "  - Phoenix Engine core algorithm source code (312 files)\n"
        "  - API specification documents (89 files)\n"
        "  - Performance benchmark data (124 files)\n"
        "  - Architecture decision records (78 files)\n"
        "  - Internal testing frameworks (244 files)\n\n"
        "B. USB Device Usage\n\n"
        "Digital forensic analysis of Kim's company laptop revealed that a Samsung T7 portable SSD "
        "(serial number: S4EMNF0R829571) was connected on March 28 at 11:47 PM and March 29 at "
        "12:15 AM. File transfer activity was detected but specific files could not be identified "
        "due to encryption on the external drive.",

        "V. FINDINGS - LISA CHEN\n\n"
        "A. Email Activity\n\n"
        "Between March 15 and March 31, 2024, Lisa Chen sent 14 emails to her personal Gmail address "
        "(l.chen.personal@gmail.com) containing attachments. The emails were sent during non-business "
        "hours (between 10 PM and 6 AM). Attachments included:\n\n"
        "  - Enterprise Platform architecture diagrams (3 files, total 45 MB)\n"
        "  - Database schema documentation (2 files, total 12 MB)\n"
        "  - Customer integration specifications (4 files, total 28 MB)\n"
        "  - Performance optimization research notes (5 files, total 8 MB)\n\n"
        "B. Cloud Storage Access\n\n"
        "AWS CloudTrail logs show that Chen accessed the S3 bucket containing the Platform Architecture "
        "documentation on 23 separate occasions between March 10 and March 31, downloading a total of "
        "2.3 GB of data. Her typical monthly download volume was approximately 200 MB.\n\n"
        "C. Exit Interview\n\n"
        "During her exit interview on April 15, Chen denied taking any company proprietary information. "
        "When asked about the emails to her personal address, she stated they contained 'personal notes' "
        "and 'general industry research.'",

        "VI. LEGAL ANALYSIS\n\n"
        "A. Non-Compete Enforceability\n\n"
        "Under California Business & Professions Code Section 16600, non-compete agreements are generally "
        "unenforceable in California with limited exceptions. The employees' non-compete clauses (Section 4.3 "
        "of their respective Employment Agreements) are likely unenforceable.\n\n"
        "B. Trade Secret Protection\n\n"
        "The California Uniform Trade Secrets Act (Cal. Civ. Code 3426-3426.11) provides robust protection "
        "for trade secrets independent of any contractual obligations. The Phoenix Engine algorithms and "
        "architectural specifications likely qualify as trade secrets if Meridian can demonstrate:\n"
        "  1. The information derives independent economic value from not being generally known\n"
        "  2. Meridian has made reasonable efforts to maintain secrecy\n\n"
        "Based on our review, both elements appear to be satisfied.\n\n"
        "C. Computer Fraud\n\n"
        "The bulk downloading of files by Kim and the email forwarding by Chen may constitute violations of "
        "the Computer Fraud and Abuse Act (18 U.S.C. 1030) and the California Comprehensive Computer Data "
        "Access and Fraud Act (Cal. Penal Code 502).",

        "VII. RECOMMENDATIONS\n\n"
        "Based on our investigation findings, we recommend the following course of action:\n\n"
        "1. IMMEDIATE: Send cease-and-desist letters to both David Kim and Lisa Chen demanding:\n"
        "   a. Return of all Meridian proprietary materials\n"
        "   b. Certification of deletion of all electronic copies\n"
        "   c. Preservation of all relevant documents for potential litigation\n\n"
        "2. SHORT-TERM: Engage with Vertex Labs' legal counsel to:\n"
        "   a. Notify them of the potential trade secret issues\n"
        "   b. Request implementation of ethical screening procedures\n"
        "   c. Negotiate an information barrier ('ethical wall') protocol\n\n"
        "3. LITIGATION PREPAREDNESS:\n"
        "   a. File for a Temporary Restraining Order if cease-and-desist is not effective\n"
        "   b. Prepare complaint for trade secret misappropriation under CUTSA\n"
        "   c. Consider federal claims under the Defend Trade Secrets Act (DTSA)\n"
        "   d. Estimated litigation budget: $750,000 - $1,200,000\n\n"
        "4. INTERNAL REMEDIATION:\n"
        "   a. Implement enhanced DLP (Data Loss Prevention) systems\n"
        "   b. Revoke all access for departing employees immediately upon notice\n"
        "   c. Conduct security audit of remaining Horizon team members\n"
        "   d. Update exit protocols to include forensic device imaging",

        "VIII. FORENSIC EVIDENCE SUMMARY\n\n"
        "The following evidence has been preserved and is available for litigation:\n\n"
        "Digital Evidence:\n"
        "  - Forensic images of Kim's laptop (Dell Latitude 5540, SN: JK4829FN)\n"
        "  - Forensic image of Chen's laptop (Dell Latitude 5540, SN: LC7193QM)\n"
        "  - Email server exports (PST format) for both employees\n"
        "  - GitHub Enterprise audit logs (January 1 - April 30, 2024)\n"
        "  - AWS CloudTrail logs (January 1 - April 30, 2024)\n"
        "  - VPN access logs (January 1 - April 30, 2024)\n"
        "  - Badge access records for both employees\n\n"
        "Physical Evidence:\n"
        "  - Company-issued laptops (retained by Meridian IT)\n"
        "  - Badge access card logs\n"
        "  - Visitor logs showing Vertex Labs representatives visited Meridian campus on February 15\n\n"
        "Chain of Custody:\n"
        "  All digital evidence was collected and preserved by Stroz Friedberg under the direction of "
        "this firm. Forensic images were created using EnCase 8.x with SHA-256 hash verification.",

        "IX. TIMELINE OF KEY EVENTS\n\n"
        "February 15, 2024 - Vertex Labs representatives visit Meridian for 'partnership discussions'\n"
        "March 1, 2024 - Kim and Chen begin having regular off-site lunch meetings (per badge data)\n"
        "March 10, 2024 - Chen begins increased S3 bucket access pattern\n"
        "March 15, 2024 - Chen begins forwarding emails to personal address\n"
        "March 28, 2024 - Kim connects USB drive to company laptop (11:47 PM)\n"
        "March 29, 2024 - Kim connects USB drive again (12:15 AM)\n"
        "March 29-April 1 - Kim downloads 847 files from Horizon repository\n"
        "April 1, 2024 - Both employees submit resignation letters\n"
        "April 2, 2024 - Marcus Torres notifies Sarah Whitfield\n"
        "April 5, 2024 - Whitfield requests legal review of non-compete clauses\n"
        "April 10, 2024 - Morrison & Foerster retained; legal hold implemented\n"
        "April 15, 2024 - Exit interviews conducted\n"
        "April 30, 2024 - Last day of employment for both individuals\n"
        "May 6, 2024 - Both employees confirmed to have started at Vertex Labs\n"
        "May 28, 2024 - Investigation report completed",

        "X. APPENDICES\n\n"
        "Appendix A: Employment Agreement - David Kim (executed January 8, 2021)\n"
        "Appendix B: Employment Agreement - Lisa Chen (executed March 2, 2020)\n"
        "Appendix C: Meridian Technologies Information Security Policy v4.2\n"
        "Appendix D: Digital Forensics Report - Stroz Friedberg (May 20, 2024)\n"
        "Appendix E: GitHub Repository Access Log Summary\n"
        "Appendix F: AWS CloudTrail Access Log Summary\n"
        "Appendix G: Email Server Log Analysis\n"
        "Appendix H: Witness Interview Memoranda (Privileged)\n"
        "Appendix I: Comparative Analysis of Meridian and Vertex Patent Filings\n"
        "Appendix J: Sample Cease-and-Desist Letter (Draft)\n\n\n"
        "DISCLAIMER\n\n"
        "This report has been prepared by Morrison & Foerster LLP for the sole use of Meridian Technologies, "
        "Inc. and is protected by attorney-client privilege and the work product doctrine. This report should "
        "not be disclosed to any third party without the prior written consent of Morrison & Foerster LLP.\n\n"
        "Respectfully submitted,\n\n"
        "Katherine M. Davenport, Esq.\n"
        "Partner, Morrison & Foerster LLP\n"
        "May 28, 2024",
    ]

    for i, content in enumerate(investigation_pages):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        add_page_header(page, 4, i + 2, 11)
        rect = pymupdf.Rect(54, 72, 558, 720)
        page.insert_textbox(rect, content, fontsize=10, fontname="tiro", color=(0, 0, 0))


def create_initial():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Exhibit 1: Employment Agreement (pages 1-10)
    create_exhibit_1(doc)

    # Exhibit 2: Email Correspondence (pages 11-25)
    create_exhibit_2(doc)

    # Exhibit 3: Financial Records (pages 26-34)
    create_exhibit_3(doc)

    # Exhibit 4: Internal Investigation Report (pages 35-45)
    create_exhibit_4(doc)

    assert doc.page_count == 45, f"Expected 45 pages, got {doc.page_count}"

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT} (45 pages)')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
