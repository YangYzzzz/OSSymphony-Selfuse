"""
Initial Setup: Create a 10-page report PDF with realistic content, no sidebar annotations.
Task ID: pdf_ro_031
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_031'
OUTPUT = f'{WORKDIR}/Documents/report.pdf'

LETTER_WIDTH, LETTER_HEIGHT = 612, 792


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
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    doc = pymupdf.open()

    # Report content for each page
    pages_content = [
        {
            "title": "Meridian Technologies - Annual Report 2025",
            "body": (
                "This document presents the comprehensive annual review of Meridian Technologies Inc. "
                "for the fiscal year ending December 31, 2025. The report covers financial performance, "
                "operational highlights, strategic initiatives, and forward-looking guidance for stakeholders.\n\n"
                "Meridian Technologies has continued its trajectory of sustainable growth, achieving record "
                "revenues of $2.47 billion, representing a 14.3% year-over-year increase. Our commitment to "
                "innovation in cloud infrastructure and enterprise AI solutions has positioned us favorably "
                "in an increasingly competitive market landscape."
            ),
        },
        {
            "title": "Executive Summary",
            "body": (
                "Key Highlights for Fiscal Year 2025:\n\n"
                "Revenue: $2.47 billion (up 14.3% YoY)\n"
                "Operating Income: $412 million (up 18.7% YoY)\n"
                "Net Income: $338 million (up 21.2% YoY)\n"
                "Earnings Per Share: $4.82 (up from $3.98)\n"
                "Free Cash Flow: $487 million\n\n"
                "The company expanded its customer base to over 12,400 enterprise clients across 47 countries. "
                "Notable achievements include the successful launch of the Aurora AI Platform, which has already "
                "been adopted by 2,300 organizations within the first six months of availability."
            ),
        },
        {
            "title": "Financial Performance Overview",
            "body": (
                "Revenue Breakdown by Segment:\n\n"
                "Cloud Infrastructure Services: $1.12B (45.3% of total)\n"
                "Enterprise AI Solutions: $689M (27.9% of total)\n"
                "Professional Services: $418M (16.9% of total)\n"
                "Licensing and Maintenance: $243M (9.9% of total)\n\n"
                "Gross margin improved to 67.2% from 64.8% in the prior year, driven by increased adoption "
                "of higher-margin AI offerings and continued optimization of cloud delivery infrastructure. "
                "Operating expenses were well-controlled at $1.24 billion, with R&D investment increasing "
                "strategically to $487 million (19.7% of revenue)."
            ),
        },
        {
            "title": "Product and Technology Review",
            "body": (
                "Aurora AI Platform:\n"
                "Our flagship AI platform achieved general availability in March 2025 and has rapidly become "
                "the cornerstone of our enterprise offerings. Key capabilities include automated model training, "
                "real-time inference at scale, and seamless integration with existing data pipelines.\n\n"
                "CloudSpan Infrastructure:\n"
                "The CloudSpan network expanded to 28 global regions with 84 availability zones. Network "
                "throughput increased by 340% following the deployment of next-generation switching fabric. "
                "Customer workload migration velocity improved by 2.8x through our enhanced migration toolkit."
            ),
        },
        {
            "title": "Market Analysis and Competitive Position",
            "body": (
                "The global enterprise cloud market reached $624 billion in 2025, growing at a CAGR of 19.2%. "
                "Meridian Technologies maintained its position as the fourth-largest provider by revenue, with a "
                "market share of approximately 3.96%.\n\n"
                "Competitive advantages include:\n"
                "- Industry-leading AI integration capabilities\n"
                "- Superior hybrid cloud orchestration\n"
                "- 99.997% uptime SLA achievement\n"
                "- Lowest total cost of ownership in comparative analyst studies\n\n"
                "Customer retention rate remained strong at 94.7%, with net revenue retention reaching 118.3%, "
                "indicating significant expansion within existing accounts."
            ),
        },
        {
            "title": "Workforce and Talent Development",
            "body": (
                "Meridian Technologies employed 18,420 full-time employees as of December 31, 2025, an increase "
                "of 2,180 from the prior year. Hiring was concentrated in engineering (1,340 new hires) and "
                "customer success (480 new hires).\n\n"
                "Employee Engagement Score: 4.3/5.0 (industry avg: 3.8)\n"
                "Voluntary Turnover Rate: 8.2% (industry avg: 14.1%)\n"
                "Internal Mobility Rate: 23.4%\n"
                "Training Investment Per Employee: $4,850\n\n"
                "The Meridian Leadership Academy graduated its third cohort of 145 high-potential leaders, "
                "with 78% of graduates receiving promotions within 12 months of completion."
            ),
        },
        {
            "title": "Sustainability and ESG Initiatives",
            "body": (
                "Environmental commitments remained central to our operations in 2025:\n\n"
                "Carbon Emissions: Reduced Scope 1 and 2 emissions by 31% vs. 2020 baseline\n"
                "Renewable Energy: 82% of data center power sourced from renewables\n"
                "Water Usage: PUE improved to 1.18 across all facilities\n"
                "E-Waste: 97.3% of decommissioned hardware recycled or refurbished\n\n"
                "Social impact programs reached 45,000 students through our STEM education initiative across "
                "underserved communities in North America and Southeast Asia. The Meridian Foundation disbursed "
                "$12.4 million in grants supporting digital literacy and workforce development programs."
            ),
        },
        {
            "title": "Risk Factors and Mitigation",
            "body": (
                "Key risk areas identified and addressed during 2025:\n\n"
                "1. Cybersecurity Threats: Invested $89 million in security infrastructure upgrades. Zero "
                "material breaches reported. Achieved SOC 2 Type II, ISO 27001, and FedRAMP High certifications.\n\n"
                "2. Supply Chain Disruptions: Diversified hardware suppliers from 12 to 19 vendors. Maintained "
                "strategic inventory buffers of 90 days for critical components.\n\n"
                "3. Regulatory Compliance: Established dedicated AI governance team of 34 specialists to ensure "
                "compliance with emerging AI regulations across jurisdictions.\n\n"
                "4. Macroeconomic Uncertainty: Maintained a strong balance sheet with $1.8 billion in cash "
                "and short-term investments, providing significant operational flexibility."
            ),
        },
        {
            "title": "Strategic Outlook for 2026",
            "body": (
                "Management guidance for fiscal year 2026:\n\n"
                "Revenue: $2.78 - $2.85 billion (12-15% growth)\n"
                "Operating Margin: 17.5% - 18.5%\n"
                "Capital Expenditure: $520 - $560 million\n"
                "Headcount Growth: 15-18% increase\n\n"
                "Strategic priorities include:\n"
                "- Expansion of Aurora AI Platform with agentic workflow capabilities\n"
                "- Entry into three new geographic markets (Brazil, India, Saudi Arabia)\n"
                "- Launch of sovereign cloud offerings for government clients\n"
                "- Acquisition of complementary technologies in the observability space\n"
                "- Deepening partnerships with major hyperscalers for hybrid deployments"
            ),
        },
        {
            "title": "Board of Directors and Corporate Governance",
            "body": (
                "Board Composition (as of December 31, 2025):\n\n"
                "Dr. Elena Vasquez - Chairperson, Independent Director\n"
                "James T. Harrington - CEO and Director\n"
                "Dr. Aisha Patel - Lead Independent Director\n"
                "Robert Nakamura - Independent Director\n"
                "Sarah Lindqvist - Independent Director\n"
                "Marcus Chen-Williams - Independent Director\n"
                "Patricia O'Brien - Independent Director\n"
                "Dr. Kwame Asante - Independent Director\n\n"
                "The board met 8 times during the fiscal year, with an average attendance rate of 96.5%. "
                "All committees (Audit, Compensation, Nominating & Governance, Technology) maintained full "
                "independence and met their respective charter requirements."
            ),
        },
    ]

    for i, page_data in enumerate(pages_content):
        page = doc.new_page(width=LETTER_WIDTH, height=LETTER_HEIGHT)

        # Title
        page.insert_text(
            pymupdf.Point(72, 72),
            page_data["title"],
            fontsize=18,
            fontname="hebo",
            color=(0.1, 0.1, 0.3),
        )

        # Horizontal rule under title
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
        shape.finish(color=(0.3, 0.3, 0.5), width=1)
        shape.commit()

        # Body text
        body_rect = pymupdf.Rect(72, 100, 540, 740)
        page.insert_textbox(
            body_rect,
            page_data["body"],
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Page number footer
        page.insert_text(
            pymupdf.Point(290, 770),
            f"Page {i + 1} of 10",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    doc.set_metadata({
        "title": "Meridian Technologies Annual Report 2025",
        "author": "Meridian Technologies Inc.",
        "subject": "Annual Report",
        "keywords": "annual report, technology, cloud, AI, 2025",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
