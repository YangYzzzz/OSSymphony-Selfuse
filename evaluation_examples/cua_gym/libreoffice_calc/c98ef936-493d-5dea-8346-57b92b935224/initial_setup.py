"""
Initial Setup: Create 25 PDF files in /home/user/pdf_archive/ for inventory task
Task ID: pdf_gf3_004
Domain: pdf / libreoffice_calc
"""

import os
import shlex
import subprocess
import time
import random

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_004'
ARCHIVE_DIR = f'{WORKDIR}/pdf_archive'

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


# PDF document definitions: (filename, page_count, topic/content_seed)
PDF_DOCS = [
    ("annual_report_2024.pdf", 42, "Annual Financial Report"),
    ("employee_handbook.pdf", 28, "Employee Handbook"),
    ("meeting_minutes_jan.pdf", 3, "January Board Meeting Minutes"),
    ("meeting_minutes_feb.pdf", 4, "February Board Meeting Minutes"),
    ("meeting_minutes_mar.pdf", 2, "March Board Meeting Minutes"),
    ("project_alpha_proposal.pdf", 15, "Project Alpha Business Proposal"),
    ("q1_sales_data.pdf", 8, "Q1 Sales Performance Data"),
    ("q2_sales_data.pdf", 9, "Q2 Sales Performance Data"),
    ("client_contract_apex.pdf", 12, "Client Contract - Apex Industries"),
    ("client_contract_zenith.pdf", 14, "Client Contract - Zenith Corp"),
    ("training_manual.pdf", 35, "New Hire Training Manual"),
    ("safety_guidelines.pdf", 18, "Workplace Safety Guidelines"),
    ("marketing_plan.pdf", 22, "2024 Marketing Strategy Plan"),
    ("budget_forecast.pdf", 6, "Annual Budget Forecast"),
    ("audit_findings.pdf", 11, "Internal Audit Findings Report"),
    ("policy_update_memo.pdf", 1, "Policy Update Memorandum"),
    ("vendor_evaluation.pdf", 7, "Vendor Evaluation Summary"),
    ("it_infrastructure.pdf", 25, "IT Infrastructure Assessment"),
    ("customer_survey.pdf", 16, "Customer Satisfaction Survey Results"),
    ("compliance_report.pdf", 20, "Regulatory Compliance Report"),
    ("product_catalog.pdf", 50, "Product Catalog 2024"),
    ("onboarding_checklist.pdf", 5, "New Employee Onboarding Checklist"),
    ("exit_interview_summary.pdf", 10, "Exit Interview Summary Report"),
    ("strategic_plan_2025.pdf", 33, "Strategic Plan 2025-2027"),
    ("travel_expense_policy.pdf", 13, "Travel and Expense Policy"),
]

def create_pdf(filepath, num_pages, title):
    """Create a PDF with the specified number of pages and realistic content."""
    import pymupdf

    doc = pymupdf.open()

    # Use a seed based on filename for reproducible content
    rng = random.Random(filepath)

    departments = ["Engineering", "Marketing", "Finance", "Operations", "Human Resources",
                   "Sales", "Legal", "IT", "Customer Support", "Research"]
    people = ["Sarah Chen", "Marcus Johnson", "Elena Rodriguez", "David Kim",
              "Priya Patel", "James Wilson", "Fatima Al-Hassan", "Robert Taylor",
              "Maria Santos", "Thomas Mueller"]

    for page_num in range(num_pages):
        page = doc.new_page(width=595, height=842)  # A4

        # Title on first page
        if page_num == 0:
            page.insert_text(
                pymupdf.Point(72, 80),
                title,
                fontsize=20,
                fontname="hebo",
                color=(0.1, 0.1, 0.4),
            )
            page.insert_text(
                pymupdf.Point(72, 110),
                f"Prepared by: {rng.choice(people)}",
                fontsize=11,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
            )
            page.insert_text(
                pymupdf.Point(72, 130),
                f"Department: {rng.choice(departments)}",
                fontsize=11,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
            )
            page.insert_text(
                pymupdf.Point(72, 150),
                "Date: March 15, 2024",
                fontsize=11,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
            )

            # Draw a line separator
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 170), pymupdf.Point(523, 170))
            shape.finish(color=(0.5, 0.5, 0.5), width=1)
            shape.commit()

            y_start = 200
        else:
            y_start = 72

        # Header for each page
        page.insert_text(
            pymupdf.Point(72, y_start),
            f"Section {page_num + 1}",
            fontsize=14,
            fontname="hebo",
            color=(0.2, 0.2, 0.5),
        )

        # Generate some body text
        y = y_start + 30
        paragraphs = [
            f"This section covers the key findings from the {rng.choice(departments).lower()} division's quarterly review.",
            f"According to analysis conducted by {rng.choice(people)}, the operational metrics show significant trends.",
            f"The budget allocation for this initiative was ${rng.randint(10, 500) * 1000:,}, with an expected ROI of {rng.randint(5, 25)}%.",
            f"Stakeholder feedback collected from {rng.randint(20, 150)} participants indicates broad support for the proposed changes.",
            f"Implementation timeline is projected at {rng.randint(2, 18)} months, pending resource availability.",
        ]

        for para in paragraphs:
            if y > 750:
                break
            rect = pymupdf.Rect(72, y, 523, y + 60)
            page.insert_textbox(
                rect,
                para,
                fontsize=10,
                fontname="helv",
                color=(0, 0, 0),
            )
            y += 65

        # Page footer
        page.insert_text(
            pymupdf.Point(250, 810),
            f"Page {page_num + 1} of {num_pages}",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    doc.save(filepath)
    doc.close()


def create_initial():
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    # Ensure pdf_inventory.csv does NOT exist
    csv_path = f'{WORKDIR}/pdf_inventory.csv'
    if os.path.exists(csv_path):
        os.remove(csv_path)

    for filename, page_count, title in PDF_DOCS:
        filepath = os.path.join(ARCHIVE_DIR, filename)
        create_pdf(filepath, page_count, title)
        print(f"  Created: {filename} ({page_count} pages)")

    print(f"\nCreated {len(PDF_DOCS)} PDF files in {ARCHIVE_DIR}")

    # Open file manager to show the archive directory
    launch_gui(f'nautilus "{ARCHIVE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
