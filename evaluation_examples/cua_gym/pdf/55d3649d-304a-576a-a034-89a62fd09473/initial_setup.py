"""
Initial Setup: Create a 12-page scanned document PDF with some pages incorrectly oriented.
Task ID: pdf_pw_024
Domain: pdf
Pages 3, 5, 7 are landscape (rotation=270), page 10 is upside down (rotation=180).
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_024'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/mixed_scans.pdf'


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

    # Page content for a realistic mixed-scan document (office/business docs)
    page_contents = [
        {
            "title": "Meridian Corp — Employee Handbook",
            "body": (
                "Welcome to Meridian Corporation. This handbook outlines our policies, "
                "benefits, and expectations for all employees. Please review each section "
                "carefully and direct questions to Human Resources.\n\n"
                "Effective Date: January 15, 2025\nRevision: 3.2"
            ),
        },
        {
            "title": "Section 1: Code of Conduct",
            "body": (
                "All employees are expected to maintain the highest standards of professional "
                "behavior. This includes respecting colleagues, protecting confidential information, "
                "and adhering to all applicable laws and regulations.\n\n"
                "Violations may result in disciplinary action up to and including termination."
            ),
        },
        {
            "title": "Section 2: Compensation & Benefits Overview",
            "body": (
                "Salary Range Table — Engineering Division\n\n"
                "Junior Engineer: $68,000 – $85,000\n"
                "Mid-Level Engineer: $90,000 – $120,000\n"
                "Senior Engineer: $125,000 – $165,000\n"
                "Principal Engineer: $170,000 – $210,000\n\n"
                "Benefits include health, dental, vision, 401(k) match up to 6%, "
                "and 20 days PTO annually."
            ),
        },
        {
            "title": "Section 3: Leave Policies",
            "body": (
                "Meridian Corp offers the following leave categories:\n\n"
                "• Vacation: 20 days per year (accrued monthly)\n"
                "• Sick Leave: 10 days per year\n"
                "• Personal Days: 3 days per year\n"
                "• Parental Leave: 12 weeks (birth/adoption)\n"
                "• Bereavement: Up to 5 days\n\n"
                "Unused vacation carries over up to 5 days into the next calendar year."
            ),
        },
        {
            "title": "Section 4: Expense Reimbursement",
            "body": (
                "Employees may submit expense reports for approved business travel, "
                "client entertainment, and professional development.\n\n"
                "Per Diem Rates (Domestic):\n"
                "  Meals: $75/day\n"
                "  Lodging: Up to $200/night\n"
                "  Mileage: $0.67/mile\n\n"
                "All receipts over $25 must be attached. Reports due within 30 days of travel."
            ),
        },
        {
            "title": "Section 5: Performance Reviews",
            "body": (
                "Performance evaluations are conducted semi-annually in March and September. "
                "Each review includes self-assessment, peer feedback, and manager evaluation.\n\n"
                "Rating Scale:\n"
                "5 — Exceptional: Consistently exceeds expectations\n"
                "4 — Strong: Frequently exceeds expectations\n"
                "3 — Satisfactory: Meets expectations\n"
                "2 — Needs Improvement: Below expectations\n"
                "1 — Unsatisfactory: Fails to meet requirements"
            ),
        },
        {
            "title": "Section 6: IT Security Policies",
            "body": (
                "All employees must complete annual cybersecurity training. Key requirements:\n\n"
                "• Passwords must be 12+ characters with mixed case, numbers, and symbols\n"
                "• Two-factor authentication is mandatory for all internal systems\n"
                "• USB drives and external storage are prohibited on company devices\n"
                "• Report suspicious emails to security@meridian-corp.com immediately\n\n"
                "Failure to comply may result in access suspension."
            ),
        },
        {
            "title": "Section 7: Remote Work Policy",
            "body": (
                "Eligible employees may work remotely up to 3 days per week with manager "
                "approval. Remote workers must:\n\n"
                "1. Maintain a dedicated workspace with reliable internet\n"
                "2. Be available during core hours (10am – 3pm local time)\n"
                "3. Attend in-person team meetings when scheduled\n"
                "4. Use company VPN for all work-related network access\n\n"
                "Remote work arrangements are reviewed quarterly."
            ),
        },
        {
            "title": "Section 8: Workplace Safety",
            "body": (
                "Meridian Corp is committed to providing a safe work environment. "
                "Emergency procedures are posted on each floor.\n\n"
                "Key Contacts:\n"
                "  Facilities Manager: David Okafor — ext. 4521\n"
                "  Safety Officer: Priya Sharma — ext. 4530\n"
                "  Emergency Line: ext. 9911\n\n"
                "Fire drills are conducted quarterly. Evacuation routes are marked in green."
            ),
        },
        {
            "title": "Section 9: Intellectual Property",
            "body": (
                "All work product created during employment is the property of Meridian Corp. "
                "This includes software, designs, documentation, and inventions.\n\n"
                "Employees must sign the Intellectual Property Assignment Agreement within "
                "the first 30 days of employment. Outside consulting or freelance work "
                "requires written approval from the VP of Engineering.\n\n"
                "Patent filing assistance is available through Legal (legal@meridian-corp.com)."
            ),
        },
        {
            "title": "Section 10: Grievance Procedure",
            "body": (
                "Employees who wish to file a complaint should follow these steps:\n\n"
                "Step 1: Discuss the issue with your direct manager\n"
                "Step 2: If unresolved, escalate to HR via the online portal\n"
                "Step 3: HR will investigate within 10 business days\n"
                "Step 4: A resolution meeting will be scheduled\n"
                "Step 5: Appeals may be directed to the Ombudsman Office\n\n"
                "Retaliation against employees who file grievances is strictly prohibited."
            ),
        },
        {
            "title": "Acknowledgment Page",
            "body": (
                "I, the undersigned, acknowledge that I have received and read the "
                "Meridian Corp Employee Handbook (Revision 3.2, January 2025).\n\n"
                "I understand that this handbook is a guide and does not constitute a "
                "contract of employment.\n\n"
                "Employee Name: ________________________________\n\n"
                "Employee Signature: ____________________________\n\n"
                "Date: _____/_____/_________\n\n"
                "Department: ________________________________"
            ),
        },
    ]

    # Pages that should be rotated (0-indexed: 2, 4, 6 → pages 3, 5, 7)
    landscape_pages = {2, 4, 6}  # rotation=270 (scanned in landscape / CCW 90°)
    upside_down_pages = {9}       # rotation=180 (scanned upside down) — page 10

    for i, content in enumerate(page_contents):
        page = doc.new_page(width=595, height=842)  # A4

        # Title
        page.insert_text(
            pymupdf.Point(72, 80),
            content["title"],
            fontsize=18,
            fontname="hebo",
            color=(0.1, 0.1, 0.3),
        )

        # Divider line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 92), pymupdf.Point(523, 92))
        shape.finish(color=(0.3, 0.3, 0.5), width=1)
        shape.commit()

        # Body text
        body_rect = pymupdf.Rect(72, 110, 523, 780)
        page.insert_textbox(
            body_rect,
            content["body"],
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Page number footer
        page.insert_text(
            pymupdf.Point(280, 820),
            f"Page {i + 1} of 12",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Apply rotation for misoriented pages
        if i in landscape_pages:
            page.set_rotation(270)
        elif i in upside_down_pages:
            page.set_rotation(180)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
