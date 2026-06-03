"""
Initial Setup: Create a 20-page presentation PDF and empty slides directory.
Task ID: pdf_ro_018
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_018'
OUTPUT = f'{WORKDIR}/Documents/presentation.pdf'
SLIDES_DIR = f'{WORKDIR}/Documents/slides'

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

# Slide content for a realistic 20-page corporate presentation
SLIDES = [
    {
        "title": "Q4 2025 Strategic Review",
        "subtitle": "Presented by the Executive Leadership Team",
        "body": "Nextera Solutions Inc.\nDecember 15, 2025",
        "color": (0.1, 0.2, 0.45),  # dark navy
    },
    {
        "title": "Agenda",
        "body": (
            "1. Executive Summary\n"
            "2. Revenue Performance\n"
            "3. Product Development Updates\n"
            "4. Customer Acquisition Metrics\n"
            "5. Regional Market Analysis\n"
            "6. Technology Infrastructure\n"
            "7. Talent & Workforce Planning\n"
            "8. Risk Assessment\n"
            "9. Q1 2026 Roadmap\n"
            "10. Appendix"
        ),
        "color": (0.15, 0.25, 0.5),
    },
    {
        "title": "Executive Summary",
        "body": (
            "Revenue grew 18.3% year-over-year to $142.7M in Q4, exceeding the forecast of $135M.\n\n"
            "Net new customers: 2,847 (+23% QoQ)\n"
            "Annual recurring revenue: $487.2M\n"
            "Customer retention rate: 94.6%\n"
            "EBITDA margin improved from 22.1% to 26.4%"
        ),
        "color": (0.0, 0.35, 0.25),
    },
    {
        "title": "Revenue by Segment",
        "body": (
            "Enterprise Solutions    $67.3M   (+21%)\n"
            "Mid-Market Platform     $42.1M   (+15%)\n"
            "SMB Products            $21.8M   (+12%)\n"
            "Professional Services   $11.5M   (+24%)\n\n"
            "Total Revenue: $142.7M"
        ),
        "color": (0.3, 0.15, 0.4),
    },
    {
        "title": "Customer Growth Trends",
        "body": (
            "Jan 2025: 12,340 active accounts\n"
            "Mar 2025: 13,890 active accounts\n"
            "Jun 2025: 15,620 active accounts\n"
            "Sep 2025: 17,410 active accounts\n"
            "Dec 2025: 19,540 active accounts\n\n"
            "Average deal size increased from $24,500 to $28,700"
        ),
        "color": (0.1, 0.3, 0.5),
    },
    {
        "title": "Product Development Highlights",
        "body": (
            "- Launched Analytics Pro v3.2 with predictive modeling\n"
            "- Released mobile companion app (iOS & Android)\n"
            "- Deployed AI-powered customer support chatbot\n"
            "- Completed SOC 2 Type II certification\n"
            "- Reduced average page load time by 40%"
        ),
        "color": (0.2, 0.1, 0.35),
    },
    {
        "title": "Engineering Velocity",
        "body": (
            "Sprint velocity: 127 story points/sprint (up from 98)\n"
            "Deployment frequency: 14 deployments/week\n"
            "Mean time to recovery: 23 minutes\n"
            "Code coverage: 87.3%\n"
            "Open bugs: 42 (P1: 0, P2: 3, P3: 39)\n\n"
            "Team size: 68 engineers across 9 squads"
        ),
        "color": (0.35, 0.2, 0.1),
    },
    {
        "title": "Regional Performance: North America",
        "body": (
            "Revenue: $89.4M (62.6% of total)\n"
            "New customers: 1,523\n"
            "Key wins: Meridian Health Systems ($2.1M ACV),\n"
            "  Pacific Coast Financial ($1.8M ACV),\n"
            "  Great Lakes Manufacturing ($1.4M ACV)\n\n"
            "Pipeline: $34.7M in qualified opportunities"
        ),
        "color": (0.0, 0.3, 0.35),
    },
    {
        "title": "Regional Performance: EMEA",
        "body": (
            "Revenue: $32.8M (23.0% of total)\n"
            "New customers: 824\n"
            "Key wins: Berliner Technik GmbH ($950K ACV),\n"
            "  Nordic Logistics AB ($780K ACV),\n"
            "  Thames Digital PLC ($1.1M ACV)\n\n"
            "Opened new offices in Amsterdam and Warsaw"
        ),
        "color": (0.25, 0.1, 0.3),
    },
    {
        "title": "Regional Performance: APAC",
        "body": (
            "Revenue: $20.5M (14.4% of total)\n"
            "New customers: 500\n"
            "Key wins: Sakura Technologies ($620K ACV),\n"
            "  Singapore Digital Hub ($540K ACV)\n\n"
            "APAC revenue grew 31% YoY, fastest-growing region.\n"
            "Hired VP of APAC Operations (based in Singapore)"
        ),
        "color": (0.4, 0.15, 0.15),
    },
    {
        "title": "Customer Satisfaction Scores",
        "body": (
            "Net Promoter Score (NPS): 72 (up from 65)\n"
            "Customer Satisfaction (CSAT): 4.6 / 5.0\n"
            "Customer Effort Score (CES): 4.2 / 5.0\n\n"
            "Top feedback themes:\n"
            "  + Excellent onboarding experience\n"
            "  + Responsive support team\n"
            "  - API documentation needs improvement\n"
            "  - Mobile app performance on Android"
        ),
        "color": (0.1, 0.35, 0.2),
    },
    {
        "title": "Technology Infrastructure",
        "body": (
            "Cloud spend: $4.8M/quarter (optimized 12% from Q3)\n"
            "Uptime SLA: 99.97% achieved\n"
            "Data centers: 4 regions (US-East, US-West, EU-West, APAC-SE)\n"
            "CDN edge locations: 47 globally\n\n"
            "Completed migration from PostgreSQL 14 to 16\n"
            "Kubernetes cluster: 340 pods across 28 nodes"
        ),
        "color": (0.2, 0.25, 0.4),
    },
    {
        "title": "Security & Compliance",
        "body": (
            "Achieved certifications:\n"
            "  - SOC 2 Type II\n"
            "  - ISO 27001:2022\n"
            "  - HIPAA (healthcare vertical)\n"
            "  - GDPR compliance audit (clean)\n\n"
            "Zero critical security incidents in Q4\n"
            "Penetration testing: 0 critical, 2 medium findings (resolved)"
        ),
        "color": (0.3, 0.1, 0.1),
    },
    {
        "title": "Talent & Workforce",
        "body": (
            "Total headcount: 412 (up from 367)\n"
            "Engineering: 68  |  Sales: 54  |  Marketing: 32\n"
            "Customer Success: 45  |  Operations: 28\n"
            "Product: 22  |  G&A: 163\n\n"
            "Employee engagement score: 8.2 / 10\n"
            "Voluntary attrition: 8.4% (industry avg: 13.2%)"
        ),
        "color": (0.15, 0.3, 0.35),
    },
    {
        "title": "Financial Overview",
        "body": (
            "Gross Revenue:        $142.7M\n"
            "Cost of Goods Sold:    $48.5M\n"
            "Gross Profit:          $94.2M  (66.0%)\n"
            "Operating Expenses:    $56.1M\n"
            "EBITDA:                $37.7M  (26.4%)\n"
            "Net Income:            $28.3M  (19.8%)\n\n"
            "Cash & equivalents: $67.4M"
        ),
        "color": (0.05, 0.2, 0.4),
    },
    {
        "title": "Risk Assessment",
        "body": (
            "HIGH: Increased competition in mid-market segment\n"
            "  Mitigation: Accelerated feature roadmap, pricing review\n\n"
            "MEDIUM: Key person dependency in ML engineering team\n"
            "  Mitigation: Cross-training program, hiring 2 senior ML engineers\n\n"
            "LOW: Currency fluctuation impact on EMEA revenue\n"
            "  Mitigation: Hedging strategy implemented"
        ),
        "color": (0.35, 0.15, 0.1),
    },
    {
        "title": "Q1 2026 Strategic Priorities",
        "body": (
            "1. Launch Enterprise Analytics v4.0 with AI features\n"
            "2. Expand APAC sales team by 40%\n"
            "3. Achieve $500M ARR milestone\n"
            "4. Complete Series D funding round ($75M target)\n"
            "5. Open Tokyo office\n"
            "6. Implement PLG motion for SMB segment"
        ),
        "color": (0.1, 0.25, 0.45),
    },
    {
        "title": "Investment Asks",
        "body": (
            "Engineering: $3.2M additional (AI/ML capabilities)\n"
            "Sales & Marketing: $2.8M (APAC expansion)\n"
            "Infrastructure: $1.5M (APAC data center)\n"
            "Talent: $1.1M (key hires across departments)\n\n"
            "Total incremental investment: $8.6M\n"
            "Expected ROI: 3.2x within 18 months"
        ),
        "color": (0.2, 0.3, 0.15),
    },
    {
        "title": "Key Milestones Timeline",
        "body": (
            "Jan 2026: Series D close\n"
            "Feb 2026: Analytics v4.0 beta launch\n"
            "Mar 2026: Tokyo office opening\n"
            "Apr 2026: $500M ARR milestone\n"
            "May 2026: APAC data center live\n"
            "Jun 2026: Analytics v4.0 GA release"
        ),
        "color": (0.25, 0.2, 0.35),
    },
    {
        "title": "Thank You",
        "subtitle": "Questions & Discussion",
        "body": (
            "Contact: strategy@nextera-solutions.com\n"
            "Investor Relations: ir@nextera-solutions.com\n\n"
            "Nextera Solutions Inc.\n"
            "1200 Innovation Drive, Suite 400\n"
            "San Francisco, CA 94105"
        ),
        "color": (0.1, 0.2, 0.45),
    },
]


def create_initial():
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)
    os.makedirs(SLIDES_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page size: 10 x 7.5 inches = 720 x 540 points
    PAGE_W = 720
    PAGE_H = 540

    for i, slide in enumerate(SLIDES):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        shape = page.new_shape()

        # Background color bar at top
        r, g, b = slide["color"]
        header_rect = pymupdf.Rect(0, 0, PAGE_W, 80)
        shape.draw_rect(header_rect)
        shape.finish(color=None, fill=(r, g, b))

        # Decorative line under header
        shape.draw_line(pymupdf.Point(40, 85), pymupdf.Point(680, 85))
        shape.finish(color=(r, g, b), width=1.5)

        shape.commit()

        # Title text (white on colored header)
        title = slide["title"]
        page.insert_text(
            pymupdf.Point(50, 55),
            title,
            fontsize=28,
            fontname="hebo",
            color=(1, 1, 1),
        )

        # Subtitle if present
        y_offset = 120
        if "subtitle" in slide:
            page.insert_text(
                pymupdf.Point(50, y_offset),
                slide["subtitle"],
                fontsize=18,
                fontname="heit",
                color=(0.3, 0.3, 0.3),
            )
            y_offset += 40

        # Body text
        if "body" in slide:
            body_rect = pymupdf.Rect(50, y_offset, 670, 500)
            page.insert_textbox(
                body_rect,
                slide["body"],
                fontsize=14,
                fontname="helv",
                color=(0.15, 0.15, 0.15),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )

        # Page number at bottom right
        page.insert_text(
            pymupdf.Point(670, 525),
            str(i + 1),
            fontsize=10,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Footer line
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(40, 510), pymupdf.Point(680, 510))
        shape2.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape2.commit()

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Created {len(SLIDES)} pages')
    print(f'Slides directory created: {SLIDES_DIR}')

    # Verify
    verify_doc = pymupdf.open(OUTPUT)
    print(f'Verification: {verify_doc.page_count} pages, page size: {verify_doc[0].rect.width}x{verify_doc[0].rect.height}')
    verify_doc.close()

    # Open the PDF in evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')

create_initial()
