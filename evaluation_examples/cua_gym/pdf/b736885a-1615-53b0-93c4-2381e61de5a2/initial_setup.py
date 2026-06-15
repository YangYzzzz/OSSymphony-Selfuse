"""
Initial Setup: Create a 5-page PDF with visible page numbers in footers.
Task ID: pdf_gf1_015
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_015'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/shuffled_slides.pdf'

# Slide content for each page - distinct topics to make pages distinguishable
SLIDES = [
    {
        "title": "Q3 2025 Revenue Overview",
        "body": (
            "Total revenue for Q3 reached $4.8 million, representing a 12% increase "
            "over the previous quarter. The North American market contributed 62% of "
            "total revenue, followed by EMEA at 24% and APAC at 14%. Subscription-based "
            "revenue grew by 18%, outpacing one-time license sales which declined by 3%."
        ),
        "color": (0.1, 0.2, 0.5),
    },
    {
        "title": "Product Development Milestones",
        "body": (
            "The engineering team shipped 14 features in Q3, including the new "
            "real-time collaboration module and the redesigned analytics dashboard. "
            "Bug resolution time improved from 4.2 days to 2.8 days on average. "
            "The mobile app beta launched with 2,300 early access users enrolled."
        ),
        "color": (0.0, 0.4, 0.3),
    },
    {
        "title": "Customer Acquisition Strategy",
        "body": (
            "New customer acquisition cost dropped to $185 per account, down from "
            "$230 in Q2. The referral program generated 340 qualified leads, converting "
            "at 28%. Enterprise segment deals increased by 5 new contracts worth a "
            "combined annual value of $1.2 million. Churn rate held steady at 4.1%."
        ),
        "color": (0.5, 0.1, 0.1),
    },
    {
        "title": "Infrastructure and Security Updates",
        "body": (
            "Migration to the new cloud provider completed ahead of schedule, reducing "
            "hosting costs by 22%. Average API response time improved from 340ms to "
            "195ms. SOC 2 Type II certification was renewed without findings. Two "
            "critical vulnerabilities were patched within 24 hours of disclosure."
        ),
        "color": (0.3, 0.3, 0.0),
    },
    {
        "title": "Hiring and Team Growth",
        "body": (
            "Headcount grew from 87 to 104 employees during Q3. Engineering added "
            "8 new hires including 3 senior backend engineers. The customer success "
            "team expanded by 4 specialists to support the growing enterprise segment. "
            "Employee satisfaction score remained at 4.3 out of 5.0 in the quarterly pulse survey."
        ),
        "color": (0.2, 0.0, 0.4),
    },
]


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
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()
    page_width, page_height = 612, 792  # Letter size

    for i, slide in enumerate(SLIDES, start=1):
        page = doc.new_page(width=page_width, height=page_height)

        # Draw a colored header band
        header_rect = pymupdf.Rect(0, 0, page_width, 100)
        page.draw_rect(header_rect, color=slide["color"], fill=slide["color"])

        # Title text (white on colored header)
        page.insert_text(
            pymupdf.Point(50, 65),
            slide["title"],
            fontsize=26,
            fontname="hebo",
            color=(1, 1, 1),
        )

        # Body text
        body_rect = pymupdf.Rect(50, 140, page_width - 50, page_height - 120)
        page.insert_textbox(
            body_rect,
            slide["body"],
            fontsize=14,
            fontname="helv",
            color=(0.15, 0.15, 0.15),
            align=0,  # LEFT
        )

        # Footer with visible page number
        footer_text = f"Page {i}"
        page.insert_text(
            pymupdf.Point(page_width / 2 - 20, page_height - 40),
            footer_text,
            fontsize=12,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

        # Thin line above footer
        page.draw_line(
            pymupdf.Point(50, page_height - 60),
            pymupdf.Point(page_width - 50, page_height - 60),
            color=(0.7, 0.7, 0.7),
            width=0.5,
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
