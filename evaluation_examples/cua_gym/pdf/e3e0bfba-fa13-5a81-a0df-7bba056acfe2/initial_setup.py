"""
Initial Setup: Create a password-protected 10-page PDF report
Task ID: pdf_fm_065
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_065'
OUTPUT_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{OUTPUT_DIR}/locked_report.pdf'


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
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Ensure qpdf is installed (task requirement)
    subprocess.run(
        'echo "password" | sudo -S apt-get install -y qpdf',
        shell=True, capture_output=True
    )

    import pymupdf

    doc = pymupdf.open()

    # --- Page content data for a 10-page business report ---
    pages_content = [
        {
            "title": "Meridian Technologies Inc.",
            "subtitle": "Annual Performance Report - Fiscal Year 2025",
            "body": (
                "Prepared by the Office of Strategic Planning\n"
                "Confidential - Internal Distribution Only\n\n"
                "Date of Publication: March 15, 2025\n"
                "Document Reference: MTI-APR-2025-0042"
            ),
        },
        {
            "title": "Executive Summary",
            "body": (
                "Meridian Technologies achieved record revenue of $127.4 million in FY2025, "
                "representing a 14.2% year-over-year increase. Our cloud infrastructure division "
                "led growth with $58.3 million in revenue, while the cybersecurity services unit "
                "contributed $41.7 million. The enterprise solutions segment generated $27.4 million.\n\n"
                "Operating margins improved to 18.6%, up from 15.3% in the prior fiscal year. "
                "This improvement was driven by operational efficiencies in our data center operations "
                "and the successful migration of 340 enterprise clients to our managed services platform.\n\n"
                "Headcount grew from 1,245 to 1,512 employees, with the majority of new hires "
                "concentrated in engineering (142 positions) and customer success (78 positions). "
                "Employee retention rate remained strong at 91.4%."
            ),
        },
        {
            "title": "Revenue Breakdown by Division",
            "body": (
                "Cloud Infrastructure Services:\n"
                "  Q1: $12.8M  |  Q2: $14.1M  |  Q3: $15.2M  |  Q4: $16.2M  |  Total: $58.3M\n\n"
                "Cybersecurity Services:\n"
                "  Q1: $9.4M   |  Q2: $10.1M  |  Q3: $10.8M  |  Q4: $11.4M  |  Total: $41.7M\n\n"
                "Enterprise Solutions:\n"
                "  Q1: $6.2M   |  Q2: $6.5M   |  Q3: $7.1M   |  Q4: $7.6M   |  Total: $27.4M\n\n"
                "Total Company Revenue:\n"
                "  Q1: $28.4M  |  Q2: $30.7M  |  Q3: $33.1M  |  Q4: $35.2M  |  Total: $127.4M\n\n"
                "Year-over-year growth was consistent across all divisions, with cloud infrastructure "
                "showing the strongest momentum at 19.8% growth."
            ),
        },
        {
            "title": "Operating Expenses Analysis",
            "body": (
                "Total operating expenses for FY2025 were $103.7 million, broken down as follows:\n\n"
                "Personnel Costs: $62.4M (60.2% of OpEx)\n"
                "  - Salaries and wages: $48.2M\n"
                "  - Benefits and insurance: $9.8M\n"
                "  - Stock-based compensation: $4.4M\n\n"
                "Technology Infrastructure: $21.3M (20.5% of OpEx)\n"
                "  - Data center operations: $12.1M\n"
                "  - Software licenses: $5.4M\n"
                "  - Hardware depreciation: $3.8M\n\n"
                "Sales and Marketing: $12.8M (12.3% of OpEx)\n"
                "  - Digital marketing: $4.2M\n"
                "  - Sales team compensation: $6.1M\n"
                "  - Events and conferences: $2.5M\n\n"
                "General and Administrative: $7.2M (6.9% of OpEx)"
            ),
        },
        {
            "title": "Client Portfolio Overview",
            "body": (
                "As of December 31, 2025, Meridian Technologies serves 1,847 active clients "
                "across 14 industry verticals.\n\n"
                "Top Clients by Annual Contract Value:\n"
                "  1. Northstar Financial Group - $4.2M\n"
                "  2. Pacific Healthcare Systems - $3.8M\n"
                "  3. Atlas Manufacturing Corp - $3.1M\n"
                "  4. Vertex Telecommunications - $2.9M\n"
                "  5. Pinnacle Retail Holdings - $2.6M\n\n"
                "Client Concentration:\n"
                "  - Top 10 clients: 22.4% of total revenue\n"
                "  - Top 50 clients: 48.7% of total revenue\n"
                "  - Remaining clients: 51.3% of total revenue\n\n"
                "Net Promoter Score improved from 62 to 71, reflecting enhanced service delivery "
                "and the launch of our 24/7 premium support tier."
            ),
        },
        {
            "title": "Technology and Innovation",
            "body": (
                "R&D Investment: $14.8 million (11.6% of revenue)\n\n"
                "Key Initiatives Completed in FY2025:\n\n"
                "1. Project Aurora - Next-generation cloud orchestration platform\n"
                "   Status: Launched Q3 2025 | 127 enterprise clients migrated\n"
                "   Impact: 34% reduction in deployment time, 22% cost savings\n\n"
                "2. CyberShield 3.0 - AI-powered threat detection\n"
                "   Status: GA release Q2 2025 | 89 clients deployed\n"
                "   Impact: 47% improvement in threat detection speed\n\n"
                "3. DataBridge Integration Suite\n"
                "   Status: Beta Q4 2025 | 15 pilot clients\n"
                "   Impact: Seamless cross-platform data synchronization\n\n"
                "Patent filings: 12 new patents filed, 8 granted during FY2025."
            ),
        },
        {
            "title": "Human Resources and Culture",
            "body": (
                "Workforce Demographics (as of Dec 31, 2025):\n"
                "  Total employees: 1,512\n"
                "  Engineering: 624 (41.3%)\n"
                "  Customer Success: 298 (19.7%)\n"
                "  Sales and Marketing: 214 (14.2%)\n"
                "  Operations: 187 (12.4%)\n"
                "  General & Administrative: 189 (12.5%)\n\n"
                "Diversity Metrics:\n"
                "  Women in leadership: 38.4% (up from 34.1%)\n"
                "  Underrepresented groups: 31.2% (up from 28.7%)\n\n"
                "Employee Satisfaction Survey Results:\n"
                "  Overall satisfaction: 4.2/5.0\n"
                "  Work-life balance: 4.0/5.0\n"
                "  Career development: 3.9/5.0\n"
                "  Compensation fairness: 3.8/5.0\n\n"
                "Training investment per employee: $2,840 (industry avg: $1,950)"
            ),
        },
        {
            "title": "Risk Assessment and Mitigation",
            "body": (
                "Key Risk Categories and Mitigation Strategies:\n\n"
                "1. Cybersecurity Threats (Severity: High)\n"
                "   - Implemented zero-trust architecture across all internal systems\n"
                "   - Conducted 4 red team exercises with external auditors\n"
                "   - Achieved SOC 2 Type II and ISO 27001 recertification\n\n"
                "2. Talent Acquisition Competition (Severity: Medium-High)\n"
                "   - Enhanced equity compensation packages for senior engineers\n"
                "   - Launched remote-first hiring policy for 60% of positions\n"
                "   - Established university partnership program with 8 institutions\n\n"
                "3. Regulatory Compliance (Severity: Medium)\n"
                "   - Dedicated compliance team expanded to 14 specialists\n"
                "   - Automated compliance monitoring for GDPR, CCPA, HIPAA\n"
                "   - Zero regulatory violations or fines in FY2025\n\n"
                "4. Supply Chain Dependencies (Severity: Medium)\n"
                "   - Diversified cloud provider relationships (AWS, Azure, GCP)\n"
                "   - Maintained 99.97% uptime across all service tiers"
            ),
        },
        {
            "title": "Strategic Outlook - FY2026",
            "body": (
                "Revenue Target: $152 million (19.3% growth)\n"
                "Operating Margin Target: 20.5%\n"
                "Headcount Plan: 1,750 employees\n\n"
                "Strategic Priorities:\n\n"
                "1. International Expansion\n"
                "   - Open European headquarters in Dublin, Ireland (Q2 2026)\n"
                "   - Target 15% of revenue from international markets by Q4 2026\n"
                "   - Hire regional sales teams in UK, Germany, and Netherlands\n\n"
                "2. AI-First Product Strategy\n"
                "   - Integrate generative AI across all product lines\n"
                "   - Launch AI Operations Center for automated incident response\n"
                "   - R&D budget increase to $19.5M (12.8% of projected revenue)\n\n"
                "3. Strategic Acquisitions\n"
                "   - $40M acquisition budget approved by Board\n"
                "   - Focus areas: edge computing, IoT security, compliance automation\n"
                "   - Due diligence active on 3 target companies\n\n"
                "4. Customer Experience Enhancement\n"
                "   - Launch self-service portal 2.0\n"
                "   - Reduce average ticket resolution time by 25%\n"
                "   - Achieve NPS score of 75+"
            ),
        },
        {
            "title": "Appendix and Legal Disclosures",
            "body": (
                "This document contains forward-looking statements that involve risks and "
                "uncertainties. Actual results may differ materially from those projected.\n\n"
                "Financial figures have been prepared in accordance with Generally Accepted "
                "Accounting Principles (GAAP) and reviewed by Deloitte & Touche LLP.\n\n"
                "Contact Information:\n"
                "  Meridian Technologies Inc.\n"
                "  1200 Innovation Drive, Suite 400\n"
                "  San Jose, CA 95134\n"
                "  Tel: (408) 555-0142\n"
                "  Email: investor.relations@meridiantech.com\n"
                "  Web: www.meridiantech.com\n\n"
                "Board of Directors:\n"
                "  - Dr. Elena Vasquez, Chairperson\n"
                "  - Robert Nakamura, CEO\n"
                "  - Sarah Mitchell, CFO\n"
                "  - James Okonkwo, CTO\n"
                "  - Lisa Brennan, Independent Director\n"
                "  - David Patel, Independent Director\n\n"
                "Document Classification: Confidential\n"
                "Distribution: Internal stakeholders and Board members only\n"
                "Copyright 2025 Meridian Technologies Inc. All rights reserved."
            ),
        },
    ]

    # Create 10 pages of content
    for i, page_data in enumerate(pages_content):
        page = doc.new_page(width=612, height=792)  # Letter size

        # Title
        if i == 0:
            # Cover page
            page.insert_text(
                pymupdf.Point(72, 280),
                page_data["title"],
                fontsize=28,
                fontname="hebo",
                color=(0.0, 0.2, 0.4),
            )
            page.insert_text(
                pymupdf.Point(72, 320),
                page_data["subtitle"],
                fontsize=16,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
            )
            # Body text
            rect = pymupdf.Rect(72, 380, 540, 700)
            page.insert_textbox(
                rect,
                page_data["body"],
                fontsize=12,
                fontname="helv",
                color=(0.2, 0.2, 0.2),
            )
            # Draw a decorative line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 340), pymupdf.Point(540, 340))
            shape.finish(color=(0.0, 0.2, 0.4), width=2)
            shape.commit()
        else:
            # Regular page
            page.insert_text(
                pymupdf.Point(72, 60),
                page_data["title"],
                fontsize=20,
                fontname="hebo",
                color=(0.0, 0.2, 0.4),
            )
            # Underline below title
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 68), pymupdf.Point(540, 68))
            shape.finish(color=(0.0, 0.2, 0.4), width=1)
            shape.commit()

            # Body text
            rect = pymupdf.Rect(72, 90, 540, 740)
            page.insert_textbox(
                rect,
                page_data["body"],
                fontsize=11,
                fontname="helv",
                color=(0.1, 0.1, 0.1),
            )

            # Page number
            page.insert_text(
                pymupdf.Point(290, 770),
                f"Page {i + 1}",
                fontsize=9,
                fontname="helv",
                color=(0.5, 0.5, 0.5),
            )

    # Set metadata
    doc.set_metadata({
        "title": "Annual Performance Report - Fiscal Year 2025",
        "author": "Meridian Technologies Inc.",
        "subject": "Annual Report",
        "keywords": "annual report, financial, performance, FY2025",
        "creator": "Meridian Technologies",
        "producer": "Internal Document System",
    })

    # Set table of contents
    toc = [
        [1, "Executive Summary", 2],
        [1, "Revenue Breakdown by Division", 3],
        [1, "Operating Expenses Analysis", 4],
        [1, "Client Portfolio Overview", 5],
        [1, "Technology and Innovation", 6],
        [1, "Human Resources and Culture", 7],
        [1, "Risk Assessment and Mitigation", 8],
        [1, "Strategic Outlook - FY2026", 9],
        [1, "Appendix and Legal Disclosures", 10],
    ]
    doc.set_toc(toc)

    # Save unencrypted first
    temp_path = f'{OUTPUT_DIR}/_temp_report.pdf'
    doc.save(temp_path)
    doc.close()

    # Now encrypt with pikepdf
    import pikepdf
    pdf = pikepdf.open(temp_path)
    pdf.save(
        OUTPUT,
        encryption=pikepdf.Encryption(
            owner="OldPass123",
            user="OldPass123",
            R=4,
            allow=pikepdf.Permissions(
                extract=True,
                modify_annotation=True,
                print_lowres=True,
                print_highres=True,
                modify_form=True,
                modify_other=True,
                modify_assembly=True,
            ),
        ),
    )
    pdf.close()
    os.remove(temp_path)
    print(f'Initial file created: {OUTPUT}')

    # Open a terminal so the user can use qpdf
    launch_gui('bash -c "cd /home/user/Documents && exec bash"', delay_sec=1.0)
    # Also open the file manager to Documents
    launch_gui('nautilus "/home/user/Documents"', delay_sec=2.0)
    print('GUI_READY: launched required app(s) with DISPLAY=:0')


create_initial()
