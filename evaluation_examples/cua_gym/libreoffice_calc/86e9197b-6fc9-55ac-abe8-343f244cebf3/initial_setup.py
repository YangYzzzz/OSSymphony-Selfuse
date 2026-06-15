"""
Initial Setup: Create a multi-page PDF document intended for printing with varying margins.
Task ID: pdf_cr_073
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_073'
OUTPUT = f'{WORKDIR}/Desktop/printable.pdf'


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

    doc = pymupdf.open()

    # --- Constants ---
    W, H = 612, 792  # US Letter in points
    MARGIN = 36  # 0.5 inch in points

    # ===== Page 1: Title page with good margins (all content well within margins) =====
    page1 = doc.new_page(width=W, height=H)
    # Title centered, well within margins
    page1.insert_text(
        pymupdf.Point(W / 2 - 120, 200),
        "Greenfield Analytics",
        fontsize=28,
        fontname="hebo",
        color=(0.1, 0.15, 0.4),
    )
    page1.insert_text(
        pymupdf.Point(W / 2 - 140, 240),
        "Quarterly Performance Report",
        fontsize=18,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page1.insert_text(
        pymupdf.Point(W / 2 - 50, 290),
        "Q1 2026",
        fontsize=16,
        fontname="heit",
        color=(0.4, 0.4, 0.4),
    )
    # Decorative line well inside margins
    shape1 = page1.new_shape()
    shape1.draw_line(pymupdf.Point(100, 310), pymupdf.Point(512, 310))
    shape1.finish(color=(0.2, 0.3, 0.6), width=2)
    shape1.commit()

    page1.insert_text(
        pymupdf.Point(150, 400),
        "Prepared by: Elena Marchetti, VP of Strategy",
        fontsize=12,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page1.insert_text(
        pymupdf.Point(150, 420),
        "Date: March 28, 2026",
        fontsize=12,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page1.insert_text(
        pymupdf.Point(150, 440),
        "Distribution: Internal - Confidential",
        fontsize=12,
        fontname="helv",
        color=(0.6, 0.1, 0.1),
    )

    # ===== Page 2: Revenue table - good margins =====
    page2 = doc.new_page(width=W, height=H)
    page2.insert_text(
        pymupdf.Point(72, 60),
        "Revenue Breakdown by Region",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.15, 0.4),
    )

    # Draw a table with realistic data - well within margins
    regions = [
        ("Region", "Q4 2025", "Q1 2026", "Change"),
        ("North America", "$4,872,300", "$5,213,450", "+7.0%"),
        ("Europe", "$3,145,600", "$3,389,100", "+7.7%"),
        ("Asia Pacific", "$2,567,800", "$2,841,200", "+10.6%"),
        ("Latin America", "$1,234,500", "$1,302,800", "+5.5%"),
        ("Middle East & Africa", "$876,200", "$945,700", "+7.9%"),
        ("Total", "$12,696,400", "$13,692,250", "+7.8%"),
    ]
    y_start = 90
    col_positions = [72, 200, 320, 440]
    for row_idx, row in enumerate(regions):
        y = y_start + row_idx * 28
        fontname = "hebo" if row_idx == 0 or row_idx == len(regions) - 1 else "helv"
        fontsize = 11
        for col_idx, cell in enumerate(row):
            page2.insert_text(
                pymupdf.Point(col_positions[col_idx], y),
                cell,
                fontsize=fontsize,
                fontname=fontname,
                color=(0, 0, 0),
            )
    # Horizontal lines for table
    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, y_start + 5), pymupdf.Point(540, y_start + 5))
    shape2.finish(color=(0, 0, 0), width=1)
    shape2.draw_line(pymupdf.Point(72, y_start + 28 + 5), pymupdf.Point(540, y_start + 28 + 5))
    shape2.finish(color=(0.5, 0.5, 0.5), width=0.5)
    shape2.draw_line(pymupdf.Point(72, y_start + (len(regions) - 1) * 28 - 3), pymupdf.Point(540, y_start + (len(regions) - 1) * 28 - 3))
    shape2.finish(color=(0, 0, 0), width=1)
    shape2.commit()

    # Additional narrative text below table
    narrative_y = y_start + len(regions) * 28 + 40
    rect2 = pymupdf.Rect(72, narrative_y, 540, narrative_y + 200)
    page2.insert_textbox(
        rect2,
        "North America continued to lead revenue growth, driven primarily by enterprise "
        "software licensing renewals and new cloud infrastructure contracts. The Asia Pacific "
        "region showed the strongest quarter-over-quarter improvement at 10.6%, reflecting "
        "successful expansion into the Southeast Asian market following the Singapore office "
        "opening in November 2025. Latin America showed modest but steady growth, with the "
        "Brazil operations stabilizing after the leadership transition in Q3 2025.",
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # ===== Page 3: Content too close to LEFT edge (FAIL) =====
    page3 = doc.new_page(width=W, height=H)
    page3.insert_text(
        pymupdf.Point(10, 60),  # Only 10pt from left edge - FAILS (need >= 36pt)
        "Employee Satisfaction Metrics",
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.15, 0.4),
    )
    metrics = [
        "Overall Satisfaction Index: 82.4 / 100",
        "Work-Life Balance Score: 78.9 / 100",
        "Career Development Rating: 85.1 / 100",
        "Management Effectiveness: 79.3 / 100",
        "Compensation Fairness: 71.6 / 100",
        "Team Collaboration: 88.2 / 100",
        "Innovation Culture: 83.7 / 100",
        "Remote Work Satisfaction: 86.5 / 100",
    ]
    for i, metric in enumerate(metrics):
        page3.insert_text(
            pymupdf.Point(10, 100 + i * 24),  # 10pt from left
            f"  {metric}",
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
        )

    page3.insert_text(
        pymupdf.Point(72, 340),
        "Survey conducted February 2026 | 847 of 923 employees responded (91.8%)",
        fontsize=9,
        fontname="heit",
        color=(0.4, 0.4, 0.4),
    )

    # ===== Page 4: Content too close to BOTTOM edge (FAIL) =====
    page4 = doc.new_page(width=W, height=H)
    page4.insert_text(
        pymupdf.Point(72, 60),
        "Project Pipeline Status",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.15, 0.4),
    )

    projects = [
        ("Project Aurora", "Cloud Migration", "In Progress", "78%", "$2.1M"),
        ("Project Beacon", "CRM Integration", "Planning", "12%", "$890K"),
        ("Project Cascade", "Data Warehouse", "In Progress", "45%", "$1.5M"),
        ("Project Delta", "Mobile App v3", "Testing", "91%", "$1.2M"),
        ("Project Echo", "Security Audit", "Complete", "100%", "$340K"),
        ("Project Forge", "AI Analytics", "In Progress", "33%", "$3.4M"),
        ("Project Gateway", "API Platform", "Planning", "5%", "$780K"),
        ("Project Harbor", "Compliance System", "In Progress", "62%", "$1.8M"),
    ]

    y_start = 90
    headers = ["Project", "Category", "Status", "Progress", "Budget"]
    hx = [72, 190, 320, 420, 500]
    for ci, h in enumerate(headers):
        page4.insert_text(pymupdf.Point(hx[ci], y_start), h, fontsize=10, fontname="hebo", color=(0, 0, 0))

    for pi, proj in enumerate(projects):
        for ci, val in enumerate(proj):
            page4.insert_text(
                pymupdf.Point(hx[ci], y_start + (pi + 1) * 24),
                val, fontsize=10, fontname="helv", color=(0, 0, 0),
            )

    # Add text very close to the bottom
    page4.insert_text(
        pymupdf.Point(72, H - 15),  # Only 15pt from bottom (792 - 15 = 777) - FAILS
        "Confidential - Greenfield Analytics Internal Use Only - Do Not Distribute",
        fontsize=9,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )
    page4.insert_text(
        pymupdf.Point(72, H - 5),  # 5pt from bottom - definitely FAILS
        "Page 4 of 5",
        fontsize=8,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    # ===== Page 5: Good margins - summary page =====
    page5 = doc.new_page(width=W, height=H)
    page5.insert_text(
        pymupdf.Point(72, 72),
        "Executive Summary & Recommendations",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.15, 0.4),
    )

    rect5 = pymupdf.Rect(72, 100, 540, 450)
    page5.insert_textbox(
        rect5,
        "Key Findings:\n\n"
        "1. Revenue grew 7.8% quarter-over-quarter, exceeding the 6.5% target set by the "
        "board in January 2026. Asia Pacific was the standout performer.\n\n"
        "2. Employee satisfaction remains strong at 82.4/100, with particular improvement "
        "in remote work satisfaction following the hybrid policy update.\n\n"
        "3. The project pipeline shows healthy progress with 5 of 8 active projects on "
        "track or ahead of schedule. Project Delta is expected to launch in April.\n\n"
        "Recommendations:\n\n"
        "- Increase investment in APAC sales team by 15% to capitalize on growth momentum\n"
        "- Address compensation fairness concerns (scored lowest at 71.6) through market "
        "adjustment review in Q2\n"
        "- Accelerate Project Beacon timeline to align with CRM vendor contract renewal\n"
        "- Initiate succession planning for three senior roles flagged in HR review\n",
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # Footer well within margins
    page5.insert_text(
        pymupdf.Point(200, 700),
        "End of Report",
        fontsize=14,
        fontname="hebo",
        color=(0.3, 0.3, 0.3),
    )

    # Ensure Desktop directory exists
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open PDF in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
