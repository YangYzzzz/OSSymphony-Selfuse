"""
Initial Setup: Create a 10-page certificate of completion PDF
Task ID: pdf_pw_035
Domain: pdf

Creates /home/user/Documents/certificate_batch.pdf with 10 pages,
each containing a certificate of completion for a different recipient.
Page size: Letter (612x792). No borders or decorative elements.
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCUMENTS = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_pw_035'
OUTPUT = f'{DOCUMENTS}/certificate_batch.pdf'

# Letter page dimensions in points
PAGE_W, PAGE_H = 612, 792


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


# Certificate recipients with realistic details
recipients = [
    {"name": "Sarah Chen", "course": "Advanced Data Analytics", "date": "March 15, 2025", "id": "CERT-2025-0471"},
    {"name": "Marcus Johnson", "course": "Project Management Professional", "date": "March 22, 2025", "id": "CERT-2025-0482"},
    {"name": "Elena Rodriguez", "course": "Cloud Architecture Fundamentals", "date": "April 3, 2025", "id": "CERT-2025-0495"},
    {"name": "David Kim", "course": "Machine Learning Engineering", "date": "April 10, 2025", "id": "CERT-2025-0503"},
    {"name": "Priya Patel", "course": "Cybersecurity Essentials", "date": "April 18, 2025", "id": "CERT-2025-0517"},
    {"name": "James O'Brien", "course": "Full Stack Web Development", "date": "April 25, 2025", "id": "CERT-2025-0528"},
    {"name": "Aisha Mohammed", "course": "UX Design Principles", "date": "May 2, 2025", "id": "CERT-2025-0536"},
    {"name": "Thomas Weber", "course": "DevOps and CI/CD Pipelines", "date": "May 9, 2025", "id": "CERT-2025-0544"},
    {"name": "Mei-Ling Wu", "course": "Business Intelligence Reporting", "date": "May 16, 2025", "id": "CERT-2025-0559"},
    {"name": "Carlos Mendez", "course": "Agile Software Development", "date": "May 23, 2025", "id": "CERT-2025-0567"},
]


def create_certificate_page(doc, recipient):
    """Create a single certificate page with realistic content."""
    page = doc.new_page(width=PAGE_W, height=PAGE_H)

    # Title: "Certificate of Completion"
    page.insert_text(
        pymupdf.Point(PAGE_W / 2 - 150, 160),
        "Certificate of Completion",
        fontsize=28,
        fontname="tibo",  # Times-Bold
        color=(0.1, 0.1, 0.4),  # dark navy
    )

    # Subtitle line
    page.insert_text(
        pymupdf.Point(PAGE_W / 2 - 110, 200),
        "This certificate is awarded to",
        fontsize=14,
        fontname="tiit",  # Times-Italic
        color=(0.3, 0.3, 0.3),
    )

    # Recipient name (large, prominent)
    name = recipient["name"]
    # Center the name roughly
    name_width_est = len(name) * 10
    page.insert_text(
        pymupdf.Point(PAGE_W / 2 - name_width_est / 2, 260),
        name,
        fontsize=24,
        fontname="tibo",
        color=(0.0, 0.0, 0.0),
    )

    # Horizontal line under name
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(150, 275), pymupdf.Point(462, 275))
    shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
    shape.commit()

    # Course description
    page.insert_text(
        pymupdf.Point(PAGE_W / 2 - 130, 320),
        "for successful completion of the course",
        fontsize=12,
        fontname="tiro",  # Times-Roman
        color=(0.3, 0.3, 0.3),
    )

    # Course name
    course = recipient["course"]
    course_width_est = len(course) * 7.5
    page.insert_text(
        pymupdf.Point(PAGE_W / 2 - course_width_est / 2, 360),
        course,
        fontsize=18,
        fontname="tiit",
        color=(0.15, 0.15, 0.5),
    )

    # Organization info
    page.insert_text(
        pymupdf.Point(PAGE_W / 2 - 95, 420),
        "Offered by TechForward Institute",
        fontsize=12,
        fontname="tiro",
        color=(0.3, 0.3, 0.3),
    )

    page.insert_text(
        pymupdf.Point(PAGE_W / 2 - 85, 445),
        "Professional Development Division",
        fontsize=10,
        fontname="tiro",
        color=(0.4, 0.4, 0.4),
    )

    # Date of completion
    page.insert_text(
        pymupdf.Point(120, 540),
        f"Date of Completion: {recipient['date']}",
        fontsize=11,
        fontname="tiro",
        color=(0.2, 0.2, 0.2),
    )

    # Certificate ID
    page.insert_text(
        pymupdf.Point(120, 565),
        f"Certificate ID: {recipient['id']}",
        fontsize=10,
        fontname="cour",  # Courier
        color=(0.4, 0.4, 0.4),
    )

    # Signature lines
    # Left signature
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(120, 660), pymupdf.Point(280, 660))
    shape2.finish(color=(0.3, 0.3, 0.3), width=0.5)
    shape2.commit()

    page.insert_text(
        pymupdf.Point(145, 680),
        "Dr. Amanda Foster",
        fontsize=10,
        fontname="tibo",
        color=(0.2, 0.2, 0.2),
    )
    page.insert_text(
        pymupdf.Point(155, 695),
        "Program Director",
        fontsize=9,
        fontname="tiro",
        color=(0.4, 0.4, 0.4),
    )

    # Right signature
    shape3 = page.new_shape()
    shape3.draw_line(pymupdf.Point(350, 660), pymupdf.Point(500, 660))
    shape3.finish(color=(0.3, 0.3, 0.3), width=0.5)
    shape3.commit()

    page.insert_text(
        pymupdf.Point(370, 680),
        "Robert S. Harrington",
        fontsize=10,
        fontname="tibo",
        color=(0.2, 0.2, 0.2),
    )
    page.insert_text(
        pymupdf.Point(385, 695),
        "Chief Academic Officer",
        fontsize=9,
        fontname="tiro",
        color=(0.4, 0.4, 0.4),
    )


def create_initial():
    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = pymupdf.open()

    for recipient in recipients:
        create_certificate_page(doc, recipient)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {len(recipients)}')

    # Open the PDF in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
