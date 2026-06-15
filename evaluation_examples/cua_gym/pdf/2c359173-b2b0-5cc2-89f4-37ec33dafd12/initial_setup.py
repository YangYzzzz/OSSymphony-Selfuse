"""
Initial Setup: Create an unencrypted 8-page board minutes PDF
Task ID: pdf_fm_080
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_080'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS_DIR}/board_minutes.pdf'


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
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page dimensions ---
    W, H = 612, 792  # US Letter

    # --- Page 1: Cover Page ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 120), "ACME GLOBAL INDUSTRIES, INC.", fontsize=22, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 160), "Board of Directors Meeting Minutes", fontsize=18, fontname="hebo", color=(0.2, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 175), pymupdf.Point(540, 175))
    shape.finish(color=(0.2, 0.2, 0.5), width=2)
    shape.commit()
    page.insert_text(pymupdf.Point(72, 210), "Meeting Date: March 15, 2025", fontsize=13, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 230), "Location: Corporate Headquarters, 2400 Meridian Blvd, Suite 1200, San Francisco, CA", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 250), "Time: 9:00 AM - 12:30 PM (Pacific Time)", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 290), "CONFIDENTIAL", fontsize=16, fontname="hebo", color=(0.7, 0, 0))
    page.insert_text(pymupdf.Point(72, 320), "Prepared by: Victoria Langford, Corporate Secretary", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 340), "Distribution: Board Members Only", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))

    # --- Page 2: Attendees ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "1. ATTENDANCE AND QUORUM", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    y = 90
    page.insert_text(pymupdf.Point(72, y), "Directors Present:", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 20
    attendees = [
        "Robert A. Mitchell — Chairperson",
        "Dr. Sandra K. Nguyen — Vice Chairperson",
        "James T. Harrington — Independent Director",
        "Patricia M. Vasquez — Independent Director",
        "Dr. William R. Chen — Independent Director",
        "Eleanor J. Blackwood — Independent Director",
        "Michael S. Okonkwo — Director (CFO)",
        "Aisha R. Patel — Director (COO)",
    ]
    for att in attendees:
        page.insert_text(pymupdf.Point(90, y), f"• {att}", fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 18

    y += 10
    page.insert_text(pymupdf.Point(72, y), "Directors Absent:", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 20
    page.insert_text(pymupdf.Point(90, y), "• Thomas L. Rivera — Independent Director (excused, medical leave)", fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 30
    page.insert_text(pymupdf.Point(72, y), "Also Present:", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 20
    others = [
        "Victoria Langford — Corporate Secretary",
        "David Kimura — General Counsel",
        "Rachel Torres — Chief Technology Officer (for agenda item 4)",
        "Marcus Everly — VP of Investor Relations (for agenda item 5)",
    ]
    for o in others:
        page.insert_text(pymupdf.Point(90, y), f"• {o}", fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 18

    y += 15
    page.insert_text(pymupdf.Point(72, y), "A quorum being present, Chairperson Mitchell called the meeting to order at 9:03 AM.", fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 3: Approval of Minutes & CEO Report ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "2. APPROVAL OF PREVIOUS MINUTES", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    rect = pymupdf.Rect(72, 75, 540, 160)
    page.insert_textbox(rect,
        "The minutes of the regular board meeting held on January 18, 2025, were distributed to all "
        "directors prior to the meeting. Director Harrington moved to approve the minutes as presented. "
        "Director Vasquez seconded the motion. The motion carried unanimously (8-0) with no abstentions.",
        fontsize=11, fontname="helv", color=(0, 0, 0))

    page.insert_text(pymupdf.Point(72, 180), "3. CHAIRPERSON AND CEO REPORT", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    rect = pymupdf.Rect(72, 195, 540, 450)
    page.insert_textbox(rect,
        "Chairperson Mitchell presented the quarterly overview highlighting several key developments:\n\n"
        "Revenue for Q1 2025 reached $247.3 million, representing a 12.4% year-over-year increase. "
        "The EBITDA margin improved to 28.6%, up from 25.1% in the prior-year quarter. Net income "
        "totaled $38.9 million, or $2.14 per diluted share.\n\n"
        "The company successfully completed the acquisition of DataStream Analytics on February 28, 2025, "
        "for $156 million in cash and stock. Integration planning is on track with an expected completion "
        "date of Q3 2025. Early synergy estimates suggest annual cost savings of $18-22 million.\n\n"
        "Employee headcount grew to 4,287 worldwide, with notable hiring in the AI and machine learning "
        "division. Voluntary attrition remained low at 7.2% annualized.\n\n"
        "The Board discussed competitive positioning and market share trends in the enterprise software "
        "segment. Director Blackwood raised questions about the Asia-Pacific expansion timeline, which "
        "the Chairperson addressed by referencing the strategic plan milestones.",
        fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 4: Technology and Product Update ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "4. TECHNOLOGY AND PRODUCT UPDATE", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    rect = pymupdf.Rect(72, 75, 540, 420)
    page.insert_textbox(rect,
        "CTO Rachel Torres joined the meeting and presented the technology roadmap update:\n\n"
        "Product Development Highlights:\n"
        "• Platform v5.2 release scheduled for April 2025 with enhanced AI-driven analytics\n"
        "• Customer-facing API redesign completed, currently in beta with 23 enterprise clients\n"
        "• Cloud infrastructure migration to multi-region architecture is 78% complete\n"
        "• Mobile application redesign achieving 4.7-star rating in beta testing\n\n"
        "Research & Development:\n"
        "• R&D spending for Q1 was $41.2 million (16.7% of revenue)\n"
        "• Filed 14 new patent applications in quantum-resistant encryption and edge computing\n"
        "• Partnership with MIT Lincoln Laboratory on advanced threat detection progressing well\n\n"
        "Cybersecurity Posture:\n"
        "• SOC 2 Type II audit completed with zero findings\n"
        "• Implemented zero-trust network architecture across all production environments\n"
        "• Average incident response time reduced to 4.2 minutes from 11.8 minutes year-over-year\n\n"
        "Director Chen commended the security improvements and asked about post-quantum cryptography "
        "readiness. Torres confirmed the company is piloting NIST-approved algorithms in the development "
        "environment with full production deployment planned for Q4 2025.\n\n"
        "The Board discussed the competitive implications of the AI analytics features and the potential "
        "to differentiate from competitors in the mid-market segment.",
        fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 5: Financial Review ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "5. FINANCIAL REVIEW AND INVESTOR RELATIONS", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    rect = pymupdf.Rect(72, 75, 540, 440)
    page.insert_textbox(rect,
        "CFO Okonkwo and VP Marcus Everly presented the financial review:\n\n"
        "Q1 2025 Financial Summary:\n"
        "• Total Revenue: $247.3M (+12.4% YoY)\n"
        "• Recurring Revenue: $198.1M (80.1% of total, +15.7% YoY)\n"
        "• Gross Margin: 71.3% (up from 69.8%)\n"
        "• Operating Expenses: $134.6M (54.4% of revenue)\n"
        "• Free Cash Flow: $52.7M (21.3% margin)\n"
        "• Cash & Equivalents: $412.8M (post-acquisition)\n"
        "• Total Debt: $275.0M (debt-to-equity ratio: 0.42)\n\n"
        "Capital Allocation:\n"
        "• Quarterly dividend of $0.35/share approved (record date April 10, 2025)\n"
        "• Share repurchase program: $28.4M utilized in Q1 of $150M authorization\n"
        "• Capital expenditures: $19.8M focused on data center expansion\n\n"
        "Investor Relations Update:\n"
        "• Stock price performance: +18.3% YTD vs. S&P 500 +9.7%\n"
        "• Analyst consensus: 14 Buy, 4 Hold, 1 Sell\n"
        "• Next earnings call scheduled for April 24, 2025\n"
        "• Annual shareholder meeting set for June 12, 2025\n\n"
        "Director Nguyen requested additional analysis on the impact of the DataStream acquisition "
        "on cash flow projections for the remainder of the fiscal year. CFO Okonkwo agreed to "
        "circulate a supplemental analysis within two weeks.",
        fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 6: Governance and Compensation ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "6. GOVERNANCE AND COMPENSATION COMMITTEE REPORTS", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    rect = pymupdf.Rect(72, 75, 540, 440)
    page.insert_textbox(rect,
        "Governance Committee Report (Director Vasquez, Committee Chair):\n\n"
        "• Board composition review completed — recommendation to add one director with healthcare "
        "technology expertise by Q4 2025\n"
        "• Annual board self-evaluation process concluded with overall effectiveness rated 4.3/5.0\n"
        "• ESG reporting framework aligned with SASB and TCFD standards\n"
        "• Whistleblower hotline: 3 reports received in Q1, all investigated and resolved\n"
        "• Updated the Corporate Governance Guidelines to reflect new SEC rules on cybersecurity "
        "disclosure requirements\n\n"
        "Compensation Committee Report (Director Harrington, Committee Chair):\n\n"
        "• Executive compensation benchmarking study completed by Willis Towers Watson\n"
        "• Recommended CEO total compensation package of $4.8M (base: $950K, target bonus: 150%, "
        "LTIP: $2.4M in RSUs and performance shares)\n"
        "• Proposed amendments to the 2023 Equity Incentive Plan to increase the share reserve by "
        "2.5 million shares — to be presented at the annual shareholder meeting\n"
        "• Clawback policy updated to comply with Dodd-Frank final rules\n"
        "• Non-employee director compensation increased to $85,000 annual retainer plus $2,500 per "
        "committee meeting attended\n\n"
        "RESOLUTION 2025-03-001:\n"
        "Moved by Director Harrington, seconded by Director Blackwood: The Board approves the CEO "
        "compensation package as recommended by the Compensation Committee. Approved unanimously (7-0, "
        "CEO Mitchell recused).",
        fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 7: Risk Management and Strategic Items ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "7. RISK MANAGEMENT AND STRATEGIC INITIATIVES", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    rect = pymupdf.Rect(72, 75, 540, 440)
    page.insert_textbox(rect,
        "Risk Management Update (General Counsel David Kimura):\n\n"
        "• Enterprise Risk Assessment refreshed; top risks identified:\n"
        "  1. Cybersecurity and data privacy (residual risk: Medium-High)\n"
        "  2. Regulatory compliance — EU AI Act and SEC climate disclosure (Medium)\n"
        "  3. Key talent retention in AI/ML roles (Medium)\n"
        "  4. Geopolitical risks affecting supply chain (Medium-Low)\n"
        "  5. Interest rate environment impact on acquisition financing (Low)\n\n"
        "• Insurance program renewed with D&O coverage of $50M and cyber liability of $25M\n"
        "• Litigation update: Two pending matters (both classified as remote likelihood of loss)\n\n"
        "Strategic Initiatives Discussion:\n\n"
        "• Asia-Pacific Expansion: MOU signed with Toshiba Digital Solutions for distribution "
        "partnership in Japan. Singapore office lease signed, opening July 2025.\n"
        "• Vertical Market Strategy: Healthcare and financial services verticals now represent 38% "
        "of new ARR, up from 29% a year ago.\n"
        "• Sustainability Commitment: Carbon neutrality target accelerated from 2030 to 2028. "
        "Solar installations at primary data centers expected to offset 40% of energy consumption.\n\n"
        "RESOLUTION 2025-03-002:\n"
        "Moved by Director Nguyen, seconded by Director Chen: The Board authorizes management to "
        "proceed with the Singapore office establishment and Japan distribution partnership, with "
        "combined investment not to exceed $12 million. Approved (8-0).",
        fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 8: Adjournment ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "8. OTHER BUSINESS AND ADJOURNMENT", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    rect = pymupdf.Rect(72, 75, 540, 300)
    page.insert_textbox(rect,
        "Other Business:\n\n"
        "Director Patel raised the topic of board member continuing education, recommending that all "
        "directors complete a cybersecurity awareness program by the end of Q2 2025. The Board agreed "
        "by consensus.\n\n"
        "Director Blackwood inquired about the timeline for refreshing the company's five-year "
        "strategic plan. Chairperson Mitchell confirmed that a strategic planning offsite is scheduled "
        "for May 3-4, 2025, at the Ritz-Carlton Half Moon Bay.\n\n"
        "Next Meeting: The next regular board meeting is scheduled for May 17, 2025, at 9:00 AM PT.\n\n"
        "Adjournment:\n"
        "There being no further business, Director Vasquez moved to adjourn. Director Okonkwo seconded. "
        "The motion carried unanimously, and the meeting was adjourned at 12:22 PM.\n\n",
        fontsize=11, fontname="helv", color=(0, 0, 0))

    y = 340
    page.insert_text(pymupdf.Point(72, y), "Respectfully submitted,", fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 40
    page.insert_text(pymupdf.Point(72, y), "Victoria Langford", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 18
    page.insert_text(pymupdf.Point(72, y), "Corporate Secretary", fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 18
    page.insert_text(pymupdf.Point(72, y), "ACME Global Industries, Inc.", fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 40
    page.insert_text(pymupdf.Point(72, y), "Approved:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 25
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(300, y))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    y += 15
    page.insert_text(pymupdf.Point(72, y), "Robert A. Mitchell, Chairperson", fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 18
    page.insert_text(pymupdf.Point(72, y), "Date: _______________", fontsize=11, fontname="helv", color=(0, 0, 0))

    # Set metadata
    doc.set_metadata({
        "title": "Board of Directors Meeting Minutes - March 15, 2025",
        "author": "Victoria Langford",
        "subject": "ACME Global Industries Board Meeting",
        "keywords": "board minutes, corporate governance, Q1 2025",
        "creator": "ACME Global Industries",
        "producer": "ACME Document Services",
    })

    # Set TOC
    toc = [
        [1, "Attendance and Quorum", 2],
        [1, "Approval of Previous Minutes", 3],
        [1, "Chairperson and CEO Report", 3],
        [1, "Technology and Product Update", 4],
        [1, "Financial Review and Investor Relations", 5],
        [1, "Governance and Compensation Committee Reports", 6],
        [1, "Risk Management and Strategic Initiatives", 7],
        [1, "Other Business and Adjournment", 8],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Ensure qpdf is available (task states it is installed)
    result = subprocess.run(['which', 'qpdf'], capture_output=True, text=True)
    if result.returncode != 0:
        print('Installing qpdf...')
        subprocess.run('echo "password" | sudo -S apt-get update -qq', shell=True, capture_output=True)
        subprocess.run('echo "password" | sudo -S apt-get install -y -qq qpdf', shell=True, capture_output=True)
        print('qpdf installed.')
    else:
        print(f'qpdf already available at: {result.stdout.strip()}')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
