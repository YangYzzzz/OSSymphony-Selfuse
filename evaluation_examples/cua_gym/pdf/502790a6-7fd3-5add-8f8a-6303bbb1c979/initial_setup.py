"""
Initial Setup: Create an unencrypted 6-page financial report PDF
Task ID: pdf_gf1_012
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCUMENTS = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_gf1_012'
OUTPUT = f'{DOCUMENTS}/confidential_report.pdf'


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
    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = pymupdf.open()

    # ---- Page 1: Title Page ----
    page = doc.new_page(width=612, height=792)  # Letter size
    page.insert_text(pymupdf.Point(72, 120), "CONFIDENTIAL", fontsize=14, fontname="hebo", color=(0.8, 0, 0))
    page.insert_text(pymupdf.Point(72, 200), "Meridian Capital Partners", fontsize=28, fontname="hebo", color=(0, 0.15, 0.4))
    page.insert_text(pymupdf.Point(72, 250), "Annual Financial Report", fontsize=22, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(72, 290), "Fiscal Year 2025", fontsize=16, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 350), "Prepared by: Office of the Chief Financial Officer", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 370), "Date: March 15, 2026", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 390), "Classification: Internal Use Only", fontsize=11, fontname="hebo", color=(0.6, 0, 0))

    # Decorative line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 310), pymupdf.Point(540, 310))
    shape.finish(color=(0, 0.15, 0.4), width=2)
    shape.commit()

    # ---- Page 2: Executive Summary ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "Executive Summary", fontsize=20, fontname="hebo", color=(0, 0.15, 0.4))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 70), pymupdf.Point(540, 70))
    shape.finish(color=(0, 0.15, 0.4), width=1)
    shape.commit()

    summary_text = (
        "Meridian Capital Partners delivered strong financial performance in Fiscal Year 2025, "
        "achieving consolidated revenue of $487.3 million, representing a 12.4% increase over the "
        "prior year. Net income rose to $68.2 million, reflecting improved operational efficiency "
        "and successful execution of our strategic initiatives across all business segments.\n\n"
        "Key highlights for the fiscal year include:\n\n"
        "Revenue Growth: Total revenue increased by $53.8 million year-over-year, driven primarily "
        "by the Asset Management and Advisory Services divisions, which contributed $31.2 million "
        "and $14.6 million in incremental revenue respectively.\n\n"
        "Margin Expansion: Operating margin improved to 18.7% from 16.2% in the prior year, "
        "reflecting cost optimization efforts and increased scale benefits. The EBITDA margin "
        "reached 24.1%, up 210 basis points from FY2024.\n\n"
        "Capital Position: Total assets under management grew to $12.8 billion, a 15.3% increase. "
        "The firm maintained a healthy balance sheet with a debt-to-equity ratio of 0.42 and "
        "cash reserves of $156.4 million.\n\n"
        "Client Acquisition: We onboarded 47 new institutional clients and expanded relationships "
        "with 89 existing clients, resulting in net new assets of $1.7 billion."
    )
    page.insert_textbox(pymupdf.Rect(72, 90, 540, 720), summary_text, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # ---- Page 3: Revenue Breakdown ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "Revenue Breakdown by Segment", fontsize=20, fontname="hebo", color=(0, 0.15, 0.4))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 70), pymupdf.Point(540, 70))
    shape.finish(color=(0, 0.15, 0.4), width=1)
    shape.commit()

    # Table header
    y_start = 100
    headers = ["Business Segment", "FY2025 Revenue", "FY2024 Revenue", "Change (%)"]
    col_x = [72, 220, 340, 460]

    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(col_x[i], y_start), h, fontsize=10, fontname="hebo", color=(1, 1, 1))

    # Table header background
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(70, y_start - 14, 542, y_start + 4))
    shape.finish(fill=(0, 0.15, 0.4), color=(0, 0.15, 0.4))
    shape.commit()
    # Re-draw header text on top
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(col_x[i], y_start), h, fontsize=10, fontname="hebo", color=(1, 1, 1))

    rows = [
        ["Asset Management", "$198,450,000", "$172,300,000", "+15.2%"],
        ["Advisory Services", "$124,800,000", "$110,200,000", "+13.2%"],
        ["Wealth Management", "$87,600,000", "$79,400,000", "+10.3%"],
        ["Trading & Securities", "$52,150,000", "$48,900,000", "+6.6%"],
        ["Research & Analytics", "$24,300,000", "$22,700,000", "+7.0%"],
        ["Total", "$487,300,000", "$433,500,000", "+12.4%"],
    ]

    for r_idx, row in enumerate(rows):
        y = y_start + 24 + r_idx * 20
        fn = "hebo" if row[0] == "Total" else "helv"
        for c_idx, cell in enumerate(row):
            page.insert_text(pymupdf.Point(col_x[c_idx], y), cell, fontsize=9.5, fontname=fn, color=(0, 0, 0))

    # Additional commentary
    commentary = (
        "The Asset Management division continued to be the largest revenue contributor, accounting "
        "for 40.7% of total revenue. Growth was fueled by the launch of three new fund strategies "
        "and favorable market conditions in the second half of the fiscal year.\n\n"
        "Advisory Services saw robust demand for M&A advisory, with 23 completed transactions "
        "valued at over $8.4 billion in aggregate. The pipeline remains strong with 31 mandated "
        "engagements currently in progress.\n\n"
        "Wealth Management benefited from rising assets under advisement, which reached $4.2 billion, "
        "and the successful rollout of the proprietary digital wealth platform to 12,000 clients."
    )
    page.insert_textbox(pymupdf.Rect(72, 290, 540, 650), commentary, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # ---- Page 4: Operating Expenses ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "Operating Expenses Analysis", fontsize=20, fontname="hebo", color=(0, 0.15, 0.4))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 70), pymupdf.Point(540, 70))
    shape.finish(color=(0, 0.15, 0.4), width=1)
    shape.commit()

    expenses_text = (
        "Total operating expenses for FY2025 were $396.2 million, a 10.1% increase from the prior "
        "year's $359.8 million. Despite the absolute increase, operating expenses as a percentage "
        "of revenue declined from 83.0% to 81.3%, demonstrating improved cost efficiency.\n\n"
        "Compensation and Benefits: $241.8 million (61.0% of expenses)\n"
        "The largest expense category, reflecting our commitment to attracting and retaining top "
        "talent. The compensation-to-revenue ratio improved to 49.6% from 51.2%.\n\n"
        "Technology and Infrastructure: $58.3 million (14.7% of expenses)\n"
        "Investments in data analytics platforms, cybersecurity enhancements, and cloud migration "
        "drove a 22% increase in technology spending. These investments are expected to yield "
        "operational savings of $12-15 million annually beginning in FY2027.\n\n"
        "Occupancy and Facilities: $34.7 million (8.8% of expenses)\n"
        "Includes the new Singapore office build-out ($4.2M) and London headquarters renovation "
        "($6.8M). Ongoing lease obligations are being optimized through hybrid work arrangements.\n\n"
        "Professional Services: $28.9 million (7.3% of expenses)\n"
        "Legal, audit, and consulting fees remained largely stable year-over-year.\n\n"
        "Marketing and Business Development: $18.4 million (4.6% of expenses)\n"
        "Increased investment in brand awareness campaigns and client acquisition initiatives.\n\n"
        "Other Operating Expenses: $14.1 million (3.6% of expenses)\n"
        "Includes travel, insurance, and miscellaneous administrative costs."
    )
    page.insert_textbox(pymupdf.Rect(72, 90, 540, 750), expenses_text, fontsize=10, fontname="helv", color=(0, 0, 0))

    # ---- Page 5: Balance Sheet Highlights ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "Balance Sheet Highlights", fontsize=20, fontname="hebo", color=(0, 0.15, 0.4))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 70), pymupdf.Point(540, 70))
    shape.finish(color=(0, 0.15, 0.4), width=1)
    shape.commit()

    balance_text = (
        "As of December 31, 2025, Meridian Capital Partners maintained a robust financial position "
        "with total assets of $2.14 billion and shareholders' equity of $892.6 million.\n\n"
        "Assets:\n"
        "  Cash and Cash Equivalents: $156.4 million\n"
        "  Short-term Investments: $312.8 million\n"
        "  Accounts Receivable: $89.3 million\n"
        "  Investment Securities: $1,024.5 million\n"
        "  Property and Equipment: $187.2 million\n"
        "  Goodwill and Intangibles: $284.6 million\n"
        "  Other Assets: $85.2 million\n"
        "  Total Assets: $2,140.0 million\n\n"
        "Liabilities:\n"
        "  Short-term Borrowings: $124.3 million\n"
        "  Accounts Payable: $45.7 million\n"
        "  Accrued Compensation: $198.4 million\n"
        "  Long-term Debt: $248.9 million\n"
        "  Deferred Revenue: $67.2 million\n"
        "  Other Liabilities: $562.9 million\n"
        "  Total Liabilities: $1,247.4 million\n\n"
        "Equity:\n"
        "  Common Stock: $125.0 million\n"
        "  Retained Earnings: $642.8 million\n"
        "  Other Comprehensive Income: $124.8 million\n"
        "  Total Shareholders' Equity: $892.6 million\n\n"
        "The debt-to-equity ratio stands at 0.42, well within our target range of 0.35-0.55, "
        "providing ample capacity for strategic investments and potential acquisitions."
    )
    page.insert_textbox(pymupdf.Rect(72, 90, 540, 750), balance_text, fontsize=10, fontname="helv", color=(0, 0, 0))

    # ---- Page 6: Outlook & Risk Factors ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "Outlook and Risk Factors", fontsize=20, fontname="hebo", color=(0, 0.15, 0.4))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 70), pymupdf.Point(540, 70))
    shape.finish(color=(0, 0.15, 0.4), width=1)
    shape.commit()

    outlook_text = (
        "Forward Guidance:\n\n"
        "Management projects FY2026 revenue in the range of $530-$555 million, representing "
        "anticipated growth of 9-14%. This outlook is predicated on continued expansion of "
        "assets under management, successful integration of the recently acquired Northbridge "
        "Analytics platform, and a stable macroeconomic environment.\n\n"
        "Key strategic priorities for FY2026 include:\n"
        "1. Expansion of the alternative investments platform with target AUM of $3.5 billion\n"
        "2. Launch of the European institutional client coverage team based in Frankfurt\n"
        "3. Completion of the technology modernization program (Phase II)\n"
        "4. Exploration of strategic acquisitions in the $50-200 million range\n\n"
        "Risk Factors:\n\n"
        "Market Risk: Adverse movements in equity markets, interest rates, or credit spreads "
        "could materially affect AUM-based fee revenues and investment portfolio valuations.\n\n"
        "Regulatory Risk: Evolving financial regulations across jurisdictions may increase "
        "compliance costs and restrict certain business activities.\n\n"
        "Operational Risk: Technology failures, cybersecurity breaches, or key personnel "
        "departures could disrupt business operations and client relationships.\n\n"
        "Competitive Risk: Continued fee compression across the asset management industry "
        "and the growing presence of passive investment strategies may pressure margins.\n\n"
        "Geopolitical Risk: International trade tensions, geopolitical conflicts, and "
        "macroeconomic instability in key markets could impact client sentiment and deal flow."
    )
    page.insert_textbox(pymupdf.Rect(72, 90, 540, 750), outlook_text, fontsize=10, fontname="helv", color=(0, 0, 0))

    # Set metadata
    doc.set_metadata({
        "title": "Meridian Capital Partners - Annual Financial Report FY2025",
        "author": "Office of the Chief Financial Officer",
        "subject": "Annual Financial Report",
        "keywords": "financial, report, annual, FY2025, confidential",
        "creator": "Meridian Capital Partners",
        "producer": "Internal Document System",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify page count
    verify_doc = pymupdf.open(OUTPUT)
    print(f'Page count: {verify_doc.page_count}')
    verify_doc.close()

    # GUI-ready startup - open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
