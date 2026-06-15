"""
Initial Setup: Create mixed orientation PDF with portrait and landscape pages.
Task ID: pdf_gf1_039
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/mixed_orientation.pdf'


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
    import pymupdf

    os.makedirs(DOCS_DIR, exist_ok=True)

    PORTRAIT_W, PORTRAIT_H = 612, 792   # Letter portrait
    LANDSCAPE_W, LANDSCAPE_H = 792, 612  # Letter landscape

    # Page configs: (width, height, title, body_text)
    pages = [
        (PORTRAIT_W, PORTRAIT_H, "Executive Summary",
         "This document provides an overview of the Q4 2025 financial performance "
         "for Meridian Holdings. Revenue increased by 12% year-over-year, driven by "
         "strong demand in the Asia-Pacific region. Operating margins improved to 23.4%, "
         "reflecting successful cost optimization initiatives launched in Q2."),

        (PORTRAIT_W, PORTRAIT_H, "Revenue Breakdown",
         "North America: $45.2M (+8%)\nEurope: $32.1M (+5%)\n"
         "Asia-Pacific: $28.7M (+22%)\nLatin America: $12.4M (+15%)\n\n"
         "Total consolidated revenue reached $118.4M, exceeding analyst "
         "consensus estimates of $112.0M by approximately 5.7%."),

        (LANDSCAPE_W, LANDSCAPE_H, "Quarterly Comparison Chart",
         "This landscape page contains a wide-format comparison chart showing "
         "quarterly trends across all business units from Q1 2024 through Q4 2025. "
         "The visualization spans eight quarters with multi-series bar and line overlays."),

        (PORTRAIT_W, PORTRAIT_H, "Operating Expenses",
         "Research & Development: $18.3M (15.5% of revenue)\n"
         "Sales & Marketing: $22.1M (18.7% of revenue)\n"
         "General & Administrative: $9.8M (8.3% of revenue)\n\n"
         "Total operating expenses were $50.2M, representing a 2.1% decrease "
         "from the prior quarter despite increased headcount in engineering."),

        (PORTRAIT_W, PORTRAIT_H, "Balance Sheet Highlights",
         "Cash and equivalents: $89.3M\nShort-term investments: $45.0M\n"
         "Accounts receivable: $31.2M\nTotal current assets: $178.5M\n\n"
         "Long-term debt decreased to $120.0M following the early repayment "
         "of the 2023 term loan facility in October 2025."),

        (LANDSCAPE_W, LANDSCAPE_H, "Regional Performance Dashboard",
         "This landscape page presents a comprehensive regional dashboard with "
         "heat maps showing market penetration rates across 42 countries. "
         "Top performers include Japan (+34%), Australia (+28%), and South Korea (+25%)."),

        (PORTRAIT_W, PORTRAIT_H, "Risk Factors",
         "Key risks identified for the upcoming fiscal year include:\n"
         "1. Foreign currency exposure in emerging markets\n"
         "2. Regulatory changes in EU data protection frameworks\n"
         "3. Supply chain disruptions affecting hardware deliveries\n"
         "4. Competitive pressure from new market entrants in APAC\n"
         "5. Rising interest rates impacting capital expenditure plans"),

        (PORTRAIT_W, PORTRAIT_H, "Forward-Looking Guidance",
         "For FY2026, management expects:\n"
         "Revenue: $480M - $510M (growth of 10-17%)\n"
         "Adjusted EBITDA margin: 28-30%\n"
         "Capital expenditures: $35M - $40M\n"
         "Free cash flow: $95M - $110M\n\n"
         "These projections assume stable macroeconomic conditions and "
         "successful execution of the product roadmap announced in November 2025."),
    ]

    doc = pymupdf.open()

    for i, (w, h, title, body) in enumerate(pages):
        page = doc.new_page(width=w, height=h)

        # Page number
        page.insert_text(
            pymupdf.Point(w - 60, h - 30),
            f"Page {i + 1}",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Title
        page.insert_text(
            pymupdf.Point(72, 72),
            title,
            fontsize=20,
            fontname="hebo",
            color=(0.1, 0.1, 0.4),
        )

        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(w - 72, 82))
        shape.finish(color=(0.3, 0.3, 0.6), width=1.5)
        shape.commit()

        # Body text in a textbox
        text_rect = pymupdf.Rect(72, 110, w - 72, h - 72)
        page.insert_textbox(
            text_rect,
            body,
            fontsize=12,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify page dimensions
    doc = pymupdf.open(OUTPUT)
    for i, page in enumerate(doc):
        r = page.rect
        print(f'  Page {i+1}: {r.width:.0f}x{r.height:.0f}')
    doc.close()

    # GUI-ready: open in evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
