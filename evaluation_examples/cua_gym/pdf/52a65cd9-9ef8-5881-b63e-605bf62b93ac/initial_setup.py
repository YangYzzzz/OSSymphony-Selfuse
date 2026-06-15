"""
Initial Setup: Create 5 PDF files in ~/Documents/batch_pdfs/ with different authors.
Task ID: pdf_mbc_012
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
BATCH_DIR = f'{WORKDIR}/Documents/batch_pdfs'

# Authors for each file
AUTHORS = {
    'file1.pdf': 'Alice',
    'file2.pdf': 'Bob',
    'file3.pdf': 'Charlie',
    'file4.pdf': 'Diana',
    'file5.pdf': 'Eve',
}

# Realistic content for each file
CONTENT = {
    'file1.pdf': {
        'title': 'Q1 2025 Marketing Strategy',
        'subject': 'Marketing',
        'text': (
            'Q1 2025 Marketing Strategy\n\n'
            'Executive Summary\n\n'
            'This document outlines the marketing strategy for the first quarter of 2025. '
            'Our primary focus will be on expanding brand awareness in the Asia-Pacific region '
            'and strengthening our digital presence across social media platforms.\n\n'
            'Key Objectives:\n'
            '1. Increase social media engagement by 25%\n'
            '2. Launch three new product campaigns targeting millennials\n'
            '3. Establish partnerships with five regional influencers\n'
            '4. Achieve a 15% increase in website traffic from organic search\n\n'
            'Budget allocation for Q1 stands at $245,000, distributed across digital advertising, '
            'content creation, and event sponsorships.'
        ),
    },
    'file2.pdf': {
        'title': 'Employee Onboarding Handbook',
        'subject': 'Human Resources',
        'text': (
            'Employee Onboarding Handbook\n\n'
            'Welcome to TechNova Solutions!\n\n'
            'We are thrilled to have you join our team. This handbook provides essential '
            'information to help you get started on your first day and beyond.\n\n'
            'Office Hours: Monday through Friday, 9:00 AM to 6:00 PM\n'
            'Dress Code: Business casual\n'
            'IT Support: ext. 4500 or helpdesk@technova.com\n\n'
            'Your first week will include orientation sessions covering company culture, '
            'security protocols, benefits enrollment, and introductions to your department leads. '
            'Please bring a valid photo ID and your signed offer letter on Day 1.\n\n'
            'Manager: Sarah Chen, VP of Engineering\n'
            'HR Contact: Marcus Rivera, HR Coordinator'
        ),
    },
    'file3.pdf': {
        'title': 'Project Phoenix - Technical Specification',
        'subject': 'Engineering',
        'text': (
            'Project Phoenix - Technical Specification\n\n'
            'Version 2.3 | Last Updated: March 10, 2025\n\n'
            'Overview\n\n'
            'Project Phoenix is a microservices migration initiative designed to decompose '
            'our monolithic order management system into independently deployable services. '
            'The target architecture uses Kubernetes orchestration with gRPC inter-service '
            'communication.\n\n'
            'Service Breakdown:\n'
            '- Order Service (Go, port 8080)\n'
            '- Inventory Service (Rust, port 8081)\n'
            '- Payment Gateway (Java, port 8082)\n'
            '- Notification Service (Python, port 8083)\n\n'
            'Estimated completion: Q3 2025\n'
            'Team size: 12 engineers across 3 squads'
        ),
    },
    'file4.pdf': {
        'title': 'Annual Financial Review 2024',
        'subject': 'Finance',
        'text': (
            'Annual Financial Review 2024\n\n'
            'Prepared by the Finance Department\n\n'
            'Revenue Summary\n\n'
            'Total revenue for FY2024 reached $18.7 million, representing a 12% increase '
            'over FY2023. Gross margin improved to 64.3% from 61.8% the previous year.\n\n'
            'Key Metrics:\n'
            '- Net Income: $3.2M (up from $2.5M)\n'
            '- Operating Expenses: $11.9M\n'
            '- EBITDA: $5.1M\n'
            '- Customer Acquisition Cost: $127 (down 8%)\n'
            '- Monthly Recurring Revenue: $1.56M\n\n'
            'The board has approved a capital expenditure budget of $4.5M for 2025, '
            'primarily allocated to infrastructure upgrades and R&D expansion.'
        ),
    },
    'file5.pdf': {
        'title': 'Sustainability Report - Environmental Impact',
        'subject': 'Corporate Responsibility',
        'text': (
            'Sustainability Report - Environmental Impact\n\n'
            'Fiscal Year 2024\n\n'
            'Our commitment to sustainability remains at the core of our operations. '
            'This report details progress toward our 2030 carbon neutrality goals.\n\n'
            'Highlights:\n'
            '- Carbon emissions reduced by 18% compared to 2023 baseline\n'
            '- 73% of office energy sourced from renewable providers\n'
            '- Paper consumption decreased by 42% through digitization\n'
            '- 95% of electronic waste properly recycled through certified partners\n\n'
            'Water Usage: 12,400 cubic meters (down from 14,800)\n'
            'Waste Diversion Rate: 81%\n'
            'Green Procurement Spend: $2.3M\n\n'
            'Looking ahead, we plan to install solar panels at our Denver and Austin '
            'facilities by Q2 2025, which is projected to offset 35% of on-site energy use.'
        ),
    },
}


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
    os.makedirs(BATCH_DIR, exist_ok=True)

    for filename, author in AUTHORS.items():
        filepath = os.path.join(BATCH_DIR, filename)
        info = CONTENT[filename]

        doc = pymupdf.open()
        page = doc.new_page(width=595, height=842)  # A4

        # Insert title
        page.insert_text(
            pymupdf.Point(72, 72),
            info['title'],
            fontsize=18,
            fontname="hebo",
            color=(0, 0, 0.5),
        )

        # Insert body text using textbox for wrapping
        rect = pymupdf.Rect(72, 110, 523, 770)
        page.insert_textbox(
            rect,
            info['text'],
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Set metadata with unique author
        doc.set_metadata({
            "title": info['title'],
            "author": author,
            "subject": info['subject'],
            "creator": "TechNova Internal Tools",
            "producer": "PyMuPDF",
        })

        doc.save(filepath)
        doc.close()
        print(f'Created {filepath} with author: {author}')

    # Open file manager to show the batch_pdfs directory
    launch_gui(f'nautilus "{BATCH_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')


create_initial()
