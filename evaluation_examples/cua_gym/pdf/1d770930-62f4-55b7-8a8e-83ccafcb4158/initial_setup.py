"""
Initial Setup: Create an 8-page US Letter PDF for page scaling task
Task ID: pdf_fm_079
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_079'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/us_letter.pdf'

# US Letter dimensions in points
LETTER_W, LETTER_H = 612, 792

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
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: Title Page ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 200), "Meridian Analytics Group", fontsize=28, fontname="hebo", color=(0.1, 0.15, 0.4))
    page.insert_text(pymupdf.Point(72, 250), "2025 Strategic Growth Report", fontsize=20, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 300), "Prepared for the Board of Directors", fontsize=14, fontname="heit", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(72, 340), "March 15, 2025", fontsize=12, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(72, 380), "Confidential - Internal Use Only", fontsize=10, fontname="hebo", color=(0.7, 0.1, 0.1))
    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 270), pymupdf.Point(540, 270))
    shape.finish(color=(0.1, 0.15, 0.4), width=2)
    shape.commit()

    # --- Page 2: Executive Summary ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 72), "Executive Summary", fontsize=22, fontname="hebo", color=(0.1, 0.15, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape.commit()
    summary_text = (
        "Meridian Analytics Group achieved record-breaking performance in fiscal year 2024, "
        "with consolidated revenue reaching $487.3 million, a 23% year-over-year increase. "
        "Our expansion into the Asia-Pacific region contributed $78.2 million in new revenue, "
        "while our core North American operations grew by 18%. Operating margins improved to "
        "31.4%, up from 27.8% in the prior year, driven by strategic automation initiatives "
        "and a disciplined approach to cost management.\n\n"
        "Key highlights include the successful launch of our Predictive Insights Platform, "
        "which onboarded 142 enterprise clients in its first quarter. Customer retention rates "
        "remained strong at 94.7%, reflecting the deep value our analytics solutions deliver. "
        "We also completed the acquisition of DataVista Technologies for $52 million, adding "
        "specialized capabilities in real-time streaming analytics.\n\n"
        "Looking ahead to 2025, we project revenue growth of 18-22% as we scale our cloud-native "
        "offerings and deepen penetration in the financial services and healthcare verticals. "
        "Capital expenditures are budgeted at $35 million to support infrastructure modernization "
        "and talent acquisition across our five global offices."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 700), summary_text, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 3: Revenue Breakdown ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 72), "Revenue Breakdown by Division", fontsize=22, fontname="hebo", color=(0.1, 0.15, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape.commit()

    # Table header
    y_start = 110
    headers = ["Division", "FY2023 ($M)", "FY2024 ($M)", "Growth (%)"]
    col_x = [72, 220, 340, 460]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(col_x[i], y_start), h, fontsize=10, fontname="hebo", color=(1, 1, 1))
    # Header background
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(70, y_start - 12, 542, y_start + 4))
    shape.finish(fill=(0.1, 0.15, 0.4), color=(0.1, 0.15, 0.4))
    shape.commit()
    # Re-draw headers on top
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(col_x[i], y_start), h, fontsize=10, fontname="hebo", color=(1, 1, 1))

    rows = [
        ["Enterprise Analytics", "156.8", "198.4", "26.5"],
        ["Cloud Services", "89.3", "112.7", "26.2"],
        ["Consulting & Advisory", "67.4", "78.2", "16.0"],
        ["Data Integration", "45.1", "52.8", "17.1"],
        ["Asia-Pacific Operations", "38.6", "45.2", "17.1"],
        ["Total", "397.2", "487.3", "22.7"],
    ]
    for r_idx, row in enumerate(rows):
        y = y_start + 22 + r_idx * 20
        fn = "hebo" if row[0] == "Total" else "helv"
        for i, val in enumerate(row):
            page.insert_text(pymupdf.Point(col_x[i], y), val, fontsize=10, fontname=fn, color=(0.1, 0.1, 0.1))
        if r_idx % 2 == 0 and row[0] != "Total":
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(70, y - 12, 542, y + 6))
            shape.finish(fill=(0.93, 0.93, 0.97), color=(0.93, 0.93, 0.97))
            shape.commit()
            for i, val in enumerate(row):
                page.insert_text(pymupdf.Point(col_x[i], y), val, fontsize=10, fontname=fn, color=(0.1, 0.1, 0.1))

    page.insert_textbox(
        pymupdf.Rect(72, 280, 540, 500),
        "Enterprise Analytics remains our largest division, contributing 40.7% of total revenue. "
        "The division benefited from increased demand for predictive modeling services among Fortune 500 "
        "clients. Cloud Services showed the strongest growth trajectory, fueled by migrations from "
        "on-premise deployments. The Asia-Pacific expansion, led by our Singapore and Tokyo offices, "
        "exceeded initial projections by 12%, validating our investment thesis for the region.\n\n"
        "Consulting & Advisory revenue grew steadily as clients sought strategic guidance on AI integration "
        "and data governance frameworks. We anticipate this division will accelerate in 2025 as regulatory "
        "requirements around data privacy drive demand for compliance consulting.",
        fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 4: Client Metrics ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 72), "Client Engagement Metrics", fontsize=22, fontname="hebo", color=(0.1, 0.15, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape.commit()

    metrics_text = (
        "Our client base expanded to 1,247 active accounts across 38 countries, representing a net "
        "addition of 186 new enterprise clients. The average contract value increased to $391,000, "
        "up from $342,000 in the prior year, reflecting deeper platform adoption and expanded scope "
        "of engagements.\n\n"
        "Key client metrics for FY2024:\n\n"
        "  - Net Promoter Score (NPS): 72 (up from 68)\n"
        "  - Customer Retention Rate: 94.7%\n"
        "  - Average Revenue Per Account: $391,000\n"
        "  - Time-to-Value (median): 6.2 weeks\n"
        "  - Support Ticket Resolution: 4.1 hours (SLA target: 8 hours)\n"
        "  - Platform Uptime: 99.97%\n\n"
        "Our top 50 clients contributed 34% of total revenue, with the largest single account "
        "generating $8.7 million. We successfully reduced client concentration risk, with no single "
        "client representing more than 2% of revenue. Cross-selling initiatives drove a 28% increase "
        "in multi-product adoption among existing clients."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 700), metrics_text, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))

    # --- Page 5: Technology & Innovation ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 72), "Technology & Innovation", fontsize=22, fontname="hebo", color=(0.1, 0.15, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape.commit()

    tech_text = (
        "The Predictive Insights Platform, launched in Q2 2024, represents our most significant product "
        "innovation in five years. Built on a microservices architecture with Kubernetes orchestration, "
        "the platform processes over 2.3 billion data points daily with sub-second query response times.\n\n"
        "R&D investment totaled $43.5 million (8.9% of revenue), directed toward three strategic areas:\n\n"
        "1. Generative AI Integration - We embedded large language model capabilities into our analytics "
        "   suite, enabling natural language queries across structured datasets. Early adopters report "
        "   a 40% reduction in time spent on ad-hoc analysis.\n\n"
        "2. Real-Time Streaming Analytics - The DataVista acquisition accelerated our roadmap by "
        "   18 months. The integrated streaming engine now supports Apache Kafka, Amazon Kinesis, "
        "   and Azure Event Hubs natively.\n\n"
        "3. Edge Computing - Prototype deployments at three manufacturing clients demonstrated the "
        "   viability of on-premise inference models that synchronize with our cloud platform. We "
        "   expect general availability in Q3 2025.\n\n"
        "Patent applications filed: 14 (granted: 9). Our intellectual property portfolio now covers "
        "47 active patents across data processing, visualization, and machine learning methodologies."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 720), tech_text, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 6: Workforce & Culture ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 72), "Workforce & Culture", fontsize=22, fontname="hebo", color=(0.1, 0.15, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape.commit()

    workforce_text = (
        "Meridian's global workforce grew to 2,847 employees across offices in Boston, San Francisco, "
        "London, Singapore, and Tokyo. We hired 412 new team members in 2024, with a particular focus "
        "on data scientists, platform engineers, and client success managers.\n\n"
        "Employee engagement scores averaged 4.3 out of 5.0, placing us in the top quartile of "
        "technology companies tracked by Glassdoor. Voluntary attrition decreased to 11.2% from "
        "14.8%, reflecting improvements in compensation, career development pathways, and flexible "
        "work arrangements.\n\n"
        "Diversity, Equity & Inclusion Progress:\n"
        "  - Women in leadership roles: 38% (target: 42% by 2026)\n"
        "  - Underrepresented minorities in technical roles: 24% (up from 19%)\n"
        "  - Gender pay gap analysis: within 2.1% (adjusted for role and tenure)\n"
        "  - Employee Resource Groups: 8 active groups with 64% participation\n\n"
        "Our Learning & Development budget increased by 35% to support upskilling in AI, cloud "
        "architecture, and leadership. The Meridian Academy program graduated 89 participants, "
        "with 73% receiving promotions within six months of completion."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 720), workforce_text, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))

    # --- Page 7: Financial Outlook ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 72), "Financial Outlook 2025", fontsize=22, fontname="hebo", color=(0.1, 0.15, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape.commit()

    outlook_text = (
        "Based on current pipeline visibility and market conditions, management projects the following "
        "guidance for fiscal year 2025:\n\n"
        "Revenue: $575M - $605M (18-24% growth)\n"
        "Operating Margin: 32-34%\n"
        "Free Cash Flow: $95M - $110M\n"
        "Capital Expenditure: $33M - $37M\n"
        "Headcount: 3,200 - 3,400 employees\n\n"
        "Growth will be driven by three primary vectors:\n\n"
        "First, the expansion of our cloud-native platform is expected to convert 200+ on-premise "
        "clients to subscription-based cloud deployments, improving revenue predictability and "
        "lifetime value. Migration incentives and dedicated support teams are already in place.\n\n"
        "Second, our healthcare analytics vertical is projected to double in revenue following "
        "regulatory changes that mandate enhanced data reporting. We have secured partnerships with "
        "four of the top ten US hospital networks.\n\n"
        "Third, international expansion will continue with planned office openings in Sydney and "
        "Frankfurt, targeting the Australasian and DACH markets respectively. Combined, these "
        "regions represent a $4.2 billion addressable market opportunity.\n\n"
        "Risk factors include potential macroeconomic softening, currency headwinds in international "
        "operations, and increased competition from well-funded AI startups. Our mitigation strategy "
        "emphasizes platform differentiation and deep domain expertise."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 740), outlook_text, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 8: Appendix ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 72), "Appendix: Key Definitions & Methodology", fontsize=22, fontname="hebo", color=(0.1, 0.15, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape.commit()

    appendix_text = (
        "Revenue Recognition: Revenue is recognized in accordance with ASC 606, with performance "
        "obligations satisfied over the subscription term for SaaS products and upon delivery for "
        "consulting engagements.\n\n"
        "Operating Margin: Calculated as operating income divided by total revenue, excluding "
        "one-time restructuring charges and acquisition-related expenses.\n\n"
        "Net Promoter Score (NPS): Measured quarterly through standardized surveys sent to primary "
        "account contacts. Responses are collected on a 0-10 scale and categorized as Detractors "
        "(0-6), Passives (7-8), and Promoters (9-10).\n\n"
        "Customer Retention Rate: The percentage of clients with active contracts at the end of "
        "the fiscal year compared to the beginning, excluding acquisitions and divestitures.\n\n"
        "Free Cash Flow: Operating cash flow minus capital expenditures, adjusted for changes in "
        "working capital and excluding proceeds from asset disposals.\n\n"
        "Addressable Market: Total addressable market (TAM) estimates are based on third-party "
        "research from Gartner, IDC, and internal analysis of customer spend patterns across "
        "the analytics and business intelligence sector.\n\n"
        "This report contains forward-looking statements that involve risks and uncertainties. "
        "Actual results may differ materially from those projected. See our SEC filings for a "
        "complete discussion of risk factors."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 720), appendix_text, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Remove any pre-existing output file
    output_a4 = f'{DOCS_DIR}/us_letter_a4.pdf'
    if os.path.exists(output_a4):
        os.remove(output_a4)

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
