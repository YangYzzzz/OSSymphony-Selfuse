"""
Initial Setup: quality_report.pdf with 10 pages; page 7 has a yellow highlight annotation.
Task ID: pdf_basic_120
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_basic_120'
OUTPUT = f'{WORKDIR}/Desktop/quality_report.pdf'


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
    doc = pymupdf.open()

    # Page content data - 10 pages of a quality report
    pages_content = [
        {
            "title": "Quality Assurance Report",
            "subtitle": "Product Line Assessment — FY2024",
            "body": (
                "This report presents a comprehensive evaluation of product quality across "
                "all manufacturing divisions for the fiscal year 2024. Our assessment covers "
                "defect rates, customer complaints, process efficiency, and compliance with "
                "industry standards ISO 9001:2015.\n\n"
                "Executive Summary: Overall quality metrics improved by 12% compared to FY2023. "
                "Key areas of focus include supply chain reliability, assembly tolerance control, "
                "and post-market surveillance programs."
            ),
        },
        {
            "title": "Section 1: Methodology",
            "body": (
                "1.1 Data Collection\n"
                "Data was gathered from 14 production facilities across three geographic regions. "
                "Inspection records, customer feedback databases, and supplier audit reports "
                "were consolidated into a unified dataset.\n\n"
                "1.2 Sampling Strategy\n"
                "A stratified random sampling approach was applied. Sample sizes were determined "
                "using standard statistical methods (confidence level 95%, margin of error ±3%).\n\n"
                "1.3 Analysis Tools\n"
                "Statistical process control (SPC) charts, Pareto analysis, and root cause "
                "investigation frameworks were employed throughout the assessment period."
            ),
        },
        {
            "title": "Section 2: Defect Analysis",
            "body": (
                "2.1 Defect Categories\n"
                "Defects were classified into five primary categories: cosmetic (surface finish), "
                "dimensional (out-of-tolerance), functional (performance failure), "
                "documentation (labeling/packaging), and regulatory non-conformance.\n\n"
                "2.2 Defect Rates by Category\n"
                "  - Cosmetic defects:       2.3%\n"
                "  - Dimensional defects:    0.8%\n"
                "  - Functional defects:     0.4%\n"
                "  - Documentation defects:  1.1%\n"
                "  - Regulatory issues:      0.2%\n\n"
                "Total defect rate: 4.8% (down from 5.5% in FY2023)."
            ),
        },
        {
            "title": "Section 3: Customer Feedback",
            "body": (
                "3.1 Complaint Volume\n"
                "A total of 1,247 customer complaints were received during FY2024, representing "
                "a 9% reduction compared to the prior year. The majority of complaints (62%) "
                "were resolved within the 5-business-day target.\n\n"
                "3.2 Top Complaint Themes\n"
                "  - Packaging damage:        28%\n"
                "  - Missing components:      19%\n"
                "  - Incorrect specifications: 17%\n"
                "  - Cosmetic issues:          14%\n"
                "  - Performance complaints:   12%\n"
                "  - Other:                   10%\n\n"
                "3.3 Net Promoter Score\n"
                "Customer NPS improved from 42 to 51, reflecting enhanced satisfaction with "
                "responsiveness and resolution quality."
            ),
        },
        {
            "title": "Section 4: Supplier Performance",
            "body": (
                "4.1 Supplier Qualification\n"
                "All Tier-1 suppliers (n=38) underwent annual qualification audits. "
                "Three suppliers were placed on corrective action plans following findings "
                "related to process control documentation.\n\n"
                "4.2 Incoming Inspection Results\n"
                "Incoming rejection rate: 1.9% (target: <2.0%). Categories with highest "
                "rejection rates include precision castings (4.2%) and electronic sub-assemblies (2.8%).\n\n"
                "4.3 Supplier Development Initiatives\n"
                "A supplier development workshop series was launched in Q2, with 22 suppliers "
                "participating in advanced SPC training and yield improvement programs."
            ),
        },
        {
            "title": "Section 5: Process Improvements",
            "body": (
                "5.1 Lean Six Sigma Projects\n"
                "Seven active Lean Six Sigma projects were completed in FY2024, delivering "
                "an estimated $2.3M in annualized savings. Projects addressed welding defect "
                "reduction, painting cycle time, and assembly rework rates.\n\n"
                "5.2 Automation Integration\n"
                "Automated optical inspection (AOI) systems were deployed at three additional "
                "production lines, increasing automated inspection coverage from 54% to 71%.\n\n"
                "5.3 Employee Training\n"
                "Over 3,400 training hours were delivered across quality-related topics. "
                "Certification completion rate reached 94% against an 85% target."
            ),
        },
        {
            "title": "Section 6: Regulatory Compliance",
            "body": (
                "6.1 Standards and Certifications\n"
                "Facilities maintained ISO 9001:2015 certification with zero major non-conformances "
                "during surveillance audits. Two facilities achieved initial IATF 16949 "
                "certification in FY2024.\n\n"
                "6.2 Regulatory Submissions\n"
                "Fourteen regulatory submissions were filed during the year. No warning letters "
                "or enforcement actions were received from regulatory authorities.\n\n"
                "6.3 Product Safety\n"
                "Zero product safety recalls were issued. Two voluntary field notifications "
                "were executed proactively as part of post-market surveillance findings, "
                "affecting fewer than 500 units in total."
            ),
        },
        # PAGE 7 — this page will have the yellow highlight annotation
        {
            "title": "Section 7: Risk Management",
            "body": (
                "7.1 Quality Risk Register\n"
                "The quality risk register was updated quarterly. Seventeen active risk items "
                "were tracked, with four classified as high-priority. All high-priority risks "
                "had mitigation plans in place by end of Q3.\n\n"
                "7.2 Critical Control Points\n"
                "Critical control points (CCPs) were reviewed and validated for all product "
                "families. Process capability indices (Cpk) for critical dimensions averaged "
                "1.42, exceeding the minimum acceptable threshold of 1.33.\n\n"
                "7.3 Business Continuity Planning\n"
                "Business continuity plans were tested via tabletop exercises in Q1 and Q3. "
                "Backup supplier qualification was completed for 11 single-source components, "
                "reducing supply chain risk exposure by an estimated 35%."
            ),
        },
        {
            "title": "Section 8: Continuous Improvement Roadmap",
            "body": (
                "8.1 FY2025 Quality Objectives\n"
                "  - Reduce overall defect rate to below 4.0%\n"
                "  - Achieve NPS score of 60 or above\n"
                "  - Expand automated inspection coverage to 85%\n"
                "  - Complete ISO 14001 gap assessment for all sites\n\n"
                "8.2 Strategic Initiatives\n"
                "Digital quality management system (QMS) deployment is scheduled for H1 FY2025, "
                "consolidating inspection records, CAPA tracking, and supplier scorecards "
                "into a single integrated platform.\n\n"
                "8.3 Investment Plan\n"
                "Capital expenditure of $4.7M is planned for quality infrastructure, including "
                "expanded metrology laboratory capacity and additional AOI equipment."
            ),
        },
        {
            "title": "Section 9: Conclusions and Acknowledgements",
            "body": (
                "9.1 Summary of Findings\n"
                "FY2024 demonstrated sustained progress across all major quality performance "
                "indicators. The reduction in overall defect rate, improved customer NPS, "
                "and successful regulatory outcomes reflect the commitment of the organization "
                "to quality excellence.\n\n"
                "9.2 Key Achievements\n"
                "  - Defect rate reduced from 5.5% to 4.8%\n"
                "  - NPS improved from 42 to 51\n"
                "  - Zero product safety recalls\n"
                "  - Two new IATF 16949 certifications achieved\n\n"
                "9.3 Acknowledgements\n"
                "The Quality Assurance team thanks all division leaders, plant managers, "
                "and front-line inspection personnel for their contributions to this year's "
                "quality improvement efforts."
            ),
        },
    ]

    # Create Desktop directory if needed
    # (Script runs on VM where /home/user/Desktop should exist)
    # Build each page
    for i, content in enumerate(pages_content):
        page = doc.new_page(width=612, height=792)  # US Letter
        y = 72

        # Title
        page.insert_text(
            pymupdf.Point(72, y),
            content["title"],
            fontsize=18,
            fontname="hebo",
            color=(0.1, 0.1, 0.4),
        )
        y += 30

        # Subtitle (if any)
        if "subtitle" in content:
            page.insert_text(
                pymupdf.Point(72, y),
                content["subtitle"],
                fontsize=12,
                fontname="tiit",
                color=(0.3, 0.3, 0.3),
            )
            y += 20

        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, y + 5), pymupdf.Point(540, y + 5))
        shape.finish(color=(0.2, 0.2, 0.6), width=1.5)
        shape.commit()
        y += 20

        # Page number (footer)
        page.insert_text(
            pymupdf.Point(296, 750),
            f"Page {i + 1} of {len(pages_content)}",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Body text — insert in a textbox
        body_rect = pymupdf.Rect(72, y, 540, 720)
        page.insert_textbox(
            body_rect,
            content["body"],
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

    # --- Add YELLOW highlight annotation on page 7 (index 6) ---
    page7 = doc[6]

    # Search for text to highlight on page 7
    highlight_text = "Critical Control Points"
    instances = page7.search_for(highlight_text)

    if instances:
        for inst in instances:
            annot = page7.add_highlight_annot(inst)
            annot.set_colors(stroke=(1, 1, 0))  # yellow
            annot.update()
    else:
        # Fallback: add highlight at a fixed position if text search fails
        fallback_rect = pymupdf.Rect(72, 200, 300, 215)
        annot = page7.add_highlight_annot(fallback_rect)
        annot.set_colors(stroke=(1, 1, 0))  # yellow
        annot.update()

    # Set PDF metadata
    doc.set_metadata({
        "title": "Quality Assurance Report FY2024",
        "author": "Quality Assurance Division",
        "subject": "Annual Quality Report",
        "keywords": "quality, assurance, report, FY2024",
        "creator": "QA Department",
        "producer": "PyMuPDF",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup — open PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
