"""
Initial Setup: Import bookmarks from text file into PDF
Task ID: pdf_mbc_049
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_049'
DOCS_DIR = f'{WORKDIR}/Documents'
PDF_OUTPUT = f'{DOCS_DIR}/blank_report.pdf'
TXT_OUTPUT = f'{DOCS_DIR}/bookmark_data.txt'


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

    # --- Create 60-page blank report PDF (realistic content, NO bookmarks) ---
    doc = pymupdf.open()

    # Section titles and page ranges for realistic content
    sections = [
        ("Executive Summary", 1, 4),
        ("Financial Overview", 5, 14),
        ("Revenue Analysis", 5, 9),
        ("Expense Breakdown", 10, 14),
        ("Projections", 15, 25),
        ("Q1 Forecast", 15, 19),
        ("Q2 Forecast", 20, 25),
        ("Operational Metrics", 26, 35),
        ("Human Resources", 36, 42),
        ("Technology Infrastructure", 43, 50),
        ("Risk Assessment", 51, 55),
        ("Appendices", 56, 60),
    ]

    # Build a map of page -> section title for headers
    page_headers = {}
    for title, start, end in sections:
        for p in range(start, end + 1):
            if p not in page_headers:
                page_headers[p] = title

    # Realistic body text paragraphs
    body_paragraphs = [
        "The organization demonstrated strong performance across all key metrics during the reporting period. Revenue growth exceeded initial projections by 12%, driven primarily by expansion in the Asia-Pacific region and successful product launches in Q3.",
        "Operating expenses remained within budget constraints, with notable efficiencies achieved in supply chain management and procurement processes. The implementation of automated workflows reduced processing times by an average of 23%.",
        "Market analysis indicates favorable conditions for continued growth in the upcoming fiscal year. Consumer confidence indices remain elevated, and industry-specific demand drivers show sustained momentum across primary business segments.",
        "Strategic investments in digital transformation initiatives are expected to yield measurable returns within the next 18 months. Cloud migration efforts have achieved 78% completion, with full deployment targeted for Q2 of the next fiscal year.",
        "Employee engagement scores improved by 8 percentage points year-over-year, reflecting the positive impact of revised compensation structures and enhanced professional development programs introduced in the first half of the year.",
        "Capital expenditure allocations were directed toward infrastructure modernization and capacity expansion at key manufacturing facilities. These investments support projected demand growth and strengthen the organization's competitive positioning.",
        "Risk mitigation frameworks were enhanced to address emerging cybersecurity threats and regulatory compliance requirements. Third-party audits confirmed adherence to industry standards and best practices across all operational domains.",
        "Customer satisfaction metrics maintained strong positive trends, with Net Promoter Scores increasing from 62 to 71 during the reporting period. Service delivery improvements contributed to a 15% reduction in customer complaint volumes.",
    ]

    for page_num in range(1, 61):
        page = doc.new_page(width=595, height=842)  # A4

        # Header
        header_text = page_headers.get(page_num, "Annual Report 2025")
        page.insert_text(
            pymupdf.Point(72, 50),
            header_text,
            fontsize=18,
            fontname="hebo",
            color=(0.1, 0.1, 0.4),
        )

        # Horizontal rule under header
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 60), pymupdf.Point(523, 60))
        shape.finish(color=(0.3, 0.3, 0.6), width=1.5)
        shape.commit()

        # Body text - multiple paragraphs per page
        y_pos = 90
        for i in range(3):
            para_idx = (page_num * 3 + i) % len(body_paragraphs)
            paragraph = body_paragraphs[para_idx]

            rect = pymupdf.Rect(72, y_pos, 523, y_pos + 180)
            page.insert_textbox(
                rect,
                paragraph,
                fontsize=11,
                fontname="helv",
                color=(0.1, 0.1, 0.1),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )
            y_pos += 195

        # Page number footer
        page.insert_text(
            pymupdf.Point(280, 810),
            f"Page {page_num}",
            fontsize=9,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

        # Company footer
        page.insert_text(
            pymupdf.Point(72, 825),
            "Meridian Global Partners - Confidential",
            fontsize=8,
            fontname="heit",
            color=(0.5, 0.5, 0.5),
        )

    # Set metadata (no TOC/bookmarks)
    doc.set_metadata({
        "title": "Annual Report 2025 - Meridian Global Partners",
        "author": "Meridian Global Partners",
        "subject": "Annual Financial and Operational Report",
        "creator": "Report Generation System",
    })

    # Explicitly ensure no TOC
    doc.set_toc([])

    doc.save(PDF_OUTPUT)
    doc.close()
    print(f"Initial PDF created: {PDF_OUTPUT} (60 pages, no bookmarks)")

    # --- Create bookmark_data.txt ---
    bookmark_lines = [
        "0|Executive Summary|1",
        "0|Financial Overview|5",
        "1|Revenue|5",
        "1|Expenses|10",
        "0|Projections|15",
        "1|Q1 Forecast|15",
        "1|Q2 Forecast|20",
    ]
    with open(TXT_OUTPUT, 'w') as f:
        f.write('\n'.join(bookmark_lines) + '\n')
    print(f"Bookmark data created: {TXT_OUTPUT}")

    # GUI-ready startup: open the PDF in Evince
    launch_gui(f'evince "{PDF_OUTPUT}"', delay_sec=2.0)
    print("GUI_READY: launched Evince with DISPLAY=:0")


create_initial()
