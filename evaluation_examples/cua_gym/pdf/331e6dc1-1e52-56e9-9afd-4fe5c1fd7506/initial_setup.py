"""
Initial Setup: Create a 6-page PDF for rotation testing
Task ID: pdf_fm_089
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_089'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/test_rotations.pdf'


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
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page content definitions - realistic business document pages
    pages_content = [
        {
            "title": "Quarterly Sales Report - Q1 2025",
            "body": (
                "Executive Summary\n\n"
                "Total revenue for Q1 2025 reached $4.72 million, representing a 12% increase "
                "over the previous quarter. The North American region led growth with a 18% "
                "year-over-year improvement, driven primarily by enterprise software licensing.\n\n"
                "Key Highlights:\n"
                "- New customer acquisitions: 47 accounts\n"
                "- Average deal size: $98,400\n"
                "- Customer retention rate: 94.2%\n"
                "- Pipeline coverage ratio: 3.1x"
            ),
        },
        {
            "title": "Regional Performance Breakdown",
            "body": (
                "North America\n"
                "Revenue: $2,340,000 | Growth: +18% YoY\n"
                "Top performer: Sarah Chen (West Coast)\n\n"
                "Europe & Middle East\n"
                "Revenue: $1,450,000 | Growth: +8% YoY\n"
                "Top performer: Marcus Weber (DACH region)\n\n"
                "Asia Pacific\n"
                "Revenue: $930,000 | Growth: +22% YoY\n"
                "Top performer: Yuki Tanaka (Japan)"
            ),
        },
        {
            "title": "Product Line Analysis",
            "body": (
                "Enterprise Suite Pro\n"
                "Units sold: 312 | Revenue: $2,180,000\n"
                "Average selling price: $6,987\n\n"
                "Cloud Analytics Platform\n"
                "Active subscriptions: 1,847 | MRR: $425,000\n"
                "Churn rate: 2.1% monthly\n\n"
                "Professional Services\n"
                "Engagements: 89 | Revenue: $1,115,000\n"
                "Average project duration: 6.2 weeks"
            ),
        },
        {
            "title": "Marketing Campaign Results",
            "body": (
                "Digital Marketing Performance - Q1 2025\n\n"
                "Email Campaigns:\n"
                "- Campaigns sent: 24\n"
                "- Total recipients: 145,000\n"
                "- Open rate: 28.3%\n"
                "- Click-through rate: 4.7%\n\n"
                "Webinar Series:\n"
                "- Events hosted: 6\n"
                "- Total registrations: 3,240\n"
                "- Attendance rate: 52%\n"
                "- Leads generated: 487"
            ),
        },
        {
            "title": "Human Resources Update",
            "body": (
                "Workforce Statistics - March 2025\n\n"
                "Total headcount: 342 employees\n"
                "New hires this quarter: 28\n"
                "Voluntary turnover: 3.8%\n\n"
                "Department Distribution:\n"
                "- Engineering: 124 (36%)\n"
                "- Sales & Marketing: 87 (25%)\n"
                "- Customer Success: 56 (16%)\n"
                "- Operations: 42 (12%)\n"
                "- G&A: 33 (10%)"
            ),
        },
        {
            "title": "Financial Projections - Q2 2025",
            "body": (
                "Revenue Forecast\n\n"
                "Projected total revenue: $5.15 million\n"
                "Growth target: +9% QoQ\n\n"
                "Budget Allocation:\n"
                "- R&D: $1,800,000 (35%)\n"
                "- Sales & Marketing: $1,290,000 (25%)\n"
                "- Operations: $770,000 (15%)\n"
                "- G&A: $515,000 (10%)\n"
                "- Reserve: $775,000 (15%)\n\n"
                "Key investments: AI-powered analytics module, APAC expansion, "
                "SOC 2 Type II certification"
            ),
        },
    ]

    for i, content in enumerate(pages_content):
        page = doc.new_page(width=595, height=842)  # A4

        # Page header with line
        page.insert_text(
            pymupdf.Point(72, 50),
            f"Page {i + 1} of 6",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 58), pymupdf.Point(523, 58))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()

        # Title
        page.insert_text(
            pymupdf.Point(72, 90),
            content["title"],
            fontsize=18,
            fontname="hebo",
            color=(0.0, 0.2, 0.4),
        )

        # Body text in a textbox for wrapping
        rect = pymupdf.Rect(72, 120, 523, 780)
        page.insert_textbox(
            rect,
            content["body"],
            fontsize=11,
            fontname="helv",
            color=(0.1, 0.1, 0.1),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Footer
        page.insert_text(
            pymupdf.Point(72, 820),
            "Confidential - Acme Corp Internal Use Only",
            fontsize=8,
            fontname="heit",
            color=(0.6, 0.6, 0.6),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Ensure test_rotations_fixed.pdf does NOT exist
    fixed_path = f'{DOCS_DIR}/test_rotations_fixed.pdf'
    if os.path.exists(fixed_path):
        os.remove(fixed_path)

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
