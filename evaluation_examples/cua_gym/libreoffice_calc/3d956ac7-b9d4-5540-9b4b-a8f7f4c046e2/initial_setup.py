"""
Initial Setup: Create a presentation-style PDF with specific metadata fields
Task ID: pdf_mbc_023
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
TASK_ID = 'pdf_mbc_023'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS_DIR}/exported_slides.pdf'


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
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    # Remove creation_info.txt if it somehow exists (must NOT be present initially)
    info_path = f'{DOCUMENTS_DIR}/creation_info.txt'
    if os.path.exists(info_path):
        os.remove(info_path)

    # Create a multi-page presentation PDF
    doc = pymupdf.open()

    # --- Slide 1: Title Slide ---
    page = doc.new_page(width=792, height=612)  # Landscape letter
    # Blue header bar
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, 792, 120))
    shape.finish(fill=(0.17, 0.24, 0.46), color=(0.17, 0.24, 0.46))
    shape.commit()

    page.insert_text(
        pymupdf.Point(80, 80),
        "Q4 2025 Strategic Planning Review",
        fontsize=28,
        fontname="hebo",
        color=(1, 1, 1),
    )
    page.insert_text(
        pymupdf.Point(80, 200),
        "Prepared by: Operations & Strategy Division",
        fontsize=16,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(80, 240),
        "December 15, 2025",
        fontsize=14,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    page.insert_text(
        pymupdf.Point(80, 280),
        "Confidential - Internal Use Only",
        fontsize=12,
        fontname="heit",
        color=(0.6, 0.6, 0.6),
    )

    # --- Slide 2: Revenue Overview ---
    page2 = doc.new_page(width=792, height=612)
    shape2 = page2.new_shape()
    shape2.draw_rect(pymupdf.Rect(0, 0, 792, 60))
    shape2.finish(fill=(0.17, 0.24, 0.46), color=(0.17, 0.24, 0.46))
    shape2.commit()

    page2.insert_text(
        pymupdf.Point(40, 42),
        "Revenue Performance Summary",
        fontsize=22,
        fontname="hebo",
        color=(1, 1, 1),
    )

    # Table-like content
    y_start = 100
    headers = ["Region", "Q3 Actual", "Q4 Target", "Q4 Actual", "Variance"]
    col_x = [60, 200, 340, 480, 620]
    for i, h in enumerate(headers):
        page2.insert_text(pymupdf.Point(col_x[i], y_start), h,
                          fontsize=12, fontname="hebo", color=(0.17, 0.24, 0.46))

    data_rows = [
        ["North America", "$4.2M", "$4.8M", "$5.1M", "+6.3%"],
        ["Europe", "$2.8M", "$3.1M", "$2.9M", "-6.5%"],
        ["Asia Pacific", "$1.9M", "$2.3M", "$2.5M", "+8.7%"],
        ["Latin America", "$0.8M", "$1.0M", "$1.1M", "+10.0%"],
        ["Middle East", "$0.5M", "$0.6M", "$0.7M", "+16.7%"],
    ]

    for r, row in enumerate(data_rows):
        y = y_start + 30 + r * 28
        for c, val in enumerate(row):
            page2.insert_text(pymupdf.Point(col_x[c], y), val,
                              fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))

    # Summary line
    page2.insert_text(
        pymupdf.Point(60, y_start + 30 + len(data_rows) * 28 + 20),
        "Total Revenue: $12.3M vs Target $11.8M (+4.2% above plan)",
        fontsize=12,
        fontname="hebo",
        color=(0.0, 0.4, 0.0),
    )

    # --- Slide 3: Key Initiatives ---
    page3 = doc.new_page(width=792, height=612)
    shape3 = page3.new_shape()
    shape3.draw_rect(pymupdf.Rect(0, 0, 792, 60))
    shape3.finish(fill=(0.17, 0.24, 0.46), color=(0.17, 0.24, 0.46))
    shape3.commit()

    page3.insert_text(
        pymupdf.Point(40, 42),
        "Key Strategic Initiatives for 2026",
        fontsize=22,
        fontname="hebo",
        color=(1, 1, 1),
    )

    initiatives = [
        "1. Cloud Migration Program - Phase 2 rollout targeting 85% workload migration by Q2",
        "2. Customer Experience Transformation - Deploy AI-powered support across all channels",
        "3. Market Expansion - Establish regional offices in Singapore and Dubai",
        "4. Product Innovation Lab - Launch dedicated R&D center in Austin, TX",
        "5. Sustainability Goals - Achieve carbon-neutral operations by end of 2026",
        "6. Workforce Development - Upskill 500+ employees through digital literacy program",
    ]

    for i, item in enumerate(initiatives):
        page3.insert_text(
            pymupdf.Point(60, 100 + i * 40),
            item,
            fontsize=13,
            fontname="helv",
            color=(0.2, 0.2, 0.2),
        )

    page3.insert_text(
        pymupdf.Point(60, 100 + len(initiatives) * 40 + 30),
        "Budget allocation: $28.5M across all initiatives",
        fontsize=12,
        fontname="heit",
        color=(0.4, 0.4, 0.4),
    )

    # --- Slide 4: Next Steps ---
    page4 = doc.new_page(width=792, height=612)
    shape4 = page4.new_shape()
    shape4.draw_rect(pymupdf.Rect(0, 0, 792, 60))
    shape4.finish(fill=(0.17, 0.24, 0.46), color=(0.17, 0.24, 0.46))
    shape4.commit()

    page4.insert_text(
        pymupdf.Point(40, 42),
        "Next Steps & Action Items",
        fontsize=22,
        fontname="hebo",
        color=(1, 1, 1),
    )

    next_steps = [
        "Finalize 2026 budget allocations by January 10, 2026",
        "Schedule department head reviews for Q1 planning (Jan 15-20)",
        "Submit revised market expansion proposals to the board",
        "Kick off Cloud Migration Phase 2 with vendor selection",
        "Distribute employee survey results and action plans",
    ]

    for i, step in enumerate(next_steps):
        # Bullet point style
        page4.insert_text(
            pymupdf.Point(80, 110 + i * 36),
            f"\u2022  {step}",
            fontsize=13,
            fontname="helv",
            color=(0.2, 0.2, 0.2),
        )

    page4.insert_text(
        pymupdf.Point(80, 400),
        "Contact: strategy@globalcorp.com",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.7),
    )

    # Set metadata: Producer = LibreOffice 7.6, Creator = Impress
    doc.set_metadata({
        "title": "Q4 2025 Strategic Planning Review",
        "author": "Operations & Strategy Division",
        "subject": "Quarterly Strategic Review",
        "keywords": "strategy, planning, Q4, 2025, review",
        "creator": "Impress",
        "producer": "LibreOffice 7.6",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify metadata was set
    verify_doc = pymupdf.open(OUTPUT)
    meta = verify_doc.metadata
    print(f'  Producer: {meta.get("producer", "")}')
    print(f'  Creator: {meta.get("creator", "")}')
    print(f'  Pages: {verify_doc.page_count}')
    verify_doc.close()

    # Open in Evince for GUI readiness
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
