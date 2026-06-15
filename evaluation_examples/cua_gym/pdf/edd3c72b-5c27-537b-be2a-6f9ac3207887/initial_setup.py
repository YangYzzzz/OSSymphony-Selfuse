"""
Initial Setup: Create a multi-page PDF with sequential page numbering in footers.
Task ID: pdf_cr_070
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_070'
PDF_PATH = f'{WORKDIR}/Desktop/numbered.pdf'
CHECK_PATH = f'{WORKDIR}/Desktop/numbering_check.txt'

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
    # Remove any pre-existing check file (must NOT exist for initial state)
    if os.path.exists(CHECK_PATH):
        os.remove(CHECK_PATH)

    doc = pymupdf.open()

    # --- Page content for an 8-page company quarterly report ---
    page_contents = [
        {
            "title": "Meridian Analytics — Q4 2025 Performance Report",
            "body": (
                "This document provides a comprehensive overview of Meridian Analytics' "
                "operational and financial performance for the fourth quarter of fiscal year 2025. "
                "The report covers revenue growth, client acquisition metrics, product development "
                "milestones, and strategic initiatives undertaken during October through December 2025.\n\n"
                "Prepared by the Office of the Chief Financial Officer\n"
                "Distribution: Board of Directors, Senior Leadership Team\n"
                "Classification: Internal — Confidential"
            ),
        },
        {
            "title": "Executive Summary",
            "body": (
                "Meridian Analytics achieved record quarterly revenue of $14.8 million in Q4 2025, "
                "representing a 23% year-over-year increase. Net client additions reached 47 enterprise "
                "accounts, bringing total active clients to 312. The successful launch of our predictive "
                "analytics module in November contributed $2.1 million in new recurring revenue.\n\n"
                "Key highlights include:\n"
                "  • Revenue: $14.8M (vs. $12.0M in Q4 2024)\n"
                "  • Gross margin: 71.3% (vs. 68.9% prior year)\n"
                "  • Customer retention rate: 94.6%\n"
                "  • Employee headcount: 218 (net addition of 31)"
            ),
        },
        {
            "title": "Revenue Breakdown by Segment",
            "body": (
                "Enterprise Solutions contributed $8.9 million (60.1% of total revenue), while the "
                "Mid-Market segment generated $4.2 million (28.4%). The SMB tier accounted for the "
                "remaining $1.7 million (11.5%).\n\n"
                "Segment Performance Details:\n"
                "  Enterprise Solutions: $8.9M — 18 new contracts signed\n"
                "  Mid-Market Analytics: $4.2M — 22 new clients onboarded\n"
                "  SMB Self-Service: $1.7M — 7 upgrades from free tier\n\n"
                "Geographic distribution remained consistent with prior quarters, with North America "
                "representing 64% of revenue, EMEA at 24%, and APAC at 12%."
            ),
        },
        {
            "title": "Product Development Updates",
            "body": (
                "The engineering team shipped 3 major releases during Q4 2025:\n\n"
                "Release 4.7 (October 8): Enhanced data pipeline connectors supporting Snowflake, "
                "Databricks, and BigQuery native integrations. Average query latency reduced by 34%.\n\n"
                "Release 4.8 (November 12): Predictive Analytics Module — our flagship ML-powered "
                "forecasting engine. Initial adoption exceeded projections by 40%, with 89 enterprise "
                "clients activating the feature within the first two weeks.\n\n"
                "Release 4.9 (December 15): Security and compliance hardening. SOC 2 Type II audit "
                "completed successfully. Added role-based access controls and audit logging."
            ),
        },
        {
            "title": "Client Acquisition and Retention",
            "body": (
                "New client acquisition velocity improved significantly in Q4, driven by targeted "
                "outbound campaigns and expanded partnership channels.\n\n"
                "Notable new enterprise clients:\n"
                "  • Thornfield Capital Partners — $420K annual contract\n"
                "  • Cascade Health Systems — $385K annual contract\n"
                "  • Evergreen Logistics Corp — $310K annual contract\n"
                "  • Pacific Rim Technologies — $275K annual contract\n\n"
                "Churn analysis: 17 accounts were lost during Q4 (5.4% annualized churn), primarily "
                "attributed to budget constraints at smaller organizations. The revenue impact of "
                "churned accounts was offset 3.2x by expansion revenue from existing clients."
            ),
        },
        {
            "title": "Operational Metrics",
            "body": (
                "Infrastructure uptime: 99.97% (exceeding 99.9% SLA target)\n"
                "Average API response time: 142ms (down from 189ms in Q3)\n"
                "Support ticket resolution: 4.2 hours median (vs. 6.1 hours in Q3)\n"
                "Customer satisfaction (NPS): 72 (up from 68)\n\n"
                "Headcount by department as of December 31, 2025:\n"
                "  Engineering: 94 employees\n"
                "  Sales & Marketing: 52 employees\n"
                "  Customer Success: 38 employees\n"
                "  Operations & Finance: 22 employees\n"
                "  Executive: 12 employees\n"
                "  Total: 218 employees"
            ),
        },
        {
            "title": "Financial Outlook — Q1 2026",
            "body": (
                "Management projects Q1 2026 revenue in the range of $15.5M to $16.2M, reflecting "
                "continued momentum in enterprise sales and the full-quarter impact of the predictive "
                "analytics module.\n\n"
                "Planned investments:\n"
                "  • $1.8M in R&D for natural language query interface\n"
                "  • $900K in APAC market expansion (Singapore office)\n"
                "  • $600K in data center capacity (US-East and EU-West regions)\n\n"
                "Risk factors: Potential headwinds from macroeconomic uncertainty in European markets "
                "and increasing competition from well-funded startups in the analytics space. "
                "Management believes differentiation through ML capabilities and customer service "
                "will sustain competitive advantage."
            ),
        },
        {
            "title": "Appendix: Quarterly Comparison Table",
            "body": (
                "Quarterly Revenue Comparison (in millions USD):\n\n"
                "  Quarter    Revenue    Growth    Clients    NPS\n"
                "  Q1 2025    $11.2      +15%      248       64\n"
                "  Q2 2025    $12.1      +19%      265       66\n"
                "  Q3 2025    $13.4      +21%      289       68\n"
                "  Q4 2025    $14.8      +23%      312       72\n\n"
                "Full Year 2025 Total Revenue: $51.5 million\n"
                "Full Year 2024 Total Revenue: $39.8 million\n"
                "Year-over-Year Growth: 29.4%\n\n"
                "This document is the proprietary information of Meridian Analytics, Inc. "
                "Unauthorized distribution is prohibited."
            ),
        },
    ]

    for page_num, content in enumerate(page_contents, start=1):
        # A4 page
        page = doc.new_page(width=595, height=842)

        # --- Title ---
        title_fontsize = 18 if page_num == 1 else 15
        title_fontname = "hebo"  # Helvetica-Bold
        title_y = 72
        page.insert_text(
            pymupdf.Point(72, title_y),
            content["title"],
            fontsize=title_fontsize,
            fontname=title_fontname,
            color=(0.1, 0.1, 0.3),
        )

        # --- Horizontal rule under title ---
        shape = page.new_shape()
        rule_y = title_y + 12
        shape.draw_line(pymupdf.Point(72, rule_y), pymupdf.Point(523, rule_y))
        shape.finish(color=(0.6, 0.6, 0.6), width=0.8)
        shape.commit()

        # --- Body text ---
        body_rect = pymupdf.Rect(72, rule_y + 18, 523, 790)
        page.insert_textbox(
            body_rect,
            content["body"],
            fontsize=11,
            fontname="helv",
            color=(0.1, 0.1, 0.1),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # --- Footer with page number ---
        footer_text = f"— {page_num} —"
        page.insert_text(
            pymupdf.Point(280, 825),
            footer_text,
            fontsize=9,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

    doc.save(PDF_PATH)
    doc.close()
    print(f'Initial file created: {PDF_PATH}')

    # Ensure Desktop directory exists
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    # GUI-ready startup: open the PDF in Evince
    launch_gui(f'evince "{PDF_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
