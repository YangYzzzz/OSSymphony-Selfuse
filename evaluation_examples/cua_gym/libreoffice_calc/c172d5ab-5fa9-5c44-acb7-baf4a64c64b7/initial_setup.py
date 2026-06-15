"""
Initial Setup: Create survey_report.pdf with customer satisfaction data
Task ID: pdf_cross_064
Domain: pdf (cross-domain: source PDF + LibreOffice Impress output)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_064'
OUTPUT = f'{WORKDIR}/survey_report.pdf'


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

    os.makedirs(WORKDIR, exist_ok=True)

    doc = pymupdf.open()

    # ---- Page 1: Cover page / Introduction ----
    page1 = doc.new_page(width=595, height=842)

    # Title
    page1.insert_text(
        pymupdf.Point(297, 120),
        "Customer Satisfaction Survey Report",
        fontsize=22,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
        rotate=0,
    )
    # Subtitle centered
    page1.insert_text(
        pymupdf.Point(297, 160),
        "Q1 2025 — Annual Review",
        fontsize=14,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
        rotate=0,
    )

    # Decorative line
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 185), pymupdf.Point(523, 185))
    shape.finish(color=(0.1, 0.2, 0.5), width=2)
    shape.commit()

    # Introduction paragraph
    intro_rect = pymupdf.Rect(72, 200, 523, 380)
    intro_text = (
        "This report presents the results of our comprehensive customer satisfaction "
        "survey conducted across all service areas during Q1 2025. A total of 500 "
        "customers participated, evaluating five key performance categories. "
        "The findings reflect customer perceptions on product quality, service "
        "delivery, value, and overall experience.\n\n"
        "Survey Period: January 1, 2025 – March 31, 2025\n"
        "Total Respondents: 500\n"
        "Response Rate: 94.3%\n"
        "Methodology: Online survey with 5-point Likert scale"
    )
    page1.insert_textbox(
        intro_rect,
        intro_text,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=0,
    )

    # Summary box header
    shape2 = page1.new_shape()
    shape2.draw_rect(pymupdf.Rect(72, 400, 523, 430))
    shape2.finish(color=(0.1, 0.2, 0.5), fill=(0.1, 0.2, 0.5), width=0)
    shape2.commit()

    page1.insert_text(
        pymupdf.Point(82, 422),
        "Survey Categories Overview",
        fontsize=12,
        fontname="hebo",
        color=(1, 1, 1),
    )

    # Table headers
    page1.insert_text(pymupdf.Point(82, 455), "Category", fontsize=11, fontname="hebo", color=(0.1, 0.2, 0.5))
    page1.insert_text(pymupdf.Point(280, 455), "Satisfied", fontsize=11, fontname="hebo", color=(0.1, 0.2, 0.5))
    page1.insert_text(pymupdf.Point(370, 455), "Total", fontsize=11, fontname="hebo", color=(0.1, 0.2, 0.5))
    page1.insert_text(pymupdf.Point(450, 455), "Score", fontsize=11, fontname="hebo", color=(0.1, 0.2, 0.5))

    shape3 = page1.new_shape()
    shape3.draw_line(pymupdf.Point(72, 462), pymupdf.Point(523, 462))
    shape3.finish(color=(0.5, 0.5, 0.5), width=0.5)
    shape3.commit()

    # Table data rows
    categories = [
        ("Product Quality", "435", "500", "87%"),
        ("Customer Service", "460", "500", "92%"),
        ("Delivery Speed", "390", "500", "78%"),
        ("Value for Money", "415", "500", "83%"),
        ("Overall Experience", "445", "500", "89%"),
    ]

    row_y = 480
    for i, (cat, satisfied, total, score) in enumerate(categories):
        bg_color = (0.95, 0.97, 1.0) if i % 2 == 0 else (1.0, 1.0, 1.0)
        shape_r = page1.new_shape()
        shape_r.draw_rect(pymupdf.Rect(72, row_y - 12, 523, row_y + 8))
        shape_r.finish(color=None, fill=bg_color, width=0)
        shape_r.commit()

        page1.insert_text(pymupdf.Point(82, row_y), cat, fontsize=10, fontname="helv", color=(0, 0, 0))
        page1.insert_text(pymupdf.Point(280, row_y), satisfied, fontsize=10, fontname="helv", color=(0, 0, 0))
        page1.insert_text(pymupdf.Point(370, row_y), total, fontsize=10, fontname="helv", color=(0, 0, 0))
        page1.insert_text(pymupdf.Point(450, row_y), score, fontsize=10, fontname="hebo", color=(0.1, 0.5, 0.2))
        row_y += 26

    # Footer
    page1.insert_text(
        pymupdf.Point(297, 800),
        "Page 1 of 2 — Confidential",
        fontsize=9,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    # ---- Page 2: Detailed Breakdown ----
    page2 = doc.new_page(width=595, height=842)

    page2.insert_text(
        pymupdf.Point(297, 55),
        "Detailed Category Analysis",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )

    shape4 = page2.new_shape()
    shape4.draw_line(pymupdf.Point(72, 72), pymupdf.Point(523, 72))
    shape4.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape4.commit()

    # Detailed data for each category
    details = [
        {
            "name": "Product Quality",
            "score": 87,
            "count": 435,
            "total": 500,
            "desc": (
                "Customers rated product quality highly, with 87% expressing satisfaction. "
                "Key drivers included build quality, reliability, and adherence to specifications. "
                "This represents a 3-point improvement over the previous quarter."
            ),
        },
        {
            "name": "Customer Service",
            "score": 92,
            "count": 460,
            "total": 500,
            "desc": (
                "Customer service achieved the highest satisfaction score at 92%, driven by "
                "fast response times (avg. 2.4 hours) and effective issue resolution rates of 96%. "
                "Staff professionalism was cited as the top positive factor."
            ),
        },
        {
            "name": "Delivery Speed",
            "score": 78,
            "count": 390,
            "total": 500,
            "desc": (
                "Delivery speed scored 78%, the lowest among all categories. "
                "Key concerns included delays during peak periods and last-mile delivery challenges. "
                "Improvement initiatives are scheduled for Q2 2025."
            ),
        },
        {
            "name": "Value for Money",
            "score": 83,
            "count": 415,
            "total": 500,
            "desc": (
                "Value for money was rated at 83%, reflecting positive perception of pricing "
                "relative to product quality. Recent promotional campaigns contributed to a "
                "2-point increase from last quarter."
            ),
        },
        {
            "name": "Overall Experience",
            "score": 89,
            "count": 445,
            "total": 500,
            "desc": (
                "Overall customer experience scored 89%, indicating strong general satisfaction. "
                "The holistic rating reflects the combined effect of all other categories "
                "and places the company in the top quartile for the industry."
            ),
        },
    ]

    y_pos = 100
    for detail in details:
        # Category heading
        page2.insert_text(
            pymupdf.Point(82, y_pos),
            f"{detail['name']}   —   {detail['score']}% ({detail['count']}/{detail['total']})",
            fontsize=12,
            fontname="hebo",
            color=(0.1, 0.2, 0.5),
        )
        y_pos += 18

        # Progress bar background
        bar_bg = page2.new_shape()
        bar_bg.draw_rect(pymupdf.Rect(82, y_pos, 450, y_pos + 12))
        bar_bg.finish(color=(0.7, 0.7, 0.7), fill=(0.85, 0.85, 0.85), width=0.5)
        bar_bg.commit()

        # Progress bar fill
        fill_width = 368 * detail['score'] / 100.0
        bar_fill = page2.new_shape()
        bar_fill.draw_rect(pymupdf.Rect(82, y_pos, 82 + fill_width, y_pos + 12))
        bar_fill.finish(color=None, fill=(0.15, 0.55, 0.3), width=0)
        bar_fill.commit()

        # Percentage label
        page2.insert_text(
            pymupdf.Point(458, y_pos + 10),
            f"{detail['score']}%",
            fontsize=10,
            fontname="hebo",
            color=(0.1, 0.2, 0.5),
        )
        y_pos += 22

        # Description
        desc_rect = pymupdf.Rect(82, y_pos, 523, y_pos + 45)
        page2.insert_textbox(
            desc_rect,
            detail['desc'],
            fontsize=9,
            fontname="helv",
            color=(0.2, 0.2, 0.2),
            align=0,
        )
        y_pos += 60

    # Footer
    page2.insert_text(
        pymupdf.Point(297, 800),
        "Page 2 of 2 — Confidential",
        fontsize=9,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open survey_report.pdf in evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
