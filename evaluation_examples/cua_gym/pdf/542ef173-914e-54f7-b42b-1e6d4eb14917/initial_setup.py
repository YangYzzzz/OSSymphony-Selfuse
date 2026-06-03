"""
Initial Setup: Create 5 source PDF documents in /home/user/archive/docs/
Task ID: pdf_pw_050
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_050'
ARCHIVE_DIR = f'{WORKDIR}/archive'
DOCS_DIR = f'{ARCHIVE_DIR}/docs'


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


def create_report(filepath, title, author, content_pages):
    """Create a realistic multi-page PDF report with metadata."""
    doc = pymupdf.open()

    for page_num, page_content in enumerate(content_pages):
        page = doc.new_page(width=595, height=842)  # A4

        # Header bar
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(0, 0, 595, 60))
        shape.finish(fill=(0.15, 0.25, 0.45), color=(0.15, 0.25, 0.45))
        shape.commit()

        # Title in header (white text)
        page.insert_text(
            pymupdf.Point(40, 40),
            title,
            fontsize=18,
            fontname="hebo",
            color=(1, 1, 1),
        )

        # Page number
        page.insert_text(
            pymupdf.Point(500, 40),
            f"Page {page_num + 1}",
            fontsize=10,
            fontname="helv",
            color=(1, 1, 1),
        )

        # Section heading
        y = 100
        page.insert_text(
            pymupdf.Point(50, y),
            page_content["heading"],
            fontsize=14,
            fontname="hebo",
            color=(0.15, 0.25, 0.45),
        )
        y += 30

        # Body text
        rect = pymupdf.Rect(50, y, 545, 780)
        page.insert_textbox(
            rect,
            page_content["body"],
            fontsize=11,
            fontname="helv",
            color=(0.1, 0.1, 0.1),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Footer line
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(50, 800), pymupdf.Point(545, 800))
        shape2.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape2.commit()

        page.insert_text(
            pymupdf.Point(50, 820),
            f"{title} | Confidential",
            fontsize=8,
            fontname="heit",
            color=(0.5, 0.5, 0.5),
        )

    doc.set_metadata({
        "title": title,
        "author": author,
        "subject": f"Report: {title}",
        "creator": "CUA-Gym Document System",
    })

    doc.save(filepath)
    doc.close()
    print(f"Created: {filepath}")


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Report A: Financial Performance
    create_report(
        f"{DOCS_DIR}/report_a.pdf",
        "Q4 2025 Financial Performance Review",
        "Elena Martinez",
        [
            {
                "heading": "Executive Summary",
                "body": (
                    "The fourth quarter of 2025 demonstrated strong financial performance across all business units. "
                    "Total revenue reached $48.7 million, representing a 12.3% year-over-year increase. Operating margins "
                    "improved to 23.4%, driven by cost optimization initiatives and higher-margin product mix. The enterprise "
                    "software division led growth with $22.1 million in bookings, while professional services contributed "
                    "$15.3 million. Cash flow from operations was $11.2 million, and free cash flow reached $8.9 million "
                    "after capital expenditures of $2.3 million. Headcount grew to 342 full-time employees, a net addition "
                    "of 28 positions focused primarily in engineering and customer success teams."
                ),
            },
            {
                "heading": "Revenue Breakdown by Segment",
                "body": (
                    "Enterprise Software: $22.1M (45.4%) - Growth driven by new client acquisitions in healthcare and "
                    "financial services verticals. Average deal size increased 18% to $245,000. Professional Services: "
                    "$15.3M (31.4%) - Implementation revenue grew alongside software bookings, with utilization rates "
                    "at 82%. Managed Services: $8.2M (16.8%) - Recurring revenue base expanded with 96% renewal rate. "
                    "Training & Certification: $3.1M (6.4%) - Online training platform saw 34% growth in enrollments."
                ),
            },
            {
                "heading": "Outlook for Q1 2026",
                "body": (
                    "Pipeline visibility remains strong heading into Q1 2026 with $67.3 million in qualified opportunities. "
                    "We anticipate revenue in the range of $50-52 million, supported by three enterprise deals expected to "
                    "close by mid-February. Key risks include potential budget freezes at two major accounts and currency "
                    "headwinds in EMEA markets. Strategic priorities include launching the AI-powered analytics module and "
                    "expanding the partner ecosystem with three new channel partners in Asia-Pacific."
                ),
            },
        ],
    )

    # Report B: Technology Infrastructure
    create_report(
        f"{DOCS_DIR}/report_b.pdf",
        "Infrastructure Modernization Progress Report",
        "David Park",
        [
            {
                "heading": "Cloud Migration Status",
                "body": (
                    "Phase 2 of the cloud migration initiative is now 78% complete, with 142 of 182 workloads "
                    "successfully transitioned to AWS. The remaining 40 workloads, primarily legacy Java applications "
                    "running on WebSphere, are scheduled for migration in Q1 2026. Key achievements this quarter include "
                    "containerizing 35 microservices using Kubernetes, achieving 99.97% uptime across production environments, "
                    "and reducing monthly cloud spend by $18,400 through right-sizing and reserved instance optimization. "
                    "The zero-trust security framework deployment reached 89% coverage with Okta SSO integration completed "
                    "for all Tier 1 applications."
                ),
            },
            {
                "heading": "Performance Metrics",
                "body": (
                    "Average API response time decreased from 340ms to 125ms following the CDN deployment and database "
                    "query optimization sprint. Database query performance improved by 45% after index restructuring on "
                    "the primary PostgreSQL clusters. Peak concurrent user capacity increased to 12,000 from 7,500 through "
                    "horizontal scaling implementations. Disaster recovery testing completed successfully with 4-hour RPO "
                    "and 2-hour RTO achieved, meeting our SLA commitments to enterprise clients."
                ),
            },
        ],
    )

    # Report C: Human Resources
    create_report(
        f"{DOCS_DIR}/report_c.pdf",
        "Annual Workforce Analytics Report 2025",
        "Rachel Thompson",
        [
            {
                "heading": "Workforce Composition Overview",
                "body": (
                    "As of December 31, 2025, the organization employs 342 full-time equivalents across 6 departments "
                    "and 4 geographic regions. Engineering remains the largest department with 128 employees (37.4%), "
                    "followed by Sales & Marketing with 76 (22.2%), Professional Services with 54 (15.8%), Customer "
                    "Success with 38 (11.1%), G&A with 28 (8.2%), and Product Management with 18 (5.3%). Gender diversity "
                    "improved to 41% female representation, up from 37% in 2024. The voluntary turnover rate decreased "
                    "to 11.2% from 14.8%, below the industry benchmark of 15.3%."
                ),
            },
            {
                "heading": "Talent Acquisition Metrics",
                "body": (
                    "The talent acquisition team processed 4,230 applications and extended 156 offers throughout 2025, "
                    "maintaining an offer acceptance rate of 87.2%. Average time-to-fill decreased to 34 days from 42 days "
                    "in 2024, driven by improvements in the screening process and employer branding initiatives. The "
                    "employee referral program generated 31% of all hires, with referred candidates showing 23% higher "
                    "retention rates. Total recruitment spend was $892,000, yielding a cost-per-hire of $5,718."
                ),
            },
            {
                "heading": "Learning and Development",
                "body": (
                    "Total training investment reached $1.34 million in 2025, averaging $3,918 per employee. The "
                    "internal learning management system recorded 8,940 course completions across 127 programs. "
                    "Technical skills development accounted for 58% of training hours, with leadership development "
                    "at 24% and compliance training at 18%. Employee satisfaction with L&D opportunities scored 4.2 "
                    "out of 5.0 in the annual engagement survey, a significant improvement from 3.6 in 2024."
                ),
            },
        ],
    )

    # Report D: Product Development
    create_report(
        f"{DOCS_DIR}/report_d.pdf",
        "Product Development Roadmap Review",
        "James Liu",
        [
            {
                "heading": "Release Highlights - Version 8.3",
                "body": (
                    "Version 8.3 shipped on November 15, 2025, delivering 47 new features and resolving 183 defects. "
                    "The headline feature, AI-powered anomaly detection, leverages a proprietary machine learning pipeline "
                    "trained on 2.1 billion data points. Beta testing with 23 enterprise customers showed a 94% accuracy "
                    "rate in detecting operational anomalies, with average alert latency under 45 seconds. Additional "
                    "features include advanced role-based access controls, a redesigned reporting dashboard, and native "
                    "integration with ServiceNow, Jira, and PagerDuty. Customer adoption of v8.3 reached 62% within "
                    "the first 30 days, the fastest in company history."
                ),
            },
            {
                "heading": "Q1 2026 Development Priorities",
                "body": (
                    "Sprint planning for Q1 2026 focuses on three strategic initiatives. First, the multi-tenant "
                    "architecture overhaul will enable per-customer resource isolation and independent scaling, targeting "
                    "FedRAMP compliance by mid-2026. Second, the GraphQL API layer will replace the existing REST endpoints "
                    "for complex data queries, reducing average payload size by 60%. Third, the mobile companion app "
                    "for iOS and Android is targeted for closed beta in March 2026, starting with read-only dashboards "
                    "and alert management capabilities."
                ),
            },
        ],
    )

    # Report E: Market Analysis
    create_report(
        f"{DOCS_DIR}/report_e.pdf",
        "Competitive Market Analysis - Enterprise SaaS",
        "Sarah Nakamura",
        [
            {
                "heading": "Market Overview",
                "body": (
                    "The enterprise SaaS observability market is projected to reach $42.8 billion by 2027, growing at "
                    "a CAGR of 14.2%. The market is consolidating around three primary players: Datadog (26% share), "
                    "Splunk/Cisco (19% share), and New Relic (11% share). Mid-market challengers including our platform "
                    "collectively hold 18% share and are growing faster than incumbents. Key trends driving adoption "
                    "include cloud-native architectures, AI/ML-powered analytics, and regulatory compliance requirements "
                    "in financial services and healthcare verticals."
                ),
            },
            {
                "heading": "Competitive Positioning Analysis",
                "body": (
                    "Our platform differentiates on three dimensions: deployment flexibility (hybrid cloud support), "
                    "cost predictability (usage-based pricing without overages), and implementation speed (average 14-day "
                    "time-to-value vs. 60+ days for incumbent solutions). Win/loss analysis from 127 competitive deals "
                    "in 2025 shows a 58% win rate overall, with strongest performance in healthcare (72% win rate) and "
                    "manufacturing (65% win rate). Primary loss drivers include brand recognition gaps (34% of losses) "
                    "and feature parity concerns in advanced APM capabilities (28% of losses)."
                ),
            },
            {
                "heading": "Strategic Recommendations",
                "body": (
                    "Based on market analysis, three strategic imperatives emerge for 2026. First, accelerate AI/ML "
                    "feature development to close the capability gap with Datadog's AI-powered features. Second, invest "
                    "in brand awareness through analyst relations, conference sponsorships, and customer case studies to "
                    "address the recognition gap. Third, expand vertical-specific solutions for healthcare and financial "
                    "services to capitalize on regulatory-driven demand and our strong competitive position in these segments."
                ),
            },
        ],
    )

    # Verify
    for fname in ['report_a.pdf', 'report_b.pdf', 'report_c.pdf', 'report_d.pdf', 'report_e.pdf']:
        fpath = f"{DOCS_DIR}/{fname}"
        if os.path.exists(fpath):
            doc = pymupdf.open(fpath)
            meta = doc.metadata
            print(f"  {fname}: {doc.page_count} pages, title='{meta.get('title', '')}'")
            doc.close()
        else:
            print(f"  ERROR: {fname} not found!")

    # No master_index.pdf should exist yet
    index_path = f"{ARCHIVE_DIR}/master_index.pdf"
    if os.path.exists(index_path):
        os.remove(index_path)
        print("Removed pre-existing master_index.pdf")

    # GUI-ready: open file manager to show the archive directory
    launch_gui(f'nautilus "{ARCHIVE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
