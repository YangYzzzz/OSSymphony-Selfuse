"""
Initial Setup: Create a 10-page PDF report with blank pages 4 and 7
Task ID: pdf_gf1_033
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user/Documents'
OUTPUT = f'{WORKDIR}/report_with_blanks.pdf'

A4_WIDTH, A4_HEIGHT = 595, 842

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

# Page content for the 10 pages. Pages 4 and 7 (1-indexed) are blank.
page_content = {
    1: {
        "title": "Quarterly Business Review - Q1 2025",
        "body": (
            "Prepared by: Sarah Chen, VP of Strategy\n"
            "Date: March 31, 2025\n\n"
            "This report summarizes the key performance indicators, revenue trends, "
            "and strategic initiatives for Meridian Technologies during the first quarter "
            "of fiscal year 2025. Overall, the company achieved a 12% year-over-year "
            "revenue growth, driven primarily by expansion in the cloud services division "
            "and strong adoption of our enterprise AI platform."
        ),
    },
    2: {
        "title": "Executive Summary",
        "body": (
            "Key Highlights:\n\n"
            "- Total revenue reached $45.2M, exceeding projections by 8%\n"
            "- Cloud services revenue grew 23% quarter-over-quarter\n"
            "- Customer retention rate improved to 94.7%\n"
            "- New enterprise contracts signed: 37 (up from 28 in Q4 2024)\n"
            "- Operating margin expanded to 18.3% from 16.1%\n\n"
            "The strong performance was supported by the successful launch of "
            "our Aurora Analytics platform in January, which has already onboarded "
            "142 enterprise customers across North America and Europe."
        ),
    },
    3: {
        "title": "Revenue Breakdown by Division",
        "body": (
            "Cloud Services Division:\n"
            "  Revenue: $18.9M (42% of total)\n"
            "  Growth: +23% QoQ\n"
            "  Key driver: Aurora Analytics platform adoption\n\n"
            "Enterprise Software Division:\n"
            "  Revenue: $14.7M (33% of total)\n"
            "  Growth: +5% QoQ\n"
            "  Key driver: License renewals and upsells\n\n"
            "Professional Services Division:\n"
            "  Revenue: $8.1M (18% of total)\n"
            "  Growth: +2% QoQ\n"
            "  Key driver: Implementation consulting\n\n"
            "Hardware & Other:\n"
            "  Revenue: $3.5M (7% of total)\n"
            "  Growth: -4% QoQ\n"
            "  Note: Planned phase-down of legacy hardware line"
        ),
    },
    4: None,  # Blank page
    5: {
        "title": "Customer Acquisition & Retention",
        "body": (
            "New Customer Metrics:\n"
            "  Total new accounts: 142\n"
            "  Average contract value: $318,500\n"
            "  Sales cycle (avg): 47 days (down from 62 days)\n"
            "  Win rate: 34% (up from 29%)\n\n"
            "Retention Metrics:\n"
            "  Logo retention: 94.7%\n"
            "  Net revenue retention: 112%\n"
            "  Churn reasons breakdown:\n"
            "    - Budget constraints: 38%\n"
            "    - Competitor switch: 25%\n"
            "    - Product fit: 22%\n"
            "    - Other: 15%\n\n"
            "Notable new customers include GlobalPharma Inc., TechBridge Solutions, "
            "and Sentinel Financial Group."
        ),
    },
    6: {
        "title": "Product Development Update",
        "body": (
            "Aurora Analytics Platform (v2.1):\n"
            "  Released: January 15, 2025\n"
            "  Features: Real-time dashboards, predictive modeling, NLP query engine\n"
            "  Adoption: 142 enterprise customers in first 75 days\n\n"
            "Meridian Core ERP (v8.4):\n"
            "  Released: February 28, 2025\n"
            "  Features: Enhanced workflow automation, API marketplace\n"
            "  Migration: 67% of existing customers upgraded\n\n"
            "Upcoming Releases:\n"
            "  - Aurora Analytics v2.2 (April 2025): Multi-tenant support\n"
            "  - Meridian Mobile SDK (May 2025): Cross-platform development kit\n"
            "  - Sentinel Security Suite (June 2025): Zero-trust architecture"
        ),
    },
    7: None,  # Blank page
    8: {
        "title": "Financial Projections - Q2 2025",
        "body": (
            "Revenue Forecast:\n"
            "  Conservative estimate: $47.8M\n"
            "  Base case: $50.1M\n"
            "  Optimistic scenario: $53.4M\n\n"
            "Key Assumptions:\n"
            "  - Cloud services growth continues at 18-25% QoQ\n"
            "  - 45 new enterprise contracts expected\n"
            "  - Professional services pipeline at $12M\n"
            "  - No major competitive disruptions\n\n"
            "Investment Priorities:\n"
            "  - R&D headcount expansion: +22 engineers\n"
            "  - Sales team growth: +15 account executives\n"
            "  - Infrastructure: $2.4M for cloud capacity expansion\n"
            "  - Marketing: $1.8M for Aurora Analytics campaign"
        ),
    },
    9: {
        "title": "Risk Assessment & Mitigation",
        "body": (
            "High Priority Risks:\n\n"
            "1. Market Competition\n"
            "   Risk Level: High\n"
            "   Impact: Potential 5-8% revenue erosion\n"
            "   Mitigation: Accelerate product differentiation, loyalty programs\n\n"
            "2. Talent Retention\n"
            "   Risk Level: Medium-High\n"
            "   Impact: Development delays, knowledge loss\n"
            "   Mitigation: Enhanced compensation packages, remote work flexibility\n\n"
            "3. Regulatory Changes (Data Privacy)\n"
            "   Risk Level: Medium\n"
            "   Impact: Compliance costs estimated at $1.2M\n"
            "   Mitigation: Dedicated compliance team, proactive auditing\n\n"
            "4. Supply Chain (Hardware Division)\n"
            "   Risk Level: Low-Medium\n"
            "   Impact: Delivery delays for legacy contracts\n"
            "   Mitigation: Diversified supplier base, buffer inventory"
        ),
    },
    10: {
        "title": "Appendix & Contact Information",
        "body": (
            "Report prepared by Meridian Technologies Strategic Planning Team\n\n"
            "Primary Contacts:\n"
            "  Sarah Chen, VP of Strategy - sarah.chen@meridiantech.com\n"
            "  Marcus Johnson, CFO - marcus.johnson@meridiantech.com\n"
            "  Priya Patel, CTO - priya.patel@meridiantech.com\n"
            "  David Kim, VP of Sales - david.kim@meridiantech.com\n\n"
            "Data Sources:\n"
            "  - Salesforce CRM (customer metrics)\n"
            "  - NetSuite (financial data)\n"
            "  - Jira (product development tracking)\n"
            "  - Tableau (analytics and visualizations)\n\n"
            "Confidentiality Notice:\n"
            "This document contains proprietary information belonging to Meridian "
            "Technologies Inc. Distribution is restricted to authorized personnel only."
        ),
    },
}


def create_initial():
    os.makedirs(WORKDIR, exist_ok=True)

    doc = pymupdf.open()

    for page_num in range(1, 11):
        page = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
        content = page_content.get(page_num)

        if content is None:
            # Blank page - just add a small footer to mark it
            page.insert_text(
                pymupdf.Point(A4_WIDTH / 2 - 20, A4_HEIGHT - 30),
                f"Page {page_num}",
                fontsize=8,
                fontname="helv",
                color=(0.7, 0.7, 0.7),
            )
            continue

        # Title
        page.insert_text(
            pymupdf.Point(72, 72),
            content["title"],
            fontsize=18,
            fontname="hebo",
            color=(0.0, 0.13, 0.4),
        )

        # Horizontal rule under title
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
        shape.finish(color=(0.0, 0.13, 0.4), width=1.5)
        shape.commit()

        # Body text
        body_rect = pymupdf.Rect(72, 100, 523, 780)
        page.insert_textbox(
            body_rect,
            content["body"],
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Page number footer
        page.insert_text(
            pymupdf.Point(A4_WIDTH / 2 - 10, A4_HEIGHT - 30),
            f"Page {page_num}",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    # Set metadata
    doc.set_metadata({
        "title": "Quarterly Business Review - Q1 2025",
        "author": "Meridian Technologies",
        "subject": "Q1 2025 Performance Report",
        "creator": "CUA-Gym Setup",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
