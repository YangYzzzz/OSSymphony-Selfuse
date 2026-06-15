"""
Initial Setup: Create a 10-page web report PDF with ~25 hyperlinks
Task ID: pdf_ro_042
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_042'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/web_report.pdf'


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

    # Remove links.txt if it exists - agent must create it
    links_path = f'{DOCS_DIR}/links.txt'
    if os.path.exists(links_path):
        os.remove(links_path)

    doc = pymupdf.open()

    # Page dimensions
    W, H = 595, 842  # A4

    # Define hyperlinks across 10 pages - mix of visible text links and URI annotations
    # Each entry: (page_index, link_text, url, y_position)
    page_contents = [
        {
            "title": "Meridian Technologies - Annual Web Presence Report 2025",
            "subtitle": "Prepared by the Digital Strategy Division",
            "body": (
                "This report provides a comprehensive overview of Meridian Technologies' "
                "online presence, including key partnerships, technology resources, and "
                "digital infrastructure utilized throughout the fiscal year 2025."
            ),
            "links": [
                ("Company Homepage", "https://www.meridiantech.com"),
                ("Investor Relations Portal", "https://investors.meridiantech.com/annual-report"),
                ("Industry Overview - Gartner", "https://www.gartner.com/en/information-technology"),
            ],
        },
        {
            "title": "Chapter 1: Cloud Infrastructure",
            "body": (
                "Meridian's cloud infrastructure continues to leverage multiple providers "
                "for resilience and performance. Our primary workloads run across three "
                "major platforms, with disaster recovery handled through geographic distribution."
            ),
            "links": [
                ("AWS Documentation", "https://docs.aws.amazon.com/cloud-infrastructure"),
                ("Google Cloud Platform", "https://cloud.google.com/solutions/enterprise"),
                ("Microsoft Azure Portal", "https://portal.azure.com/meridian-workspace"),
            ],
        },
        {
            "title": "Chapter 2: Development Tools and Repositories",
            "body": (
                "Our engineering teams rely on a standardized set of development tools "
                "and version control practices. All repositories are hosted on enterprise "
                "GitHub with automated CI/CD pipelines for every project."
            ),
            "links": [
                ("GitHub Enterprise", "https://github.com/meridian-technologies"),
                ("CI/CD Pipeline Dashboard", "https://jenkins.meridiantech.com/dashboard"),
                ("Internal Wiki", "https://confluence.meridiantech.com/engineering"),
            ],
        },
        {
            "title": "Chapter 3: Analytics and Monitoring",
            "body": (
                "Real-time monitoring and analytics form the backbone of our operational "
                "visibility. The following platforms are integral to detecting performance "
                "anomalies and understanding user behavior across our digital properties."
            ),
            "links": [
                ("Google Analytics Dashboard", "https://analytics.google.com/meridian-main"),
                ("Datadog Monitoring", "https://app.datadoghq.com/meridian/overview"),
            ],
        },
        {
            "title": "Chapter 4: Security and Compliance",
            "body": (
                "Security remains a top priority for Meridian Technologies. Our compliance "
                "framework adheres to SOC 2 Type II, ISO 27001, and GDPR standards. Regular "
                "audits and penetration testing ensure our defenses stay current."
            ),
            "links": [
                ("NIST Cybersecurity Framework", "https://www.nist.gov/cyberframework"),
                ("OWASP Top Ten", "https://owasp.org/www-project-top-ten/"),
                ("Compliance Dashboard", "https://security.meridiantech.com/compliance"),
            ],
        },
        {
            "title": "Chapter 5: Partner Ecosystem",
            "body": (
                "Meridian's partner ecosystem spans technology vendors, consulting firms, "
                "and academic institutions. These partnerships drive innovation and provide "
                "access to cutting-edge research and development capabilities."
            ),
            "links": [
                ("Salesforce AppExchange", "https://appexchange.salesforce.com/meridian"),
                ("Partner Portal", "https://partners.meridiantech.com/login"),
            ],
        },
        {
            "title": "Chapter 6: Customer Engagement Platforms",
            "body": (
                "Our customer-facing platforms have undergone significant enhancements this "
                "year. The support portal now features AI-powered ticket routing, and the "
                "community forum has grown to over 50,000 active contributors."
            ),
            "links": [
                ("Customer Support Portal", "https://support.meridiantech.com"),
                ("Community Forum", "https://community.meridiantech.com/forums"),
                ("Knowledge Base", "https://help.meridiantech.com/articles"),
            ],
        },
        {
            "title": "Chapter 7: Marketing and Content Strategy",
            "body": (
                "Content marketing initiatives drove a 34% increase in organic traffic. "
                "Our blog and social media channels continue to serve as primary touchpoints "
                "for thought leadership and brand awareness."
            ),
            "links": [
                ("Corporate Blog", "https://blog.meridiantech.com"),
                ("LinkedIn Company Page", "https://www.linkedin.com/company/meridian-technologies"),
            ],
        },
        {
            "title": "Chapter 8: Research and Development",
            "body": (
                "R&D efforts this year focused on machine learning operations, quantum-safe "
                "cryptography, and sustainable computing practices. Three patents were filed "
                "and two major open-source projects were released."
            ),
            "links": [
                ("R&D Publication Archive", "https://research.meridiantech.com/publications"),
                ("Open Source Projects", "https://opensource.meridiantech.com"),
            ],
        },
        {
            "title": "Appendix: Reference Links and Resources",
            "body": (
                "The following resources provide additional context and supporting "
                "documentation referenced throughout this report. Please contact the "
                "Digital Strategy team for access credentials where required."
            ),
            "links": [
                ("Annual Report PDF Archive", "https://docs.meridiantech.com/reports/2025"),
                ("API Documentation", "https://api.meridiantech.com/v2/docs"),
                ("Status Page", "https://status.meridiantech.com"),
            ],
        },
    ]

    for page_idx, page_data in enumerate(page_contents):
        page = doc.new_page(width=W, height=H)

        y = 60

        # Page number at top right
        page.insert_text(
            pymupdf.Point(W - 80, 30),
            f"Page {page_idx + 1}",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Title
        if page_idx == 0:
            fontsize = 18
        else:
            fontsize = 16
        page.insert_text(
            pymupdf.Point(72, y),
            page_data["title"],
            fontsize=fontsize,
            fontname="hebo",
            color=(0.1, 0.1, 0.4),
        )
        y += 30

        # Subtitle (only for cover page)
        if "subtitle" in page_data:
            page.insert_text(
                pymupdf.Point(72, y),
                page_data["subtitle"],
                fontsize=12,
                fontname="heit",
                color=(0.3, 0.3, 0.3),
            )
            y += 25

        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(W - 72, y))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()
        y += 20

        # Body text
        body_rect = pymupdf.Rect(72, y, W - 72, y + 100)
        page.insert_textbox(
            body_rect,
            page_data["body"],
            fontsize=11,
            fontname="helv",
            color=(0.15, 0.15, 0.15),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )
        y += 110

        # Section label for links
        page.insert_text(
            pymupdf.Point(72, y),
            "Related Resources:",
            fontsize=11,
            fontname="hebo",
            color=(0.2, 0.2, 0.2),
        )
        y += 20

        # Insert links as blue underlined text with URI annotations
        for link_text, url in page_data["links"]:
            # Draw link text in blue
            display_text = f"{link_text}"
            page.insert_text(
                pymupdf.Point(90, y),
                display_text,
                fontsize=10,
                fontname="helv",
                color=(0.0, 0.2, 0.8),
            )

            # Calculate approximate text width for link rect
            text_width = len(display_text) * 6.2  # approximate (generous to capture full text)
            link_rect = pymupdf.Rect(90, y - 10, 90 + text_width, y + 3)

            # Add URI link annotation
            page.insert_link({
                "kind": pymupdf.LINK_URI,
                "from": link_rect,
                "uri": url,
            })

            # Add underline decoration
            shape2 = page.new_shape()
            shape2.draw_line(pymupdf.Point(90, y + 2), pymupdf.Point(90 + text_width, y + 2))
            shape2.finish(color=(0.0, 0.2, 0.8), width=0.5)
            shape2.commit()

            y += 18

        # Footer line
        footer_y = H - 40
        shape3 = page.new_shape()
        shape3.draw_line(pymupdf.Point(72, footer_y), pymupdf.Point(W - 72, footer_y))
        shape3.finish(color=(0.8, 0.8, 0.8), width=0.3)
        shape3.commit()

        page.insert_text(
            pymupdf.Point(72, footer_y + 15),
            "Meridian Technologies - Confidential",
            fontsize=8,
            fontname="heit",
            color=(0.6, 0.6, 0.6),
        )

    # Set document metadata
    doc.set_metadata({
        "title": "Meridian Technologies - Annual Web Presence Report 2025",
        "author": "Digital Strategy Division",
        "subject": "Web Presence Analysis",
        "keywords": "web, report, hyperlinks, infrastructure, analytics",
        "creator": "Meridian Report Generator",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify link count
    verify_doc = pymupdf.open(OUTPUT)
    total_links = 0
    for p in verify_doc:
        total_links += len(p.get_links())
    verify_doc.close()
    print(f'Total hyperlinks in PDF: {total_links}')

    # Launch Evince to display the PDF
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
