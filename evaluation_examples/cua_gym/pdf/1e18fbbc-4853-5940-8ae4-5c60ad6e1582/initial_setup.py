"""
Initial Setup: Create 5 certificate PDFs in /home/user/certs/
Task ID: pdf_ro_034
Domain: pdf

Creates cert1.pdf through cert5.pdf, each a single-page certificate
with realistic layout (border, title, recipient, date).
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_034'
CERTS_DIR = f'{WORKDIR}/certs'

CERTIFICATES = [
    ('cert1.pdf', 'AWS Solutions Architect'),
    ('cert2.pdf', 'PMP'),
    ('cert3.pdf', 'CISSP'),
    ('cert4.pdf', 'Google Cloud Professional'),
    ('cert5.pdf', 'Kubernetes Administrator'),
]

CERT_DETAILS = {
    'AWS Solutions Architect': {
        'issuer': 'Amazon Web Services',
        'recipient': 'Elena Rodriguez',
        'date': 'March 15, 2024',
        'credential_id': 'AWS-SAA-2024-07842',
        'description': 'Has demonstrated expertise in designing distributed systems on AWS infrastructure.',
    },
    'PMP': {
        'issuer': 'Project Management Institute',
        'recipient': 'Elena Rodriguez',
        'date': 'June 22, 2023',
        'credential_id': 'PMI-PMP-2023-31056',
        'description': 'Has met the rigorous requirements for Project Management Professional certification.',
    },
    'CISSP': {
        'issuer': 'International Information Systems Security Certification Consortium',
        'recipient': 'Elena Rodriguez',
        'date': 'September 8, 2023',
        'credential_id': 'ISC2-CISSP-2023-88421',
        'description': 'Has demonstrated advanced knowledge in information security and risk management.',
    },
    'Google Cloud Professional': {
        'issuer': 'Google Cloud',
        'recipient': 'Elena Rodriguez',
        'date': 'January 10, 2025',
        'credential_id': 'GCP-PRO-2025-14293',
        'description': 'Has proven proficiency in designing and managing Google Cloud Platform solutions.',
    },
    'Kubernetes Administrator': {
        'issuer': 'Cloud Native Computing Foundation',
        'recipient': 'Elena Rodriguez',
        'date': 'November 5, 2024',
        'credential_id': 'CNCF-CKA-2024-62017',
        'description': 'Has demonstrated the skills required to be a Kubernetes cluster administrator.',
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


def create_certificate(filepath, cert_name):
    """Create a single-page certificate PDF with realistic formatting."""
    details = CERT_DETAILS[cert_name]

    doc = pymupdf.open()
    # Use Letter size (landscape for certificate look)
    page = doc.new_page(width=792, height=612)

    # Draw decorative border
    shape = page.new_shape()
    # Outer border
    outer = pymupdf.Rect(30, 30, 762, 582)
    shape.draw_rect(outer)
    shape.finish(color=(0.1, 0.2, 0.5), width=3)
    # Inner border
    inner = pymupdf.Rect(40, 40, 752, 572)
    shape.draw_rect(inner)
    shape.finish(color=(0.6, 0.5, 0.2), width=1.5)
    # Decorative line under title area
    shape.draw_line(pymupdf.Point(120, 180), pymupdf.Point(672, 180))
    shape.finish(color=(0.6, 0.5, 0.2), width=1, dashes="[4 2]")
    # Decorative line above footer
    shape.draw_line(pymupdf.Point(120, 470), pymupdf.Point(672, 470))
    shape.finish(color=(0.6, 0.5, 0.2), width=1, dashes="[4 2]")
    shape.commit()

    # "Certificate of Achievement" header
    page.insert_textbox(
        pymupdf.Rect(80, 60, 712, 100),
        "CERTIFICATE OF ACHIEVEMENT",
        fontsize=14,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    # Certificate name (main title)
    page.insert_textbox(
        pymupdf.Rect(80, 110, 712, 170),
        cert_name,
        fontsize=28,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    # "This certifies that"
    page.insert_textbox(
        pymupdf.Rect(80, 200, 712, 230),
        "This certifies that",
        fontsize=13,
        fontname="tiit",
        color=(0.3, 0.3, 0.3),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    # Recipient name
    page.insert_textbox(
        pymupdf.Rect(80, 240, 712, 290),
        details['recipient'],
        fontsize=24,
        fontname="tibo",
        color=(0.1, 0.1, 0.1),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    # Description
    page.insert_textbox(
        pymupdf.Rect(120, 300, 672, 370),
        details['description'],
        fontsize=12,
        fontname="tiro",
        color=(0.2, 0.2, 0.2),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    # Issuing organization
    page.insert_textbox(
        pymupdf.Rect(80, 380, 712, 410),
        f"Issued by: {details['issuer']}",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    # Date
    page.insert_textbox(
        pymupdf.Rect(80, 420, 400, 450),
        f"Date: {details['date']}",
        fontsize=10,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # Credential ID
    page.insert_textbox(
        pymupdf.Rect(400, 420, 712, 450),
        f"Credential ID: {details['credential_id']}",
        fontsize=10,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
        align=pymupdf.TEXT_ALIGN_RIGHT,
    )

    # Footer
    page.insert_textbox(
        pymupdf.Rect(80, 490, 712, 560),
        f"This certificate verifies that the holder has successfully completed all requirements\n"
        f"for the {cert_name} certification program.",
        fontsize=9,
        fontname="tiit",
        color=(0.5, 0.5, 0.5),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    doc.save(filepath)
    doc.close()


def create_initial():
    # Create certs directory
    os.makedirs(CERTS_DIR, exist_ok=True)

    # Generate each certificate
    for filename, cert_name in CERTIFICATES:
        filepath = os.path.join(CERTS_DIR, filename)
        create_certificate(filepath, cert_name)
        print(f'Created: {filepath}')

    print(f'All {len(CERTIFICATES)} certificates created in {CERTS_DIR}')

    # Open file manager to show the certs directory
    launch_gui(f'nautilus "{CERTS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
