"""
Initial Setup: Create a quarterly report PDF with metadata for metadata extraction task
Task ID: pdf_mbc_001
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_001'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS_DIR}/quarterly_report.pdf'


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

    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    # Create a realistic multi-page quarterly financial report PDF
    doc = pymupdf.open()

    # --- Page 1: Cover Page ---
    page = doc.new_page(width=595, height=842)  # A4
    # Company logo area (blue rectangle header)
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, 595, 120))
    shape.finish(fill=(0.0, 0.2, 0.5))
    shape.commit()

    page.insert_text(
        pymupdf.Point(72, 80),
        "Meridian Analytics Corp.",
        fontsize=28,
        fontname="hebo",
        color=(1, 1, 1),
    )

    page.insert_text(
        pymupdf.Point(150, 300),
        "Q3 2024 Financial Report",
        fontsize=32,
        fontname="hebo",
        color=(0.0, 0.15, 0.4),
    )

    page.insert_text(
        pymupdf.Point(180, 370),
        "July - September 2024",
        fontsize=18,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    page.insert_text(
        pymupdf.Point(160, 450),
        "Prepared by: Finance Department",
        fontsize=14,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )

    page.insert_text(
        pymupdf.Point(160, 480),
        "Classification: Internal Use Only",
        fontsize=12,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )

    page.insert_text(
        pymupdf.Point(200, 700),
        "September 15, 2024",
        fontsize=14,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # --- Page 2: Executive Summary ---
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text(
        pymupdf.Point(72, 60),
        "Executive Summary",
        fontsize=22,
        fontname="hebo",
        color=(0.0, 0.2, 0.5),
    )

    # Horizontal rule
    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 70), pymupdf.Point(523, 70))
    shape2.finish(color=(0.0, 0.2, 0.5), width=1.5)
    shape2.commit()

    summary_text = (
        "Meridian Analytics Corp. delivered strong financial performance in Q3 2024, "
        "driven by continued growth in our enterprise SaaS segment and successful "
        "expansion into the Asia-Pacific market. Total revenue reached $48.7M, "
        "representing a 23% year-over-year increase. Operating margins improved to "
        "18.4%, up from 15.2% in the prior quarter, reflecting our ongoing cost "
        "optimization initiatives and economies of scale.\n\n"
        "Key highlights for the quarter include:\n"
        "  - Enterprise client base grew by 34 new accounts\n"
        "  - Annual recurring revenue (ARR) surpassed $180M\n"
        "  - Customer retention rate maintained at 96.8%\n"
        "  - Successfully launched DataInsight Pro v3.2\n"
        "  - Opened regional offices in Singapore and Tokyo\n\n"
        "Looking ahead to Q4, management expects continued momentum with projected "
        "revenue of $52-54M, supported by a robust pipeline of enterprise deals and "
        "seasonal strength in the government sector."
    )

    page2.insert_textbox(
        pymupdf.Rect(72, 90, 523, 500),
        summary_text,
        fontsize=11,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 3: Revenue Breakdown ---
    page3 = doc.new_page(width=595, height=842)
    page3.insert_text(
        pymupdf.Point(72, 60),
        "Revenue Breakdown",
        fontsize=22,
        fontname="hebo",
        color=(0.0, 0.2, 0.5),
    )

    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, 70), pymupdf.Point(523, 70))
    shape3.finish(color=(0.0, 0.2, 0.5), width=1.5)
    shape3.commit()

    # Revenue table header
    table_top = 100
    col_x = [72, 200, 310, 420]
    headers = ["Segment", "Revenue ($M)", "Growth (%)", "Margin (%)"]

    # Header background
    shape3b = page3.new_shape()
    shape3b.draw_rect(pymupdf.Rect(72, table_top - 5, 523, table_top + 18))
    shape3b.finish(fill=(0.0, 0.2, 0.5))
    shape3b.commit()

    for i, h in enumerate(headers):
        page3.insert_text(
            pymupdf.Point(col_x[i] + 5, table_top + 12),
            h,
            fontsize=10,
            fontname="hebo",
            color=(1, 1, 1),
        )

    # Table data
    rows = [
        ["Enterprise SaaS", "28.4", "31.2", "24.5"],
        ["SMB Solutions", "11.2", "12.8", "15.3"],
        ["Professional Services", "5.8", "8.4", "11.7"],
        ["Data Analytics Platform", "2.1", "45.6", "8.2"],
        ["Training & Certification", "1.2", "18.9", "42.1"],
    ]

    for r_idx, row in enumerate(rows):
        y = table_top + 35 + r_idx * 22
        # Alternating row background
        if r_idx % 2 == 0:
            shape_row = page3.new_shape()
            shape_row.draw_rect(pymupdf.Rect(72, y - 5, 523, y + 17))
            shape_row.finish(fill=(0.93, 0.95, 0.98))
            shape_row.commit()
        for c_idx, val in enumerate(row):
            page3.insert_text(
                pymupdf.Point(col_x[c_idx] + 5, y + 10),
                val,
                fontsize=10,
                fontname="helv",
                color=(0.1, 0.1, 0.1),
            )

    # Total row
    total_y = table_top + 35 + len(rows) * 22
    shape_total = page3.new_shape()
    shape_total.draw_line(pymupdf.Point(72, total_y - 5), pymupdf.Point(523, total_y - 5))
    shape_total.finish(color=(0, 0, 0), width=0.8)
    shape_total.commit()

    page3.insert_text(
        pymupdf.Point(77, total_y + 10),
        "Total",
        fontsize=10,
        fontname="hebo",
        color=(0.1, 0.1, 0.1),
    )
    page3.insert_text(
        pymupdf.Point(205, total_y + 10),
        "48.7",
        fontsize=10,
        fontname="hebo",
        color=(0.1, 0.1, 0.1),
    )
    page3.insert_text(
        pymupdf.Point(315, total_y + 10),
        "23.0",
        fontsize=10,
        fontname="hebo",
        color=(0.1, 0.1, 0.1),
    )

    # --- Page 4: Operational Metrics ---
    page4 = doc.new_page(width=595, height=842)
    page4.insert_text(
        pymupdf.Point(72, 60),
        "Operational Metrics",
        fontsize=22,
        fontname="hebo",
        color=(0.0, 0.2, 0.5),
    )

    shape4 = page4.new_shape()
    shape4.draw_line(pymupdf.Point(72, 70), pymupdf.Point(523, 70))
    shape4.finish(color=(0.0, 0.2, 0.5), width=1.5)
    shape4.commit()

    metrics_text = (
        "Employee Headcount: 847 (up from 792 in Q2)\n"
        "New Hires: 68 across engineering, sales, and support\n"
        "Voluntary Turnover Rate: 4.2%\n\n"
        "Customer Metrics:\n"
        "  Active Enterprise Clients: 412\n"
        "  New Enterprise Clients: 34\n"
        "  Average Contract Value: $436,900\n"
        "  Net Promoter Score: 72\n"
        "  Customer Support Resolution Time: 4.2 hours (avg)\n\n"
        "Product Metrics:\n"
        "  Platform Uptime: 99.97%\n"
        "  API Response Time (p99): 145ms\n"
        "  Monthly Active Users: 128,400\n"
        "  Feature Adoption Rate (v3.2): 67%\n\n"
        "Infrastructure:\n"
        "  Cloud Spend: $3.8M (within budget)\n"
        "  Data Processed: 42.7 PB\n"
        "  Security Incidents: 0 (critical), 2 (minor)\n"
    )

    page4.insert_textbox(
        pymupdf.Rect(72, 90, 523, 600),
        metrics_text,
        fontsize=11,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
    )

    # --- Set Metadata ---
    doc.set_metadata({
        "title": "Q3 2024 Financial Report",
        "author": "Sarah Chen",
        "subject": "Quarterly Financial Performance",
        "keywords": "Q3 2024, financial report, Meridian Analytics",
        "creator": "Meridian Analytics Finance Dept",
        "producer": "Internal Document System",
        "creationDate": "D:20240915083000",
        "modDate": "D:20240915083000",
    })

    # --- Table of Contents ---
    toc = [
        [1, "Executive Summary", 2],
        [1, "Revenue Breakdown", 3],
        [1, "Operational Metrics", 4],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify metadata was written
    doc_check = pymupdf.open(OUTPUT)
    meta = doc_check.metadata
    print(f'Metadata check - Title: {meta.get("title")}')
    print(f'Metadata check - Author: {meta.get("author")}')
    print(f'Metadata check - CreationDate: {meta.get("creationDate")}')
    doc_check.close()

    # Make sure report_metadata.txt does NOT exist (agent must create it)
    metadata_txt = f'{DOCUMENTS_DIR}/report_metadata.txt'
    if os.path.exists(metadata_txt):
        os.remove(metadata_txt)
        print(f'Removed pre-existing {metadata_txt}')

    # GUI-ready startup: open PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
