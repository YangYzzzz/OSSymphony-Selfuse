"""
Initial Setup: Create a corrupted PDF report that pikepdf can recover
Task ID: pdf_fm_094
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import struct

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_094'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/damaged_report.pdf'


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

    # First, create a valid PDF with realistic multi-page report content
    import pymupdf

    doc = pymupdf.open()

    # --- Page 1: Title Page ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(
        pymupdf.Point(72, 120),
        "Meridian Analytics Group",
        fontsize=28,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )
    page.insert_text(
        pymupdf.Point(72, 170),
        "Q4 2025 Performance Report",
        fontsize=22,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )
    page.insert_text(
        pymupdf.Point(72, 220),
        "Prepared by: Elena Vasquez, Senior Data Analyst",
        fontsize=12,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(72, 245),
        "Date: December 15, 2025",
        fontsize=12,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(72, 270),
        "Classification: Internal - Confidential",
        fontsize=11,
        fontname="heit",
        color=(0.6, 0.1, 0.1),
    )

    # Decorative line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 290), pymupdf.Point(540, 290))
    shape.finish(color=(0.1, 0.2, 0.5), width=2)
    shape.commit()

    page.insert_textbox(
        pymupdf.Rect(72, 320, 540, 500),
        "This report provides a comprehensive analysis of Meridian Analytics Group's "
        "performance during Q4 2025. Key areas examined include revenue growth across "
        "regional offices, client acquisition metrics, project delivery timelines, and "
        "operational efficiency benchmarks. The data presented herein was compiled from "
        "internal tracking systems, client feedback surveys, and financial statements "
        "audited by Thornton & Associates.",
        fontsize=11,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 2: Revenue Overview ---
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(
        pymupdf.Point(72, 60),
        "1. Revenue Overview",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 68), pymupdf.Point(540, 68))
    shape2.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape2.commit()

    page2.insert_textbox(
        pymupdf.Rect(72, 80, 540, 160),
        "Q4 2025 saw robust revenue performance with total consolidated revenue reaching "
        "$14.8 million, representing a 12.3% increase over Q3 2025 and an 18.7% year-over-year "
        "improvement. The growth was primarily driven by expansion in the Asia-Pacific region "
        "and the successful launch of our predictive analytics service line.",
        fontsize=11,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Revenue table
    table_data = [
        ["Region", "Q3 2025", "Q4 2025", "Change"],
        ["North America", "$5,230,000", "$5,680,000", "+8.6%"],
        ["Europe", "$3,410,000", "$3,720,000", "+9.1%"],
        ["Asia-Pacific", "$2,180,000", "$2,940,000", "+34.9%"],
        ["Latin America", "$1,050,000", "$1,210,000", "+15.2%"],
        ["Middle East & Africa", "$840,000", "$1,250,000", "+48.8%"],
        ["Total", "$12,710,000", "$14,800,000", "+16.4%"],
    ]

    y_start = 180
    row_height = 22
    col_widths = [150, 100, 100, 80]
    x_start = 90

    for row_idx, row in enumerate(table_data):
        y = y_start + row_idx * row_height
        for col_idx, cell in enumerate(row):
            x = x_start + sum(col_widths[:col_idx])
            if row_idx == 0:
                page2.insert_text(pymupdf.Point(x + 5, y + 15), cell, fontsize=10, fontname="hebo", color=(1, 1, 1))
            elif row_idx == len(table_data) - 1:
                page2.insert_text(pymupdf.Point(x + 5, y + 15), cell, fontsize=10, fontname="hebo", color=(0.1, 0.2, 0.5))
            else:
                page2.insert_text(pymupdf.Point(x + 5, y + 15), cell, fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))

    # Draw table borders and header background
    shape3 = page2.new_shape()
    # Header background
    shape3.draw_rect(pymupdf.Rect(x_start, y_start, x_start + sum(col_widths), y_start + row_height))
    shape3.finish(color=(0.1, 0.2, 0.5), fill=(0.1, 0.2, 0.5))
    # Total row background
    total_y = y_start + (len(table_data) - 1) * row_height
    shape3.draw_rect(pymupdf.Rect(x_start, total_y, x_start + sum(col_widths), total_y + row_height))
    shape3.finish(color=(0.85, 0.9, 0.95), fill=(0.85, 0.9, 0.95))
    # Grid lines
    for i in range(len(table_data) + 1):
        y = y_start + i * row_height
        shape3.draw_line(pymupdf.Point(x_start, y), pymupdf.Point(x_start + sum(col_widths), y))
        shape3.finish(color=(0.7, 0.7, 0.7), width=0.5)
    for j in range(len(col_widths) + 1):
        x = x_start + sum(col_widths[:j])
        shape3.draw_line(pymupdf.Point(x, y_start), pymupdf.Point(x, y_start + len(table_data) * row_height))
        shape3.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape3.commit()

    # --- Page 3: Client Metrics ---
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(
        pymupdf.Point(72, 60),
        "2. Client Acquisition & Retention",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    shape4 = page3.new_shape()
    shape4.draw_line(pymupdf.Point(72, 68), pymupdf.Point(540, 68))
    shape4.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape4.commit()

    metrics_text = (
        "New enterprise clients acquired in Q4: 23 (vs. 17 in Q3)\n"
        "Client retention rate: 94.2% (target: 92%)\n"
        "Average contract value: $184,500 (up from $162,000)\n"
        "Net Promoter Score: 72 (industry average: 45)\n\n"
        "Notable new clients include Pinnacle Healthcare Systems, Westbridge Financial Corp., "
        "and Sakura Technologies. The partnership with Pinnacle represents our largest single "
        "engagement to date, valued at $2.3M over 18 months.\n\n"
        "Client churn analysis reveals that 78% of departing clients cited budget constraints "
        "rather than service quality, indicating strong satisfaction among our active portfolio. "
        "The implementation of quarterly business reviews has contributed to a 15% reduction "
        "in voluntary churn compared to the previous year."
    )
    page3.insert_textbox(
        pymupdf.Rect(72, 80, 540, 400),
        metrics_text,
        fontsize=11,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # --- Page 4: Project Delivery ---
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(
        pymupdf.Point(72, 60),
        "3. Project Delivery & Operations",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    shape5 = page4.new_shape()
    shape5.draw_line(pymupdf.Point(72, 68), pymupdf.Point(540, 68))
    shape5.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape5.commit()

    ops_text = (
        "Project delivery performance improved significantly in Q4 2025:\n\n"
        "- On-time delivery rate: 91.4% (Q3: 86.2%)\n"
        "- Average project margin: 38.5% (Q3: 35.1%)\n"
        "- Resource utilization: 82.7% (target: 80%)\n"
        "- Defect rate post-delivery: 2.1% (Q3: 3.8%)\n\n"
        "The introduction of the Agile PMO framework in September has shown measurable "
        "improvements across all delivery metrics. The framework includes standardized sprint "
        "ceremonies, automated progress dashboards, and mandatory peer code reviews.\n\n"
        "Key project highlights:\n"
        "- Westbridge Financial: Real-time fraud detection system deployed 2 weeks ahead of schedule\n"
        "- Pinnacle Healthcare: Patient outcome prediction model achieved 94.3% accuracy\n"
        "- Sakura Technologies: Supply chain optimization reduced logistics costs by 22%\n\n"
        "Staffing: Headcount grew from 187 to 214 employees. The engineering team expanded by "
        "18 new hires, including 5 senior machine learning engineers from top-tier firms."
    )
    page4.insert_textbox(
        pymupdf.Rect(72, 80, 540, 550),
        ops_text,
        fontsize=11,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # --- Page 5: Outlook ---
    page5 = doc.new_page(width=612, height=792)
    page5.insert_text(
        pymupdf.Point(72, 60),
        "4. Outlook & Strategic Priorities",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    shape6 = page5.new_shape()
    shape6.draw_line(pymupdf.Point(72, 68), pymupdf.Point(540, 68))
    shape6.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape6.commit()

    outlook_text = (
        "Looking ahead to Q1 2026, Meridian Analytics Group is well-positioned for continued "
        "growth. The sales pipeline currently contains $8.4M in qualified opportunities, "
        "representing a 40% increase over the same period last year.\n\n"
        "Strategic priorities for the upcoming quarter:\n\n"
        "1. Launch the AI-Powered Insights Platform (APIP) — our flagship SaaS product "
        "targeting mid-market enterprises. Beta testing with 12 pilot clients has yielded "
        "positive results with an average satisfaction score of 4.6/5.0.\n\n"
        "2. Expand the Singapore office to serve as the regional hub for Southeast Asia. "
        "Target headcount: 35 by end of Q2 2026.\n\n"
        "3. Complete SOC 2 Type II certification to unlock government and healthcare "
        "contract eligibility.\n\n"
        "4. Establish a formal partnership program with major cloud providers (AWS, Azure, GCP) "
        "to enhance our go-to-market strategy.\n\n"
        "The board has approved a capital expenditure budget of $3.2M for Q1 2026 to support "
        "these initiatives, with an expected ROI timeline of 12-18 months."
    )
    page5.insert_textbox(
        pymupdf.Rect(72, 80, 540, 600),
        outlook_text,
        fontsize=11,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Set metadata
    doc.set_metadata({
        "title": "Q4 2025 Performance Report",
        "author": "Elena Vasquez",
        "subject": "Quarterly Performance Analysis",
        "keywords": "Q4, 2025, performance, revenue, analytics",
        "creator": "Meridian Analytics Group",
        "producer": "Internal Reports System",
    })

    # Set TOC
    toc = [
        [1, "Revenue Overview", 2],
        [1, "Client Acquisition & Retention", 3],
        [1, "Project Delivery & Operations", 4],
        [1, "Outlook & Strategic Priorities", 5],
    ]
    doc.set_toc(toc)

    # Save a clean version first
    clean_path = f'{DOCUMENTS}/_clean_report.pdf'
    doc.save(clean_path)
    doc.close()

    # Now corrupt the PDF to make it damaged but recoverable by pikepdf
    with open(clean_path, 'rb') as f:
        data = bytearray(f.read())

    file_size = len(data)

    # Strategy: Aggressively corrupt the xref table and trailer so that
    # normal PDF readers (evince, etc.) refuse to open the file.
    # pikepdf (backed by QPDF) can reconstruct xref from object markers.

    # 1. Completely destroy the xref table
    xref_pos = data.rfind(b'xref')
    if xref_pos > 0:
        # Wipe the entire xref section up to trailer
        trailer_pos = data.find(b'trailer', xref_pos)
        if trailer_pos > xref_pos:
            for i in range(xref_pos, trailer_pos):
                data[i] = ord(b'X')
        else:
            # Wipe 200 bytes from xref
            for i in range(xref_pos, min(xref_pos + 200, file_size)):
                data[i] = ord(b'X')

    # 2. Corrupt the trailer dictionary
    trailer_pos = data.rfind(b'trailer')
    if trailer_pos > 0:
        # Damage trailer keyword itself
        data[trailer_pos:trailer_pos + 7] = b'DAMAGED'

    # 3. Corrupt startxref
    startxref_pos = data.rfind(b'startxref')
    if startxref_pos > 0:
        data[startxref_pos:startxref_pos + 9] = b'XXXXXXXXX'

    # 4. Corrupt the %%EOF marker
    eof_pos = data.rfind(b'%%EOF')
    if eof_pos > 0:
        data[eof_pos:eof_pos + 5] = b'XXXXX'

    # 5. Insert some garbage bytes in the middle of a content stream
    # (This further damages the file but QPDF can still find objects)
    mid = file_size // 3
    stream_pos = data.find(b'stream', mid)
    if stream_pos > 0 and stream_pos + 30 < file_size:
        for i in range(stream_pos + 10, min(stream_pos + 25, file_size)):
            data[i] = 0x00

    with open(OUTPUT, 'wb') as f:
        f.write(data)

    # Clean up temp file
    os.remove(clean_path)

    print(f'Corrupted PDF created: {OUTPUT}')

    # Verify it's actually corrupted (pymupdf should have trouble)
    try:
        test_doc = pymupdf.open(OUTPUT)
        print(f'WARNING: pymupdf opened without error, pages={test_doc.page_count}')
        test_doc.close()
    except Exception as e:
        print(f'Good: pymupdf reports error: {e}')

    # Open file manager to show the Documents directory
    launch_gui(f'nautilus "{DOCUMENTS}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus with DISPLAY=:0')


create_initial()
