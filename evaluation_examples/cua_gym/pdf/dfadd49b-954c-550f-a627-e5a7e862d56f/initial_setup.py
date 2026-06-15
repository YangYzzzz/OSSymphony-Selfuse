"""
Initial Setup: Create four quarterly financial report PDFs for merging task.
Task ID: pdf_pw_049
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_049'
FINANCE_DIR = f'{WORKDIR}/finance'

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


def add_header_footer(page, quarter_label, page_num_in_quarter, total_in_quarter):
    """Add header and footer to a report page."""
    # Header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(50, 60), pymupdf.Point(W - 50, 60))
    shape.finish(color=(0.2, 0.3, 0.5), width=1.5)
    shape.commit()

    # Header text
    page.insert_text(pymupdf.Point(50, 50), f"Nextera Corp - {quarter_label} Financial Report",
                     fontsize=10, fontname="hebo", color=(0.2, 0.3, 0.5))
    page.insert_text(pymupdf.Point(W - 150, 50), "CONFIDENTIAL",
                     fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))


def create_title_page(doc, quarter_label, date_range, year=2025):
    """Create a title page for a quarterly report."""
    page = doc.new_page(width=W, height=H)

    # Company name
    page.insert_text(pymupdf.Point(W/2 - 120, 200), "NEXTERA CORPORATION",
                     fontsize=22, fontname="hebo", color=(0.15, 0.25, 0.45))

    # Decorative line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(150, 220), pymupdf.Point(W - 150, 220))
    shape.finish(color=(0.7, 0.15, 0.15), width=2)
    shape.commit()

    # Quarter title
    page.insert_text(pymupdf.Point(W/2 - 140, 280), f"{quarter_label} Financial Report",
                     fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.1))

    # Date range
    page.insert_text(pymupdf.Point(W/2 - 80, 310), date_range,
                     fontsize=14, fontname="tiro", color=(0.3, 0.3, 0.3))

    # Year
    page.insert_text(pymupdf.Point(W/2 - 30, 340), f"Fiscal Year {year}",
                     fontsize=12, fontname="tiit", color=(0.4, 0.4, 0.4))

    # Footer
    page.insert_text(pymupdf.Point(W/2 - 100, H - 100),
                     "Prepared by the Finance Department",
                     fontsize=10, fontname="tiro", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(W/2 - 60, H - 80),
                     "For Internal Use Only",
                     fontsize=9, fontname="tiit", color=(0.5, 0.5, 0.5))
    return page


def add_text_page(doc, quarter_label, title, paragraphs):
    """Add a text content page."""
    page = doc.new_page(width=W, height=H)
    add_header_footer(page, quarter_label, 0, 0)

    y = 90
    page.insert_text(pymupdf.Point(50, y), title,
                     fontsize=16, fontname="hebo", color=(0.15, 0.25, 0.45))
    y += 30

    for para in paragraphs:
        rect = pymupdf.Rect(50, y, W - 50, y + 120)
        excess = page.insert_textbox(rect, para, fontsize=10, fontname="tiro",
                                     color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 120 - max(0, excess) + 10
        if y > H - 100:
            break
    return page


def add_table_page(doc, quarter_label, title, headers, rows):
    """Add a page with a simple table using text positioning."""
    page = doc.new_page(width=W, height=H)
    add_header_footer(page, quarter_label, 0, 0)

    y = 90
    page.insert_text(pymupdf.Point(50, y), title,
                     fontsize=14, fontname="hebo", color=(0.15, 0.25, 0.45))
    y += 30

    # Table header background
    col_width = (W - 100) / len(headers)
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(50, y - 12, W - 50, y + 6))
    shape.finish(color=(0.15, 0.25, 0.45), fill=(0.15, 0.25, 0.45), width=0.5)
    shape.commit()

    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(55 + i * col_width, y),
                         h, fontsize=9, fontname="hebo", color=(1, 1, 1))
    y += 18

    for row_idx, row in enumerate(rows):
        if row_idx % 2 == 0:
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(50, y - 12, W - 50, y + 6))
            shape.finish(fill=(0.94, 0.94, 0.97), width=0)
            shape.commit()
        for i, val in enumerate(row):
            page.insert_text(pymupdf.Point(55 + i * col_width, y),
                             str(val), fontsize=9, fontname="tiro", color=(0.1, 0.1, 0.1))
        y += 18
        if y > H - 80:
            break

    return page


def create_quarterly_report(filepath, quarter_num, num_pages):
    """Create a quarterly financial report PDF with the specified number of pages."""
    doc = pymupdf.open()

    quarter_labels = {1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"}
    date_ranges = {
        1: "January - March 2025",
        2: "April - June 2025",
        3: "July - September 2025",
        4: "October - December 2025"
    }
    ql = quarter_labels[quarter_num]
    dr = date_ranges[quarter_num]

    # Page 1: Title page
    create_title_page(doc, ql, dr)
    pages_created = 1

    # Page 2: Executive Summary
    exec_paragraphs = [
        f"The {ql} period demonstrated continued momentum across all business segments. "
        f"Total revenue reached ${'%.1f' % (42.3 + quarter_num * 3.7)}M, representing a "
        f"{'%.1f' % (5.2 + quarter_num * 1.1)}% increase over the prior quarter. Operating margins "
        f"improved to {'%.1f' % (18.5 + quarter_num * 0.8)}%, driven by operational efficiencies "
        f"and favorable product mix shifts.",

        f"Key achievements during {ql} include the successful launch of three new product lines, "
        f"expansion into two additional international markets, and the completion of our digital "
        f"transformation initiative. Customer acquisition costs decreased by {'%.1f' % (3.2 + quarter_num * 0.5)}% "
        f"while customer lifetime value increased by {'%.1f' % (7.1 + quarter_num * 1.2)}%.",

        f"Looking ahead, management remains optimistic about the growth trajectory. The pipeline "
        f"for the upcoming quarter includes {12 + quarter_num * 3} pending enterprise deals valued at "
        f"an estimated ${'%.1f' % (8.5 + quarter_num * 2.1)}M in annual recurring revenue."
    ]
    add_text_page(doc, ql, "Executive Summary", exec_paragraphs)
    pages_created += 1

    # Page 3: Revenue Breakdown
    rev_headers = ["Segment", "Revenue", "Growth", "Margin", "Contribution"]
    rev_data = [
        ["Enterprise Software", f"${14.2 + quarter_num * 1.2:.1f}M", f"+{6.3 + quarter_num:.1f}%", f"{22.1 + quarter_num:.1f}%", f"{33 + quarter_num}%"],
        ["Cloud Services", f"${11.8 + quarter_num * 0.9:.1f}M", f"+{8.7 + quarter_num * 0.5:.1f}%", f"{28.4 + quarter_num * 0.3:.1f}%", f"{27 + quarter_num}%"],
        ["Professional Services", f"${8.5 + quarter_num * 0.6:.1f}M", f"+{3.1 + quarter_num * 0.3:.1f}%", f"{15.6 + quarter_num * 0.2:.1f}%", f"{20 - quarter_num}%"],
        ["Managed Solutions", f"${5.3 + quarter_num * 0.5:.1f}M", f"+{4.5 + quarter_num * 0.4:.1f}%", f"{19.2 + quarter_num * 0.5:.1f}%", f"{12 + quarter_num}%"],
        ["Consulting", f"${2.5 + quarter_num * 0.3:.1f}M", f"+{2.8 + quarter_num * 0.2:.1f}%", f"{12.3 + quarter_num * 0.4:.1f}%", f"{8 - quarter_num}%"],
    ]
    add_table_page(doc, ql, "Revenue Breakdown by Segment", rev_headers, rev_data)
    pages_created += 1

    # Page 4: Operating Expenses
    exp_headers = ["Category", "Amount", "% of Revenue", "vs Prior Q", "Budget Var"]
    exp_data = [
        ["Cost of Revenue", f"${18.2 + quarter_num * 0.8:.1f}M", f"{42.3 - quarter_num * 0.5:.1f}%", f"+{2.1 + quarter_num * 0.3:.1f}%", f"-{0.8 + quarter_num * 0.1:.1f}%"],
        ["R&D", f"${7.8 + quarter_num * 0.4:.1f}M", f"{18.1 + quarter_num * 0.2:.1f}%", f"+{5.3 + quarter_num * 0.2:.1f}%", f"+{1.2 + quarter_num * 0.1:.1f}%"],
        ["Sales & Marketing", f"${6.2 + quarter_num * 0.3:.1f}M", f"{14.4 - quarter_num * 0.3:.1f}%", f"+{1.8 + quarter_num * 0.1:.1f}%", f"-{0.5 + quarter_num * 0.1:.1f}%"],
        ["G&A", f"${3.5 + quarter_num * 0.2:.1f}M", f"{8.1 + quarter_num * 0.1:.1f}%", f"+{0.9 + quarter_num * 0.1:.1f}%", f"+{0.3:.1f}%"],
        ["Depreciation", f"${1.8 + quarter_num * 0.1:.1f}M", f"{4.2:.1f}%", f"+{0.5:.1f}%", f"{0.0:.1f}%"],
    ]
    add_table_page(doc, ql, "Operating Expenses", exp_headers, exp_data)
    pages_created += 1

    # Page 5: Balance Sheet Summary
    bs_paragraphs = [
        f"Total assets at the end of {ql} stood at ${'%.1f' % (285.4 + quarter_num * 12.3)}M, "
        f"reflecting growth in both current and non-current asset categories. Cash and equivalents "
        f"increased to ${'%.1f' % (45.6 + quarter_num * 3.8)}M, providing strong liquidity for "
        f"planned capital expenditures and strategic acquisitions.",

        f"Total liabilities decreased to ${'%.1f' % (128.7 - quarter_num * 2.1)}M as the company "
        f"continued its deleveraging strategy. The debt-to-equity ratio improved to "
        f"{'%.2f' % (0.82 - quarter_num * 0.05)}, within our target range of 0.6-0.8.",

        f"Stockholders' equity reached ${'%.1f' % (156.7 + quarter_num * 14.4)}M, driven by "
        f"retained earnings growth and favorable mark-to-market adjustments on investment securities."
    ]
    add_text_page(doc, ql, "Balance Sheet Summary", bs_paragraphs)
    pages_created += 1

    # Page 6: Cash Flow
    cf_headers = ["Item", "Amount", "vs Prior Q", "YTD"]
    cf_data = [
        ["Operating Cash Flow", f"${9.8 + quarter_num * 1.1:.1f}M", f"+{4.2 + quarter_num * 0.3:.1f}%", f"${9.8 * quarter_num:.1f}M"],
        ["Capital Expenditures", f"-${3.2 + quarter_num * 0.2:.1f}M", f"+{1.5 + quarter_num * 0.1:.1f}%", f"-${3.2 * quarter_num:.1f}M"],
        ["Free Cash Flow", f"${6.6 + quarter_num * 0.9:.1f}M", f"+{5.8 + quarter_num * 0.4:.1f}%", f"${6.6 * quarter_num:.1f}M"],
        ["Dividends Paid", f"-${1.5:.1f}M", "0.0%", f"-${1.5 * quarter_num:.1f}M"],
        ["Share Repurchases", f"-${2.0 + quarter_num * 0.3:.1f}M", f"+{8.0 + quarter_num * 0.5:.1f}%", f"-${2.0 * quarter_num:.1f}M"],
        ["Net Cash Change", f"${3.1 + quarter_num * 0.6:.1f}M", f"+{3.3 + quarter_num * 0.2:.1f}%", f"${3.1 * quarter_num:.1f}M"],
    ]
    add_table_page(doc, ql, "Cash Flow Statement", cf_headers, cf_data)
    pages_created += 1

    # Page 7: Key Metrics
    km_headers = ["Metric", "Current", "Prior Q", "YoY Change", "Target"]
    km_data = [
        ["Revenue Growth", f"{5.2 + quarter_num * 1.1:.1f}%", f"{4.8 + quarter_num * 0.9:.1f}%", f"+{2.3 + quarter_num * 0.4:.1f}pp", ">5.0%"],
        ["EBITDA Margin", f"{22.4 + quarter_num * 0.6:.1f}%", f"{21.8 + quarter_num * 0.5:.1f}%", f"+{1.5 + quarter_num * 0.2:.1f}pp", ">20.0%"],
        ["Net Income Margin", f"{12.8 + quarter_num * 0.4:.1f}%", f"{12.2 + quarter_num * 0.3:.1f}%", f"+{0.8 + quarter_num * 0.1:.1f}pp", ">10.0%"],
        ["Customer Count", f"{2340 + quarter_num * 85}", f"{2255 + quarter_num * 70}", f"+{180 + quarter_num * 15}", ">2500"],
        ["Avg Deal Size", f"${34.5 + quarter_num * 1.2:.1f}K", f"${33.8 + quarter_num * 1.0:.1f}K", f"+{5.2 + quarter_num * 0.3:.1f}%", ">$30K"],
        ["NPS Score", f"{72 + quarter_num * 2}", f"{70 + quarter_num}", f"+{3 + quarter_num}", ">70"],
        ["Churn Rate", f"{2.1 - quarter_num * 0.1:.1f}%", f"{2.3 - quarter_num * 0.1:.1f}%", f"-{0.3 + quarter_num * 0.05:.2f}pp", "<2.5%"],
        ["ARR", f"${168.5 + quarter_num * 8.2:.1f}M", f"${160.3 + quarter_num * 7.5:.1f}M", f"+{12.4 + quarter_num * 1.1:.1f}%", ">$170M"],
    ]
    add_table_page(doc, ql, "Key Performance Indicators", km_headers, km_data)
    pages_created += 1

    # Fill remaining pages with varied content
    additional_sections = [
        ("Regional Performance", [
            f"North America delivered strong results with revenue of ${'%.1f' % (25.3 + quarter_num * 2.1)}M, "
            f"representing {58 + quarter_num}% of total revenue. The region benefited from enterprise "
            f"deal closures and expansion within existing accounts.",
            f"EMEA contributed ${'%.1f' % (10.8 + quarter_num * 0.9)}M, with particular strength in "
            f"the DACH region and Nordic countries. The UK market showed signs of recovery following "
            f"the regulatory compliance deadline.",
            f"Asia-Pacific revenue reached ${'%.1f' % (6.2 + quarter_num * 0.7)}M, led by Japan and "
            f"Australia. Market entry efforts in Southeast Asia are progressing with {3 + quarter_num} "
            f"new partnership agreements signed during the quarter."
        ]),
        ("Product Development Update", [
            f"The engineering team shipped {15 + quarter_num * 3} feature releases during {ql}, "
            f"including the highly anticipated real-time analytics dashboard and AI-powered "
            f"recommendation engine. Platform uptime averaged {99.92 + quarter_num * 0.02:.2f}%.",
            f"R&D investment continued at {'%.1f' % (18.1 + quarter_num * 0.2)}% of revenue, "
            f"focused on machine learning capabilities, platform scalability, and security enhancements. "
            f"Patent applications filed: {4 + quarter_num}.",
            f"Customer-requested feature completion rate improved to {87 + quarter_num * 2}%, "
            f"with average time-to-delivery reduced from 45 days to {38 - quarter_num * 2} days."
        ]),
        ("Risk Assessment", [
            f"Key risk factors monitored during {ql} include foreign exchange exposure, "
            f"with hedging coverage maintaining at {82 + quarter_num * 3}% of forecasted "
            f"international revenue streams.",
            f"Cybersecurity posture strengthened with {zero_day_count} zero-day vulnerabilities "
            f"detected and patched within SLA. SOC 2 Type II audit completed with no material findings."
            if False else
            f"Cybersecurity posture strengthened with zero critical vulnerabilities during {ql}. "
            f"SOC 2 Type II audit completed successfully with no material findings.",
            f"Regulatory compliance remains strong across all operating jurisdictions. GDPR and "
            f"CCPA compliance audits passed with minor observations addressed within 30 days."
        ]),
        ("Human Resources", [
            f"Headcount at end of {ql}: {845 + quarter_num * 28} employees across {12 + quarter_num} "
            f"global offices. Net new hires: {42 + quarter_num * 5}, with {68 + quarter_num * 2}% in "
            f"technical roles.",
            f"Employee engagement score: {4.2 + quarter_num * 0.05:.1f}/5.0 (industry avg: 3.8). "
            f"Voluntary attrition rate declined to {8.5 - quarter_num * 0.3:.1f}% annualized. "
            f"Diversity hiring targets exceeded with {45 + quarter_num}% of new hires from "
            f"underrepresented groups.",
            f"Training investment: ${1.2 + quarter_num * 0.1:.1f}M allocated to professional "
            f"development programs. Leadership development program enrolled {24 + quarter_num * 3} "
            f"high-potential managers."
        ]),
        ("Strategic Initiatives", [
            f"The digital transformation roadmap is {65 + quarter_num * 8}% complete, with "
            f"migration of legacy systems to cloud infrastructure proceeding ahead of schedule. "
            f"Expected annual savings: ${'%.1f' % (4.5 + quarter_num * 0.8)}M upon completion.",
            f"Strategic partnership with Meridian Technologies expanded to include joint "
            f"go-to-market initiatives in {3 + quarter_num} new verticals, expected to generate "
            f"${'%.1f' % (2.8 + quarter_num * 0.6)}M in incremental revenue over 18 months.",
            f"M&A pipeline includes {2 + quarter_num} qualified targets under evaluation, "
            f"with combined addressable market opportunity estimated at ${'%.0f' % (45 + quarter_num * 12)}M."
        ]),
    ]

    section_idx = 0
    while pages_created < num_pages:
        if section_idx < len(additional_sections):
            title, paras = additional_sections[section_idx]
            add_text_page(doc, ql, title, paras)
            section_idx += 1
        else:
            # Add more table/data pages
            extra_headers = ["Month", "Transactions", "Avg Value", "Total", "Status"]
            months_base = {1: ["Jan", "Feb", "Mar"], 2: ["Apr", "May", "Jun"],
                          3: ["Jul", "Aug", "Sep"], 4: ["Oct", "Nov", "Dec"]}
            extra_data = []
            for m in months_base[quarter_num]:
                for week in range(1, 5):
                    extra_data.append([
                        f"{m} W{week}",
                        f"{320 + quarter_num * 15 + week * 8}",
                        f"${1.2 + quarter_num * 0.1 + week * 0.05:.2f}K",
                        f"${(320 + quarter_num * 15 + week * 8) * (1.2 + quarter_num * 0.1 + week * 0.05):.1f}K",
                        "Reconciled"
                    ])
            add_table_page(doc, ql, f"Detailed Transaction Log - {ql}", extra_headers, extra_data[:12])
            section_idx += 1
        pages_created += 1

    doc.save(filepath)
    doc.close()
    print(f"Created {filepath} with {num_pages} pages")


def create_initial():
    os.makedirs(FINANCE_DIR, exist_ok=True)

    # Create the four quarterly reports
    # Q1: 12 pages, Q2: 14 pages, Q3: 11 pages, Q4: 13 pages
    create_quarterly_report(f'{FINANCE_DIR}/q1.pdf', 1, 12)
    create_quarterly_report(f'{FINANCE_DIR}/q2.pdf', 2, 14)
    create_quarterly_report(f'{FINANCE_DIR}/q3.pdf', 3, 11)
    create_quarterly_report(f'{FINANCE_DIR}/q4.pdf', 4, 13)

    print(f"All quarterly reports created in {FINANCE_DIR}")

    # Open the finance directory in file manager for the agent
    launch_gui(f'nautilus "{FINANCE_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched file manager with DISPLAY=:0")


create_initial()
