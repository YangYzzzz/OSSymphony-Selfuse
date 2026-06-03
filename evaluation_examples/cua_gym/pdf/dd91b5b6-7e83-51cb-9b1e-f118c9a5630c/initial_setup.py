"""
Initial Setup: Create 6 PDF report files in /home/user/Documents/reports/
Task ID: pdf_gf2_026
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_026'
REPORTS_DIR = f'{WORKDIR}/Documents/reports'


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


def add_text_page(doc, page_num_label, title, paragraphs, width=612, height=792):
    """Add a page with title and paragraph text to a document."""
    page = doc.new_page(width=width, height=height)

    # Title
    page.insert_text(
        pymupdf.Point(72, 60),
        title,
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.1, 0.3),
    )

    # Separator line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 72), pymupdf.Point(540, 72))
    shape.finish(color=(0.3, 0.3, 0.5), width=1.5)
    shape.commit()

    # Body text
    y_offset = 100
    for para in paragraphs:
        rect = pymupdf.Rect(72, y_offset, 540, y_offset + 80)
        page.insert_textbox(
            rect,
            para,
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )
        y_offset += 85

    # Page number footer
    page.insert_text(
        pymupdf.Point(290, 775),
        f"Page {page_num_label}",
        fontsize=9,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )
    return page


def create_report_q1():
    """Q1 Report - 3 pages"""
    doc = pymupdf.open()
    add_text_page(doc, 1, "Q1 2025 Financial Report",
                  [
                      "Executive Summary: The first quarter of 2025 showed strong revenue growth across all divisions, "
                      "with total consolidated revenue reaching $14.2 million, a 12% increase year-over-year.",
                      "Key highlights include the successful launch of the Meridian product line in February, which "
                      "contributed $2.1 million in new revenue. Operating margins improved to 18.3% from 15.7% in Q4 2024.",
                      "The Engineering division led growth with a 22% increase driven by enterprise contract renewals "
                      "and expansion into the Asia-Pacific market segment.",
                      "Cash position remains healthy at $8.4 million with no outstanding credit facility draws. "
                      "Capital expenditures were $1.2 million, primarily for data center expansion.",
                  ])
    add_text_page(doc, 2, "Revenue Breakdown by Division",
                  [
                      "Engineering Services: $5.8M (Q4: $4.7M) - Growth driven by three new enterprise clients "
                      "and the renewal of the Vertex Technologies contract valued at $1.4M annually.",
                      "Product Sales: $4.9M (Q4: $4.3M) - Meridian launch exceeded projections by 15%. Legacy "
                      "product lines maintained steady performance with minimal churn.",
                      "Consulting: $2.3M (Q4: $2.1M) - Strategic advisory engagements increased with the addition "
                      "of six new mid-market clients in the healthcare vertical.",
                      "Support & Maintenance: $1.2M (Q4: $1.1M) - Renewal rates held at 94%, with average "
                      "contract value increasing 8% due to premium tier adoption.",
                  ])
    add_text_page(doc, 3, "Outlook and Projections",
                  [
                      "Q2 2025 Guidance: Revenue is projected at $15.0-15.5 million, reflecting continued momentum "
                      "from the Meridian product line and seasonal strength in consulting engagements.",
                      "Risk Factors: Supply chain disruptions in the semiconductor sector may impact hardware delivery "
                      "timelines. The team is actively diversifying supplier relationships to mitigate this risk.",
                      "Strategic Initiatives: The board has approved a $3.5M investment in AI-powered analytics "
                      "capabilities, expected to generate revenue starting Q4 2025.",
                  ])
    output = os.path.join(REPORTS_DIR, 'report_q1.pdf')
    doc.save(output)
    doc.close()
    print(f'Created: {output} (3 pages)')


def create_report_q2():
    """Q2 Report - 4 pages"""
    doc = pymupdf.open()
    add_text_page(doc, 1, "Q2 2025 Financial Report",
                  [
                      "Executive Summary: Q2 2025 delivered record revenue of $15.8 million, surpassing guidance. "
                      "The company achieved its first quarter of positive free cash flow since the restructuring.",
                      "Net income reached $1.9 million, a significant improvement from the $0.3 million loss in Q2 2024. "
                      "Employee headcount grew to 342, with key hires in the product engineering and sales teams.",
                      "The Meridian product line continued its strong trajectory with $3.4 million in quarterly revenue, "
                      "now representing 21.5% of total company revenue.",
                  ])
    add_text_page(doc, 2, "Operational Metrics",
                  [
                      "Customer Acquisition: 47 new accounts added (vs. 31 in Q1), with average deal size of $68,000. "
                      "Enterprise segment grew by 18 accounts with average contract value of $142,000.",
                      "Customer Retention: Net revenue retention rate improved to 112%, driven by upsell of premium "
                      "features and expanded scope of existing consulting engagements.",
                      "Pipeline: Qualified pipeline stands at $42.3 million, a 28% increase from Q1. "
                      "Win rate on qualified opportunities improved to 34% from 29%.",
                  ])
    add_text_page(doc, 3, "Department Performance",
                  [
                      "Engineering (Sarah Chen, VP): Shipped 14 product releases including the Meridian 2.0 update "
                      "with AI-assisted analytics. Team grew from 89 to 104 engineers.",
                      "Sales (Marcus Johnson, SVP): Closed the Pinnacle Healthcare deal worth $2.1M ARR. "
                      "Built out the channel partner program with 12 new certified partners.",
                      "Marketing (Lisa Park, CMO): Brand awareness increased 35% per survey data. Digital marketing "
                      "spend efficiency improved with CAC dropping from $4,200 to $3,100.",
                  ])
    add_text_page(doc, 4, "Financial Statements Summary",
                  [
                      "Balance Sheet: Total assets $32.4M. Cash and equivalents $9.1M. Accounts receivable $6.8M "
                      "with DSO of 39 days, improved from 44 days in Q1.",
                      "Income Statement: Gross margin 62.3% (Q1: 60.1%). R&D expense $3.2M (20.2% of revenue). "
                      "SG&A expense $4.1M (25.9% of revenue).",
                      "Cash Flow: Operating cash flow $2.8M. Free cash flow $1.6M after $1.2M in capex. "
                      "No debt repayment obligations until Q3 2026.",
                  ])
    output = os.path.join(REPORTS_DIR, 'report_q2.pdf')
    doc.save(output)
    doc.close()
    print(f'Created: {output} (4 pages)')


def create_report_q3():
    """Q3 Report - 5 pages"""
    doc = pymupdf.open()
    add_text_page(doc, 1, "Q3 2025 Financial Report",
                  [
                      "Executive Summary: Revenue reached $16.4 million in Q3, representing 4% sequential growth. "
                      "The company maintained profitability with net income of $2.1 million.",
                      "International expansion progressed with the opening of the Singapore office, adding $1.3M "
                      "in APAC revenue. The European market showed signs of recovery with 8% growth.",
                  ])
    add_text_page(doc, 2, "Product Performance",
                  [
                      "Meridian Suite: $4.1M revenue (+21% QoQ). Enterprise adoption accelerated with 28 new "
                      "logos. The AI analytics module showed 89% user engagement rate.",
                      "Legacy Products: $3.8M revenue (-5% QoQ). Managed decline through migration incentives. "
                      "42% of legacy customers have migrated or committed to migrate to Meridian.",
                      "Professional Services: $2.9M revenue (+8% QoQ). Implementation backlog grew to 14 weeks, "
                      "indicating strong demand but capacity constraints.",
                  ])
    add_text_page(doc, 3, "Market Analysis",
                  [
                      "Competitive Landscape: Two new entrants in the mid-market segment. Our differentiation "
                      "through integrated AI capabilities and vertical-specific solutions remains strong.",
                      "Pricing Strategy: Average selling price increased 6% through value-based pricing. "
                      "Premium tier adoption reached 38% of new customers, up from 25% in Q2.",
                      "Industry Trends: Growing demand for unified platforms driving consolidation. "
                      "Our all-in-one approach aligns well with buyer preferences.",
                  ])
    add_text_page(doc, 4, "Risk Assessment",
                  [
                      "Talent Acquisition: Engineering hiring remains competitive. Offer acceptance rate dropped "
                      "to 62%. Implementing retention bonuses and flexible work arrangements.",
                      "Regulatory: New data privacy regulations in the EU may require product modifications. "
                      "Compliance team estimates $400K in implementation costs for Q4.",
                      "Supply Chain: Hardware component lead times have stabilized at 8-10 weeks. "
                      "Secondary supplier agreements now cover 80% of critical components.",
                  ])
    add_text_page(doc, 5, "Q4 Outlook",
                  [
                      "Revenue Guidance: $17.0-17.5M, reflecting seasonal strength and pipeline conversion. "
                      "Full-year revenue expected to exceed $63 million, surpassing initial guidance.",
                      "Strategic Priorities: Complete Singapore office build-out. Launch Meridian 3.0 with "
                      "collaborative workspace features. Expand channel partner program to 25 partners.",
                      "Capital Allocation: Board approved $5M share repurchase program. Evaluating one "
                      "strategic acquisition target in the data visualization space.",
                  ])
    output = os.path.join(REPORTS_DIR, 'report_q3.pdf')
    doc.save(output)
    doc.close()
    print(f'Created: {output} (5 pages)')


def create_report_q4():
    """Q4 Report - 6 pages"""
    doc = pymupdf.open()
    add_text_page(doc, 1, "Q4 2025 Financial Report",
                  [
                      "Executive Summary: Q4 capped a transformative year with record revenue of $18.2 million. "
                      "Full-year revenue reached $64.6 million, a 19% increase over 2024.",
                      "Net income for the quarter was $2.8 million. The company ended the year with $11.3 million "
                      "in cash and zero net debt, providing strong financial flexibility.",
                  ])
    add_text_page(doc, 2, "Annual Revenue Summary",
                  [
                      "2025 Revenue by Quarter: Q1 $14.2M, Q2 $15.8M, Q3 $16.4M, Q4 $18.2M. Total: $64.6M. "
                      "Year-over-year growth: 19%. Organic growth excluding acquisitions: 16%.",
                      "Revenue by Geography: North America 68% ($43.9M), Europe 19% ($12.3M), "
                      "Asia-Pacific 10% ($6.5M), Rest of World 3% ($1.9M).",
                  ])
    add_text_page(doc, 3, "Product Line Review",
                  [
                      "Meridian Suite: Full-year revenue $12.8M, representing 20% of total revenue. "
                      "Customer count grew from 45 to 189. NPS score: 72.",
                      "Enterprise Solutions: $28.4M, stable with 2% growth. Focus on margin improvement "
                      "through automation and self-service capabilities.",
                      "Consulting & Services: $11.2M, growing 14%. High-margin advisory engagements "
                      "now represent 40% of services revenue.",
                  ])
    add_text_page(doc, 4, "Technology Investments",
                  [
                      "AI Analytics Platform: $3.5M invested in 2025. Early customer feedback indicates "
                      "30% productivity improvement. Full commercial launch scheduled for Q1 2026.",
                      "Infrastructure Modernization: Completed migration to multi-cloud architecture. "
                      "Reduced infrastructure costs by 22% while improving uptime to 99.97%.",
                      "Security Enhancements: Achieved SOC 2 Type II certification. Implemented zero-trust "
                      "architecture across all production systems.",
                  ])
    add_text_page(doc, 5, "Human Capital",
                  [
                      "Headcount: 378 employees at year-end (up from 298). Voluntary turnover: 11.2%, "
                      "below industry average of 15.8%. Employee satisfaction score: 4.2/5.0.",
                      "Key Hires: CTO Dr. Raj Patel (ex-Google), VP of APAC Sales Thomas Ng (ex-Salesforce), "
                      "Director of AI Research Dr. Emily Watson (ex-DeepMind).",
                      "Culture & DEI: Launched mentorship program with 85% participation. Gender diversity "
                      "in technical roles improved to 34% from 28%.",
                  ])
    add_text_page(doc, 6, "2026 Strategic Plan",
                  [
                      "Revenue Target: $78-82M (21-27% growth). Key drivers: Meridian expansion, "
                      "APAC market penetration, and AI analytics monetization.",
                      "Planned Investments: $8M in product development, $4M in sales capacity expansion, "
                      "$2M in data center expansion. Total capex budget: $14M.",
                      "M&A Strategy: Active evaluation of two targets in adjacent markets. "
                      "Board has authorized up to $20M for strategic acquisitions.",
                  ])
    output = os.path.join(REPORTS_DIR, 'report_q4.pdf')
    doc.save(output)
    doc.close()
    print(f'Created: {output} (6 pages)')


def create_report_annual():
    """Annual Report - 12 pages"""
    doc = pymupdf.open()

    sections = [
        ("Annual Report 2025 - Nexus Technologies Inc.", [
            "Dear Shareholders: I am pleased to present the Annual Report for Nexus Technologies Inc. "
            "for the fiscal year ended December 31, 2025. This has been a year of exceptional growth.",
            "Revenue grew 19% to $64.6 million, driven by the successful launch of our Meridian platform "
            "and strategic expansion into international markets.",
            "We enter 2026 with strong momentum, a robust pipeline, and the team to execute our vision "
            "of becoming the leading enterprise technology platform.",
            "Sincerely, David Chen, Chief Executive Officer",
        ]),
        ("Company Overview", [
            "Nexus Technologies provides integrated enterprise software solutions serving mid-market and "
            "enterprise customers across 28 countries. Founded in 2018, the company has grown to 378 employees.",
            "Our flagship Meridian Suite combines workflow automation, analytics, and collaboration tools "
            "into a unified platform designed for the modern hybrid workplace.",
            "Headquarters: San Francisco, CA. Regional offices: New York, London, Singapore, Sydney.",
        ]),
        ("Financial Highlights", [
            "Revenue: $64.6M (+19% YoY). Gross Margin: 63.1% (+2.8pp). Operating Income: $8.2M (+45%).",
            "Net Income: $7.1M vs $3.2M in 2024. EPS: $1.42 vs $0.64. Free Cash Flow: $6.8M.",
            "ARR: $58.3M at year-end. Net Revenue Retention: 114%. Gross Revenue Retention: 92%.",
        ]),
        ("Engineering and Product Development", [
            "The engineering team delivered 52 product releases in 2025, including three major platform updates. "
            "Meridian 3.0 introduced collaborative workspaces and real-time co-editing.",
            "R&D investment totaled $12.8M (19.8% of revenue), focused on AI capabilities, platform "
            "scalability, and security enhancements.",
            "Patent portfolio expanded to 14 granted patents with 8 pending applications in machine "
            "learning and natural language processing.",
        ]),
        ("Sales and Marketing", [
            "New customer acquisition: 186 accounts (vs. 124 in 2024). Average deal size increased "
            "15% to $87,000. Enterprise deals (>$100K ARR): 42 closed.",
            "Channel partner program grew to 25 certified partners generating 18% of new business. "
            "Marketing efficiency improved with CAC payback period dropping to 14 months.",
        ]),
        ("International Operations", [
            "International revenue grew 32% to $20.7M, now representing 32% of total revenue. "
            "APAC region showed the strongest growth at 48%.",
            "Singapore office became fully operational in Q3 with 28 employees. Plans to open "
            "a Tokyo representative office in Q2 2026.",
            "European operations stabilized with new GDPR-compliant infrastructure deployed across "
            "all EU data centers. Partnership with local system integrators driving growth.",
        ]),
        ("Corporate Governance", [
            "Board of Directors: 7 members, 5 independent. Added two new independent directors with "
            "expertise in AI and international expansion.",
            "Compensation: CEO total compensation aligned with shareholder value creation. "
            "80% of executive pay is performance-based.",
            "Risk Management: Enterprise risk framework updated. Cybersecurity insurance coverage "
            "increased to $25M. Business continuity plans tested quarterly.",
        ]),
        ("Environmental, Social, and Governance (ESG)", [
            "Carbon Footprint: Reduced Scope 1+2 emissions by 18% through renewable energy procurement "
            "and office efficiency improvements. Committed to carbon neutral by 2028.",
            "Community Impact: $420K donated to STEM education programs. 2,400 employee volunteer hours "
            "logged across 12 community organizations.",
            "Governance: Adopted enhanced supplier code of conduct. Published first transparency report "
            "on data handling practices.",
        ]),
        ("Technology Infrastructure", [
            "Completed migration to multi-cloud architecture (AWS + GCP). Achieved 99.97% uptime "
            "across all production services, exceeding the 99.95% SLA commitment.",
            "Security: Zero critical security incidents. Achieved SOC 2 Type II and ISO 27001 certifications. "
            "Implemented zero-trust architecture across all systems.",
            "Scalability: Platform handles 2.3M daily active users, up from 1.4M at start of year. "
            "Response time p95 improved from 340ms to 210ms.",
        ]),
        ("Customer Success Stories", [
            "Pinnacle Healthcare: Reduced administrative workload by 35% using Meridian workflow automation. "
            "Full deployment across 12 hospital locations completed in 8 months.",
            "Atlas Financial Group: Consolidated 7 legacy tools into Meridian Suite, saving $1.2M annually. "
            "Employee adoption reached 94% within 6 months of deployment.",
            "GreenPath Energy: Used our analytics platform to optimize renewable energy grid operations, "
            "achieving 12% improvement in energy distribution efficiency.",
        ]),
        ("Forward-Looking Statements", [
            "2026 Revenue Guidance: $78-82M. Growth Drivers: Meridian platform expansion, AI analytics "
            "monetization, APAC market penetration, and strategic acquisitions.",
            "Investment Priorities: $8M product development, $4M sales expansion, $2M infrastructure. "
            "M&A: Active evaluation of targets in data visualization and workflow automation.",
            "Long-term Vision: Achieve $150M ARR by 2028 through organic growth and strategic acquisitions, "
            "becoming the top-3 enterprise platform for mid-market companies globally.",
        ]),
        ("Appendix - Key Financial Tables", [
            "Consolidated Revenue by Quarter: Q1 $14.2M, Q2 $15.8M, Q3 $16.4M, Q4 $18.2M. "
            "Total: $64.6M. Prior Year: $54.3M.",
            "Operating Expenses: COGS $23.8M, R&D $12.8M, S&M $14.2M, G&A $5.6M. Total OpEx: $56.4M.",
            "Cash Flow: Operating $9.2M, Investing ($5.8M), Financing ($1.1M). Net Change: $2.3M.",
        ]),
    ]

    for i, (title, paras) in enumerate(sections):
        add_text_page(doc, i + 1, title, paras)

    output = os.path.join(REPORTS_DIR, 'report_annual.pdf')
    doc.save(output)
    doc.close()
    print(f'Created: {output} (12 pages)')


def create_report_summary():
    """Summary Report - 2 pages"""
    doc = pymupdf.open()
    add_text_page(doc, 1, "Executive Summary Report - 2025",
                  [
                      "Nexus Technologies delivered exceptional results in fiscal year 2025, achieving $64.6 million "
                      "in revenue, a 19% year-over-year increase that exceeded initial guidance of $60-62 million.",
                      "The Meridian product suite emerged as the primary growth engine, contributing $12.8 million "
                      "in its first full year. Customer satisfaction scores reached an all-time high of NPS 72.",
                      "Operating margins expanded 280 basis points to 12.7%, demonstrating improving unit economics "
                      "and operational leverage as the company scales.",
                      "International markets, particularly Asia-Pacific, showed strong momentum with 48% growth. "
                      "The Singapore office is now fully staffed with 28 professionals.",
                      "The company enters 2026 with $11.3 million in cash, zero net debt, and a qualified pipeline "
                      "of $52 million, positioning it well for continued growth.",
                  ])
    add_text_page(doc, 2, "Key Performance Indicators",
                  [
                      "Financial: Revenue $64.6M (+19%), Gross Margin 63.1%, Net Income $7.1M, FCF $6.8M, "
                      "Cash $11.3M, ARR $58.3M, NRR 114%.",
                      "Customers: Total accounts 612 (+186 new), Enterprise accounts 142 (+42), "
                      "Average deal size $87K (+15%), Churn rate 8%, NPS 72.",
                      "Operations: Employees 378 (+80), Uptime 99.97%, Releases 52, Patents 14 granted / 8 pending, "
                      "Turnover 11.2%, Satisfaction 4.2/5.0.",
                      "2026 Targets: Revenue $78-82M, Headcount 450+, International >35% of revenue, "
                      "Meridian >30% of revenue, Operating margin >15%.",
                  ])
    output = os.path.join(REPORTS_DIR, 'report_summary.pdf')
    doc.save(output)
    doc.close()
    print(f'Created: {output} (2 pages)')


def create_initial():
    """Create all 6 report PDFs in the reports directory."""
    os.makedirs(REPORTS_DIR, exist_ok=True)

    create_report_q1()      # 3 pages
    create_report_q2()      # 4 pages
    create_report_q3()      # 5 pages
    create_report_q4()      # 6 pages
    create_report_annual()  # 12 pages
    create_report_summary() # 2 pages

    print(f'\nAll 6 reports created in {REPORTS_DIR}')

    # Open file manager showing the reports directory
    launch_gui(f'nautilus "{REPORTS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
