"""
Initial Setup: Create a 22-page budget proposal PDF with no headers
Task ID: pdf_fin_030
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_030'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/budget_proposal_2025.pdf'

# Page layout constants
PAGE_W, PAGE_H = 612, 792  # US Letter
MARGIN_LEFT = 72
MARGIN_RIGHT = 540
MARGIN_TOP = 72
CONTENT_WIDTH = MARGIN_RIGHT - MARGIN_LEFT


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


def add_page_content(doc, title, body_lines, page_num):
    """Add a page with title and body text lines."""
    page = doc.new_page(width=PAGE_W, height=PAGE_H)

    # Page title
    page.insert_text(
        pymupdf.Point(MARGIN_LEFT, MARGIN_TOP),
        title,
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.1, 0.3),
    )

    # Underline for title
    shape = page.new_shape()
    shape.draw_line(
        pymupdf.Point(MARGIN_LEFT, MARGIN_TOP + 6),
        pymupdf.Point(MARGIN_RIGHT, MARGIN_TOP + 6),
    )
    shape.finish(color=(0.3, 0.3, 0.5), width=0.8)
    shape.commit()

    # Body text
    y = MARGIN_TOP + 36
    for line in body_lines:
        if y > 740:
            break
        if line.startswith("##"):
            # Sub-heading
            page.insert_text(
                pymupdf.Point(MARGIN_LEFT, y),
                line[2:].strip(),
                fontsize=12,
                fontname="hebo",
                color=(0.15, 0.15, 0.35),
            )
            y += 20
        elif line.startswith("|"):
            # Table row
            page.insert_text(
                pymupdf.Point(MARGIN_LEFT + 10, y),
                line,
                fontsize=9,
                fontname="cour",
                color=(0, 0, 0),
            )
            y += 14
        else:
            # Regular paragraph text
            rect = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, y + 60)
            excess = page.insert_textbox(
                rect, line,
                fontsize=10,
                fontname="helv",
                color=(0.1, 0.1, 0.1),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )
            y += 60 - max(excess, 0) + 6

    # Page number at bottom center
    page.insert_text(
        pymupdf.Point(PAGE_W / 2 - 10, 770),
        str(page_num),
        fontsize=9,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    return page


def create_initial():
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()

    # -- Page 1: Cover Page --
    p = doc.new_page(width=PAGE_W, height=PAGE_H)
    p.insert_text(pymupdf.Point(150, 280), "Zenith Corporation", fontsize=28, fontname="hebo", color=(0.05, 0.1, 0.3))
    p.insert_text(pymupdf.Point(155, 330), "FY2025 Budget Proposal", fontsize=22, fontname="hebo", color=(0.2, 0.2, 0.4))
    p.insert_text(pymupdf.Point(195, 380), "Fiscal Year: January - December 2025", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(195, 410), "Prepared by: Office of the CFO", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(195, 430), "Date: November 15, 2024", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(195, 450), "Version: 3.2 (Board Review Draft)", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    shape = p.new_shape()
    shape.draw_rect(pymupdf.Rect(130, 250, 482, 470))
    shape.finish(color=(0.1, 0.1, 0.3), width=2)
    shape.commit()

    # -- Page 2: Table of Contents --
    add_page_content(doc, "Table of Contents", [
        "## 1. Executive Summary .................. 3",
        "## 2. Revenue Projections ................. 4",
        "## 3. Operating Expenses .................. 6",
        "## 4. Capital Expenditures ................ 8",
        "## 5. Human Resources Budget .............. 10",
        "## 6. Marketing & Sales ................... 12",
        "## 7. Technology & Infrastructure ......... 14",
        "## 8. Research & Development .............. 16",
        "## 9. Risk Analysis & Contingency ......... 18",
        "## 10. Cash Flow Projections .............. 19",
        "## 11. Departmental Summaries ............. 20",
        "## 12. Appendices ......................... 22",
    ], 2)

    # -- Page 3: Executive Summary --
    add_page_content(doc, "1. Executive Summary", [
        "Zenith Corporation projects total revenue of $247.8 million for FY2025, representing a 12.3% increase over FY2024 actual revenue of $220.7 million. This growth is driven primarily by expansion in the Asia-Pacific region and the launch of our next-generation CloudSync platform.",
        "Total operating expenses are budgeted at $198.4 million, yielding projected operating income of $49.4 million and an operating margin of 19.9%. This represents an improvement of 1.8 percentage points over the current fiscal year.",
        "## Key Financial Highlights",
        "| Revenue Growth:           12.3% YoY ($247.8M vs $220.7M)",
        "| Operating Margin:         19.9% (up from 18.1%)",
        "| EBITDA:                   $62.1M (25.1% margin)",
        "| Capital Expenditures:     $31.5M (12.7% of revenue)",
        "| Headcount Growth:         +142 FTEs (8.2% increase)",
        "| R&D Investment:           $37.2M (15.0% of revenue)",
        "",
        "The board is requested to approve this budget proposal for immediate implementation effective January 1, 2025. All departmental allocations have been reviewed and endorsed by respective division heads during the October planning cycle.",
    ], 3)

    # -- Page 4: Revenue Projections Part 1 --
    add_page_content(doc, "2. Revenue Projections", [
        "## 2.1 Revenue by Business Segment",
        "| Segment              | FY2024 Actual | FY2025 Budget | Growth",
        "| ---------------------|---------------|---------------|-------",
        "| Enterprise Software  | $98.4M        | $112.6M       | 14.4%",
        "| Cloud Services       | $67.2M        | $79.8M        | 18.8%",
        "| Professional Svcs    | $32.1M        | $34.5M        |  7.5%",
        "| Maintenance & Support| $23.0M        | $20.9M        | -9.1%",
        "| Total                | $220.7M       | $247.8M       | 12.3%",
        "",
        "## 2.2 Revenue by Geography",
        "| Region               | FY2024 Actual | FY2025 Budget | Growth",
        "| ---------------------|---------------|---------------|-------",
        "| North America        | $132.4M       | $143.7M       |  8.5%",
        "| Europe (EMEA)        | $52.9M        | $59.3M        | 12.1%",
        "| Asia-Pacific         | $26.5M        | $34.6M        | 30.6%",
        "| Latin America        | $8.9M         | $10.2M        | 14.6%",
        "| Total                | $220.7M       | $247.8M       | 12.3%",
    ], 4)

    # -- Page 5: Revenue Projections Part 2 --
    add_page_content(doc, "2. Revenue Projections (continued)", [
        "## 2.3 Quarterly Revenue Forecast",
        "| Quarter | Enterprise  | Cloud     | Prof Svcs | Maint   | Total",
        "| --------|-------------|-----------|-----------|---------|------",
        "| Q1 2025 | $25.8M      | $18.2M    | $8.1M     | $5.4M   | $57.5M",
        "| Q2 2025 | $27.3M      | $19.5M    | $8.4M     | $5.3M   | $60.5M",
        "| Q3 2025 | $28.9M      | $20.8M    | $8.7M     | $5.2M   | $63.6M",
        "| Q4 2025 | $30.6M      | $21.3M    | $9.3M     | $5.0M   | $66.2M",
        "| Total   | $112.6M     | $79.8M    | $34.5M    | $20.9M  | $247.8M",
        "",
        "## 2.4 Key Revenue Assumptions",
        "Enterprise Software growth is driven by the v8.0 release scheduled for March 2025, which includes AI-powered analytics features. Cloud Services growth reflects migration of 340 existing on-premise customers to Zenith CloudSync, with an expected average ARR uplift of 28%.",
        "The decline in Maintenance & Support revenue reflects the strategic shift toward cloud-based delivery. Approximately 15% of legacy maintenance contracts are expected to convert to cloud subscriptions, with net-positive revenue impact captured in the Cloud Services line.",
    ], 5)

    # -- Page 6: Operating Expenses Part 1 --
    add_page_content(doc, "3. Operating Expenses", [
        "## 3.1 Expense Summary by Category",
        "| Category                | FY2024 Actual | FY2025 Budget | Change",
        "| ------------------------|---------------|---------------|-------",
        "| Cost of Revenue         | $68.4M        | $74.3M        |  8.6%",
        "| Sales & Marketing       | $44.1M        | $48.7M        | 10.4%",
        "| Research & Development  | $33.2M        | $37.2M        | 12.0%",
        "| General & Administrative| $21.3M        | $22.8M        |  7.0%",
        "| Facilities & Operations | $13.0M        | $15.4M        | 18.5%",
        "| Total OpEx              | $180.0M       | $198.4M       | 10.2%",
        "",
        "## 3.2 Cost of Revenue Breakdown",
        "Cost of Revenue includes hosting infrastructure ($28.1M), customer success staffing ($19.7M), third-party software licenses ($14.2M), and implementation delivery costs ($12.3M). The 8.6% increase is below revenue growth, improving gross margins from 69.0% to 70.0%.",
    ], 6)

    # -- Page 7: Operating Expenses Part 2 --
    add_page_content(doc, "3. Operating Expenses (continued)", [
        "## 3.3 Expense Ratio Analysis",
        "| Metric                  | FY2024  | FY2025  | Target",
        "| ------------------------|---------|---------|-------",
        "| Gross Margin            | 69.0%   | 70.0%   | 72.0%",
        "| S&M as % of Revenue     | 20.0%   | 19.7%   | 18.0%",
        "| R&D as % of Revenue     | 15.0%   | 15.0%   | 15.0%",
        "| G&A as % of Revenue     |  9.7%   |  9.2%   |  8.5%",
        "| Operating Margin        | 18.1%   | 19.9%   | 22.0%",
        "",
        "## 3.4 Headcount-Related Expenses",
        "Total compensation and benefits represent 62% of operating expenses at $123.0M. This includes base salaries ($89.4M), performance bonuses ($15.6M), equity-based compensation ($11.2M), and benefits/insurance ($6.8M).",
        "The FY2025 budget includes a 3.5% merit increase pool effective April 1, 2025, and a market adjustment pool of $2.1M for critical retention cases identified during the annual compensation review.",
    ], 7)

    # -- Page 8: Capital Expenditures Part 1 --
    add_page_content(doc, "4. Capital Expenditures", [
        "## 4.1 CapEx Summary",
        "| Category                  | FY2024 Actual | FY2025 Budget",
        "| --------------------------|---------------|-------------",
        "| Data Center Infrastructure| $8.2M         | $12.4M",
        "| Office Buildout           | $3.1M         | $5.8M",
        "| IT Equipment & Software   | $4.5M         | $6.3M",
        "| Lab & Testing Equipment   | $2.8M         | $3.2M",
        "| Vehicle Fleet             | $1.4M         | $1.6M",
        "| Security Systems          | $0.9M         | $2.2M",
        "| Total CapEx               | $20.9M        | $31.5M",
        "",
        "## 4.2 Data Center Expansion",
        "The $12.4M data center budget supports the buildout of our new Singapore facility (co-location at Equinix SG3), expansion of the Denver primary site with 400 additional rack units, and GPU cluster deployment for AI workloads. The Singapore facility is critical for APAC latency requirements and data sovereignty compliance.",
    ], 8)

    # -- Page 9: Capital Expenditures Part 2 --
    add_page_content(doc, "4. Capital Expenditures (continued)", [
        "## 4.3 Office Buildout Details",
        "| Location          | Project              | Budget  | Timeline",
        "| ------------------|----------------------|---------|--------",
        "| Austin HQ         | Floor 4 renovation   | $2.1M   | Q1-Q2",
        "| London Office     | New lease fitout      | $1.8M   | Q2-Q3",
        "| Singapore Office  | New office setup      | $1.2M   | Q1",
        "| Toronto Office    | Expansion (20 seats)  | $0.7M   | Q3",
        "| Total             |                      | $5.8M   |",
        "",
        "## 4.4 CapEx ROI Projections",
        "The data center investment is projected to deliver $4.8M in annual hosting cost savings beginning Q3 2025, representing a 2.6-year payback period. The Singapore facility alone is expected to enable $8.2M in incremental APAC revenue by reducing latency to sub-50ms for enterprise customers in the region.",
        "All capital projects above $500K have been reviewed by the Capital Allocation Committee and assigned priority scores based on strategic alignment, financial return, and risk profile.",
    ], 9)

    # -- Page 10: Human Resources Budget Part 1 --
    add_page_content(doc, "5. Human Resources Budget", [
        "## 5.1 Headcount Plan",
        "| Department           | Current FTE | FY2025 Plan | Net Change",
        "| ---------------------|-------------|-------------|----------",
        "| Engineering          | 612         | 678         | +66",
        "| Sales                | 284         | 305         | +21",
        "| Customer Success     | 196         | 218         | +22",
        "| Marketing            | 87          | 95          | +8",
        "| G&A / Finance        | 142         | 152         | +10",
        "| Product Management   | 64          | 72          | +8",
        "| IT / Infrastructure  | 93          | 100         | +7",
        "| Total                | 1,478       | 1,620       | +142",
        "",
        "## 5.2 Hiring Timeline",
        "Hiring is front-loaded to Q1-Q2 to support the CloudSync v8.0 launch and APAC expansion. Engineering hires focus on cloud infrastructure (24), AI/ML (18), security (12), and platform (12). Sales hires target APAC (12) and enterprise accounts (9).",
    ], 10)

    # -- Page 11: Human Resources Budget Part 2 --
    add_page_content(doc, "5. Human Resources Budget (continued)", [
        "## 5.3 Compensation & Benefits",
        "| Component                | FY2024   | FY2025   | Change",
        "| -------------------------|----------|----------|------",
        "| Base Salaries            | $82.1M   | $89.4M   | 8.9%",
        "| Performance Bonuses      | $14.2M   | $15.6M   | 9.9%",
        "| Equity Compensation      | $9.8M    | $11.2M   | 14.3%",
        "| Benefits & Insurance     | $6.2M    | $6.8M    | 9.7%",
        "| Total Compensation       | $112.3M  | $123.0M  | 9.5%",
        "",
        "## 5.4 Training & Development",
        "The L&D budget of $3.4M includes technical certification programs ($1.2M), leadership development ($0.8M), cloud skills training ($0.6M), conference attendance ($0.5M), and tuition reimbursement ($0.3M). Per-employee training spend increases from $2,050 to $2,100.",
        "A new AI Skills Academy launching in Q2 will train 200+ engineers on large language model integration, prompt engineering, and responsible AI practices, with an allocated budget of $0.4M.",
    ], 11)

    # -- Page 12: Marketing & Sales Part 1 --
    add_page_content(doc, "6. Marketing & Sales", [
        "## 6.1 Marketing Budget",
        "| Category               | FY2024 Actual | FY2025 Budget | Change",
        "| -----------------------|---------------|---------------|------",
        "| Digital Marketing      | $6.8M         | $7.9M         | 16.2%",
        "| Events & Conferences   | $4.2M         | $5.1M         | 21.4%",
        "| Content & Brand        | $3.1M         | $3.4M         | 9.7%",
        "| Product Marketing      | $2.4M         | $2.8M         | 16.7%",
        "| Partner Marketing      | $1.8M         | $2.2M         | 22.2%",
        "| Analyst Relations       | $0.9M         | $1.0M         | 11.1%",
        "| Total Marketing        | $19.2M        | $22.4M        | 16.7%",
        "",
        "## 6.2 Key Marketing Initiatives",
        "ZenithConnect 2025 (annual user conference) is budgeted at $2.8M with an expected attendance of 4,500 participants, up from 3,200 in 2024. The event will showcase CloudSync v8.0 and host the inaugural AI Innovation Summit track.",
    ], 12)

    # -- Page 13: Marketing & Sales Part 2 --
    add_page_content(doc, "6. Marketing & Sales (continued)", [
        "## 6.3 Sales Operations",
        "| Metric                   | FY2024 Actual | FY2025 Target",
        "| -------------------------|---------------|-------------",
        "| Quota-Carrying Reps      | 142           | 158",
        "| Average Quota            | $1.05M        | $1.12M",
        "| Quota Attainment (avg)   | 87%           | 90%",
        "| Sales Cycle (days)       | 94            | 85",
        "| Win Rate                 | 31%           | 34%",
        "| Customer Acquisition Cost| $18,400       | $16,800",
        "",
        "## 6.4 Channel Strategy",
        "The FY2025 channel program expands our partner ecosystem from 85 to 120 certified partners. A new tiered incentive structure allocates $4.2M in channel rebates and MDF (market development funds). Target: 35% of new bookings through channel by Q4 2025, up from 28% currently.",
        "Strategic alliance with Nakamura Systems (signed October 2024) is expected to generate $6.5M in co-sell revenue, with a joint go-to-market budget of $1.1M shared equally between parties.",
    ], 13)

    # -- Page 14: Technology & Infrastructure Part 1 --
    add_page_content(doc, "7. Technology & Infrastructure", [
        "## 7.1 IT Operating Budget",
        "| Category               | FY2024 Actual | FY2025 Budget",
        "| -----------------------|---------------|-------------",
        "| Cloud Hosting (AWS/GCP)| $18.4M        | $22.1M",
        "| SaaS Subscriptions     | $5.6M         | $6.8M",
        "| Network & Telecom      | $3.2M         | $3.5M",
        "| Cybersecurity Tools    | $2.8M         | $4.1M",
        "| IT Support & Helpdesk  | $2.1M         | $2.3M",
        "| Software Licenses      | $1.9M         | $2.0M",
        "| Total IT OpEx          | $34.0M        | $40.8M",
        "",
        "## 7.2 Cloud Infrastructure Strategy",
        "Multi-cloud strategy continues with primary workloads on AWS (65%), GCP for AI/ML (25%), and Azure for Microsoft ecosystem integration (10%). Reserved instance coverage target: 72% of steady-state compute, saving an estimated $3.8M versus on-demand pricing.",
    ], 14)

    # -- Page 15: Technology & Infrastructure Part 2 --
    add_page_content(doc, "7. Technology & Infrastructure (continued)", [
        "## 7.3 Cybersecurity Investments",
        "| Initiative                    | Budget  | Priority",
        "| ------------------------------|---------|--------",
        "| Zero Trust Architecture       | $1.2M   | Critical",
        "| SOC 2 Type II Compliance      | $0.8M   | High",
        "| Endpoint Detection & Response | $0.6M   | High",
        "| Identity & Access Management  | $0.5M   | Critical",
        "| Penetration Testing Program   | $0.4M   | Medium",
        "| Security Awareness Training   | $0.3M   | Medium",
        "| Incident Response Retainer    | $0.3M   | High",
        "| Total Cybersecurity           | $4.1M   |",
        "",
        "## 7.4 Technology Modernization",
        "The legacy ERP migration (SAP S/4HANA) enters Phase 2 in Q1 2025 with Finance and Supply Chain modules going live. Total remaining project cost: $4.2M (of $11.8M total program). Expected completion: Q3 2025. Annual licensing savings post-migration: $1.6M.",
    ], 15)

    # -- Page 16: R&D Part 1 --
    add_page_content(doc, "8. Research & Development", [
        "## 8.1 R&D Investment Overview",
        "| Category                 | FY2024 Actual | FY2025 Budget",
        "| -------------------------|---------------|-------------",
        "| Core Platform Dev        | $14.8M        | $15.2M",
        "| AI/ML Capabilities       | $5.4M         | $9.8M",
        "| Cloud Infrastructure     | $6.2M         | $5.6M",
        "| Mobile & UX              | $3.1M         | $3.2M",
        "| Quality & Testing        | $2.4M         | $2.1M",
        "| Innovation Lab           | $1.3M         | $1.3M",
        "| Total R&D                | $33.2M        | $37.2M",
        "",
        "## 8.2 AI/ML Investment Rationale",
        "The 81% increase in AI/ML spending reflects the strategic imperative to embed intelligent automation across the Zenith platform. Key initiatives include a predictive analytics engine for enterprise customers ($3.2M), natural language query interface ($2.8M), intelligent document processing ($2.1M), and anomaly detection for security monitoring ($1.7M).",
    ], 16)

    # -- Page 17: R&D Part 2 --
    add_page_content(doc, "8. Research & Development (continued)", [
        "## 8.3 Product Roadmap Alignment",
        "| Release     | Target Date | Key Features                  | R&D Cost",
        "| ------------|-------------|-------------------------------|--------",
        "| v8.0        | Mar 2025    | AI Analytics, New Dashboard   | $6.4M",
        "| v8.1        | Jun 2025    | Mobile Overhaul, API v3       | $4.1M",
        "| v8.2        | Sep 2025    | NLP Query, Doc Processing     | $5.2M",
        "| v8.3        | Dec 2025    | Security AI, Workflow Engine  | $4.8M",
        "",
        "## 8.4 Patent & IP Strategy",
        "The FY2025 IP budget of $1.8M covers 12 planned patent filings (primarily in AI/ML methods and cloud architecture), trademark registrations in 8 new international markets, and ongoing IP litigation defense. The Zenith AI patent portfolio is projected to reach 47 issued patents by year-end, up from 31 currently.",
        "Innovation Lab continues to operate with a 6-month horizon, evaluating emerging technologies including edge computing, quantum-resistant cryptography, and spatial computing interfaces.",
    ], 17)

    # -- Page 18: Risk Analysis --
    add_page_content(doc, "9. Risk Analysis & Contingency", [
        "## 9.1 Key Financial Risks",
        "| Risk Factor              | Probability | Impact  | Mitigation",
        "| -------------------------|-------------|---------|----------",
        "| APAC revenue shortfall   | Medium      | $8-12M  | Pipeline diversification",
        "| Cloud migration delays   | Medium      | $4-6M   | Parallel support model",
        "| Talent market pressure   | High        | $3-5M   | Retention packages",
        "| FX rate fluctuation      | Medium      | $2-4M   | Hedging program",
        "| Regulatory compliance    | Low         | $5-8M   | Proactive audit",
        "| Cybersecurity incident   | Low         | $10-20M | Insurance + SOC",
        "",
        "## 9.2 Contingency Reserve",
        "A contingency reserve of $8.5M (3.4% of total budget) is established for unplanned expenses. This reserve is governed by the CFO with board notification required for draws exceeding $2M. Historical usage: FY2024 reserve was $7.2M with $4.1M drawn (57% utilization).",
        "Scenario planning indicates that a 5% revenue shortfall would reduce operating margin to 16.8%, requiring $6.2M in discretionary expense reductions from marketing events and non-critical hiring.",
    ], 18)

    # -- Page 19: Cash Flow Projections --
    add_page_content(doc, "10. Cash Flow Projections", [
        "## 10.1 Cash Flow Summary",
        "| Category                    | Q1       | Q2       | Q3       | Q4       | Total",
        "| ----------------------------|----------|----------|----------|----------|------",
        "| Operating Cash Flow         | $10.2M   | $12.8M   | $14.1M   | $16.3M   | $53.4M",
        "| Capital Expenditures        | ($9.8M)  | ($8.4M)  | ($7.2M)  | ($6.1M)  | ($31.5M)",
        "| Free Cash Flow              | $0.4M    | $4.4M    | $6.9M    | $10.2M   | $21.9M",
        "| Debt Service                | ($1.2M)  | ($1.2M)  | ($1.2M)  | ($1.2M)  | ($4.8M)",
        "| Net Cash Flow               | ($0.8M)  | $3.2M    | $5.7M    | $9.0M    | $17.1M",
        "",
        "## 10.2 Liquidity Position",
        "Projected year-end cash balance: $64.2M (up from $47.1M at FY2024 close). The revolving credit facility of $50M remains undrawn and available. Working capital ratio is projected at 2.4x, above the 2.0x covenant requirement.",
        "## 10.3 Debt Profile",
        "Outstanding term loan: $38.0M at SOFR + 175bps, maturing June 2027. Annual principal payments of $4.0M. No refinancing planned for FY2025. Interest rate risk is hedged through a $25M interest rate swap at 4.25% fixed through maturity.",
    ], 19)

    # -- Page 20: Departmental Summaries Part 1 --
    add_page_content(doc, "11. Departmental Summaries", [
        "## 11.1 Engineering Division (VP: Sarah Chen)",
        "Total Budget: $68.4M | Headcount: 678 FTEs",
        "Priority: CloudSync v8.x platform delivery, AI capability buildout, Singapore engineering hub establishment (15 engineers by Q4). Technical debt reduction target: 20% of sprint capacity allocated to infrastructure modernization.",
        "",
        "## 11.2 Sales Division (VP: Marcus Rodriguez)",
        "Total Budget: $52.3M | Headcount: 305 FTEs",
        "Priority: APAC market penetration ($34.6M revenue target), enterprise upsell campaign (avg deal size increase from $285K to $340K), channel partner activation (120 certified partners). New vertical focus: healthcare and financial services.",
        "",
        "## 11.3 Customer Success Division (VP: Priya Sharma)",
        "Total Budget: $24.8M | Headcount: 218 FTEs",
        "Priority: Net revenue retention target of 118% (up from 114%), implementation backlog reduction (avg onboarding time from 45 to 30 days), launch of self-service portal for SMB segment.",
    ], 20)

    # -- Page 21: Departmental Summaries Part 2 --
    add_page_content(doc, "11. Departmental Summaries (continued)", [
        "## 11.4 Finance & Administration (CFO: David Kim)",
        "Total Budget: $18.6M | Headcount: 152 FTEs",
        "Priority: SAP S/4HANA Phase 2 completion, FP&A automation initiative ($0.8M investment for 40% reporting cycle reduction), SOX compliance program expansion for international entities, and treasury management optimization.",
        "",
        "## 11.5 Marketing Division (CMO: Elena Vasquez)",
        "Total Budget: $22.4M | Headcount: 95 FTEs",
        "Priority: ZenithConnect 2025 conference (4,500 attendees), brand refresh launch in Q2, demand generation pipeline target of $180M (3.6x coverage ratio), and ABM program expansion to top 200 enterprise accounts.",
        "",
        "## 11.6 Product Management (VP: James Okafor)",
        "Total Budget: $8.9M | Headcount: 72 FTEs",
        "Priority: AI feature adoption metrics (30% of enterprise customers by Q4), competitive displacement program (target: 50 wins from competitor X), UX research expansion (8 studies planned), and pricing model revision for cloud-native offerings.",
    ], 21)

    # -- Page 22: Appendices --
    add_page_content(doc, "12. Appendices", [
        "## Appendix A: Budget Approval History",
        "| Date          | Version | Reviewed By            | Status",
        "| --------------|---------|------------------------|--------",
        "| Sep 15, 2024  | 1.0     | Department Heads       | Draft",
        "| Oct 3, 2024   | 2.0     | Executive Committee    | Revised",
        "| Oct 22, 2024  | 2.5     | CFO Review             | Updated",
        "| Nov 1, 2024   | 3.0     | Audit Committee        | Endorsed",
        "| Nov 15, 2024  | 3.2     | Board of Directors     | Pending",
        "",
        "## Appendix B: Methodology Notes",
        "Revenue projections use a bottoms-up model based on pipeline analysis, historical conversion rates, and market growth assumptions from Gartner and IDC reports. Expense budgets reflect departmental submissions adjusted for corporate efficiency targets of 2% YoY improvement in key operational ratios.",
        "",
        "## Appendix C: Glossary",
        "ARR: Annual Recurring Revenue | CAC: Customer Acquisition Cost | FTE: Full-Time Equivalent | MDF: Market Development Funds | NRR: Net Revenue Retention | SOFR: Secured Overnight Financing Rate",
        "",
        "## Appendix D: Contact",
        "Budget inquiries: David Kim, CFO (d.kim@zenithcorp.com) | Technical questions: IT Budget Office (budget-ops@zenithcorp.com)",
    ], 22)

    # Set metadata
    doc.set_metadata({
        "title": "FY2025 Budget Proposal",
        "author": "Zenith Corporation - Office of the CFO",
        "subject": "Annual Budget Proposal for Fiscal Year 2025",
        "keywords": "budget, FY2025, Zenith, proposal, finance",
        "creator": "Zenith Financial Planning",
    })

    # Set TOC
    toc = [
        [1, "Executive Summary", 3],
        [1, "Revenue Projections", 4],
        [1, "Operating Expenses", 6],
        [1, "Capital Expenditures", 8],
        [1, "Human Resources Budget", 10],
        [1, "Marketing & Sales", 12],
        [1, "Technology & Infrastructure", 14],
        [1, "Research & Development", 16],
        [1, "Risk Analysis & Contingency", 18],
        [1, "Cash Flow Projections", 19],
        [1, "Departmental Summaries", 20],
        [1, "Appendices", 22],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 22')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
