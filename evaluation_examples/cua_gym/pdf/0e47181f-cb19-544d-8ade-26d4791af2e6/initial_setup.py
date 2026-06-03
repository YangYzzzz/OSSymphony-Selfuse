"""
Initial Setup: Create 10 source PDF files with metadata in /home/user/reports/source_docs/
Task ID: pdf_pw_045
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_045'
SOURCE_DIR = f'{WORKDIR}/reports/source_docs'
REPORT_PATH = f'{WORKDIR}/reports/metadata_report.pdf'

# 10 realistic source PDF definitions with varying content
SOURCE_PDFS = [
    {
        "filename": "Q1_2025_Financial_Summary.pdf",
        "title": "Q1 2025 Financial Summary",
        "author": "Sarah Chen",
        "creation_date": "D:20250115093000",
        "num_pages": 4,
        "content_lines": [
            "Q1 2025 Financial Summary",
            "Revenue: $2,450,000",
            "Operating Expenses: $1,820,000",
            "Net Income: $630,000",
            "This report covers January through March 2025.",
        ],
    },
    {
        "filename": "Employee_Handbook_2025.pdf",
        "title": "Employee Handbook 2025 Edition",
        "author": "Marcus Johnson",
        "creation_date": "D:20250203140000",
        "num_pages": 12,
        "content_lines": [
            "Employee Handbook - 2025 Edition",
            "Chapter 1: Company Overview",
            "Chapter 2: Code of Conduct",
            "Chapter 3: Benefits and Compensation",
            "Chapter 4: Leave Policies",
        ],
    },
    {
        "filename": "Project_Atlas_Proposal.pdf",
        "title": "Project Atlas Technical Proposal",
        "author": "Priya Sharma",
        "creation_date": "D:20250310110000",
        "num_pages": 7,
        "content_lines": [
            "Project Atlas - Technical Proposal",
            "Objective: Modernize legacy data pipeline",
            "Timeline: 6 months",
            "Budget: $340,000",
            "Team: 5 engineers, 2 data scientists",
        ],
    },
    {
        "filename": "Marketing_Strategy_Q2.pdf",
        "title": "Q2 Marketing Strategy",
        "author": "Elena Rodriguez",
        "creation_date": "D:20250322160000",
        "num_pages": 5,
        "content_lines": [
            "Q2 Marketing Strategy Document",
            "Target Audience: Enterprise B2B",
            "Channels: LinkedIn, Google Ads, Webinars",
            "Budget Allocation: $180,000",
            "Expected ROI: 3.2x",
        ],
    },
    {
        "filename": "Security_Audit_Report.pdf",
        "title": "Annual Security Audit Report",
        "author": "James O'Brien",
        "creation_date": "D:20250118100000",
        "num_pages": 9,
        "content_lines": [
            "Annual Security Audit Report",
            "Audit Period: January 2024 - December 2024",
            "Critical Findings: 2",
            "High Priority: 5",
            "Medium Priority: 12",
        ],
    },
    {
        "filename": "Product_Roadmap_2025.pdf",
        "title": "Product Roadmap 2025",
        "author": "Wei Liu",
        "creation_date": "D:20250205083000",
        "num_pages": 3,
        "content_lines": [
            "Product Roadmap 2025",
            "Phase 1: Core Platform Upgrade (Q1-Q2)",
            "Phase 2: AI Integration (Q3)",
            "Phase 3: Global Expansion (Q4)",
        ],
    },
    {
        "filename": "Client_Satisfaction_Survey.pdf",
        "title": "2024 Client Satisfaction Survey Results",
        "author": "Aisha Patel",
        "creation_date": "D:20250128143000",
        "num_pages": 6,
        "content_lines": [
            "Client Satisfaction Survey Results - 2024",
            "Response Rate: 78%",
            "Overall Satisfaction: 4.3/5.0",
            "Net Promoter Score: 62",
            "Key Improvement Area: Response Time",
        ],
    },
    {
        "filename": "Infrastructure_Cost_Analysis.pdf",
        "title": "Cloud Infrastructure Cost Analysis",
        "author": "David Kim",
        "creation_date": "D:20250215091500",
        "num_pages": 8,
        "content_lines": [
            "Cloud Infrastructure Cost Analysis",
            "Monthly Spend: $45,230",
            "YoY Change: +12%",
            "Top Service: EC2 Compute ($18,400)",
            "Optimization Potential: $8,200/month",
        ],
    },
    {
        "filename": "Training_Program_Outline.pdf",
        "title": "New Hire Training Program",
        "author": "Rachel Torres",
        "creation_date": "D:20250301120000",
        "num_pages": 5,
        "content_lines": [
            "New Hire Training Program Outline",
            "Week 1: Company Orientation",
            "Week 2: Technical Foundations",
            "Week 3: Tools and Workflows",
            "Week 4: Mentorship Pairing",
        ],
    },
    {
        "filename": "Board_Meeting_Minutes_Feb.pdf",
        "title": "Board Meeting Minutes - February 2025",
        "author": "Thomas Nakamura",
        "creation_date": "D:20250228170000",
        "num_pages": 2,
        "content_lines": [
            "Board Meeting Minutes",
            "Date: February 28, 2025",
            "Attendees: 8 of 9 board members",
            "Key Decision: Approved Series C funding round",
            "Next Meeting: March 28, 2025",
        ],
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


def create_source_pdf(filepath, pdf_def):
    """Create a PDF with specified metadata, page count, and content."""
    doc = pymupdf.open()

    # Create pages with content
    for page_idx in range(pdf_def["num_pages"]):
        page = doc.new_page(width=595, height=842)  # A4

        if page_idx == 0:
            # Title page
            y = 72
            page.insert_text(
                pymupdf.Point(72, y),
                pdf_def["content_lines"][0],
                fontsize=18,
                fontname="hebo",
                color=(0, 0, 0.5),
            )
            y += 40
            for line in pdf_def["content_lines"][1:]:
                page.insert_text(
                    pymupdf.Point(72, y),
                    line,
                    fontsize=12,
                    fontname="helv",
                    color=(0, 0, 0),
                )
                y += 20
        else:
            # Additional pages with filler content
            page.insert_text(
                pymupdf.Point(72, 72),
                f"{pdf_def['content_lines'][0]} - Page {page_idx + 1}",
                fontsize=14,
                fontname="hebo",
                color=(0, 0, 0),
            )
            page.insert_text(
                pymupdf.Point(72, 110),
                f"Detailed content for section {page_idx + 1} of this document. "
                f"This page contains supplementary information and analysis "
                f"supporting the main findings presented in the executive summary.",
                fontsize=11,
                fontname="helv",
                color=(0.1, 0.1, 0.1),
            )

    # Set metadata
    doc.set_metadata({
        "title": pdf_def["title"],
        "author": pdf_def["author"],
        "creationDate": pdf_def["creation_date"],
        "creator": "CUA-Gym Document Generator",
        "producer": "PyMuPDF",
    })

    doc.save(filepath)
    doc.close()


def create_initial():
    # Create directories
    os.makedirs(SOURCE_DIR, exist_ok=True)
    os.makedirs(f'{WORKDIR}/reports', exist_ok=True)

    # Make sure metadata_report.pdf does NOT exist
    if os.path.exists(REPORT_PATH):
        os.remove(REPORT_PATH)

    # Create all 10 source PDFs
    for pdf_def in SOURCE_PDFS:
        filepath = os.path.join(SOURCE_DIR, pdf_def["filename"])
        create_source_pdf(filepath, pdf_def)
        print(f'Created: {filepath}')

    print(f'\nAll 10 source PDFs created in {SOURCE_DIR}')
    print(f'metadata_report.pdf does NOT exist: {not os.path.exists(REPORT_PATH)}')

    # Open file manager showing source_docs directory
    launch_gui(f'nautilus "{SOURCE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus with DISPLAY=:0')


create_initial()
