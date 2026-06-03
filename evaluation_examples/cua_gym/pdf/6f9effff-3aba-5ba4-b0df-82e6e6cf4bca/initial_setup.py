"""
Initial Setup: Create a 35-page deposition exhibit package PDF
Task ID: pdf_legal_088
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_088'
OUTPUT_DIR = f'{WORKDIR}/legal/depo'
OUTPUT = f'{OUTPUT_DIR}/exhibits_package.pdf'

# Page dimensions: US Letter
W, H = 612, 792


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


def add_header_footer(page, page_num_display, exhibit_label=None):
    """Add standard legal header/footer to a page."""
    # Footer: page number centered
    page.insert_text(
        pymupdf.Point(W / 2 - 20, H - 30),
        f"Page {page_num_display}",
        fontsize=9,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    # Top border line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(54, 54), pymupdf.Point(W - 54, 54))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()


def create_exhibit_1(doc):
    """Exhibit 1 (pages 1-7): Employment Agreement"""
    # Page 1 - Title page
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(180, 120), "EMPLOYMENT AGREEMENT", fontsize=18, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(54, 170), "This Employment Agreement ('Agreement') is entered into as of March 15, 2024,", fontsize=11, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(54, 188), "by and between Meridian Technologies, Inc., a Delaware corporation ('Company'),", fontsize=11, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(54, 206), "and Dr. Katherine R. Thornton ('Employee').", fontsize=11, fontname="tiro", color=(0, 0, 0))

    page.insert_text(pymupdf.Point(54, 250), "1. POSITION AND DUTIES", fontsize=12, fontname="hebo", color=(0, 0, 0))
    rect = pymupdf.Rect(54, 268, W - 54, 400)
    page.insert_textbox(rect,
        "Employee shall serve as Chief Technology Officer reporting directly to the "
        "Chief Executive Officer. Employee shall devote substantially all of her working "
        "time, attention, and energies to the performance of her duties hereunder. Employee "
        "shall have such authority and responsibilities as are customarily associated with "
        "the position of CTO, including oversight of all technology development, engineering "
        "teams, and intellectual property strategy.",
        fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(54, 420), "2. COMPENSATION", fontsize=12, fontname="hebo", color=(0, 0, 0))
    rect = pymupdf.Rect(54, 438, W - 54, 580)
    page.insert_textbox(rect,
        "a) Base Salary: Company shall pay Employee an annual base salary of Four Hundred "
        "Twenty-Five Thousand Dollars ($425,000.00), payable in accordance with the Company's "
        "standard payroll practices. b) Annual Bonus: Employee shall be eligible for an annual "
        "performance bonus of up to 40% of base salary, based on achievement of mutually agreed "
        "performance targets. c) Equity Grant: Employee shall receive an initial grant of 150,000 "
        "stock options under the Company's 2024 Equity Incentive Plan, vesting over four years "
        "with a one-year cliff.",
        fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(54, 600), "3. TERM AND TERMINATION", fontsize=12, fontname="hebo", color=(0, 0, 0))
    rect = pymupdf.Rect(54, 618, W - 54, 740)
    page.insert_textbox(rect,
        "This Agreement shall commence on April 1, 2024 and continue for an initial term of "
        "three (3) years, unless earlier terminated pursuant to the provisions herein. Either "
        "party may terminate this Agreement upon sixty (60) days written notice. Company may "
        "terminate for Cause as defined in Section 3(b) below.",
        fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_header_footer(page, 1)

    # Pages 2-7: remaining agreement sections
    sections = [
        ("4. BENEFITS AND PERQUISITES",
         "Employee shall be entitled to participate in all benefit programs generally available "
         "to senior executives, including health insurance (medical, dental, vision), life insurance "
         "at 3x base salary, disability coverage, and the Company's 401(k) plan with 6% employer "
         "match. Employee shall receive four (4) weeks paid vacation annually, plus Company holidays. "
         "Company shall provide Employee with a monthly automobile allowance of $1,200 and shall "
         "reimburse reasonable business expenses in accordance with Company policy.",
         "5. NON-COMPETITION AND NON-SOLICITATION",
         "During the term of employment and for a period of eighteen (18) months following "
         "termination, Employee agrees not to: (a) engage in any business that competes directly "
         "with the Company's core products in the enterprise software market; (b) solicit or hire "
         "any Company employee or contractor who was employed during the twelve months preceding "
         "termination; (c) solicit any customer or prospective customer with whom Employee had "
         "material contact during the last two years of employment."),
        ("6. CONFIDENTIALITY AND INTELLECTUAL PROPERTY",
         "Employee acknowledges that during employment she will have access to Confidential "
         "Information including trade secrets, customer lists, pricing strategies, product roadmaps, "
         "and proprietary technology. Employee agrees to maintain strict confidentiality of all such "
         "information during and after employment. All inventions, developments, and works of "
         "authorship created during employment shall be the exclusive property of the Company.",
         "7. DISPUTE RESOLUTION",
         "Any dispute arising under this Agreement shall be resolved through binding arbitration "
         "administered by JAMS in San Francisco, California, under the JAMS Employment Arbitration "
         "Rules. The arbitrator's decision shall be final and binding. Each party shall bear its own "
         "costs and attorneys' fees unless the arbitrator determines otherwise."),
        ("8. SEVERANCE",
         "In the event of termination without Cause or resignation for Good Reason, Employee shall "
         "receive: (a) twelve (12) months base salary continuation; (b) pro-rated annual bonus for "
         "the year of termination; (c) accelerated vesting of 25% of unvested equity awards; "
         "(d) continuation of health benefits at Company expense for twelve months (COBRA). Payment "
         "of severance is conditioned upon Employee's execution of a general release of claims.",
         "9. REPRESENTATIONS AND WARRANTIES",
         "Employee represents that: (a) she is not bound by any non-competition agreement or other "
         "obligation that would prevent her from fulfilling her duties; (b) she has not brought and "
         "will not bring any proprietary information from former employers; (c) all information "
         "provided during the hiring process was truthful and complete."),
        ("10. CHANGE OF CONTROL",
         "In the event of a Change of Control (as defined herein), all unvested equity awards shall "
         "immediately vest in full. If Employee is terminated within twelve (12) months following a "
         "Change of Control, she shall receive enhanced severance equal to two (2) years base salary "
         "plus target bonus, payable in a lump sum within thirty (30) days of termination.",
         "11. GENERAL PROVISIONS",
         "This Agreement constitutes the entire understanding between the parties and supersedes all "
         "prior negotiations and agreements. This Agreement shall be governed by the laws of the "
         "State of California. No modification shall be effective unless in writing signed by both "
         "parties. If any provision is found unenforceable, the remaining provisions shall continue "
         "in full force and effect."),
        ("SIGNATURES",
         "IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.\n\n"
         "MERIDIAN TECHNOLOGIES, INC.\n\n"
         "By: _______________________________\n"
         "    James R. Whitfield, CEO\n"
         "    Date: March 15, 2024\n\n\n"
         "EMPLOYEE\n\n"
         "_______________________________\n"
         "Dr. Katherine R. Thornton\n"
         "Date: March 15, 2024",
         "", ""),
        ("SCHEDULE A: PERFORMANCE TARGETS FOR FISCAL YEAR 2024-2025",
         "1. Revenue Target: Achieve $45M in enterprise software revenue (weight: 30%)\n"
         "2. Product Delivery: Launch v3.0 platform by September 30, 2024 (weight: 25%)\n"
         "3. Team Growth: Expand engineering team from 42 to 65 FTEs (weight: 15%)\n"
         "4. Customer Retention: Maintain 95%+ annual retention rate (weight: 15%)\n"
         "5. Infrastructure: Achieve 99.95% platform uptime SLA (weight: 15%)",
         "SCHEDULE B: EQUITY GRANT DETAILS",
         "Option Type: Incentive Stock Options (ISOs)\n"
         "Number of Shares: 150,000\n"
         "Exercise Price: $12.50 per share (FMV at grant date)\n"
         "Vesting Schedule: 25% after 12 months, then monthly over 36 months\n"
         "Expiration: 10 years from grant date\n"
         "Acceleration: Per Section 10 (Change of Control)"),
    ]

    for i, (title1, body1, title2, body2) in enumerate(sections, 2):
        page = doc.new_page(width=W, height=H)
        y = 80
        page.insert_text(pymupdf.Point(54, y), title1, fontsize=12, fontname="hebo", color=(0, 0, 0))
        y += 20
        rect = pymupdf.Rect(54, y, W - 54, y + 200)
        page.insert_textbox(rect, body1, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        if title2:
            y += 220
            page.insert_text(pymupdf.Point(54, y), title2, fontsize=12, fontname="hebo", color=(0, 0, 0))
            y += 20
            rect = pymupdf.Rect(54, y, W - 54, y + 200)
            page.insert_textbox(rect, body2, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        add_header_footer(page, i)


def create_exhibit_2(doc):
    """Exhibit 2 (pages 8-14): Email Correspondence"""
    emails = [
        ("From: j.whitfield@meridiantech.com", "To: k.thornton@meridiantech.com",
         "Date: June 12, 2024 9:47 AM", "Subject: Q2 Product Development Update Request",
         "Katherine,\n\nI need an updated timeline for the v3.0 platform release. The board meeting "
         "is scheduled for June 28 and I want to present current progress metrics. Please also include "
         "headcount projections for Q3 -- I know we discussed expanding the ML infrastructure team "
         "but I want to see how that fits into the overall engineering budget.\n\n"
         "Also, Westbrook Financial has expressed interest in an enterprise pilot. Can you have your "
         "team prepare a technical capabilities deck by next Friday?\n\nBest,\nJames"),
        ("From: k.thornton@meridiantech.com", "To: j.whitfield@meridiantech.com",
         "Date: June 12, 2024 2:15 PM", "Subject: Re: Q2 Product Development Update Request",
         "James,\n\nHere's the current status:\n\n"
         "- Core platform: 78% complete, on track for August beta\n"
         "- ML pipeline module: 62% complete, delayed 2 weeks due to GPU procurement issues\n"
         "- API gateway: 91% complete, ahead of schedule\n"
         "- Security audit: Scheduled for July 15-19 with CrowdStrike\n\n"
         "For headcount, we need 8 additional engineers in Q3 (4 backend, 2 ML, 2 DevOps). "
         "Projected cost: $1.2M annually fully loaded.\n\n"
         "I'll have the Westbrook deck ready by Thursday. Sarah Chen on my team has prior "
         "experience with financial services clients.\n\nKatherine"),
        ("From: m.rodriguez@meridiantech.com", "To: k.thornton@meridiantech.com",
         "Date: July 3, 2024 11:22 AM", "Subject: URGENT: Production Database Incident",
         "Dr. Thornton,\n\nWe experienced a critical production incident at 10:45 AM EST. "
         "The primary database cluster in us-east-1 became unresponsive, affecting approximately "
         "340 enterprise customers. The on-call team has implemented failover to the secondary "
         "cluster. Current service restoration is at 87%.\n\n"
         "Root cause appears to be a misconfigured connection pool limit introduced in last night's "
         "deployment (commit 4a7f2c1). We're preparing a rollback.\n\n"
         "Estimated full recovery: 2 hours.\n\nMarcos Rodriguez\nSr. DevOps Engineer"),
        ("From: k.thornton@meridiantech.com", "To: m.rodriguez@meridiantech.com",
         "Date: July 3, 2024 11:31 AM", "Subject: Re: URGENT: Production Database Incident",
         "Marcos,\n\nProceed with the rollback immediately. I'm pulling David Park and Lisa Wang "
         "into a war room call in 10 minutes. Please prepare a full incident timeline.\n\n"
         "After recovery, I want a post-mortem scheduled within 48 hours. We need to review "
         "our deployment validation process -- this should have been caught in staging.\n\n"
         "Also loop in the customer success team -- they need to start proactive outreach "
         "to our top-tier accounts.\n\nKatherine"),
        ("From: k.thornton@meridiantech.com", "To: engineering-all@meridiantech.com",
         "Date: July 5, 2024 4:30 PM", "Subject: Post-Incident Review and New Deployment Protocols",
         "Team,\n\nFollowing the July 3rd production incident, I'm implementing the following changes "
         "effective immediately:\n\n"
         "1. All production deployments require sign-off from two senior engineers\n"
         "2. Mandatory canary deployment phase (5% traffic for 30 minutes)\n"
         "3. Automated rollback triggers for error rate > 0.1% or latency > 500ms p99\n"
         "4. Weekly deployment windows: Tuesday and Thursday, 10 AM - 2 PM EST only\n"
         "5. Connection pool configurations now require DBA review\n\n"
         "The full post-mortem document is available in Confluence. Please review before our "
         "all-hands on Monday.\n\nKatherine Thornton\nChief Technology Officer"),
        ("From: s.chen@meridiantech.com", "To: k.thornton@meridiantech.com",
         "Date: August 8, 2024 3:18 PM", "Subject: Westbrook Financial Pilot - Technical Issues",
         "Katherine,\n\nThe Westbrook pilot is encountering performance issues in their environment. "
         "Their data volumes are 3x what we modeled in the POC. Specifically:\n\n"
         "- Batch processing jobs timing out after 4 hours (expected: 45 minutes)\n"
         "- Memory usage on worker nodes exceeding 90% during peak loads\n"
         "- Their compliance module requires SOC 2 Type II certification, which we're still pursuing\n\n"
         "I've proposed a phased rollout starting with their smaller datasets, but their CTO "
         "(Robert Kwan) is pushing back. He wants full production capability by September 15.\n\n"
         "Can we discuss resource allocation options? We may need to temporarily reassign "
         "2-3 engineers from the ML team.\n\nSarah Chen\nDirector of Enterprise Solutions"),
        ("From: k.thornton@meridiantech.com", "To: s.chen@meridiantech.com",
         "Date: August 8, 2024 5:42 PM", "Subject: Re: Westbrook Financial Pilot - Technical Issues",
         "Sarah,\n\nLet's approach this strategically. I'm authorizing the following:\n\n"
         "1. Reassign David Park and one junior engineer from ML team for 4 weeks\n"
         "2. Fast-track the horizontal scaling feature from the v3.1 roadmap\n"
         "3. Schedule a joint technical review with Robert Kwan's team next week\n"
         "4. Engage our SOC 2 auditors for an expedited timeline (contact Legal re: budget)\n\n"
         "The Westbrook deal is worth $2.8M ARR -- we need to make this work. But I don't want to "
         "compromise v3.0 launch quality. Let's find the balance.\n\n"
         "Set up a 30-minute sync for tomorrow morning.\n\nKatherine"),
    ]

    for i, (from_line, to_line, date_line, subject_line, body) in enumerate(emails):
        page = doc.new_page(width=W, height=H)
        y = 80
        page.insert_text(pymupdf.Point(54, y), from_line, fontsize=10, fontname="cour", color=(0.2, 0.2, 0.2))
        y += 16
        page.insert_text(pymupdf.Point(54, y), to_line, fontsize=10, fontname="cour", color=(0.2, 0.2, 0.2))
        y += 16
        page.insert_text(pymupdf.Point(54, y), date_line, fontsize=10, fontname="cour", color=(0.2, 0.2, 0.2))
        y += 16
        page.insert_text(pymupdf.Point(54, y), subject_line, fontsize=10, fontname="cobo", color=(0, 0, 0))
        y += 30

        # Separator line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(54, y), pymupdf.Point(W - 54, y))
        shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape.commit()
        y += 15

        rect = pymupdf.Rect(54, y, W - 54, H - 60)
        page.insert_textbox(rect, body, fontsize=11, fontname="tiro", color=(0, 0, 0))
        add_header_footer(page, 8 + i)


def create_exhibit_3(doc):
    """Exhibit 3 (pages 15-19): Financial Summary"""
    # Page 15: Financial overview
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(150, 90), "MERIDIAN TECHNOLOGIES, INC.", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(160, 115), "Financial Summary: FY 2024-2025", fontsize=14, fontname="hebo", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(220, 138), "Prepared: October 15, 2024", fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))

    page.insert_text(pymupdf.Point(54, 180), "REVENUE BREAKDOWN BY QUARTER", fontsize=12, fontname="hebo", color=(0, 0, 0))

    # Table header
    y = 205
    cols = [54, 170, 280, 390, 500]
    headers = ["Category", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024 (Proj)"]
    for col, h in zip(cols, headers):
        page.insert_text(pymupdf.Point(col, y), h, fontsize=9, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(54, y + 5), pymupdf.Point(W - 54, y + 5))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()

    data = [
        ["Enterprise SaaS", "$8.2M", "$9.1M", "$10.4M", "$11.8M"],
        ["Professional Services", "$1.4M", "$1.6M", "$1.8M", "$2.1M"],
        ["Platform Licensing", "$2.3M", "$2.5M", "$2.7M", "$3.0M"],
        ["Maintenance & Support", "$0.8M", "$0.9M", "$0.9M", "$1.0M"],
        ["Total Revenue", "$12.7M", "$14.1M", "$15.8M", "$17.9M"],
    ]
    y += 22
    for row in data:
        fname = "hebo" if row[0] == "Total Revenue" else "helv"
        for col, val in zip(cols, row):
            page.insert_text(pymupdf.Point(col, y), val, fontsize=9, fontname=fname, color=(0, 0, 0))
        y += 16

    page.insert_text(pymupdf.Point(54, y + 30), "OPERATING EXPENSES", fontsize=12, fontname="hebo", color=(0, 0, 0))
    expenses = [
        ["Engineering & R&D", "$4.8M", "$5.2M", "$5.7M", "$6.1M"],
        ["Sales & Marketing", "$3.1M", "$3.4M", "$3.6M", "$3.9M"],
        ["General & Admin", "$1.5M", "$1.6M", "$1.7M", "$1.8M"],
        ["Total OpEx", "$9.4M", "$10.2M", "$11.0M", "$11.8M"],
    ]
    y += 52
    for col, h in zip(cols, headers):
        page.insert_text(pymupdf.Point(col, y), h, fontsize=9, fontname="hebo", color=(0, 0, 0))
    y += 20
    for row in expenses:
        fname = "hebo" if "Total" in row[0] else "helv"
        for col, val in zip(cols, row):
            page.insert_text(pymupdf.Point(col, y), val, fontsize=9, fontname=fname, color=(0, 0, 0))
        y += 16

    add_header_footer(page, 15)

    # Pages 16-19: Additional financial detail
    fin_pages = [
        ("HEADCOUNT AND PERSONNEL COSTS",
         "Engineering Department:\n"
         "  Q1: 42 FTEs | Avg Salary: $165,000 | Total: $6.93M annually\n"
         "  Q2: 48 FTEs | Avg Salary: $168,000 | Total: $8.06M annually\n"
         "  Q3: 55 FTEs | Avg Salary: $170,000 | Total: $9.35M annually\n"
         "  Q4: 63 FTEs (projected) | Avg Salary: $172,000 | Total: $10.84M annually\n\n"
         "Sales Department:\n"
         "  Q1: 28 FTEs | Avg Salary: $135,000 | Total: $3.78M annually\n"
         "  Q2: 31 FTEs | Avg Salary: $138,000 | Total: $4.28M annually\n"
         "  Q3: 34 FTEs | Avg Salary: $140,000 | Total: $4.76M annually\n"
         "  Q4: 38 FTEs (projected) | Avg Salary: $142,000 | Total: $5.40M annually\n\n"
         "Total Company Headcount: 142 (Q1) -> 178 (Q4 projected)\n"
         "Year-over-Year Growth: 25.4%"),
        ("CUSTOMER METRICS",
         "Enterprise Customers: 340 (as of September 30, 2024)\n"
         "  New Logos Q1-Q3: 47\n"
         "  Churned Accounts: 8\n"
         "  Net Revenue Retention: 118%\n"
         "  Annual Retention Rate: 97.6%\n\n"
         "Top 10 Customers by ARR:\n"
         "  1. Westbrook Financial Group    $2,800,000\n"
         "  2. Cascade Health Systems        $2,150,000\n"
         "  3. Atlas Manufacturing Corp      $1,890,000\n"
         "  4. Pinnacle Insurance Holdings   $1,620,000\n"
         "  5. Summit Energy Partners        $1,450,000\n"
         "  6. Nordic Semiconductor USA      $1,380,000\n"
         "  7. Commonwealth Bank of VA       $1,210,000\n"
         "  8. Redwood Analytics, Inc.       $1,150,000\n"
         "  9. Harbor Point Capital          $1,080,000\n"
         "  10. Clearwater Logistics         $980,000\n\n"
         "Total ARR from Top 10: $15,710,000 (26% of total ARR)"),
        ("CAPITAL EXPENDITURES AND INFRASTRUCTURE",
         "Cloud Infrastructure (AWS):\n"
         "  Compute (EC2/EKS): $1.24M/quarter\n"
         "  Storage (S3/EBS): $380K/quarter\n"
         "  Data Transfer: $210K/quarter\n"
         "  GPU Instances (ML): $560K/quarter\n"
         "  Total Cloud Spend: $2.39M/quarter | $9.56M annualized\n\n"
         "On-Premise Equipment:\n"
         "  Development Servers: $180K (one-time, Q1)\n"
         "  Network Equipment Upgrade: $95K (Q2)\n"
         "  Security Appliances: $120K (Q3)\n\n"
         "Software Licenses:\n"
         "  Development Tools: $340K annually\n"
         "  Security & Compliance: $220K annually\n"
         "  Collaboration Tools: $85K annually"),
        ("PROJECTIONS AND KEY ASSUMPTIONS - FY 2025-2026",
         "Revenue Projections:\n"
         "  Total Revenue: $72.5M (18% growth over FY 2024-2025)\n"
         "  Enterprise SaaS: $48.2M (driven by Westbrook expansion and new verticals)\n"
         "  Professional Services: $10.5M\n"
         "  Platform Licensing: $13.8M\n\n"
         "Key Assumptions:\n"
         "  - v3.0 platform launch drives 15% uplift in new logo acquisition\n"
         "  - Net revenue retention improves to 122% with expanded feature set\n"
         "  - Engineering headcount reaches 85 FTEs by end of FY 2025-2026\n"
         "  - SOC 2 Type II certification enables entry into financial services vertical\n"
         "  - No major pricing changes; modest 3-5% annual price increase for renewals\n\n"
         "Risk Factors:\n"
         "  - GPU procurement delays could impact ML feature roadmap\n"
         "  - Competitive pressure from CloudVault and DataBridge in mid-market\n"
         "  - Regulatory changes in EU data sovereignty may require infrastructure investment"),
    ]

    for i, (title, body) in enumerate(fin_pages):
        page = doc.new_page(width=W, height=H)
        page.insert_text(pymupdf.Point(54, 90), title, fontsize=13, fontname="hebo", color=(0, 0, 0.5))
        rect = pymupdf.Rect(54, 120, W - 54, H - 60)
        page.insert_textbox(rect, body, fontsize=10, fontname="helv", color=(0, 0, 0))
        add_header_footer(page, 16 + i)


def create_exhibit_4(doc):
    """Exhibit 4 (pages 20-27): Board Meeting Minutes"""
    # Page 20: First page of board minutes
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(140, 90), "MERIDIAN TECHNOLOGIES, INC.", fontsize=16, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(150, 115), "Minutes of the Board of Directors Meeting", fontsize=13, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(230, 138), "September 28, 2024", fontsize=11, fontname="helv", color=(0, 0, 0))

    rect = pymupdf.Rect(54, 170, W - 54, H - 60)
    page.insert_textbox(rect,
        "PRESENT:\n"
        "  James R. Whitfield, CEO and Chairman\n"
        "  Dr. Katherine R. Thornton, CTO\n"
        "  Michael S. Brannigan, CFO\n"
        "  Patricia Delgado-Ruiz, Independent Director\n"
        "  Thomas Hashimoto, Independent Director\n"
        "  Victoria M. Ashworth, Lead Independent Director\n\n"
        "ALSO PRESENT:\n"
        "  Rebecca Torres, General Counsel\n"
        "  Amanda Foster, Corporate Secretary\n\n"
        "CALL TO ORDER:\n"
        "Chairman Whitfield called the meeting to order at 10:00 AM PDT. A quorum was "
        "confirmed present.\n\n"
        "1. APPROVAL OF PRIOR MINUTES\n"
        "Director Ashworth moved to approve the minutes of the August 15, 2024 Board meeting "
        "as circulated. Director Hashimoto seconded. The motion was approved unanimously.\n\n"
        "2. CEO REPORT\n"
        "Mr. Whitfield presented the CEO's quarterly report, highlighting:\n"
        "  - Year-to-date revenue of $42.6M, exceeding plan by 4.2%\n"
        "  - Successful close of Series D funding ($85M at $1.2B valuation)\n"
        "  - Strategic partnership discussions with three Fortune 500 companies\n"
        "  - IPO readiness assessment initiated with Goldman Sachs and Morgan Stanley",
        fontsize=10, fontname="helv", color=(0, 0, 0))
    add_header_footer(page, 20)

    board_pages = [
        ("3. CTO TECHNOLOGY UPDATE\n"
         "Dr. Thornton presented the technology roadmap and v3.0 platform status:\n\n"
         "Platform Development:\n"
         "  - Core platform: 92% complete, beta launch October 15\n"
         "  - ML pipeline module: 85% complete, addressing Westbrook scale requirements\n"
         "  - API gateway: Released to production September 1\n"
         "  - Mobile SDK: Development initiated, targeting Q1 2025 release\n\n"
         "July 3rd Production Incident:\n"
         "Dr. Thornton provided a detailed post-mortem of the production database incident. "
         "She outlined the new deployment protocols implemented, including mandatory canary "
         "deployments and automated rollback triggers. Director Delgado-Ruiz inquired about "
         "customer impact. Dr. Thornton confirmed 340 customers were affected for approximately "
         "2.5 hours, with 3 customers requesting SLA credits totaling $45,000.\n\n"
         "Security and Compliance:\n"
         "  - SOC 2 Type II audit in progress (expected completion: December 2024)\n"
         "  - GDPR data processing agreements updated for EU customers\n"
         "  - Penetration testing completed with no critical findings\n"
         "  - Bug bounty program launched in August (12 submissions, 3 valid, all resolved)"),
        ("4. CFO FINANCIAL UPDATE\n"
         "Mr. Brannigan presented the financial review:\n\n"
         "Q3 2024 Results:\n"
         "  Revenue: $15.8M (7% above plan)\n"
         "  Gross Margin: 74.2% (up from 71.8% in Q2)\n"
         "  Operating Loss: ($2.1M) (improved from ($3.4M) in Q2)\n"
         "  Cash Position: $98.3M (post Series D)\n"
         "  Monthly Burn Rate: $4.2M\n"
         "  Runway: 23.4 months at current burn\n\n"
         "Series D Closing:\n"
         "The $85M Series D round closed on September 15, led by Sequoia Capital with "
         "participation from existing investors Andreessen Horowitz and Accel Partners. "
         "Pre-money valuation: $1.115B. The round includes a $15M secondary component "
         "for early employee liquidity.\n\n"
         "Director Ashworth asked about path to profitability. Mr. Brannigan projected "
         "cash-flow breakeven by Q4 2025, assuming planned revenue growth and controlled "
         "hiring pace."),
        ("5. COMPENSATION COMMITTEE REPORT\n"
         "Director Delgado-Ruiz presented the Compensation Committee recommendations:\n\n"
         "  a) 2024 Executive Bonus Pool: Approved at $1.8M (based on 112% plan attainment)\n"
         "  b) Dr. Thornton Annual Review: Performance rated 'Exceeds Expectations'\n"
         "     - Base salary increase: $425,000 -> $465,000 (effective January 1, 2025)\n"
         "     - Supplemental equity grant: 50,000 additional stock options at current FMV\n"
         "     - Retention bonus: $100,000 payable upon 2-year continued employment\n"
         "  c) Company-wide equity refresh program: 200,000 options allocated across top performers\n\n"
         "Director Hashimoto recused himself from the vote on item (c) due to his advisory "
         "relationship with a participating employee. The remaining directors approved all "
         "items unanimously.\n\n"
         "6. LEGAL UPDATE\n"
         "General Counsel Torres reported on:\n"
         "  - Patent portfolio: 14 patents granted, 8 applications pending\n"
         "  - Pending litigation: Carter v. Meridian (employment dispute) - settlement recommended\n"
         "  - Data processing agreements: 97% of enterprise customers on updated terms\n"
         "  - Export control compliance review completed (no issues identified)"),
        ("7. STRATEGIC DISCUSSION: IPO READINESS\n"
         "Chairman Whitfield led a confidential discussion on IPO readiness:\n\n"
         "Timeline: Targeting S-1 filing in Q3 2025 for potential Q4 2025 IPO\n\n"
         "Key Milestones Required:\n"
         "  - Two consecutive quarters of positive operating cash flow\n"
         "  - ARR exceeding $80M with >115% net revenue retention\n"
         "  - SOC 2 Type II and ISO 27001 certifications completed\n"
         "  - CFO hire or upgrade (Mr. Brannigan to be assessed for public company readiness)\n"
         "  - Audit committee composition (need one additional financial expert)\n\n"
         "Underwriter Selection:\n"
         "Goldman Sachs and Morgan Stanley have been engaged for bake-off presentations. "
         "Additional consideration for J.P. Morgan and Barclays as co-managers.\n\n"
         "Director Ashworth cautioned about market conditions and recommended maintaining "
         "optionality between IPO and additional private funding. The Board agreed to continue "
         "preparations while monitoring market conditions.\n\n"
         "[DISCUSSION UNDER NDA - DIRECTORS ONLY]"),
        ("8. GOVERNANCE MATTERS\n"
         "a) Board Composition:\n"
         "The Nominating Committee recommends adding a seventh board member with financial "
         "services expertise, aligned with the Westbrook relationship and planned expansion "
         "into financial vertical. Target: appointment by Q1 2025.\n\n"
         "b) D&O Insurance Renewal:\n"
         "General Counsel Torres presented the D&O insurance renewal proposal. Coverage "
         "increased from $20M to $35M in anticipation of IPO requirements. Premium: $420,000 "
         "annually (up from $285,000). Approved unanimously.\n\n"
         "c) Code of Conduct Update:\n"
         "Updated Code of Conduct incorporating AI ethics guidelines and expanded insider "
         "trading policy was presented. Directors to review and provide comments within "
         "two weeks. Final approval targeted for next meeting.\n\n"
         "9. EXECUTIVE SESSION\n"
         "Independent directors convened in executive session at 12:45 PM PDT. No actions "
         "taken. Executive session concluded at 1:15 PM PDT.\n\n"
         "10. ADJOURNMENT\n"
         "There being no further business, the meeting was adjourned at 1:20 PM PDT.\n\n"
         "Respectfully submitted,\n"
         "Amanda Foster, Corporate Secretary"),
        ("RESOLUTIONS ADOPTED BY UNANIMOUS WRITTEN CONSENT\n\n"
         "RESOLUTION 2024-09-01: SERIES D CLOSING\n"
         "RESOLVED, that the Board hereby ratifies and approves the closing of the Series D "
         "Preferred Stock financing on the terms set forth in the Stock Purchase Agreement "
         "dated September 10, 2024, and authorizes the issuance of 6,800,000 shares of "
         "Series D Preferred Stock at $12.50 per share.\n\n"
         "RESOLUTION 2024-09-02: EXECUTIVE COMPENSATION\n"
         "RESOLVED, that the Compensation Committee recommendations for FY2024 executive "
         "bonuses, Dr. Thornton's compensation adjustment, and the company-wide equity "
         "refresh program are hereby approved as presented.\n\n"
         "RESOLUTION 2024-09-03: D&O INSURANCE\n"
         "RESOLVED, that the Company is authorized to renew its Directors and Officers "
         "Liability Insurance policy with increased coverage of $35M as presented.\n\n"
         "RESOLUTION 2024-09-04: AUDITOR ENGAGEMENT\n"
         "RESOLVED, that Deloitte & Touche LLP is hereby engaged as the Company's "
         "independent auditor for fiscal year 2024-2025, at the fees set forth in the "
         "engagement letter dated September 20, 2024.\n\n"
         "CERTIFIED TRUE AND CORRECT:\n\n"
         "_______________________________\n"
         "Amanda Foster, Corporate Secretary\n"
         "Date: October 1, 2024"),
        ("EXHIBIT LIST AND DOCUMENT INDEX\n\n"
         "Documents referenced in Board Meeting of September 28, 2024:\n\n"
         "  A. CEO Quarterly Report (12 pages)\n"
         "  B. CTO Technology Roadmap Presentation (28 slides)\n"
         "  C. CFO Financial Package Q3 2024 (15 pages)\n"
         "  D. Series D Stock Purchase Agreement (executed copy)\n"
         "  E. Compensation Committee Report and Recommendations\n"
         "  F. SOC 2 Type II Audit Progress Report\n"
         "  G. D&O Insurance Renewal Proposal\n"
         "  H. Updated Code of Conduct (redlined version)\n"
         "  I. Patent Portfolio Summary\n"
         "  J. Litigation Status Report (Carter v. Meridian)\n\n"
         "Note: Documents A through J are maintained in the Company's secure board portal "
         "(Diligent Boards) and are available to directors upon request.\n\n"
         "CONFIDENTIALITY NOTICE:\n"
         "These minutes contain confidential and privileged information of Meridian "
         "Technologies, Inc. Unauthorized disclosure, copying, or distribution is strictly "
         "prohibited and may constitute a violation of applicable securities laws."),
    ]

    for i, body in enumerate(board_pages):
        page = doc.new_page(width=W, height=H)
        rect = pymupdf.Rect(54, 80, W - 54, H - 60)
        page.insert_textbox(rect, body, fontsize=10, fontname="helv", color=(0, 0, 0))
        add_header_footer(page, 21 + i)


def create_exhibit_5(doc):
    """Exhibit 5 (pages 28-35): Intellectual Property Assignment"""
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(130, 90), "INTELLECTUAL PROPERTY ASSIGNMENT AGREEMENT", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(200, 115), "Effective Date: April 1, 2024", fontsize=11, fontname="helv", color=(0, 0, 0))

    rect = pymupdf.Rect(54, 150, W - 54, H - 60)
    page.insert_textbox(rect,
        "This Intellectual Property Assignment Agreement ('IP Agreement') is made by and between "
        "Meridian Technologies, Inc., a Delaware corporation ('Company'), and Dr. Katherine R. "
        "Thornton ('Assignor'), in connection with Assignor's employment with the Company.\n\n"
        "RECITALS\n\n"
        "WHEREAS, Assignor possesses specialized knowledge and expertise in distributed systems "
        "architecture, machine learning pipeline optimization, and cloud-native platform design;\n\n"
        "WHEREAS, Company desires to engage Assignor's services and Assignor will have access to "
        "Company's proprietary technology and trade secrets;\n\n"
        "WHEREAS, the parties wish to define the ownership of intellectual property created during "
        "the course of Assignor's employment;\n\n"
        "NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth herein "
        "and in the Employment Agreement of even date, the parties agree as follows:\n\n"
        "1. DEFINITIONS\n\n"
        "'Assigned IP' means all inventions, discoveries, improvements, works of authorship, designs, "
        "formulas, algorithms, software code, data structures, architectures, processes, and "
        "know-how, whether or not patentable or copyrightable, that are: (a) conceived, developed, "
        "or reduced to practice by Assignor, alone or jointly, during the period of employment; and "
        "(b) relate to the Company's actual or demonstrably anticipated business, research, or "
        "development activities.",
        fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_header_footer(page, 28)

    ip_pages = [
        ("2. ASSIGNMENT OF RIGHTS\n\n"
         "2.1 Present Assignment. Assignor hereby irrevocably assigns, transfers, and conveys to "
         "Company all right, title, and interest in and to all Assigned IP, including all patent "
         "rights, copyrights, trade secret rights, and any other intellectual property rights therein.\n\n"
         "2.2 Future Assignment. Assignor agrees to promptly disclose and assign to Company all "
         "Assigned IP conceived or developed during the employment period.\n\n"
         "2.3 Moral Rights. To the extent permitted by law, Assignor waives all moral rights in the "
         "Assigned IP, including rights of attribution and integrity.\n\n"
         "2.4 Cooperation. Assignor agrees to execute all documents and take all actions reasonably "
         "requested by Company to perfect, evidence, and enforce Company's rights in the Assigned IP, "
         "including patent applications, copyright registrations, and assignments.\n\n"
         "3. PRIOR INVENTIONS\n\n"
         "3.1 Disclosure. Assignor has disclosed on Schedule A all inventions, improvements, and "
         "works of authorship made by Assignor prior to employment ('Prior Inventions').\n\n"
         "3.2 License. Assignor grants Company a non-exclusive, royalty-free, irrevocable, "
         "worldwide license to use, modify, and distribute any Prior Invention that is incorporated "
         "into Company products or services, solely to the extent necessary for Company's business."),
        ("4. EXCLUDED INVENTIONS\n\n"
         "4.1 California Labor Code Section 2870. Assignor is notified that the assignment provisions "
         "of this Agreement do not apply to any invention that qualifies fully under California Labor "
         "Code Section 2870, which provides:\n\n"
         "'Any provision in an employment agreement which provides that an employee shall assign, or "
         "offer to assign, any of his or her rights in an invention to his or her employer shall not "
         "apply to an invention that the employee developed entirely on his or her own time without "
         "using the employer's equipment, supplies, facilities, or trade secret information except "
         "for those inventions that either: (1) Relate at the time of conception or reduction to "
         "practice of the invention to the employer's business, or actual or demonstrably anticipated "
         "research or development of the employer. (2) Result from any work performed by the employee "
         "for the employer.'\n\n"
         "5. RECORDS AND DISCLOSURE\n\n"
         "5.1 Assignor shall maintain adequate written records of all Assigned IP, including dates "
         "of conception, development notes, and contributor identification.\n\n"
         "5.2 Assignor shall make prompt written disclosure to Company's Legal Department of any "
         "invention or discovery that may constitute Assigned IP, using the Company's standard "
         "Invention Disclosure Form."),
        ("6. ENFORCEMENT AND REMEDIES\n\n"
         "6.1 Injunctive Relief. Assignor acknowledges that any breach of this Agreement would cause "
         "irreparable harm to Company for which monetary damages would be inadequate. Company shall "
         "be entitled to seek injunctive relief without the necessity of proving actual damages or "
         "posting a bond.\n\n"
         "6.2 Attorney's Fees. The prevailing party in any action to enforce this Agreement shall be "
         "entitled to recover reasonable attorney's fees and costs.\n\n"
         "6.3 Survival. The obligations under Sections 2, 3, and 6 shall survive termination of "
         "employment for any reason.\n\n"
         "7. REPRESENTATIONS AND WARRANTIES\n\n"
         "Assignor represents and warrants that:\n"
         "(a) Assignor has full authority to enter into this Agreement;\n"
         "(b) The execution of this Agreement does not conflict with any prior obligation;\n"
         "(c) All Prior Inventions have been fully disclosed on Schedule A;\n"
         "(d) Assignor will not incorporate any third-party proprietary material into Assigned IP "
         "without Company's prior written consent.\n\n"
         "8. MISCELLANEOUS\n\n"
         "8.1 Governing Law. This Agreement shall be governed by the laws of the State of California.\n"
         "8.2 Entire Agreement. This Agreement, together with the Employment Agreement, constitutes "
         "the entire agreement regarding IP assignment.\n"
         "8.3 Severability. If any provision is held unenforceable, the remaining provisions continue "
         "in full force and effect.\n"
         "8.4 Amendment. This Agreement may be amended only by written instrument signed by both parties."),
        ("SCHEDULE A: PRIOR INVENTIONS OF DR. KATHERINE R. THORNTON\n\n"
         "The following is a complete list of inventions and intellectual property developed by "
         "Dr. Thornton prior to her employment with Meridian Technologies, Inc.:\n\n"
         "1. DistribCache v2.0 - Open-source distributed caching framework\n"
         "   Status: Published on GitHub under Apache 2.0 license\n"
         "   Description: Consistent hashing-based cache distribution system\n"
         "   Relevance: May be referenced in Company platform architecture\n\n"
         "2. Neural Pipeline Optimizer - Research prototype\n"
         "   Status: Described in published paper (IEEE ICDE 2023)\n"
         "   Description: ML-based query optimization for distributed databases\n"
         "   Relevance: Concepts may inform Company's ML pipeline development\n\n"
         "3. StreamGraph Analytics Engine - Proprietary (Stanford research)\n"
         "   Status: Licensed to Stanford University; Assignor retains improvement rights\n"
         "   Description: Real-time graph analytics on streaming data\n"
         "   Relevance: No anticipated overlap with Company business\n\n"
         "4. Secure Multi-Party Computation Library - Open-source\n"
         "   Status: Published under MIT license\n"
         "   Description: Privacy-preserving computation primitives\n"
         "   Relevance: May be incorporated into Company's compliance module\n\n"
         "Assignor certifies this list is complete and accurate as of the date of this Agreement."),
        ("SCHEDULE B: COMPANY INVENTIONS ASSIGNED TO DATE\n\n"
         "The following inventions have been disclosed and assigned by Dr. Thornton during her "
         "employment with Meridian Technologies, Inc. (April 1, 2024 - September 30, 2024):\n\n"
         "Invention Disclosure #MT-2024-017:\n"
         "  Title: Adaptive Resource Allocation in Multi-Tenant Cloud Environments\n"
         "  Date Conceived: April 28, 2024\n"
         "  Co-inventors: Dr. K. Thornton, David Park\n"
         "  Status: Patent application filed (US Provisional No. 63/XXX,XXX)\n\n"
         "Invention Disclosure #MT-2024-023:\n"
         "  Title: Predictive Scaling Algorithm for Containerized Workloads\n"
         "  Date Conceived: June 15, 2024\n"
         "  Co-inventors: Dr. K. Thornton\n"
         "  Status: Under review by patent counsel\n\n"
         "Invention Disclosure #MT-2024-031:\n"
         "  Title: Zero-Copy Data Pipeline Architecture for ML Training Workflows\n"
         "  Date Conceived: August 22, 2024\n"
         "  Co-inventors: Dr. K. Thornton, Lisa Wang, Marcus Rodriguez\n"
         "  Status: Provisional patent application in preparation\n\n"
         "Invention Disclosure #MT-2024-038:\n"
         "  Title: Federated Query Processing with Differential Privacy Guarantees\n"
         "  Date Conceived: September 10, 2024\n"
         "  Co-inventors: Dr. K. Thornton, Sarah Chen\n"
         "  Status: Initial disclosure submitted; review pending"),
        ("SIGNATURES\n\n"
         "IN WITNESS WHEREOF, the parties have executed this Intellectual Property Assignment "
         "Agreement as of the Effective Date.\n\n\n"
         "MERIDIAN TECHNOLOGIES, INC.\n\n\n"
         "By: _______________________________\n"
         "    James R. Whitfield\n"
         "    Chief Executive Officer\n"
         "    Date: April 1, 2024\n\n\n\n"
         "ASSIGNOR\n\n\n"
         "_______________________________\n"
         "Dr. Katherine R. Thornton\n"
         "Date: April 1, 2024\n\n\n\n"
         "WITNESSED BY:\n\n\n"
         "_______________________________\n"
         "Rebecca Torres, Esq.\n"
         "General Counsel\n"
         "Date: April 1, 2024\n\n\n"
         "NOTARIZATION:\n\n"
         "State of California\n"
         "County of San Francisco\n\n"
         "On April 1, 2024, before me, the undersigned notary public, personally appeared "
         "Dr. Katherine R. Thornton, proved to me on the basis of satisfactory evidence to "
         "be the person whose name is subscribed to the within instrument and acknowledged "
         "to me that she executed the same in her authorized capacity.\n\n"
         "_______________________________\n"
         "Notary Public\n"
         "My Commission Expires: December 31, 2026"),
        ("APPENDIX: MERIDIAN TECHNOLOGIES INVENTION DISCLOSURE FORM\n\n"
         "Instructions: Complete this form for any invention, discovery, improvement, or work "
         "of authorship that may qualify as Assigned IP under your IP Assignment Agreement.\n\n"
         "1. Title of Invention: _________________________________________\n\n"
         "2. Date Conceived: _____________ Date Reduced to Practice: _____________\n\n"
         "3. Inventor(s) (list all contributors):\n"
         "   Name: ________________________ Employee ID: ____________\n"
         "   Name: ________________________ Employee ID: ____________\n"
         "   Name: ________________________ Employee ID: ____________\n\n"
         "4. Description (attach additional pages if needed):\n"
         "_________________________________________________________________\n"
         "_________________________________________________________________\n"
         "_________________________________________________________________\n\n"
         "5. Was any Company equipment, supplies, or facilities used?  [ ] Yes  [ ] No\n\n"
         "6. Was any Company trade secret information used?  [ ] Yes  [ ] No\n\n"
         "7. Does this relate to Company business or R&D?  [ ] Yes  [ ] No\n\n"
         "8. Was this developed during working hours?  [ ] Yes  [ ] No  [ ] Partially\n\n"
         "9. Any third-party IP incorporated?  [ ] Yes  [ ] No\n"
         "   If Yes, describe: ____________________________________________\n\n"
         "10. Potential commercial applications:\n"
         "_________________________________________________________________\n\n"
         "Inventor Signature: ________________________ Date: ____________\n"
         "Manager Approval: _________________________ Date: ____________\n"
         "Legal Review: _____________________________ Date: ____________"),
    ]

    for i, body in enumerate(ip_pages):
        page = doc.new_page(width=W, height=H)
        rect = pymupdf.Rect(54, 80, W - 54, H - 60)
        page.insert_textbox(rect, body, fontsize=10, fontname="tiro", color=(0, 0, 0))
        add_header_footer(page, 29 + i)


def create_initial():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()

    create_exhibit_1(doc)   # Pages 1-7 (indices 0-6)
    create_exhibit_2(doc)   # Pages 8-14 (indices 7-13)
    create_exhibit_3(doc)   # Pages 15-19 (indices 14-18)
    create_exhibit_4(doc)   # Pages 20-27 (indices 19-26)
    create_exhibit_5(doc)   # Pages 28-35 (indices 27-34)

    assert doc.page_count == 35, f"Expected 35 pages, got {doc.page_count}"

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 35')

    # GUI-ready: open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
