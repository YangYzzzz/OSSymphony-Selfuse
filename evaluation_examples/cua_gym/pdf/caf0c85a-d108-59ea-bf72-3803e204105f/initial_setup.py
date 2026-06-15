"""
Initial Setup: Create header_page.pdf, footer_page.pdf, and 3 PDFs in wrap_batch/ for PDF merging task.
Task ID: pdf_adv_182
Domain: pdf

Initial state:
  ~/Documents/header_page.pdf  — 1 page (company header/letterhead)
  ~/Documents/footer_page.pdf  — 1 page (disclaimer/signature footer)
  ~/Documents/wrap_batch/
    doc1.pdf  — 4 pages (project proposal content)
    doc2.pdf  — 6 pages (quarterly report content)
    doc3.pdf  — 3 pages (meeting minutes content)
  ~/Documents/wrap_batch/wrapped/  — does NOT yet exist (agent must create it)

The task requires the agent to merge header + doc + footer for each of the 3 docs
and save results in wrapped/.
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

DOCUMENTS_DIR = '/home/user/Documents'
WRAP_BATCH_DIR = '/home/user/Documents/wrap_batch'
HEADER_PDF = '/home/user/Documents/header_page.pdf'
FOOTER_PDF = '/home/user/Documents/footer_page.pdf'


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


def create_header_pdf():
    """Create header_page.pdf — a professional company letterhead (1 page)."""
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)  # A4

    shape = page.new_shape()

    # Header background band
    shape.draw_rect(pymupdf.Rect(0, 0, 595, 100))
    shape.finish(color=(0.13, 0.29, 0.53), fill=(0.13, 0.29, 0.53), width=0)

    # Bottom border line
    shape.draw_line(pymupdf.Point(0, 100), pymupdf.Point(595, 100))
    shape.finish(color=(0.8, 0.6, 0.1), width=3)

    shape.commit()

    # Company name
    page.insert_text(
        pymupdf.Point(50, 55),
        "MERIDIAN CONSULTING GROUP",
        fontsize=22,
        fontname="hebo",
        color=(1, 1, 1),
    )

    # Tagline
    page.insert_text(
        pymupdf.Point(50, 80),
        "Strategic Solutions · Business Excellence · Innovation",
        fontsize=10,
        fontname="heit",
        color=(0.85, 0.90, 0.95),
    )

    # Contact info on right
    page.insert_text(
        pymupdf.Point(400, 45),
        "www.meridiancg.com",
        fontsize=9,
        fontname="helv",
        color=(0.85, 0.90, 0.95),
    )
    page.insert_text(
        pymupdf.Point(400, 62),
        "info@meridiancg.com",
        fontsize=9,
        fontname="helv",
        color=(0.85, 0.90, 0.95),
    )
    page.insert_text(
        pymupdf.Point(400, 79),
        "+1 (800) 555-0190",
        fontsize=9,
        fontname="helv",
        color=(0.85, 0.90, 0.95),
    )

    # Instruction text area
    page.insert_text(
        pymupdf.Point(50, 150),
        "DOCUMENT COVER PAGE",
        fontsize=18,
        fontname="hebo",
        color=(0.13, 0.29, 0.53),
    )

    rect = pymupdf.Rect(50, 180, 545, 400)
    page.insert_textbox(
        rect,
        "This document is issued by Meridian Consulting Group and is intended solely for "
        "the use of the named recipient(s). The contents of this document are confidential "
        "and proprietary. Unauthorized use, distribution, or reproduction of this material "
        "is strictly prohibited.\n\n"
        "For inquiries regarding the contents of this document, please contact your "
        "designated account manager or reach our main office at the contact details "
        "provided above.",
        fontsize=11,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Divider
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(50, 420), pymupdf.Point(545, 420))
    shape2.finish(color=(0.13, 0.29, 0.53), width=1.5)
    shape2.commit()

    page.insert_text(
        pymupdf.Point(50, 450),
        "Document Reference Information",
        fontsize=12,
        fontname="hebo",
        color=(0.13, 0.29, 0.53),
    )

    fields = [
        ("Prepared by:", "Meridian Consulting Group"),
        ("Classification:", "Confidential — Internal Use Only"),
        ("Distribution:", "Authorized Recipients Only"),
        ("Revision:", "Final"),
    ]
    y = 480
    for label, value in fields:
        page.insert_text(pymupdf.Point(50, y), label, fontsize=10, fontname="hebo", color=(0.3, 0.3, 0.3))
        page.insert_text(pymupdf.Point(200, y), value, fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 22

    doc.save(HEADER_PDF)
    doc.close()
    print(f"Created: {HEADER_PDF} (1 page)")


def create_footer_pdf():
    """Create footer_page.pdf — a legal disclaimer / signature page (1 page)."""
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)  # A4

    shape = page.new_shape()

    # Top divider
    shape.draw_line(pymupdf.Point(50, 60), pymupdf.Point(545, 60))
    shape.finish(color=(0.13, 0.29, 0.53), width=2)

    # Footer band at bottom
    shape.draw_rect(pymupdf.Rect(0, 760, 595, 842))
    shape.finish(color=(0.13, 0.29, 0.53), fill=(0.13, 0.29, 0.53), width=0)

    shape.commit()

    page.insert_text(
        pymupdf.Point(50, 45),
        "END OF DOCUMENT — APPROVAL & SIGNATURE PAGE",
        fontsize=13,
        fontname="hebo",
        color=(0.13, 0.29, 0.53),
    )

    # Disclaimer block
    rect = pymupdf.Rect(50, 80, 545, 260)
    page.insert_textbox(
        rect,
        "LEGAL DISCLAIMER: This document and all information contained herein is provided "
        "on an 'as-is' basis. Meridian Consulting Group makes no representations or "
        "warranties of any kind, express or implied, about the completeness, accuracy, "
        "reliability, suitability, or availability with respect to the document or the "
        "information contained in the document. Any reliance you place on such information "
        "is therefore strictly at your own risk. In no event shall Meridian Consulting Group "
        "be liable for any loss or damage including without limitation, indirect or "
        "consequential loss or damage, or any loss or damage whatsoever arising from loss "
        "of data or profits arising out of, or in connection with, the use of this document.",
        fontsize=9,
        fontname="helv",
        color=(0.35, 0.35, 0.35),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Signature section
    page.insert_text(
        pymupdf.Point(50, 290),
        "AUTHORIZATION SIGNATURES",
        fontsize=12,
        fontname="hebo",
        color=(0.2, 0.2, 0.2),
    )

    sig_blocks = [
        (50, "Prepared By", "Senior Analyst"),
        (210, "Reviewed By", "Project Manager"),
        (370, "Approved By", "Managing Director"),
    ]

    for x, title, role in sig_blocks:
        page.insert_text(pymupdf.Point(x, 320), title + ":", fontsize=9, fontname="hebo", color=(0.3, 0.3, 0.3))
        # Signature line
        shape3 = page.new_shape()
        shape3.draw_line(pymupdf.Point(x, 380), pymupdf.Point(x + 140, 380))
        shape3.finish(color=(0.2, 0.2, 0.2), width=1)
        shape3.commit()
        page.insert_text(pymupdf.Point(x, 395), role, fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4))
        page.insert_text(pymupdf.Point(x, 412), "Date: ___________", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))

    # Version history table
    page.insert_text(pymupdf.Point(50, 460), "REVISION HISTORY", fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))

    headers = ["Version", "Date", "Author", "Description"]
    col_x = [50, 130, 230, 340]
    # Header row background
    shape4 = page.new_shape()
    shape4.draw_rect(pymupdf.Rect(45, 475, 550, 493))
    shape4.finish(color=(0.13, 0.29, 0.53), fill=(0.13, 0.29, 0.53), width=0)
    shape4.commit()
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(col_x[i], 489), h, fontsize=9, fontname="hebo", color=(1, 1, 1))

    rows = [
        ["1.0", "2025-01-10", "A. Roberts", "Initial draft"],
        ["1.1", "2025-02-03", "M. Chen", "Updated analysis"],
        ["2.0", "2025-03-15", "A. Roberts", "Final revision"],
    ]
    y = 510
    for ri, row in enumerate(rows):
        if ri % 2 == 0:
            shape5 = page.new_shape()
            shape5.draw_rect(pymupdf.Rect(45, y - 13, 550, y + 7))
            shape5.finish(color=None, fill=(0.94, 0.96, 0.99), width=0)
            shape5.commit()
        for i, val in enumerate(row):
            page.insert_text(pymupdf.Point(col_x[i], y), val, fontsize=9, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 22

    # Bottom footer text
    page.insert_text(
        pymupdf.Point(50, 785),
        "© 2025 Meridian Consulting Group. All Rights Reserved.  |  Confidential",
        fontsize=8,
        fontname="helv",
        color=(1, 1, 1),
    )
    page.insert_text(
        pymupdf.Point(430, 785),
        "Page — END",
        fontsize=8,
        fontname="helv",
        color=(1, 1, 1),
    )

    doc.save(FOOTER_PDF)
    doc.close()
    print(f"Created: {FOOTER_PDF} (1 page)")


def create_doc1():
    """doc1.pdf — Project Proposal: 4 pages."""
    doc = pymupdf.open()

    # Page 1: Title page
    page = doc.new_page(width=595, height=842)
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, 595, 842))
    shape.finish(color=(0.97, 0.97, 0.99), fill=(0.97, 0.97, 0.99), width=0)
    shape.draw_rect(pymupdf.Rect(0, 320, 595, 500))
    shape.finish(color=(0.18, 0.38, 0.62), fill=(0.18, 0.38, 0.62), width=0)
    shape.commit()

    page.insert_text(pymupdf.Point(72, 290), "PROJECT PROPOSAL", fontsize=28, fontname="hebo", color=(0.18, 0.38, 0.62))
    page.insert_text(pymupdf.Point(72, 345), "Digital Transformation Initiative", fontsize=20, fontname="helv", color=(1, 1, 1))
    page.insert_text(pymupdf.Point(72, 375), "Phase II: Cloud Infrastructure Migration", fontsize=14, fontname="heit", color=(0.85, 0.90, 0.95))
    page.insert_text(pymupdf.Point(72, 520), "Prepared for:", fontsize=11, fontname="hebo", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 538), "Northgate Financial Services Ltd.", fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
    page.insert_text(pymupdf.Point(72, 570), "Prepared by:", fontsize=11, fontname="hebo", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 588), "Technology Advisory Division, Meridian Consulting Group", fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
    page.insert_text(pymupdf.Point(72, 620), "Date:", fontsize=11, fontname="hebo", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 638), "March 15, 2025", fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))

    # Page 2: Executive Summary
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text(pymupdf.Point(72, 72), "Executive Summary", fontsize=18, fontname="hebo", color=(0.18, 0.38, 0.62))
    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 85), pymupdf.Point(523, 85))
    shape2.finish(color=(0.18, 0.38, 0.62), width=1.5)
    shape2.commit()

    rect2 = pymupdf.Rect(72, 100, 523, 680)
    page2.insert_textbox(
        rect2,
        "Northgate Financial Services Ltd. has identified a critical need to modernize its "
        "existing on-premise IT infrastructure. The current systems, many of which are over "
        "eight years old, present increasing operational risk, limited scalability, and "
        "escalating maintenance costs.\n\n"
        "Meridian Consulting Group proposes a phased migration to a hybrid cloud architecture "
        "utilizing Microsoft Azure as the primary cloud platform. This approach will deliver:\n\n"
        "  • 40% reduction in infrastructure operating costs within 18 months\n"
        "  • 99.9% service availability SLA across all core banking systems\n"
        "  • Enhanced disaster recovery with 4-hour RTO and 1-hour RPO\n"
        "  • SOC 2 Type II and ISO 27001 compliance posture\n"
        "  • Scalable compute capacity to support 300% projected customer growth\n\n"
        "The total investment for Phase II is estimated at $2.4M over 14 months, with an "
        "expected ROI of 180% within three years. The migration will be conducted in three "
        "workstreams: infrastructure assessment and design, data migration, and application "
        "modernization.\n\n"
        "Meridian's certified cloud architects and project management team have successfully "
        "delivered 47 similar engagements for financial services clients in the past five "
        "years, with a 98% on-time, on-budget delivery record.",
        fontsize=10.5,
        fontname="helv",
        color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 3: Scope of Work
    page3 = doc.new_page(width=595, height=842)
    page3.insert_text(pymupdf.Point(72, 72), "Scope of Work", fontsize=18, fontname="hebo", color=(0.18, 0.38, 0.62))
    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, 85), pymupdf.Point(523, 85))
    shape3.finish(color=(0.18, 0.38, 0.62), width=1.5)
    shape3.commit()

    sections = [
        ("Workstream 1: Infrastructure Assessment & Design",
         "Comprehensive audit of existing 127 servers, 34 network appliances, and 2.8TB of "
         "storage. Design target-state architecture aligned with Azure Well-Architected Framework. "
         "Deliverables: As-Is assessment report, To-Be architecture blueprint, migration runbook."),
        ("Workstream 2: Data Migration",
         "Migrate 18 production databases (PostgreSQL, Oracle 12c, MS SQL Server 2016) to Azure "
         "SQL Managed Instance and Azure Database for PostgreSQL. Includes data validation, "
         "integrity checks, and parallel-run period. Estimated data volume: 4.7TB."),
        ("Workstream 3: Application Modernization",
         "Containerize 23 legacy applications using Docker and deploy to Azure Kubernetes Service. "
         "Implement CI/CD pipelines using Azure DevOps. Refactor 6 monolithic applications to "
         "microservices architecture for core customer-facing systems."),
    ]
    y = 110
    for title, body in sections:
        page3.insert_text(pymupdf.Point(72, y), title, fontsize=12, fontname="hebo", color=(0.2, 0.2, 0.2))
        y += 18
        rect3 = pymupdf.Rect(72, y, 523, y + 100)
        page3.insert_textbox(rect3, body, fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 115
        shape3b = page3.new_shape()
        shape3b.draw_line(pymupdf.Point(72, y - 5), pymupdf.Point(523, y - 5))
        shape3b.finish(color=(0.85, 0.85, 0.85), width=0.5)
        shape3b.commit()

    # Page 4: Timeline and Budget
    page4 = doc.new_page(width=595, height=842)
    page4.insert_text(pymupdf.Point(72, 72), "Timeline & Investment Summary", fontsize=18, fontname="hebo", color=(0.18, 0.38, 0.62))
    shape4 = page4.new_shape()
    shape4.draw_line(pymupdf.Point(72, 85), pymupdf.Point(523, 85))
    shape4.finish(color=(0.18, 0.38, 0.62), width=1.5)
    shape4.commit()

    page4.insert_text(pymupdf.Point(72, 110), "Project Timeline (14 months)", fontsize=12, fontname="hebo", color=(0.2, 0.2, 0.2))
    milestones = [
        ("Month 1-2", "Infrastructure assessment and architecture design"),
        ("Month 3-5", "Data migration — Phase 1 (non-production systems)"),
        ("Month 6-9", "Application containerization and CI/CD implementation"),
        ("Month 10-12", "Production data migration and cutover"),
        ("Month 13-14", "Parallel run, hypercare, and handover"),
    ]
    y = 135
    for period, desc in milestones:
        page4.insert_text(pymupdf.Point(72, y), f"• {period}:", fontsize=10, fontname="hebo", color=(0.18, 0.38, 0.62))
        page4.insert_text(pymupdf.Point(195, y), desc, fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15))
        y += 20

    page4.insert_text(pymupdf.Point(72, y + 20), "Investment Breakdown", fontsize=12, fontname="hebo", color=(0.2, 0.2, 0.2))
    items = [
        ("Professional Services (consulting, architecture, PM)", "$1,280,000"),
        ("Azure Infrastructure (14-month estimated spend)", "$720,000"),
        ("Licensing and tooling", "$240,000"),
        ("Training and knowledge transfer", "$95,000"),
        ("Contingency (10%)", "$65,000"),
        ("TOTAL INVESTMENT", "$2,400,000"),
    ]
    col1, col2 = 72, 420
    y += 45
    for i, (desc, amt) in enumerate(items):
        if i == len(items) - 1:
            shape4b = page4.new_shape()
            shape4b.draw_rect(pymupdf.Rect(67, y - 14, 530, y + 6))
            shape4b.finish(color=(0.18, 0.38, 0.62), fill=(0.18, 0.38, 0.62), width=0)
            shape4b.commit()
            page4.insert_text(pymupdf.Point(col1, y), desc, fontsize=10, fontname="hebo", color=(1, 1, 1))
            page4.insert_text(pymupdf.Point(col2, y), amt, fontsize=10, fontname="hebo", color=(1, 1, 1))
        else:
            page4.insert_text(pymupdf.Point(col1, y), desc, fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15))
            page4.insert_text(pymupdf.Point(col2, y), amt, fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15))
        y += 22

    doc.save(f'{WRAP_BATCH_DIR}/doc1.pdf')
    doc.close()
    print(f"Created: {WRAP_BATCH_DIR}/doc1.pdf (4 pages)")


def create_doc2():
    """doc2.pdf — Quarterly Report: 6 pages."""
    doc = pymupdf.open()

    titles = [
        "Q4 2024 Financial Performance Report",
        "Revenue Analysis — Q4 2024",
        "Regional Performance Breakdown",
        "Risk Management & Compliance Update",
        "Strategic Initiatives Progress",
        "Outlook and Guidance — Q1 2025",
    ]

    contents = [
        # Page 1: Cover
        None,
        # Page 2: Revenue
        ("Revenue Performance",
         "Total consolidated revenue for Q4 2024 reached $48.7M, representing a 12.3% "
         "increase year-over-year and a 4.1% increase quarter-over-quarter. This result "
         "exceeded analyst consensus estimates by $2.1M.\n\n"
         "Key revenue drivers included the successful launch of the PrimeEdge SaaS platform "
         "($8.4M contribution), expansion of the enterprise licensing program ($12.6M), and "
         "strong performance in the Asia-Pacific region ($9.8M, +22% YoY).\n\n"
         "Recurring revenue now represents 67% of total revenue, up from 58% in Q4 2023, "
         "demonstrating the successful transition to a subscription-based business model."),
        # Page 3: Regional
        ("Regional Performance",
         "North America: $23.4M (+8% YoY) — Continued strength in enterprise segment, "
         "offset by softness in SMB market due to macroeconomic headwinds.\n\n"
         "Europe & Middle East: $11.2M (+15% YoY) — Strong growth driven by GDPR compliance "
         "solution adoption and new partnerships with three Tier-1 banks in Germany and France.\n\n"
         "Asia-Pacific: $9.8M (+22% YoY) — Record quarter led by Japan ($3.2M) and Singapore "
         "($2.8M) operations. New office opening in Sydney expected Q1 2025.\n\n"
         "Latin America: $4.3M (+6% YoY) — Steady growth; Brazil remains largest market "
         "contributing $2.1M."),
        # Page 4: Risk
        ("Risk Management",
         "Regulatory Compliance: All major jurisdictions maintained full compliance during Q4. "
         "ISO 27001 recertification completed November 2024. SOC 2 Type II audit scheduled "
         "for February 2025.\n\n"
         "Cybersecurity: Zero critical security incidents reported in Q4. Phishing simulation "
         "program expanded to all 2,847 employees. Penetration testing completed with all "
         "high-severity findings remediated.\n\n"
         "Operational Risk: Business continuity plan tested in October 2024 with successful "
         "failover to secondary data center within 2-hour RTO target."),
        # Page 5: Initiatives
        ("Strategic Initiatives",
         "AI Product Integration (on track): Machine learning features integrated into 3 of "
         "5 core products. Customer adoption rate: 34% of enterprise tier. Projected full "
         "rollout by Q3 2025.\n\n"
         "Market Expansion — APAC (on track): Sydney office lease signed. Initial team of "
         "12 FTEs to be hired Q1 2025. Partner ecosystem development in progress.\n\n"
         "Platform Consolidation (at risk): Technical debt remediation delayed by 6 weeks "
         "due to resource constraints. New timeline: Q2 2025. Additional $400K budget "
         "approved by board."),
        # Page 6: Outlook
        ("Q1 2025 Guidance",
         "Revenue guidance: $50.5M - $52.0M (organic growth of 12-15% YoY)\n"
         "Gross margin target: 71-73% (improvement from 69.4% in Q4 2024)\n"
         "Adjusted EBITDA margin: 22-24%\n"
         "Free cash flow: $8.5M - $10.0M\n\n"
         "Key assumptions: Successful Sydney office launch contributing $0.8M in Q1; "
         "Enterprise pipeline conversion rate of 28%; No material adverse regulatory changes "
         "in key markets.\n\n"
         "The Board of Directors has authorized a $15M share buyback program commencing "
         "January 2025, reflecting confidence in the company's financial position and "
         "long-term growth trajectory."),
    ]

    for i in range(6):
        page = doc.new_page(width=595, height=842)

        if i == 0:
            # Cover page
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(0, 0, 595, 180))
            shape.finish(color=(0.06, 0.18, 0.36), fill=(0.06, 0.18, 0.36), width=0)
            shape.commit()
            page.insert_text(pymupdf.Point(50, 80), "Q4 2024", fontsize=32, fontname="hebo", color=(1, 1, 1))
            page.insert_text(pymupdf.Point(50, 120), "Financial Performance Report", fontsize=20, fontname="helv", color=(0.8, 0.85, 0.9))
            page.insert_text(pymupdf.Point(50, 150), "Fiscal Year End | December 31, 2024", fontsize=12, fontname="heit", color=(0.7, 0.75, 0.8))
            page.insert_text(pymupdf.Point(50, 250), "Nexagen Technologies Inc.", fontsize=16, fontname="hebo", color=(0.06, 0.18, 0.36))
            page.insert_text(pymupdf.Point(50, 275), "NASDAQ: NXGN", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
            page.insert_text(pymupdf.Point(50, 320), "Strictly Confidential — For Internal Distribution Only", fontsize=10, fontname="heit", color=(0.5, 0.5, 0.5))
        else:
            title_text, body_text = contents[i]
            page.insert_text(pymupdf.Point(72, 72), titles[i], fontsize=17, fontname="hebo", color=(0.06, 0.18, 0.36))
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 86), pymupdf.Point(523, 86))
            shape.finish(color=(0.06, 0.18, 0.36), width=1.5)
            shape.commit()
            page.insert_text(pymupdf.Point(72, 104), title_text, fontsize=12, fontname="hebo", color=(0.2, 0.2, 0.2))
            rect = pymupdf.Rect(72, 122, 523, 750)
            page.insert_textbox(rect, body_text, fontsize=10.5, fontname="helv", color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)

        # Page number footer
        page.insert_text(pymupdf.Point(72, 820), "Nexagen Technologies Inc. — Q4 2024 Report", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
        page.insert_text(pymupdf.Point(500, 820), f"Page {i + 1} of 6", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    doc.save(f'{WRAP_BATCH_DIR}/doc2.pdf')
    doc.close()
    print(f"Created: {WRAP_BATCH_DIR}/doc2.pdf (6 pages)")


def create_doc3():
    """doc3.pdf — Meeting Minutes: 3 pages."""
    doc = pymupdf.open()

    # Page 1
    page1 = doc.new_page(width=595, height=842)
    page1.insert_text(pymupdf.Point(72, 72), "MEETING MINUTES", fontsize=22, fontname="hebo", color=(0.25, 0.25, 0.25))
    shape1 = page1.new_shape()
    shape1.draw_line(pymupdf.Point(72, 88), pymupdf.Point(523, 88))
    shape1.finish(color=(0.25, 0.25, 0.25), width=2)
    shape1.commit()

    meta = [
        ("Meeting Title:", "Product Roadmap Review — H1 2025 Planning Session"),
        ("Date & Time:", "Thursday, January 23, 2025 at 14:00–16:30 GMT"),
        ("Location:", "Conference Room A, HQ London / Video Conference"),
        ("Facilitator:", "Priya Nair, Chief Product Officer"),
        ("Note Taker:", "Daniel Okonkwo, Program Manager"),
    ]
    y = 110
    for label, value in meta:
        page1.insert_text(pymupdf.Point(72, y), label, fontsize=10, fontname="hebo", color=(0.3, 0.3, 0.3))
        page1.insert_text(pymupdf.Point(220, y), value, fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 20

    page1.insert_text(pymupdf.Point(72, y + 10), "Attendees:", fontsize=10, fontname="hebo", color=(0.3, 0.3, 0.3))
    attendees = [
        "Priya Nair (CPO)", "Marcus Webb (CTO)", "Sophia Lindqvist (VP Engineering)",
        "James Obi (Head of Product)", "Fatima Al-Rashid (Lead Architect)",
        "Tom Bergström (QA Manager)", "Yuki Tanaka (UX Lead)", "Daniel Okonkwo (PM)",
    ]
    y += 28
    for att in attendees:
        page1.insert_text(pymupdf.Point(90, y), f"• {att}", fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15))
        y += 18

    page1.insert_text(pymupdf.Point(72, y + 15), "1. Agenda Item: Q4 2024 Product Review", fontsize=12, fontname="hebo", color=(0.2, 0.2, 0.2))
    y += 35
    rect1 = pymupdf.Rect(72, y, 523, y + 200)
    page1.insert_textbox(
        rect1,
        "Priya Nair opened the session by reviewing Q4 2024 product KPIs. The PrimeEdge "
        "SaaS platform achieved 94% of its monthly active user target (18,800 vs. 20,000 "
        "goal). Customer satisfaction (CSAT) remained strong at 4.3/5.0.\n\n"
        "Marcus Webb highlighted three critical technical debt items resolved in Q4: "
        "the payment gateway latency issue (reduced from 1.2s to 0.18s), the reporting "
        "module memory leak, and the mobile app push notification reliability issue "
        "(99.4% delivery rate, up from 87.2%).\n\n"
        "Decision: Q1 2025 will focus on MAU growth to 25,000 and achieving CSAT of 4.5. "
        "Resource reallocation approved: 3 engineers from infrastructure to product.",
        fontsize=10,
        fontname="helv",
        color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 2
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text(pymupdf.Point(72, 72), "Meeting Minutes (continued) — Page 2", fontsize=13, fontname="hebo", color=(0.25, 0.25, 0.25))
    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 85), pymupdf.Point(523, 85))
    shape2.finish(color=(0.25, 0.25, 0.25), width=1)
    shape2.commit()

    items = [
        ("2. Agenda Item: H1 2025 Roadmap Prioritization",
         "Sophia Lindqvist presented the engineering capacity model for H1 2025. Available "
         "engineering capacity: 148 story points per sprint (16 engineers, 2-week sprints). "
         "Technical debt allocation: 20% of capacity (29.6 SP per sprint).\n\n"
         "Proposed priority stack for H1 2025:\n"
         "  P1: AI-powered analytics dashboard (estimated 8 sprints, 240 SP)\n"
         "  P2: Multi-tenant SSO integration — SAML 2.0 and OAuth 2.0 (4 sprints, 120 SP)\n"
         "  P3: Mobile app v3.0 redesign (6 sprints, 180 SP)\n"
         "  P4: API v2 public release with GraphQL support (3 sprints, 90 SP)\n\n"
         "After discussion, the group agreed to defer Mobile app v3.0 to H2 2025 to allow "
         "completion of the SSO integration, which has three enterprise clients blocked on "
         "this feature."),
        ("3. Agenda Item: Resource & Hiring Plan",
         "James Obi presented the open headcount requirements: 2 Senior Backend Engineers "
         "(Python/Go), 1 ML Engineer (NLP focus), 1 Senior UX Researcher. "
         "All positions approved by Finance; JDs to be published by February 3.\n\n"
         "Yuki Tanaka noted that the UX Researcher role is critical for the AI analytics "
         "dashboard user testing program. Target hire date: March 15, 2025."),
    ]
    y = 105
    for title, body in items:
        page2.insert_text(pymupdf.Point(72, y), title, fontsize=12, fontname="hebo", color=(0.2, 0.2, 0.2))
        y += 18
        rect = pymupdf.Rect(72, y, 523, y + 200)
        page2.insert_textbox(rect, body, fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 215

    # Page 3: Action Items
    page3 = doc.new_page(width=595, height=842)
    page3.insert_text(pymupdf.Point(72, 72), "Meeting Minutes (continued) — Page 3: Action Items", fontsize=13, fontname="hebo", color=(0.25, 0.25, 0.25))
    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, 85), pymupdf.Point(523, 85))
    shape3.finish(color=(0.25, 0.25, 0.25), width=1)
    shape3.commit()

    page3.insert_text(pymupdf.Point(72, 110), "4. Action Items & Owners", fontsize=12, fontname="hebo", color=(0.2, 0.2, 0.2))

    # Table headers
    cols = [72, 280, 390, 490]
    hdrs = ["Action Item", "Owner", "Due Date", "Priority"]
    shape3b = page3.new_shape()
    shape3b.draw_rect(pymupdf.Rect(67, 125, 530, 143))
    shape3b.finish(color=(0.25, 0.25, 0.25), fill=(0.25, 0.25, 0.25), width=0)
    shape3b.commit()
    for i, h in enumerate(hdrs):
        page3.insert_text(pymupdf.Point(cols[i], 139), h, fontsize=9, fontname="hebo", color=(1, 1, 1))

    actions = [
        ("Publish H1 2025 roadmap to all-hands", "J. Obi", "Feb 7", "HIGH"),
        ("Post JDs for 4 open positions", "HR / J. Obi", "Feb 3", "HIGH"),
        ("Finalize AI dashboard UX wireframes", "Y. Tanaka", "Feb 14", "HIGH"),
        ("SSO integration kickoff meeting", "S. Lindqvist", "Feb 10", "MEDIUM"),
        ("Update sprint capacity model for H1", "S. Lindqvist", "Jan 31", "MEDIUM"),
        ("API v2 technical spec document", "M. Webb", "Feb 21", "MEDIUM"),
        ("Schedule UX Researcher interviews", "HR", "Mar 1", "MEDIUM"),
        ("Q4 retrospective report distribution", "D. Okonkwo", "Jan 28", "LOW"),
    ]
    y = 158
    for ri, (action, owner, due, priority) in enumerate(actions):
        if ri % 2 == 0:
            shape3c = page3.new_shape()
            shape3c.draw_rect(pymupdf.Rect(67, y - 12, 530, y + 8))
            shape3c.finish(color=None, fill=(0.94, 0.94, 0.96), width=0)
            shape3c.commit()
        page3.insert_text(pymupdf.Point(cols[0], y), action[:42], fontsize=8.5, fontname="helv", color=(0.1, 0.1, 0.1))
        page3.insert_text(pymupdf.Point(cols[1], y), owner, fontsize=8.5, fontname="helv", color=(0.1, 0.1, 0.1))
        page3.insert_text(pymupdf.Point(cols[2], y), due, fontsize=8.5, fontname="helv", color=(0.1, 0.1, 0.1))
        color = (0.7, 0.1, 0.1) if priority == "HIGH" else ((0.6, 0.4, 0.0) if priority == "MEDIUM" else (0.3, 0.5, 0.2))
        page3.insert_text(pymupdf.Point(cols[3], y), priority, fontsize=8.5, fontname="hebo", color=color)
        y += 22

    page3.insert_text(pymupdf.Point(72, y + 25), "Next Meeting:", fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
    page3.insert_text(pymupdf.Point(200, y + 25), "February 27, 2025 at 14:00 GMT — Sprint Review & Q1 Mid-Check", fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15))

    doc.save(f'{WRAP_BATCH_DIR}/doc3.pdf')
    doc.close()
    print(f"Created: {WRAP_BATCH_DIR}/doc3.pdf (3 pages)")


def main():
    # Create directories
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    os.makedirs(WRAP_BATCH_DIR, exist_ok=True)
    # NOTE: wrapped/ directory must NOT exist — the agent must create it
    wrapped_dir = f'{WRAP_BATCH_DIR}/wrapped'
    if os.path.exists(wrapped_dir):
        import shutil
        shutil.rmtree(wrapped_dir)

    # Create all PDF files
    create_header_pdf()
    create_footer_pdf()
    create_doc1()
    create_doc2()
    create_doc3()

    # Verify counts
    import pymupdf as _fitz
    for fname, expected_pages in [('doc1.pdf', 4), ('doc2.pdf', 6), ('doc3.pdf', 3)]:
        fpath = f'{WRAP_BATCH_DIR}/{fname}'
        d = _fitz.open(fpath)
        assert d.page_count == expected_pages, f"{fname}: expected {expected_pages} pages, got {d.page_count}"
        d.close()
    for fname, expected_pages in [('header_page.pdf', 1), ('footer_page.pdf', 1)]:
        fpath = f'{DOCUMENTS_DIR}/{fname}'
        d = _fitz.open(fpath)
        assert d.page_count == expected_pages, f"{fname}: expected {expected_pages} pages, got {d.page_count}"
        d.close()

    print("\nAll files created and verified:")
    print(f"  {HEADER_PDF} (1 page)")
    print(f"  {FOOTER_PDF} (1 page)")
    print(f"  {WRAP_BATCH_DIR}/doc1.pdf (4 pages)")
    print(f"  {WRAP_BATCH_DIR}/doc2.pdf (6 pages)")
    print(f"  {WRAP_BATCH_DIR}/doc3.pdf (3 pages)")
    print(f"  {WRAP_BATCH_DIR}/wrapped/ — NOT created (agent's task)")

    # Open Evince with the header as a preview and file manager to see the batch
    launch_gui(f'evince "{HEADER_PDF}"', delay_sec=1.5)
    launch_gui(f'nautilus "{WRAP_BATCH_DIR}"', delay_sec=1.0)
    print("GUI_READY: Evince and Nautilus launched with DISPLAY=:0")


main()
