"""
Initial Setup: Create an 8-page brochure PDF in sequential page order.
Task ID: pdf_gf2_050
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCS_DIR = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_gf2_050'
OUTPUT = f'{DOCS_DIR}/brochure.pdf'

# Page content for a realistic company brochure
PAGE_CONTENT = [
    {
        "title": "Meridian Technologies",
        "subtitle": "Innovation Through Excellence",
        "body": "Annual Product Catalog 2025\nYour Trusted Partner in Enterprise Solutions",
        "footer": "Page 1 of 8",
        "color": (0.0, 0.2, 0.5),  # dark blue
    },
    {
        "title": "About Us",
        "subtitle": "Who We Are",
        "body": (
            "Founded in 2008, Meridian Technologies has grown from a small startup in "
            "Portland, Oregon to a global leader in enterprise software solutions. Our team "
            "of over 2,400 professionals serves clients across 35 countries.\n\n"
            "Our mission is to empower businesses with cutting-edge technology that drives "
            "efficiency, collaboration, and growth. We believe in sustainable innovation "
            "and long-term partnerships with our clients."
        ),
        "footer": "Page 2 of 8",
        "color": (0.0, 0.3, 0.6),
    },
    {
        "title": "Cloud Infrastructure",
        "subtitle": "MeridianCloud Platform",
        "body": (
            "Our flagship cloud platform provides:\n\n"
            "  - Auto-scaling compute instances (up to 10,000 nodes)\n"
            "  - 99.99% uptime SLA guarantee\n"
            "  - Multi-region data replication\n"
            "  - Real-time monitoring and alerting\n"
            "  - SOC 2 Type II certified security\n\n"
            "Starting at $0.023/hour per compute unit.\n"
            "Enterprise plans available with dedicated support."
        ),
        "footer": "Page 3 of 8",
        "color": (0.1, 0.4, 0.2),  # green
    },
    {
        "title": "Data Analytics Suite",
        "subtitle": "MeridianInsight 3.0",
        "body": (
            "Transform raw data into actionable intelligence:\n\n"
            "  - Process up to 50TB of data per hour\n"
            "  - Built-in machine learning pipelines\n"
            "  - Interactive dashboard builder\n"
            "  - Natural language query interface\n"
            "  - Connectors for 200+ data sources\n\n"
            "Trusted by Fortune 500 companies including Apex Financial Group, "
            "Sterling Healthcare, and Nova Logistics."
        ),
        "footer": "Page 4 of 8",
        "color": (0.5, 0.2, 0.0),  # brown/orange
    },
    {
        "title": "Cybersecurity Solutions",
        "subtitle": "MeridianShield Enterprise",
        "body": (
            "Comprehensive protection for your digital assets:\n\n"
            "  - Zero-trust network architecture\n"
            "  - AI-powered threat detection\n"
            "  - Automated incident response\n"
            "  - Compliance management (GDPR, HIPAA, PCI-DSS)\n"
            "  - 24/7 Security Operations Center\n\n"
            "In 2024, MeridianShield blocked over 12 million threats "
            "across our client base, with an average detection time of 0.3 seconds."
        ),
        "footer": "Page 5 of 8",
        "color": (0.5, 0.0, 0.0),  # red
    },
    {
        "title": "Customer Success Stories",
        "subtitle": "Real Results, Real Impact",
        "body": (
            "Apex Financial Group:\n"
            "  Reduced infrastructure costs by 42% after migrating to MeridianCloud.\n"
            "  ROI achieved within 8 months of deployment.\n\n"
            "Sterling Healthcare:\n"
            "  Processed 3.2 million patient records using MeridianInsight,\n"
            "  improving diagnostic accuracy by 18%.\n\n"
            "Nova Logistics:\n"
            "  Prevented $4.7M in potential losses through MeridianShield's\n"
            "  threat detection capabilities in the first year."
        ),
        "footer": "Page 6 of 8",
        "color": (0.3, 0.0, 0.5),  # purple
    },
    {
        "title": "Pricing & Plans",
        "subtitle": "Flexible Options for Every Organization",
        "body": (
            "Starter Plan - $2,500/month\n"
            "  Up to 50 users, 5TB storage, email support\n\n"
            "Professional Plan - $7,500/month\n"
            "  Up to 500 users, 50TB storage, priority support\n\n"
            "Enterprise Plan - Custom pricing\n"
            "  Unlimited users, custom storage, dedicated account manager\n"
            "  On-premise deployment option, custom SLA\n\n"
            "All plans include a 30-day free trial with full features."
        ),
        "footer": "Page 7 of 8",
        "color": (0.0, 0.4, 0.4),  # teal
    },
    {
        "title": "Contact Us",
        "subtitle": "Get Started Today",
        "body": (
            "Headquarters:\n"
            "  1200 Innovation Drive, Suite 400\n"
            "  Portland, OR 97201\n\n"
            "Phone: +1 (503) 555-0142\n"
            "Email: sales@meridiantech.example.com\n"
            "Web: www.meridiantech.example.com\n\n"
            "Regional Offices:\n"
            "  London  |  Singapore  |  Sydney  |  Toronto\n\n"
            "Follow us on LinkedIn and Twitter @MeridianTech"
        ),
        "footer": "Page 8 of 8",
        "color": (0.0, 0.2, 0.5),  # dark blue (matches cover)
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
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    for i, page_info in enumerate(PAGE_CONTENT):
        page = doc.new_page(width=595, height=842)  # A4

        color = page_info["color"]

        # Draw header bar
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(0, 0, 595, 80))
        shape.finish(color=color, fill=color)
        shape.commit()

        # Title in white on header bar
        page.insert_text(
            pymupdf.Point(50, 45),
            page_info["title"],
            fontsize=24,
            fontname="hebo",
            color=(1, 1, 1),
        )

        # Subtitle
        page.insert_text(
            pymupdf.Point(50, 70),
            page_info["subtitle"],
            fontsize=12,
            fontname="heit",
            color=(0.9, 0.9, 0.9),
        )

        # Body text in a textbox for auto-wrapping
        body_rect = pymupdf.Rect(50, 110, 545, 780)
        page.insert_textbox(
            body_rect,
            page_info["body"],
            fontsize=12,
            fontname="helv",
            color=(0.1, 0.1, 0.1),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Footer line
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(50, 810), pymupdf.Point(545, 810))
        shape2.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape2.commit()

        # Footer text
        page.insert_text(
            pymupdf.Point(50, 828),
            page_info["footer"],
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Page identifier watermark (subtle, for verification)
        page.insert_text(
            pymupdf.Point(480, 828),
            f"BRO-2025-{i+1:03d}",
            fontsize=7,
            fontname="cour",
            color=(0.7, 0.7, 0.7),
        )

    # Set metadata
    doc.set_metadata({
        "title": "Meridian Technologies - Annual Product Catalog 2025",
        "author": "Meridian Technologies Marketing",
        "subject": "Product Catalog",
        "keywords": "cloud, analytics, cybersecurity, enterprise",
    })

    # Add table of contents
    toc = [
        [1, "Cover", 1],
        [1, "About Us", 2],
        [1, "Cloud Infrastructure", 3],
        [1, "Data Analytics Suite", 4],
        [1, "Cybersecurity Solutions", 5],
        [1, "Customer Success Stories", 6],
        [1, "Pricing & Plans", 7],
        [1, "Contact Us", 8],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
