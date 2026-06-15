"""
Initial Setup: Compare PDF metadata and write differences
Task ID: pdf_mbc_017
Domain: pdf

Creates two PDFs with different metadata in ~/Documents/:
  - report_v1.pdf: Title='Draft Report', Author='John', ModDate='D:20240601'
  - report_v2.pdf: Title='Final Report', Author='John Smith', ModDate='D:20240815'
Both share the same Subject and Keywords.
Opens a file manager to ~/Documents/ for the agent.
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCS = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_mbc_017'

V1_PATH = f'{DOCS}/report_v1.pdf'
V2_PATH = f'{DOCS}/report_v2.pdf'


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


def create_report_pdf(path, title, author, mod_date, subject, keywords):
    """Create a multi-page report PDF with realistic content and specified metadata."""
    doc = pymupdf.open()

    # --- Page 1: Title page ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(150, 200), title, fontsize=28, fontname="hebo", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(200, 260), f"Prepared by: {author}", fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(200, 290), "Acme Corporation", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(200, 320), "Confidential", fontsize=11, fontname="heit", color=(0.5, 0.0, 0.0))

    # --- Page 2: Executive Summary ---
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text(pymupdf.Point(72, 72), "Executive Summary", fontsize=20, fontname="hebo", color=(0, 0, 0.4))
    shape = page2.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(523, 80))
    shape.finish(color=(0, 0, 0.4), width=1.5)
    shape.commit()

    summary_text = (
        "This report provides a comprehensive analysis of the quarterly financial performance "
        "of Acme Corporation for the period ending March 2024. Key findings indicate a 12% "
        "increase in overall revenue compared to the previous quarter, driven primarily by "
        "growth in the SaaS product line. Operating expenses remained stable at $2.3M, "
        "resulting in an improved EBITDA margin of 18.5%. The report also covers regional "
        "performance breakdowns, customer acquisition metrics, and forward-looking guidance "
        "for Q2 2024."
    )
    rect = pymupdf.Rect(72, 100, 523, 400)
    page2.insert_textbox(rect, summary_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 3: Financial Data ---
    page3 = doc.new_page(width=595, height=842)
    page3.insert_text(pymupdf.Point(72, 72), "Financial Highlights", fontsize=20, fontname="hebo", color=(0, 0, 0.4))

    # Draw a simple table
    headers = ["Metric", "Q4 2023", "Q1 2024", "Change"]
    data_rows = [
        ["Total Revenue", "$4.1M", "$4.6M", "+12.2%"],
        ["SaaS Revenue", "$2.8M", "$3.3M", "+17.9%"],
        ["Operating Expenses", "$2.3M", "$2.3M", "0.0%"],
        ["Net Income", "$0.9M", "$1.2M", "+33.3%"],
        ["EBITDA Margin", "15.2%", "18.5%", "+3.3pp"],
        ["Customer Count", "1,245", "1,389", "+11.6%"],
        ["Churn Rate", "3.2%", "2.8%", "-0.4pp"],
    ]

    y_start = 100
    col_widths = [150, 90, 90, 90]
    row_height = 25
    x_start = 72

    # Header row background
    shape3 = page3.new_shape()
    shape3.draw_rect(pymupdf.Rect(x_start, y_start, x_start + sum(col_widths), y_start + row_height))
    shape3.finish(color=(0, 0, 0.4), fill=(0, 0, 0.4), width=0.5)
    shape3.commit()

    # Header text
    x = x_start + 5
    for i, h in enumerate(headers):
        page3.insert_text(pymupdf.Point(x, y_start + 17), h, fontsize=10, fontname="hebo",
                          color=(1, 1, 1))
        x += col_widths[i]

    # Data rows
    for r_idx, row in enumerate(data_rows):
        y = y_start + (r_idx + 1) * row_height
        # Alternating row background
        if r_idx % 2 == 0:
            s = page3.new_shape()
            s.draw_rect(pymupdf.Rect(x_start, y, x_start + sum(col_widths), y + row_height))
            s.finish(fill=(0.93, 0.93, 0.97), width=0)
            s.commit()

        x = x_start + 5
        for c_idx, cell in enumerate(row):
            page3.insert_text(pymupdf.Point(x, y + 17), cell, fontsize=10, fontname="helv",
                              color=(0, 0, 0))
            x += col_widths[c_idx]

    # Grid lines
    shape3b = page3.new_shape()
    for r in range(len(data_rows) + 2):
        y = y_start + r * row_height
        shape3b.draw_line(pymupdf.Point(x_start, y), pymupdf.Point(x_start + sum(col_widths), y))
    x = x_start
    for w in col_widths:
        shape3b.draw_line(pymupdf.Point(x, y_start), pymupdf.Point(x, y_start + (len(data_rows) + 1) * row_height))
        x += w
    shape3b.draw_line(pymupdf.Point(x, y_start), pymupdf.Point(x, y_start + (len(data_rows) + 1) * row_height))
    shape3b.finish(color=(0.5, 0.5, 0.5), width=0.5)
    shape3b.commit()

    # Set metadata
    doc.set_metadata({
        "title": title,
        "author": author,
        "subject": subject,
        "keywords": keywords,
        "creator": "Acme Report Generator",
        "producer": "PyMuPDF",
        "modDate": mod_date,
        "creationDate": "D:20240101",
    })

    doc.save(path)
    doc.close()
    print(f"Created: {path}")


def create_initial():
    os.makedirs(DOCS, exist_ok=True)

    # Shared metadata fields
    subject = "Quarterly Financial Performance"
    keywords = "finance, quarterly, acme, performance"

    # report_v1.pdf
    create_report_pdf(
        V1_PATH,
        title="Draft Report",
        author="John",
        mod_date="D:20240601",
        subject=subject,
        keywords=keywords,
    )

    # report_v2.pdf
    create_report_pdf(
        V2_PATH,
        title="Final Report",
        author="John Smith",
        mod_date="D:20240815",
        subject=subject,
        keywords=keywords,
    )

    # Make sure metadata_diff.txt does NOT exist
    diff_path = f'{DOCS}/metadata_diff.txt'
    if os.path.exists(diff_path):
        os.remove(diff_path)

    # GUI-ready: open file manager to Documents directory
    launch_gui(f'nautilus "{DOCS}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus for ~/Documents with DISPLAY=:0')


create_initial()
