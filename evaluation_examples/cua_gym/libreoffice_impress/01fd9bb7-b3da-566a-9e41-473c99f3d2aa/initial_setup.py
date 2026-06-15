"""
Initial Setup: Create strategic_plan.pdf with SWOT analysis on page 4
Task ID: pdf_cross_066
Domain: libreoffice_impress (pdf cross-domain)
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user/Documents'
OUTPUT_PDF = f'{WORKDIR}/strategic_plan.pdf'


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
    # Ensure Documents directory exists
    os.makedirs(WORKDIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: Title / Executive Summary ---
    page1 = doc.new_page(width=612, height=792)
    shape1 = page1.new_shape()

    # Header bar
    header_rect = pymupdf.Rect(0, 0, 612, 80)
    shape1.draw_rect(header_rect)
    shape1.finish(color=(0.1, 0.2, 0.5), fill=(0.1, 0.2, 0.5), width=0)
    shape1.commit()

    page1.insert_text(
        pymupdf.Point(72, 50),
        "ACME CORPORATION",
        fontsize=22,
        fontname="hebo",
        color=(1, 1, 1),
    )
    page1.insert_text(
        pymupdf.Point(72, 120),
        "Strategic Plan 2025–2028",
        fontsize=28,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )
    page1.insert_text(
        pymupdf.Point(72, 165),
        "Prepared by the Office of Corporate Strategy",
        fontsize=13,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page1.insert_text(
        pymupdf.Point(72, 190),
        "Confidential — March 2025",
        fontsize=11,
        fontname="tiit",
        color=(0.5, 0.5, 0.5),
    )

    # Divider
    shape1b = page1.new_shape()
    shape1b.draw_line(pymupdf.Point(72, 210), pymupdf.Point(540, 210))
    shape1b.finish(color=(0.1, 0.2, 0.5), width=2)
    shape1b.commit()

    exec_summary = (
        "Executive Summary\n\n"
        "This strategic plan outlines ACME Corporation's vision, mission, and objectives for the "
        "next three years. It is designed to guide decision-making and resource allocation across "
        "all business units. The plan incorporates market intelligence, competitive benchmarking, "
        "and internal capability assessments to chart a course for sustainable growth.\n\n"
        "Key focus areas include digital transformation, market expansion into emerging economies, "
        "workforce development, and responsible environmental stewardship. The plan concludes with "
        "a comprehensive SWOT analysis on page 4 that informs the strategic priorities described "
        "throughout this document."
    )
    page1.insert_textbox(
        pymupdf.Rect(72, 230, 540, 600),
        exec_summary,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    page1.insert_text(pymupdf.Point(72, 750), "Page 1", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 2: Mission, Vision & Values ---
    page2 = doc.new_page(width=612, height=792)
    shape2 = page2.new_shape()
    shape2.draw_rect(pymupdf.Rect(0, 0, 612, 80))
    shape2.finish(color=(0.1, 0.2, 0.5), fill=(0.1, 0.2, 0.5), width=0)
    shape2.commit()

    page2.insert_text(
        pymupdf.Point(72, 50),
        "ACME CORPORATION — Strategic Plan 2025–2028",
        fontsize=14,
        fontname="hebo",
        color=(1, 1, 1),
    )
    page2.insert_text(
        pymupdf.Point(72, 110),
        "Section 1: Mission, Vision & Core Values",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    page2.insert_textbox(
        pymupdf.Rect(72, 145, 540, 720),
        (
            "Our Mission\n\n"
            "To deliver innovative, high-quality products and services that create measurable value "
            "for our customers, employees, and communities while building a resilient, future-ready "
            "organization.\n\n"
            "Our Vision\n\n"
            "To be the leading provider of integrated solutions in our industry, recognized globally "
            "for excellence, integrity, and sustainable impact by 2028.\n\n"
            "Core Values\n\n"
            "1. Customer Obsession — We place the customer at the center of every decision.\n"
            "2. Integrity — We operate with transparency and accountability at all times.\n"
            "3. Innovation — We invest continuously in new ideas and technologies.\n"
            "4. Collaboration — We achieve more together than as individuals.\n"
            "5. Sustainability — We are stewards of the environment and community.\n\n"
            "Strategic Objectives\n\n"
            "Over the planning horizon, ACME aims to: (a) grow revenue by 20% year-on-year, "
            "(b) reduce operational costs by 15% through process automation, (c) expand into "
            "three new international markets, and (d) achieve carbon neutrality by 2027."
        ),
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    page2.insert_text(pymupdf.Point(72, 750), "Page 2", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 3: Market Analysis ---
    page3 = doc.new_page(width=612, height=792)
    shape3 = page3.new_shape()
    shape3.draw_rect(pymupdf.Rect(0, 0, 612, 80))
    shape3.finish(color=(0.1, 0.2, 0.5), fill=(0.1, 0.2, 0.5), width=0)
    shape3.commit()

    page3.insert_text(
        pymupdf.Point(72, 50),
        "ACME CORPORATION — Strategic Plan 2025–2028",
        fontsize=14,
        fontname="hebo",
        color=(1, 1, 1),
    )
    page3.insert_text(
        pymupdf.Point(72, 110),
        "Section 2: Market Analysis & Competitive Landscape",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    page3.insert_textbox(
        pymupdf.Rect(72, 145, 540, 720),
        (
            "Global Market Overview\n\n"
            "The global market for integrated enterprise solutions is projected to reach USD 1.2 "
            "trillion by 2027, representing a CAGR of 8.4%. Key growth drivers include the rapid "
            "adoption of cloud-based technologies, growing demand for automation, and accelerating "
            "digital transformation initiatives across industries.\n\n"
            "Competitive Landscape\n\n"
            "ACME operates in a highly competitive market with several established players and a "
            "growing number of agile start-ups. Our primary competitors have significant advantages "
            "in brand recognition and distribution networks. However, ACME differentiates itself "
            "through superior customer service, proprietary IP, and a highly skilled workforce.\n\n"
            "Customer Segmentation\n\n"
            "Enterprise Clients (>500 employees): 62% of revenue. These clients require deep "
            "integration, long-term support contracts, and compliance capabilities.\n\n"
            "Mid-Market Clients (50–500 employees): 28% of revenue. This segment shows the fastest "
            "growth and highest satisfaction scores.\n\n"
            "SMBs (<50 employees): 10% of revenue. A high-volume, lower-margin segment served "
            "primarily through self-service digital channels.\n\n"
            "Continued on next page..."
        ),
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    page3.insert_text(pymupdf.Point(72, 750), "Page 3", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 4: SWOT Analysis ---
    page4 = doc.new_page(width=612, height=792)
    shape4 = page4.new_shape()
    shape4.draw_rect(pymupdf.Rect(0, 0, 612, 80))
    shape4.finish(color=(0.1, 0.2, 0.5), fill=(0.1, 0.2, 0.5), width=0)
    shape4.commit()

    page4.insert_text(
        pymupdf.Point(72, 50),
        "ACME CORPORATION — Strategic Plan 2025–2028",
        fontsize=14,
        fontname="hebo",
        color=(1, 1, 1),
    )
    page4.insert_text(
        pymupdf.Point(72, 110),
        "Section 3: SWOT Analysis",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )
    page4.insert_textbox(
        pymupdf.Rect(72, 140, 540, 165),
        "The following SWOT analysis provides a structured evaluation of ACME's current position:",
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
    )

    # Draw 4 SWOT quadrants
    quad_colors = {
        "strengths":     (0.0, 0.627, 0.235),   # green
        "weaknesses":    (0.20, 0.40, 0.70),     # blue
        "opportunities": (0.87, 0.45, 0.14),     # orange
        "threats":       (0.80, 0.10, 0.10),     # red
    }

    # Layout: 2x2 grid, starting y=175, each box ~255 wide x 270 tall
    boxes = {
        "strengths":     pymupdf.Rect(50,  175, 305, 445),
        "weaknesses":    pymupdf.Rect(307, 175, 562, 445),
        "opportunities": pymupdf.Rect(50,  447, 305, 717),
        "threats":       pymupdf.Rect(307, 447, 562, 717),
    }

    swot_data = {
        "strengths": {
            "title": "STRENGTHS",
            "items": [
                "Strong brand recognition",
                "Loyal customer base",
                "Skilled and experienced workforce",
            ],
        },
        "weaknesses": {
            "title": "WEAKNESSES",
            "items": [
                "Limited online presence",
                "High operational costs",
                "Aging infrastructure",
            ],
        },
        "opportunities": {
            "title": "OPPORTUNITIES",
            "items": [
                "Emerging markets expansion",
                "Digital transformation initiatives",
                "Strategic partnerships",
                "Sustainability trends",
            ],
        },
        "threats": {
            "title": "THREATS",
            "items": [
                "New market competitors",
                "Regulatory changes",
                "Economic uncertainty",
            ],
        },
    }

    for key, rect in boxes.items():
        color = quad_colors[key]
        # Draw header background
        header_r = pymupdf.Rect(rect.x0, rect.y0, rect.x1, rect.y0 + 30)
        sh = page4.new_shape()
        sh.draw_rect(header_r)
        sh.finish(color=color, fill=color, width=0)
        # Draw box border
        sh.draw_rect(rect)
        sh.finish(color=color, fill=None, width=1.5)
        sh.commit()

        # Header text
        page4.insert_text(
            pymupdf.Point(rect.x0 + 6, rect.y0 + 21),
            swot_data[key]["title"],
            fontsize=11,
            fontname="hebo",
            color=(1, 1, 1),
        )

        # Bullet items
        y_pos = rect.y0 + 48
        for item in swot_data[key]["items"]:
            page4.insert_text(
                pymupdf.Point(rect.x0 + 10, y_pos),
                f"• {item}",
                fontsize=10,
                fontname="helv",
                color=(0, 0, 0),
            )
            y_pos += 20

    page4.insert_text(pymupdf.Point(72, 750), "Page 4", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT_PDF)
    doc.close()
    print(f"Initial file created: {OUTPUT_PDF}")

    # GUI-ready startup: open PDF at page 4 (0-indexed = 3)
    launch_gui(f'evince --page-index=3 "{OUTPUT_PDF}"', delay_sec=2.0)
    print("GUI_READY: launched evince with DISPLAY=:0 at page 4")


create_initial()
