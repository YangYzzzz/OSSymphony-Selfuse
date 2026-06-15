"""
Initial Setup: Create an 8-page portrait PDF scanned report needing rotation correction.
Task ID: pdf_gf3_001
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_001'
DOCDIR = f'{WORKDIR}/documents'
OUTPUT = f'{DOCDIR}/report.pdf'

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
    os.makedirs(DOCDIR, exist_ok=True)

    doc = pymupdf.open()  # new empty PDF

    # --- Page content data: simulate a scanned business report ---
    pages_content = [
        {
            "title": "Meridian Consulting Group",
            "subtitle": "Annual Operations Review 2025",
            "body": (
                "Prepared by: Elena Vasquez, Senior Operations Analyst\n"
                "Date: March 14, 2025\n"
                "Distribution: Internal — Board of Directors\n\n"
                "This document provides a comprehensive review of operational performance "
                "across all divisions for the fiscal year ending December 31, 2025. "
                "All figures are presented in US dollars unless otherwise noted."
            ),
        },
        {
            "title": "Executive Summary",
            "subtitle": "",
            "body": (
                "Meridian Consulting Group achieved a record revenue of $14.2 million in FY2025, "
                "representing a 17.3% increase over the prior year. Operating margins improved "
                "from 22.1% to 25.8%, driven primarily by efficiency gains in the Digital "
                "Transformation practice and increased utilization rates across all service lines.\n\n"
                "Key highlights:\n"
                "  - Total engagements delivered: 247 (up from 198)\n"
                "  - Client retention rate: 94.2%\n"
                "  - Average project value: $57,490\n"
                "  - Employee headcount grew from 86 to 112\n"
                "  - Net Promoter Score: 72 (industry average: 54)"
            ),
        },
        {
            "title": "Revenue Breakdown by Division",
            "subtitle": "",
            "body": (
                "Division                    Revenue       % of Total   YoY Growth\n"
                "---------------------------------------------------------------\n"
                "Digital Transformation      $4,850,000      34.2%        +28.1%\n"
                "Strategy & Advisory         $3,620,000      25.5%        +11.4%\n"
                "Risk & Compliance           $2,940,000      20.7%        +15.9%\n"
                "Human Capital               $1,580,000      11.1%        +8.3%\n"
                "Technology Services         $1,210,000       8.5%        +22.6%\n"
                "---------------------------------------------------------------\n"
                "Total                      $14,200,000     100.0%        +17.3%\n\n"
                "The Digital Transformation division surpassed Strategy & Advisory as the "
                "largest revenue contributor for the first time in company history."
            ),
        },
        {
            "title": "Client Portfolio Analysis",
            "subtitle": "",
            "body": (
                "Meridian serves clients across six primary industry verticals. The healthcare "
                "and financial services sectors continue to represent the majority of revenue.\n\n"
                "Industry Sector         Clients    Revenue       Avg. Engagement\n"
                "---------------------------------------------------------------\n"
                "Healthcare               42       $3,980,000     $94,762\n"
                "Financial Services       38       $3,550,000     $93,421\n"
                "Technology               31       $2,840,000     $91,613\n"
                "Manufacturing            24       $1,730,000     $72,083\n"
                "Government               18       $1,290,000     $71,667\n"
                "Other                    14         $810,000     $57,857\n"
                "---------------------------------------------------------------\n"
                "Total                   167      $14,200,000     $85,030"
            ),
        },
        {
            "title": "Operational Efficiency Metrics",
            "subtitle": "",
            "body": (
                "Utilization rates improved significantly across all practice areas, reflecting "
                "better resource allocation and project planning.\n\n"
                "Metric                         FY2024    FY2025    Target\n"
                "---------------------------------------------------------------\n"
                "Billable utilization rate       71.2%     78.6%     80.0%\n"
                "Project on-time delivery        82.4%     89.1%     90.0%\n"
                "Budget adherence rate           77.8%     84.3%     85.0%\n"
                "Average days to close proposal  18.3      12.7      10.0\n"
                "Rework rate                      8.1%      4.9%      3.0%\n\n"
                "The implementation of automated time-tracking and the new resource management "
                "platform contributed to a 7.4 percentage point increase in utilization."
            ),
        },
        {
            "title": "Human Resources & Talent",
            "subtitle": "",
            "body": (
                "Headcount growth was strategically focused on senior consultants and technical "
                "specialists to support expanding Digital Transformation engagements.\n\n"
                "Level              Start     End    Net Change   Turnover\n"
                "---------------------------------------------------------------\n"
                "Partners               8       9        +1        0.0%\n"
                "Senior Consultants    22      31        +9        8.2%\n"
                "Consultants           34      42        +8       12.4%\n"
                "Analysts              16      22        +6       18.3%\n"
                "Support Staff          6       8        +2        5.0%\n"
                "---------------------------------------------------------------\n"
                "Total                 86     112       +26       11.8%\n\n"
                "Average compensation increased 4.2%, in line with market adjustments. "
                "The annual employee satisfaction survey returned a score of 4.1/5.0."
            ),
        },
        {
            "title": "Strategic Initiatives for FY2026",
            "subtitle": "",
            "body": (
                "The leadership team has identified five strategic priorities for the coming "
                "fiscal year:\n\n"
                "1. Launch AI & Machine Learning Advisory Practice\n"
                "   Target: $1.5M revenue in first year; recruit 8 specialists by Q2\n\n"
                "2. Expand Geographic Footprint\n"
                "   Open satellite offices in Denver and Austin to serve Southwest clients\n\n"
                "3. Develop Proprietary Analytics Platform\n"
                "   Investment: $620,000 over 18 months; expected ROI within 3 years\n\n"
                "4. Achieve ISO 27001 Certification\n"
                "   Timeline: Audit scheduled for September 2026\n\n"
                "5. Increase Recurring Revenue to 30% of Total\n"
                "   Current: 18.4%; Strategy: introduce retainer-based advisory packages"
            ),
        },
        {
            "title": "Appendix: Financial Summary",
            "subtitle": "",
            "body": (
                "Income Statement Highlights (in thousands)\n\n"
                "                             FY2024      FY2025     Change\n"
                "---------------------------------------------------------------\n"
                "Revenue                     $12,108     $14,200     +17.3%\n"
                "Cost of Services             $8,430      $9,520     +12.9%\n"
                "Gross Profit                 $3,678      $4,680     +27.2%\n"
                "Operating Expenses           $1,006      $1,014     +0.8%\n"
                "Operating Income             $2,672      $3,666     +37.2%\n"
                "Interest & Other               ($84)       ($71)   -15.5%\n"
                "Net Income                   $2,588      $3,595     +38.9%\n\n"
                "Operating Margin              22.1%       25.8%\n"
                "Net Margin                    21.4%       25.3%\n\n"
                "Note: All figures are unaudited. Final audited statements will be "
                "available by April 30, 2026.\n\n"
                "Document ID: MCG-OPS-2025-AR-001\n"
                "Classification: Internal — Confidential"
            ),
        },
    ]

    for i, content in enumerate(pages_content):
        # A4 portrait pages
        page = doc.new_page(width=595, height=842)

        y = 72  # top margin

        # Title
        page.insert_text(
            pymupdf.Point(72, y),
            content["title"],
            fontsize=18 if i == 0 else 16,
            fontname="hebo",  # Helvetica Bold
            color=(0.1, 0.1, 0.3),
        )
        y += 30

        # Subtitle (if present)
        if content["subtitle"]:
            page.insert_text(
                pymupdf.Point(72, y),
                content["subtitle"],
                fontsize=13,
                fontname="heit",  # Helvetica Italic
                color=(0.3, 0.3, 0.3),
            )
            y += 24

        # Horizontal rule
        y += 8
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(523, y))
        shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape.commit()
        y += 16

        # Body text in a textbox
        rect = pymupdf.Rect(72, y, 523, 790)
        page.insert_textbox(
            rect,
            content["body"],
            fontsize=10,
            fontname="helv",
            color=(0.1, 0.1, 0.1),
        )

        # Page number at bottom
        page.insert_text(
            pymupdf.Point(280, 820),
            f"Page {i + 1} of 8",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify
    check = pymupdf.open(OUTPUT)
    print(f'Page count: {check.page_count}')
    for i in range(check.page_count):
        p = check[i]
        print(f'  Page {i}: rotation={p.rotation}, size={p.rect.width}x{p.rect.height}')
    check.close()

    # Open PDF in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
