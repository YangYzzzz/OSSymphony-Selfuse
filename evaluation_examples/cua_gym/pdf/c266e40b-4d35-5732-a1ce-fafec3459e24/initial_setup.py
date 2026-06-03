"""
Initial Setup: Create an AES-256 encrypted PDF at ~/Documents/scan_001.pdf
Task ID: pdf_mbc_018
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_018'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT_PDF = f'{DOCS_DIR}/scan_001.pdf'
STATUS_FILE = f'{DOCS_DIR}/encryption_status.txt'


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

    # Remove any pre-existing encryption_status.txt (must NOT exist in initial state)
    if os.path.exists(STATUS_FILE):
        os.remove(STATUS_FILE)

    # Step 1: Create a realistic multi-page PDF with content using PyMuPDF
    import pymupdf

    doc = pymupdf.open()

    # Page 1 - Cover page
    page = doc.new_page(width=612, height=792)  # Letter size
    page.insert_text(
        pymupdf.Point(180, 200),
        "CONFIDENTIAL",
        fontsize=28,
        fontname="hebo",
        color=(0.2, 0.2, 0.2),
    )
    page.insert_text(
        pymupdf.Point(140, 260),
        "Medical Benefits Claim",
        fontsize=22,
        fontname="hebo",
        color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(160, 310),
        "Claim Reference: MBC-2025-04892",
        fontsize=14,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(190, 350),
        "Date: March 15, 2025",
        fontsize=12,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(130, 400),
        "Patient: Rebecca Thornton-Haskell",
        fontsize=12,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(130, 430),
        "Provider: Lakewood Regional Medical Center",
        fontsize=12,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # Page 2 - Claim details
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 72), "Claim Summary", fontsize=18, fontname="hebo", color=(0, 0, 0))

    details = [
        "Claim Number: MBC-2025-04892",
        "Policy Number: PLH-887234-A",
        "Member ID: MTH-442918",
        "",
        "Service Date: February 28, 2025",
        "Date of Admission: February 27, 2025",
        "Date of Discharge: March 2, 2025",
        "",
        "Diagnosis Code (ICD-10): M54.5 - Low back pain",
        "Procedure Code (CPT): 99213 - Office visit, established patient",
        "",
        "Charges Submitted: $4,287.50",
        "Allowed Amount: $3,650.00",
        "Co-pay Applied: $250.00",
        "Deductible Remaining: $475.00",
        "Plan Pays (80%): $2,340.00",
        "Member Responsibility: $1,947.50",
        "",
        "Provider NPI: 1234567890",
        "Attending Physician: Dr. Jonathan M. Reeves, MD",
        "Facility: Lakewood Regional Medical Center",
        "Address: 4521 Lakewood Blvd, Suite 300, Lakewood, CA 90712",
    ]

    y = 110
    for line in details:
        page2.insert_text(pymupdf.Point(72, y), line, fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 18

    # Page 3 - Authorization and notes
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(72, 72), "Authorization & Notes", fontsize=18, fontname="hebo", color=(0, 0, 0))

    rect = pymupdf.Rect(72, 110, 540, 500)
    notes_text = (
        "Prior Authorization Number: PA-20250227-3847\n\n"
        "Clinical Notes:\n"
        "Patient presented with acute exacerbation of chronic low back pain following "
        "workplace incident on February 25, 2025. Initial evaluation revealed limited "
        "range of motion in lumbar spine with positive straight leg raise test bilateral. "
        "MRI ordered and completed on February 28, showing L4-L5 disc herniation with "
        "mild neural foraminal stenosis.\n\n"
        "Treatment Plan:\n"
        "1. Physical therapy - 3x/week for 6 weeks\n"
        "2. NSAIDs prescribed (Naproxen 500mg BID)\n"
        "3. Epidural steroid injection referral if no improvement in 4 weeks\n"
        "4. Follow-up appointment scheduled for April 10, 2025\n\n"
        "This claim has been reviewed and approved for payment under the terms of "
        "the member's benefit plan. All services rendered were deemed medically necessary "
        "based on the clinical documentation provided.\n\n"
        "Reviewed by: Sarah Kim, Claims Analyst\n"
        "Review Date: March 12, 2025\n"
        "Status: APPROVED"
    )
    page3.insert_textbox(rect, notes_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # Save unencrypted version temporarily
    temp_pdf = f'{DOCS_DIR}/_temp_scan_001.pdf'
    doc.save(temp_pdf)
    doc.close()

    # Step 2: Encrypt the PDF using pikepdf with AES-256
    import pikepdf

    pdf = pikepdf.open(temp_pdf)
    pdf.save(
        OUTPUT_PDF,
        encryption=pikepdf.Encryption(
            owner="OwnerPass2025!",
            user="ClaimView#892",
            R=6,  # AES-256 encryption
            allow=pikepdf.Permissions(
                extract=False,
                modify_annotation=False,
                print_lowres=True,
                print_highres=True,
                modify_form=False,
                modify_other=False,
                modify_assembly=False,
            ),
        ),
    )

    # Clean up temp file
    os.remove(temp_pdf)
    print(f'Encrypted PDF created: {OUTPUT_PDF}')

    # Verify encryption
    test_pdf = pikepdf.open(OUTPUT_PDF, password="ClaimView#892")
    enc_details = test_pdf.encryption
    print(f'Encryption verified - Method: {enc_details}')
    test_pdf.close()

    # GUI-ready startup: open file manager to Documents directory
    launch_gui(f'nautilus "{DOCS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
