"""
Initial Setup: Create a PDF with metadata for metadata extraction task
Task ID: pdf_gf1_028
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
DOCUMENTS = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_gf1_028'
OUTPUT = f'{DOCUMENTS}/unknown_document.pdf'


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

    # Remove any pre-existing metadata_report.txt (must NOT exist in initial state)
    report_path = f'{DOCUMENTS}/metadata_report.txt'
    if os.path.exists(report_path):
        os.remove(report_path)

    doc = pymupdf.open()

    # --- Page 1: Title Page ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(
        pymupdf.Point(150, 250),
        "Q3 Financial Summary",
        fontsize=28,
        fontname="hebo",
        color=(0.0, 0.13, 0.4),
    )
    page.insert_text(
        pymupdf.Point(180, 310),
        "Fiscal Year 2025",
        fontsize=18,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(170, 370),
        "Prepared by: Finance Team",
        fontsize=14,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    page.insert_text(
        pymupdf.Point(200, 410),
        "September 30, 2025",
        fontsize=12,
        fontname="tiit",
        color=(0.5, 0.5, 0.5),
    )

    # --- Page 2: Executive Summary ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Executive Summary", fontsize=20, fontname="hebo", color=(0, 0.13, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0.13, 0.4), width=1.5)
    shape.commit()
    summary_text = (
        "The third quarter of fiscal year 2025 demonstrated strong performance across all major "
        "business segments. Total revenue reached $142.8 million, representing a 12.3% increase "
        "year-over-year. Operating margins improved to 23.7%, driven by operational efficiencies "
        "and favorable product mix. Net income for the quarter was $33.9 million, exceeding "
        "analyst consensus estimates by approximately 4.2%. Cash flow from operations remained "
        "robust at $48.6 million, supporting continued investment in R&D and strategic acquisitions."
    )
    page.insert_textbox(
        pymupdf.Rect(72, 100, 540, 350),
        summary_text,
        fontsize=11,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 3: Revenue Breakdown ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Revenue Breakdown by Segment", fontsize=18, fontname="hebo", color=(0, 0.13, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0.13, 0.4), width=1.5)
    shape.commit()

    # Table header
    y = 110
    headers = ["Segment", "Q3 2025 ($M)", "Q3 2024 ($M)", "YoY Change"]
    x_positions = [72, 200, 340, 460]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(x_positions[i], y), h, fontsize=10, fontname="hebo", color=(1, 1, 1))
    # Header background
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(68, y - 14, 544, y + 4))
    shape.finish(fill=(0, 0.13, 0.4), color=(0, 0.13, 0.4))
    shape.commit()
    # Re-draw header text on top
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(x_positions[i], y), h, fontsize=10, fontname="hebo", color=(1, 1, 1))

    rows = [
        ["Enterprise Software", "58.4", "51.2", "+14.1%"],
        ["Cloud Services", "42.1", "36.8", "+14.4%"],
        ["Professional Services", "24.7", "22.9", "+7.9%"],
        ["Hardware Solutions", "12.3", "11.8", "+4.2%"],
        ["Licensing & Support", "5.3", "4.5", "+17.8%"],
        ["Total", "142.8", "127.2", "+12.3%"],
    ]
    for idx, row in enumerate(rows):
        y += 22
        for i, val in enumerate(row):
            fn = "hebo" if idx == len(rows) - 1 else "helv"
            page.insert_text(pymupdf.Point(x_positions[i], y), val, fontsize=10, fontname=fn, color=(0.1, 0.1, 0.1))

    # --- Page 4: Operating Expenses ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Operating Expenses", fontsize=18, fontname="hebo", color=(0, 0.13, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0.13, 0.4), width=1.5)
    shape.commit()
    expenses_text = (
        "Total operating expenses for Q3 2025 were $108.9 million, compared to $100.3 million "
        "in Q3 2024. The increase was primarily driven by strategic investments in research and "
        "development ($38.2 million, up 15.1% YoY) and increased headcount in cloud engineering. "
        "Sales and marketing expenses were $31.6 million (22.1% of revenue), while general and "
        "administrative costs remained well-controlled at $14.8 million (10.4% of revenue). "
        "Cost of revenue was $24.3 million, reflecting improved gross margins of 83.0%."
    )
    page.insert_textbox(
        pymupdf.Rect(72, 100, 540, 350),
        expenses_text,
        fontsize=11,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 5: Balance Sheet Highlights ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Balance Sheet Highlights", fontsize=18, fontname="hebo", color=(0, 0.13, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0.13, 0.4), width=1.5)
    shape.commit()
    bs_text = (
        "Total assets as of September 30, 2025 were $892.4 million, up from $781.6 million "
        "at the end of Q2. Cash and cash equivalents totaled $214.3 million. Total current "
        "liabilities were $156.7 million, resulting in a current ratio of 2.8x. Long-term "
        "debt remained at $180.0 million following the refinancing completed in Q1. "
        "Stockholders' equity increased to $498.2 million, driven by retained earnings growth."
    )
    page.insert_textbox(
        pymupdf.Rect(72, 100, 540, 350),
        bs_text,
        fontsize=11,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 6: Cash Flow Statement ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Cash Flow Statement", fontsize=18, fontname="hebo", color=(0, 0.13, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0.13, 0.4), width=1.5)
    shape.commit()
    cf_text = (
        "Cash flow from operating activities was $48.6 million for Q3 2025, compared to "
        "$41.3 million in the prior year period. Capital expenditures totaled $8.9 million, "
        "primarily for data center expansion and office improvements. Free cash flow was "
        "$39.7 million (27.8% of revenue). During the quarter, the company repurchased "
        "$15.0 million of common stock under the existing $100 million share repurchase program. "
        "Dividends paid to shareholders totaled $6.2 million ($0.12 per share)."
    )
    page.insert_textbox(
        pymupdf.Rect(72, 100, 540, 350),
        cf_text,
        fontsize=11,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 7: Key Metrics and KPIs ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Key Performance Indicators", fontsize=18, fontname="hebo", color=(0, 0.13, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0.13, 0.4), width=1.5)
    shape.commit()

    kpis = [
        ("Revenue Growth (YoY)", "12.3%"),
        ("Gross Margin", "83.0%"),
        ("Operating Margin", "23.7%"),
        ("Net Income Margin", "23.7%"),
        ("Customer Retention Rate", "94.6%"),
        ("Annual Recurring Revenue (ARR)", "$487.2M"),
        ("Net Promoter Score (NPS)", "72"),
        ("Employee Headcount", "3,847"),
        ("R&D as % of Revenue", "26.8%"),
    ]
    y = 110
    for label, value in kpis:
        page.insert_text(pymupdf.Point(72, y), label, fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))
        page.insert_text(pymupdf.Point(400, y), value, fontsize=11, fontname="hebo", color=(0, 0.13, 0.4))
        y += 24

    # --- Page 8: Outlook and Guidance ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Q4 2025 Outlook and Guidance", fontsize=18, fontname="hebo", color=(0, 0.13, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0.13, 0.4), width=1.5)
    shape.commit()
    outlook_text = (
        "For the fourth quarter of fiscal year 2025, management expects revenue in the range "
        "of $148 million to $153 million, representing year-over-year growth of 10% to 14%. "
        "Operating margin is expected to be in the range of 22% to 25%. The company reaffirms "
        "its full-year revenue guidance of $555 million to $565 million. Key strategic priorities "
        "for Q4 include the launch of the next-generation cloud platform, expansion into the "
        "Asia-Pacific market, and completion of the DataVault acquisition expected to close "
        "in November 2025."
    )
    page.insert_textbox(
        pymupdf.Rect(72, 100, 540, 350),
        outlook_text,
        fontsize=11,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Set metadata
    doc.set_metadata({
        "title": "Q3 Financial Summary",
        "author": "Finance Team",
        "creator": "Microsoft Word",
        "producer": "Adobe PDF Library",
        "creationDate": "D:20250915083000+00'00'",
        "modDate": "D:20250920141500+00'00'",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify page count
    verify_doc = pymupdf.open(OUTPUT)
    print(f'Page count: {verify_doc.page_count}')
    meta = verify_doc.metadata
    print(f'Metadata - Title: {meta.get("title", "")}')
    print(f'Metadata - Author: {meta.get("author", "")}')
    print(f'Metadata - Creator: {meta.get("creator", "")}')
    print(f'Metadata - Producer: {meta.get("producer", "")}')
    print(f'Metadata - CreationDate: {meta.get("creationDate", "")}')
    print(f'Metadata - ModDate: {meta.get("modDate", "")}')
    verify_doc.close()

    # GUI-ready: open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
