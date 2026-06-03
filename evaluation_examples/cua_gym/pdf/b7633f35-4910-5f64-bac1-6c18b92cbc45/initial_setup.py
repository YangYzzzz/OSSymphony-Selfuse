"""
Initial Setup: Create four quarterly financial PDFs for NexGen Industries
Task ID: pdf_fin_051
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_051'
QUARTERLY_DIR = f'{WORKDIR}/finance/quarterly'

# Page dimensions (Letter size)
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


def add_title_page(doc, quarter_label, year="2024"):
    """Add a title/cover page for a quarterly report."""
    page = doc.new_page(width=W, height=H)
    # Company logo area (just a colored rectangle)
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(50, 50, 562, 130))
    shape.finish(fill=(0.0, 0.2, 0.45), color=(0.0, 0.2, 0.45))
    shape.commit()

    page.insert_text(pymupdf.Point(72, 105), "NEXGEN INDUSTRIES", fontsize=28, fontname="hebo", color=(1, 1, 1))
    page.insert_text(pymupdf.Point(72, 220), f"{quarter_label} Financial Report", fontsize=24, fontname="hebo", color=(0.0, 0.2, 0.45))
    page.insert_text(pymupdf.Point(72, 260), f"Fiscal Year {year}", fontsize=16, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 310), "Prepared by: Finance Department", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 330), "Date: March 2025", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 370), "Distribution: Board of Directors, Senior Management", fontsize=11, fontname="heit", color=(0.4, 0.4, 0.4))


def add_summary_page(doc, quarter, revenue, expenses, net_income, headcount):
    """Add an executive summary page."""
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(72, y), "Executive Summary", fontsize=18, fontname="hebo", color=(0.0, 0.2, 0.45))
    y += 35

    summary_text = (
        f"NexGen Industries reported total revenue of ${revenue:,.0f} for {quarter}, "
        f"representing continued growth in our core business segments. Operating expenses "
        f"totaled ${expenses:,.0f}, resulting in a net income of ${net_income:,.0f}. "
        f"The company maintained a workforce of {headcount} full-time employees across "
        f"all divisions."
    )
    rect = pymupdf.Rect(72, y, 540, y + 120)
    page.insert_textbox(rect, summary_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    y += 140
    page.insert_text(pymupdf.Point(72, y), "Key Highlights:", fontsize=14, fontname="hebo", color=(0.0, 0.2, 0.45))
    y += 25
    highlights = [
        f"Revenue growth of {((revenue - expenses) / expenses * 100):.1f}% over operating costs",
        "Successful launch of CloudSync Pro platform in APAC region",
        "Strategic partnership with Meridian Technologies finalized",
        f"Employee headcount increased to {headcount} (+3.2% QoQ)",
        "R&D investment expanded to 18% of total revenue",
    ]
    for h in highlights:
        page.insert_text(pymupdf.Point(90, y), f"- {h}", fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 18


def add_revenue_page(doc, quarter, segments):
    """Add a revenue breakdown page."""
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(72, y), "Revenue Breakdown by Segment", fontsize=18, fontname="hebo", color=(0.0, 0.2, 0.45))
    y += 40

    # Draw table header
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(72, y, 540, y + 25))
    shape.finish(fill=(0.0, 0.2, 0.45), color=(0.0, 0.2, 0.45))
    shape.commit()

    headers = ["Segment", "Revenue ($)", "% of Total", "YoY Growth"]
    x_positions = [80, 220, 370, 470]
    for i, hdr in enumerate(headers):
        page.insert_text(pymupdf.Point(x_positions[i], y + 17), hdr, fontsize=10, fontname="hebo", color=(1, 1, 1))
    y += 30

    total_rev = sum(s[1] for s in segments)
    for idx, (name, rev, growth) in enumerate(segments):
        bg = (0.95, 0.95, 0.97) if idx % 2 == 0 else (1, 1, 1)
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(72, y, 540, y + 22))
        shape.finish(fill=bg, color=(0.85, 0.85, 0.85))
        shape.commit()

        pct = rev / total_rev * 100
        page.insert_text(pymupdf.Point(80, y + 15), name, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(220, y + 15), f"${rev:,.0f}", fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(370, y + 15), f"{pct:.1f}%", fontsize=10, fontname="helv", color=(0, 0, 0))
        growth_color = (0, 0.5, 0) if growth >= 0 else (0.8, 0, 0)
        page.insert_text(pymupdf.Point(470, y + 15), f"{growth:+.1f}%", fontsize=10, fontname="helv", color=growth_color)
        y += 22


def add_expense_page(doc, quarter, categories):
    """Add an expense analysis page."""
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(72, y), "Operating Expense Analysis", fontsize=18, fontname="hebo", color=(0.0, 0.2, 0.45))
    y += 40

    for cat_name, items in categories:
        page.insert_text(pymupdf.Point(72, y), cat_name, fontsize=13, fontname="hebo", color=(0.15, 0.15, 0.15))
        y += 22
        for item_name, amount in items:
            page.insert_text(pymupdf.Point(90, y), f"{item_name}:", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            page.insert_text(pymupdf.Point(350, y), f"${amount:,.0f}", fontsize=10, fontname="helv", color=(0, 0, 0))
            y += 17
        y += 10
        if y > 700:
            break


def add_narrative_page(doc, title, paragraphs):
    """Add a page with narrative text content."""
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(72, y), title, fontsize=16, fontname="hebo", color=(0.0, 0.2, 0.45))
    y += 35
    for para in paragraphs:
        rect = pymupdf.Rect(72, y, 540, y + 80)
        excess = page.insert_textbox(rect, para, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 85
        if y > 720:
            break


def add_filler_pages(doc, count, section_title):
    """Add filler content pages for realistic page count."""
    subsections = [
        ("Regional Performance", [
            "The North American division continued to outperform expectations with strong demand for enterprise solutions. Client retention rates exceeded 94% across all major accounts. The EMEA region showed recovery in the second half with new deployments in Germany and the UK driving growth.",
            "Asia-Pacific operations expanded with the opening of the Singapore technology center. Japan enterprise sales grew 15% driven by financial services sector adoption. Australia and New Zealand showed steady growth in mid-market segment.",
        ]),
        ("Product Development", [
            "The engineering team delivered three major product releases during the quarter. CloudSync Pro received significant enhancements including multi-tenant architecture and advanced analytics dashboards. The platform now supports over 200 enterprise integrations.",
            "Research initiatives in machine learning and predictive analytics continued to progress. The AI-powered recommendation engine entered beta testing with select enterprise clients, receiving positive feedback on accuracy and performance metrics.",
        ]),
        ("Market Analysis", [
            "Industry analysts project continued growth in the enterprise software market through 2025. NexGen Industries maintains a strong competitive position with differentiated offerings in cloud infrastructure and data management solutions.",
            "Competitive landscape remains dynamic with increased M&A activity among mid-tier players. NexGen's strategic acquisitions of DataFlow Systems and CloudBridge have strengthened our market position in key verticals.",
        ]),
        ("Risk Assessment", [
            "Currency fluctuation exposure remains a key concern for international operations. The finance team has implemented enhanced hedging strategies to mitigate foreign exchange risks across major trading currencies.",
            "Regulatory compliance requirements continue to evolve globally. The compliance team has proactively updated policies and procedures to align with GDPR amendments and emerging data sovereignty regulations in Asian markets.",
        ]),
        ("Human Resources", [
            "Talent acquisition efforts yielded strong results with 127 new hires across engineering, sales, and operations. The company maintained an employee satisfaction score of 4.2 out of 5.0, above industry benchmarks.",
            "The leadership development program graduated its third cohort of 24 high-potential managers. Training investments totaled $2.4M for the quarter, focused on technical upskilling and management development.",
        ]),
        ("Operational Metrics", [
            "System uptime averaged 99.97% across all production environments. Customer support ticket resolution time decreased by 12% to an average of 4.2 hours. Net Promoter Score improved to 72, up from 68 in the prior quarter.",
            "Supply chain optimization initiatives reduced infrastructure procurement costs by 8%. Data center consolidation projects progressed on schedule with migration of three legacy environments to cloud-native architecture.",
        ]),
        ("Sustainability Report", [
            "Carbon emissions reduction targets progressed with a 15% decrease in scope 2 emissions. Renewable energy now powers 60% of global data center operations. The sustainability committee approved new ESG reporting frameworks aligned with GRI standards.",
            "Community engagement programs contributed over 2,000 volunteer hours. The NexGen Foundation distributed $500K in grants supporting STEM education initiatives across underserved communities.",
        ]),
    ]

    for i in range(count):
        idx = i % len(subsections)
        title, paras = subsections[idx]
        add_narrative_page(doc, f"{section_title} - {title}", paras)


def create_quarterly_pdf(filepath, quarter_label, quarter_short, num_pages, revenue, expenses, net_income, headcount):
    """Create a single quarterly financial report PDF."""
    doc = pymupdf.open()

    # Page 1: Title page
    add_title_page(doc, quarter_label)

    # Page 2: Executive Summary
    add_summary_page(doc, quarter_short, revenue, expenses, net_income, headcount)

    # Page 3: Revenue Breakdown
    segments = [
        ("Enterprise Software", revenue * 0.42, 8.3),
        ("Cloud Services", revenue * 0.28, 15.7),
        ("Professional Services", revenue * 0.15, 3.2),
        ("Data Analytics", revenue * 0.10, 22.1),
        ("Support & Maintenance", revenue * 0.05, -1.4),
    ]
    add_revenue_page(doc, quarter_short, segments)

    # Page 4: Expense Analysis
    categories = [
        ("Personnel Costs", [
            ("Salaries & Wages", expenses * 0.45),
            ("Benefits & Insurance", expenses * 0.12),
            ("Recruitment & Training", expenses * 0.03),
        ]),
        ("Technology & Infrastructure", [
            ("Cloud Hosting & Services", expenses * 0.10),
            ("Software Licenses", expenses * 0.05),
            ("Hardware & Equipment", expenses * 0.04),
        ]),
        ("Sales & Marketing", [
            ("Marketing Campaigns", expenses * 0.08),
            ("Sales Operations", expenses * 0.06),
            ("Events & Conferences", expenses * 0.02),
        ]),
        ("General & Administrative", [
            ("Office & Facilities", expenses * 0.03),
            ("Legal & Professional Fees", expenses * 0.015),
            ("Insurance & Compliance", expenses * 0.005),
        ]),
    ]
    add_expense_page(doc, quarter_short, categories)

    # Pages 5+: Fill remaining pages with detailed content
    remaining = num_pages - 4
    if remaining > 0:
        add_filler_pages(doc, remaining, f"{quarter_label} Detailed Analysis")

    doc.save(filepath)
    doc.close()
    print(f"Created {filepath} with {num_pages} pages")


def create_initial():
    os.makedirs(QUARTERLY_DIR, exist_ok=True)

    # Q1: 15 pages
    create_quarterly_pdf(
        f"{QUARTERLY_DIR}/q1.pdf", "Q1 2024", "Q1",
        num_pages=15, revenue=28_450_000, expenses=22_360_000,
        net_income=6_090_000, headcount=1_245
    )

    # Q2: 14 pages
    create_quarterly_pdf(
        f"{QUARTERLY_DIR}/q2.pdf", "Q2 2024", "Q2",
        num_pages=14, revenue=31_200_000, expenses=24_150_000,
        net_income=7_050_000, headcount=1_298
    )

    # Q3: 16 pages
    create_quarterly_pdf(
        f"{QUARTERLY_DIR}/q3.pdf", "Q3 2024", "Q3",
        num_pages=16, revenue=29_870_000, expenses=23_540_000,
        net_income=6_330_000, headcount=1_312
    )

    # Q4: 15 pages
    create_quarterly_pdf(
        f"{QUARTERLY_DIR}/q4.pdf", "Q4 2024", "Q4",
        num_pages=15, revenue=34_680_000, expenses=26_210_000,
        net_income=8_470_000, headcount=1_356
    )

    # Open file manager to show the quarterly directory
    launch_gui(f'nautilus "{QUARTERLY_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
