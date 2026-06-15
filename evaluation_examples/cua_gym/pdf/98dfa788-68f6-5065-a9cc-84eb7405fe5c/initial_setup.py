"""
Initial Setup: Create four quarterly report PDFs in /home/user/finance/
Task ID: pdf_gf2_001
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
TASK_ID = 'pdf_gf2_001'
FINANCE_DIR = f'{WORKDIR}/finance'

# Page dimensions (Letter size)
WIDTH, HEIGHT = 612, 792


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


def add_title_page(doc, quarter_label, year="2025"):
    """Add a title/cover page for a quarterly report."""
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    # Company name
    page.insert_text(pymupdf.Point(WIDTH / 2 - 120, 200), "Meridian Technologies Inc.",
                     fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    # Report title
    page.insert_text(pymupdf.Point(WIDTH / 2 - 100, 280), f"{quarter_label} Financial Report",
                     fontsize=22, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(WIDTH / 2 - 60, 320), f"Fiscal Year {year}",
                     fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))
    # Divider line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(100, 360), pymupdf.Point(WIDTH - 100, 360))
    shape.finish(color=(0.2, 0.2, 0.6), width=2)
    shape.commit()
    # Prepared by
    page.insert_text(pymupdf.Point(100, 420), "Prepared by: Office of the Chief Financial Officer",
                     fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(100, 445), "Classification: Internal - Confidential",
                     fontsize=10, fontname="heit", color=(0.5, 0.5, 0.5))


def add_content_page(doc, title, paragraphs, page_number_text=""):
    """Add a content page with a heading and paragraphs of text."""
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    y = 72
    # Header bar
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, WIDTH, 50))
    shape.finish(fill=(0.15, 0.15, 0.45), color=(0.15, 0.15, 0.45))
    shape.commit()
    page.insert_text(pymupdf.Point(72, 35), title,
                     fontsize=14, fontname="hebo", color=(1, 1, 1))
    y = 80

    for para in paragraphs:
        rect = pymupdf.Rect(72, y, WIDTH - 72, HEIGHT - 72)
        rc = page.insert_textbox(rect, para, fontsize=10, fontname="helv",
                                  color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        # Estimate vertical space consumed
        lines_used = para.count('\n') + len(para) // 70 + 2
        y += lines_used * 13
        if y > HEIGHT - 100:
            break

    # Page footer
    page.insert_text(pymupdf.Point(WIDTH / 2 - 30, HEIGHT - 30),
                     page_number_text, fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))


def add_table_page(doc, title, headers, rows, page_number_text=""):
    """Add a page with a table of financial data."""
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    # Header bar
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, WIDTH, 50))
    shape.finish(fill=(0.15, 0.15, 0.45), color=(0.15, 0.15, 0.45))
    shape.commit()
    page.insert_text(pymupdf.Point(72, 35), title,
                     fontsize=14, fontname="hebo", color=(1, 1, 1))

    y_start = 80
    col_widths = [140, 100, 100, 100, 100]
    x_start = 72

    # Draw header row
    x = x_start
    for i, h in enumerate(headers):
        cw = col_widths[i] if i < len(col_widths) else 100
        page.insert_text(pymupdf.Point(x + 4, y_start + 14), h,
                         fontsize=9, fontname="hebo", color=(0.15, 0.15, 0.45))
        x += cw

    # Header underline
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(x_start, y_start + 20),
                     pymupdf.Point(x_start + sum(col_widths[:len(headers)]), y_start + 20))
    shape2.finish(color=(0.15, 0.15, 0.45), width=1)
    shape2.commit()

    y = y_start + 30
    for row in rows:
        x = x_start
        for i, val in enumerate(row):
            cw = col_widths[i] if i < len(col_widths) else 100
            page.insert_text(pymupdf.Point(x + 4, y + 12), str(val),
                             fontsize=9, fontname="helv", color=(0, 0, 0))
            x += cw
        y += 18
        if y > HEIGHT - 80:
            break

    # Footer
    page.insert_text(pymupdf.Point(WIDTH / 2 - 30, HEIGHT - 30),
                     page_number_text, fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))


def create_q1_report():
    """Q1 report: 8 pages."""
    doc = pymupdf.open()
    # Page 1: Title
    add_title_page(doc, "Q1 (January - March)")

    # Page 2: Executive Summary
    add_content_page(doc, "Executive Summary", [
        "The first quarter of fiscal year 2025 demonstrated strong performance across all business segments. "
        "Total consolidated revenue reached $48.7 million, representing a 12.3% increase year-over-year. "
        "Operating margins improved to 18.2%, driven by cost optimization initiatives launched in late 2024.",
        "Key highlights include the successful launch of the CloudSync Enterprise platform, which generated "
        "$5.2 million in new recurring revenue. The Asia-Pacific region continued its growth trajectory with "
        "a 23% increase in bookings compared to Q1 2024.",
        "Research and development expenditures totaled $8.1 million, reflecting our continued investment in "
        "next-generation AI-powered analytics capabilities. We filed 14 new patent applications during the quarter."
    ], "Page 2")

    # Page 3: Revenue Breakdown
    add_table_page(doc, "Revenue Breakdown by Segment",
                   ["Segment", "Revenue", "YoY Growth", "Margin", "Forecast"],
                   [
                       ["Enterprise Software", "$22.4M", "+15.1%", "24.3%", "$24.0M"],
                       ["Cloud Services", "$14.8M", "+28.6%", "19.7%", "$16.5M"],
                       ["Professional Services", "$6.2M", "+3.2%", "12.1%", "$6.5M"],
                       ["Hardware Solutions", "$3.1M", "-5.4%", "8.6%", "$3.0M"],
                       ["Licensing & Royalties", "$2.2M", "+7.8%", "82.3%", "$2.3M"],
                   ], "Page 3")

    # Page 4: Operating Expenses
    add_table_page(doc, "Operating Expenses Summary",
                   ["Category", "Amount", "% Revenue", "Budget", "Variance"],
                   [
                       ["Cost of Goods Sold", "$19.8M", "40.7%", "$20.5M", "-$0.7M"],
                       ["R&D", "$8.1M", "16.6%", "$8.0M", "+$0.1M"],
                       ["Sales & Marketing", "$7.3M", "15.0%", "$7.5M", "-$0.2M"],
                       ["General & Admin", "$4.6M", "9.4%", "$4.8M", "-$0.2M"],
                       ["Depreciation", "$1.2M", "2.5%", "$1.2M", "$0.0M"],
                       ["Other", "$0.8M", "1.6%", "$1.0M", "-$0.2M"],
                   ], "Page 4")

    # Page 5: Regional Performance
    add_content_page(doc, "Regional Performance Analysis", [
        "North America maintained its position as the largest revenue contributor with $28.4 million, "
        "accounting for 58.3% of total revenue. Growth was primarily driven by enterprise software renewals "
        "and new cloud service subscriptions from Fortune 500 clients.",
        "EMEA generated $11.6 million in revenue, a 9.7% increase. The region benefited from regulatory "
        "compliance demand driving adoption of our data governance solutions. New partnerships with "
        "Siemens and Deutsche Telekom are expected to accelerate Q2 growth.",
        "Asia-Pacific delivered $8.7 million, with notable expansion in Japan (+31%) and Australia (+19%). "
        "Our Singapore data center, operational since November 2024, has reduced latency and improved "
        "customer satisfaction scores by 15 basis points."
    ], "Page 5")

    # Page 6: Key Metrics Dashboard
    add_table_page(doc, "Key Performance Indicators",
                   ["Metric", "Q1 2025", "Q4 2024", "Q1 2024", "Target"],
                   [
                       ["Total Revenue", "$48.7M", "$51.2M", "$43.4M", "$47.0M"],
                       ["Gross Margin", "59.3%", "58.1%", "56.8%", "58.0%"],
                       ["Operating Margin", "18.2%", "16.9%", "15.4%", "17.5%"],
                       ["Net Income", "$6.8M", "$7.1M", "$5.2M", "$6.5M"],
                       ["Free Cash Flow", "$9.3M", "$12.4M", "$7.8M", "$8.5M"],
                       ["Employee Count", "1,247", "1,231", "1,189", "1,250"],
                       ["Customer NPS", "72", "69", "65", "70"],
                       ["ARR", "$178.4M", "$172.1M", "$158.6M", "$175.0M"],
                   ], "Page 6")

    # Page 7: Risk Factors
    add_content_page(doc, "Risk Factors & Mitigation", [
        "Supply Chain Disruption: Global semiconductor shortages continue to affect hardware delivery "
        "timelines. We have secured secondary suppliers and increased buffer inventory to 8 weeks.",
        "Foreign Exchange Exposure: Approximately 35% of revenue is denominated in non-USD currencies. "
        "Our hedging program covers 70% of expected foreign currency receipts through Q3 2025.",
        "Competitive Landscape: New entrants in the cloud analytics space pose pricing pressure. "
        "We are responding with enhanced product differentiation and value-added service bundles.",
        "Regulatory Changes: Evolving data privacy regulations in the EU and APAC require ongoing "
        "investment in compliance infrastructure. Budget allocation increased by $1.2M for Q2."
    ], "Page 7")

    # Page 8: Outlook
    add_content_page(doc, "Q2 2025 Outlook & Guidance", [
        "Management projects consolidated revenue of $50.5 - $52.0 million for Q2 2025, representing "
        "year-over-year growth of 10-13%. Operating margins are expected to remain in the 17-19% range.",
        "Key catalysts for Q2 include the general availability launch of our AI Analytics Suite, "
        "expected to generate $2-3 million in incremental revenue. Additionally, our partnership with "
        "Amazon Web Services for a co-branded solution is projected to onboard 25+ new enterprise accounts.",
        "Capital expenditure guidance remains at $12-14 million for the full fiscal year. We anticipate "
        "approximately $4 million in CapEx during Q2, primarily for data center expansion in Frankfurt "
        "and the buildout of our new Austin engineering campus."
    ], "Page 8")

    path = f'{FINANCE_DIR}/q1_report.pdf'
    doc.save(path)
    doc.close()
    print(f'Created: {path} ({8} pages)')


def create_q2_report():
    """Q2 report: 9 pages."""
    doc = pymupdf.open()
    add_title_page(doc, "Q2 (April - June)")

    add_content_page(doc, "Executive Summary", [
        "Meridian Technologies delivered a record-setting second quarter with consolidated revenue of "
        "$52.3 million, surpassing the upper end of guidance by $0.3 million. Year-over-year growth "
        "accelerated to 14.1%, driven by the successful launch of the AI Analytics Suite.",
        "Operating income reached $10.2 million with an operating margin of 19.5%, the highest in "
        "company history. Adjusted EBITDA was $13.8 million, representing a 26.4% margin.",
        "The quarter saw 47 new enterprise customers added, bringing total enterprise accounts to 892. "
        "Net dollar retention rate improved to 118%, reflecting strong expansion within existing accounts."
    ], "Page 2")

    add_table_page(doc, "Revenue by Product Line",
                   ["Product", "Revenue", "QoQ Change", "Margin", "Mix %"],
                   [
                       ["AI Analytics Suite", "$3.1M", "New", "31.2%", "5.9%"],
                       ["Enterprise Software", "$23.8M", "+6.3%", "25.1%", "45.5%"],
                       ["Cloud Services", "$16.2M", "+9.5%", "21.3%", "31.0%"],
                       ["Professional Services", "$5.8M", "-6.5%", "11.8%", "11.1%"],
                       ["Hardware Solutions", "$2.0M", "-35.5%", "7.2%", "3.8%"],
                       ["Licensing & Royalties", "$1.4M", "-36.4%", "79.5%", "2.7%"],
                   ], "Page 3")

    add_table_page(doc, "Balance Sheet Highlights",
                   ["Item", "Q2 2025", "Q1 2025", "Change"],
                   [
                       ["Cash & Equivalents", "$67.8M", "$62.4M", "+$5.4M"],
                       ["Accounts Receivable", "$31.2M", "$28.9M", "+$2.3M"],
                       ["Total Current Assets", "$112.5M", "$104.8M", "+$7.7M"],
                       ["PP&E (Net)", "$45.3M", "$43.1M", "+$2.2M"],
                       ["Total Assets", "$298.6M", "$287.4M", "+$11.2M"],
                       ["Current Liabilities", "$38.9M", "$36.2M", "+$2.7M"],
                       ["Long-term Debt", "$42.0M", "$45.0M", "-$3.0M"],
                       ["Shareholders' Equity", "$189.7M", "$180.2M", "+$9.5M"],
                   ], "Page 4")

    add_content_page(doc, "Strategic Initiatives Update", [
        "AI Analytics Suite Launch: The general availability release exceeded expectations with 156 "
        "trial activations and a 42% conversion rate in the first 60 days. Early adopter feedback "
        "highlights the natural language query interface and automated insight generation as standout features.",
        "AWS Partnership: The co-branded Meridian+AWS solution launched on AWS Marketplace in May. "
        "Initial traction includes 31 new accounts, with pipeline visibility suggesting 50+ additional "
        "opportunities in the evaluation stage.",
        "Austin Campus: Construction is 65% complete with occupancy targeted for September 2025. "
        "The 120,000 sq ft facility will house 400 engineering and product development team members."
    ], "Page 5")

    add_content_page(doc, "Customer Success Highlights", [
        "Global Financial Group: Deployed our full enterprise suite across 12 countries, achieving "
        "a 40% reduction in quarterly close time and $3.2M in projected annual savings.",
        "Pacific Health Systems: Implemented AI Analytics Suite for patient flow optimization, "
        "resulting in a 15% improvement in bed utilization and 22% reduction in wait times.",
        "Eurotech Manufacturing: Cloud migration completed, consolidating 47 legacy systems into "
        "our unified platform. Annual IT maintenance costs reduced by $1.8M."
    ], "Page 6")

    add_table_page(doc, "Cash Flow Statement",
                   ["Category", "Q2 2025", "Q1 2025", "YoY Change"],
                   [
                       ["Operating Cash Flow", "$14.2M", "$11.8M", "+28.2%"],
                       ["Capital Expenditures", "-$3.8M", "-$2.5M", "+52.0%"],
                       ["Free Cash Flow", "$10.4M", "$9.3M", "+11.8%"],
                       ["Acquisitions", "$0.0M", "$0.0M", "N/A"],
                       ["Debt Repayment", "-$3.0M", "-$1.5M", "+100%"],
                       ["Share Repurchases", "-$2.5M", "$0.0M", "N/A"],
                       ["Dividends Paid", "-$1.2M", "-$1.2M", "0.0%"],
                   ], "Page 7")

    add_content_page(doc, "Workforce & Culture", [
        "Total headcount reached 1,278 at quarter end, a net increase of 31 positions. Key hires "
        "include Dr. Priya Sharma as VP of AI Research and David Chen as Regional Director for Japan.",
        "Employee engagement survey results showed an overall satisfaction score of 4.2/5.0, up from "
        "4.0 in Q1. Areas of strength include team collaboration (4.5) and professional development (4.3). "
        "Areas for improvement include work-life balance (3.8) and internal communications (3.7).",
        "Diversity metrics: Women in leadership roles increased to 38% (from 35% in Q4 2024). "
        "Underrepresented minorities in technical roles reached 24%, surpassing our 2025 target of 22%."
    ], "Page 8")

    add_content_page(doc, "Q3 2025 Outlook", [
        "We are raising full-year revenue guidance to $205-$210 million (from $198-$204 million) "
        "based on strong first-half performance and robust pipeline visibility.",
        "Q3 revenue is expected in the range of $53.0-$54.5 million. Operating margin guidance "
        "is 18-20%. We anticipate approximately $3.5M in CapEx for the quarter.",
        "Key Q3 milestones: Austin campus completion, AI Analytics Suite v2.0 release with "
        "computer vision capabilities, and expansion into the South Korean market."
    ], "Page 9")

    path = f'{FINANCE_DIR}/q2_report.pdf'
    doc.save(path)
    doc.close()
    print(f'Created: {path} ({9} pages)')


def create_q3_report():
    """Q3 report: 7 pages."""
    doc = pymupdf.open()
    add_title_page(doc, "Q3 (July - September)")

    add_content_page(doc, "Executive Summary", [
        "Third quarter results reflect continued momentum with consolidated revenue of $54.1 million, "
        "above the midpoint of guidance. Year-over-year growth was 13.5%, with organic growth of 11.8%.",
        "Operating margin of 19.1% remained near the record high set in Q2. Net income was $7.9 million "
        "or $0.62 per diluted share, compared to $6.1 million ($0.48/share) in Q3 2024.",
        "Annual Recurring Revenue (ARR) crossed the $200 million milestone, reaching $204.7 million "
        "at quarter end. This represents a 17.2% increase from $174.6 million at the end of Q3 2024."
    ], "Page 2")

    add_table_page(doc, "Segment Revenue Performance",
                   ["Segment", "Revenue", "YoY Growth", "Margin", "Headcount"],
                   [
                       ["Enterprise Software", "$24.6M", "+12.8%", "25.8%", "412"],
                       ["Cloud Services", "$18.1M", "+32.1%", "22.5%", "298"],
                       ["AI Analytics", "$5.8M", "N/A", "28.4%", "87"],
                       ["Professional Services", "$3.9M", "-8.2%", "10.5%", "156"],
                       ["Other", "$1.7M", "-12.3%", "45.2%", "42"],
                   ], "Page 3")

    add_content_page(doc, "Product Development Milestones", [
        "AI Analytics Suite v2.0: Released in August with computer vision capabilities for document "
        "processing and image analysis. Early adoption metrics show 2.3x higher engagement rates "
        "compared to v1.0 at the same stage of its lifecycle.",
        "CloudSync Platform 4.5: Major release featuring real-time collaboration, improved API "
        "throughput (3x improvement), and native Kubernetes orchestration support.",
        "Security Operations Center: Launched managed security service offering targeting mid-market "
        "customers. Initial pipeline of $4.2M with expected general availability in Q4.",
        "Patent Portfolio: 8 new patents granted during Q3, bringing total active patents to 127. "
        "Filed 11 additional applications related to AI model optimization and data pipeline architecture."
    ], "Page 4")

    add_table_page(doc, "Geographic Revenue Distribution",
                   ["Region", "Revenue", "% Total", "Growth", "Key Driver"],
                   [
                       ["North America", "$30.8M", "56.9%", "+11.2%", "AI Analytics"],
                       ["EMEA", "$13.2M", "24.4%", "+14.8%", "Compliance"],
                       ["Asia-Pacific", "$8.4M", "15.5%", "+22.7%", "Cloud Adopt."],
                       ["Latin America", "$1.7M", "3.1%", "+45.3%", "New Market"],
                   ], "Page 5")

    add_content_page(doc, "Operational Highlights", [
        "Austin Campus: Grand opening held September 15 with full occupancy achieved ahead of schedule. "
        "The facility includes state-of-the-art labs, a 200-seat auditorium, and sustainability features "
        "targeting LEED Gold certification.",
        "Data Center Expansion: Frankfurt facility doubled capacity to support growing European demand. "
        "New Tokyo point-of-presence established, reducing Asia-Pacific latency by 40%.",
        "Customer Base: Total paying customers reached 4,127 (up from 3,891 in Q2). Enterprise "
        "accounts grew to 923, with average contract value increasing 8.3% to $187,000."
    ], "Page 6")

    add_content_page(doc, "Q4 Outlook & Full-Year Guidance", [
        "Q4 revenue guidance: $55.0-$57.0 million. Full-year guidance raised to $209-$213 million. "
        "Operating margin target of 18.5-20% for Q4.",
        "Strategic priorities for Q4 include closing the pipeline for our new managed security service, "
        "finalizing the South Korean market entry, and completing the AI Analytics platform integration "
        "with the core enterprise suite.",
        "Board of Directors has approved a $15 million share repurchase program to be executed "
        "over the next 12 months, reflecting confidence in long-term value creation."
    ], "Page 7")

    path = f'{FINANCE_DIR}/q3_report.pdf'
    doc.save(path)
    doc.close()
    print(f'Created: {path} ({7} pages)')


def create_q4_report():
    """Q4 report: 10 pages."""
    doc = pymupdf.open()
    add_title_page(doc, "Q4 (October - December)")

    add_content_page(doc, "Executive Summary", [
        "Meridian Technologies concluded fiscal year 2025 with an outstanding fourth quarter. "
        "Revenue of $57.2 million represented 15.8% year-over-year growth, bringing full-year "
        "revenue to $212.3 million — a new company record.",
        "Operating income of $11.4 million (19.9% margin) and net income of $8.5 million "
        "($0.67/share) both set quarterly records. Full-year operating margin of 19.2% exceeded "
        "the target range of 17-19%.",
        "The Board declared a special dividend of $0.15/share in addition to the regular quarterly "
        "dividend of $0.10/share, reflecting the strong financial performance."
    ], "Page 2")

    add_table_page(doc, "Full Year Revenue Summary",
                   ["Quarter", "Revenue", "Op. Income", "Net Income", "EPS"],
                   [
                       ["Q1 2025", "$48.7M", "$8.9M", "$6.8M", "$0.53"],
                       ["Q2 2025", "$52.3M", "$10.2M", "$7.6M", "$0.60"],
                       ["Q3 2025", "$54.1M", "$10.3M", "$7.9M", "$0.62"],
                       ["Q4 2025", "$57.2M", "$11.4M", "$8.5M", "$0.67"],
                       ["FY 2025", "$212.3M", "$40.8M", "$30.8M", "$2.42"],
                       ["FY 2024", "$184.1M", "$31.2M", "$23.4M", "$1.84"],
                       ["YoY Growth", "+15.3%", "+30.8%", "+31.6%", "+31.5%"],
                   ], "Page 3")

    add_table_page(doc, "Q4 Segment Performance",
                   ["Segment", "Revenue", "QoQ Growth", "Margin", "FY Total"],
                   [
                       ["Enterprise Software", "$25.8M", "+4.9%", "26.2%", "$96.6M"],
                       ["Cloud Services", "$19.4M", "+7.2%", "23.1%", "$68.5M"],
                       ["AI Analytics", "$7.2M", "+24.1%", "30.8%", "$16.1M"],
                       ["Professional Services", "$3.2M", "-17.9%", "9.8%", "$19.1M"],
                       ["Other", "$1.6M", "-5.9%", "41.3%", "$12.0M"],
                   ], "Page 4")

    add_content_page(doc, "Strategic Achievements", [
        "AI Analytics Suite exceeded all targets, generating $16.1 million in its first year — "
        "48% above the initial forecast of $10.9 million. The product now serves 312 enterprise "
        "accounts with a 94% satisfaction rating.",
        "South Korea Market Entry: Established Seoul office in October with a team of 15. "
        "Signed 8 enterprise contracts in Q4 with combined annual value of $2.1 million. "
        "Partnership with Samsung SDS for co-marketing announced in December.",
        "Managed Security Service: General availability in November, with 45 customers onboarded "
        "by year end. Pipeline exceeds $12 million entering 2026."
    ], "Page 5")

    add_table_page(doc, "Annual Balance Sheet",
                   ["Item", "Dec 2025", "Dec 2024", "Change"],
                   [
                       ["Cash & Equivalents", "$78.4M", "$58.2M", "+$20.2M"],
                       ["Short-term Investments", "$15.0M", "$10.0M", "+$5.0M"],
                       ["Accounts Receivable", "$34.8M", "$29.1M", "+$5.7M"],
                       ["Total Current Assets", "$142.7M", "$108.9M", "+$33.8M"],
                       ["PP&E (Net)", "$52.1M", "$38.7M", "+$13.4M"],
                       ["Goodwill & Intangibles", "$67.3M", "$67.3M", "$0.0M"],
                       ["Total Assets", "$328.4M", "$276.2M", "+$52.2M"],
                       ["Total Liabilities", "$108.2M", "$98.4M", "+$9.8M"],
                       ["Shareholders' Equity", "$220.2M", "$177.8M", "+$42.4M"],
                   ], "Page 6")

    add_content_page(doc, "Research & Innovation", [
        "R&D investment totaled $34.8 million for FY 2025, representing 16.4% of revenue. "
        "This includes $8.2 million specifically allocated to AI/ML capabilities development.",
        "Patent portfolio grew to 142 active patents (from 114 at end of FY 2024). Key areas "
        "include natural language processing (28 patents), data pipeline optimization (19 patents), "
        "and cybersecurity algorithms (15 patents).",
        "Research partnerships established with MIT Media Lab and Stanford AI Institute. "
        "Three joint papers published in peer-reviewed journals during Q4."
    ], "Page 7")

    add_content_page(doc, "Environmental, Social & Governance", [
        "Carbon Footprint: Achieved 15% reduction in Scope 1 and 2 emissions year-over-year. "
        "Austin campus powered by 100% renewable energy through long-term PPA with NextEra Energy.",
        "Diversity & Inclusion: Women in leadership 40% (target: 38%). Underrepresented minorities "
        "in technical roles 26% (target: 22%). Launched mentorship program pairing 120 participants.",
        "Community Investment: $2.4 million in corporate giving including the Meridian STEM "
        "Scholarship Fund ($500K), disaster relief contributions ($350K), and local community grants.",
        "Governance: Added two new independent directors bringing board size to 9 members. "
        "Implemented enhanced cybersecurity oversight framework with quarterly board briefings."
    ], "Page 8")

    add_table_page(doc, "Annual Cash Flow Summary",
                   ["Category", "FY 2025", "FY 2024", "Change"],
                   [
                       ["Operating Cash Flow", "$52.8M", "$38.4M", "+37.5%"],
                       ["Capital Expenditures", "-$14.2M", "-$9.8M", "+44.9%"],
                       ["Free Cash Flow", "$38.6M", "$28.6M", "+35.0%"],
                       ["Acquisitions", "$0.0M", "-$15.2M", "N/A"],
                       ["Debt Changes (Net)", "-$8.0M", "+$12.0M", "N/A"],
                       ["Share Repurchases", "-$7.5M", "-$3.0M", "+150%"],
                       ["Dividends Paid", "-$5.6M", "-$4.8M", "+16.7%"],
                       ["Net Cash Change", "+$17.5M", "+$8.0M", "+118.8%"],
                   ], "Page 9")

    add_content_page(doc, "FY 2026 Outlook & Strategic Priorities", [
        "Revenue guidance for FY 2026: $245-$255 million, representing 15-20% growth. "
        "Operating margin target: 19-21%. CapEx budget: $16-$18 million.",
        "Strategic priorities: (1) Scale AI Analytics Suite to $40M+ ARR, (2) Expand managed "
        "security services to 200+ customers, (3) Establish presence in 3 additional APAC markets, "
        "(4) Launch next-generation cloud platform with edge computing capabilities.",
        "M&A: Board has authorized exploration of tuck-in acquisitions in the $20-$50M range "
        "targeting complementary AI/ML capabilities and geographic expansion opportunities.",
        "We enter FY 2026 with record backlog, a diversified product portfolio, and strong balance "
        "sheet positioning us well for continued double-digit growth."
    ], "Page 10")

    path = f'{FINANCE_DIR}/q4_report.pdf'
    doc.save(path)
    doc.close()
    print(f'Created: {path} ({10} pages)')


def create_initial():
    # Create finance directory
    os.makedirs(FINANCE_DIR, exist_ok=True)

    # Create all four quarterly reports
    create_q1_report()
    create_q2_report()
    create_q3_report()
    create_q4_report()

    # Verify no merged file exists
    merged_path = f'{FINANCE_DIR}/annual_report_2025.pdf'
    if os.path.exists(merged_path):
        os.remove(merged_path)
        print(f'Removed pre-existing merged file: {merged_path}')

    print(f'\nAll quarterly reports created in {FINANCE_DIR}')

    # Open the file manager showing the finance directory for GUI-ready state
    launch_gui(f'nautilus "{FINANCE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')


create_initial()
